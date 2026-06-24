from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class ExpansionPack:
    name: str
    display_name: str
    description: str = ""
    source: str = "local"        # "local" or "installed"
    source_path: str = ""        # file path for local; package name for installed
    block_names: list[str] = field(default_factory=list)
