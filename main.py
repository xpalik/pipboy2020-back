import time
from core.InitDevice import InitDevice
import asyncio

if __name__ == '__main__':
    start_time = time.time()
    a = InitDevice('192.168.103.88')
    # a = InitDevice('192.168.103.245', snmp=True)
    print(a.serivces)
    a = a.type_define()
    asyncio.run(a.check_services())
    a.check_all_snmp_properties()
    a.debug_print()

    
    print("--- %s seconds ---" % (time.time() - start_time))