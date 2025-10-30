import customtkinter as ctk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scheduler.simulation import run_simulation
from scheduler.utils import to_dataframe, compute_averages, create_gantt_chart
from gui.scrollable_frame import ScrollableFrame


class FCFSPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#0b0c10")
        self.controller = controller

        # === Scrollable region ===
        scroll_area = ScrollableFrame(self, fg_color="#0b0c10")
        scroll_area.pack(expand=True, fill="both")
        content = scroll_area.scrollable_frame  # All widgets go inside here

        # === Header ===
        header_frame = ctk.CTkFrame(content, fg_color="transparent")
        header_frame.pack(fill="x", pady=(10, 20))

        title_label = ctk.CTkLabel(
            header_frame,
            text="🔴 First-Come, First-Serve Scheduling",
            font=("Orbitron", 26, "bold"),
            text_color="#00ffff"
        )
        title_label.pack(side="left", padx=30, pady=10)

        back_button = ctk.CTkButton(
            header_frame,
            text="⬅ Back to Menu",
            fg_color="#1f2833",
            hover_color="#45A29E",
            text_color="white",
            corner_radius=12,
            width=150,
            height=40,
            font=("Helvetica", 13, "bold"),
            command=lambda: controller.show_frame("MenuPage"),
        )
        back_button.pack(side="right", padx=30, pady=10)

        # === Input Frame ===
        self.input_frame = ctk.CTkFrame(content, fg_color="#111827", corner_radius=12)
        self.input_frame.pack(pady=10, padx=40, fill="x")

        self.num_processes = ctk.IntVar(value=3)

        ctk.CTkLabel(
            self.input_frame,
            text="Number of Processes:",
            text_color="#66FCF1",
            font=("Helvetica", 14, "bold")
        ).grid(row=0, column=0, padx=10, pady=10, sticky="e")

        ctk.CTkEntry(self.input_frame, textvariable=self.num_processes, width=100).grid(
            row=0, column=1, padx=10, pady=10, sticky="w"
        )

        ctk.CTkButton(
            self.input_frame,
            text="Set Processes",
            fg_color="#45A29E",
            hover_color="#66FCF1",
            text_color="#0b0c10",
            corner_radius=12,
            command=self.make_process_table
        ).grid(row=0, column=2, padx=20, pady=10)

        # === Dynamic Frames ===
        self.table_frame = ctk.CTkFrame(content, fg_color="#0b0c10")
        self.table_frame.pack(pady=20)

        self.result_frame = ctk.CTkFrame(content, fg_color="#0b0c10")
        self.result_frame.pack(pady=20, fill="both", expand=True)

        self.entries = []  # To hold process entry fields

    # --------------------------------------------------------
    def make_process_table(self):
        """Generate dynamic process entry fields."""
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        n = self.num_processes.get()
        self.entries = []

        headers = ["Process", "Arrival Time", "Burst Time"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                self.table_frame,
                text=header,
                text_color="#66FCF1",
                font=("Helvetica", 13, "bold")
            ).grid(row=0, column=i, padx=10, pady=5)

        for i in range(n):
            ctk.CTkLabel(
                self.table_frame,
                text=f"P{i+1}",
                text_color="white",
                font=("Helvetica", 12)
            ).grid(row=i + 1, column=0, padx=10, pady=5)

            arr = ctk.CTkEntry(self.table_frame, width=100)
            burst = ctk.CTkEntry(self.table_frame, width=100)
            arr.grid(row=i + 1, column=1, padx=10, pady=5)
            burst.grid(row=i + 1, column=2, padx=10, pady=5)
            arr.insert(0, "0")
            burst.insert(0, "5")

            self.entries.append((arr, burst))

        ctk.CTkButton(
            self.table_frame,
            text="▶ Run Simulation",
            fg_color="#4f46e5",
            hover_color="#6d28d9",
            text_color="white",
            corner_radius=15,
            width=200,
            height=40,
            font=("Helvetica", 14, "bold"),
            command=self.run_simulation
        ).grid(columnspan=3, pady=20)

    # --------------------------------------------------------
    def run_simulation(self):
        """Run FCFS scheduling and display results."""
        try:
            for widget in self.result_frame.winfo_children():
                widget.destroy()

            processes = []
            for i, (arr, burst) in enumerate(self.entries):
                processes.append({
                    "pid": i + 1,
                    "arrival": int(arr.get()),
                    "burst": int(burst.get())
                })

            result, gantt = run_simulation("FCFS", processes)
            df = to_dataframe(result)
            avg_wait, avg_turn = compute_averages(df)

            # === Gantt Chart ===
            fig = create_gantt_chart(gantt)
            fig.patch.set_facecolor("#0b0c10")
            ax = fig.axes[0]
            ax.set_facecolor("#0b0c10")
            ax.tick_params(colors="white", labelsize=9)
            ax.title.set_color("#66FCF1")

            canvas = FigureCanvasTkAgg(fig, self.result_frame)
            canvas.get_tk_widget().pack(pady=10)
            canvas.draw()

            # === Results Summary ===
            results_text = (
                f"📊 Average Waiting Time: {avg_wait:.2f}\n"
                f"🪐 Average Turnaround Time: {avg_turn:.2f}"
            )

            ctk.CTkLabel(
                self.result_frame,
                text=results_text,
                font=("Helvetica", 15, "bold"),
                text_color="#00ffff"
            ).pack(pady=20)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --------------------------------------------------------
    def reset_page(self):
        """Reset all inputs and results when reopened."""
        self.num_processes.set(3)
        for frame in [self.table_frame, self.result_frame]:
            for widget in frame.winfo_children():
                widget.destroy()
        self.entries.clear()