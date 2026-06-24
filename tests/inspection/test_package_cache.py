import json
import pytest
from pathlib import Path
from pyblocks.inspection.package_cache import PackageCache


def test_get_returns_none_when_no_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(PackageCache, "cache_dir", staticmethod(lambda: tmp_path))
    assert PackageCache.get("pygame") is None


def test_write_then_get_round_trips(tmp_path, monkeypatch):
    monkeypatch.setattr(PackageCache, "cache_dir", staticmethod(lambda: tmp_path))
    monkeypatch.setattr(
        PackageCache, "_installed_version",
        staticmethod(lambda name: "2.6.0"),
    )
    entries = [{"qualname": "pygame.draw.rect", "params": ["surface"], "submodule": "pygame.draw"}]
    PackageCache.write("pygame", "2.6.0", "#fab387", entries)
    data = PackageCache.get("pygame")
    assert data is not None
    assert data["package"] == "pygame"
    assert data["version"] == "2.6.0"
    assert data["color"] == "#fab387"
    assert data["entries"][0]["qualname"] == "pygame.draw.rect"


def test_get_returns_none_when_version_mismatch(tmp_path, monkeypatch):
    monkeypatch.setattr(PackageCache, "cache_dir", staticmethod(lambda: tmp_path))
    monkeypatch.setattr(
        PackageCache, "_installed_version",
        staticmethod(lambda name: "2.6.0"),
    )
    # Write cache for 2.5.0, but installed is 2.6.0 — should not find it
    entries = [{"qualname": "pygame.init", "params": [], "submodule": "pygame"}]
    PackageCache.write("pygame", "2.5.0", "#fab387", entries)
    result = PackageCache.get("pygame")
    assert result is None


def test_write_creates_cache_dir(tmp_path, monkeypatch):
    cache_dir = tmp_path / "packages"
    monkeypatch.setattr(PackageCache, "cache_dir", staticmethod(lambda: cache_dir))
    assert not cache_dir.exists()
    PackageCache.write("mypkg", "1.0.0", "#89b4fa", [])
    assert cache_dir.exists()
    assert (cache_dir / "mypkg_1.0.0.json").exists()


def test_write_stores_scanned_at(tmp_path, monkeypatch):
    monkeypatch.setattr(PackageCache, "cache_dir", staticmethod(lambda: tmp_path))
    PackageCache.write("mypkg", "1.0.0", "#89b4fa", [])
    data = json.loads((tmp_path / "mypkg_1.0.0.json").read_text())
    assert "scanned_at" in data
