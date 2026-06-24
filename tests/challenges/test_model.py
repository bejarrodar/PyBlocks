# tests/challenges/test_model.py
from pyblocks.challenges.model import Challenge


def test_challenge_creation():
    c = Challenge(
        title="Hello World",
        description="Print 'Hello, World!' to the console.",
        difficulty="beginner",
        starter_comment="# Start here",
    )
    assert c.title == "Hello World"
    assert c.difficulty == "beginner"


def test_challenge_defaults():
    c = Challenge(title="T", description="D")
    assert c.difficulty == "beginner"
    assert c.starter_comment == ""


def test_challenge_to_dict():
    c = Challenge(title="T", description="D", difficulty="easy",
                  starter_comment="# hint")
    d = c.to_dict()
    assert d["title"] == "T"
    assert d["difficulty"] == "easy"


def test_challenge_from_dict():
    data = {"title": "T", "description": "D",
            "difficulty": "medium", "starter_comment": "# go"}
    c = Challenge.from_dict(data)
    assert c.title == "T"
    assert c.starter_comment == "# go"
