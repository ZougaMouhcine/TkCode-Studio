"""Menu bar for TkLearn Studio.

Builds the application menu bar with File, Lessons, Execution,
Tools, and Help menus. Fully decoupled via a callbacks dictionary.
"""

import tkinter as tk

from src.utils.constants import MENU_BG, MENU_FG, MENU_ACTIVE_BG, MENU_ACTIVE_FG, UI_FONT


def _styled_menu(parent):
    """Create a consistently styled submenu."""
    return tk.Menu(
        parent,
        tearoff=0,
        bg=MENU_BG,
        fg=MENU_FG,
        activebackground=MENU_ACTIVE_BG,
        activeforeground=MENU_ACTIVE_FG,
        font=UI_FONT,
        relief=tk.FLAT,
        bd=0,
    )


class MenuBar:
    """Builds and attaches a menu bar to the application window."""

    def __init__(self, root, callbacks):
        """Initialize the menu bar.

        Args:
            root: The main Tk window to attach the menu to.
            callbacks: A dict mapping action names to callables.
                Expected keys:
                    new, open, save, quit,
                    lesson_empty, lesson_labels, lesson_buttons,
                    lesson_entry, lesson_grid,
                    run, reset_preview,
                    color_picker,
                    documentation, about
        """
        self._root = root
        self._callbacks = callbacks
        self._menubar = tk.Menu(
            root,
            bg=MENU_BG,
            fg=MENU_FG,
            activebackground=MENU_ACTIVE_BG,
            activeforeground=MENU_ACTIVE_FG,
            font=UI_FONT,
            relief=tk.FLAT,
            bd=0,
        )
        self._build_file_menu()
        self._build_lessons_menu()
        self._build_execution_menu()
        self._build_tools_menu()
        self._build_help_menu()
        root.config(menu=self._menubar)

    def _build_file_menu(self):
        """Build the File menu."""
        menu = _styled_menu(self._menubar)
        menu.add_command(label="  \U0001F4C4  New", command=self._callbacks.get("new"), accelerator="Ctrl+N")
        menu.add_command(label="  \U0001F4C2  Open...", command=self._callbacks.get("open"), accelerator="Ctrl+O")
        menu.add_command(label="  \U0001F4BE  Save", command=self._callbacks.get("save"), accelerator="Ctrl+S")
        menu.add_separator()
        menu.add_command(label="  \u2716  Quit", command=self._callbacks.get("quit"), accelerator="Alt+F4")
        self._menubar.add_cascade(label=" File ", menu=menu)

    def _build_lessons_menu(self):
        """Build the Lessons menu."""
        menu = _styled_menu(self._menubar)
        menu.add_command(label="  \u25A1  Empty Window", command=self._callbacks.get("lesson_empty"))
        menu.add_command(label="  \U0001F3F7  Labels", command=self._callbacks.get("lesson_labels"))
        menu.add_command(label="  \U0001F518  Buttons", command=self._callbacks.get("lesson_buttons"))
        menu.add_command(label="  \u270D  Entry Fields", command=self._callbacks.get("lesson_entry"))
        menu.add_command(label="  \u2B1C  Grid Layout", command=self._callbacks.get("lesson_grid"))
        self._menubar.add_cascade(label=" Lessons ", menu=menu)

    def _build_execution_menu(self):
        """Build the Execution menu."""
        menu = _styled_menu(self._menubar)
        menu.add_command(label="  \u25B6  Run", command=self._callbacks.get("run"), accelerator="F5")
        menu.add_command(label="  \u27F3  Reset Preview", command=self._callbacks.get("reset_preview"))
        self._menubar.add_cascade(label=" Execution ", menu=menu)

    def _build_tools_menu(self):
        """Build the Tools menu."""
        menu = _styled_menu(self._menubar)
        menu.add_command(label="  \U0001F3A8  Color Picker", command=self._callbacks.get("color_picker"))
        self._menubar.add_cascade(label=" Tools ", menu=menu)

    def _build_help_menu(self):
        """Build the Help menu."""
        menu = _styled_menu(self._menubar)
        menu.add_command(label="  \U0001F4D6  Documentation", command=self._callbacks.get("documentation"))
        menu.add_command(label="  \u2139  About", command=self._callbacks.get("about"))
        self._menubar.add_cascade(label=" Help ", menu=menu)
