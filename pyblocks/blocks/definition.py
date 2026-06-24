from __future__ import annotations
import inspect
from dataclasses import dataclass, field
from typing import Callable

_REGISTRY: dict[str, "BlockDefinition"] = {}

@dataclass
class BlockDefinition:
    name: str
    label: str
    category: str
    color: str
    description: str
    indent: bool
    inputs: list[str]
    _fn: Callable

    def generate(self, **kwargs) -> str:
        return self._fn(**kwargs)

def block(label: str, category: str, color: str = "#89b4fa",
          description: str = "", indent: bool = False):
    """Decorator to register a block definition."""
    def decorator(fn: Callable) -> Callable:
        params = list(inspect.signature(fn).parameters.keys())
        defn = BlockDefinition(
            name=fn.__name__,
            label=label,
            category=category,
            color=color,
            description=description,
            indent=indent,
            inputs=params,
            _fn=fn,
        )
        _REGISTRY[fn.__name__] = defn
        return fn
    return decorator

def get_registry() -> dict[str, BlockDefinition]:
    return _REGISTRY

def clear_registry() -> None:
    _REGISTRY.clear()

def register_block(defn: "BlockDefinition") -> None:
    _REGISTRY[defn.name] = defn
