from pyblocks.canvas.model import Block, CanvasModel
from pyblocks.canvas.renderer import CanvasRenderer

def test_drag_state_starts_idle(tk_root):
    cm = CanvasModel()
    renderer = CanvasRenderer(tk_root, canvas_model=cm)
    assert renderer._drag_state is None

def test_drag_start_sets_state(tk_root):
    b = Block(id="drag1", type="print")
    cm = CanvasModel(blocks=[b])
    renderer = CanvasRenderer(tk_root, canvas_model=cm)
    renderer.redraw()
    renderer._begin_drag("drag1", cursor_x=20, cursor_y=20)
    assert renderer._drag_state is not None
    assert renderer._drag_state["id"] == "drag1"

def test_drag_end_calls_on_change(tk_root):
    changes = []
    b1 = Block(id="dr1", type="print")
    b2 = Block(id="dr2", type="print")
    cm = CanvasModel(blocks=[b1, b2])
    renderer = CanvasRenderer(tk_root, canvas_model=cm, on_change=lambda: changes.append(1))
    renderer.redraw()
    renderer._begin_drag("dr2", cursor_x=20, cursor_y=50)
    # Drop above the first block
    renderer._commit_drag(drop_parent_id=None, drop_index=0)
    assert len(changes) >= 1
    assert cm.blocks[0].id == "dr2"

def test_drag_state_is_dataclass(tk_root):
    from pyblocks.canvas.drag import DragState
    ds = DragState(block_id="x", start_x=0.0, start_y=0.0,
                   offset_x=0.0, offset_y=0.0)
    assert ds.is_dragging is False
    assert ds.block_id == "x"

def test_renderer_drag_state_is_none_initially(tk_root):
    from pyblocks.canvas.model import CanvasModel
    from pyblocks.canvas.renderer import CanvasRenderer
    cm = CanvasModel()
    r = CanvasRenderer(tk_root, canvas_model=cm)
    assert r._drag is None

def test_darken_hex():
    from pyblocks.canvas.renderer import _darken
    result = _darken("#ffffff", 40)
    assert result == "#d7d7d7"  # 255-40=215 → d7

def test_darken_clamps_at_zero():
    from pyblocks.canvas.renderer import _darken
    result = _darken("#101010", 40)
    assert result == "#000000"

def test_draw_rounded_rect_returns_item_id(tk_root):
    from pyblocks.canvas.renderer import _draw_rounded_rect
    canvas = __import__("tkinter").Canvas(tk_root)
    item = _draw_rounded_rect(canvas, 10, 10, 100, 40, r=6, fill="#89b4fa")
    assert isinstance(item, int)  # tkinter canvas item id

def test_parse_label_no_fields():
    from pyblocks.canvas.renderer import parse_label
    assert parse_label("PASS") == ["PASS"]

def test_parse_label_one_field():
    from pyblocks.canvas.renderer import parse_label
    assert parse_label("print({value})") == ["print(", ("value",), ")"]

def test_parse_label_two_fields():
    from pyblocks.canvas.renderer import parse_label
    result = parse_label("set {name} = {value}")
    assert result == ["set ", ("name",), " = ", ("value",), ""]

def test_parse_label_strips_empty_strings():
    from pyblocks.canvas.renderer import parse_label
    result = parse_label("{result} = abs({value})")
    non_empty = [s for s in result if s != ""]
    assert ("result",) in non_empty
    assert ("value",) in non_empty

def test_rounded_block_draws_polygon_not_rectangle(tk_root):
    """Blocks should be drawn as polygons (rounded) not rectangles."""
    from pyblocks.canvas.model import Block, CanvasModel
    from pyblocks.canvas.renderer import CanvasRenderer
    b = Block(id="v1", type="print_block", label_template="print({value})",
              inputs={"value": "hello"}, color="#a6e3a1")
    cm = CanvasModel(blocks=[b])
    r = CanvasRenderer(tk_root, canvas_model=cm)
    r.redraw()
    poly_items = [i for i in r.find_all() if r.type(i) == "polygon"]
    assert len(poly_items) > 0

def test_block_height_is_36(tk_root):
    from pyblocks.canvas.renderer import BLOCK_H
    assert BLOCK_H == 36

