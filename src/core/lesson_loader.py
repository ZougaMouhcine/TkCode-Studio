"""Lesson loader for TkLearn Studio.

Provides access to predefined lesson code snippets that demonstrate
various Tkinter widgets and layout techniques.
"""

from lessons.lesson_label import CODE as LABEL_CODE
from lessons.lesson_button import CODE as BUTTON_CODE
from lessons.lesson_entry import CODE as ENTRY_CODE
from lessons.lesson_grid import CODE as GRID_CODE


# Lesson: Empty window (minimal inline snippet)
_EMPTY_CODE = '''# Empty Window
# 'root' is the preview frame — add your widgets here!
# 'window' is the top-level Tk window (for key bindings, title, etc.)

lbl = tk.Label(root, text="Start coding!", font=("Arial", 16))
lbl.pack(expand=True)
'''


class LessonLoader:
    """Registry of lesson names to their source code strings."""

    LESSONS = {
        "empty": _EMPTY_CODE,
        "labels": LABEL_CODE,
        "buttons": BUTTON_CODE,
        "entry": ENTRY_CODE,
        "grid": GRID_CODE,
    }

    @classmethod
    def load_lesson(cls, name):
        """Return the code string for the named lesson.

        Args:
            name: The lesson key (e.g. "labels", "buttons").

        Returns:
            str: The lesson source code.

        Raises:
            KeyError: If the lesson name is not found.
        """
        return cls.LESSONS[name]

    @classmethod
    def available_lessons(cls):
        """Return a list of available lesson names.

        Returns:
            list[str]: Sorted list of lesson keys.
        """
        return sorted(cls.LESSONS.keys())
