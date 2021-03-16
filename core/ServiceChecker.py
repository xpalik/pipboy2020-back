from core.functions import *


class ServiceChecker:
    service_tcp_ports = {
        'ping': None,
        'telnet': 23,
        'web': 80,
        'winbox': 8291,
        'ros_api': 8728,
        'ssh': 22,
        'snmp': None
    }

    def __init__(self, ip, **kwargs):
        self.ip = ip
        self.online = False
        if 'type' in kwargs:
            self.type = kwargs['type']
        else:
            self.type = 'other'
        self.serivces = {
            'telnet': False,
            'web': False,
            'winbox': False,
            'ros_api': False,
            'ssh': False,
            'ping': False,
            'snmp': False
        }
        for service in self.serivces.keys():
            if service in kwargs:
                self.serivces[service] = kwargs[service]

    def is_online(self):
        for service in self.serivces.items():
            if service[1]:
                if service[0] == 'ping':
                    if check_ping(self.ip):
                        self.online = True
                        return True
                elif service[0] == 'snmp':
                    if check_snmp(self.ip):
                        self.online = True
                        return True
                elif ServiceChecker.service_tcp_ports[service[0]]:
                    if check_socket(self.ip, ServiceChecker.service_tcp_ports[service[0]]):
                        self.online = True
                        return True
        return False

    async def check_services(self):
        tasks = []
        for service in self.serivces.keys():
            if ServiceChecker.service_tcp_ports[service]:
                tasks.append([service,
                              asyncio.create_task(
                                  check_socket_async(self.ip, ServiceChecker.service_tcp_ports[service]))])
            if service == 'snmp':
                self.serivces[service] = check_snmp(self.ip)
            if service == 'ping':
                self.serivces[service] = check_ping(self.ip)
        for task in tasks:
            self.serivces[task[0]] = await task[1]

    def debug_print(self):
        print('==================================')
        print("====> ip: %s, type: %s, online: %s" % (self.ip, self.type, self.online))
        for service in self.serivces.items():
            print(service)
