from functions import check_ping, check_snmp, check_socket, snmp_get, type_by_string
import asyncio
import time


class InitDevice:
    serivce_dict = {
        'ping': {'icmp': 0, 'status': False},
        'telnet': {'tcp_port': 23, 'status': False},
        'web': {'tcp_port': 80, 'status': False},
        'winbox': {'tcp_port': 8291, 'status': False},
        'ros_api': {'tcp_port': 8728, 'status': False},
        'ssh': {'tcp_port': 22, 'status': False},
        'snmp': {'snmp': 161, 'status': False}
        }

    def __init__(self, ip, **kwargs):
        self.ip = ip
        self.online = False
        if 'type' in kwargs:
            self.type = kwargs['type']
        else:
            self.type = 'other'
        for service in self.serivce_dict.keys():
            if service in kwargs:
                self.serivce_dict[service]['status'] = kwargs[service]

    def is_online(self):
        for service in self.serivce_dict.items():
            if service[1]['status']:
                if service[0] == 'ping':
                    if check_ping(self.ip):
                        self.online = True
                        return True
                if service[0] == 'snmp':
                    if check_snmp(self.ip):
                        self.online = True
                        return True
                if 'tcp_port' in service[1]:
                    if check_socket(self.ip, service[1]['tcp_port']):
                        self.online = True
                        return True
        return False

    def check_services(self):
        for service in self.serivce_dict.items():
            if 'tcp_port' in service[1]:
                self.serivce_dict[service[0]]['status'] = check_socket(self.ip, service[1]['tcp_port'])
            if service[0] == 'snmp':
                self.serivce_dict[service[0]]['status'] = check_snmp(self.ip)
            if service[0] == 'ping':
                self.serivce_dict[service[0]]['status'] = check_ping(self.ip)
            if 'status' in self.serivce_dict[service[0]]:
                if self.serivce_dict[service[0]]['status']:
                    self.online = True

    def type_define(self):
        if self.is_online():
            snmp_answer = snmp_get(self.ip, '.1.3.6.1.2.1.1.1.0')
            if snmp_answer is not None:
                self.type = type_by_string(snmp_answer[1])
                if self.type == 'DES3200C':
                    return DES3200C(self.ip)

    def debug_print(self):
        print("ip: %s, type: %s, online: %s" % (self.ip, self.type, self.online))
        for service in self.serivce_dict.items():
            print(service)


class DES3200C(InitDevice):
    def check_firmware(self):
        if self.is_online():
            print('its work')


start_time = time.time()
a = InitDevice('192.168.105.3', ping=True, snmp=True)
# a.check_services()
a.is_online()
a = a.type_define()
a.check_firmware()
a.debug_print()

print("--- %s seconds ---" % (time.time() - start_time))
