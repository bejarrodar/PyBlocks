import pytest
from pyblocks.codegen.error_mapper import ErrorMapper


SAMPLE_TRACEBACK = """
Traceback (most recent call last):
  File "main.py", line 3, in <module>
    print(undefined_var)
NameError: name 'undefined_var' is not defined
"""

SAMPLE_SOURCE = "x = 42  # __pyblocks_id__:a1\ny = \"hello\"  # __pyblocks_id__:a2\nprint(undefined_var)  # __pyblocks_id__:a3"


def test_extract_error_line():
    line_no = ErrorMapper.extract_error_line(SAMPLE_TRACEBACK)
    assert line_no == 3


def test_find_block_id_for_line():
    block_id = ErrorMapper.find_block_id(SAMPLE_SOURCE, line_no=3)
    assert block_id == "a3"


def test_find_block_id_nearest_preceding():
    # Line 2 has no __pyblocks_id__ — should fall back to line 1
    source = "x = 42  # __pyblocks_id__:b1\nsome_expr\n"
    block_id = ErrorMapper.find_block_id(source, line_no=2)
    assert block_id == "b1"


def test_no_traceback_returns_none():
    assert ErrorMapper.extract_error_line("no traceback here") is None


def test_map_full_pipeline():
    result = ErrorMapper.map(SAMPLE_TRACEBACK, SAMPLE_SOURCE)
    assert result == "a3"


def test_map_returns_none_when_no_id_found():
    result = ErrorMapper.map(SAMPLE_TRACEBACK, "print(x)\n")
    assert result is None
