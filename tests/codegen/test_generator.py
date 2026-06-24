# tests/codegen/test_generator.py
import pytest
from pyblocks.canvas.model import Block, CanvasModel
from pyblocks.codegen.generator import CodeGenerator


def test_single_print_block():
    cm = CanvasModel(blocks=[
        Block(id="a1", type="print", label_template="PRINT {value}",
              inputs={"value": '"hello"'}, color="#a6e3a1"),
    ])
    code = CodeGenerator.generate(cm)
    assert 'print("hello")' in code
    assert "# __pyblocks_id__:a1" in code


def test_assign_block():
    cm = CanvasModel(blocks=[
        Block(id="b1", type="assign", label_template="SET {name} = {value}",
              inputs={"name": "x", "value": "42"}, color="#89b4fa"),
    ])
    code = CodeGenerator.generate(cm)
    assert "x = 42" in code
    assert "# __pyblocks_id__:b1" in code


def test_empty_canvas():
    code = CodeGenerator.generate(CanvasModel())
    assert code.strip() == ""


def test_multiple_blocks_order():
    cm = CanvasModel(blocks=[
        Block(id="c1", type="assign", inputs={"name": "x", "value": "1"}),
        Block(id="c2", type="print", inputs={"value": "x"}),
    ])
    code = CodeGenerator.generate(cm)
    lines = [l for l in code.splitlines() if l.strip()]
    id_lines = [i for i, l in enumerate(lines) if "# __pyblocks_id__" in l]
    assert id_lines[0] < id_lines[1]  # c1 appears before c2


def test_if_block_with_children():
    child = Block(id="d2", type="print", inputs={"value": '"yes"'})
    parent = Block(id="d1", type="if_block", label_template="IF {condition}",
                    inputs={"condition": "x > 0"}, indent=True, children=[child])
    cm = CanvasModel(blocks=[parent])
    code = CodeGenerator.generate(cm)
    assert "if x > 0:" in code
    assert '    print("yes")' in code
    assert "# __pyblocks_id__:d1" in code
    assert "# __pyblocks_id__:d2" in code


def test_nested_def_block():
    body = Block(id="e2", type="print", inputs={"value": '"in func"'})
    func = Block(id="e1", type="def_block", label_template="DEF {name}({args})",
                  inputs={"name": "greet", "args": ""}, indent=True, children=[body])
    cm = CanvasModel(blocks=[func])
    code = CodeGenerator.generate(cm)
    assert "def greet():" in code
    assert '    print("in func")' in code


def test_empty_container_generates_pass():
    func = Block(id="f1", type="def_block", label_template="DEF {name}({args})",
                  inputs={"name": "empty", "args": ""}, indent=True, children=[])
    cm = CanvasModel(blocks=[func])
    code = CodeGenerator.generate(cm)
    assert "    pass" in code


def test_block_id_to_line_map():
    cm = CanvasModel(blocks=[
        Block(id="g1", type="print", inputs={"value": '"a"'}),
        Block(id="g2", type="print", inputs={"value": '"b"'}, color="#89b4fa"),
    ])
    code, id_map = CodeGenerator.generate_with_map(cm)
    assert "g1" in id_map
    assert "g2" in id_map
    assert id_map["g1"] != id_map["g2"]


def test_top_level_blank_lines_between_defs():
    f1 = Block(id="h1", type="def_block", label_template="DEF {name}({args})",
                inputs={"name": "foo", "args": ""}, indent=True, children=[
                    Block(id="h2", type="print", inputs={"value": '"a"'})])
    f2 = Block(id="h3", type="def_block", label_template="DEF {name}({args})",
                inputs={"name": "bar", "args": ""}, indent=True, children=[
                    Block(id="h4", type="print", inputs={"value": '"b"'})])
    cm = CanvasModel(blocks=[f1, f2])
    code = CodeGenerator.generate(cm)
    # Should have blank line between top-level defs
    assert "\n\n" in code
