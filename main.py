import tkinter as tk
from gui import WelcomePage, MenuPage, FCFSPage, LRJFPage, RRPage, SRJFPage, BattleRoyalPage, SJFPage

class CPUSchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CPU Scheduling Simulator")
        self.geometry("900x700")
        self.configure(bg="#1e1e2f")

        self.frames = {}
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        for F in (WelcomePage, MenuPage, FCFSPage, LRJFPage, RRPage, SRJFPage, BattleRoyalPage, SJFPage):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = CPUSchedulerApp()
    app.mainloop()