import textwrap
import pytest
from pathlib import Path
from pyblocks.expansions.loader import ExpansionLoader
from pyblocks.blocks.definition import get_registry, clear_registry

@pytest.fixture(autouse=True)
def clean_registry():
    clear_registry()
    import pyblocks.blocks.builtins
    yield
    clear_registry()

@pytest.fixture
def project_with_expansion(tmp_path):
    exp_dir = tmp_path / "expansions"
    exp_dir.mkdir()
    src = textwrap.dedent("""
        from pyblocks.blocks.definition import block

        @block(label="Say Hello", category="Demo", color="#fab387",
               description="Prints hello")
        def demo_hello():
            return 'print("hello")'
    """)
    (exp_dir / "demo_pack.py").write_text(src)
    return tmp_path

def test_discover_local_packs(project_with_expansion):
    loader = ExpansionLoader(project_with_expansion)
    packs = loader.discover()
    names = [p.name for p in packs]
    assert "demo_pack" in names

def test_local_pack_has_display_name(project_with_expansion):
    loader = ExpansionLoader(project_with_expansion)
    packs = loader.discover()
    pack = next(p for p in packs if p.name == "demo_pack")
    assert pack.display_name == "demo_pack"
    assert pack.source == "local"

def test_load_pack_registers_blocks(project_with_expansion):
    loader = ExpansionLoader(project_with_expansion)
    packs = loader.discover()
    pack = next(p for p in packs if p.name == "demo_pack")
    loader.load(pack)
    assert "demo_hello" in get_registry()

def test_discover_no_expansions(tmp_path):
    loader = ExpansionLoader(tmp_path)
    packs = loader.discover()
    assert packs == []
