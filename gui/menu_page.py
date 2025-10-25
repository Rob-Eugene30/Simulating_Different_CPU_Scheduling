import tkinter as tk
from tkinter import ttk


class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e2f")
        self.controller = controller

        title = tk.Label(self, text="⚙️ Choose Simulation Mode",
                         font=("Helvetica", 22, "bold"), fg="white", bg="#1e1e2f")
        title.pack(pady=40)

        ttk.Button(self, text="🔴 First-Come, First-Serve",
                   command=lambda: controller.show_frame("FCFSPage")).pack(pady=10)
        ttk.Button(self, text="🔵 Longest Remaining Job First",
                   command=lambda: controller.show_frame("LRJFPage")).pack(pady=10)
        ttk.Button(self, text="🟢 Round Robin",
                   command=lambda: controller.show_frame("RRPage")).pack(pady=10)
        ttk.Button(self, text="🟡 Shortest Remaining Job First",
                   command=lambda: controller.show_frame("SRJFPage")).pack(pady=10)
        ttk.Button(self, text="🏆 Battle Royale",
                   command=lambda: controller.show_frame("BattleRoyalPage")).pack(pady=10)

        ttk.Button(self, text="⬅ Back",
                   command=lambda: controller.show_frame("WelcomePage")).pack(pady=30)