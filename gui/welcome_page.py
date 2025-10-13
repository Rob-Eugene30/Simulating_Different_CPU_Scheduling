import tkinter as tk
from tkinter import ttk

class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e2f")
        self.controller = controller

        title = tk.Label(self, text="💻 CPU Scheduling Simulator",
                         font=("Helvetica", 26, "bold"), fg="white", bg="#1e1e2f")
        title.pack(pady=60)

        desc = tk.Label(self, text="Simulate CPU scheduling algorithms visually!",
                        font=("Helvetica", 14), fg="#aaa", bg="#1e1e2f")
        desc.pack(pady=10)

        start_btn = ttk.Button(self, text="🚀 Start Simulation",
                               command=lambda: controller.show_frame("MenuPage"))
        start_btn.pack(pady=30)
