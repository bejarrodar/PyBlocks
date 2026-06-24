from pyblocks.canvas.model import Block, CanvasModel


def test_find_block_top_level():
    b = Block(id="f1", type="print")
    cm = CanvasModel(blocks=[b])
    found, parent, idx = cm.find_block("f1")
    assert found is b
    assert parent is None


def test_find_block_nested():
    child = Block(id="fc", type="print")
    parent_block = Block(id="fp", type="if_block", indent=True, children=[child])
    cm = CanvasModel(blocks=[parent_block])
    found, parent, idx = cm.find_block("fc")
    assert found is child
    assert parent is parent_block


def test_find_block_missing():
    cm = CanvasModel()
    result = cm.find_block("nonexistent")
    assert result == (None, None, -1)


def test_move_block_top_level_reorder():
    b1 = Block(id="m1", type="print")
    b2 = Block(id="m2", type="print")
    b3 = Block(id="m3", type="print")
    cm = CanvasModel(blocks=[b1, b2, b3])
    cm.move_block("m3", target_parent_id=None, target_index=0)
    assert cm.blocks[0].id == "m3"
    assert cm.blocks[1].id == "m1"
    assert cm.blocks[2].id == "m2"


def test_move_block_into_container():
    container = Block(id="con1", type="if_block", indent=True, children=[])
    stmt = Block(id="st1", type="print")
    cm = CanvasModel(blocks=[container, stmt])
    cm.move_block("st1", target_parent_id="con1", target_index=0)
    assert cm.blocks[0].children[0].id == "st1"
    assert len(cm.blocks) == 1


def test_move_block_out_of_container():
    child = Block(id="co1", type="print")
    container = Block(id="ct1", type="if_block", indent=True, children=[child])
    cm = CanvasModel(blocks=[container])
    cm.move_block("co1", target_parent_id=None, target_index=1)
    assert len(cm.blocks) == 2
    assert cm.blocks[1].id == "co1"
    assert container.children == []


def test_move_block_respects_max_depth():
    """Moving a container that would exceed depth 5 must be rejected."""
    def make_deep(depth):
        if depth == 0:
            return Block(id=f"d{depth}", type="print")
        return Block(id=f"d{depth}", type="if_block", indent=True,
                     children=[make_deep(depth - 1)])
    deep = make_deep(4)  # already depth=4; adding it inside another = 5
    outer = Block(id="outer", type="if_block", indent=True, children=[])
    cm = CanvasModel(blocks=[outer, deep])
    result = cm.move_block("d4", target_parent_id="outer", target_index=0)
    # Should succeed (total depth 1 + 4 = 5, exactly at limit)
    assert result is True

    # A 5-deep subtree inside outer would be 6 — reject
    too_deep = make_deep(5)
    cm2 = CanvasModel(blocks=[outer, too_deep])
    result2 = cm2.move_block(f"d5", target_parent_id="outer", target_index=0)
    assert result2 is False
