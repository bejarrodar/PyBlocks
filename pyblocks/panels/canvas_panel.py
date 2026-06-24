from __future__ import annotations
import json
import tkinter as tk
from tkinter import ttk
from pyblocks.canvas.model import CanvasModel
from pyblocks.canvas.renderer import CanvasRenderer
from pyblocks.panels.base import Panel

class CanvasPanel(Panel):

    def __init__(self, root: tk.Tk, canvas_model: CanvasModel, on_change=None, **kwargs):
        super().__init__(root, title="③ Canvas", panel_id="canvas", **kwargs)
        self._external_on_change = on_change
        self._undo_stack: list[str] = []  # JSON snapshots
        self._redo_stack: list[str] = []
        self._bind_undo_redo()
        self._build_canvas(canvas_model)

    def _build_canvas(self, canvas_model: CanvasModel) -> None:
        frame = self.content
        self.renderer = CanvasRenderer(frame, canvas_model=canvas_model,
                                     on_change=self._wrapped_change)
        h_scroll = ttk.Scrollbar(frame, orient="horizontal",
                                  command=self.renderer.xview)
        v_scroll = ttk.Scrollbar(frame, orient="vertical",
                                  command=self.renderer.yview)
        self.renderer.configure(
            xscrollcommand=h_scroll.set,
            yscrollcommand=v_scroll.set,
            scrollregion=(0, 0, 2000, 4000),
        )
        self.renderer.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self.renderer.redraw()

    def _wrapped_change(self):
        self._push_undo()
        if self._external_on_change:
            self._external_on_change()

    def _bind_undo_redo(self) -> None:
        root = self._root
        root.bind_all("<Control-z>", lambda _: self.undo())
        root.bind_all("<Control-y>", lambda _: self.redo())

    def _snapshot(self) -> str:
        from pyblocks.canvas.serializer import _block_to_dict
        data = {"blocks": [_block_to_dict(b) for b in self.renderer._model.blocks],
                "scroll": list(self.renderer._model.scroll)}
        return json.dumps(data)

    def _restore(self, snapshot: str) -> None:
        from pyblocks.canvas.serializer import _dict_to_block
        data = json.loads(snapshot)
        from pyblocks.canvas.model import CanvasModel
        model = CanvasModel(
            blocks=[_dict_to_block(b) for b in data["blocks"]],
            scroll=tuple(data["scroll"]),
        )
        self.renderer.set_model(model)

    def _push_undo(self) -> None:
        self._undo_stack.append(self._snapshot())
        if len(self._undo_stack) > 50:
            self._undo_stack.pop(0)
        self._redo_stack.clear()

    def undo(self) -> None:
        if not self._undo_stack:
            return
        self._redo_stack.append(self._undo_stack.pop())
        if self._undo_stack:
            self._restore(self._undo_stack[-1])

    def redo(self) -> None:
        if not self._redo_stack:
            return
        self._undo_stack.append(self._redo_stack.pop())
        self._restore(self._undo_stack[-1])
