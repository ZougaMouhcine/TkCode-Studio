"""Lesson: Label Widget Demo.

Demonstrates creating and styling Label widgets in Tkinter.
"""

CODE = '''# Lesson: Label Widget
# Demonstrates different Label styles and configurations

import tkinter as tk

# Simple label
lbl1 = tk.Label(root, text="Hello, Tkinter!", font=("Arial", 18, "bold"))
lbl1.pack(pady=10)

# Styled label with background color
lbl2 = tk.Label(
    root,
    text="Styled Label",
    bg="lightblue",
    fg="darkblue",
    font=("Arial", 14),
    padx=20,
    pady=10,
    relief=tk.RAISED,
    bd=2,
)
lbl2.pack(pady=10)

# Label with wrapping text
long_text = (
    "This is a longer label that demonstrates text wrapping. "
    "Labels can display multi-line text by setting the wraplength option."
)
lbl3 = tk.Label(
    root,
    text=long_text,
    wraplength=300,
    justify=tk.LEFT,
    font=("Arial", 11),
    bg="#ffffcc",
    padx=10,
    pady=10,
)
lbl3.pack(pady=10, padx=20, fill=tk.X)

# Multiple colored labels in a row
frame = tk.Frame(root)
frame.pack(pady=10)

colors = ["#ff6b6b", "#69ff94", "#6bc5ff", "#ffd93d", "#c084fc"]
for i, color in enumerate(colors):
    tk.Label(
        frame,
        text=f" Color {i+1} ",
        bg=color,
        font=("Arial", 10, "bold"),
        padx=8,
        pady=4,
    ).pack(side=tk.LEFT, padx=2)
'''
