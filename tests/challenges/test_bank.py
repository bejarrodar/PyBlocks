# tests/challenges/test_bank.py
import pytest
from pyblocks.challenges.bank import ChallengeBank
from pyblocks.challenges.model import Challenge

def test_load_returns_challenges():
    bank = ChallengeBank.load()
    assert len(bank.all()) > 0

def test_all_items_are_challenges():
    bank = ChallengeBank.load()
    for item in bank.all():
        assert isinstance(item, Challenge)

def test_random_returns_challenge():
    bank = ChallengeBank.load()
    c = bank.random()
    assert isinstance(c, Challenge)
    assert c.title != ""

def test_load_from_custom_data():
    data = [{"title": "T", "description": "D", "difficulty": "easy",
              "starter_comment": ""}]
    bank = ChallengeBank(data=[Challenge.from_dict(d) for d in data])
    assert len(bank.all()) == 1

def test_random_on_empty_raises():
    bank = ChallengeBank(data=[])
    with pytest.raises(ValueError):
        bank.random()
