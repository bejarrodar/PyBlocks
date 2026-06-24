from pathlib import Path
import json
import pytest
from pyblocks.project.io import ProjectIO


def test_create_project(tmp_path):
    project = ProjectIO.create(name="test_game", root=tmp_path / "test_game")
    assert (tmp_path / "test_game").is_dir()
    assert (tmp_path / "test_game" / "main.py").exists()
    assert (tmp_path / "test_game" / ".pyblocks").is_dir()
    assert (tmp_path / "test_game" / ".pyblocks" / "project.json").exists()
    assert (tmp_path / "test_game" / ".pyblocks" / "canvas.json").exists()
    assert (tmp_path / "test_game" / ".pyblocks" / "layout.json").exists()


def test_create_writes_project_json(tmp_path):
    project = ProjectIO.create(name="test_game", root=tmp_path / "test_game")
    data = json.loads((tmp_path / "test_game" / ".pyblocks" / "project.json").read_text())
    assert data["name"] == "test_game"
    assert data["active_file"] == "main.py"
    assert data["expansions"] == []
    assert data["enabled_packages"] == []


def test_load_project(tmp_path):
    ProjectIO.create(name="test_game", root=tmp_path / "test_game")
    loaded = ProjectIO.load(tmp_path / "test_game")
    assert loaded.name == "test_game"
    assert loaded.root == tmp_path / "test_game"


def test_save_and_reload(tmp_path):
    project = ProjectIO.create(name="test_game", root=tmp_path / "test_game")
    project.active_file = "player.py"
    project.expansions = ["auth_pack"]
    ProjectIO.save(project)
    reloaded = ProjectIO.load(tmp_path / "test_game")
    assert reloaded.active_file == "player.py"
    assert reloaded.expansions == ["auth_pack"]


def test_load_invalid_dir(tmp_path):
    with pytest.raises(FileNotFoundError):
        ProjectIO.load(tmp_path / "no_such_project")


def test_load_empty_dir(tmp_path):
    empty = tmp_path / "empty_project"
    empty.mkdir()
    with pytest.raises(FileNotFoundError):
        ProjectIO.load(empty)


def test_load_includes_enabled_packages(tmp_path):
    root = tmp_path / "test_game"
    root.mkdir()
    pyblocks_dir = root / ".pyblocks"
    pyblocks_dir.mkdir()
    data = {"name": "test_game", "active_file": "main.py", "expansions": [], "enabled_packages": ["pygame", "requests"]}
    (pyblocks_dir / "project.json").write_text(json.dumps(data))
    project = ProjectIO.load(root)
    assert project.enabled_packages == ["pygame", "requests"]


def test_load_defaults_enabled_packages_to_empty(tmp_path):
    root = tmp_path / "test_game"
    root.mkdir()
    pyblocks_dir = root / ".pyblocks"
    pyblocks_dir.mkdir()
    data = {"name": "test_game", "active_file": "main.py", "expansions": []}
    (pyblocks_dir / "project.json").write_text(json.dumps(data))
    project = ProjectIO.load(root)
    assert project.enabled_packages == []


def test_save_writes_enabled_packages(tmp_path):
    from pyblocks.project.model import Project
    root = tmp_path / "test_game"
    root.mkdir()
    pyblocks_dir = root / ".pyblocks"
    pyblocks_dir.mkdir()
    project = Project(name="test_game", root=root, enabled_packages=["pygame"])
    ProjectIO.save(project)
    saved = json.loads((pyblocks_dir / "project.json").read_text())
    assert saved["enabled_packages"] == ["pygame"]
