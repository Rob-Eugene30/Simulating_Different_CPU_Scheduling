import tkinter as tk
from tkinter import ttk, messagebox
from scheduler.simulation import run_simulation
from scheduler.utils import to_dataframe, compute_averages, create_gantt_chart
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class BattleRoyalPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e2f")
        self.controller = controller

        tk.Label(self, text="🏆 Battle Royale: LRJF vs Round Robin",
                 font=("Helvetica", 22, "bold"), fg="white", bg="#1e1e2f").pack(pady=20)

        # Inputs
        self.num_processes = tk.IntVar(value=3)
        self.quantum = tk.IntVar(value=4)

        ttk.Label(self, text="Number of Processes:").pack()
        ttk.Entry(self, textvariable=self.num_processes).pack(pady=5)

        ttk.Label(self, text="Quantum (for Round Robin):").pack()
        ttk.Entry(self, textvariable=self.quantum).pack(pady=5)

        self.entries = []
        self.table_frame = tk.Frame(self, bg="#1e1e2f")
        self.table_frame.pack(pady=10)

        ttk.Button(self, text="Set Processes", command=self.make_process_table).pack(pady=10)
        ttk.Button(self, text="⬅ Back", command=lambda: controller.show_frame("MenuPage")).pack(side="bottom", pady=20)

    def make_process_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.entries.clear()

        n = self.num_processes.get()
        for i in range(n):
            tk.Label(self.table_frame, text=f"P{i+1}", fg="white", bg="#1e1e2f").grid(row=i, column=0, padx=5, pady=3)
            arr = tk.Entry(self.table_frame, width=10)
            burst = tk.Entry(self.table_frame, width=10)
            arr.grid(row=i, column=1)
            burst.grid(row=i, column=2)
            arr.insert(0, "0")
            burst.insert(0, "5")
            self.entries.append((arr, burst))

        ttk.Button(self.table_frame, text="⚔ Run Battle", command=self.run_battle).grid(columnspan=3, pady=10)

    def run_battle(self):
        try:
            processes = []
            for i, (arr, burst) in enumerate(self.entries):
                processes.append({
                    "pid": i + 1,
                    "arrival": int(arr.get()),
                    "burst": int(burst.get())
                })

            # Run both simulations
            lrjf_result, lrjf_gantt = run_simulation("LRJF", [p.copy() for p in processes])
            rr_result, rr_gantt = run_simulation("Round Robin", [p.copy() for p in processes], self.quantum.get())

            lrjf_df = to_dataframe(lrjf_result)
            rr_df = to_dataframe(rr_result)

            lrjf_avg_wait, lrjf_avg_turn = compute_averages(lrjf_df)
            rr_avg_wait, rr_avg_turn = compute_averages(rr_df)

            # Destroy old charts if any
            for widget in self.table_frame.winfo_children():
                if isinstance(widget, tk.Canvas):
                    widget.destroy()

            # Show results
            res = (
                f"🔵 LRJF\nWaiting: {lrjf_avg_wait:.2f} | Turnaround: {lrjf_avg_turn:.2f}\n\n"
                f"🟢 Round Robin\nWaiting: {rr_avg_wait:.2f} | Turnaround: {rr_avg_turn:.2f}"
            )
            messagebox.showinfo("Results", res)

            # Display Gantt charts side by side
            frame_lrjf = tk.Frame(self, bg="#1e1e2f")
            frame_rr = tk.Frame(self, bg="#1e1e2f")
            frame_lrjf.pack(side="left", expand=True, padx=10, pady=10)
            frame_rr.pack(side="right", expand=True, padx=10, pady=10)

            fig_lrjf = create_gantt_chart(lrjf_gantt, "LRJF Gantt Chart")
            fig_rr = create_gantt_chart(rr_gantt, "Round Robin Gantt Chart")

            canvas_lrjf = FigureCanvasTkAgg(fig_lrjf, frame_lrjf)
            canvas_lrjf.get_tk_widget().pack()
            canvas_lrjf.draw()

            canvas_rr = FigureCanvasTkAgg(fig_rr, frame_rr)
            canvas_rr.get_tk_widget().pack()
            canvas_rr.draw()

        except Exception as e:
            messagebox.showerror("Error", str(e))
