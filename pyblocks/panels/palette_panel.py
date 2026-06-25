from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from pyblocks.blocks.variables import make_user_variable_chip, make_user_function_chip
from pyblocks.blocks.definition import _REGISTRY, get_registry, BlockDefinition
from pyblocks.panels.base import Panel
from pyblocks import theme

_USER_VAR_CAT = "User Variables"
_USER_FN_CAT = "User Functions"

class PalettePanel(Panel):

    def __init__(self, root: tk.Tk, on_palette_drag=None, **kwargs):
        super().__init__(root, title="② Palette", panel_id="palette", **kwargs)
        self._on_palette_drag = on_palette_drag
        self._category_blocks: dict[str, list[BlockDefinition]] = {}
        self._search_var = tk.StringVar()
        self._block_item_tags: dict[str, tuple] = {}
        self._build_palette()

    def _build_palette(self) -> None:
        frame = self.content

        # Search bar at top
        search_frame = ttk.Frame(frame)
        search_frame.pack(side="top", fill="x", padx=4, pady=2)
        ttk.Label(search_frame, text="🔍").pack(side="left")
        ttk.Entry(search_frame, textvariable=self._search_var).pack(
            side="left", fill="x", expand=True)
        self._search_var.trace_add("write", lambda *_: self._apply_search())

        # Description pane at bottom (packed before tree so it anchors to bottom)
        desc_outer = tk.Frame(frame, bg=theme.BG)
        desc_outer.pack(side="bottom", fill="x")

        tk.Frame(desc_outer, bg=theme.SURFACE2, height=1).pack(fill="x")

        self._desc_name = tk.Label(
            desc_outer, text="Select a block to see details",
            anchor="w", padx=8, pady=4,
            bg=theme.BG, fg=theme.SUBTEXT,
            font=("Segoe UI", 10, "bold"),
        )
        self._desc_name.pack(fill="x")

        self._desc_text = tk.Text(
            desc_outer, height=4, state="disabled", wrap="word",
            bg=theme.BG, fg=theme.SUBTEXT,
            font=("Segoe UI", 9), relief="flat", bd=0,
            padx=8, pady=2,
        )
        self._desc_text.pack(fill="x")

        # Treeview fills remaining space
        tree_frame = ttk.Frame(frame)
        tree_frame.pack(fill="both", expand=True)

        self._tree = ttk.Treeview(tree_frame, selectmode="browse", show="tree")
        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=scroll.set)
        self._tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self._tree.tag_configure("category",
            font=("Segoe UI", 10, "bold"), foreground=theme.ACCENT)

        self._tree.bind("<ButtonPress-1>", self._on_tree_press)
        self._tree.bind("<B1-Motion>", self._on_tree_drag)
        self._tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        self._populate()

    def _populate(self) -> None:
        self._category_blocks.clear()
        self._block_item_tags.clear()
        reg = get_registry()
        for defn in reg.values():
            self._category_blocks.setdefault(defn.category, []).append(defn)

        self._tree.delete(*self._tree.get_children())
        for cat in sorted(self._category_blocks):
            cat_id = self._tree.insert("", "end", text=cat,
                                         open=(cat != "Advanced"),
                                         tags=("category",))
            for defn in sorted(self._category_blocks[cat], key=lambda d: d.label):
                color_tag = f"clr_{defn.color.lstrip('#')}"
                self._tree.tag_configure(color_tag, foreground=defn.color)
                item_tags = (color_tag, "block")
                self._block_item_tags[defn.name] = item_tags
                self._tree.insert(cat_id, "end", text=defn.label,
                                    iid=defn.name, tags=item_tags)

    def get_categories(self) -> list[str]:
        return list(self._category_blocks.keys())

    def _apply_search(self) -> None:
        query = self._search_var.get().lower().strip()
        for cat_id in self._tree.get_children():
            cat_visible = False
            for item_id in self._tree.get_children(cat_id):
                text = self._tree.item(item_id, "text").lower()
                match = not query or query in text or query in item_id.lower()
                saved_tags = self._block_item_tags.get(item_id, ("block",))
                self._tree.item(item_id, tags=saved_tags if match else ("hidden",))
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

    def _on_tree_select(self, event: tk.Event) -> None:
        sel = self._tree.selection()
        if not sel:
            return
        item = sel[0]
        if "block" not in self._tree.item(item, "tags"):
            self._clear_desc()
            return

        defn = _REGISTRY.get(item)
        if defn is None:
            for blocks in self._category_blocks.values():
                for b in blocks:
                    if b.name == item:
                        defn = b
                        break
                if defn:
                    break
        if defn is None:
            self._clear_desc()
            return

        self._desc_name.configure(text=defn.label, fg=defn.color)

        lines: list[str] = []
        if defn.description:
            lines.append(defn.description)
        if defn.inputs:
            if lines:
                lines.append("")
            lines.append("Inputs:  " + ",  ".join(defn.inputs))

        self._desc_text.configure(state="normal")
        self._desc_text.delete("1.0", "end")
        self._desc_text.insert("end", "\n".join(lines))
        self._desc_text.configure(state="disabled")

    def _clear_desc(self) -> None:
        self._desc_name.configure(
            text="Select a block to see details", fg=theme.SUBTEXT)
        self._desc_text.configure(state="normal")
        self._desc_text.delete("1.0", "end")
        self._desc_text.configure(state="disabled")

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

        for key in current_keys - wanted_keys:
            self._tree.delete(key)
            _REGISTRY.pop(key, None)
            self._block_item_tags.pop(key, None)

        for var_name in var_names:
            key = f"user_var_{var_name}"
            if key not in current_keys:
                defn = make_user_variable_chip(var_name)
                _REGISTRY[key] = defn
                cat_id = self._get_or_create_category(_USER_VAR_CAT)
                color_tag = f"clr_{defn.color.lstrip('#')}"
                self._tree.tag_configure(color_tag, foreground=defn.color)
                item_tags = (color_tag, "block")
                self._block_item_tags[key] = item_tags
                self._tree.insert(cat_id, "end", text=var_name, iid=key,
                                   tags=item_tags)

    def sync_user_functions(self, fn_names: set[str]) -> None:
        current_keys = {
            iid
            for cat_id in self._tree.get_children()
            for iid in self._tree.get_children(cat_id)
            if iid.startswith("user_fn_")
        }
        wanted_keys = {f"user_fn_{n}" for n in fn_names}

        for key in current_keys - wanted_keys:
            self._tree.delete(key)
            _REGISTRY.pop(key, None)
            self._block_item_tags.pop(key, None)

        for fn_name in fn_names:
            key = f"user_fn_{fn_name}"
            if key not in current_keys:
                defn = make_user_function_chip(fn_name)
                _REGISTRY[key] = defn
                cat_id = self._get_or_create_category(_USER_FN_CAT)
                color_tag = f"clr_{defn.color.lstrip('#')}"
                self._tree.tag_configure(color_tag, foreground=defn.color)
                item_tags = (color_tag, "block")
                self._block_item_tags[key] = item_tags
                self._tree.insert(cat_id, "end", text=f"{fn_name}()",
                                   iid=key, tags=item_tags)

    def _get_or_create_category(self, cat_name: str) -> str:
        for cat_id in self._tree.get_children():
            if self._tree.item(cat_id, "text") == cat_name:
                return cat_id
        return self._tree.insert("", "0", text=cat_name, open=True,
                                 tags=("category",))
