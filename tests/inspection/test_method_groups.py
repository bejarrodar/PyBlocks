from pyblocks.inspection.method_groups import split_methods

def test_public_methods():
    g = split_methods(["bark", "sit", "_fetch", "__init__", "__str__"])
    assert g["public"] == ["bark", "sit"]

def test_private_methods():
    g = split_methods(["bark", "_fetch", "_hidden"])
    assert g["private"] == ["_fetch", "_hidden"]

def test_dunder_methods():
    g = split_methods(["__init__", "__str__", "bark"])
    assert g["dunder"] == ["__init__", "__str__"]

def test_empty_list():
    g = split_methods([])
    assert g == {"public": [], "private": [], "dunder": []}
