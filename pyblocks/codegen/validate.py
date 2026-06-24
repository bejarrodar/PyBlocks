from __future__ import annotations
import keyword

# (block_type, input_key) → human label used in error messages
_IDENTIFIER_FIELDS: dict[tuple[str, str], str] = {
    ("def_block",        "name"):        "function name",
    ("class_block",      "name"):        "class name",
    ("assign_block",     "name"):        "variable name",
    ("global_block",     "name"):        "variable name",
    ("for_block",        "target"):      "loop variable",
    ("create_instance",  "var_name"):    "variable name",
    ("create_instance",  "class_name"):  "class name",
    ("call_method",      "var_name"):    "variable name",
    ("call_method",      "method_name"): "method name",
}

# Fields that must not be left blank (regardless of identifier rules)
_REQUIRED_FIELDS: dict[tuple[str, str], str] = {
    ("def_block",    "name"):   "function name",
    ("class_block",  "name"):   "class name",
    ("assign_block", "name"):   "variable name",
    ("assign_block", "value"):  "value",
    ("for_block",    "target"): "loop variable",
    ("for_block",    "iterable"): "iterable",
}


def validate_block_inputs(block_type: str, inputs: dict[str, str]) -> list[str]:
    """Return a list of human-readable error strings; empty means valid."""
    errors: list[str] = []
    seen: set[str] = set()

    # Identifier checks
    for (btype, field), label in _IDENTIFIER_FIELDS.items():
        if btype != block_type:
            continue
        value = inputs.get(field, "").strip()
        seen.add(field)
        if not value:
            errors.append(f"{label.capitalize()} cannot be empty.")
            continue
        if not value.isidentifier():
            # Give a specific hint for the most common mistake: spaces
            if " " in value:
                errors.append(
                    f'"{value}" is not a valid {label} — '
                    "names cannot contain spaces "
                    f'(did you mean "{value.replace(" ", "_")}"?)'
                )
            elif value[0].isdigit():
                errors.append(
                    f'"{value}" is not a valid {label} — '
                    "names cannot start with a digit."
                )
            else:
                errors.append(
                    f'"{value}" is not a valid {label} — '
                    "use only letters, digits, and underscores."
                )
        elif keyword.iskeyword(value):
            errors.append(
                f'"{value}" is a Python keyword and cannot be used as a {label}.'
            )

    # Required-field checks for fields not already covered above
    for (btype, field), label in _REQUIRED_FIELDS.items():
        if btype != block_type or field in seen:
            continue
        value = inputs.get(field, "").strip()
        if not value:
            errors.append(f"{label.capitalize()} cannot be empty.")

    return errors
