from __future__ import annotations
import importlib
import importlib.util
import sys
from pathlib import Path

_MODULE_KEY = "_pyblocks_custom_blocks"

class CustomBlockLoader:

    def __init__(self, project_root: Path) -> None:
        self._root = project_root

    def load_or_reload(self) -> None:
        path = self._root / "expansions" / "custom_blocks.py"
        if not path.exists():
            return
        if _MODULE_KEY in sys.modules:
            spec = importlib.util.spec_from_file_location(_MODULE_KEY, path)
            mod = importlib.util.module_from_spec(spec)
            sys.modules[_MODULE_KEY] = mod
            spec.loader.exec_module(mod)
        else:
            spec = importlib.util.spec_from_file_location(_MODULE_KEY, path)
            mod = importlib.util.module_from_spec(spec)
            sys.modules[_MODULE_KEY] = mod
            try:
                spec.loader.exec_module(mod)
            except Exception as exc:
                del sys.modules[_MODULE_KEY]
                raise RuntimeError(f"Failed to load custom blocks: {exc}") from exc
