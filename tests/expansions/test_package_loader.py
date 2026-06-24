import pytest
from unittest.mock import patch, MagicMock
from pyblocks.expansions.package_loader import PackageLoader
from pyblocks.blocks.definition import get_registry, clear_registry
from pyblocks.inspection.package_scanner import CallableEntry
from pyblocks.blocks.definition import BlockDefinition


@pytest.fixture(autouse=True)
def clean_registry():
    clear_registry()
    yield
    clear_registry()


def test_load_enabled_registers_blocks():
    fake_entry = {"qualname": "mypkg.foo", "params": ["x"], "submodule": "mypkg"}
    fake_cache = {
        "package": "mypkg",
        "version": "1.0",
        "color": "#fab387",
        "entries": [fake_entry],
    }
    with patch("pyblocks.expansions.package_loader.PackageCache.get", return_value=fake_cache):
        PackageLoader.load_enabled(["mypkg"])
    registry = get_registry()
    assert "mypkg.foo" in registry


def test_load_enabled_skips_missing_cache():
    with patch("pyblocks.expansions.package_loader.PackageCache.get", return_value=None):
        PackageLoader.load_enabled(["nonexistent"])
    assert "nonexistent.foo" not in get_registry()


def test_load_enabled_empty_list():
    PackageLoader.load_enabled([])
    assert get_registry() == {}


def test_load_enabled_block_generates_code():
    fake_entry = {"qualname": "mypkg.foo", "params": ["x"], "submodule": "mypkg"}
    fake_cache = {
        "package": "mypkg",
        "version": "1.0",
        "color": "#fab387",
        "entries": [fake_entry],
    }
    with patch("pyblocks.expansions.package_loader.PackageCache.get", return_value=fake_cache):
        PackageLoader.load_enabled(["mypkg"])
    defn = get_registry()["mypkg.foo"]
    assert defn.generate(result="r", x="1") == "r = mypkg.foo(1)"


def test_load_enabled_multiple_packages():
    def fake_get(name):
        return {
            "package": name,
            "version": "1.0",
            "color": "#fab387",
            "entries": [{"qualname": f"{name}.bar", "params": [], "submodule": name}],
        }
    with patch("pyblocks.expansions.package_loader.PackageCache.get", side_effect=fake_get):
        PackageLoader.load_enabled(["pkga", "pkgb"])
    registry = get_registry()
    assert "pkga.bar" in registry
    assert "pkgb.bar" in registry
