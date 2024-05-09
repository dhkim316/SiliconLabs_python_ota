# SiliconLabs_python_ota

Thanks a lot Mr. Kiril Zyapkov

Environment

1. macOS Monterey 12.7.4
2. Python 3.9.13
3. bleak

How to use
1. scan your device by bleScan.py
2. copy device address in scan result
3. paste device address in ota.py
    updater = BLEOTAUpdater("AF2946F5-BDCE-2B17-0BD7-0F6C7A16B132", self.selected_file, self.dfu_message_label)

4. run ota.apy
5. select gbl
6. start dfu

any question ijelectron@gmail.com


