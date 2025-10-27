import tkinter as tk
from tkinter import ttk, messagebox
from scheduler.simulation import run_simulation
from scheduler.utils import to_dataframe, compute_averages, create_gantt_chart
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SJFPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e2f")
        self.controller = controller

        # --- Title ---
        tk.Label(self, text="🟡 Shortest Job First (Non-Preemptive)",
                 font=("Helvetica", 22, "bold"), fg="white", bg="#1e1e2f").pack(pady=20)

        # --- Input for number of processes ---
        self.num_processes = tk.IntVar(value=3)
        ttk.Label(self, text="Number of Processes:").pack()
        ttk.Entry(self, textvariable=self.num_processes).pack(pady=5)

        self.entries = []
        self.table_frame = tk.Frame(self, bg="#1e1e2f")
        self.table_frame.pack(pady=10)

        ttk.Button(self, text="Set Processes", command=self.make_process_table).pack(pady=10)
        ttk.Button(self, text="⬅ Back", command=lambda: controller.show_frame("MenuPage")).pack(side="bottom", pady=20)

        # --- Result frames ---
        self.result_frame = tk.Frame(self, bg="#1e1e2f")
        self.result_frame.pack(pady=10, fill="both", expand=True)

    # --------------------------------------------------------
    def make_process_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.entries.clear()

        # Table headers
        headers = ["Process", "Arrival Time", "Burst Time"]
        for i, header in enumerate(headers):
            tk.Label(self.table_frame, text=header, fg="yellow", bg="#1e1e2f",
                     font=("Helvetica", 10, "bold")).grid(row=0, column=i, padx=5, pady=5)

        # Dynamic entry fields
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

    # --------------------------------------------------------
    def run_simulation(self):
        try:
            # Clear old results
            for widget in self.result_frame.winfo_children():
                widget.destroy()

            # Collect process data
            processes = []
            for i, (arr, burst) in enumerate(self.entries):
                processes.append({
                    "pid": i + 1,
                    "arrival": int(arr.get()),
                    "burst": int(burst.get())
                })

            # Run scheduler (note the algorithm name "SJF")
            result, gantt = run_simulation("SJF", processes)
            df = to_dataframe(result)
            avg_wait, avg_turn = compute_averages(df)

            # --- Gantt Chart ---
            fig = create_gantt_chart(gantt)
            canvas = FigureCanvasTkAgg(fig, self.result_frame)
            canvas.get_tk_widget().pack(pady=10)
            canvas.draw()

            # --- Table of results ---
            columns = ["PID", "Arrival", "Burst", "Completion", "Turnaround", "Waiting"]
            tree = ttk.Treeview(self.result_frame, columns=columns, show="headings", height=8)
            style = ttk.Style()
            style.configure("Treeview", background="#1e1e2f", foreground="white", fieldbackground="#1e1e2f")
            style.map("Treeview", background=[("selected", "#007acc")])

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center", width=100)

            for _, row in df.iterrows():
                tree.insert("", "end", values=(
                    row["pid"], row["arrival"], row["burst"],
                    row["completion"], row["turnaround"], row["waiting"]
                ))

            tree.pack(pady=10)

            # --- Averages display ---
            avg_label = tk.Label(
                self.result_frame,
                text=f"📊 Average Waiting Time: {avg_wait:.2f}     |     Average Turnaround Time: {avg_turn:.2f}",
                fg="white", bg="#1e1e2f", font=("Helvetica", 11, "bold")
            )
            avg_label.pack(pady=5)

        except Exception as e:
            messagebox.showerror("Error", str(e))