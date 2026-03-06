"""Console output panel for TkLearn Studio.

Provides a read-only text console for displaying execution logs,
success messages, and Python error tracebacks.
"""

import tkinter as tk
from tkinter import ttk

from src.utils.constants import (
    CONSOLE_BG,
    CONSOLE_ERROR_FG,
    CONSOLE_FG,
    CONSOLE_FONT,
    CONSOLE_SUCCESS_FG,
    CONSOLE_INFO_FG,
    CONSOLE_TIMESTAMP_FG,
    CONSOLE_HEADER_BG,
    CONSOLE_ACCENT,
    HEADER_FONT,
    BG_BORDER,
)
from src.utils.helpers import timestamp


class ConsoleFrame(ttk.Frame):
    """A read-only console frame for displaying execution output."""

    def __init__(self, parent, **kwargs):
        """Initialize the console frame.

        Args:
            parent: The parent widget.
        """
        super().__init__(parent, **kwargs)
        self._build_ui()

    def _build_ui(self):
        """Construct the console UI components."""
        # ── Colored header bar ──
        header_bar = tk.Frame(self, bg=CONSOLE_HEADER_BG, height=28)
        header_bar.pack(side=tk.TOP, fill=tk.X)
        header_bar.pack_propagate(False)

        accent = tk.Frame(header_bar, bg=CONSOLE_ACCENT, width=4)
        accent.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(
            header_bar,
            text="  \u2630  Console",
            font=HEADER_FONT,
            bg=CONSOLE_HEADER_BG,
            fg=CONSOLE_ACCENT,
            anchor=tk.W,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)

        # Accent line
        tk.Frame(self, bg=CONSOLE_ACCENT, height=1).pack(side=tk.TOP, fill=tk.X)

        container = tk.Frame(self, bg=CONSOLE_BG)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._text = tk.Text(
            container,
            wrap=tk.WORD,
            font=CONSOLE_FONT,
            bg=CONSOLE_BG,
            fg=CONSOLE_FG,
            state=tk.DISABLED,
            height=8,
            padx=10,
            pady=6,
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set,
        )
        self._text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self._text.yview)

        # Configure text tags for colored output
        self._text.tag_config("error", foreground=CONSOLE_ERROR_FG, font=("Consolas", 10, "bold"))
        self._text.tag_config("success", foreground=CONSOLE_SUCCESS_FG)
        self._text.tag_config("info", foreground=CONSOLE_INFO_FG)
        self._text.tag_config("ts", foreground=CONSOLE_TIMESTAMP_FG)

    def log(self, message):
        """Append a success/info message to the console.

        Args:
            message: The message string to display.
        """
        self._append(f"[{timestamp()}] ", "ts")
        self._append(f"✔ {message}\n", "success")

    def log_error(self, message):
        """Append an error message to the console.

        Args:
            message: The error message string to display.
        """
        self._append(f"[{timestamp()}] ", "ts")
        self._append(f"✘ ERROR:\n{message}\n", "error")

    def log_info(self, message):
        """Append an informational message to the console.

        Args:
            message: The info message string to display.
        """
        self._append(f"[{timestamp()}] ", "ts")
        self._append(f"● {message}\n", "info")

    def clear(self):
        """Clear all text from the console."""
        self._text.config(state=tk.NORMAL)
        self._text.delete("1.0", tk.END)
        self._text.config(state=tk.DISABLED)

    def _append(self, text, tag=None):
        """Append text to the console with an optional tag.

        Args:
            text: The text to append.
            tag: Optional text tag for styling.
        """
        self._text.config(state=tk.NORMAL)
        if tag:
            self._text.insert(tk.END, text, tag)
        else:
            self._text.insert(tk.END, text)
        self._text.config(state=tk.DISABLED)
        self._text.see(tk.END)
