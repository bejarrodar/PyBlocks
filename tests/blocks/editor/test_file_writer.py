import ast
import pytest
from pathlib import Path
from pyblocks.blocks.editor.model import CustomBlockDef
from pyblocks.blocks.editor.file_writer import BlockFileWriter


@pytest.fixture
def project(tmp_path):
    (tmp_path / "expansions").mkdir()
    return tmp_path


def test_writes_file(project):
    defns = [CustomBlockDef(name="greet", label="Greet {name}",
                             inputs=["name"],
                             template='print(f"Hello, {name}!")')]
    BlockFileWriter.write(project, defns)
    path = project / "expansions" / "custom_blocks.py"
    assert path.exists()


def test_generated_file_is_valid_python(project):
    defns = [CustomBlockDef(name="greet", label="Greet {name}",
                             inputs=["name"],
                             template='print(f"Hello, {name}!")')]
    BlockFileWriter.write(project, defns)
    src = (project / "expansions" / "custom_blocks.py").read_text()
    ast.parse(src)  # should not raise


def test_multiple_blocks_written(project):
    defns = [
        CustomBlockDef(name="block_a", label="Block A"),
        CustomBlockDef(name="block_b", label="Block B"),
    ]
    BlockFileWriter.write(project, defns)
    src = (project / "expansions" / "custom_blocks.py").read_text()
    assert "def block_a" in src
    assert "def block_b" in src


def test_empty_list_writes_empty_module(project):
    BlockFileWriter.write(project, [])
    src = (project / "expansions" / "custom_blocks.py").read_text()
    assert "from pyblocks" in src
    assert "def " not in src
