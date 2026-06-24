import json
import pytest
tk = pytest.importorskip("tkinter")
ttk = pytest.importorskip("tkinter.ttk")
from pyblocks.panels.base import Panel
from pyblocks.panels.manager import PanelManager
from pyblocks.project.model import Project


def make_project(tmp_path):
    from pyblocks.project.io import ProjectIO
    return ProjectIO.create("game", tmp_path / "game")


def test_register_panel(tk_root, tmp_path):
    project = make_project(tmp_path)
    pm = PanelManager(tk_root, project)
    panel = Panel(tk_root, title="Files", panel_id="files")
    pm.register(panel)
    assert "files" in pm.panels


def test_save_layout(tk_root, tmp_path):
    project = make_project(tmp_path)
    pm = PanelManager(tk_root, project)
    panel = Panel(tk_root, title="Files", panel_id="files")
    pm.register(panel)
    pm.save_layout()
    layout_file = project.pyblocks_dir / "layout.json"
    data = json.loads(layout_file.read_text())
    assert "panels" in data
    assert "files" in data["panels"]


def test_restore_layout_hidden(tk_root, tmp_path):
    project = make_project(tmp_path)
    layout_file = project.pyblocks_dir / "layout.json"
    layout_file.write_text(json.dumps({
        "panels": {"files": {"floating": False, "hidden": True}}
    }))
    pm = PanelManager(tk_root, project)
    panel = Panel(tk_root, title="Files", panel_id="files")
    pm.register(panel)
    pm.restore_layout()
    assert panel.is_hidden is True


def test_toggle_panel_visibility(tk_root, tmp_path):
    project = make_project(tmp_path)
    pm = PanelManager(tk_root, project)
    panel = Panel(tk_root, title="Files", panel_id="files")
    pm.register(panel)
    pm.toggle("files")
    assert panel.is_hidden is True
    pm.toggle("files")
    assert panel.is_hidden is False
