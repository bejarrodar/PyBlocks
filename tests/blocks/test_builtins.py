# tests/blocks/test_builtins.py
import pytest
import pyblocks.blocks.builtins  # triggers registration
from pyblocks.blocks.definition import get_registry


def test_print_block_registered():
    reg = get_registry()
    assert "print_block" in reg
    assert reg["print_block"].category == "Output"


def test_assign_block_registered():
    reg = get_registry()
    assert "assign_block" in reg
    assert reg["assign_block"].category == "Variables"


def test_if_block_is_indent():
    reg = get_registry()
    assert "if_block" in reg
    assert reg["if_block"].indent is True


def test_for_block_is_indent():
    reg = get_registry()
    assert "for_block" in reg
    assert reg["for_block"].indent is True


def test_def_block_is_indent():
    reg = get_registry()
    assert "def_block" in reg
    assert reg["def_block"].indent is True


def test_all_builtins_have_labels():
    reg = get_registry()
    for name, defn in reg.items():
        assert defn.label, f"{name} has no label"
        assert defn.category, f"{name} has no category"


def test_print_block_generates_code():
    reg = get_registry()
    code = reg["print_block"].generate(value='"hello"')
    assert code == 'print("hello")'


def test_assign_block_generates_code():
    reg = get_registry()
    code = reg["assign_block"].generate(name="x", value="42")
    assert code == "x = 42"


def test_io_blocks_registered():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    reg = get_registry()
    for name in ["io_print", "io_print_sep", "io_print_end",
                 "io_print_fstring", "io_input", "io_open"]:
        assert name in reg, f"{name} not registered"


def test_io_input_generates_assignment():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["io_input"].generate(result="x", prompt='"Enter: "')
    assert code == 'x = input("Enter: ")'


def test_io_open_generates_open_call():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["io_open"].generate(result="f", path='"data.txt"', mode='"r"')
    assert code == 'f = open("data.txt", "r")'


def test_io_print_fstring_generates_fstring():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["io_print_fstring"].generate(text="x + 5")
    assert code == 'print(f"{x + 5}")'


def test_io_print_sep_generates_sep_param():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["io_print_sep"].generate(value='"a", "b"', sep='", "')
    assert code == 'print("a", "b", sep=", ")'


def test_io_print_end_generates_end_param():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["io_print_end"].generate(value='"hello"', end='""')
    assert code == 'print("hello", end="")'


def test_cast_blocks_registered():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    reg = get_registry()
    for name in ["cast_int", "cast_str", "cast_float", "cast_bool",
                 "cast_list", "cast_tuple", "cast_set", "cast_frozenset",
                 "cast_dict", "cast_bytes", "cast_bytearray", "cast_complex",
                 "cast_chr", "cast_ord", "cast_bin", "cast_hex", "cast_oct",
                 "cast_repr", "cast_ascii", "cast_format", "cast_int_base"]:
        assert name in reg, f"{name} not registered"


def test_cast_int_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["cast_int"].generate(result="n", value='"42"')
    assert code == 'n = int("42")'


def test_cast_int_base_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["cast_int_base"].generate(result="n", value='"ff"', base="16")
    assert code == 'n = int("ff", 16)'


def test_cast_complex_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["cast_complex"].generate(result="c", real="3", imag="4")
    assert code == "c = complex(3, 4)"


def test_cast_format_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["cast_format"].generate(result="s", value='"hello"', spec='"s"')
    assert code == 's = format("hello", "s")'


def test_math_blocks_registered():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    reg = get_registry()
    for name in ["math_abs", "math_round", "math_pow", "math_pow_mod",
                 "math_divmod", "math_min", "math_max", "math_sum",
                 "math_hash", "math_id"]:
        assert name in reg, f"{name} not registered"

def test_math_abs_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["math_abs"].generate(result="n", value="-5")
    assert code == "n = abs(-5)"

def test_math_pow_mod_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["math_pow_mod"].generate(result="r", base="2", exp="10", mod="1000")
    assert code == "r = pow(2, 10, 1000)"

def test_math_round_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["math_round"].generate(result="r", value="3.14159", ndigits="2")
    assert code == "r = round(3.14159, 2)"

def test_sequence_blocks_registered():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    reg = get_registry()
    for name in ["seq_index", "seq_slice", "seq_slice_step", "seq_len",
                 "seq_sorted", "seq_sorted_key", "seq_reversed", "seq_enumerate",
                 "seq_zip", "seq_map", "seq_filter", "seq_range",
                 "seq_range_start", "seq_range_step", "seq_all", "seq_any"]:
        assert name in reg, f"{name} not registered"

def test_seq_index_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["seq_index"].generate(result="x", seq="my_list", index="0")
    assert code == "x = my_list[0]"

def test_seq_slice_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["seq_slice"].generate(result="s", seq="text", start="1", stop="4")
    assert code == "s = text[1:4]"

def test_seq_range_step_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["seq_range_step"].generate(result="r", start="0", stop="10", step="2")
    assert code == "r = range(0, 10, 2)"

def test_seq_len_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["seq_len"].generate(result="n", seq="items")
    assert code == "n = len(items)"


