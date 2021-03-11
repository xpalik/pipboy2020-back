import time
from core.InitDevice import InitDevice

if __name__ == '__main__':
    start_time = time.time()
    a = InitDevice('192.168.105.3')
    a.check_services()
    a.debug_print()
    a.is_online()
    a = a.type_define()
    a.check_all_snmp_properties()
    a.debug_print()
    
    print("--- %s seconds ---" % (time.time() - start_time))