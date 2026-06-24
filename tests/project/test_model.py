from pathlib import Path
from pyblocks.project.model import Project


def test_project_defaults(tmp_path):
    p = Project(name="my_game", root=tmp_path / "my_game")
    assert p.active_file == "main.py"
    assert p.expansions == []


def test_project_pyblocks_dir(tmp_path):
    p = Project(name="my_game", root=tmp_path / "my_game")
    assert p.pyblocks_dir == tmp_path / "my_game" / ".pyblocks"


def test_project_cache_dir(tmp_path):
    p = Project(name="my_game", root=tmp_path / "my_game")
    assert p.cache_dir == tmp_path / "my_game" / ".pyblocks_cache"


def test_project_expansions_are_independent(tmp_path):
    p1 = Project(name="game1", root=tmp_path / "game1")
    p2 = Project(name="game2", root=tmp_path / "game2")
    p1.expansions.append("auth_pack")
    assert p2.expansions == [], "expansions list must not be shared between instances"
