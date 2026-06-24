from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

_INSPECT_SCRIPT = """
import sys, inspect, importlib.util, json
path, class_name = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("_mod", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
cls = getattr(mod, class_name)
methods = [name for name, _ in inspect.getmembers(cls, predicate=inspect.isfunction)]
print(json.dumps(methods))
"""

class SubprocessInspector:

    @staticmethod
    def get_methods(project_root: Path, src_file: Path,
                    class_name: str) -> list[str] | None:
        cache_dir = project_root / ".pyblocks_cache"
        cache_file = cache_dir / f"{class_name}.json"

        mtime = src_file.stat().st_mtime if src_file.exists() else 0

        if cache_file.exists():
            try:
                data = json.loads(cache_file.read_text())
                if data.get("mtime") == mtime:
                    return data["methods"]
            except (json.JSONDecodeError, KeyError):
                pass

        try:
            result = subprocess.run(
                [sys.executable, "-c", _INSPECT_SCRIPT,
                 str(src_file), class_name],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode != 0:
                return None
            methods = json.loads(result.stdout.strip())
        except Exception:
            return None

        cache_dir.mkdir(exist_ok=True)
        cache_file.write_text(json.dumps({"mtime": mtime, "methods": methods}))
        return methods
