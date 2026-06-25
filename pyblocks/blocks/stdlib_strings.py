from pyblocks.blocks.definition import block

# ── Strings ──────────────────────────────────────────────────────────────

# Case Conversion

@block(label="{result} = {s}.upper()", category="Strings", color="#a6e3a1",
       description="Convert string to uppercase.")
def str_upper(result, s):
    return f"{result} = {s}.upper()"


@block(label="{result} = {s}.lower()", category="Strings", color="#a6e3a1",
       description="Convert string to lowercase.")
def str_lower(result, s):
    return f"{result} = {s}.lower()"


@block(label="{result} = {s}.title()", category="Strings", color="#a6e3a1",
       description="Return titlecased version of string (first letter of each word capitalized).")
def str_title(result, s):
    return f"{result} = {s}.title()"


@block(label="{result} = {s}.capitalize()", category="Strings", color="#a6e3a1",
       description="Return capitalized version of string (first character uppercase, rest lowercase).")
def str_capitalize(result, s):
    return f"{result} = {s}.capitalize()"


@block(label="{result} = {s}.swapcase()", category="Strings", color="#a6e3a1",
       description="Return a string with all uppercase characters converted to lowercase and vice versa.")
def str_swapcase(result, s):
    return f"{result} = {s}.swapcase()"


# Stripping Whitespace

@block(label="{result} = {s}.strip()", category="Strings", color="#a6e3a1",
       description="Return a copy of string with leading and trailing whitespace removed.")
def str_strip(result, s):
    return f"{result} = {s}.strip()"


@block(label="{result} = {s}.lstrip()", category="Strings", color="#a6e3a1",
       description="Return a copy of string with leading whitespace removed.")
def str_lstrip(result, s):
    return f"{result} = {s}.lstrip()"


@block(label="{result} = {s}.rstrip()", category="Strings", color="#a6e3a1",
       description="Return a copy of string with trailing whitespace removed.")
def str_rstrip(result, s):
    return f"{result} = {s}.rstrip()"


# Splitting and Joining

@block(label="{result} = {s}.split({sep})", category="Strings", color="#a6e3a1",
       description="Split string by separator and return a list of substrings.")
def str_split(result, s, sep):
    return f"{result} = {s}.split({sep})"


@block(label="{result} = {s}.split()", category="Strings", color="#a6e3a1",
       description="Split string on whitespace and return a list of substrings.")
def str_split_ws(result, s):
    return f"{result} = {s}.split()"


@block(label="{result} = {sep}.join({iterable})", category="Strings", color="#a6e3a1",
       description="Join elements of an iterable with this string as separator.")
def str_join(result, sep, iterable):
    return f"{result} = {sep}.join({iterable})"


@block(label="{result} = {s}.splitlines()", category="Strings", color="#a6e3a1",
       description="Split string by line boundaries and return a list of lines.")
def str_splitlines(result, s):
    return f"{result} = {s}.splitlines()"


# Searching and Replacing

@block(label="{result} = {s}.replace({old}, {new})", category="Strings", color="#a6e3a1",
       description="Replace all occurrences of substring with another substring.")
def str_replace(result, s, old, new):
    return f"{result} = {s}.replace({old}, {new})"


@block(label="{result} = {s}.find({sub})", category="Strings", color="#a6e3a1",
       description="Return the index of first occurrence of substring, or -1 if not found.")
def str_find(result, s, sub):
    return f"{result} = {s}.find({sub})"


@block(label="{result} = {s}.rfind({sub})", category="Strings", color="#a6e3a1",
       description="Return the index of last occurrence of substring, or -1 if not found.")
def str_rfind(result, s, sub):
    return f"{result} = {s}.rfind({sub})"


@block(label="{result} = {s}.index({sub})", category="Strings", color="#a6e3a1",
       description="Return the index of first occurrence of substring, or raise ValueError if not found.")
def str_index(result, s, sub):
    return f"{result} = {s}.index({sub})"


@block(label="{result} = {s}.count({sub})", category="Strings", color="#a6e3a1",
       description="Return the number of non-overlapping occurrences of substring.")
