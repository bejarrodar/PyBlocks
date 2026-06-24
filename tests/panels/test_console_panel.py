import pytest
tk = pytest.importorskip("tkinter")
from pyblocks.panels.console_panel import ConsolePanel


def test_console_panel_creates(tk_root):
    panel = ConsolePanel(tk_root)
    assert panel.panel_id == "console"


def test_append_stdout(tk_root):
    panel = ConsolePanel(tk_root)
    panel.append_stdout("hello output")
    content = panel._get_tab_content("all")
    assert "hello output" in content


def test_append_stderr(tk_root):
    panel = ConsolePanel(tk_root)
    panel.append_stderr("error line")
    content = panel._get_tab_content("errors")
    assert "error line" in content


def test_stderr_not_in_subprocess_tab(tk_root):
    panel = ConsolePanel(tk_root)
    panel.append_stderr("error only")
    content = panel._get_tab_content("subprocess")
    assert "error only" not in content


def test_clear(tk_root):
    panel = ConsolePanel(tk_root)
    panel.append_stdout("some output")
    panel.clear()
    assert panel._get_tab_content("all").strip() == ""


def test_set_running_state(tk_root):
    panel = ConsolePanel(tk_root)
    panel.set_running(True)
    assert panel._running is True
    panel.set_running(False)
    assert panel._running is False
