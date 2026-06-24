from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from pyblocks.panels.base import Panel
from pyblocks.project.model import Project

_HIDDEN = {".pyblocks", ".pyblocks_cache", "__pycache__", ".git"}


class FileExplorerPanel(Panel):
    def __init__(self, root: tk.Tk, project: Project, **kwargs):
        super().__init__(root, title="① Files", panel_id="files", **kwargs)
        self._project = project
        self._on_select_callback = None
        self._build_tree()
        self.refresh()

    def _build_tree(self):
        frame = self.content
        self._tree = ttk.Treeview(frame, show="tree", selectmode="browse")
        scrollbar = ttk.Scrollbar(frame, orient="vertical",
                                   command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        self._tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self._tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        # Context menu
        self._ctx_menu = tk.Menu(self._tree, tearoff=0)
        self._ctx_menu.add_command(label="New File...", command=self._prompt_new_file)
        self._ctx_menu.add_command(label="Delete", command=self._prompt_delete)
        self._tree.bind("<Button-3>", self._show_context_menu)

    def refresh(self):
        self._tree.delete(*self._tree.get_children())
        root_id = self._tree.insert("", "end", text=self._project.name, open=True)
        for path in sorted(self._project.root.iterdir()):
            if path.name in _HIDDEN:
                continue
            self._insert_path(root_id, path)

    def _insert_path(self, parent_id: str, path: Path):
        label = path.name + ("/" if path.is_dir() else "")
        node_id = self._tree.insert(parent_id, "end", text=label,
                                     values=[str(path)])
        if path.is_dir():
            for child in sorted(path.iterdir()):
                if child.name not in _HIDDEN:
                    self._insert_path(node_id, child)

    def visible_files(self) -> list[str]:
        result = []
        roots = self._tree.get_children()
        if not roots:
            return result
        for item in self._tree.get_children(roots[0]):
            text = self._tree.item(item, "text").rstrip("/")
            result.append(text)
        return result

    def create_file(self, name: str) -> Path:
        path = self._project.root / name
        path.touch()
        self.refresh()
        return path

    def delete_file(self, name: str) -> None:
        path = self._project.root / name
        if path.exists():
            path.unlink()
        self.refresh()

    def on_select(self, callback):
        self._on_select_callback = callback

    def _on_tree_select(self, _event):
        selection = self._tree.selection()
        if not selection:
            return
        values = self._tree.item(selection[0], "values")
        if values and self._on_select_callback:
            self._on_select_callback(Path(values[0]))

    def _show_context_menu(self, event):
        self._ctx_menu.post(event.x_root, event.y_root)

    def _prompt_new_file(self):
        from tkinter import simpledialog
        name = simpledialog.askstring("New File", "File name:", parent=self._root)
        if name:
            self.create_file(name)

    def _prompt_delete(self):
        from tkinter import messagebox
        sel = self._tree.selection()
        if not sel:
            return
        name = self._tree.item(sel[0], "text").rstrip("/")
        if messagebox.askyesno("Delete", f"Delete {name}?"):
            self.delete_file(name)
