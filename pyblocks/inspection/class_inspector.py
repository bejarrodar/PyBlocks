from __future__ import annotations
from pathlib import Path
from pyblocks.inspection.ast_inspector import ASTInspector
from pyblocks.inspection.subprocess_inspector import SubprocessInspector
from pyblocks.inspection.method_groups import split_methods

class ClassInspector:

    def __init__(self, project_root: Path) -> None:
        self._root = project_root

    def get_methods(self, src_file: Path, class_name: str) -> list[str]:
        result = ASTInspector.get_methods(src_file, class_name)
        if result is None:
            result = SubprocessInspector.get_methods(
                self._root, src_file, class_name)
        return result or []

    def get_method_groups(self, src_file: Path,
                          class_name: str) -> dict[str, list[str]]:
        return split_methods(self.get_methods(src_file, class_name))
