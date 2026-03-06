"""Code execution engine for TkLearn Studio.

Executes user-written Tkinter code dynamically inside the preview
frame with a hardened sandbox: restricted builtins, blocked dangerous
imports, and captured stdout/stderr.

Security layers:
    1. Whitelisted __builtins__ — no open(), __import__(), exec(), eval(),
       compile(), getattr(), setattr(), delattr(), breakpoint(), vars(),
       globals(), locals(), dir(), memoryview(), or type().
    2. Guarded import function — only allows a safe set of modules.
       Blocks os, sys, subprocess, shutil, socket, http, ctypes, pathlib,
       importlib, signal, code, pickle, shelve, webbrowser, and more.
    3. stdout/stderr redirected so print() output goes to the console.
"""

import builtins
import io
import sys
import traceback
import tkinter as tk
from tkinter import ttk

# ── Safe builtins whitelist ──────────────────────────────────────────────
# Only harmless, educational-use builtins are exposed to user code.
_SAFE_BUILTIN_NAMES = [
    # Types and constructors
    "bool", "int", "float", "complex", "str", "bytes", "bytearray",
    "list", "tuple", "set", "frozenset", "dict",
    # Iteration / sequence helpers
    "range", "enumerate", "zip", "map", "filter", "reversed", "sorted",
    "len", "min", "max", "sum", "abs", "round", "pow", "divmod",
    "all", "any", "next", "iter",
    # String / repr
    "repr", "ascii", "chr", "ord", "format", "hex", "oct", "bin",
    "hash", "id", "callable", "isinstance", "issubclass",
    # I/O (safe)
    "print", "input",
    # Functional
    "staticmethod", "classmethod", "property", "super",
    "__build_class__",
    # Exceptions (needed for try/except in user code)
    "Exception", "BaseException",
    "ArithmeticError", "AssertionError", "AttributeError",
    "BlockingIOError", "BrokenPipeError", "BufferError",
    "ChildProcessError", "ConnectionAbortedError",
    "ConnectionError", "ConnectionRefusedError",
    "ConnectionResetError", "EOFError", "FileExistsError",
    "FileNotFoundError", "FloatingPointError", "GeneratorExit",
    "IOError", "ImportError", "IndexError", "InterruptedError",
    "IsADirectoryError", "KeyError", "KeyboardInterrupt",
    "LookupError", "MemoryError", "ModuleNotFoundError",
    "NameError", "NotADirectoryError", "NotImplementedError",
    "OSError", "OverflowError", "PermissionError",
    "ProcessLookupError", "RecursionError", "ReferenceError",
    "RuntimeError", "StopAsyncIteration", "StopIteration",
    "SyntaxError", "SystemError", "SystemExit", "TimeoutError",
    "TypeError", "UnboundLocalError", "UnicodeDecodeError",
    "UnicodeEncodeError", "UnicodeError", "UnicodeTranslationError",
    "ValueError", "ZeroDivisionError",
    # Constants
    "True", "False", "None",
    "NotImplemented", "Ellipsis",
    # Object
    "object",
]

# Build the safe builtins dict once at import time
_SAFE_BUILTINS = {}
for _name in _SAFE_BUILTIN_NAMES:
    _obj = getattr(builtins, _name, None)
    if _obj is not None:
        _SAFE_BUILTINS[_name] = _obj


# ── Guarded import ──────────────────────────────────────────────────────
# Only modules that are safe for Tkinter learning are allowed.
_ALLOWED_MODULES = frozenset({
    # Tkinter (already injected but allow explicit import)
    "tkinter", "tkinter.ttk", "tkinter.messagebox",
    "tkinter.colorchooser", "tkinter.font",
    "tkinter.simpledialog", "tkinter.scrolledtext",
    # Safe standard-library modules for learning
    "math", "random", "string", "textwrap",
    "datetime", "time", "calendar",
    "itertools", "functools", "operator",
    "collections", "collections.abc",
    "enum", "dataclasses", "typing",
    "re", "json", "copy",
    "statistics", "decimal", "fractions",
    "abc",
})

