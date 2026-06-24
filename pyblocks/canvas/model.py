from __future__ import annotations
import uuid
from dataclasses import dataclass, field

MAX_NESTING_DEPTH = 5


def _new_id() -> str:
    return uuid.uuid4().hex[:8]


@dataclass
class Block:
    id: str = field(default_factory=_new_id)
    type: str = "print"
    label_template: str = "PRINT {value}"
    inputs: dict[str, str] = field(default_factory=dict)
    children: list["Block"] = field(default_factory=list)
    color: str = "#89b4fa"
    indent: bool = False
    x: int = 0
    y: int = 0

    def depth(self) -> int:
        if not self.children:
            return 0
        return 1 + max(c.depth() for c in self.children)

    def can_add_child(self, current_depth: int) -> bool:
        return current_depth < MAX_NESTING_DEPTH


@dataclass
class CanvasModel:
    blocks: list[Block] = field(default_factory=list)
    scroll: tuple[int, int] = (0, 0)

    def find_block(self, block_id: str
                   ) -> tuple["Block | None", "Block | None", int]:
        """Return (block, parent, index). parent=None for top-level."""
        for i, b in enumerate(self.blocks):
            if b.id == block_id:
                return b, None, i
            result = _find_in_children(b, block_id)
            if result[0] is not None:
                return result
        return None, None, -1

    def remove_block(self, block_id: str) -> bool:
        for i, b in enumerate(self.blocks):
            if b.id == block_id:
                self.blocks.pop(i)
                return True
            if _remove_from_children(b, block_id):
                return True
        return False

    def move_block(self, block_id: str, target_parent_id: str | None,
                   target_index: int) -> bool:
        """Move block to new position. Returns False if depth would exceed MAX."""
        block, old_parent, old_idx = self.find_block(block_id)
        if block is None:
            return False

        # Depth check
        if target_parent_id is not None:
            target_block, _, _ = self.find_block(target_parent_id)
            if target_block is None:
                return False
            # Depth of current parent chain + subtree depth of block
            parent_depth = _block_depth_in_model(self, target_parent_id)
            if parent_depth + 1 + block.depth() > MAX_NESTING_DEPTH:
                return False

        # Remove from current location
        if old_parent is None:
            self.blocks.pop(old_idx)
        else:
            old_parent.children.pop(old_idx)

        # Insert at target
        if target_parent_id is None:
            idx = min(target_index, len(self.blocks))
            self.blocks.insert(idx, block)
        else:
            target_block, _, _ = self.find_block(target_parent_id)
            idx = min(target_index, len(target_block.children))
            target_block.children.insert(idx, block)

        return True

def _find_in_children(parent: Block, block_id: str
                       ) -> tuple["Block | None", "Block | None", int]:
    for i, child in enumerate(parent.children):
        if child.id == block_id:
            return child, parent, i
        result = _find_in_children(child, block_id)
        if result[0] is not None:
            return result
    return None, None, -1

def _block_depth_in_model(model: "CanvasModel", block_id: str) -> int:
    """Return how deep block_id sits in the tree (0 = top level)."""
    def _search(blocks, depth):
        for b in blocks:
            if b.id == block_id:
                return depth
            result = _search(b.children, depth + 1)
            if result >= 0:
                return result
        return -1
    return _search(model.blocks, 0)

def _remove_from_children(block: Block, block_id: str) -> bool:
    for i, child in enumerate(block.children):
        if child.id == block_id:
            block.children.pop(i)
            return True
        if _remove_from_children(child, block_id):
            return True
    return False
