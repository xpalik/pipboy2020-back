from core.DataClass import DataClass
from core.functions import *
import time


class Dlink3200(DataClass):
    def __init__(self, ip, **kwargs):
        super().__init__(ip, **kwargs)

    def check_all_snmp_properties(self):
        self.properties['snmp_name'] = snmp_get(self.ip, '.1.3.6.1.2.1.1.1.0')[1]
        self.check_sntp()
        self.check_fdb_table()
        self.check_arp_table()
        self.check_route_table()
        self.find_root_port()

    def check_sntp(self):
        if self.is_online():
            self.properties['system_ntp'] = snmp_get(self.ip, '1.3.6.1.4.1.171.12.10.11.3.0')[1]
            self.properties['system_time'] = snmp_get(self.ip, '1.3.6.1.4.1.171.12.10.10.1.0')[1]
            self.properties['system_time_scanned_at'] = time.ctime()

    def check_fdb_table(self):
        if self.is_online():
            snmp_raw = snmp_walk(self.ip, '.1.3.6.1.2.1.17.7.1.2.2.1.2')
            for row in snmp_raw:
                vlan, _, mac_raw = (row[0].partition('1.3.6.1.2.1.17.7.1.2.2.1.2.')[2].partition('.'))

                mac = ''
                for octet in mac_raw.split('.'):
                    if int(octet) < 16:
                        mac = mac + '0' + str(hex(int(octet)).split('x')[-1])
                    else:
                        mac = mac + str(hex(int(octet))[2:].split('x')[-1])

                self.mac_table.append([vlan, mac, row[1]])

    def check_arp_table(self):
        if self.is_online():
            snmp_interface = snmp_walk(self.ip, '.1.3.6.1.2.1.4.22.1.1')
            snmp_macs = snmp_walk(self.ip, '.1.3.6.1.2.1.4.22.1.2')
            snmp_ips = snmp_walk(self.ip, '.1.3.6.1.2.1.4.22.1.3')
            snmp_type = snmp_walk(self.ip, '.1.3.6.1.2.1.4.22.1.4')
            for i in range(0, len(snmp_macs) - 1):
                mac = snmp_macs[i][1].split('x')[-1]
                if snmp_type[i][1] == '3':
                    self.arp_entry.append([
                        snmp_interface[i][1],
                        mac,
                        snmp_ips[i][1]
                    ])

    def check_route_table(self):
        if self.is_online():
            self.properties['default_gateway'] = snmp_get(self.ip, '.1.3.6.1.2.1.4.21.1.7.0.0.0.0')[1]

    def find_root_port(self):
        try:
            gateway_mac = False
            for arp_item in self.arp_entry:
                if arp_item[2] == self.properties['default_gateway']:
                    gateway_mac = arp_item[1]
            if gateway_mac:
                for mac_table_item in self.mac_table:
                    if mac_table_item[1] == gateway_mac:
                        self.properties['root_port'] = mac_table_item[2]
                        self.properties['root_vlan'] = mac_table_item[0]
        except KeyError:
            self.properties['root_port'] = False
            self.properties['root_vlan'] = False
