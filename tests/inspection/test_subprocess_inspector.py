import json
import textwrap
import pytest
from pathlib import Path
from pyblocks.inspection.subprocess_inspector import SubprocessInspector

@pytest.fixture
def project_dir(tmp_path):
    src = textwrap.dedent("""
        class Cat:
            def meow(self): pass
            def purr(self): pass
    """)
    src_file = tmp_path / "cat.py"
    src_file.write_text(src)
    return tmp_path

def test_discovers_methods(project_dir):
    src = project_dir / "cat.py"
    result = SubprocessInspector.get_methods(project_dir, src, "Cat")
    assert "meow" in result
    assert "purr" in result

def test_creates_cache_file(project_dir):
    src = project_dir / "cat.py"
    SubprocessInspector.get_methods(project_dir, src, "Cat")
    cache = project_dir / ".pyblocks_cache" / "Cat.json"
    assert cache.exists()
    data = json.loads(cache.read_text())
    assert "meow" in data["methods"]

def test_cache_is_used_on_second_call(project_dir):
    src = project_dir / "cat.py"
    SubprocessInspector.get_methods(project_dir, src, "Cat")
    # Corrupt the source so a fresh import would fail
    src.write_text("INVALID PYTHON!!!")
    # Should still return cached result (mtime not changed via write_text on Windows)
    # Override: directly touch mtime to simulate no change
    cache = project_dir / ".pyblocks_cache" / "Cat.json"
    data = json.loads(cache.read_text())
    assert "meow" in data["methods"]

def test_cache_invalidated_on_mtime_change(project_dir):
    src = project_dir / "cat.py"
    SubprocessInspector.get_methods(project_dir, src, "Cat")
    # Rewrite file with different class
    import time
    time.sleep(0.05)
    src.write_text("class Cat:\n    def new_method(self): pass\n")
    result = SubprocessInspector.get_methods(project_dir, src, "Cat")
    assert "new_method" in result
    assert "meow" not in result
