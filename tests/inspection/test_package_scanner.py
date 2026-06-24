import pytest
from pyblocks.inspection.package_scanner import PackageScanner, CallableEntry


@pytest.fixture(scope="session")
def json_entries():
    return PackageScanner.scan("json")


def test_scan_returns_callable_entries(json_entries):
    assert json_entries is not None
    assert len(json_entries) > 0
    assert all(isinstance(e, CallableEntry) for e in json_entries)


def test_scan_finds_json_dumps(json_entries):
    qualnames = [e.qualname for e in json_entries]
    assert "json.dumps" in qualnames


def test_scan_entry_has_params(json_entries):
    dumps_entry = next(e for e in json_entries if e.qualname == "json.dumps")
    assert "obj" in dumps_entry.params


def test_scan_entry_has_correct_submodule(json_entries):
    dumps_entry = next(e for e in json_entries if e.qualname == "json.dumps")
    assert dumps_entry.submodule == "json"


def test_scan_finds_submodule_entries(json_entries):
    submodules = {e.submodule for e in json_entries}
    assert any(s.startswith("json.") for s in submodules)


def test_scan_returns_none_for_missing_package():
    result = PackageScanner.scan("_totally_nonexistent_pkg_xyz_123")
    assert result is None


def test_scan_no_private_functions(json_entries):
    for e in json_entries:
        local_name = e.qualname.split(".")[-1]
        assert not local_name.startswith("_"), f"Private function leaked: {e.qualname}"


def test_callable_entry_fields():
    entry = CallableEntry(qualname="json.dumps", params=["obj"], submodule="json")
    assert entry.qualname == "json.dumps"
    assert entry.params == ["obj"]
    assert entry.submodule == "json"
