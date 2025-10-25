import tkinter as tk
from tkinter import ttk, messagebox
from scheduler.simulation import run_simulation
from scheduler.utils import to_dataframe, compute_averages, create_gantt_chart
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FCFSPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e2f")
        self.controller = controller

        tk.Label(self, text="🔴 First-Come, First-Serve",
                 font=("Helvetica", 22, "bold"), fg="white", bg="#1e1e2f").pack(pady=20)

        self.num_processes = tk.IntVar(value=3)
        ttk.Label(self, text="Number of Processes:").pack()
        ttk.Entry(self, textvariable=self.num_processes).pack(pady=5)

        self.entries = []
        self.table_frame = tk.Frame(self, bg="#1e1e2f")
        self.table_frame.pack(pady=10)

        ttk.Button(self, text="Set Processes", command=self.make_process_table).pack(pady=10)
        ttk.Button(self, text="⬅ Back", command=lambda: controller.show_frame("MenuPage")).pack(side="bottom", pady=20)
    
    def make_process_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.entries.clear()

        #HEADERS
        tk.Label(self.table_frame, text="Process", fg="yellow", bg="#1e1e2f", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self.table_frame, text="Arrival Time", fg="yellow", bg="#1e1e2f", font=("Helvetica", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(self.table_frame, text="Burst Time", fg="yellow", bg="#1e1e2f", font=("Helvetica", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)

        n = self.num_processes.get()
        for i in range(n):
            tk.Label(self.table_frame, text=f"P{i+1}", fg="white", bg="#1e1e2f").grid(row=i+1, column=0, padx=5, pady=3) 
            arr = tk.Entry(self.table_frame, width=10)
            burst = tk.Entry(self.table_frame, width=10)
            arr.grid(row=i+1, column=1)  
            burst.grid(row=i+1, column=2) 
            arr.insert(0, "0")
            burst.insert(0, "5")
            self.entries.append((arr, burst))
        ttk.Button(self.table_frame, text="▶ Run Simulation", command=self.run_simulation).grid(columnspan=3, pady=10)

    def run_simulation(self):
        try:
            processes = []
            for i, (arr, burst) in enumerate(self.entries):
                processes.append({
                    "pid": i+1,
                    "arrival": int(arr.get()),
                    "burst": int(burst.get())
                })

            result, gantt = run_simulation("FCFS", processes)
            df = to_dataframe(result)
            avg_wait, avg_turn = compute_averages(df)

            messagebox.showinfo("Results", f"Avg Waiting: {avg_wait:.2f}\nAvg Turnaround: {avg_turn:.2f}")

            fig = create_gantt_chart(gantt)
            canvas = FigureCanvasTkAgg(fig, self)
            canvas.get_tk_widget().pack()
            canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", str(e))
