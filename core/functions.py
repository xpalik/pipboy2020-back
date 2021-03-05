from pythonping import ping
from pysnmp.hlapi import *
import socket

community_string = "public"
port_snmp = 161
OID_sysName = ''
deviceOptions = {}


def snmp_getcmd(community, ip, port, OID):
    return (getCmd(SnmpEngine(),
                   CommunityData(community),
                   UdpTransportTarget((ip, port)),
                   ContextData(),
                   ObjectType(ObjectIdentity(OID))))


def snmp_get_next(community, ip, port, OID):
    errorIndication, errorStatus, errorIndex, varBinds = next(snmp_getcmd(community, ip, port, OID))
    for name, val in varBinds:
        return (val.prettyPrint())


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


def snmp_get(ip, oid):
    return snmp_get_next(community_string, ip, port_snmp, oid)


def check_snmp(ip):
    answer = snmp_get_next(community_string, ip, port_snmp, '.1.3.6.1.2.1.1.1.0')
    if answer is not None:
        return True
    else:
        return False
