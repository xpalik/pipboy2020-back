from core.ServiceChecker import ServiceChecker
from core.functions import mssql_update_dict, mssql_select_dict
import pyodbc
import accouts


class DataClass(ServiceChecker):
    def __init__(self, ip, **kwargs):
        super().__init__(ip, **kwargs)
        self.properties = {}
        self.mac_table = []
        self.arp_entry = []

    def debug_print(self):
        super().debug_print()
        print('==> properties')
        for prop in self.properties.items():
            print(prop)
        i = 0
        for item in self.mac_table:
            print(item)
            i += 1
            if i > 5:
                print('and more ...')
                break
        i = 0
        for item in self.arp_entry:
            print(item)
            i += 1
            if i > 5:
                print('and more...')
                break

    def mssql_update(self):
        super(DataClass, self).mssql_update()
        if self.online:
            mssql_update_dict('device_properties', self.ip, self.properties)

    def mssql_select(self):
        self.properties.update(mssql_select_dict('device_properties', self.ip))
