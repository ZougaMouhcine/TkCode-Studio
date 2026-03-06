"""Code editor panel for TkLearn Studio.

Provides a scrollable text editor with line numbers, monospace font,
and a styled header for writing Tkinter code.
"""

import tkinter as tk
from tkinter import ttk

from src.utils.constants import (
    EDITOR_BG,
    EDITOR_FG,
    EDITOR_FONT,
    EDITOR_INSERT_COLOR,
    EDITOR_SELECT_BG,
    EDITOR_SELECT_FG,
    EDITOR_LINE_BG,
    EDITOR_LINE_FG,
    EDITOR_HEADER_BG,
    EDITOR_ACCENT,
    HEADER_FONT,
    BG_BORDER,
    FG_PRIMARY,
)


class EditorFrame(ttk.Frame):
    """A code editor frame with line numbers, Text widget, and scrollbar."""

    def __init__(self, parent, **kwargs):
        """Initialize the editor frame.

        Args:
            parent: The parent widget.
        """
        super().__init__(parent, **kwargs)
        self._build_ui()

    def _build_ui(self):
        """Construct the editor UI components."""
        # ── Colored header bar ──
        header_bar = tk.Frame(self, bg=EDITOR_HEADER_BG, height=32)
        header_bar.pack(side=tk.TOP, fill=tk.X)
        header_bar.pack_propagate(False)

        # Accent stripe on left
        accent = tk.Frame(header_bar, bg=EDITOR_ACCENT, width=4)
        accent.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(
            header_bar,
            text="  \u270E  Code Editor",
            font=HEADER_FONT,
            bg=EDITOR_HEADER_BG,
            fg=EDITOR_ACCENT,
            anchor=tk.W,
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)

        # Thin border below header
        tk.Frame(self, bg=EDITOR_ACCENT, height=1).pack(side=tk.TOP, fill=tk.X)

        # ── Main editing area ──
        container = tk.Frame(self, bg=EDITOR_BG)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self._scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL)
        self._scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Line number gutter
        self._line_numbers = tk.Text(
            container,
            width=4,
            bg=EDITOR_LINE_BG,
            fg=EDITOR_LINE_FG,
            font=EDITOR_FONT,
            state=tk.DISABLED,
            padx=4,
            pady=8,
            bd=0,
            highlightthickness=0,
            takefocus=0,
        )
        self._line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Gutter border
        tk.Frame(container, bg=BG_BORDER, width=1).pack(side=tk.LEFT, fill=tk.Y)

        self._text = tk.Text(
            container,
            wrap=tk.NONE,
            font=EDITOR_FONT,
            bg=EDITOR_BG,
            fg=EDITOR_FG,
            insertbackground=EDITOR_INSERT_COLOR,
            insertwidth=2,
            selectbackground=EDITOR_SELECT_BG,
            selectforeground=EDITOR_SELECT_FG,
            undo=True,
            padx=10,
            pady=8,
            bd=0,
            highlightthickness=0,
            yscrollcommand=self._on_scroll,
        )
        self._text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._scrollbar.config(command=self._on_scrollbar)

        # Horizontal scrollbar
        h_scroll = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self._text.xview)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self._text.config(xscrollcommand=h_scroll.set)

        # Bind events for updating line numbers
        self._text.bind("<KeyRelease>", lambda e: self._update_line_numbers())
        self._text.bind("<MouseWheel>", lambda e: self.after(1, self._update_line_numbers))
        self._text.bind("<<Modified>>", self._on_modified)

    # ── Scrolling ──

    def _on_scroll(self, *args):
        """Sync scrollbar and line numbers on text scroll."""
        self._scrollbar.set(*args)
        self._line_numbers.yview_moveto(args[0])

    def _on_scrollbar(self, *args):
        """Handle scrollbar dragging."""
        self._text.yview(*args)
        self._line_numbers.yview(*args)

    def _on_modified(self, _event=None):
        """Handle text modification to refresh line numbers."""
        self._text.edit_modified(False)
        self._update_line_numbers()

    def _update_line_numbers(self):
        """Redraw line numbers to match current text content."""
        self._line_numbers.config(state=tk.NORMAL)
        self._line_numbers.delete("1.0", tk.END)

        line_count = int(self._text.index("end-1c").split(".")[0])
        numbers = "\n".join(str(i) for i in range(1, line_count + 1))
        self._line_numbers.insert("1.0", numbers)

        self._line_numbers.config(state=tk.DISABLED)
        # Keep gutter in sync with text scroll position
        self._line_numbers.yview_moveto(self._text.yview()[0])

    # ── Public API ──

    def get_code(self):
        """Return the current code from the editor.

        Returns:
            str: The text content of the editor.
        """
        return self._text.get("1.0", tk.END).rstrip("\n")

    def set_code(self, code):
        """Replace all editor content with the given code.

        Args:
            code: The code string to insert into the editor.
        """
        self._text.delete("1.0", tk.END)
        self._text.insert("1.0", code)
        self._update_line_numbers()

    def clear(self):
        """Clear all text from the editor."""
        self._text.delete("1.0", tk.END)
        self._update_line_numbers()
