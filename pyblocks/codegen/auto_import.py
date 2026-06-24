from __future__ import annotations
from pathlib import Path
from pyblocks.canvas.model import Block, CanvasModel

_BUILTINS = {
    "int", "str", "float", "list", "dict", "set", "tuple", "bool",
    "bytes", "bytearray", "complex", "frozenset", "type", "object",
}

class AutoImporter:

    @staticmethod
    def compute_imports(canvas: CanvasModel, project_root: Path) -> list[str]:
        class_names: set[str] = set()
        for block in canvas.blocks:
            _collect_class_names(block, class_names)

        imports = []
        for name in sorted(class_names):
            if name in _BUILTINS:
                continue
            module = _find_module(project_root, name)
            if module:
                imports.append(f"from {module} import {name}")
        return imports

def _collect_class_names(block: Block, result: set[str]) -> None:
    if block.type == "create_instance":
        name = block.inputs.get("class_name", "").strip()
        if name:
            result.add(name)
    for child in block.children:
        _collect_class_names(child, result)

def _find_module(project_root: Path, class_name: str) -> str | None:
    for py_file in project_root.glob("*.py"):
        if py_file.name == "main.py":
            continue
        text = py_file.read_text(encoding="utf-8", errors="ignore")
        if f"class {class_name}" in text:
            return py_file.stem
    return None
