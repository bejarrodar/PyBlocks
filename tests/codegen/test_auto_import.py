import textwrap
import pytest
from pathlib import Path
from pyblocks.canvas.model import Block, CanvasModel
from pyblocks.codegen.auto_import import AutoImporter

@pytest.fixture
def project_dir(tmp_path):
    (tmp_path / "dog.py").write_text("class Dog:\n    def bark(self): pass\n")
    return tmp_path

def test_single_class_import(project_dir):
    b = Block(id="ci1", type="create_instance",
              inputs={"var_name": "d", "class_name": "Dog", "args": ""})
    cm = CanvasModel(blocks=[b])
    imports = AutoImporter.compute_imports(cm, project_dir)
    assert "from dog import Dog" in imports

def test_no_import_for_builtin_class(project_dir):
    b = Block(id="ci2", type="create_instance",
              inputs={"var_name": "x", "class_name": "list", "args": ""})
    cm = CanvasModel(blocks=[b])
    imports = AutoImporter.compute_imports(cm, project_dir)
    assert imports == []

def test_deduplicates_imports(project_dir):
    b1 = Block(id="ci1", type="create_instance",
               inputs={"var_name": "d1", "class_name": "Dog", "args": ""})
    b2 = Block(id="ci2", type="create_instance",
               inputs={"var_name": "d2", "class_name": "Dog", "args": ""})
    cm = CanvasModel(blocks=[b1, b2])
    imports = AutoImporter.compute_imports(cm, project_dir)
    assert imports.count("from dog import Dog") == 1
