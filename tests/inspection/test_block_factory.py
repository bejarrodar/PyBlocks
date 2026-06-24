import pytest
from pyblocks.inspection.block_factory import BlockFactory, package_color, PALETTE
from pyblocks.inspection.package_scanner import CallableEntry
from pyblocks.blocks.definition import BlockDefinition


def test_palette_has_12_colors():
    assert len(PALETTE) == 12
    for c in PALETTE:
        assert c.startswith("#") and len(c) == 7


def test_package_color_deterministic():
    c1 = package_color("pygame")
    c2 = package_color("pygame")
    assert c1 == c2
    assert c1 in PALETTE


def test_package_color_different_packages():
    # pygame -> MD5 digest[0] % 12 == 0, requests -> 2; confirmed different
    assert package_color("pygame") != package_color("requests")


def test_from_entries_returns_block_definitions():
    entries = [
        CallableEntry(qualname="mypkg.foo", params=["x", "y"], submodule="mypkg")
    ]
    defns = BlockFactory.from_entries(entries, "#fab387")
    assert len(defns) == 1
    assert isinstance(defns[0], BlockDefinition)


def test_from_entries_label_format():
    entries = [
        CallableEntry(qualname="mypkg.foo", params=["x", "y"], submodule="mypkg")
    ]
    defns = BlockFactory.from_entries(entries, "#fab387")
    assert defns[0].label == "{result} = mypkg.foo({x}, {y})"


def test_from_entries_label_no_params():
    entries = [
        CallableEntry(qualname="mypkg.init", params=[], submodule="mypkg")
    ]
    defns = BlockFactory.from_entries(entries, "#fab387")
    assert defns[0].label == "{result} = mypkg.init()"


def test_from_entries_category_top_level():
    entries = [
        CallableEntry(qualname="mypkg.foo", params=[], submodule="mypkg")
    ]
    defns = BlockFactory.from_entries(entries, "#fab387")
    assert defns[0].category == "Mypkg"


def test_from_entries_category_submodule():
    entries = [
        CallableEntry(qualname="mypkg.draw.rect", params=[], submodule="mypkg.draw")
    ]
    defns = BlockFactory.from_entries(entries, "#fab387")
    assert defns[0].category == "Mypkg: draw"


def test_from_entries_color():
    entries = [
        CallableEntry(qualname="mypkg.foo", params=[], submodule="mypkg")
    ]
    defns = BlockFactory.from_entries(entries, "#89b4fa")
    assert defns[0].color == "#89b4fa"


def test_from_entries_generates_code():
    entries = [
        CallableEntry(qualname="mypkg.foo", params=["x", "y"], submodule="mypkg")
    ]
    defns = BlockFactory.from_entries(entries, "#fab387")
    code = defns[0].generate(result="r", x="1", y="2")
    assert code == "r = mypkg.foo(1, 2)"


def test_from_entries_generate_defaults():
    entries = [
        CallableEntry(qualname="mypkg.foo", params=["x"], submodule="mypkg")
    ]
    defns = BlockFactory.from_entries(entries, "#fab387")
    code = defns[0].generate()
    assert code == "_ = mypkg.foo(x)"


def test_from_entries_empty():
    assert BlockFactory.from_entries([], "#fab387") == []


def test_from_entries_inputs_field():
    entries = [
        CallableEntry(qualname="mypkg.foo", params=["x", "y"], submodule="mypkg")
    ]
    defns = BlockFactory.from_entries(entries, "#fab387")
    assert defns[0].inputs == ["result", "x", "y"]
