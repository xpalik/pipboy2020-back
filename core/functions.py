from pythonping import ping
from pysnmp.hlapi import *
import socket
import routeros_api
import asyncio
from accouts import RouterOSAccouts

community_string = "public"
port_snmp = 161
OID_sysName = ''
deviceOptions = {}


def snmp_get(ip, oid):
    iterator = getCmd(SnmpEngine(),
                      CommunityData(community_string),
                      UdpTransportTarget((ip, port_snmp)),
                      ContextData(),
                      # ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
                      ObjectType(ObjectIdentity(oid)),
                      lookupMib=False
                      # lexicographicMode=False
                      )

    error_indication, error_status, error_index, var_binds = next(iterator)

    if error_indication:  # SNMP engine errors
        print(ip, ' -> SNMP engine error: ', error_indication)
        return None
    else:
        if error_status:  # SNMP agent errors
            print(
                ' -> %s at %s' % (error_status.prettyPrint(), var_binds[int(error_index) - 1] if error_index else '?'))
            return None
        else:
            for varBind in var_binds:  # SNMP response contents
                answer = [x.prettyPrint() for x in varBind]
                if answer[1] == 'No Such Object currently exists at this OID':
                    return None
                else:
                    return answer


def snmp_walk(ip, root_oid):
    answer = []
    for errorIndication, errorStatus, \
        errorIndex, varBinds in bulkCmd(
        SnmpEngine(),
        CommunityData(community_string),
        UdpTransportTarget((ip, port_snmp)),
        ContextData(),
        0, 50,  # GETBULK specific: request up to 50 OIDs in a single response
        ObjectType(ObjectIdentity(root_oid)),
        lookupMib=False, lexicographicMode=False):

        if errorIndication:
            print(ip, ' -> SNMP walk engine error: ', errorIndication)
            break
        elif errorStatus:
            print(' -> %s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            break
        else:
            for varBind in varBinds:
                answer.append([x.prettyPrint() for x in varBind])
    if not answer:
        return None
    else:
        return answer


def check_ping(ip):
    if ping(ip).success():
        return True
    else:
        return False


async def check_socket(ip, port):
    try:
        reader, writer = await asyncio.open_connection(ip, port)
        writer.close()
        print(reader, writer)
        return True
    except OSError:
        return False


def check_snmp(ip):
    answer = snmp_get(ip, '.1.3.6.1.2.1.1.1.0')
    if answer is not None:
        return True
    else:
        return False


def type_by_string(snmp_string):
    if str(snmp_string)[0:8] == 'RouterOS':
        return 'RouterOS'
    elif str(snmp_string)[0:8] == 'DES-3200':
        return 'DES3200C'
    elif str(snmp_string)[0:15] == 'D-Link DES-3200':
        return 'DES3200A'
    elif str(snmp_string)[0:13] == 'DGS-3100-24TG':
        return 'DGS3100'
    elif str(snmp_string) != 'None':
        return 'other'
    else:
        return 'other'


def routeros_api_get_resource(ip, resource, call):
    for username, password in RouterOSAccouts:
        try:
            connection = routeros_api.RouterOsApiPool(ip, username=username, password=password)
            api = connection.get_api()
            return api.get_resource(resource).call(call)
        except routeros_api.exceptions.RouterOsApiCommunicationError:
            pass
    return False
