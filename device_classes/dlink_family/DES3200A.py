from device_classes.dlink_family.Dlink3200 import Dlink3200
from core.functions import *


class DES3200A(Dlink3200):
    def __init__(self, ip, **kwargs):
        super().__init__(ip, **kwargs)
        self.type = 'DES3200A'

    def check_all_snmp_properties(self):
        super().check_all_snmp_properties()
        self.check_firmware()

    def check_firmware(self):
        if self.is_online():
            self.properties['firmware_slot1'] = snmp_get(self.ip, '.1.3.6.1.4.1.171.12.1.2.7.1.2.1')[1]
            self.properties['firmware_slot2'] = snmp_get(self.ip, '.1.3.6.1.4.1.171.12.1.2.7.1.2.2')[1]
            if self.properties['firmware_slot1'][0] == '*':
                self.properties['firmware_boot'] = 'slot1'
            elif self.properties['firmware_slot2'][0] == '*':
                self.properties['firmware_boot'] = 'slot2'