def test_field_rects_populated_after_redraw(tk_root):
    from pyblocks.canvas.model import Block, CanvasModel
    from pyblocks.canvas.renderer import CanvasRenderer
    b = Block(id="fr1", type="assign_block",
              label_template="set {name} = {value}",
              inputs={"name": "x", "value": "42"}, color="#89b4fa")
    cm = CanvasModel(blocks=[b])
    r = CanvasRenderer(tk_root, canvas_model=cm)
    r.redraw()
    assert ("fr1", "name") in r._field_rects
    assert ("fr1", "value") in r._field_rects

def test_field_rect_has_four_coords(tk_root):
    from pyblocks.canvas.model import Block, CanvasModel
    from pyblocks.canvas.renderer import CanvasRenderer
    b = Block(id="fr2", type="print_block",
              label_template="print({value})",
              inputs={"value": "hi"}, color="#a6e3a1")
    cm = CanvasModel(blocks=[b])
    r = CanvasRenderer(tk_root, canvas_model=cm)
    r.redraw()
    rect = r._field_rects[("fr2", "value")]
    assert len(rect) == 4
    x1, y1, x2, y2 = rect
    assert x2 > x1 and y2 > y1

def test_short_motion_does_not_commit_drag(tk_root):
    """Motion under threshold should not count as drag."""
    from pyblocks.canvas.model import Block, CanvasModel
    from pyblocks.canvas.renderer import CanvasRenderer
    b = Block(id="nd1", type="print_block", label_template="print({value})",
              inputs={"value": "x"}, color="#a6e3a1")
    cm = CanvasModel(blocks=[b])
    r = CanvasRenderer(tk_root, canvas_model=cm)
    r.redraw()
    r._begin_drag("nd1", cursor_x=20, cursor_y=20)
    assert r._drag is not None
    assert r._drag.is_dragging is False

def test_motion_over_threshold_sets_is_dragging(tk_root):
    from pyblocks.canvas.model import Block, CanvasModel
    from pyblocks.canvas.renderer import CanvasRenderer, DRAG_THRESHOLD
    b = Block(id="nd2", type="print_block", label_template="print({value})",
              inputs={"value": "x"}, color="#a6e3a1")
    cm = CanvasModel(blocks=[b])
    r = CanvasRenderer(tk_root, canvas_model=cm)
    r.redraw()
    r._begin_drag("nd2", cursor_x=20, cursor_y=20)
    class E: pass
    e = E(); e.x = 20 + DRAG_THRESHOLD + 1; e.y = 20
    r._on_drag(e)
    assert r._drag.is_dragging is True

def test_try_open_field_editor_finds_field(tk_root):
    """Clicking inside a field rect opens an Entry widget."""
    from pyblocks.canvas.model import Block, CanvasModel
    from pyblocks.canvas.renderer import CanvasRenderer
    b = Block(id="fe1", type="print_block",
              label_template="print({value})",
              inputs={"value": "hello"}, color="#a6e3a1")
    cm = CanvasModel(blocks=[b])
    r = CanvasRenderer(tk_root, canvas_model=cm)
    r.redraw()
    rect = r._field_rects.get(("fe1", "value"))
    assert rect is not None, "field rect must exist after redraw"
    cx = (rect[0] + rect[2]) // 2
    cy = (rect[1] + rect[3]) // 2
    r._try_open_field_editor(cx, cy)
    assert r._active_editor is not None

def test_commit_edit_updates_block_input(tk_root):
    from pyblocks.canvas.model import Block, CanvasModel
    from pyblocks.canvas.renderer import CanvasRenderer
    changes = []
    b = Block(id="fe2", type="print_block",
              label_template="print({value})",
              inputs={"value": "old"}, color="#a6e3a1")
    cm = CanvasModel(blocks=[b])
    r = CanvasRenderer(tk_root, canvas_model=cm, on_change=lambda: changes.append(1))
    r.redraw()
    rect = r._field_rects[("fe2", "value")]
    cx = (rect[0] + rect[2]) // 2
    cy = (rect[1] + rect[3]) // 2
    r._try_open_field_editor(cx, cy)
    r._active_editor["entry"].delete(0, "end")
    r._active_editor["entry"].insert(0, "new")
    r._commit_edit()
    assert b.inputs["value"] == "new"
    assert len(changes) == 1

