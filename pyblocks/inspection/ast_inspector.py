from __future__ import annotations
import ast
from pathlib import Path

class ASTInspector:

    @staticmethod
    def get_methods(filepath: Path, class_name: str) -> list[str] | None:
        """
        Returns method names for class_name in filepath.
        Returns None if the file cannot be parsed (caller should try next tier).
        Returns [] if the file parses but the class isn't found.
        """
        try:
            tree = ast.parse(filepath.read_text(encoding="utf-8"))
        except (SyntaxError, OSError):
            return None

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                return [
                    n.name
                    for n in node.body
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                ]
        return []
