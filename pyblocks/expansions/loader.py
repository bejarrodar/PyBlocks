from __future__ import annotations
import importlib.util
import sys
from pathlib import Path
from pyblocks.expansions.pack import ExpansionPack

try:
    from importlib.metadata import entry_points
except ImportError:
    entry_points = None  # Python < 3.9 fallback

class ExpansionLoader:

    def __init__(self, project_root: Path) -> None:
        self._root = project_root

    def discover(self) -> list[ExpansionPack]:
        packs = []
        packs.extend(self._discover_local())
        packs.extend(self._discover_installed())
        return packs

    def _discover_local(self) -> list[ExpansionPack]:
        exp_dir = self._root / "expansions"
        if not exp_dir.is_dir():
            return []
        result = []
        for py_file in sorted(exp_dir.glob("*.py")):
            if py_file.stem.startswith("_"):
                continue
            result.append(ExpansionPack(
                name=py_file.stem,
                display_name=py_file.stem,
                source="local",
                source_path=str(py_file),
            ))
        return result

    def _discover_installed(self) -> list[ExpansionPack]:
        if entry_points is None:
            return []
        eps = entry_points(group="pyblocks_expansion")
        result = []
        for ep in eps:
            result.append(ExpansionPack(
                name=ep.name,
                display_name=ep.name,
                source="installed",
                source_path=ep.value,
            ))
        return result

    def load(self, pack: ExpansionPack) -> None:
        if pack.source == "local":
            self._load_file(Path(pack.source_path))
        elif pack.source == "installed":
            import importlib
            importlib.import_module(pack.source_path.split(":")[0])

    def _load_file(self, path: Path) -> None:
        module_name = f"_pyblocks_expansion_{path.stem}"
        if module_name in sys.modules:
            return
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None:
            return
        mod = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = mod
        try:
            spec.loader.exec_module(mod)
        except Exception as exc:
            del sys.modules[module_name]
            raise RuntimeError(f"Failed to load expansion {path.name}: {exc}") from exc
