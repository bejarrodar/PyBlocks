import pytest
tk = pytest.importorskip("tkinter")
import pyblocks.blocks.builtins
import pyblocks.blocks.variables
from pyblocks.panels.palette_panel import PalettePanel


def test_sync_adds_variable_chip(tk_root):
    panel = PalettePanel(tk_root)
    panel.sync_user_variables({"my_var"})
    names = panel._visible_block_names()
    assert "user_var_my_var" in names


def test_sync_removes_stale_variable(tk_root):
    panel = PalettePanel(tk_root)
    panel.sync_user_variables({"x", "y"})
    panel.sync_user_variables({"x"})  # y removed
    names = panel._visible_block_names()
    assert "user_var_y" not in names
    assert "user_var_x" in names


def test_sync_empty_removes_all(tk_root):
    panel = PalettePanel(tk_root)
    panel.sync_user_variables({"a", "b"})
    panel.sync_user_variables(set())
    names = panel._visible_block_names()
    assert not any(n.startswith("user_var_") for n in names)
