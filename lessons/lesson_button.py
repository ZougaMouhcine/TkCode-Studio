"""Lesson: Button Widget Demo.

Demonstrates creating buttons with various styles and command callbacks.
"""

CODE = '''# Lesson: Button Widget
# Demonstrates buttons with commands and styling

import tkinter as tk

# Click counter
counter = {"count": 0}

def on_click():
    counter["count"] += 1
    result_label.config(text=f"Button clicked {counter['count']} time(s)")

# Title
tk.Label(root, text="Button Demo", font=("Arial", 16, "bold")).pack(pady=10)

# Standard button
btn1 = tk.Button(
    root,
    text="Click Me!",
    command=on_click,
    font=("Arial", 12),
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    padx=20,
    pady=8,
    cursor="hand2",
)
btn1.pack(pady=10)

# Result label
result_label = tk.Label(root, text="Button not clicked yet", font=("Arial", 11))
result_label.pack(pady=5)

# Different button styles
styles_frame = tk.Frame(root)
styles_frame.pack(pady=15)

tk.Label(styles_frame, text="Button Styles:", font=("Arial", 12, "bold")).pack(pady=5)

button_configs = [
    ("Flat", tk.FLAT, "#2196F3", "white"),
    ("Raised", tk.RAISED, "#FF9800", "white"),
    ("Sunken", tk.SUNKEN, "#9C27B0", "white"),
    ("Ridge", tk.RIDGE, "#f44336", "white"),
    ("Groove", tk.GROOVE, "#607D8B", "white"),
]

row = tk.Frame(styles_frame)
row.pack(pady=5)

for text, relief, bg, fg in button_configs:
    tk.Button(
        row,
        text=text,
        relief=relief,
        bg=bg,
        fg=fg,
        font=("Arial", 10),
        padx=10,
        pady=4,
    ).pack(side=tk.LEFT, padx=4)

# Disabled button example
tk.Button(
    root,
    text="Disabled Button",
    state=tk.DISABLED,
    font=("Arial", 10),
).pack(pady=10)
'''
