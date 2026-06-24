import copy
from pyblocks.panels.canvas_panel import CanvasPanel
from pyblocks.canvas.model import Block, CanvasModel


def test_undo_restores_previous_state(tk_root):
    b1 = Block(id="u1", type="print")
    b2 = Block(id="u2", type="print")
    cm = CanvasModel(blocks=[b1, b2])
    panel = CanvasPanel(tk_root, canvas_model=cm)
    panel._push_undo()  # snapshot with b1, b2
    cm.blocks.pop(0)    # remove b1
    panel._push_undo()  # snapshot with b2 only
    panel.undo()
    assert len(panel.renderer._model.blocks) == 2


def test_redo_reapplies_change(tk_root):
    b1 = Block(id="r1", type="print")
    b2 = Block(id="r2", type="print")
    cm = CanvasModel(blocks=[b1, b2])
    panel = CanvasPanel(tk_root, canvas_model=cm)
    panel._push_undo()
    cm.blocks.pop(0)
    panel._push_undo()
    panel.undo()
    panel.redo()
    assert len(panel.renderer._model.blocks) == 1


def test_undo_stack_max_50(tk_root):
    cm = CanvasModel()
    panel = CanvasPanel(tk_root, canvas_model=cm)
    for _ in range(60):
        panel._push_undo()
    assert len(panel._undo_stack) <= 50
