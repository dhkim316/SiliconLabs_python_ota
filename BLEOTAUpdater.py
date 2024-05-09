import os
import asyncio
from bleak import BleakScanner, BleakClient

class BLEOTAUpdater:
    OTA_SVC_UUID = "1d14d6ee-fd63-4fa1-bfa4-8f47b42119f0"
    OTA_SVC_CHAR_CONTROL = "f7bf3564-fb6d-4e53-88a4-5e37e0326063"
    OTA_SVC_CHAR_DATA = "984227f3-34fc-4045-a5d0-2c581f81a153"
        
    def __init__(self, device_identifier, file_path, label):
        self.device_identifier = device_identifier
        self.file_path = file_path
        self.label = label
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    async def update_firmware(self):
        # Automatically decide the method based on the type of identifier provided
        if '-' in self.device_identifier or ':' in self.device_identifier:
            device = await self.find_device_by_identifier(self.device_identifier, by_name=False)
        else:
            device = await self.find_device_by_identifier(self.device_identifier, by_name=True)
        
        if not device:
            self.label.config(text="Device not found.")
            return
        self.label.config(text=f"Found device: {device.name} ({device.address})")
        
        async with BleakClient(device.address) as client:
            await self.ensure_ota_mode(client)

    async def find_device_by_identifier(self, identifier, by_name=False, timeout=0.5, retries=3):
        attempt = 0
        while attempt < retries:
            devices = await BleakScanner.discover(timeout=timeout)
            for device in devices:
                if by_name :
                    print(device.name)
                    if identifier == device.name:
                        self.label.config(text=f"Device found on attempt {attempt + 1}: {device.name} ({device.address})")
                        return device
                elif not by_name and identifier.upper() == device.address.upper():
                    self.label.config(text=f"Device found on attempt {attempt + 1}: {device.name} ({device.address})")
                    return device
            self.label.config(text=f"Device not found on attempt {attempt + 1}. Retrying...")
            attempt += 1
            await asyncio.sleep(1)
        self.label.config(text="Failed to find device after maximum retries.")
        return None    
    
    async def ensure_ota_mode(self, client):
        services = client.services
        svc, ctrl_char, data_char = self.find_ota_service_and_chars(services)
        if data_char is None:
            self.label.config(text="Entering DFU mode...")
            await client.write_gatt_char(ctrl_char, b"\x00", response=True)
            await client.disconnect()
            await asyncio.sleep(1)  # Give time for the device to reset into DFU mode (1sec)
            await client.connect()
            # services = await client.get_services()
            await asyncio.sleep(1)  # Give time for the device to get srvice (1sec)
            services = client.services
            svc, ctrl_char, data_char = self.find_ota_service_and_chars(services)
            if data_char is None:
                self.label.config(text="Could not enter DFU mode")
                return
        self.label.config(text="Device is in DFU mode.")
        await self.write_firmware(client, ctrl_char, data_char)
        
    def find_ota_service_and_chars(self, services):
        svc = None
        ctrl_char = None
        data_char = None
        for svc in filter(lambda s: s.uuid == self.OTA_SVC_UUID, services):
            ctrl_char = svc.get_characteristic(self.OTA_SVC_CHAR_CONTROL)
            data_char = svc.get_characteristic(self.OTA_SVC_CHAR_DATA)
            if data_char is not None:
                break
        return (svc, ctrl_char, data_char)
    
    async def write_firmware(self, client, ctrl_char, data_char):
        self.label.config(text="Starting firmware update...")
        await client.write_gatt_char(ctrl_char, b"\x00", True)
        written = 0
        with open(self.file_path, "rb") as gbl:
            count = 0
            while True:
                # chunk = gbl.read(128)
                chunk = gbl.read(180)
                if not chunk:
                    break
                await client.write_gatt_char(data_char, chunk, False)
                count = count + 1
                # if (count % 32) == 0 :        
                # if (count % 23) == 0 :        
                if (count % 45) == 0 :        
                    await asyncio.sleep(0.07)  # Adjust based on your device's needs
                else :
                    await asyncio.sleep(0.012)  # Adjust based on your device's needs
                written += len(chunk)
                self.label.config(text=f"{written} writes...\r")
        self.label.config(text='\n')
        await asyncio.sleep(1.0)  # Adjust based on your device's needs
        await client.write_gatt_char(ctrl_char, b"\x03", True)  # Command to indicate end of the update
        # self.label.config(text=f"Done{written}BYTES.{self.device_identifier} {client.address}")
        self.label.config(text=f"Done {written} BYTES.")

# 사용 예제
async def main():
    updater = BLEOTAUpdater("3826CA79-6A4A-F39C-C673-15D2BF28984B", "./application.gbl")
    updater.clear_screen()
    await updater.update_firmware()

if __name__ == "__main__":
    asyncio.run(main())
