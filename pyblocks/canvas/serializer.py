from __future__ import annotations
import json
from pathlib import Path
from pyblocks.canvas.model import Block, CanvasModel

def _block_to_dict(b: Block) -> dict:
    return {
        "id": b.id,
        "type": b.type,
        "label_template": b.label_template,
        "inputs": b.inputs,
        "children": [_block_to_dict(c) for c in b.children],
        "color": b.color,
        "indent": b.indent,
        "x": b.x,
        "y": b.y,
    }

def _dict_to_block(d: dict) -> Block:
    return Block(
        id=d["id"],
        type=d["type"],
        label_template=d.get("label_template", d["type"].upper()),
        inputs=d.get("inputs", {}),
        children=[_dict_to_block(c) for c in d.get("children", [])],
        color=d.get("color", "#89b4fa"),
        indent=d.get("indent", False),
        x=d.get("x", 0),
        y=d.get("y", 0),
    )

class CanvasSerializer:

    @staticmethod
    def save(canvas: CanvasModel, path: Path) -> None:
        data = {
            "blocks": [_block_to_dict(b) for b in canvas.blocks],
            "scroll": list(canvas.scroll),
        }
        path.write_text(json.dumps(data, indent=2))

    @staticmethod
    def load(path: Path) -> CanvasModel:
        if not path.exists():
            raise FileNotFoundError(f"canvas.json not found: {path}")
        data = json.loads(path.read_text())
        return CanvasModel(
            blocks=[_dict_to_block(b) for b in data.get("blocks", [])],
            scroll=tuple(data.get("scroll", [0, 0])),
        )
