import pytest
import pyblocks.blocks.classes
from pyblocks.blocks.definition import get_registry
from pyblocks.codegen.generator import CodeGenerator
from pyblocks.canvas.model import Block, CanvasModel

def setup_function():
    from pyblocks.blocks.definition import clear_registry
    import pyblocks.blocks.builtins
    import pyblocks.blocks.classes
    clear_registry()
    import importlib
    importlib.reload(pyblocks.blocks.builtins)
    importlib.reload(pyblocks.blocks.classes)

def test_create_instance_registered():
    assert "create_instance" in get_registry()

def test_call_method_registered():
    assert "call_method" in get_registry()

def test_create_instance_codegen():
    b = Block(id="ci1", type="create_instance",
              inputs={"var_name": "d", "class_name": "Dog", "args": ""})
    gen = CodeGenerator()
    code, _ = gen.generate_with_map(CanvasModel(blocks=[b]))
    assert "d = Dog()" in code

def test_call_method_codegen():
    b = Block(id="cm1", type="call_method",
              inputs={"var_name": "d", "method_name": "bark", "args": ""})
    gen = CodeGenerator()
    code, _ = gen.generate_with_map(CanvasModel(blocks=[b]))
    assert "d.bark()" in code

def test_call_method_with_args():
    b = Block(id="cm2", type="call_method",
              inputs={"var_name": "d", "method_name": "fetch",
                      "args": '"ball"'})
    gen = CodeGenerator()
    code, _ = gen.generate_with_map(CanvasModel(blocks=[b]))
    assert 'd.fetch("ball")' in code
