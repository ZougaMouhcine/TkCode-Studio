"""Preview panel for TkLearn Studio.

Displays the graphical output of the user's Tkinter code.
The inner frame acts as the 'root' widget for user code execution.
"""

import tkinter as tk
from tkinter import ttk

from src.utils.constants import (
    PREVIEW_BG,
    PREVIEW_HEADER_BG,
    PREVIEW_ACCENT,
    HEADER_FONT,
    FG_SECONDARY,
)


class PreviewFrame(ttk.Frame):
    """A preview frame where user-created Tkinter widgets are rendered."""

    def __init__(self, parent, **kwargs):
        """Initialize the preview frame.

        Args:
            parent: The parent widget.
        """
        super().__init__(parent, **kwargs)
        self._build_ui()

    def _build_ui(self):
        """Construct the preview UI components."""
        # ── Colored header bar ──
        header_bar = tk.Frame(self, bg=PREVIEW_HEADER_BG, height=32)
        header_bar.pack(side=tk.TOP, fill=tk.X)
        header_bar.pack_propagate(False)

        accent = tk.Frame(header_bar, bg=PREVIEW_ACCENT, width=4)
        accent.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(
            header_bar,
            text="  \u25A0  Preview",
            font=HEADER_FONT,
            bg=PREVIEW_HEADER_BG,
            fg=PREVIEW_ACCENT,
            anchor=tk.W,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)

        # Accent line under header
        tk.Frame(self, bg=PREVIEW_ACCENT, height=1).pack(side=tk.TOP, fill=tk.X)

        # ── Preview container ──
        self._canvas_frame = tk.Frame(self, bg=PREVIEW_BG, bd=0, highlightthickness=0)
        self._canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Watermark hint (shown when empty)
        self._watermark = tk.Label(
            self._canvas_frame,
            text="\u25B6  Press F5 to run your code",
            font=("Segoe UI", 13),
            fg="#c0c0c0",
            bg=PREVIEW_BG,
        )
        self._watermark.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    @property
    def preview_container(self):
        """Return the inner frame used as the root for user widget code.

        Returns:
            tk.Frame: The container frame for rendered widgets.
        """
        return self._canvas_frame

    def clear_preview(self):
        """Destroy all child widgets inside the preview container."""
        for widget in self._canvas_frame.winfo_children():
            widget.destroy()
        # Re-show watermark
        self._watermark = tk.Label(
            self._canvas_frame,
            text="\u25B6  Press F5 to run your code",
            font=("Segoe UI", 13),
            fg="#c0c0c0",
            bg=PREVIEW_BG,
        )
        self._watermark.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
