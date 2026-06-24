# tests/blocks/editor/test_model.py
from pyblocks.blocks.editor.model import CustomBlockDef


def test_defaults():
    defn = CustomBlockDef(name="my_block", label="My Block")
    assert defn.category == "Custom"
    assert defn.color == "#fab387"
    assert defn.inputs == []
    assert defn.template == ""
    assert defn.description == ""


def test_full_creation():
    defn = CustomBlockDef(
        name="greet",
        label="Greet {name}",
        category="Custom",
        color="#a6e3a1",
        inputs=["name"],
        template='print(f"Hello, {name}!")',
        description="Prints a greeting",
    )
    assert defn.inputs == ["name"]
    assert "Hello" in defn.template


def test_name_must_be_identifier():
    defn = CustomBlockDef(name="hello world", label="X")
    assert not defn.is_valid()
    defn2 = CustomBlockDef(name="hello_world", label="X")
    assert defn2.is_valid()


def test_name_empty_is_invalid():
    defn = CustomBlockDef(name="", label="X")
    assert not defn.is_valid()
