from __future__ import annotations
import keyword
from dataclasses import dataclass, field

@dataclass
class CustomBlockDef:
    name: str
    label: str
    category: str = "Custom"
    color: str = "#fab387"
    inputs: list[str] = field(default_factory=list)
    template: str = ""
    description: str = ""

    def is_valid(self) -> bool:
        return (
            bool(self.name)
            and self.name.isidentifier()
            and not keyword.iskeyword(self.name)
        )
