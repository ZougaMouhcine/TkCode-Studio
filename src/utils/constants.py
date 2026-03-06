"""Application-wide constants for TkLearn Studio."""

# Application metadata
APP_TITLE = "TkLearn Studio"
APP_VERSION = "1.0.0"

# Window defaults
DEFAULT_GEOMETRY = "1200x700"
MIN_WIDTH = 800
MIN_HEIGHT = 500

# ── Fonts ──────────────────────────────────────────────────────────
EDITOR_FONT = ("Consolas", 12)
EDITOR_FONT_BOLD = ("Consolas", 12, "bold")
CONSOLE_FONT = ("Consolas", 10)
UI_FONT = ("Segoe UI", 10)
UI_FONT_BOLD = ("Segoe UI", 10, "bold")
HEADER_FONT = ("Segoe UI", 10, "bold")
STATUS_FONT = ("Segoe UI", 9)
TITLE_FONT = ("Segoe UI", 11, "bold")

# ── Base palette ───────────────────────────────────────────────────
BG_DARKEST = "#0d1117"     # deepest background
BG_DARK = "#161b22"        # panels / frames
BG_MID = "#1c2333"         # slightly lighter surface
BG_LIGHT = "#21262d"       # elevated elements
BG_BORDER = "#30363d"      # subtle borders
FG_PRIMARY = "#e6edf3"     # primary text
FG_SECONDARY = "#8b949e"   # muted / secondary text
FG_DIM = "#484f58"         # line numbers, placeholders

# ── Accent colors ──────────────────────────────────────────────────
ACCENT_BLUE = "#58a6ff"    # links, info highlights
ACCENT_GREEN = "#3fb950"   # success, run
ACCENT_RED = "#f85149"     # errors
ACCENT_ORANGE = "#d29922"  # warnings, clear
ACCENT_PURPLE = "#bc8cff"  # lessons, features
ACCENT_CYAN = "#39d2c0"    # special highlights
ACCENT_PINK = "#f778ba"    # decorative

# ── Editor ─────────────────────────────────────────────────────────
EDITOR_BG = BG_DARKEST
EDITOR_FG = FG_PRIMARY
EDITOR_INSERT_COLOR = "#58a6ff"
EDITOR_SELECT_BG = "#264f78"
EDITOR_SELECT_FG = "#ffffff"
EDITOR_LINE_BG = "#161b22"
EDITOR_LINE_FG = FG_DIM
EDITOR_HEADER_BG = "#1a2233"
EDITOR_ACCENT = ACCENT_BLUE

# ── Console ────────────────────────────────────────────────────────
CONSOLE_BG = BG_DARKEST
CONSOLE_FG = FG_PRIMARY
CONSOLE_ERROR_FG = ACCENT_RED
CONSOLE_SUCCESS_FG = ACCENT_GREEN
CONSOLE_INFO_FG = ACCENT_CYAN
CONSOLE_TIMESTAMP_FG = FG_DIM
CONSOLE_HEADER_BG = "#1a1520"
CONSOLE_ACCENT = ACCENT_PURPLE

# ── Preview ────────────────────────────────────────────────────────
PREVIEW_BG = "#fafbfc"
PREVIEW_HEADER_BG = "#1a2b1a"
PREVIEW_ACCENT = ACCENT_GREEN

# ── Toolbar ────────────────────────────────────────────────────────
TOOLBAR_BG = BG_DARK
TOOLBAR_BUTTON_FG = "#ffffff"
BTN_RUN_BG = "#238636"       # green
BTN_RUN_HOVER = "#2ea043"
BTN_CLEAR_BG = "#9e6a03"     # amber
BTN_CLEAR_HOVER = "#bb8009"
BTN_SAVE_BG = "#1f6feb"      # blue
BTN_SAVE_HOVER = "#388bfd"
BTN_LESSON_BG = "#8957e5"    # purple
BTN_LESSON_HOVER = "#a371f7"

# ── Menu ───────────────────────────────────────────────────────────
MENU_BG = BG_MID
MENU_FG = FG_PRIMARY
MENU_ACTIVE_BG = ACCENT_BLUE
MENU_ACTIVE_FG = "#ffffff"

# ── Status bar ─────────────────────────────────────────────────────
STATUS_BG = ACCENT_BLUE
STATUS_FG = "#ffffff"

# ── PanedWindow ────────────────────────────────────────────────────
SASH_BG = BG_BORDER
SASH_WIDTH = 4

# File types for dialogs
PYTHON_FILE_TYPES = [
    ("Python files", "*.py"),
    ("All files", "*.*"),
]
