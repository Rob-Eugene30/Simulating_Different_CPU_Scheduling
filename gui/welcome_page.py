import customtkinter as ctk

class WelcomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#0b0c10")  # Deep space background
        self.controller = controller

        # Center content vertically and horizontally
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(expand=True, fill="both")

        # --- Title ---
        self.title_label = ctk.CTkLabel(
            content_frame,
            text="💻 CPU Scheduling Simulator",
            font=("Orbitron", 36, "bold"),
            text_color="#00ffff"
        )
        self.title_label.pack(pady=(120, 10))

        # --- Description ---
        self.desc_label = ctk.CTkLabel(
            content_frame,
            text="Simulate CPU scheduling algorithms visually in a cosmic interface!",
            font=("Helvetica", 16),
            text_color="#c5c6c7",
            wraplength=600
        )
        self.desc_label.pack(pady=10)

        # --- Divider line ---
        self.divider = ctk.CTkFrame(content_frame, fg_color="#1f2833", height=2)
        self.divider.pack(fill="x", padx=120, pady=30)

        # --- Start Button ---
        self.start_button = ctk.CTkButton(
            content_frame,
            text="🚀 Start Simulation",
            fg_color="#4f46e5",
            hover_color="#6d28d9",
            text_color="white",
            corner_radius=20,
            width=250,
            height=50,
            font=("Orbitron", 18, "bold"),
            command=lambda: controller.show_frame("MenuPage")
        )
        self.start_button.pack(pady=50)

        # --- Footer ---
        self.footer = ctk.CTkLabel(
            content_frame,
            text="Developed by AwesomePeople | Space Edition",
            font=("Consolas", 12),
            text_color="#7f8c8d"
        )
        self.footer.pack(side="bottom", pady=30)
