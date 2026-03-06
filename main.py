"""TkLearn Studio — Interactive Tkinter Learning Sandbox.

This is the main entry point of the application.  It assembles all UI
components (editor, preview, console, menus, toolbar) and wires them
to the core logic (executor, file manager, lesson loader).

Usage:
    python main.py
"""

import tkinter as tk
from tkinter import ttk, colorchooser, messagebox

from src.ui.editor import EditorFrame
from src.ui.preview import PreviewFrame
from src.ui.console import ConsoleFrame
from src.ui.menus import MenuBar
from src.core.executor import run_code
from src.core.file_manager import FileManager
from src.core.lesson_loader import LessonLoader
from src.utils.constants import (
    APP_TITLE,
    APP_VERSION,
    DEFAULT_GEOMETRY,
    MIN_HEIGHT,
    MIN_WIDTH,
    UI_FONT,
    UI_FONT_BOLD,
    HEADER_FONT,
    STATUS_FONT,
    BG_DARKEST,
    BG_DARK,
    BG_MID,
    BG_LIGHT,
    BG_BORDER,
    FG_PRIMARY,
    FG_SECONDARY,
    ACCENT_BLUE,
    ACCENT_GREEN,
    ACCENT_PURPLE,
    TOOLBAR_BG,
    TOOLBAR_BUTTON_FG,
    BTN_RUN_BG,
    BTN_RUN_HOVER,
    BTN_CLEAR_BG,
    BTN_CLEAR_HOVER,
    BTN_SAVE_BG,
    BTN_SAVE_HOVER,
    BTN_LESSON_BG,
    BTN_LESSON_HOVER,
    STATUS_BG,
    STATUS_FG,
    SASH_BG,
    SASH_WIDTH,
)
from src.utils.helpers import center_window


