import textwrap
import pytest
tk = pytest.importorskip("tkinter")
from pathlib import Path
from unittest.mock import patch, MagicMock
from pyblocks.expansions.pack import ExpansionPack
from pyblocks.panels.package_manager_panel import PackageManagerPanel
from pyblocks.blocks.definition import clear_registry
import pyblocks.blocks.builtins

@pytest.fixture(autouse=True)
def clean():
    clear_registry()
    import importlib
    importlib.reload(pyblocks.blocks.builtins)
    yield
    clear_registry()

# ── existing tests (unchanged) ────────────────────────────────────────────────

def test_panel_lists_packs(tk_root):
    packs = [
        ExpansionPack(name="pack_a", display_name="Pack A"),
        ExpansionPack(name="pack_b", display_name="Pack B"),
    ]
    panel = PackageManagerPanel(tk_root, packs=packs, enabled={})
    names = panel.pack_names()
    assert "Pack A" in names
    assert "Pack B" in names

def test_panel_shows_enabled_state(tk_root):
    packs = [ExpansionPack(name="pack_a", display_name="Pack A")]
    panel = PackageManagerPanel(tk_root, packs=packs,
                                 enabled={"pack_a": True})
    assert panel.is_checked("pack_a") is True

def test_toggle_callback_fires(tk_root):
    packs = [ExpansionPack(name="pack_a", display_name="Pack A")]
    toggled = []
    panel = PackageManagerPanel(tk_root, packs=packs, enabled={},
                                 on_toggle=lambda name, val: toggled.append((name, val)))
    panel.set_checked("pack_a", True)
    assert ("pack_a", True) in toggled

# ── new tests for Task 7 ──────────────────────────────────────────────────────

def test_toggle_package_callback_fires(tk_root):
    """on_toggle_package fires when _toggle_package is called directly."""
    toggled = []
    panel = PackageManagerPanel(
        tk_root, packs=[], enabled={},
        on_toggle_package=lambda name, val: toggled.append((name, val)),
    )
    panel._toggle_package("requests", True)
    assert ("requests", True) in toggled

def test_toggle_package_updates_internal_state(tk_root):
    """_toggle_package stores the new value in _enabled_packages."""
    panel = PackageManagerPanel(tk_root, packs=[], enabled={})
    panel._toggle_package("numpy", False)
    assert panel._enabled_packages["numpy"] is False
    panel._toggle_package("numpy", True)
    assert panel._enabled_packages["numpy"] is True

def test_toggle_package_no_callback_does_not_raise(tk_root):
    """Calling _toggle_package without a callback is safe."""
    panel = PackageManagerPanel(tk_root, packs=[], enabled={})
    panel._toggle_package("scipy", True)  # should not raise

def test_list_scanned_packages_delegates_to_cache(tk_root):
    """list_scanned_packages() returns whatever PackageCache.list_cached returns."""
    fake = [{"package": "requests", "version": "2.31.0"}]
    with patch("pyblocks.panels.package_manager_panel.PackageCache") as MockCache:
        MockCache.list_cached.return_value = fake
        # Re-create after patching so _refresh_scanned uses the mock too
        panel = PackageManagerPanel(tk_root, packs=[], enabled={})
        result = panel.list_scanned_packages()
    assert result == fake

def test_set_status_updates_string_var(tk_root):
    """_set_status() writes to _status_var."""
    panel = PackageManagerPanel(tk_root, packs=[], enabled={})
    panel._set_status("Installing…")
    assert panel._status_var.get() == "Installing…"

def test_set_status_safe_when_var_is_none(tk_root):
    """_set_status() does not raise if _status_var is None."""
    panel = PackageManagerPanel(tk_root, packs=[], enabled={})
    panel._status_var = None
    panel._set_status("anything")  # should not raise

def test_initial_status_is_ready(tk_root):
    """Status label starts as 'Ready'."""
    panel = PackageManagerPanel(tk_root, packs=[], enabled={})
    assert panel._status_var.get() == "Ready"

def test_enabled_packages_initial_state(tk_root):
    """enabled_packages kwarg seeds _enabled_packages."""
    panel = PackageManagerPanel(
        tk_root, packs=[], enabled={},
        enabled_packages={"requests": True, "numpy": False},
    )
    assert panel._enabled_packages["requests"] is True
    assert panel._enabled_packages["numpy"] is False

def test_is_package_checked_false_for_unknown(tk_root):
    """is_package_checked returns False for unknown package names."""
    panel = PackageManagerPanel(tk_root, packs=[], enabled={})
    assert panel.is_package_checked("nonexistent") is False
