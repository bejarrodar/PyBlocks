import pytest
tk = pytest.importorskip("tkinter")
from pyblocks.panels.block_editor_panel import BlockEditorPanel


def test_panel_has_name_field(tk_root):
    panel = BlockEditorPanel(tk_root, on_save=None)
    assert panel.get_name() == ""


def test_set_and_get_values(tk_root):
    panel = BlockEditorPanel(tk_root, on_save=None)
    panel.set_values(name="greet", label="Greet {name}",
                      category="Custom", color="#fab387",
                      inputs=["name"], template='print("hi")',
                      description="A greeting")
    assert panel.get_name() == "greet"
    assert panel.get_label() == "Greet {name}"
    assert panel.get_inputs() == ["name"]


def test_save_callback_fires(tk_root):
    called = []
    panel = BlockEditorPanel(tk_root, on_save=lambda defn: called.append(defn))
    panel.set_values(name="my_block", label="My Block",
                      category="Custom", color="#fab387",
                      inputs=[], template="pass", description="")
    panel.save()
    assert len(called) == 1
    assert called[0].name == "my_block"


def test_save_rejected_for_invalid_name(tk_root):
    called = []
    panel = BlockEditorPanel(tk_root, on_save=lambda d: called.append(d))
    panel.set_values(name="my block", label="Bad Name",
                      category="Custom", color="#fab387",
                      inputs=[], template="pass", description="")
    panel.save()
    assert called == []
