from functions import check_ping, check_snmp, check_socket


class InitDevice:
    online = False
    serivce_dict = {
        'ping': {'icmp': 0},
        'telnet': {'tcp_port': 23},
        'web': {'tcp_port': 80},
        'winbox': {'tcp_port': 8291},
        'ros_api': {'tcp_port': 8728},
        'ssh': {'tcp_port': 22},
        'snmp': {'snmp': 161}
        }

    def __init__(self, ip, **kwargs):
        self.ip = ip
        self.online = False
        for service in self.serivce_dict.keys():
            if service in kwargs:
                self.serivce_dict[service]['status'] = kwargs[service]

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

    def debug_print(self):
        print("ip: %s, online: %s" % (self.ip, self.online))
        for service in self.serivce_dict.items():
            print(service)


a = InitDevice('192.168.105.3', telnet=True, snmp=False)
a.check_services()
print('==')
a.debug_print()
