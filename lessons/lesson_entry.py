"""Lesson: Entry Widget Demo.

Demonstrates Entry widgets combined with Labels and Buttons
to create a simple interactive form.
"""

CODE = '''# Lesson: Entry Fields
# Demonstrates Entry widgets with Labels and Buttons

import tkinter as tk

tk.Label(root, text="Entry Fields Demo", font=("Arial", 16, "bold")).pack(pady=10)

# --- Simple input ---
frame1 = tk.Frame(root)
frame1.pack(pady=5, padx=20, fill=tk.X)

tk.Label(frame1, text="Your Name:", font=("Arial", 11)).pack(side=tk.LEFT)
name_entry = tk.Entry(frame1, font=("Arial", 11), width=25)
name_entry.pack(side=tk.LEFT, padx=10)

# --- Greeting output ---
greeting_label = tk.Label(root, text="", font=("Arial", 12), fg="green")
greeting_label.pack(pady=5)

def greet():
    name = name_entry.get().strip()
    if name:
        greeting_label.config(text=f"Hello, {name}! Welcome to TkLearn Studio!")
    else:
        greeting_label.config(text="Please enter your name.", fg="red")

tk.Button(
    root,
    text="Greet",
    command=greet,
    font=("Arial", 11),
    bg="#4CAF50",
    fg="white",
    padx=15,
    pady=4,
    cursor="hand2",
).pack(pady=5)

# --- Password entry ---
frame2 = tk.Frame(root)
frame2.pack(pady=10, padx=20, fill=tk.X)

tk.Label(frame2, text="Password:", font=("Arial", 11)).pack(side=tk.LEFT)
pass_entry = tk.Entry(frame2, font=("Arial", 11), width=25, show="*")
pass_entry.pack(side=tk.LEFT, padx=10)

# --- Read-only entry ---
frame3 = tk.Frame(root)
frame3.pack(pady=5, padx=20, fill=tk.X)

tk.Label(frame3, text="Read-only:", font=("Arial", 11)).pack(side=tk.LEFT)
ro_entry = tk.Entry(frame3, font=("Arial", 11), width=25, state="readonly")
ro_entry.pack(side=tk.LEFT, padx=10)

# Insert default text into read-only (must toggle state)
ro_entry.config(state=tk.NORMAL)
ro_entry.insert(0, "You cannot edit this text")
ro_entry.config(state="readonly")
'''
