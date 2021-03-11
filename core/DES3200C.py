from core.ServiceChecker import ServiceChecker
from core.functions import *
import time


class DES3200C(ServiceChecker):
    def __init__(self, ip, **kwargs):
        super().__init__(ip, **kwargs)
        self.type = 'DES3200C'
        self.properties = {}
        self.fdb = []

    def check_all_snmp_properties(self):
        self.check_firmware()
        self.check_sntp()

    def check_firmware(self):
        if self.is_online():
            self.properties['Firmware'] = snmp_get(self.ip, '.1.3.6.1.4.1.171.12.1.2.7.1.2.1')[1]

    def check_sntp(self):
        if self.is_online():
            self.properties['system_ntp'] = snmp_get(self.ip, '1.3.6.1.4.1.171.12.10.11.3.0')[1]
            self.properties['system_time'] = snmp_get(self.ip, '1.3.6.1.4.1.171.12.10.10.1.0')[1]
            self.properties['system_time_scanned_at'] = time.ctime()

    def check_fdb_table(self):
        if self.is_online():
            snmp_walk(self.ip, '.1.3.6.1.2.1.17.7.1.2.2.1.2')

    def debug_print(self):
        super().debug_print()
        print('== DES3200C - properties')
        for prop in self.properties.items():
            print(prop)
        # for fdb in self.fdb.items():
        #     print(fdb)


