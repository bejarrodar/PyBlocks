from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from pyblocks.blocks.variables import make_user_variable_chip, make_user_function_chip
from pyblocks.blocks.definition import _REGISTRY, get_registry, BlockDefinition
from pyblocks.panels.base import Panel

_USER_VAR_CAT = "User Variables"
_USER_FN_CAT = "User Functions"

class PalettePanel(Panel):

    def __init__(self, root: tk.Tk, on_palette_drag=None, **kwargs):
        super().__init__(root, title="② Palette", panel_id="palette", **kwargs)
        self._on_palette_drag = on_palette_drag
        self._category_blocks: dict[str, list[BlockDefinition]] = {}
        self._search_var = tk.StringVar()
        self._build_palette()

    def _build_palette(self) -> None:
        frame = self.content
        # Search bar
        search_frame = ttk.Frame(frame)
        search_frame.pack(fill="x", padx=4, pady=2)
        ttk.Label(search_frame, text="🔍").pack(side="left")
        ttk.Entry(search_frame, textvariable=self._search_var).pack(
            side="left", fill="x", expand=True)
        self._search_var.trace_add("write", lambda *_: self._apply_search())

        # Treeview
        self._tree = ttk.Treeview(frame, selectmode="browse", show="tree")
        scroll = ttk.Scrollbar(frame, orient="vertical",
                                  command=self._tree.yview)
        self._tree.configure(yscrollcommand=scroll.set)
        self._tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Style updates: larger rows and better font
        style = ttk.Style()
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 10))

        self._tree.bind("<ButtonPress-1>", self._on_tree_press)
        self._tree.bind("<B1-Motion>", self._on_tree_drag)

        self._populate()

    def _populate(self) -> None:
        self._category_blocks.clear()
        reg = get_registry()
        for defn in reg.values():
            self._category_blocks.setdefault(defn.category, []).append(defn)

        self._tree.delete(*self._tree.get_children())
        for cat in sorted(self._category_blocks):
            cat_id = self._tree.insert("", "end", text=cat,
                                         open=(cat != "Advanced"),
                                         tags=("category",))
            for defn in sorted(self._category_blocks[cat], key=lambda d: d.label):
                self._tree.insert(cat_id, "end", text=defn.label,
                                    iid=defn.name, tags=("block",))

    def get_categories(self) -> list[str]:
        return list(self._category_blocks.keys())

    def _apply_search(self) -> None:
        query = self._search_var.get().lower().strip()
        for cat_id in self._tree.get_children():
            cat_visible = False
            for item_id in self._tree.get_children(cat_id):
                text = self._tree.item(item_id, "text").lower()
                match = not query or query in text or query in item_id.lower()
                self._tree.item(item_id, tags=("block",) if match else ("hidden",))
                if match:
                    cat_visible = True
            if cat_visible:
                self._tree.item(cat_id, open=True)

    def _visible_block_names(self) -> list[str]:
        result = []
        for cat_id in self._tree.get_children():
            for item_id in self._tree.get_children(cat_id):
                if "hidden" not in self._tree.item(item_id, "tags"):
                    result.append(item_id)
        return result

    def _on_tree_press(self, event: tk.Event) -> None:
        item = self._tree.identify_row(event.y)
        if item and "block" in self._tree.item(item, "tags"):
            self._drag_item = item
        else:
            self._drag_item = None

    def _on_tree_drag(self, event: tk.Event) -> None:
        if getattr(self, "_drag_item", None):
            self._simulate_drag(self._drag_item)
            self._drag_item = None

    def _simulate_drag(self, block_name: str) -> None:
        defn = None
        for blocks in self._category_blocks.values():
            for b in blocks:
                if b.name == block_name:
                    defn = b
                    break
            if defn:
                break
        if defn is None:
            defn = _REGISTRY.get(block_name)
        if defn and self._on_palette_drag:
            self._on_palette_drag(defn)
            self._drag_item = None

    def sync_user_variables(self, var_names: set[str]) -> None:
        current_keys = {iid for iid in self._tree.get_children()
                         for iid in self._tree.get_children(iid)
                         if iid.startswith("user_var_")}
        wanted_keys = {f"user_var_{n}" for n in var_names}

        # Remove stale
        for key in current_keys - wanted_keys:
            self._tree.delete(key)
            _REGISTRY.pop(key, None)

        # Add new
        for var_name in var_names:
            key = f"user_var_{var_name}"
            if key not in current_keys:
                defn = make_user_variable_chip(var_name)
                _REGISTRY[key] = defn
                cat_id = self._get_or_create_category(_USER_VAR_CAT)
                self._tree.insert(cat_id, "end", text=var_name, iid=key,
                                   tags=("block",))

    def sync_user_functions(self, fn_names: set[str]) -> None:
        current_keys = {
            iid
            for cat_id in self._tree.get_children()
            for iid in self._tree.get_children(cat_id)
            if iid.startswith("user_fn_")
        }
        wanted_keys = {f"user_fn_{n}" for n in fn_names}

        # Remove stale
        for key in current_keys - wanted_keys:
            self._tree.delete(key)
            _REGISTRY.pop(key, None)

        # Add new
        for fn_name in fn_names:
            key = f"user_fn_{fn_name}"
            if key not in current_keys:
                defn = make_user_function_chip(fn_name)
                _REGISTRY[key] = defn
                cat_id = self._get_or_create_category(_USER_FN_CAT)
                self._tree.insert(cat_id, "end", text=f"{fn_name}()",
                                   iid=key, tags=("block",))

    def _get_or_create_category(self, cat_name: str) -> str:
        for cat_id in self._tree.get_children():
            if self._tree.item(cat_id, "text") == cat_name:
                return cat_id
        return self._tree.insert("", "0", text=cat_name, open=True,
                                 tags=("category",))
