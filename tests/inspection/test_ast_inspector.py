import pytest
import textwrap
from pathlib import Path
from pyblocks.inspection.ast_inspector import ASTInspector


@pytest.fixture
def sample_file(tmp_path):
    src = textwrap.dedent("""
        class Dog:
            def bark(self): pass
            def _fetch(self): pass
            def __init__(self): pass
            def sit(self): pass
    """)
    f = tmp_path / "dog.py"
    f.write_text(src)
    return f


def test_finds_public_methods(sample_file):
    result = ASTInspector.get_methods(sample_file, "Dog")
    assert "bark" in result
    assert "sit" in result


def test_finds_private_methods(sample_file):
    result = ASTInspector.get_methods(sample_file, "Dog")
    assert "_fetch" in result


def test_finds_dunder_methods(sample_file):
    result = ASTInspector.get_methods(sample_file, "Dog")
    assert "__init__" in result


def test_returns_empty_for_missing_class(sample_file):
    result = ASTInspector.get_methods(sample_file, "Cat")
    assert result == []


def test_returns_none_on_syntax_error(tmp_path):
    bad = tmp_path / "bad.py"
    bad.write_text("class X:\n  def (broken):")
    result = ASTInspector.get_methods(bad, "X")
    assert result is None  # signals tier 1 failure, try tier 2
