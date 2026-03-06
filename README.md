# TkLearn Studio

An interactive learning sandbox for Tkinter — write Python GUI code and instantly see the graphical result.

## Features

- **Live Code Editor** — Write Tkinter code with a monospace text editor (Consolas font, dark theme)
- **Instant Preview** — Execute your code and see rendered widgets in the preview panel
- **Error Console** — Python errors and `print()` output display in the console panel
- **Built-in Lessons** — Pre-loaded examples for Labels, Buttons, Entry fields, and Grid layout
- **File Management** — New / Open / Save scripts via the File menu
- **Color Picker** — Built-in color chooser tool (Tools → Color Picker)
- **Keyboard Shortcuts** — F5 to Run, Ctrl+N / Ctrl+O / Ctrl+S for file operations
- **Responsive Layout** — Resizable PanedWindow with draggable sash

## Requirements

- Python 3.11 or higher
- No external dependencies — uses only the Python standard library (Tkinter)

## How to Run

```bash
cd tklearn_studio
python main.py
```

## Project Structure

```
tklearn_studio/
│
├── main.py                    # Application entry point
├── README.md                  # This file
├── requirements.txt           # Dependencies (stdlib only)
│
├── assets/
│   ├── icons/                 # Placeholder for toolbar icons
│   └── images/                # Placeholder for UI images
│
├── lessons/
│   ├── __init__.py
│   ├── lesson_label.py        # Label widget lesson
│   ├── lesson_button.py       # Button widget lesson
│   ├── lesson_entry.py        # Entry widget lesson
│   └── lesson_grid.py         # Grid layout lesson
│
├── data/
│   ├── examples/              # Example scripts
│   └── saved_scripts/         # User-saved scripts
│
└── src/
    ├── __init__.py
    │
    ├── ui/
    │   ├── __init__.py
    │   ├── editor.py           # Code editor panel (EditorFrame)
    │   ├── preview.py          # Widget preview panel (PreviewFrame)
    │   ├── console.py          # Output console panel (ConsoleFrame)
    │   └── menus.py            # Menu bar builder (MenuBar)
    │
    ├── core/
    │   ├── __init__.py
    │   ├── executor.py         # Code execution engine (run_code)
    │   ├── file_manager.py     # File I/O operations (FileManager)
    │   └── lesson_loader.py    # Lesson loading registry (LessonLoader)
    │
    └── utils/
        ├── __init__.py
        ├── constants.py        # Application-wide constants
        └── helpers.py          # Utility functions
```

## Usage Guide

1. **Write code** in the left editor panel. Use `root` as the parent widget.
2. **Press F5** or click the **Run** button to execute your code.
3. **View output** — rendered widgets appear in the right preview panel.
4. **Check errors** — any Python exceptions appear in the bottom console.
5. **Load lessons** — use the Lessons menu or the Load Lesson toolbar button.

### Example Code

```python
import tkinter as tk

lbl = tk.Label(root, text="Hello, World!", font=("Arial", 20))
lbl.pack(expand=True)
```

## Menus

| Menu       | Actions                                            |
|------------|-----------------------------------------------------|
| File       | New, Open, Save, Quit                               |
| Lessons    | Empty Window, Labels, Buttons, Entry Fields, Grid   |
| Execution  | Run (F5), Reset Preview                             |
| Tools      | Color Picker                                        |
| Help       | Documentation, About                                |

## License

Educational project — free to use and modify.
