from __future__ import annotations
from pyblocks.canvas.model import Block, CanvasModel

_ASSIGN_TYPES = {"assign_block", "assign"}


class ScopeAnalyzer:

    @staticmethod
    def in_scope_at(canvas: CanvasModel, block_id: str) -> set[str]:
        """
        Walk the block tree, collecting variables defined before block_id
        in the same or enclosing scope. Returns set of variable names.
        """
        result: set[str] = set()
        _walk(canvas.blocks, block_id, result)
        return result


def _walk(blocks: list[Block], target_id: str,
          collected: set[str]) -> bool:
    """
    Walk blocks left-to-right. Collect assign names until target found.
    Returns True when target found (stops traversal).
    """
    for block in blocks:
        if block.id == target_id:
            return True
        if block.type in _ASSIGN_TYPES:
            name = block.inputs.get("name", "").strip()
            if name:
                collected.add(name)
        if block.indent and block.children:
            # Save current state, recurse into container
            snapshot = set(collected)
            found = _walk(block.children, target_id, collected)
            if found:
                return True
            # Target not in this container — undo child-only additions
            # (outer scope should not see local-only vars from sibling containers)
            collected.intersection_update(snapshot | _names_in(block.children))
    return False


def _names_in(blocks: list[Block]) -> set[str]:
    result = set()
    for b in blocks:
        if b.type in _ASSIGN_TYPES:
            n = b.inputs.get("name", "").strip()
            if n:
                result.add(n)
        result |= _names_in(b.children)
    return result
