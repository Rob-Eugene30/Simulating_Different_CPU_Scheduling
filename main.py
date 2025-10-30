import customtkinter as ctk
from gui import (WelcomePage, MenuPage, FCFSPage, LRJFPage,
                 RRPage, SRJFPage, BattleRoyalPage, SJFPage)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # === Window Configuration ===
        self.title("💻 CPU Scheduling Simulator | Space Edition")
        self.geometry("1280x720")        # Unified size for all pages
        self.minsize(1100, 600)
        self.configure(fg_color="#0b0c10")  # Deep-space background

        # === CustomTkinter Global Appearance ===
        ctk.set_appearance_mode("dark")        # Options: "dark", "light", "system"
        ctk.set_default_color_theme("blue")    # You can use "dark-blue" or a custom JSON theme

        # === Container for All Pages ===
        container = ctk.CTkFrame(self, fg_color="#0b0c10")
        container.pack(expand=True, fill="both")

        # Ensure child frames fill entire window
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # === Register All Pages ===
        self.frames = {}
        pages = (WelcomePage, MenuPage, FCFSPage, LRJFPage,
                 RRPage, SRJFPage, SJFPage, BattleRoyalPage)

        for PageClass in pages:
            page_name = PageClass.__name__
            frame = PageClass(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")  # Full coverage layout

        # === Start with Welcome Page ===
        self.show_frame("WelcomePage")

    # === Page Switching ===
    def show_frame(self, page_name: str):
        """Raise the selected page to the top of the stack."""
        frame = self.frames[page_name]
        
        # Call reset_page() if it exists
        if hasattr(frame, "reset_page"):
             frame.reset_page()
        frame.tkraise()

    # === Optional Centering (for aesthetic startup) ===
    def center_window(self):
        """Centers the window on screen after initialization."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == "__main__":
    app = App()
    app.center_window()
    app.mainloop()
