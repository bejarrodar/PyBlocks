# tests/panels/test_live_python_panel.py
import pytest
tk = pytest.importorskip("tkinter")
from pyblocks.panels.live_python_panel import LivePythonPanel


def test_live_python_panel_creates(tk_root):
    panel = LivePythonPanel(tk_root)
    assert panel.panel_id == "live_python"


def test_set_code_updates_text(tk_root):
    panel = LivePythonPanel(tk_root)
    panel.set_code('print("hi")  # __pyblocks_id__:a1\n', id_map={"a1": 0})
    content = panel._text.get("1.0", "end").strip()
    assert 'print("hi")' in content


def test_highlight_block_id(tk_root):
    panel = LivePythonPanel(tk_root)
    panel.set_code(
        'print("a")  # __pyblocks_id__:a1\nprint("b")  # __pyblocks_id__:b1\n',
        id_map={"a1": 0, "b1": 1},
    )
    panel.highlight_block("a1")
    assert panel._highlighted_id == "a1"


def test_clear_highlight(tk_root):
    panel = LivePythonPanel(tk_root)
    panel.set_code('x = 1  # __pyblocks_id__:x1\n', id_map={"x1": 0})
    panel.highlight_block("x1")
    panel.clear_highlight()
    assert panel._highlighted_id is None


def test_line_click_callback(tk_root):
    clicked = []
    panel = LivePythonPanel(tk_root, on_line_click=lambda bid: clicked.append(bid))
    panel.set_code(
        'print("a")  # __pyblocks_id__:cl1\n',
        id_map={"cl1": 0},
    )
    # Simulate a click on line 1 via the internal method
    panel._handle_line_click(line_index=0)
    assert clicked == ["cl1"]
