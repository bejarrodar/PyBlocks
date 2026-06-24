import pytest
from pyblocks.canvas.model import Block, CanvasModel
from pyblocks.canvas.scope import ScopeAnalyzer


def test_scope_at_top_level():
    b1 = Block(id="s1", type="assign_block", inputs={"name": "x", "value": "1"})
    b2 = Block(id="s2", type="print_block", inputs={"value": "x"})
    cm = CanvasModel(blocks=[b1, b2])
    scope = ScopeAnalyzer.in_scope_at(cm, "s2")
    assert "x" in scope


def test_scope_only_preceding_blocks():
    b1 = Block(id="p1", type="print_block", inputs={"value": "x"})
    b2 = Block(id="a1", type="assign_block", inputs={"name": "x", "value": "1"})
    cm = CanvasModel(blocks=[b1, b2])
    scope = ScopeAnalyzer.in_scope_at(cm, "p1")
    assert "x" not in scope  # x assigned after p1


def test_scope_inside_function():
    local = Block(id="loc1", type="assign_block", inputs={"name": "y", "value": "2"})
    target = Block(id="tgt", type="print_block", inputs={"value": "y"})
    func = Block(id="fn1", type="def_block", indent=True,
                  children=[local, target])
    cm = CanvasModel(blocks=[func])
    scope = ScopeAnalyzer.in_scope_at(cm, "tgt")
    assert "y" in scope


def test_outer_scope_visible_inside_function():
    outer_assign = Block(id="oa", type="assign_block",
                         inputs={"name": "g", "value": "10"})
    inner_print = Block(id="ip", type="print_block", inputs={"value": "g"})
    func = Block(id="fn2", type="def_block", indent=True,
                  children=[inner_print])
    cm = CanvasModel(blocks=[outer_assign, func])
    scope = ScopeAnalyzer.in_scope_at(cm, "ip")
    assert "g" in scope


def test_scope_not_found_returns_empty():
    cm = CanvasModel()
    scope = ScopeAnalyzer.in_scope_at(cm, "nonexistent")
    assert scope == set()
