from core.Dlink3200 import Dlink3200
from core.functions import *


class DGS3100(Dlink3200):
    def __init__(self, ip, **kwargs):
        super().__init__(ip, **kwargs)
        self.type = 'DGS3100'

    def check_sntp(self):
        pass

    def check_arp_table(self):
        pass

    def check_route_table(self):
        pass


