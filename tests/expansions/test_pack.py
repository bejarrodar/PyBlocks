# tests/expansions/test_pack.py
from pyblocks.expansions.pack import ExpansionPack


def test_pack_creation():
    pack = ExpansionPack(
        name="turtle_blocks",
        display_name="Turtle Graphics",
        description="Draw with Python's turtle module",
        source="local",
        source_path="expansions/turtle_blocks.py",
        block_names=["turtle_forward", "turtle_turn"],
    )
    assert pack.name == "turtle_blocks"
    assert "turtle_forward" in pack.block_names


def test_pack_defaults():
    pack = ExpansionPack(name="my_pack", display_name="My Pack")
    assert pack.block_names == []
    assert pack.description == ""
    assert pack.source == "local"
    assert pack.source_path == ""
