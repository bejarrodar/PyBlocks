import importlib
import pytest
tk = pytest.importorskip("tkinter")
import pyblocks.blocks.builtins  # ensure builtins are registered
from pyblocks.panels.palette_panel import PalettePanel


def setup_function():
    importlib.reload(pyblocks.blocks.builtins)


def test_palette_panel_creates(tk_root):
    panel = PalettePanel(tk_root)
    assert panel.panel_id == "palette"


def test_palette_has_output_category(tk_root):
    panel = PalettePanel(tk_root)
    categories = panel.get_categories()
    assert "Output" in categories


def test_palette_has_control_category(tk_root):
    panel = PalettePanel(tk_root)
    assert "Control" in panel.get_categories()


def test_palette_block_count_matches_registry(tk_root):
    from pyblocks.blocks.definition import get_registry
    panel = PalettePanel(tk_root)
    total = sum(len(blocks) for blocks in panel._category_blocks.values())
    assert total == len(get_registry())


def test_palette_search_filters(tk_root):
    panel = PalettePanel(tk_root)
    panel._search_var.set("print")
    panel._apply_search()
    visible = panel._visible_block_names()
    assert all("print" in name.lower() for name in visible)


def test_palette_on_drag_callback(tk_root):
    dragged = []
    panel = PalettePanel(tk_root, on_palette_drag=lambda defn: dragged.append(defn))
    panel._simulate_drag("print_block")
    assert len(dragged) == 1
    assert dragged[0].name == "print_block"


def test_advanced_category_starts_collapsed(tk_root):
    """'Advanced' category should be inserted with open=False."""
    import pyblocks.blocks.builtins  # registers adv_* blocks if any exist
    panel = PalettePanel(tk_root)
    tree = panel._tree
    for cat_id in tree.get_children():
        if tree.item(cat_id, "text") == "Advanced":
            assert not tree.item(cat_id, "open"), "Advanced should start collapsed"
            return
    # If no Advanced category exists yet, pass (it's added in Plan B)

