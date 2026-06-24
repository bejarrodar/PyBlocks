from __future__ import annotations
from pyblocks.canvas.model import Block, CanvasModel

_ID_MARKER = "# __pyblocks_id__"
_INDENT = "    "

# Maps block type → Python template. {inputs} keys are substituted.
# Container types (indent=True) have their header line here; children are
# recursed with increased indentation.
_TEMPLATES: dict[str, str] = {
    "print_block":  "print({value})",
    "assign_block": "{name} = {value}",
    "if_block": "if {condition}:",
    "elif_block": "elif {condition}:",
    "else_block": "else:",
    "for_block": "for {target} in {iterable}:",
    "while_block": "while {condition}:",
    "def_block": "def {name}({args}):",
    "class_block": "class {name}({bases}):",
    "with_block": "with {expr} as {target}:",
    "try_block": "try:",
    "except_block": "except {exc} as {alias}:",
    "finally_block": "finally:",
    "return_block": "return {value}",
    "import_block": "import {module}",
    "from_import_block": "from {module} import {names}",
    "global_block": "global {name}",
    "comment_block": "# {text}",
    "pass_block": "pass",
    "raise_block": "raise {exc}",
    "break_block": "break",
    "continue_block": "continue",
    "expr_block": "{expr}",
    "create_instance": "{var_name} = {class_name}({args})",
    "call_method": "{var_name}.{method_name}({args})",
}

_CONTAINER_TYPES = {
    "if_block", "elif_block", "else_block", "for_block", "while_block",
    "def_block", "class_block", "with_block", "try_block",
    "except_block", "finally_block",
}

_TOP_LEVEL_DEFS = {"def_block", "class_block"}


def _render_line(block: Block) -> str:
    template = _TEMPLATES.get(block.type, block.label_template or block.type)
    line = template
    for key, val in block.inputs.items():
        line = line.replace(f"{{{key}}}", val)
    return line


class CodeGenerator:

    @staticmethod
    def generate(canvas: CanvasModel) -> str:
        code, _ = CodeGenerator.generate_with_map(canvas)
        return code

    @staticmethod
    def generate_with_map(canvas: CanvasModel) -> tuple[str, dict[str, int]]:
        lines: list[str] = []
        id_map: dict[str, int] = {}
        prev_was_top_def = False

        for block in canvas.blocks:
            is_top_def = block.type in _TOP_LEVEL_DEFS
            if prev_was_top_def and lines:
                lines.append("")
            _emit_block(block, depth=0, lines=lines, id_map=id_map)
            prev_was_top_def = is_top_def

        return "\n".join(lines), id_map


def _emit_block(block: Block, depth: int, lines: list[str],
                 id_map: dict[str, int]) -> None:
    prefix = _INDENT * depth
    line = _render_line(block)
    ln = len(lines)
    id_map[block.id] = ln
    lines.append(f"{prefix}{line}  {_ID_MARKER}:{block.id}")

    if block.indent:
        if block.children:
            for child in block.children:
                _emit_block(child, depth + 1, lines, id_map)
        else:
            lines.append(f"{prefix}{_INDENT}pass")
