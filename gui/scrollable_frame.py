import customtkinter as ctk
import tkinter as tk

"""
Scrollable Frame
----------------
Reusable scrollable frame for CustomTkinter pages.
Adds vertical scroll when content exceeds visible height.
"""

class ScrollableFrame(ctk.CTkFrame):
    """
    A reusable scrollable frame for CustomTkinter pages.
    Automatically adds vertical scroll support when content exceeds window height.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # --- Canvas & Scrollbar setup ---
        self.canvas = tk.Canvas(self, bg="#0b0c10", highlightthickness=0)
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="transparent")

        # Bind resizing to scroll region updates
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Create a window inside the canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Link scroll commands
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # --- Layout ---
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # --- Mouse Wheel Binding (Safe) ---
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

        # Handle resizing correctly
        self.bind("<Configure>", self._on_frame_configure)

    # --------------------------------------------------
    # Scroll Behavior
    # --------------------------------------------------
    def _on_mousewheel(self, event):
        """Scroll with mouse wheel (Windows/Linux/macOS support)."""
        if event.num == 4:  # Linux scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux scroll down
            self.canvas.yview_scroll(1, "units")
        else:  # Windows / macOS
            self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def _bind_mousewheel(self, _event):
        """Enable mouse wheel scrolling when cursor is over canvas."""
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)      # Windows/macOS
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)        # Linux
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mousewheel(self, _event):
        """Disable scrolling when cursor leaves canvas."""
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    # --------------------------------------------------
    # Resizing Behavior
    # --------------------------------------------------
    def _on_frame_configure(self, event):
        """Ensure inner frame width matches visible area."""
        self.canvas.itemconfig(self.canvas_window, width=event.width)