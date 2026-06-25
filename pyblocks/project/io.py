from __future__ import annotations
import json
from pathlib import Path
from pyblocks.project.model import Project
from pyblocks.canvas.model import CanvasModel
from pyblocks.canvas.serializer import CanvasSerializer
from pyblocks.logger import get_logger

log = get_logger("project.io")

_CANVAS_DEFAULT = {"blocks": [], "scroll": [0, 0]}
_LAYOUT_DEFAULT = {"panels": {}}


class ProjectIO:

    @staticmethod
    def create(name: str, root: Path) -> Project:
        log.info("Creating project '%s' at %s", name, root)
        root.mkdir(parents=True, exist_ok=True)
        (root / "main.py").touch()
        pyblocks_dir = root / ".pyblocks"
        pyblocks_dir.mkdir(exist_ok=True)
        (root / ".pyblocks_cache").mkdir(exist_ok=True)
        project = Project(name=name, root=root)
        ProjectIO.save(project)
        (pyblocks_dir / "canvas.json").write_text(json.dumps(_CANVAS_DEFAULT, indent=2))
        (pyblocks_dir / "layout.json").write_text(json.dumps(_LAYOUT_DEFAULT, indent=2))
        log.debug("Project files written to %s", pyblocks_dir)
        return project

    @staticmethod
    def save(project: Project) -> None:
        log.debug("Saving project '%s'", project.name)
        data = {
            "name": project.name,
            "active_file": str(project.active_file),
            "expansions": project.expansions,
            "enabled_packages": project.enabled_packages,
        }
        project.pyblocks_dir.mkdir(parents=True, exist_ok=True)
        (project.pyblocks_dir / "project.json").write_text(json.dumps(data, indent=2))

    @staticmethod
    def load(root: Path) -> Project:
        project_file = root / ".pyblocks" / "project.json"
        if not project_file.exists():
            log.error("project.json not found at %s", root)
            raise FileNotFoundError(f"No PyBlocks project found at {root}")
        data = json.loads(project_file.read_text())
        log.info("Loaded project '%s' from %s", data.get("name"), root)
        return Project(
            name=data["name"],
            root=root,
            active_file=data.get("active_file", "main.py"),
            expansions=data.get("expansions", []),
            enabled_packages=data.get("enabled_packages", []),
        )

    @staticmethod
    def load_canvas(project: Project) -> CanvasModel:
        path = project.pyblocks_dir / "canvas.json"
        try:
            return CanvasSerializer.load(path)
        except FileNotFoundError:
            log.warning("canvas.json not found for '%s'; starting empty", project.name)
            return CanvasModel()

    @staticmethod
    def save_canvas(project: Project, canvas: CanvasModel) -> None:
        project.pyblocks_dir.mkdir(parents=True, exist_ok=True)
        CanvasSerializer.save(canvas, project.pyblocks_dir / "canvas.json")
        log.debug("Canvas saved for '%s'", project.name)


    @staticmethod
    def load_expansions(project: "Project") -> dict[str, bool]:
        path = project.root / "project.json"
        if not path.exists():
            return {}
        try:
            data = json.loads(path.read_text())
            return data.get("enabled_expansions", {})
        except (json.JSONDecodeError, OSError):
            return {}

    @staticmethod
    def save_expansions(project: "Project", state: dict[str, bool]) -> None:
        path = project.root / "project.json"
        try:
            data = json.loads(path.read_text()) if path.exists() else {}
        except (json.JSONDecodeError, OSError):
            data = {}
        data["enabled_expansions"] = state
        path.write_text(json.dumps(data, indent=2))

