from pyblocks.blocks.definition import block

# ── Output ──────────────────────────────────────────────────────────────
@block(label="PRINT {value}", category="Output", color="#a6e3a1",
       description="Print a value to the console.")
def print_block(value):
    return f"print({value})"


# ── Variables ────────────────────────────────────────────────────────────
@block(label="SET {name} = {value}", category="Variables", color="#89b4fa",
       description="Assign a value to a variable.")
def assign_block(name, value):
    return f"{name} = {value}"


@block(label="GLOBAL {name}", category="Variables", color="#89dceb",
       description="Declare a variable as global inside a function.")
def global_block(name):
    return f"global {name}"


# ── Control ──────────────────────────────────────────────────────────────
@block(label="IF {condition}:", category="Control", color="#cba6f7",
       indent=True,
       description="Run the body if the condition is true.")
def if_block(condition):
    return f"if {condition}:"


@block(label="ELIF {condition}:", category="Control", color="#b4befe",
       indent=True,
       description="Else-if branch.")
def elif_block(condition):
    return f"elif {condition}:"


@block(label="ELSE:", category="Control", color="#b4befe",
       indent=True,
       description="Else branch — no condition.")
def else_block():
    return "else:"


@block(label="FOR {target} IN {iterable}:", category="Control", color="#fab387",
       indent=True,
       description="Iterate over a sequence.")
def for_block(target, iterable):
    return f"for {target} in {iterable}:"


@block(label="WHILE {condition}:", category="Control", color="#fab387",
       indent=True,
       description="Repeat while condition is true.")
def while_block(condition):
    return f"while {condition}:"


@block(label="BREAK", category="Control", color="#f38ba8",
       description="Exit the current loop immediately.")
def break_block():
    return "break"


@block(label="CONTINUE", category="Control", color="#f38ba8",
       description="Skip to the next loop iteration.")
def continue_block():
    return "continue"


@block(label="RETURN {value}", category="Control", color="#a6e3a1",
       description="Return a value from a function.")
def return_block(value):
    return f"return {value}"


# ── Functions & Classes ──────────────────────────────────────────────────
@block(label="DEF {name}({args}):", category="Functions", color="#f9e2af",
       indent=True,
       description="Define a function.")
def def_block(name, args):
    return f"def {name}({args}):"


@block(label="CLASS {name}({bases}):", category="Functions", color="#f9e2af",
       indent=True,
       description="Define a class.")
def class_block(name, bases):
    return f"class {name}({bases}):"


# ── Error Handling ───────────────────────────────────────────────────────
@block(label="TRY:", category="Error Handling", color="#eba0ac",
       indent=True,
       description="Try block — wrap risky code.")
def try_block():
    return "try:"


@block(label="EXCEPT {exc} AS {alias}:", category="Error Handling", color="#eba0ac",
       indent=True,
       description="Catch an exception.")
def except_block(exc, alias):
    return f"except {exc} as {alias}:"


@block(label="FINALLY:", category="Error Handling", color="#eba0ac",
       indent=True,
       description="Always-run cleanup block.")
def finally_block():
    return "finally:"


@block(label="RAISE {exc}", category="Error Handling", color="#f38ba8",
       description="Raise an exception.")
def raise_block(exc):
    return f"raise {exc}"


# ── Imports ──────────────────────────────────────────────────────────────
@block(label="IMPORT {module}", category="Imports", color="#94e2d5",
       description="Import a module.")
def import_block(module):
    return f"import {module}"


@block(label="FROM {module} IMPORT {names}", category="Imports", color="#94e2d5",
       description="Import specific names from a module.")
def from_import_block(module, names):
    return f"from {module} import {names}"


# ── Other ────────────────────────────────────────────────────────────────
@block(label="# {text}", category="Other", color="#6c7086",
       description="Write a comment.")
def comment_block(text):
    return f"# {text}"


@block(label="PASS", category="Other", color="#6c7086",
       description="No-op placeholder.")
def pass_block():
    return "pass"


@block(label="{expr}", category="Other", color="#7f849c",
       description="Any Python expression.")
def expr_block(expr):
    return expr


# ── I/O ────────────────────────────────────────────────────────────────────
@block(label="print({value})", category="I/O", color="#a6e3a1",
       description="Print a value.")
