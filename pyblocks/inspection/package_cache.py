from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path


class PackageCache:

    @staticmethod
    def cache_dir() -> Path:
        return Path.home() / ".pyblocks" / "packages"

    @staticmethod
    def _cache_file(package_name: str, version: str) -> Path:
        return PackageCache.cache_dir() / f"{package_name}_{version}.json"

    @staticmethod
    def _installed_version(package_name: str) -> str | None:
        try:
            from importlib.metadata import version
            return version(package_name)
        except Exception:
            return None

    @staticmethod
    def get(package_name: str) -> dict | None:
        ver = PackageCache._installed_version(package_name)
        if ver is None:
            return None
        path = PackageCache._cache_file(package_name, ver)
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None

    @staticmethod
    def write(package_name: str, version: str, color: str,
              entries: list[dict]) -> None:
        cache_dir = PackageCache.cache_dir()
        cache_dir.mkdir(parents=True, exist_ok=True)
        path = PackageCache._cache_file(package_name, version)
        data = {
            "package": package_name,
            "version": version,
            "scanned_at": datetime.utcnow().isoformat(timespec="seconds"),
            "color": color,
            "entries": entries,
        }
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    @staticmethod
    def delete(package_name: str, version: str) -> None:
        path = PackageCache._cache_file(package_name, version)
        if path.exists():
            path.unlink()

    @staticmethod
    def list_cached() -> list[dict]:
        cache_dir = PackageCache.cache_dir()
        if not cache_dir.exists():
            return []
        result = []
        for path in sorted(cache_dir.glob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                result.append({"package": data["package"], "version": data["version"]})
            except (json.JSONDecodeError, KeyError, OSError):
                continue
        return result
