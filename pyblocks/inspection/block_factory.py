from __future__ import annotations
import hashlib
from pyblocks.blocks.definition import BlockDefinition
from pyblocks.inspection.package_scanner import CallableEntry

PALETTE = [
    "#fab387",  # peach
    "#a6e3a1",  # green
    "#89b4fa",  # blue
    "#cba6f7",  # mauve
    "#f38ba8",  # red
    "#f9e2af",  # yellow
    "#94e2d5",  # teal
    "#89dceb",  # sky
    "#b4befe",  # lavender
    "#f2cdcd",  # flamingo
    "#eba0ac",  # maroon
    "#74c7ec",  # sapphire
]


def package_color(package_name: str) -> str:
    digest = hashlib.md5(package_name.encode()).digest()[0]
    return PALETTE[digest % len(PALETTE)]


def _make_category(submodule: str) -> str:
    parts = submodule.split(".", 1)
    top = parts[0].capitalize()
    if len(parts) == 1:
        return top
    return f"{top}: {parts[1]}"


def _make_generator(qualname: str, params: list[str]):
    def generate(**kwargs) -> str:
        result = kwargs.get("result", "_")
        args = ", ".join(kwargs.get(p, p) for p in params)
        return f"{result} = {qualname}({args})"
    return generate


class BlockFactory:
    @staticmethod
    def from_entries(entries: list[CallableEntry], color: str) -> list[BlockDefinition]:
        defns = []
        for entry in entries:
            param_tokens = ", ".join(f"{{{p}}}" for p in entry.params)
            label = f"{{result}} = {entry.qualname}({param_tokens})"
            inputs = ["result"] + list(entry.params)
            defns.append(BlockDefinition(
                name=entry.qualname,
                label=label,
                category=_make_category(entry.submodule),
                color=color,
                description="",
                indent=False,
                inputs=inputs,
                _fn=_make_generator(entry.qualname, entry.params),
            ))
        return defns