def io_print(value):
    return f"print({value})"


@block(label="print({value}, sep={sep})", category="I/O", color="#a6e3a1",
       description="Print with custom separator.")
def io_print_sep(value, sep):
    return f"print({value}, sep={sep})"


@block(label="print({value}, end={end})", category="I/O", color="#a6e3a1",
       description="Print with custom end character.")
def io_print_end(value, end):
    return f"print({value}, end={end})"


@block(label='print(f"{text}")', category="I/O", color="#a6e3a1",
       description="Print an f-string.")
def io_print_fstring(text):
    return f'print(f"{{{text}}}")'


@block(label="{result} = input({prompt})", category="I/O", color="#a6e3a1",
       description="Read a line of input.")
def io_input(result, prompt):
    return f"{result} = input({prompt})"


@block(label="{result} = open({path}, {mode})", category="I/O", color="#a6e3a1",
       description="Open a file.")
def io_open(result, path, mode):
    return f"{result} = open({path}, {mode})"


# ── Type Casting ───────────────────────────────────────────────────────────
@block(label="{result} = int({value})", category="Type Casting", color="#89dceb",
       description="Convert to integer.")
def cast_int(result, value):
    return f"{result} = int({value})"


@block(label="{result} = int({value}, {base})", category="Type Casting", color="#89dceb",
       description="Convert string to integer with given base.")
def cast_int_base(result, value, base):
    return f"{result} = int({value}, {base})"


@block(label="{result} = str({value})", category="Type Casting", color="#89dceb",
       description="Convert to string.")
def cast_str(result, value):
    return f"{result} = str({value})"


@block(label="{result} = float({value})", category="Type Casting", color="#89dceb",
       description="Convert to float.")
def cast_float(result, value):
    return f"{result} = float({value})"


@block(label="{result} = bool({value})", category="Type Casting", color="#89dceb",
       description="Convert to boolean.")
def cast_bool(result, value):
    return f"{result} = bool({value})"


@block(label="{result} = list({value})", category="Type Casting", color="#89dceb",
       description="Convert to list.")
def cast_list(result, value):
    return f"{result} = list({value})"


@block(label="{result} = tuple({value})", category="Type Casting", color="#89dceb",
       description="Convert to tuple.")
def cast_tuple(result, value):
    return f"{result} = tuple({value})"


@block(label="{result} = set({value})", category="Type Casting", color="#89dceb",
       description="Convert to set.")
def cast_set(result, value):
    return f"{result} = set({value})"


@block(label="{result} = frozenset({value})", category="Type Casting", color="#89dceb",
       description="Convert to frozenset.")
def cast_frozenset(result, value):
    return f"{result} = frozenset({value})"


@block(label="{result} = dict({value})", category="Type Casting", color="#89dceb",
       description="Convert to dict.")
def cast_dict(result, value):
    return f"{result} = dict({value})"


@block(label="{result} = bytes({value})", category="Type Casting", color="#89dceb",
       description="Convert to bytes.")
def cast_bytes(result, value):
    return f"{result} = bytes({value})"


@block(label="{result} = bytearray({value})", category="Type Casting", color="#89dceb",
       description="Convert to bytearray.")
def cast_bytearray(result, value):
    return f"{result} = bytearray({value})"


@block(label="{result} = complex({real}, {imag})", category="Type Casting", color="#89dceb",
       description="Create a complex number.")
def cast_complex(result, real, imag):
    return f"{result} = complex({real}, {imag})"


@block(label="{result} = chr({value})", category="Type Casting", color="#89dceb",
       description="Convert integer to Unicode character.")
def cast_chr(result, value):
    return f"{result} = chr({value})"


@block(label="{result} = ord({value})", category="Type Casting", color="#89dceb",
       description="Convert character to integer code point.")
def cast_ord(result, value):
    return f"{result} = ord({value})"


@block(label="{result} = bin({value})", category="Type Casting", color="#89dceb",
       description="Convert integer to binary string.")
def cast_bin(result, value):
    return f"{result} = bin({value})"


@block(label="{result} = hex({value})", category="Type Casting", color="#89dceb",
       description="Convert integer to hex string.")
def cast_hex(result, value):
    return f"{result} = hex({value})"


