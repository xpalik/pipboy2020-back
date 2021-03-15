from core.ServiceChecker import ServiceChecker
from core.functions import *


class RouterOS(ServiceChecker):
    def __init__(self, ip, **kwargs):
        super().__init__(ip, **kwargs)
        self.type = 'RouterOS'
        self.properties = {}
        self.mac_table = []
        self.arp_entry = []

    def check_all_snmp_properties(self):
        self.check_sntp()
        self.check_firmware()
        self.check_fdb_table()
        self.check_arp_table()
        self.check_route_table()
        self.find_root_port()

    def check_sntp(self):
        resource = '/system/ntp/client'
        answer = routeros_api_get_resource(self.ip, resource, 'print')
        for prop in answer[0].items():
            self.properties[resource + '/' + prop[0]] = prop[1]

    def check_fdb_table(self):
        answer = routeros_api_get_resource(self.ip, '/interface/bridge/host', 'print')
        for item in answer:
            self.mac_table.append([
                item['bridge'],
                ''.join(item['mac-address'].lower().split(':')),
                item['on-interface']
            ])

    def check_arp_table(self):
        answer = routeros_api_get_resource(self.ip, '/ip/arp', 'print')
        for item in answer:
            self.arp_entry.append([
                item['interface'],
                ''.join(item['mac-address'].lower().split(':')),
                item['address']])

    def check_route_table(self):
        pass

    def find_root_port(self):
        pass

    def check_firmware(self):
        resource = '/system/package'
        answer = routeros_api_get_resource(self.ip, resource, 'print')
        for item in answer:
            if 'bundle' not in item:
                self.properties[resource + '/' + item['name']] = item['version']

    def debug_print(self):
        super().debug_print()
        print('== RouterOS - properties')
        for prop in self.properties.items():
            print(prop)
        # for item in self.mac_table:
        #     print(item)
        # for item in self.arp_entry:
        #     print(item)