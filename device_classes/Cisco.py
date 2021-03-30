from core.functions import *
from core.DataClass import DataClass


class Cisco(DataClass):
    def __init__(self, ip, **kwargs):
        super().__init__(ip, **kwargs)

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
                self.arp_entry.append([if_name, mac, ip])
