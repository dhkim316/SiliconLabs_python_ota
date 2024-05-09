import tkinter as tk
from tkinter import filedialog, Label
import sys
from BLEOTAUpdater import BLEOTAUpdater

import asyncio
import threading
    
class App(tk.Tk):
    def __init__(self, root):
        self.root = root
        self.selected_file = None
        self.setup_ui()
        self.loop = asyncio.get_event_loop()
        
    def setup_ui(self):
        # 파일 열기 버튼
        self.open_button = tk.Button(self.root, text="Open GBL File", command=self.open_file)
        self.open_button.pack(pady=10)

        # DFU 시작 버튼
        self.dfu_button = tk.Button(self.root, text="Start DFU", command=self.run_start_dfu)
        self.dfu_button.pack(pady=10)
        
        # 파일 경로와 메시지를 표시할 라벨
        self.message_label = Label(self.root, text="No file selected", wraplength=400)
        self.message_label.pack(pady=10)

        # DFU 메시지를 표시할 라벨
        self.dfu_message_label = Label(self.root, text="stand by...", wraplength=400)
        self.dfu_message_label.pack(pady=10)

    def open_file(self):
        # 파일 선택 다이얼로그를 사용하여 *.gbl 파일만 선택하도록 설정
        self.selected_file = filedialog.askopenfilename(
            filetypes=[("GBL files", "*.gbl")],
            title="Choose a GBL file"
        )
        if self.selected_file:
            self.message_label.config(text=f"Selected file: {self.selected_file}")
        else:
            self.message_label.config(text="No file selected.")

    async def start_dfu(self):
        # 선택한 파일로 DFU 프로세스를 시작하는 로직 구현
        if self.selected_file:
            message = f"Selected file: {self.selected_file}"
            updater = BLEOTAUpdater("AF2946F5-BDCE-2B17-0BD7-0F6C7A16B132", self.selected_file, self.dfu_message_label) #siu 01
            

            await updater.update_firmware()
            updater = None
            
            # DFU 작업을 시작하는 코드를 여기에 구현하세요.
            # 예: updater = BLEOTAUpdater(self.selected_file)
            #     updater.update_firmware()
        else:
            message = "No file selected for DFU process."
        self.message_label.config(text=message)

    def run_start_dfu(self):
        if not self.selected_file:
            self.message_label.config(text="No file selected for DFU process.")
            return

        def thread_target():
            try:
                # asyncio 이벤트 루프에서 비동기 작업을 실행합니다.
                asyncio.run(self.start_dfu())
            except Exception as e:
                # 예외가 발생하면 메인 스레드의 Tkinter 라벨을 업데이트합니다.
                error_message = f"DFU process failed: {e}"
                # Tkinter 위젯은 메인 스레드에서만 안전하게 업데이트할 수 있으므로,
                # after 메서드를 사용하여 메인 스레드에서 라벨 업데이트를 스케줄링합니다.
                self.root.after(0, lambda: self.message_label.config(text=error_message))

        # 예외 처리 로직을 포함하는 스레드를 시작합니다.
        threading.Thread(target=thread_target, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("GBL File Selector and DFU")
    app = App(root)
    root.geometry("800x200")  # 창 크기 설정
    root.mainloop()
