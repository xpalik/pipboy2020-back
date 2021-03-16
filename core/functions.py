from pythonping import ping
from pysnmp.hlapi import *
import socket
import routeros_api
import asyncio
import aioping
import aiosnmp
from accouts import RouterOSAccouts

community_string = "public"
port_snmp = 161
OID_sysName = ''
deviceOptions = {}


async def snmp_get_async(ip, oid):
    try:
        async with aiosnmp.Snmp(host=ip, port=port_snmp, community=community_string) as snmp:
            for res in await snmp.get(oid):
                return [res.oid, str(res.value).split('\'')[1]]
    except aiosnmp.exceptions.SnmpTimeoutError:
        return None


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
        # print(ip, ' -> SNMP engine error: ', error_indication)
        return [oid, None]
    else:
        if error_status:  # SNMP agent errors
            # print(
            #     ' -> %s at %s' % (error_status.prettyPrint(), var_binds[int(error_index) - 1] if error_index else '?'))
            return [oid, None]
        else:
            for varBind in var_binds:  # SNMP response contents
                answer = [x.prettyPrint() for x in varBind]
                if answer[1] == 'No Such Object currently exists at this OID':
                    return [oid, None]
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
            # print(ip, ' -> SNMP walk engine error: ', errorIndication)
            break
        elif errorStatus:
            # print(' -> %s at %s' % (errorStatus.prettyPrint(),
            #                         errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            break
        else:
            for varBind in varBinds:
                answer.append([x.prettyPrint() for x in varBind])
    if not answer:
        return None
    else:
        return answer


async def check_ping_async(ip):
    try:
        delay = await aioping.ping(ip)
        return True
    except TimeoutError:
        return False


def check_ping(ip):
    if ping(ip).success():
        return True
    else:
        return False


async def check_socket_async(ip, port):
    try:
        reader, writer = await asyncio.open_connection(ip, port)
        writer.close()
        return True
    except OSError:
        return False


def check_socket(ip, port):
    sock_stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if sock_stream.connect_ex((ip, port)) == 0:
        sock_stream.close()
        return True
    else:
        sock_stream.close()
        return False


async def check_snmp_async(ip):
    answer = await snmp_get_async(ip, '.1.3.6.1.2.1.1.1.0')
    if answer is not None:
        return True
    else:
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