def str_count(result, s, sub):
    return f"{result} = {s}.count({sub})"


# Checking Content

@block(label="{result} = {s}.startswith({prefix})", category="Strings", color="#a6e3a1",
       description="Check if string starts with the given prefix.")
def str_startswith(result, s, prefix):
    return f"{result} = {s}.startswith({prefix})"


@block(label="{result} = {s}.endswith({suffix})", category="Strings", color="#a6e3a1",
       description="Check if string ends with the given suffix.")
def str_endswith(result, s, suffix):
    return f"{result} = {s}.endswith({suffix})"


@block(label="{result} = {s}.isdigit()", category="Strings", color="#a6e3a1",
       description="Check if all characters in string are digits.")
def str_isdigit(result, s):
    return f"{result} = {s}.isdigit()"


@block(label="{result} = {s}.isalpha()", category="Strings", color="#a6e3a1",
       description="Check if all characters in string are alphabetic.")
def str_isalpha(result, s):
    return f"{result} = {s}.isalpha()"


@block(label="{result} = {s}.isalnum()", category="Strings", color="#a6e3a1",
       description="Check if all characters in string are alphanumeric (letters and digits).")
def str_isalnum(result, s):
    return f"{result} = {s}.isalnum()"


@block(label="{result} = {s}.isspace()", category="Strings", color="#a6e3a1",
       description="Check if all characters in string are whitespace.")
def str_isspace(result, s):
    return f"{result} = {s}.isspace()"


@block(label="{result} = {s}.isnumeric()", category="Strings", color="#a6e3a1",
       description="Check if all characters in string are numeric characters.")
def str_isnumeric(result, s):
    return f"{result} = {s}.isnumeric()"


@block(label="{result} = {s}.islower()", category="Strings", color="#a6e3a1",
       description="Check if all cased characters in string are lowercase.")
def str_islower(result, s):
    return f"{result} = {s}.islower()"


@block(label="{result} = {s}.isupper()", category="Strings", color="#a6e3a1",
       description="Check if all cased characters in string are uppercase.")
def str_isupper(result, s):
    return f"{result} = {s}.isupper()"


# Alignment and Padding

@block(label="{result} = {s}.center({width})", category="Strings", color="#a6e3a1",
       description="Return centered version of string with specified width.")
def str_center(result, s, width):
    return f"{result} = {s}.center({width})"


@block(label="{result} = {s}.ljust({width})", category="Strings", color="#a6e3a1",
       description="Return left-justified version of string with specified width.")
def str_ljust(result, s, width):
    return f"{result} = {s}.ljust({width})"


@block(label="{result} = {s}.rjust({width})", category="Strings", color="#a6e3a1",
       description="Return right-justified version of string with specified width.")
def str_rjust(result, s, width):
    return f"{result} = {s}.rjust({width})"


@block(label="{result} = {s}.zfill({width})", category="Strings", color="#a6e3a1",
       description="Return string padded with zeros on the left to reach specified width.")
def str_zfill(result, s, width):
    return f"{result} = {s}.zfill({width})"


# Encoding and Decoding

@block(label="{result} = {s}.encode({encoding})", category="Strings", color="#a6e3a1",
       description="Encode string using the specified encoding and return bytes.")
def str_encode(result, s, encoding):
    return f"{result} = {s}.encode({encoding})"


@block(label="{result} = {b}.decode({encoding})", category="Strings", color="#a6e3a1",
       description="Decode bytes using the specified encoding and return a string.")
def str_decode(result, b, encoding):
    return f"{result} = {b}.decode({encoding})"


# Formatting

@block(label="{result} = {s}.format({args})", category="Strings", color="#a6e3a1",
       description="Format string by substituting placeholders with provided arguments.")
def str_format(result, s, args):
    return f"{result} = {s}.format({args})"


@block(label="{result} = {s}.format_map({mapping})", category="Strings", color="#a6e3a1",
       description="Format string by substituting placeholders using a mapping (dictionary).")
def str_format_map(result, s, mapping):
    return f"{result} = {s}.format_map({mapping})"
