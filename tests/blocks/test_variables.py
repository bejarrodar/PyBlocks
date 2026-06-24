# tests/blocks/test_variables.py
import importlib
import pytest
import pyblocks.blocks.variables  # trigger registration
from pyblocks.blocks.definition import get_registry


def setup_function():
    importlib.reload(pyblocks.blocks.variables)


def test_dunder_name_registered():
    reg = get_registry()
    assert "var___name__" in reg


def test_dunder_file_registered():
    reg = get_registry()
    assert "var___file__" in reg


def test_dunder_doc_registered():
    reg = get_registry()
    assert "var___doc__" in reg


def test_dunder_all_in_preset_variables_category():
    reg = get_registry()
    preset_names = ["__name__", "__file__", "__doc__",
                    "__version__", "__author__", "__all__", "__package__"]
    for name in preset_names:
        key = f"var_{name}"
        assert key in reg, f"{key} not registered"
        assert reg[key].category == "Preset Variables"


def test_dunder_generates_variable_name():
    reg = get_registry()
    code = reg["var___name__"].generate()
    assert code == "__name__"


def test_make_user_variable_chip():
    from pyblocks.blocks.variables import make_user_variable_chip
    defn = make_user_variable_chip("my_var")
    assert defn.name == "user_var_my_var"
    assert defn.category == "User Variables"
    assert defn.generate() == "my_var"
