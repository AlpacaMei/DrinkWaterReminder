import os
import sys
import time
import threading
from tkinter import Tk, Label, Entry, Button, StringVar
from winotify import Notification, audio

def resource_path(relative_path):
    """打包後讀取資源用"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

ICON_PATH = resource_path("asset/water_icon_with_sizes.ico")

def warm_up_notification():
    """預熱通知系統"""
    try:
        toast = Notification(
            app_id="喝水提醒小幫手",
            title="初始化通知中...",
            msg="稍後將開始提醒您喝水！",
            icon=ICON_PATH
        )
        toast.set_audio(audio.Default, loop=False)
        toast.show()
    except:
        pass

class WaterReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("喝水提醒小幫手")
        self.root.geometry("300x250")

        self.interval_minutes = StringVar(value="15")
        self.max_reminders = StringVar(value="40")
        self.status = StringVar(value="尚未啟動")

        Label(root, text="請輸入提醒間隔（分鐘）:").pack(pady=5)
        Entry(root, textvariable=self.interval_minutes).pack()

        Label(root, text="請輸入提醒次數:").pack(pady=5)
        Entry(root, textvariable=self.max_reminders).pack()

        Button(root, text="啟動提醒", command=self.start_reminder).pack(pady=10)
        Button(root, text="停止提醒", command=self.stop_reminder).pack(pady=5)
        Label(root, textvariable=self.status, fg="blue").pack(pady=10)

        self.running = False
        warm_up_notification()

    def start_reminder(self):
        if not self.running:
            self.running = True
            self.status.set(f"提醒中...（每 {self.interval_minutes.get()} 分鐘，共 {self.max_reminders.get()} 次）")
            threading.Thread(target=self.remind_loop, daemon=True).start()

    def stop_reminder(self):
            self.running = False
            self.status.set("提醒已停止。")

    def remind_loop(self):
        try:
            interval = int(self.interval_minutes.get()) * 60
            max_times = int(self.max_reminders.get())
        except ValueError:
            self.status.set("請輸入正確的數字！")
            self.running = False
            return

        for i in range(max_times):
            if not self.running:
                break

            toast = Notification(
                app_id="喝水提醒小幫手",
                title="💧 喝水時間到！",
                msg=f"這是第 {i+1} 次提醒，記得補充水分！",
                icon=ICON_PATH
            )
            toast.set_audio(audio.Default, loop=False)
            toast.show()

            time.sleep(interval)

        self.status.set(f"提醒結束，共提醒 {max_times} 次。")
        self.running = False

if __name__ == "__main__":
    root = Tk()
    app = WaterReminderApp(root)
    root.mainloop()

