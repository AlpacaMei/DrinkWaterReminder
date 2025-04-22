import time
import threading
from tkinter import Tk, Label, Entry, Button, StringVar
from win11toast import toast

class WaterReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("喝水提醒小幫手")
        self.root.geometry("300x250")

        self.interval_minutes = StringVar(value="60")
        self.max_reminders = StringVar(value="5")
        self.status = StringVar(value="尚未啟動")

        Label(root, text="請輸入提醒間隔（分鐘）:").pack(pady=5)
        Entry(root, textvariable=self.interval_minutes).pack()

        Label(root, text="請輸入提醒次數:").pack(pady=5)
        Entry(root, textvariable=self.max_reminders).pack()

        Button(root, text="啟動提醒", command=self.start_reminder).pack(pady=10)
        Label(root, textvariable=self.status, fg="blue").pack(pady=10)

        self.running = False

    def start_reminder(self):
        if not self.running:
            self.running = True
            self.status.set("提醒中...（每 {} 分鐘，共 {} 次）".format(
                self.interval_minutes.get(), self.max_reminders.get()))
            threading.Thread(target=self.remind_loop, daemon=True).start()

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
            toast("💧 喝水時間到！", f"這是第 {i+1} 次提醒，記得補充水分！")
            time.sleep(interval)

        self.status.set(f"提醒結束，共提醒 {max_times} 次。")
        self.running = False

if __name__ == "__main__":
    root = Tk()
    app = WaterReminderApp(root)
    root.mainloop()
