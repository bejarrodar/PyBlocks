from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Project:
    name: str
    root: Path
    active_file: str = "main.py"
    expansions: list[str] = field(default_factory=list)
    enabled_packages: list[str] = field(default_factory=list)

    @property
    def pyblocks_dir(self) -> Path:
        return self.root / ".pyblocks"

    @property
    def cache_dir(self) -> Path:
        return self.root / ".pyblocks_cache"
