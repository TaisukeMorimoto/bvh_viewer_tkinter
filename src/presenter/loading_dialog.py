import time
import tkinter as tk
from tkinter import ttk


class LoadingDialog:
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Loading...")
        self.dialog.geometry("300x80")
        self.dialog.resizable(False, False)
        self.dialog.protocol("WM_DELETE_WINDOW", self.close)

        self.label = tk.Label(self.dialog, text="Please wait while loading...")
        self.label.pack(pady=5)

        self.progressbar = ttk.Progressbar(self.dialog, orient="horizontal", mode="indeterminate")
        self.progressbar.pack(pady=5)
        self.progressbar.start(10)

        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.dialog.after(5000, self.close)

    def close(self):
        self.dialog.grab_release()
        self.dialog.destroy()