@block(label="{result} = oct({value})", category="Type Casting", color="#89dceb",
       description="Convert integer to octal string.")
def cast_oct(result, value):
    return f"{result} = oct({value})"


@block(label="{result} = repr({value})", category="Type Casting", color="#89dceb",
       description="Return string representation of object.")
def cast_repr(result, value):
    return f"{result} = repr({value})"


@block(label="{result} = ascii({value})", category="Type Casting", color="#89dceb",
       description="Return ASCII-safe string representation.")
def cast_ascii(result, value):
    return f"{result} = ascii({value})"


@block(label="{result} = format({value}, {spec})", category="Type Casting", color="#89dceb",
       description="Format value according to format spec.")
def cast_format(result, value, spec):
    return f"{result} = format({value}, {spec})"


# ── Math ───────────────────────────────────────────────────────────────────
@block(label="{result} = abs({value})", category="Math", color="#f9e2af",
       description="Absolute value.")
def math_abs(result, value):
    return f"{result} = abs({value})"

@block(label="{result} = round({value}, {ndigits})", category="Math", color="#f9e2af",
       description="Round to ndigits decimal places.")
def math_round(result, value, ndigits):
    return f"{result} = round({value}, {ndigits})"

@block(label="{result} = pow({base}, {exp})", category="Math", color="#f9e2af",
       description="Raise base to the power exp.")
def math_pow(result, base, exp):
    return f"{result} = pow({base}, {exp})"

@block(label="{result} = pow({base}, {exp}, {mod})", category="Math", color="#f9e2af",
       description="Modular exponentiation: (base**exp) % mod.")
def math_pow_mod(result, base, exp, mod):
    return f"{result} = pow({base}, {exp}, {mod})"

@block(label="{result} = divmod({a}, {b})", category="Math", color="#f9e2af",
       description="Return (quotient, remainder) tuple.")
def math_divmod(result, a, b):
    return f"{result} = divmod({a}, {b})"

@block(label="{result} = min({iterable})", category="Math", color="#f9e2af",
       description="Smallest item in iterable.")
def math_min(result, iterable):
    return f"{result} = min({iterable})"

@block(label="{result} = max({iterable})", category="Math", color="#f9e2af",
       description="Largest item in iterable.")
def math_max(result, iterable):
    return f"{result} = max({iterable})"

@block(label="{result} = sum({iterable})", category="Math", color="#f9e2af",
       description="Sum all items in iterable.")
def math_sum(result, iterable):
    return f"{result} = sum({iterable})"

@block(label="{result} = hash({value})", category="Math", color="#f9e2af",
       description="Hash value of an object.")
def math_hash(result, value):
    return f"{result} = hash({value})"

@block(label="{result} = id({value})", category="Math", color="#f9e2af",
       description="Identity (memory address) of an object.")
def math_id(result, value):
    return f"{result} = id({value})"


# ── Sequences ─────────────────────────────────────────────────────────────
@block(label="{result} = {seq}[{index}]", category="Sequences", color="#cba6f7",
       description="Get item at index (works on list, str, tuple, bytes).")
def seq_index(result, seq, index):
    return f"{result} = {seq}[{index}]"

@block(label="{result} = {seq}[{start}:{stop}]", category="Sequences", color="#cba6f7",
       description="Slice a sequence.")
def seq_slice(result, seq, start, stop):
    return f"{result} = {seq}[{start}:{stop}]"

@block(label="{result} = {seq}[{start}:{stop}:{step}]", category="Sequences", color="#cba6f7",
       description="Slice a sequence with step.")
def seq_slice_step(result, seq, start, stop, step):
    return f"{result} = {seq}[{start}:{stop}:{step}]"

@block(label="{result} = len({seq})", category="Sequences", color="#cba6f7",
       description="Length of a sequence.")
def seq_len(result, seq):
    return f"{result} = len({seq})"

@block(label="{result} = sorted({iterable})", category="Sequences", color="#cba6f7",
       description="Return new sorted list.")
def seq_sorted(result, iterable):
    return f"{result} = sorted({iterable})"

@block(label="{result} = sorted({iterable}, key={key})", category="Sequences", color="#cba6f7",
       description="Return new sorted list with custom key function.")