# Modules explicitly blocked even if someone tries dotted imports
_BLOCKED_MODULES = frozenset({
    "os", "sys", "subprocess", "shutil", "signal",
    "socket", "http", "urllib", "ftplib", "smtplib", "ssl",
    "ctypes", "multiprocessing", "threading",
    "importlib", "runpy", "code", "codeop", "compileall",
    "pathlib", "tempfile", "glob", "fnmatch",
    "pickle", "shelve", "marshal", "dbm",
    "webbrowser", "antigravity", "turtle",
    "inspect", "dis", "ast",
    "gc", "tracemalloc", "resource",
    "io", "builtins", "_thread", "pty", "pipes",
    "mmap", "select", "selectors",
    "xmlrpc", "socketserver", "asyncio",
})


def _guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
    """Import function that only allows whitelisted modules.

    Raises:
        ImportError: If the module is not in the allowed list.
    """
    # Check the top-level module name
    top_level = name.split(".")[0]

    if top_level in _BLOCKED_MODULES:
        raise ImportError(
            f"Module '{name}' is blocked for security. "
            f"Only Tkinter and safe learning modules are allowed."
        )

    if name in _ALLOWED_MODULES or top_level in {"tkinter"}:
        return __builtins__["__import__"](name, globals, locals, fromlist, level) \
            if isinstance(__builtins__, dict) \
            else builtins.__import__(name, globals, locals, fromlist, level)

    raise ImportError(
        f"Module '{name}' is not available in this sandbox. "
        f"Only Tkinter and safe learning modules (math, random, etc.) are allowed."
    )


# Inject the guarded import into the safe builtins
_SAFE_BUILTINS["__import__"] = _guarded_import


# ── Public API ───────────────────────────────────────────────────────────

def run_code(code, preview_frame, console):
    """Execute user code with the preview frame as ``root``.

    The execution environment is sandboxed:
        - Only safe builtins are available (no open, eval, exec, etc.)
        - Only whitelisted modules can be imported
        - stdout/stderr are redirected to the console

    Args:
        code: The Python source code string to execute.
        preview_frame: The tk.Frame to use as ``root`` in user code.
        console: The ConsoleFrame instance for output logging.
    """
    console.clear()

    # Clear previous preview widgets
    for widget in preview_frame.winfo_children():
        widget.destroy()

    if not code.strip():
        console.log_info("Nothing to execute.")
        return

    # Redirect stdout and stderr to capture print() calls
    captured_out = io.StringIO()
    captured_err = io.StringIO()
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    # Get the actual top-level Tk window for key bindings etc.
    toplevel = preview_frame.winfo_toplevel()

    try:
        sys.stdout = captured_out
        sys.stderr = captured_err

        exec_globals = {
            "tk": tk,
            "ttk": ttk,
            "__builtins__": _SAFE_BUILTINS,
            # Set to __sandbox__ so `if __name__ == "__main__"` blocks
            # (which create a second Tk root) are skipped automatically.
            "__name__": "__sandbox__",
        }
        exec_locals = {
            "root": preview_frame,
            # Expose the real Tk window so user code can bind keys,
            # set title, etc. without creating a second Tk instance.
            "window": toplevel,
        }

        exec(code, exec_globals, exec_locals)

        # Ensure the preview frame can receive keyboard focus
        preview_frame.focus_set()

    except Exception:
        error_text = traceback.format_exc()
        console.log_error(error_text)
    else:
        console.log("Execution finished successfully.")
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

        # Flush captured stdout to console
        stdout_text = captured_out.getvalue()
        if stdout_text:
            console.log_info(stdout_text.rstrip("\n"))

        # Flush captured stderr to console
        stderr_text = captured_err.getvalue()
        if stderr_text:
            console.log_error(stderr_text.rstrip("\n"))
            console.log_error(stderr_text.rstrip("\n"))
