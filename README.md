# SiliconLabs_python_ota

Environment
macOS Monterey 12.7.4
Python 3.9.13
bleak

How to use
1. scan your device by bleScan.py
2. copy device address in scan result
3. paste device address in ota.py
    updater = BLEOTAUpdater("AF2946F5-BDCE-2B17-0BD7-0F6C7A16B132", self.selected_file, self.dfu_message_label)

4. run ota.apy
5. select gbl
6. start dfu

any question ijelectron@gmail.com


