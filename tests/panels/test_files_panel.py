import pytest
tk = pytest.importorskip("tkinter")
from pyblocks.panels.files_panel import FileExplorerPanel
from pyblocks.project.io import ProjectIO


def test_files_panel_loads_project_tree(tk_root, tmp_path):
    project = ProjectIO.create("game", tmp_path / "game")
    (tmp_path / "game" / "player.py").touch()
    panel = FileExplorerPanel(tk_root, project=project)
    items = panel.visible_files()
    assert "main.py" in items
    assert "player.py" in items


def test_files_panel_excludes_pyblocks_dir(tk_root, tmp_path):
    project = ProjectIO.create("game", tmp_path / "game")
    panel = FileExplorerPanel(tk_root, project=project)
    items = panel.visible_files()
    assert ".pyblocks" not in items
    assert ".pyblocks_cache" not in items


def test_files_panel_new_file(tk_root, tmp_path):
    project = ProjectIO.create("game", tmp_path / "game")
    panel = FileExplorerPanel(tk_root, project=project)
    panel.create_file("enemy.py")
    assert (tmp_path / "game" / "enemy.py").exists()
    assert "enemy.py" in panel.visible_files()


def test_files_panel_delete_file(tk_root, tmp_path):
    project = ProjectIO.create("game", tmp_path / "game")
    (tmp_path / "game" / "enemy.py").touch()
    panel = FileExplorerPanel(tk_root, project=project)
    panel.delete_file("enemy.py")
    assert not (tmp_path / "game" / "enemy.py").exists()
    assert "enemy.py" not in panel.visible_files()
