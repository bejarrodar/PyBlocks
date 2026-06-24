import pytest
from pyblocks.canvas.model import Block, CanvasModel
from pyblocks.canvas.variables import VariableTracker


def test_scan_empty_canvas():
    assert VariableTracker.scan(CanvasModel()) == set()


def test_scan_single_assign():
    b = Block(id="a", type="assign_block", inputs={"name": "x", "value": "1"})
    cm = CanvasModel(blocks=[b])
    assert VariableTracker.scan(cm) == {"x"}


def test_scan_multiple_assigns():
    b1 = Block(id="a1", type="assign_block", inputs={"name": "x", "value": "1"})
    b2 = Block(id="a2", type="assign_block", inputs={"name": "y", "value": "2"})
    cm = CanvasModel(blocks=[b1, b2])
    assert VariableTracker.scan(cm) == {"x", "y"}


def test_scan_nested_assign():
    inner = Block(id="i1", type="assign_block", inputs={"name": "z", "value": "99"})
    outer = Block(id="o1", type="if_block", indent=True, children=[inner])
    cm = CanvasModel(blocks=[outer])
    assert VariableTracker.scan(cm) == {"z"}


def test_scan_non_assign_blocks_ignored():
    b = Block(id="p1", type="print_block", inputs={"value": '"hi"'})
    cm = CanvasModel(blocks=[b])
    assert VariableTracker.scan(cm) == set()
