from core.DataClass import DataClass


class Blank(DataClass):
    def __init__(self, ip, **kwargs):
        super().__init__(ip, **kwargs)
        self.type = 'Blank'

    def check_all_snmp_properties(self):
        pass
