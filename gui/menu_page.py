import customtkinter as ctk

class MenuPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#0b0c10")  # Deep space background
        self.controller = controller

        # Central container for buttons
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill="both")

        # --- Title ---
        self.title_label = ctk.CTkLabel(
            main_frame,
            text="⚙️ Choose Simulation Mode",
            font=("Orbitron", 32, "bold"),
            text_color="#00ffff"
        )
        self.title_label.pack(pady=(80, 30))

        # --- Button style ---
        button_style = {
            "fg_color": "#45A29E",
            "hover_color": "#66FCF1",
            "text_color": "#0b0c10",
            "corner_radius": 15,
            "width": 320,
            "height": 50,
            "font": ("Helvetica", 15, "bold")
        }

        # --- Simulation Buttons ---
        ctk.CTkButton(main_frame, text="🔴 First-Come, First-Serve",
                      command=lambda: controller.show_frame("FCFSPage"), **button_style).pack(pady=10)
        ctk.CTkButton(main_frame, text="🔵 Longest Remaining Job First",
                      command=lambda: controller.show_frame("LRJFPage"), **button_style).pack(pady=10)
        ctk.CTkButton(main_frame, text="🟢 Round Robin",
                      command=lambda: controller.show_frame("RRPage"), **button_style).pack(pady=10)
        ctk.CTkButton(main_frame, text="🟡 Shortest Remaining Job First",
                      command=lambda: controller.show_frame("SRJFPage"), **button_style).pack(pady=10)
        ctk.CTkButton(main_frame, text="🟣 Shortest Job First",
                      command=lambda: controller.show_frame("SJFPage"), **button_style).pack(pady=10)
        ctk.CTkButton(main_frame, text="🏆 Battle Royale",
                      command=lambda: controller.show_frame("BattleRoyalPage"), **button_style).pack(pady=10)

        # --- Divider ---
        divider = ctk.CTkFrame(main_frame, fg_color="#1f2833", height=2)
        divider.pack(fill="x", padx=160, pady=(40, 20))

        # --- Back Button ---
        self.back_button = ctk.CTkButton(
            main_frame,
            text="⬅ Back to Home",
            fg_color="#1f2833",
            hover_color="#45A29E",
            text_color="white",
            corner_radius=15,
            width=220,
            height=45,
            font=("Helvetica", 14, "bold"),
            command=lambda: controller.show_frame("WelcomePage")
        )
        self.back_button.pack(pady=20)
