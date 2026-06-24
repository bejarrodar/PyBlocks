import pytest
tk = pytest.importorskip("tkinter")
from pyblocks.challenges.model import Challenge
from pyblocks.ui.challenge_popup import ChallengePopup

@pytest.fixture
def challenge():
    return Challenge(
        title="Hello, World!",
        description="Print 'Hello, World!' to the console.",
        difficulty="beginner",
        starter_comment="# Start here",
    )

def test_popup_creates_window(tk_root, challenge):
    popup = ChallengePopup(tk_root, challenge=challenge)
    assert popup.winfo_exists()
    popup.dismiss()

def test_popup_title_label(tk_root, challenge):
    popup = ChallengePopup(tk_root, challenge=challenge)
    assert popup.get_title_text() == "Hello, World!"
    popup.dismiss()

def test_accept_callback_fires(tk_root, challenge):
    accepted = []
    popup = ChallengePopup(tk_root, challenge=challenge,
                             on_accept=lambda c: accepted.append(c))
    popup.accept()
    assert len(accepted) == 1
    assert accepted[0].title == "Hello, World!"

def test_dismiss_closes_window(tk_root, challenge):
    popup = ChallengePopup(tk_root, challenge=challenge)
    popup.dismiss()
    assert not popup.winfo_exists()