def seq_sorted_key(result, iterable, key):
    return f"{result} = sorted({iterable}, key={key})"

@block(label="{result} = list(reversed({iterable}))", category="Sequences", color="#cba6f7",
       description="Return a reversed list.")
def seq_reversed(result, iterable):
    return f"{result} = list(reversed({iterable}))"

@block(label="{result} = enumerate({iterable})", category="Sequences", color="#cba6f7",
       description="Return (index, value) pairs.")
def seq_enumerate(result, iterable):
    return f"{result} = enumerate({iterable})"

@block(label="{result} = zip({a}, {b})", category="Sequences", color="#cba6f7",
       description="Pair up two iterables.")
def seq_zip(result, a, b):
    return f"{result} = zip({a}, {b})"

@block(label="{result} = map({func}, {iterable})", category="Sequences", color="#cba6f7",
       description="Apply function to every item.")
def seq_map(result, func, iterable):
    return f"{result} = map({func}, {iterable})"

@block(label="{result} = filter({func}, {iterable})", category="Sequences", color="#cba6f7",
       description="Keep items where function returns True.")
def seq_filter(result, func, iterable):
    return f"{result} = filter({func}, {iterable})"

@block(label="{result} = range({stop})", category="Sequences", color="#cba6f7",
       description="Range from 0 to stop.")
def seq_range(result, stop):
    return f"{result} = range({stop})"

@block(label="{result} = range({start}, {stop})", category="Sequences", color="#cba6f7",
       description="Range from start to stop.")
def seq_range_start(result, start, stop):
    return f"{result} = range({start}, {stop})"

@block(label="{result} = range({start}, {stop}, {step})", category="Sequences", color="#cba6f7",
       description="Range from start to stop with step.")
def seq_range_step(result, start, stop, step):
    return f"{result} = range({start}, {stop}, {step})"

@block(label="{result} = all({iterable})", category="Sequences", color="#cba6f7",
       description="True if all items are truthy.")
def seq_all(result, iterable):
    return f"{result} = all({iterable})"

@block(label="{result} = any({iterable})", category="Sequences", color="#cba6f7",
       description="True if any item is truthy.")
def seq_any(result, iterable):
    return f"{result} = any({iterable})"


# ── Lists ──────────────────────────────────────────────────────────────────
@block(label="{name} = []", category="Lists", color="#89b4fa",
       description="Create an empty list.")
def list_new(name):
    return f"{name} = []"

@block(label="{name} = [{values}]", category="Lists", color="#89b4fa",
       description="Create a list with initial values.")
def list_new_vals(name, values):
    return f"{name} = [{values}]"

@block(label="{name}.append({value})", category="Lists", color="#89b4fa",
       description="Append value to end of list.")
def list_append(name, value):
    return f"{name}.append({value})"

@block(label="{name}.insert({index}, {value})", category="Lists", color="#89b4fa",
       description="Insert value at index.")
def list_insert(name, index, value):
    return f"{name}.insert({index}, {value})"

@block(label="{name}.pop({index})", category="Lists", color="#89b4fa",
       description="Remove and return item at index.")
def list_pop(name, index):
    return f"{name}.pop({index})"

@block(label="{name}.remove({value})", category="Lists", color="#89b4fa",
       description="Remove first occurrence of value.")
def list_remove(name, value):
    return f"{name}.remove({value})"

@block(label="{name}.extend({other})", category="Lists", color="#89b4fa",
       description="Extend list with another iterable.")
def list_extend(name, other):
    return f"{name}.extend({other})"

@block(label="{name}.sort()", category="Lists", color="#89b4fa",
       description="Sort list in-place.")
def list_sort(name):
    return f"{name}.sort()"

@block(label="{name}.reverse()", category="Lists", color="#89b4fa",
       description="Reverse list in-place.")
def list_reverse(name):
    return f"{name}.reverse()"

@block(label="{name}.clear()", category="Lists", color="#89b4fa",
       description="Remove all items from list.")
def list_clear(name):
    return f"{name}.clear()"

@block(label="{result} = {name}.index({value})", category="Lists", color="#89b4fa",
       description="Find index of value.")
def list_index_of(result, name, value):
    return f"{result} = {name}.index({value})"

