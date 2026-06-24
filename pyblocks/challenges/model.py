from __future__ import annotations
from dataclasses import dataclass, asdict


@dataclass
class Challenge:
    title: str
    description: str
    difficulty: str = "beginner"
    starter_comment: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Challenge":
        return cls(
            title=data.get("title", ""),
            description=data.get("description", ""),
            difficulty=data.get("difficulty", "beginner"),
            starter_comment=data.get("starter_comment", ""),
        )
