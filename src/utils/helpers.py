"""Utility helper functions for TkLearn Studio."""

import datetime


def center_window(window, width, height):
    """Center a Tkinter window on the screen.

    Args:
        window: The Tkinter window (Tk or Toplevel) to center.
        width: Desired window width.
        height: Desired window height.
    """
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def timestamp():
    """Return the current time as a formatted string.

    Returns:
        str: Timestamp in HH:MM:SS format.
    """
    return datetime.datetime.now().strftime("%H:%M:%S")
