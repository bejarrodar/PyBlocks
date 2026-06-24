from __future__ import annotations
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import tkinter as tk

from pyblocks.panels.base import Panel
from pyblocks.project.model import Project


class PanelManager:

    def __init__(self, root: tk.Tk, project: Project):
        self._root = root
        self._project = project
        self.panels: dict[str, Panel] = {}

    def register(self, panel: Panel) -> None:
        if panel.panel_id in self.panels:
            raise ValueError(f"Panel already registered: {panel.panel_id}")
        self.panels[panel.panel_id] = panel

    def toggle(self, panel_id: str) -> None:
        panel = self.panels[panel_id]
        if panel.is_hidden:
            panel.show()
        else:
            panel.hide()

    def save_layout(self) -> None:
        data = {
            "panels": {
                pid: p.layout_state()
                for pid, p in self.panels.items()
            }
        }
        layout_file = self._project.pyblocks_dir / "layout.json"
        layout_file.write_text(json.dumps(data, indent=2))

    def restore_layout(self) -> None:
        layout_file = self._project.pyblocks_dir / "layout.json"
        if not layout_file.exists():
            return
        data = json.loads(layout_file.read_text())
        panel_states = data.get("panels", {})
        for panel_id, state in panel_states.items():
            if panel_id not in self.panels:
                continue
            panel = self.panels[panel_id]
            if state.get("hidden"):
                panel.hide()
            # floating restore deferred — requires knowing the dock container at restore time
