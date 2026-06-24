import pytest

try:
    import tkinter as tk
    TKINTER_AVAILABLE = True
except ModuleNotFoundError:
    TKINTER_AVAILABLE = False


@pytest.fixture(scope="session")
def tk_root():
    """Single hidden Tk root for the whole test session."""
    if not TKINTER_AVAILABLE:
        pytest.skip("tkinter not available in this environment")
    root = tk.Tk()
    root.withdraw()
    yield root
    root.destroy()
