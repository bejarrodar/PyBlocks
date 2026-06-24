import json
import pytest
from pathlib import Path
from pyblocks.project.io import ProjectIO
from pyblocks.project.model import Project


@pytest.fixture
def project(tmp_path):
    root = tmp_path / "myproject"
    root.mkdir()
    return Project(root=root, name="myproject")


def test_save_and_load_expansions(project):
    state = {"demo_pack": True, "other_pack": False}
    ProjectIO.save_expansions(project, state)
    loaded = ProjectIO.load_expansions(project)
    assert loaded == state


def test_load_expansions_missing_key(project):
    # project.json exists but has no enabled_expansions key
    (project.root / "project.json").write_text(json.dumps({"name": "myproject"}))
    loaded = ProjectIO.load_expansions(project)
    assert loaded == {}


def test_load_expansions_no_project_json(project):
    loaded = ProjectIO.load_expansions(project)
    assert loaded == {}


def test_save_expansions_written_to_project_json(project):
    ProjectIO.save_expansions(project, {"pack_a": True})
    data = json.loads((project.root / "project.json").read_text())
    assert data["enabled_expansions"] == {"pack_a": True}


def test_save_expansions_preserves_existing_keys(project):
    (project.root / "project.json").write_text(
        json.dumps({"name": "myproject", "version": "1.0"}))
    ProjectIO.save_expansions(project, {"pack_a": True})
    data = json.loads((project.root / "project.json").read_text())
    assert data["name"] == "myproject"
    assert data["version"] == "1.0"
    assert data["enabled_expansions"] == {"pack_a": True}