@block(label="{result} = {name}.count({value})", category="Lists", color="#89b4fa",
       description="Count occurrences of value.")
def list_count(result, name, value):
    return f"{result} = {name}.count({value})"

@block(label="{result} = {name}.copy()", category="Lists", color="#89b4fa",
       description="Shallow copy of list.")
def list_copy(result, name):
    return f"{result} = {name}.copy()"


# ── Dictionaries ───────────────────────────────────────────────────────────
@block(label="{name} = dict()", category="Dictionaries", color="#f9e2af",
       description="Create an empty dictionary.")
def dict_new(name):
    return f"{name} = dict()"

@block(label="{name}[{key}] = {value}", category="Dictionaries", color="#f9e2af",
       description="Set a key-value pair.")
def dict_set(name, key, value):
    return f"{name}[{key}] = {value}"

@block(label="{result} = {name}[{key}]", category="Dictionaries", color="#f9e2af",
       description="Get value by key.")
def dict_get(result, name, key):
    return f"{result} = {name}[{key}]"

@block(label="{result} = {name}.get({key}, {default})", category="Dictionaries", color="#f9e2af",
       description="Get value by key with default.")
def dict_get_default(result, name, key, default):
    return f"{result} = {name}.get({key}, {default})"

@block(label="del {name}[{key}]", category="Dictionaries", color="#f9e2af",
       description="Delete a key from dictionary.")
def dict_delete(name, key):
    return f"del {name}[{key}]"

@block(label="{result} = {name}.keys()", category="Dictionaries", color="#f9e2af",
       description="Get all keys.")
def dict_keys(result, name):
    return f"{result} = {name}.keys()"

@block(label="{result} = {name}.values()", category="Dictionaries", color="#f9e2af",
       description="Get all values.")
def dict_values(result, name):
    return f"{result} = {name}.values()"

@block(label="{result} = {name}.items()", category="Dictionaries", color="#f9e2af",
       description="Get all key-value pairs.")
def dict_items(result, name):
    return f"{result} = {name}.items()"

@block(label="{name}.update({other})", category="Dictionaries", color="#f9e2af",
       description="Merge another dict into this one.")
def dict_update(name, other):
    return f"{name}.update({other})"

@block(label="{result} = {name}.pop({key})", category="Dictionaries", color="#f9e2af",
       description="Remove key and return its value.")
def dict_pop(result, name, key):
    return f"{result} = {name}.pop({key})"

@block(label="{name}.clear()", category="Dictionaries", color="#f9e2af",
       description="Remove all items from dictionary.")
def dict_clear(name):
    return f"{name}.clear()"

@block(label="{result} = {name}.copy()", category="Dictionaries", color="#f9e2af",
       description="Shallow copy of dictionary.")
def dict_copy(result, name):
    return f"{result} = {name}.copy()"

@block(label="{result} = {key} in {name}", category="Dictionaries", color="#f9e2af",
       description="Check if key exists in dictionary.")
def dict_in(result, key, name):
    return f"{result} = {key} in {name}"


# ── Sets ───────────────────────────────────────────────────────────────────
@block(label="{name} = set()", category="Sets", color="#eba0ac",
       description="Create an empty set.")
def set_new(name):
    return f"{name} = set()"

@block(label="{name} = {values}", category="Sets", color="#eba0ac",
       description="Create a set with initial values (displayed as {values}).")
def set_new_vals(name, values):
    return name + " = {" + values + "}"

@block(label="{name}.add({value})", category="Sets", color="#eba0ac",
       description="Add value to set.")
def set_add(name, value):
    return f"{name}.add({value})"

@block(label="{name}.remove({value})", category="Sets", color="#eba0ac",
       description="Remove value (raises KeyError if missing).")
def set_remove(name, value):
    return f"{name}.remove({value})"

@block(label="{name}.discard({value})", category="Sets", color="#eba0ac",
       description="Remove value if present (no error if missing).")
def set_discard(name, value):
    return f"{name}.discard({value})"

@block(label="{result} = {a} | {b}", category="Sets", color="#eba0ac",
       description="Union of two sets.")
def set_union(result, a, b):
    return f"{result} = {a} | {b}"

@block(label="{result} = {a} & {b}", category="Sets", color="#eba0ac",
       description="Intersection of two sets.")
