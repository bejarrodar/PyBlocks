from __future__ import annotations
import json
import random
from pathlib import Path
from pyblocks.challenges.model import Challenge

_DATA_FILE = Path(__file__).parent.parent / "data" / "challenges.json"

class ChallengeBank:

    def __init__(self, data: list[Challenge]) -> None:
        self._data = data

    @classmethod
    def load(cls) -> "ChallengeBank":
        raw = json.loads(_DATA_FILE.read_text(encoding="utf-8"))
        return cls([Challenge.from_dict(d) for d in raw])

    def all(self) -> list[Challenge]:
        return list(self._data)

    def random(self) -> Challenge:
        if not self._data:
            raise ValueError("No challenges available")
        return random.choice(self._data)
