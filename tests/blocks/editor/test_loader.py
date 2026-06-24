# tests/blocks/editor/test_loader.py
import textwrap
import pytest
from pathlib import Path
from pyblocks.blocks.editor.loader import CustomBlockLoader
from pyblocks.blocks.definition import get_registry, clear_registry
import pyblocks.blocks.builtins

@pytest.fixture(autouse=True)
def clean():
    import importlib
    clear_registry()
    importlib.reload(pyblocks.blocks.builtins)
    yield
    clear_registry()
    importlib.reload(pyblocks.blocks.builtins)
    import sys
    for key in list(sys.modules):
        if "_pyblocks_custom" in key:
            del sys.modules[key]

@pytest.fixture
def project_with_custom(tmp_path):
    src = textwrap.dedent("""
        from pyblocks.blocks.definition import block

        @block(label="Say Hey", category="Custom", color="#fab387",
               description="")
        def say_hey():
            return 'print("hey")'
    """)
    exp_dir = tmp_path / "expansions"
    exp_dir.mkdir()
    (exp_dir / "custom_blocks.py").write_text(src)
    return tmp_path

def test_load_registers_blocks(project_with_custom):
    loader = CustomBlockLoader(project_with_custom)
    loader.load_or_reload()
    assert "say_hey" in get_registry()

def test_load_no_file_is_noop(tmp_path):
    loader = CustomBlockLoader(tmp_path)
    loader.load_or_reload()  # should not raise

def test_reload_picks_up_new_block(project_with_custom):
    loader = CustomBlockLoader(project_with_custom)
    loader.load_or_reload()
    # Append a new block to the file
    p = project_with_custom / "expansions" / "custom_blocks.py"
    existing = p.read_text()
    p.write_text(existing + textwrap.dedent("""

        @block(label="Say Bye", category="Custom", color="#fab387",
               description="")
        def say_bye():
            return 'print("bye")'
    """))
    loader.load_or_reload()
    assert "say_bye" in get_registry()
