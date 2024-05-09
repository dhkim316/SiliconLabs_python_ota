import asyncio
from bleak import BleakScanner

async def run():
    devices = await BleakScanner.discover(timeout=3)
    for device in devices:
        print("Device ({}): {}".format(device.address, device.name))

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
