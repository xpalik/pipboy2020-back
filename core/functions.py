from pythonping import ping
from pysnmp.hlapi import *
import socket

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


def check_socket(ip, port):
    sock_stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if sock_stream.connect_ex((ip, port)) == 0:
        sock_stream.close()
        return True
    else:
        sock_stream.close()
        return False


def check_snmp(ip):
    answer = snmp_get(ip, '.1.3.6.1.2.1.1.1.0')
    if answer is not None:
        return True
    else:
        return False