def test_list_blocks_registered():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    reg = get_registry()
    for name in ["list_new", "list_new_vals", "list_append", "list_insert",
                 "list_pop", "list_remove", "list_extend", "list_sort",
                 "list_reverse", "list_clear", "list_index_of", "list_count", "list_copy"]:
        assert name in reg, f"{name} not registered"

def test_list_append_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["list_append"].generate(name="items", value="42")
    assert code == "items.append(42)"

def test_dict_blocks_registered():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    reg = get_registry()
    for name in ["dict_new", "dict_set", "dict_get", "dict_get_default",
                 "dict_delete", "dict_keys", "dict_values", "dict_items",
                 "dict_update", "dict_pop", "dict_clear", "dict_copy", "dict_in"]:
        assert name in reg, f"{name} not registered"

def test_dict_new_generates_dict_call():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["dict_new"].generate(name="d")
    assert code == "d = dict()"

def test_dict_get_default_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["dict_get_default"].generate(result="v", name="d", key='"x"', default="0")
    assert code == 'v = d.get("x", 0)'

def test_set_blocks_registered():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    reg = get_registry()
    for name in ["set_new", "set_new_vals", "set_add", "set_remove",
                 "set_discard", "set_union", "set_intersect", "set_diff",
                 "set_sym_diff", "set_in", "set_issubset", "set_issuperset"]:
        assert name in reg, f"{name} not registered"

def test_set_new_vals_generates_braces():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["set_new_vals"].generate(name="s", values="1, 2, 3")
    assert code == "s = {1, 2, 3}"

def test_set_union_generates_pipe():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["set_union"].generate(result="c", a="s1", b="s2")
    assert code == "c = s1 | s2"

def test_inspection_blocks_registered():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    reg = get_registry()
    for name in ["insp_type", "insp_isinstance", "insp_issubclass", "insp_callable",
                 "insp_hasattr", "insp_getattr", "insp_getattr_default",
                 "insp_setattr", "insp_delattr", "insp_dir", "insp_vars",
                 "insp_globals", "insp_locals"]:
        assert name in reg, f"{name} not registered"

def test_insp_isinstance_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["insp_isinstance"].generate(result="ok", obj="x", classinfo="int")
    assert code == "ok = isinstance(x, int)"

def test_iteration_blocks_registered():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    reg = get_registry()
    for name in ["iter_iter", "iter_next", "iter_next_default",
                 "iter_aiter", "iter_anext"]:
        assert name in reg, f"{name} not registered"

def test_iter_next_default_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["iter_next_default"].generate(result="val", iterator="it", default="None")
    assert code == "val = next(it, None)"


def test_insp_globals_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["insp_globals"].generate(result="g")
    assert code == "g = globals()"


def test_insp_type_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["insp_type"].generate(result="t", value="x")
    assert code == "t = type(x)"


def test_insp_setattr_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["insp_setattr"].generate(obj="x", name='"y"', value="1")
    assert code == 'setattr(x, "y", 1)'


def test_insp_getattr_default_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["insp_getattr_default"].generate(result="v", obj="x", name='"attr"', default="0")
    assert code == 'v = getattr(x, "attr", 0)'


def test_advanced_blocks_registered():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    reg = get_registry()
    for name in ["adv_eval", "adv_exec", "adv_compile", "adv_breakpoint",
                 "adv_help", "adv_object", "adv_super", "adv_property",
                 "adv_staticmethod", "adv_classmethod", "adv_memoryview", "adv_slice"]:
        assert name in reg, f"{name} not registered"

def test_adv_breakpoint_generates_call():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["adv_breakpoint"].generate()
    assert code == "breakpoint()"

def test_adv_eval_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["adv_eval"].generate(result="x", expr='"1+1"')
    assert code == 'x = eval("1+1")'

def test_adv_exec_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["adv_exec"].generate(code='"x=1"')
    assert code == 'exec("x=1")'

def test_adv_object_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["adv_object"].generate(result="obj")
    assert code == "obj = object()"

def test_adv_slice_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["adv_slice"].generate(result="s", start="1", stop="5", step="2")
    assert code == "s = slice(1, 5, 2)"

def test_match_case_blocks_registered():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    reg = get_registry()
    for name in ["match_block", "case_block", "case_wildcard"]:
        assert name in reg, f"{name} not registered"

def test_match_block_is_indent():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    assert get_registry()["match_block"].indent is True

def test_case_block_is_indent():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    assert get_registry()["case_block"].indent is True

def test_match_block_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["match_block"].generate(expr="command")
    assert code == "match command:"

def test_case_block_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["case_block"].generate(pattern='"quit"')
    assert code == 'case "quit":'

def test_case_wildcard_generates_code():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["case_wildcard"].generate()
    assert code == "case _:"

def test_decorator_blocks_registered():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    reg = get_registry()
    assert "decorator_block" in reg
    assert "decorator_args" in reg

def test_decorator_block_is_not_indent():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    assert get_registry()["decorator_block"].indent is False

def test_decorator_block_generates_at_sign():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["decorator_block"].generate(name="my_decorator")
    assert code == "@my_decorator"

def test_decorator_args_generates_with_parens():
    import pyblocks.blocks.builtins
    from pyblocks.blocks.definition import get_registry
    code = get_registry()["decorator_args"].generate(name="app.route", args='"/home"')
    assert code == '@app.route("/home")'
