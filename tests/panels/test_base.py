import pytest
tk = pytest.importorskip("tkinter")
ttk = pytest.importorskip("tkinter.ttk")
from pyblocks.panels.base import Panel


def test_panel_has_title(tk_root):
    panel = Panel(tk_root, title="Test Panel", panel_id="test")
    assert panel.panel_title == "Test Panel"
    assert panel.panel_id == "test"


def test_panel_starts_docked(tk_root):
    panel = Panel(tk_root, title="Test Panel", panel_id="test")
    assert panel.is_floating is False
    assert panel.is_hidden is False


def test_panel_float_creates_toplevel(tk_root):
    panel = Panel(tk_root, title="Test Panel", panel_id="test")
    panel.float()
    assert panel.is_floating is True
    panel._on_float_close()  # simulates user closing the float window
    assert panel.is_floating is False
    assert panel.is_hidden is True


def test_panel_dock_after_float(tk_root):
    container = ttk.Frame(tk_root)
    panel = Panel(tk_root, title="Test Panel", panel_id="test")
    panel.float()
    panel.dock(container)
    assert panel.is_floating is False


def test_panel_hide_and_show(tk_root):
    panel = Panel(tk_root, title="Test Panel", panel_id="test")
    panel.hide()
    assert panel.is_hidden is True
    panel.show()
    assert panel.is_hidden is False


def test_panel_layout_state(tk_root):
    panel = Panel(tk_root, title="Test Panel", panel_id="test")
    state = panel.layout_state()
    assert "floating" in state
    assert "hidden" in state
    assert "panel_id" not in state
