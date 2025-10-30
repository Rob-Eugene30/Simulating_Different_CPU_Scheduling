import copy
import threading
import time
import customtkinter as ctk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt

from scheduler.simulation import run_simulation
from scheduler.utils import to_dataframe, compute_averages, create_gantt_chart
from gui.scrollable_frame import ScrollableFrame


class BattleRoyalPage(ctk.CTkFrame):
    """
    Battle Royal page: runs multiple scheduler algorithms on the same process set,
    compares averages, and displays Gantt charts. Centered layout and 1–10 process control.
    """

    ALGO_MAP = {
        "FCFS": "FCFS",
        "SJF": "SJF",
        "SRJF": "SRJF",
        "LRJF": "LRJF",
        "Round Robin": "Round Robin",
    }

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#0b0c10")
        self.controller = controller

        # === Scrollable container ===
        scroll = ScrollableFrame(self, fg_color="#0b0c10")
        scroll.pack(expand=True, fill="both")
        content = scroll.scrollable_frame

        # === Header ===
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(10, 20))

        title = ctk.CTkLabel(
            header,
            text="⚔ Battle Royal: Scheduler Showdown",
            font=("Orbitron", 28, "bold"),
            text_color="#a78bfa",
        )
        title.pack(side="left", padx=40, pady=10)

        back_button = ctk.CTkButton(
            header,
            text="⬅ Back to Menu",
            fg_color="#1f2833",
            hover_color="#a78bfa",
            text_color="white",
            corner_radius=12,
            width=160,
            height=40,
            font=("Helvetica", 13, "bold"),
            command=lambda: controller.show_frame("MenuPage"),
        )
        back_button.pack(side="right", padx=40, pady=10)

        # === Controls Frame (Centered) ===
        control_frame = ctk.CTkFrame(content, fg_color="#111827", corner_radius=15)
        control_frame.pack(padx=80, pady=(0, 20), fill="x")

        # Process count
        ctk.CTkLabel(
            control_frame,
            text="Number of Processes:",
            text_color="#c4b5fd",
            font=("Helvetica", 14, "bold"),
        ).grid(row=0, column=0, padx=10, pady=15, sticky="e")

        self.num_procs = ctk.StringVar(value="3")
        proc_selector = ctk.CTkOptionMenu(
            control_frame,
            values=[str(i) for i in range(1, 11)],
            variable=self.num_procs,
            fg_color="#4f46e5",
            button_color="#6d28d9",
            button_hover_color="#818cf8",
            text_color="white",
            width=80,
            command=lambda _: self.build_process_table(),
        )
        proc_selector.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # RR Quantum Control
        ctk.CTkLabel(
            control_frame,
            text="Round Robin Quantum:",
            text_color="#9be7ff",
            font=("Helvetica", 13, "bold"),
        ).grid(row=0, column=2, padx=(50, 5), pady=15, sticky="e")

        self.rr_quantum = ctk.IntVar(value=2)
        q_entry = ctk.CTkEntry(control_frame, textvariable=self.rr_quantum, width=80)
        q_entry.grid(row=0, column=3, padx=10, pady=10, sticky="w")

        # Algorithm checkboxes
        algo_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        algo_frame.grid(row=1, column=0, columnspan=4, pady=(10, 5))

        ctk.CTkLabel(
            algo_frame,
            text="Select Algorithms:",
            font=("Helvetica", 14, "bold"),
            text_color="#c4b5fd",
        ).pack(pady=5)

        self.selected_algos = {}
        algo_list = list(self.ALGO_MAP.keys())
        for i, name in enumerate(algo_list):
            var = ctk.BooleanVar(value=True if name != "Round Robin" else False)
            cb = ctk.CTkCheckBox(
                algo_frame,
                text=name,
                variable=var,
                fg_color="#7c3aed",
                text_color="#e2e8f0",
            )
            cb.pack(side="left", padx=10, pady=5)
            self.selected_algos[name] = var

        # === Process Table ===
        self.table_frame = ctk.CTkFrame(content, fg_color="#0b0c10")
        self.table_frame.pack(padx=120, pady=20, fill="x")

        # Build initial 3-row table
        self.process_entries = []
        self.build_process_table()

        # === Control Buttons (Centered) ===
        button_frame = ctk.CTkFrame(content, fg_color="transparent")
        button_frame.pack(pady=10)

        self.start_button = ctk.CTkButton(
            button_frame,
            text="⚔ Start Battle",
            fg_color="#7c3aed",
            hover_color="#a78bfa",
            width=200,
            height=40,
            font=("Helvetica", 15, "bold"),
            command=self.start_battle,
        )
        self.start_button.pack(side="left", padx=15)

        self.reset_button = ctk.CTkButton(
            button_frame,
            text="♻ Reset Arena",
            fg_color="#1f2833",
            hover_color="#374151",
            width=180,
            height=40,
            command=self.reset_page,
        )
        self.reset_button.pack(side="left", padx=15)

        # === Loader (Animated) ===
        self.loader_frame = ctk.CTkFrame(content, fg_color="transparent")
        self.progress = ctk.CTkProgressBar(self.loader_frame, mode="indeterminate")
        self.progress.pack(fill="x", padx=150, pady=5)
        self.loader_label = ctk.CTkLabel(
            self.loader_frame, text="", text_color="#c7bfe6"
        )
        self.loader_label.pack(pady=3)
        self.loader_frame.pack_forget()

        # === Results Frame ===
        self.results_frame = ctk.CTkFrame(content, fg_color="#0b0c10")
        self.results_frame.pack(padx=80, pady=20, fill="both", expand=True)

        self.chart_canvas = None
        self.gantt_tabs = None
        self.champion_label = None

    # ----------------------------------------------------
    def build_process_table(self):
        """Rebuilds the process input table based on dropdown value."""
        for w in self.table_frame.winfo_children():
            w.destroy()
        self.process_entries.clear()

        headers = ["Process", "Arrival Time", "Burst Time"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(
                self.table_frame, text=h, text_color="#c4b5fd", font=("Helvetica", 13, "bold")
            ).grid(row=0, column=i, padx=10, pady=6)

        n = int(self.num_procs.get())
        for i in range(n):
            ctk.CTkLabel(
                self.table_frame, text=f"P{i+1}", text_color="white", font=("Helvetica", 12)
            ).grid(row=i + 1, column=0, padx=10, pady=5)

            a = ctk.CTkEntry(self.table_frame, width=120)
            b = ctk.CTkEntry(self.table_frame, width=120)
            a.insert(0, "0")
            b.insert(0, "5")
            a.grid(row=i + 1, column=1, padx=10, pady=5)
            b.grid(row=i + 1, column=2, padx=10, pady=5)
            self.process_entries.append((a, b))

    # ----------------------------------------------------
    def start_battle(self):
        """Starts the threaded simulations and displays loader."""
        algos = [n for n, v in self.selected_algos.items() if v.get()]
        if not algos:
            messagebox.showwarning("No Algorithms", "Select at least one scheduler!")
            return

        processes = []
        try:
            for i, (a, b) in enumerate(self.process_entries):
                processes.append(
                    {"pid": i + 1, "arrival": int(a.get()), "burst": int(b.get())}
                )
        except ValueError:
            messagebox.showerror("Invalid Input", "All values must be integers.")
            return

        self._disable_buttons()
        self.loader_label.configure(text="Simulations running... please wait ⚙️")
        self.loader_frame.pack(pady=10)
        self.progress.start()

        def worker():
            try:
                results = []
                for name in algos:
                    key = self.ALGO_MAP[name]
                    q = self.rr_quantum.get()
                    time.sleep(0.05)
                    if key == "Round Robin":
                        result, gantt = run_simulation(key, copy.deepcopy(processes), q)
                    else:
                        result, gantt = run_simulation(key, copy.deepcopy(processes))
                    df = to_dataframe(result)
                    w, t = compute_averages(df)
                    results.append(
                        {"name": name, "wait": w, "turn": t, "gantt": gantt}
                    )
                self.after(0, lambda: self._show_results(results))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Error", str(e)))
            finally:
                self.after(0, self._enable_buttons)

        threading.Thread(target=worker, daemon=True).start()

    # ----------------------------------------------------
    def _show_results(self, results):
        """Displays comparative charts and champion."""
        for w in self.results_frame.winfo_children():
            w.destroy()

        self.loader_frame.pack_forget()
        self.progress.stop()

        # --- Bar Chart ---
        fig, ax = plt.subplots(figsize=(6.5, 4))
        fig.patch.set_facecolor("#0b0c10")
        ax.set_facecolor("#0b0c10")

        names = [r["name"] for r in results]
        waits = [r["wait"] for r in results]
        turns = [r["turn"] for r in results]
        x = range(len(names))
        ax.bar([i - 0.2 for i in x], waits, width=0.4, label="Avg Wait")
        ax.bar([i + 0.2 for i in x], turns, width=0.4, label="Avg Turnaround")
        ax.set_xticks(list(x))
        ax.set_xticklabels(names, color="white")
        ax.legend(facecolor="#1f2937", edgecolor="none", labelcolor="white")
        ax.tick_params(colors="white")

        canvas = FigureCanvasTkAgg(fig, self.results_frame)
        canvas.get_tk_widget().pack(pady=10)
        canvas.draw()

        # --- Gantt Tabs ---
        tabs = ctk.CTkTabview(self.results_frame, width=600)
        tabs.pack(pady=15)
        for r in results:
            tabs.add(r["name"])
            fig_g = create_gantt_chart(r["gantt"])
            fig_g.patch.set_facecolor("#0b0c10")
            ax_g = fig_g.axes[0]
            ax_g.set_facecolor("#0b0c10")
            ax_g.tick_params(colors="white", labelsize=8)
            ax_g.title.set_color("#c4b5fd")
            c = FigureCanvasTkAgg(fig_g, tabs.tab(r["name"]))
            c.get_tk_widget().pack(pady=8)
            c.draw()

        # --- Champion ---
        best = min(results, key=lambda r: (r["wait"] + r["turn"]))
        champ_text = (
            f"🏆 Champion: {best['name']} "
            f"(Wait={best['wait']:.2f}, Turn={best['turn']:.2f})"
        )
        ctk.CTkLabel(
            self.results_frame,
            text=champ_text,
            font=("Orbitron", 18, "bold"),
            text_color="#fef3c7",
        ).pack(pady=10)

    # ----------------------------------------------------
    def reset_page(self):
        """Resets page visuals."""
        self.num_procs.set("3")
        self.rr_quantum.set(2)
        for v in self.selected_algos.values():
            v.set(True)
        self.build_process_table()
        for w in self.results_frame.winfo_children():
            w.destroy()
        self.loader_frame.pack_forget()

    # ----------------------------------------------------
    def _disable_buttons(self):
        self.start_button.configure(state="disabled")
        self.reset_button.configure(state="disabled")

    def _enable_buttons(self):
        self.start_button.configure(state="normal")
        self.reset_button.configure(state="normal")