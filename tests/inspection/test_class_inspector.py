import textwrap
import pytest
from pathlib import Path
from pyblocks.inspection.class_inspector import ClassInspector

@pytest.fixture
def simple_class_file(tmp_path):
    src = textwrap.dedent("""
        class Bird:
            def fly(self): pass
            def sing(self): pass
    """)
    f = tmp_path / "bird.py"
    f.write_text(src)
    return tmp_path, f

def test_returns_methods_via_ast(simple_class_file):
    project, src = simple_class_file
    inspector = ClassInspector(project)
    methods = inspector.get_methods(src, "Bird")
    assert "fly" in methods
    assert "sing" in methods

def test_returns_empty_for_unknown_class(simple_class_file):
    project, src = simple_class_file
    inspector = ClassInspector(project)
    methods = inspector.get_methods(src, "Nonexistent")
    assert methods == []

def test_get_method_groups(simple_class_file):
    project, src = simple_class_file
    inspector = ClassInspector(project)
    groups = inspector.get_method_groups(src, "Bird")
    assert "fly" in groups["public"]
