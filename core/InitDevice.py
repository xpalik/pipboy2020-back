from core.ServiceChecker import ServiceChecker
from core.DES3200C import DES3200C
from core.DES3200A import DES3200A
from core.DGS3100 import DGS3100
from core.RouterOS import RouterOS
from core.functions import *


class InitDevice(ServiceChecker):

    def type_define(self):
        if self.is_online():
            snmp_answer = snmp_get(self.ip, '.1.3.6.1.2.1.1.1.0')
            if snmp_answer is not None:
                self.type = type_by_string(snmp_answer[1])
                if self.type == 'DES3200C':
                    return DES3200C(self.ip, **self.serivces)
                if self.type == 'DES3200A':
                    return DES3200A(self.ip, **self.serivces)
                if self.type == 'DGS3100':
                    return DGS3100(self.ip, **self.serivces)
                if self.type == 'RouterOS':
                    return RouterOS(self.ip, **self.serivces)
