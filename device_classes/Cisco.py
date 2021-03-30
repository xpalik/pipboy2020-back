from core.functions import *
from core.DataClass import DataClass


class Cisco(DataClass):
    def __init__(self, ip, **kwargs):
        super().__init__(ip, **kwargs)

    def check_all_snmp_properties(self):
        self.properties['snmp_name'] = snmp_get(self.ip, '.1.3.6.1.2.1.1.1.0')[1]
        # self.check_fdb_table()
        self.check_arp_table()

    def check_arp_table(self):
        if self.is_online():
            if_names_ans = snmp_walk(self.ip, '.1.3.6.1.2.1.31.1.1.1.1')
            if_names = {}
            for item in if_names_ans:
                if_names[item[0].split('1.3.6.1.2.1.31.1.1.1.1.')[1]] = item[1]
            snmp_ans = snmp_walk(self.ip, '.1.3.6.1.2.1.3.1.1.2')
            for row in snmp_ans:
                if_name = if_names[row[0].split('1.3.6.1.2.1.3.1.1.2.')[1].split('.')[0]]
                ip = row[0].split(
                    '1.3.6.1.2.1.3.1.1.2.'
                    + row[0].split('1.3.6.1.2.1.3.1.1.2.')[1].split('.')[0]
                    + '.1.')[1]
                mac = row[1].split('x')[-1]
                self.arp_entry.append([if_name[0:99], mac[0:11], ip[0:14]])

    def check_fdb_table(self):
        pass
        # if self.is_online():
        #     snmp_raw = snmp_walk(self.ip, '.1.3.6.1.2.1.17.7.1.2.2.1.2')
        #     for row in snmp_raw:
        #         vlan, _, mac_raw = (row[0].partition('1.3.6.1.2.1.17.7.1.2.2.1.2.')[2].partition('.'))
        #
        #         mac = ''
        #         for octet in mac_raw.split('.'):
        #             if int(octet) < 16:
        #                 mac = mac + '0' + str(hex(int(octet)).split('x')[-1])
        #             else:
        #                 mac = mac + str(hex(int(octet))[2:].split('x')[-1])
        #
        #         self.mac_table.append([vlan, mac, row[1]])

# a = Cisco('192.168.105.254', snmp=True, ping=True)
# a.check_fdb_table()
# a.debug_print()