class TkLearnStudio(tk.Tk):
    """Main application window for TkLearn Studio."""

    def __init__(self):
        """Initialize the main application."""
        super().__init__()

        self.title(f"{APP_TITLE} v{APP_VERSION}")
        self.geometry(DEFAULT_GEOMETRY)
        self.minsize(MIN_WIDTH, MIN_HEIGHT)
        self.configure(bg=BG_DARK)
        center_window(self, 1200, 700)

        self._file_manager = FileManager()

        self._configure_ttk_theme()
        self._build_ui()
        self._build_menu()
        self._bind_shortcuts()

        # Load a welcome snippet into the editor
        self.editor.set_code(
            '# Welcome to TkLearn Studio!\n'
            '# Write your Tkinter code here and press F5 or click Run.\n'
            '# The variable "root" is your parent widget.\n\n'
            'import tkinter as tk\n\n'
            'lbl = tk.Label(root, text="Hello, TkLearn Studio!", '
            'font=("Arial", 18, "bold"))\n'
            'lbl.pack(expand=True)\n'
        )
        self._update_status("Ready")

    # ------------------------------------------------------------------ #
    #  Theme Configuration
    # ------------------------------------------------------------------ #

    def _configure_ttk_theme(self):
        """Configure ttk styles for a dark, modern appearance."""
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(".", background=BG_DARK, foreground=FG_PRIMARY, font=UI_FONT)
        style.configure("TFrame", background=BG_DARK)
        style.configure("TLabel", background=BG_DARK, foreground=FG_PRIMARY)
        style.configure("TButton", background=BG_LIGHT, foreground=FG_PRIMARY, padding=6)
        style.map(
            "TButton",
            background=[("active", BG_MID)],
            foreground=[("active", FG_PRIMARY)],
        )
        style.configure(
            "Vertical.TScrollbar",
            background=BG_LIGHT,
            troughcolor=BG_DARKEST,
            arrowcolor=FG_SECONDARY,
            borderwidth=0,
        )
        style.configure(
            "Horizontal.TScrollbar",
            background=BG_LIGHT,
            troughcolor=BG_DARKEST,
            arrowcolor=FG_SECONDARY,
            borderwidth=0,
        )

    # ------------------------------------------------------------------ #
    #  UI Construction
    # ------------------------------------------------------------------ #

    def _build_ui(self):
        """Build the main application layout."""
        # ── Title bar accent line ──
        tk.Frame(self, bg=ACCENT_BLUE, height=2).pack(side=tk.TOP, fill=tk.X)

        # ── Toolbar ──
        toolbar = tk.Frame(self, bg=TOOLBAR_BG, height=44)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        toolbar.pack_propagate(False)

        # App branding in toolbar
        tk.Label(
            toolbar,
            text=f"  \u2B22 {APP_TITLE}",
            font=("Segoe UI", 11, "bold"),
            bg=TOOLBAR_BG,
            fg=ACCENT_BLUE,
        ).pack(side=tk.LEFT, padx=(8, 20))

        # Separator
        tk.Frame(toolbar, bg=BG_BORDER, width=1).pack(side=tk.LEFT, fill=tk.Y, pady=8)

        # --- Colored toolbar buttons ---
        self._make_toolbar_btn(
            toolbar, "\u25B6  Run", BTN_RUN_BG, BTN_RUN_HOVER, self._on_run
        )
        self._make_toolbar_btn(
            toolbar, "\u2716  Clear", BTN_CLEAR_BG, BTN_CLEAR_HOVER, self._on_clear
        )
        self._make_toolbar_btn(
            toolbar, "\U0001F4BE  Save", BTN_SAVE_BG, BTN_SAVE_HOVER, self._on_save
        )
        self._make_toolbar_btn(
            toolbar, "\U0001F4D6  Lessons", BTN_LESSON_BG, BTN_LESSON_HOVER,
            self._on_load_lesson_dialog,
        )

        # Right-side shortcut hint
        tk.Label(
            toolbar,
            text="F5 = Run  ",
            font=STATUS_FONT,
            bg=TOOLBAR_BG,
            fg=FG_SECONDARY,
        ).pack(side=tk.RIGHT, padx=10)

        # ── Thin separator under toolbar ──
        tk.Frame(self, bg=BG_BORDER, height=1).pack(side=tk.TOP, fill=tk.X)

        # ── Status bar (bottom) ──
        self._status_bar = tk.Frame(self, bg=STATUS_BG, height=22)
        self._status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self._status_bar.pack_propagate(False)

        self._status_label = tk.Label(
            self._status_bar,
            text=f"  \u25CF {APP_TITLE} v{APP_VERSION}",
            font=STATUS_FONT,
            bg=STATUS_BG,
            fg=STATUS_FG,
            anchor=tk.W,
        )
        self._status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)

        self._status_right = tk.Label(
            self._status_bar,
            text="Python 3 \u2022 Tkinter  ",
            font=STATUS_FONT,
            bg=STATUS_BG,
            fg=STATUS_FG,
            anchor=tk.E,
        )
        self._status_right.pack(side=tk.RIGHT, padx=4)

        # ── Console (above status bar) ──
        self.console = ConsoleFrame(self)
        self.console.pack(side=tk.BOTTOM, fill=tk.X)

        # ── Main PanedWindow (editor | preview) ──
        paned = tk.PanedWindow(
            self,
            orient=tk.HORIZONTAL,
            sashwidth=SASH_WIDTH,
            bg=SASH_BG,
            bd=0,
            opaqueresize=True,
        )
        paned.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.editor = EditorFrame(paned)
        self.preview = PreviewFrame(paned)

        paned.add(self.editor, minsize=300, stretch="always")
        paned.add(self.preview, minsize=250, stretch="always")

    @staticmethod
    def _make_toolbar_btn(parent, text, bg_color, hover_color, command):
        """Create a styled, colored toolbar button with hover effect.

        Args:
            parent: The toolbar frame.
            text: Button label text.
            bg_color: Normal background color.
            hover_color: Background color on hover.
            command: Callback function.
        """
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 9, "bold"),
            bg=bg_color,
            fg="#ffffff",
            activebackground=hover_color,
            activeforeground="#ffffff",
            bd=0,
            padx=16,
            pady=4,
            cursor="hand2",
            relief=tk.FLAT,
        )
        btn.pack(side=tk.LEFT, padx=(8, 2), pady=7)

        # Hover effect
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))

    def _build_menu(self):
        """Build the menu bar and connect callbacks."""
        callbacks = {
            "new": self._on_new,
            "open": self._on_open,
            "save": self._on_save,
            "quit": self._on_quit,
            "lesson_empty": lambda: self._load_lesson("empty"),
            "lesson_labels": lambda: self._load_lesson("labels"),
            "lesson_buttons": lambda: self._load_lesson("buttons"),
            "lesson_entry": lambda: self._load_lesson("entry"),
            "lesson_grid": lambda: self._load_lesson("grid"),
            "run": self._on_run,
            "reset_preview": self._on_reset_preview,
            "color_picker": self._on_color_picker,
            "documentation": self._on_documentation,
            "about": self._on_about,
        }
        MenuBar(self, callbacks)

    def _bind_shortcuts(self):
        """Bind keyboard shortcuts."""
        self.bind("<F5>", lambda e: self._on_run())
        self.bind("<Control-n>", lambda e: self._on_new())
        self.bind("<Control-o>", lambda e: self._on_open())
        self.bind("<Control-s>", lambda e: self._on_save())

    def _update_status(self, message):
        """Update the status bar text."""
        self._status_label.config(text=f"  \u25CF {message}")

    # ------------------------------------------------------------------ #
    #  Callbacks
    # ------------------------------------------------------------------ #

    def _on_run(self):
        """Execute the code from the editor in the preview area."""
        code = self.editor.get_code()
        self._update_status("Running...")
        run_code(code, self.preview.preview_container, self.console)
        self._update_status("Execution complete")

    def _on_clear(self):
        """Clear the editor, preview, and console."""
        self.editor.clear()
        self.preview.clear_preview()
        self.console.clear()

    def _on_new(self):
        """Create a new empty script."""
        self._file_manager.new_file(self.editor)
        self.preview.clear_preview()
        self.console.clear()
        self.console.log_info("New file created.")
        self._update_status("New file")

    def _on_open(self):
        """Open a Python file into the editor."""
        path = self._file_manager.open_file(self.editor)
        if path:
            self.console.log_info(f"Opened: {path}")
            self._update_status(f"Opened: {path}")

    def _on_save(self):
        """Save the current editor contents."""
        path = self._file_manager.save_file(self.editor)
        if path:
            self.console.log(f"Saved: {path}")
            self._update_status(f"Saved: {path}")

    def _on_quit(self):
        """Exit the application."""
        self.destroy()

    def _on_reset_preview(self):
        """Clear the preview area."""
        self.preview.clear_preview()
        self.console.log_info("Preview reset.")

    def _on_color_picker(self):
        """Open a color picker dialog and log the selected color."""
        result = colorchooser.askcolor(title="Pick a Color")
        if result and result[1]:
            hex_color = result[1]
            self.console.log(f"Selected color: {hex_color}")

    def _on_documentation(self):
        """Show documentation info."""
        messagebox.showinfo(
            "Documentation",
            "TkLearn Studio — Interactive Tkinter Sandbox\n\n"
            "Write Tkinter code in the editor panel.\n"
            "Press F5 or click Run to see results in the preview panel.\n"
            "Errors are displayed in the console below.\n\n"
            "Use the Lessons menu to load example code.\n"
            "Use 'root' as the parent widget in your code.",
        )

    def _on_about(self):
        """Show the About dialog."""
        messagebox.showinfo(
            "About",
            f"{APP_TITLE} v{APP_VERSION}\n\n"
            "An interactive learning sandbox for Tkinter.\n"
            "Built with Python and Tkinter.",
        )

    def _load_lesson(self, name):
        """Load a lesson by name into the editor.

        Args:
            name: The lesson key to load.
        """
        try:
            code = LessonLoader.load_lesson(name)
        except KeyError:
            self.console.log_error(f"Lesson '{name}' not found.")
            return
        self.editor.set_code(code)
        self.preview.clear_preview()
        self.console.log_info(f"Lesson '{name}' loaded. Press F5 to run.")
        self._update_status(f"Lesson: {name}")

    def _on_load_lesson_dialog(self):
        """Show a styled dialog to pick a lesson."""
        dialog = tk.Toplevel(self)
        dialog.title("Load Lesson")
        dialog.geometry("340x320")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(bg=BG_DARK)

        # Header
        header = tk.Frame(dialog, bg=ACCENT_PURPLE, height=50)
        header.pack(side=tk.TOP, fill=tk.X)
        header.pack_propagate(False)
        tk.Label(
            header,
            text="\U0001F4D6  Choose a Lesson",
            font=("Segoe UI", 13, "bold"),
            bg=ACCENT_PURPLE,
            fg="#ffffff",
        ).pack(expand=True)

        # Body
        body = tk.Frame(dialog, bg=BG_DARK, padx=20, pady=15)
        body.pack(fill=tk.BOTH, expand=True)

        lessons = [
            ("\u25A1  Empty Window", "empty", "#6e7681"),
            ("\U0001F3F7  Labels", "labels", ACCENT_BLUE),
            ("\U0001F518  Buttons", "buttons", ACCENT_GREEN),
            ("\u270D  Entry Fields", "entry", "#d29922"),
            ("\u2B1C  Grid Layout", "grid", ACCENT_PURPLE),
        ]

        for label, key, color in lessons:
            btn = tk.Button(
                body,
                text=f"  {label}",
                font=UI_FONT_BOLD,
                bg=BG_LIGHT,
                fg=FG_PRIMARY,
                activebackground=color,
                activeforeground="#ffffff",
                anchor=tk.W,
                bd=0,
                padx=12,
                pady=8,
                cursor="hand2",
                relief=tk.FLAT,
                command=lambda k=key: (self._load_lesson(k), dialog.destroy()),
            )
            btn.pack(fill=tk.X, pady=3)
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=c, fg="#ffffff"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=BG_LIGHT, fg=FG_PRIMARY))


# ------------------------------------------------------------------ #
#  Entry point
# ------------------------------------------------------------------ #

def main():
    """Launch TkLearn Studio."""
    app = TkLearnStudio()
    app.mainloop()


if __name__ == "__main__":
    main()
