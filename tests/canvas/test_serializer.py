# tests/canvas/test_serializer.py
import json
import pytest
from pathlib import Path
from pyblocks.canvas.model import Block, CanvasModel
from pyblocks.canvas.serializer import CanvasSerializer

def test_round_trip_simple(tmp_path):
    cm = CanvasModel(blocks=[
        Block(id="a1", type="print", label_template="PRINT {value}",
              inputs={"value": '"hello"'}, color="#fab387"),
    ])
    path = tmp_path / "canvas.json"
    CanvasSerializer.save(cm, path)
    loaded = CanvasSerializer.load(path)
    assert loaded.blocks[0].id == "a1"
    assert loaded.blocks[0].inputs["value"] == '"hello"'

def test_round_trip_nested(tmp_path):
    child = Block(id="c1", type="print", inputs={"value": "x"})
    parent = Block(id="p1", type="if_block", indent=True, children=[child])
    cm = CanvasModel(blocks=[parent])
    path = tmp_path / "canvas.json"
    CanvasSerializer.save(cm, path)
    loaded = CanvasSerializer.load(path)
    assert loaded.blocks[0].children[0].id == "c1"

def test_load_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        CanvasSerializer.load(tmp_path / "nonexistent.json")

def test_load_empty_canvas(tmp_path):
    path = tmp_path / "canvas.json"
    path.write_text(json.dumps({"blocks": [], "scroll": [0, 0]}))
    loaded = CanvasSerializer.load(path)
    assert loaded.blocks == []
    assert loaded.scroll == (0, 0)
