from __future__ import annotations
from pyblocks.canvas.model import Block, CanvasModel

_ASSIGN_TYPES = {"assign_block", "assign"}
_DEF_TYPES = {"def_block"}


class VariableTracker:

    @staticmethod
    def scan(canvas: CanvasModel) -> set[str]:
        result: set[str] = set()
        for block in canvas.blocks:
            _collect(block, result)
        return result


class FunctionTracker:

    @staticmethod
    def scan(canvas: CanvasModel) -> set[str]:
        result: set[str] = set()
        for block in canvas.blocks:
            _collect_fn(block, result)
        return result


def _collect(block: Block, result: set[str]) -> None:
    if block.type in _ASSIGN_TYPES:
        name = block.inputs.get("name", "").strip()
        if name:
            result.add(name)
    for child in block.children:
        _collect(child, result)


def _collect_fn(block: Block, result: set[str]) -> None:
    if block.type in _DEF_TYPES:
        name = block.inputs.get("name", "").strip()
        if name and name.isidentifier():
            result.add(name)
    for child in block.children:
        _collect_fn(child, result)