def set_intersect(result, a, b):
    return f"{result} = {a} & {b}"

@block(label="{result} = {a} - {b}", category="Sets", color="#eba0ac",
       description="Difference of two sets.")
def set_diff(result, a, b):
    return f"{result} = {a} - {b}"

@block(label="{result} = {a} ^ {b}", category="Sets", color="#eba0ac",
       description="Symmetric difference of two sets.")
def set_sym_diff(result, a, b):
    return f"{result} = {a} ^ {b}"

@block(label="{result} = {value} in {name}", category="Sets", color="#eba0ac",
       description="Check if value is in set.")
def set_in(result, value, name):
    return f"{result} = {value} in {name}"

@block(label="{result} = {a}.issubset({b})", category="Sets", color="#eba0ac",
       description="True if a is a subset of b.")
def set_issubset(result, a, b):
    return f"{result} = {a}.issubset({b})"

@block(label="{result} = {a}.issuperset({b})", category="Sets", color="#eba0ac",
       description="True if a is a superset of b.")
def set_issuperset(result, a, b):
    return f"{result} = {a}.issuperset({b})"


# ── Inspection ─────────────────────────────────────────────────────────────
@block(label="{result} = type({value})", category="Inspection", color="#94e2d5",
       description="Get the type of an object.")
def insp_type(result, value):
    return f"{result} = type({value})"

@block(label="{result} = isinstance({obj}, {classinfo})", category="Inspection", color="#94e2d5",
       description="Check if object is an instance of class.")
def insp_isinstance(result, obj, classinfo):
    return f"{result} = isinstance({obj}, {classinfo})"

@block(label="{result} = issubclass({cls}, {classinfo})", category="Inspection", color="#94e2d5",
       description="Check if class is a subclass.")
def insp_issubclass(result, cls, classinfo):
    return f"{result} = issubclass({cls}, {classinfo})"

@block(label="{result} = callable({obj})", category="Inspection", color="#94e2d5",
       description="True if object is callable.")
def insp_callable(result, obj):
    return f"{result} = callable({obj})"

@block(label="{result} = hasattr({obj}, {name})", category="Inspection", color="#94e2d5",
       description="True if object has the named attribute.")
def insp_hasattr(result, obj, name):
    return f"{result} = hasattr({obj}, {name})"

@block(label="{result} = getattr({obj}, {name})", category="Inspection", color="#94e2d5",
       description="Get named attribute of object.")
def insp_getattr(result, obj, name):
    return f"{result} = getattr({obj}, {name})"

@block(label="{result} = getattr({obj}, {name}, {default})", category="Inspection", color="#94e2d5",
       description="Get named attribute with fallback default.")
def insp_getattr_default(result, obj, name, default):
    return f"{result} = getattr({obj}, {name}, {default})"

@block(label="setattr({obj}, {name}, {value})", category="Inspection", color="#94e2d5",
       description="Set named attribute on object.")
def insp_setattr(obj, name, value):
    return f"setattr({obj}, {name}, {value})"

@block(label="delattr({obj}, {name})", category="Inspection", color="#94e2d5",
       description="Delete named attribute from object.")
def insp_delattr(obj, name):
    return f"delattr({obj}, {name})"

@block(label="{result} = dir({obj})", category="Inspection", color="#94e2d5",
       description="List names in current scope or object's attributes.")
def insp_dir(result, obj):
    return f"{result} = dir({obj})"

@block(label="{result} = vars({obj})", category="Inspection", color="#94e2d5",
       description="Return __dict__ of object.")
def insp_vars(result, obj):
    return f"{result} = vars({obj})"

@block(label="{result} = globals()", category="Inspection", color="#94e2d5",
       description="Return global symbol table dictionary.")
def insp_globals(result):
    return f"{result} = globals()"

@block(label="{result} = locals()", category="Inspection", color="#94e2d5",
       description="Return local symbol table dictionary.")
def insp_locals(result):
    return f"{result} = locals()"


# ── Iteration ──────────────────────────────────────────────────────────────
@block(label="{result} = iter({obj})", category="Iteration", color="#b4befe",
       description="Return an iterator for the object.")
def iter_iter(result, obj):
    return f"{result} = iter({obj})"

