from core.Dlink3200 import Dlink3200
from core.functions import *


class DES3200C(Dlink3200):
    def __init__(self, ip, **kwargs):
        super().__init__(ip, **kwargs)
        self.type = 'DES3200C'

    def check_all_snmp_properties(self):
        super().check_all_snmp_properties()
        self.check_firmware()

    def check_firmware(self):
        if self.is_online():
            self.properties['firmware'] = snmp_get(self.ip, '.1.3.6.1.4.1.171.12.1.2.7.1.2.1')[1]

