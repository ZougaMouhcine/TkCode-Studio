"""Lesson: Grid Layout Demo.

Demonstrates using the grid geometry manager to create
structured layouts with rows and columns.
"""

CODE = '''# Lesson: Grid Layout
# Demonstrates the grid geometry manager

import tkinter as tk

tk.Label(
    root, text="Grid Layout Demo", font=("Arial", 16, "bold")
).grid(row=0, column=0, columnspan=3, pady=10)

# --- Login form using grid ---
form_frame = tk.LabelFrame(root, text="Login Form", font=("Arial", 12), padx=15, pady=15)
form_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=10, sticky="ew")

tk.Label(form_frame, text="Username:", font=("Arial", 11)).grid(
    row=0, column=0, sticky=tk.W, pady=5
)
tk.Entry(form_frame, font=("Arial", 11), width=20).grid(
    row=0, column=1, padx=10, pady=5
)

tk.Label(form_frame, text="Password:", font=("Arial", 11)).grid(
    row=1, column=0, sticky=tk.W, pady=5
)
tk.Entry(form_frame, font=("Arial", 11), width=20, show="*").grid(
    row=1, column=1, padx=10, pady=5
)

tk.Label(form_frame, text="Email:", font=("Arial", 11)).grid(
    row=2, column=0, sticky=tk.W, pady=5
)
tk.Entry(form_frame, font=("Arial", 11), width=20).grid(
    row=2, column=1, padx=10, pady=5
)

btn_frame = tk.Frame(form_frame)
btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(btn_frame, text="Submit", bg="#4CAF50", fg="white", font=("Arial", 10), padx=15).pack(
    side=tk.LEFT, padx=5
)
tk.Button(btn_frame, text="Cancel", bg="#f44336", fg="white", font=("Arial", 10), padx=15).pack(
    side=tk.LEFT, padx=5
)

# --- Color grid ---
grid_frame = tk.LabelFrame(root, text="Color Grid", font=("Arial", 12), padx=10, pady=10)
grid_frame.grid(row=2, column=0, columnspan=3, padx=20, pady=10, sticky="ew")

colors = [
    ["#ff6b6b", "#ff8e8e", "#ffb3b3"],
    ["#69ff94", "#8effab", "#b3ffc6"],
    ["#6bc5ff", "#8ed4ff", "#b3e3ff"],
]

for r, row_colors in enumerate(colors):
    for c, color in enumerate(row_colors):
        tk.Label(
            grid_frame,
            text=f"({r},{c})",
            bg=color,
            width=10,
            height=2,
            font=("Arial", 9),
            relief=tk.RAISED,
        ).grid(row=r, column=c, padx=3, pady=3)

# Make columns expand evenly
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
'''