@block(label="{result} = next({iterator})", category="Iteration", color="#b4befe",
       description="Return next item from iterator.")
def iter_next(result, iterator):
    return f"{result} = next({iterator})"

@block(label="{result} = next({iterator}, {default})", category="Iteration", color="#b4befe",
       description="Return next item, or default if exhausted.")
def iter_next_default(result, iterator, default):
    return f"{result} = next({iterator}, {default})"

@block(label="{result} = aiter({obj})", category="Iteration", color="#b4befe",
       description="Return an async iterator. (3.10+)")
def iter_aiter(result, obj):
    return f"{result} = aiter({obj})"

@block(label="{result} = anext({iterator})", category="Iteration", color="#b4befe",
       description="Return next item from async iterator. (3.10+)")
def iter_anext(result, iterator):
    return f"{result} = anext({iterator})"


# ── Advanced ───────────────────────────────────────────────────────────────
@block(label="{result} = eval({expr})", category="Advanced", color="#7f849c",
       description="Evaluate a Python expression string.")
def adv_eval(result, expr):
    return f"{result} = eval({expr})"

@block(label="exec({code})", category="Advanced", color="#7f849c",
       description="Execute a Python code string.")
def adv_exec(code):
    return f"exec({code})"

@block(label="{result} = compile({src}, {filename}, {mode})", category="Advanced",
       color="#7f849c", description="Compile source to code object.")
def adv_compile(result, src, filename, mode):
    return f"{result} = compile({src}, {filename}, {mode})"

@block(label="breakpoint()", category="Advanced", color="#7f849c",
       description="Drop into the debugger.")
def adv_breakpoint():
    return "breakpoint()"

@block(label="help({obj})", category="Advanced", color="#7f849c",
       description="Show help for an object.")
def adv_help(obj):
    return f"help({obj})"

@block(label="{result} = object()", category="Advanced", color="#7f849c",
       description="Create a base object instance.")
def adv_object(result):
    return f"{result} = object()"

@block(label="{result} = super()", category="Advanced", color="#7f849c",
       description="Return a proxy to the parent class.")
def adv_super(result):
    return f"{result} = super()"

@block(label="{name} = property({fget})", category="Advanced", color="#7f849c",
       description="Create a property descriptor.")
def adv_property(name, fget):
    return f"{name} = property({fget})"

@block(label="{name} = staticmethod({func})", category="Advanced", color="#7f849c",
       description="Convert function to static method.")
def adv_staticmethod(name, func):
    return f"{name} = staticmethod({func})"

@block(label="{name} = classmethod({func})", category="Advanced", color="#7f849c",
       description="Convert function to class method.")
def adv_classmethod(name, func):
    return f"{name} = classmethod({func})"

@block(label="{result} = memoryview({obj})", category="Advanced", color="#7f849c",
       description="Create a memory view of a bytes-like object.")
def adv_memoryview(result, obj):
    return f"{result} = memoryview({obj})"

@block(label="{result} = slice({start}, {stop}, {step})", category="Advanced",
       color="#7f849c", description="Create a slice object.")
def adv_slice(result, start, stop, step):
    return f"{result} = slice({start}, {stop}, {step})"


# ── Match / Case (Python 3.10+) ────────────────────────────────────────────
@block(label="match {expr}:", category="Control", color="#cba6f7",
       indent=True,
       description="Match statement (Python 3.10+). Children must be case blocks.")
def match_block(expr):
    return f"match {expr}:"

@block(label="case {pattern}:", category="Control", color="#b4befe",
       indent=True,
       description="Case branch inside a match block.")
def case_block(pattern):
    return f"case {pattern}:"

@block(label="case _:", category="Control", color="#b4befe",
       indent=True,
       description="Wildcard case — matches anything.")
def case_wildcard():
    return "case _:"


# ── Decorators ────────────────────────────────────────────────────────────
@block(label="@{name}", category="Functions", color="#f9e2af",
       description="Decorator — place above a def or class block.")
def decorator_block(name):
    return f"@{name}"

@block(label="@{name}({args})", category="Functions", color="#f9e2af",
       description="Decorator with arguments — place above a def or class block.")
def decorator_args(name, args):
    return f"@{name}({args})"
