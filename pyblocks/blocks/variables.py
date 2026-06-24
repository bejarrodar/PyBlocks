from __future__ import annotations
from pyblocks.blocks.definition import block, BlockDefinition, _REGISTRY

_DUNDER_VARS = [
    "__name__", "__file__", "__doc__",
    "__version__", "__author__", "__all__", "__package__",
]

for _v in _DUNDER_VARS:
    _key = f"var_{_v}"
    _val = _v  # capture loop variable

    defn = BlockDefinition(
        name=_key,
        label=_v,
        category="Preset Variables",
        color="#89dceb",
        description=f"Built-in variable: {_v}",
        indent=False,
        inputs=[],
        _fn=lambda v=_val: v,
    )
    _REGISTRY[_key] = defn

def make_user_variable_chip(var_name: str) -> BlockDefinition:
    key = f"user_var_{var_name}"
    defn = BlockDefinition(
        name=key,
        label=var_name,
        category="User Variables",
        color="#89b4fa",
        description=f"Variable: {var_name}",
        indent=False,
        inputs=[],
        _fn=lambda v=var_name: v,
    )
    return defn


def make_user_function_chip(fn_name: str) -> BlockDefinition:
    key = f"user_fn_{fn_name}"
    defn = BlockDefinition(
        name=key,
        label=f"{fn_name}({{args}})",
        category="User Functions",
        color="#f9e2af",
        description=f"Call function: {fn_name}",
        indent=False,
        inputs=["args"],
        _fn=lambda args="", fn=fn_name: f"{fn}({args})",
    )
    return defn
