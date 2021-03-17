import ipaddress
import time
from core.InitDevice import InitDevice
import asyncio

subnets_array = [ipaddress.ip_network('192.168.136.192/28')
# subnets_array = [ipaddress.ip_network('192.168.136.202/32')
                 ]


async def scanner():
    to_scan = []
    tasks = []
    for subnet in subnets_array:
        for ip in list(subnet.hosts()):
            to_scan.append(InitDevice(str(ip)))
            tasks.append(asyncio.create_task(to_scan[-1].check_services()))
    for task in tasks:
        await task
    for item in to_scan:
        item = item.type_define()
        item.check_all_snmp_properties()
        item.debug_print()


start_time = time.time()
asyncio.run(scanner())

print("--- %s seconds ---" % (time.time() - start_time))
