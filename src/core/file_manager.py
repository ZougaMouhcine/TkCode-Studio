"""File manager for TkLearn Studio.

Handles opening, saving, and creating new script files
using Tkinter file dialogs.
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox

from src.utils.constants import PYTHON_FILE_TYPES


class FileManager:
    """Manages file I/O operations for the code editor."""

    def __init__(self):
        """Initialize the file manager with no active file."""
        self.current_filepath = None

    def new_file(self, editor):
        """Clear the editor and reset the current file path.

        Args:
            editor: The EditorFrame instance to clear.
        """
        editor.clear()
        self.current_filepath = None

    def open_file(self, editor):
        """Open a Python file and load its contents into the editor.

        Args:
            editor: The EditorFrame instance to load code into.

        Returns:
            str or None: The file path that was opened, or None if cancelled.
        """
        filepath = filedialog.askopenfilename(
            title="Open Script",
            filetypes=PYTHON_FILE_TYPES,
        )
        if not filepath:
            return None

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except OSError as e:
            messagebox.showerror("Error", f"Could not open file:\n{e}")
            return None

        editor.set_code(content)
        self.current_filepath = filepath
        return filepath

    def save_file(self, editor):
        """Save the editor contents to the current file, or prompt for a path.

        Args:
            editor: The EditorFrame instance to save code from.

        Returns:
            str or None: The file path saved to, or None if cancelled.
        """
        if self.current_filepath:
            return self._write_file(self.current_filepath, editor.get_code())
        return self.save_file_as(editor)

    def save_file_as(self, editor):
        """Prompt the user for a file path and save the editor contents.

        Args:
            editor: The EditorFrame instance to save code from.

        Returns:
            str or None: The file path saved to, or None if cancelled.
        """
        filepath = filedialog.asksaveasfilename(
            title="Save Script As",
            defaultextension=".py",
            filetypes=PYTHON_FILE_TYPES,
        )
        if not filepath:
            return None

        result = self._write_file(filepath, editor.get_code())
        if result:
            self.current_filepath = filepath
        return result

    @staticmethod
    def _write_file(filepath, content):
        """Write content to a file on disk.

        Args:
            filepath: The destination file path.
            content: The string content to write.

        Returns:
            str or None: The file path on success, None on failure.
        """
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")
            return None
        return filepath
