import pytest
from pyblocks.blocks.definition import block, BlockDefinition, get_registry, clear_registry, register_block

def setup_function():
    clear_registry()

def test_block_decorator_registers():
    @block(label="PRINT {value}", category="Output", color="#a6e3a1")
    def print_block(value):
        return f"print({value})"

    reg = get_registry()
    assert "print_block" in reg
    assert reg["print_block"].label == "PRINT {value}"
    assert reg["print_block"].color == "#a6e3a1"

def test_block_definition_fields():
    @block(label="SET {name} = {value}", category="Variables", color="#89b4fa",
           description="Assign a value to a variable.")
    def assign_block(name, value):
        return f"{name} = {value}"

    defn = get_registry()["assign_block"]
    assert defn.category == "Variables"
    assert defn.description == "Assign a value to a variable."
    assert defn.inputs == ["name", "value"]

def test_block_decorator_indent_flag():
    @block(label="IF {condition}:", category="Control", color="#cba6f7", indent=True)
    def if_block(condition):
        return f"if {condition}:"

    defn = get_registry()["if_block"]
    assert defn.indent is True

def test_block_generates_code():
    @block(label="PRINT {value}", category="Output", color="#a6e3a1")
    def print_block2(value):
        return f"print({value})"

    defn = get_registry()["print_block2"]
    result = defn.generate(value='"hello"')
    assert result == 'print("hello")'

def test_block_default_color():
    @block(label="PASS", category="Control")
    def pass_block():
        return "pass"

    defn = get_registry()["pass_block"]
    assert defn.color == "#89b4fa"

def test_get_registry_by_category():
    @block(label="X", category="Output", color="#a6e3a1")
    def x_block():
        return "x"

    @block(label="Y", category="Control", color="#cba6f7")
    def y_block():
        return "y"

    reg = get_registry()
    output_blocks = [d for d in reg.values() if d.category == "Output"]
    assert any(d.label == "X" for d in output_blocks)

def test_register_block_manually():
    def _gen(**kwargs): return f"{kwargs.get('x', 'x')} = 1"
    defn = BlockDefinition(
        name="manual_block",
        label="{x} = 1",
        category="Test",
        color="#fab387",
        description="",
        indent=False,
        inputs=["x"],
        _fn=_gen,
    )
    register_block(defn)
    assert "manual_block" in get_registry()
    assert get_registry()["manual_block"].label == "{x} = 1"
