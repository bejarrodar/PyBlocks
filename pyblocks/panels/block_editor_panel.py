from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from typing import Callable
from pyblocks.panels.base import Panel
from pyblocks.blocks.editor.model import CustomBlockDef

_COLORS = ["#fab387", "#a6e3a1", "#89b4fa", "#cba6f7",
           "#f38ba8", "#89dceb", "#f9e2af", "#94e2d5"]

class BlockEditorPanel(Panel):
    panel_id = "block_editor"
    panel_title = "Block Editor"

    def __init__(self, parent, on_save: Callable[[CustomBlockDef], None] | None,
                 **kwargs) -> None:
        super().__init__(parent, title=self.panel_title, panel_id=self.panel_id, **kwargs)
        self._on_save = on_save
        self._input_vars: list[tk.StringVar] = []
        self._input_frame: ttk.Frame | None = None
        self._name_var = tk.StringVar()
        self._label_var = tk.StringVar()
        self._category_var = tk.StringVar(value="Custom")
        self._color_var = tk.StringVar(value=_COLORS[0])
        self._desc_var = tk.StringVar()
        self._template_text: tk.Text | None = None
        self._build()

    def _build(self) -> None:
        c = self.content
        for row, (lbl, var) in enumerate([
            ("Name:", self._name_var),
            ("Label:", self._label_var),
            ("Category:", self._category_var),
            ("Description:", self._desc_var),
        ]):
            ttk.Label(c, text=lbl).grid(row=row, column=0, sticky="w",
                                          padx=8, pady=4)
            ttk.Entry(c, textvariable=var, width=30).grid(
                row=row, column=1, sticky="ew", padx=8)

        # Color picker row
        ttk.Label(c, text="Color:").grid(row=4, column=0, sticky="w", padx=8)
        color_frame = ttk.Frame(c)
        color_frame.grid(row=4, column=1, sticky="w", padx=8)
        for col in _COLORS:
            btn = tk.Button(color_frame, bg=col, width=2,
                            command=lambda x=col: self._color_var.set(x))
            btn.pack(side="left", padx=2)

        # Inputs
        ttk.Label(c, text="Inputs:").grid(row=5, column=0, sticky="nw",
                                            padx=8, pady=4)
        self._input_frame = ttk.Frame(c)
        self._input_frame.grid(row=5, column=1, sticky="ew", padx=8)
        ttk.Button(c, text="+ Add Input",
                    command=self._add_input).grid(row=6, column=1,
                                                   sticky="w", padx=8)

        # Template
        ttk.Label(c, text="Template:").grid(row=7, column=0, sticky="nw",
                                               padx=8, pady=4)
        self._template_text = tk.Text(c, height=5, width=40, wrap="none")
        self._template_text.grid(row=7, column=1, padx=8, pady=4)

        ttk.Button(c, text="Save Block",
                    command=self.save).grid(row=8, column=1, sticky="e",
                                             padx=8, pady=8)
        c.columnconfigure(1, weight=1)

    def _add_input(self) -> None:
        var = tk.StringVar()
        self._input_vars.append(var)
        row = len(self._input_vars) - 1
        ttk.Entry(self._input_frame, textvariable=var, width=20).grid(
            row=row, column=0, sticky="w", pady=2)
        ttk.Button(self._input_frame, text="x",
                    command=lambda r=row, v=var: self._remove_input(v)).grid(
            row=row, column=1, padx=4)

    def _remove_input(self, var: tk.StringVar) -> None:
        if var in self._input_vars:
            self._input_vars.remove(var)

    def get_name(self) -> str:
        return self._name_var.get().strip()

    def get_label(self) -> str:
        return self._label_var.get().strip()

    def get_inputs(self) -> list[str]:
        return [v.get().strip() for v in self._input_vars if v.get().strip()]

    def get_template(self) -> str:
        return self._template_text.get("1.0", "end").strip() if self._template_text else ""

    def set_values(self, name: str, label: str, category: str, color: str,
                    inputs: list[str], template: str, description: str) -> None:
        self._name_var.set(name)
        self._label_var.set(label)
        self._category_var.set(category)
        self._color_var.set(color)
        self._desc_var.set(description)
        self._input_vars.clear()
        for inp in inputs:
            var = tk.StringVar(value=inp)
            self._input_vars.append(var)
        if self._template_text:
            self._template_text.delete("1.0", "end")
            self._template_text.insert("1.0", template)

    def save(self) -> None:
        defn = CustomBlockDef(
            name=self.get_name(),
            label=self.get_label(),
            category=self._category_var.get(),
            color=self._color_var.get(),
            inputs=self.get_inputs(),
            template=self.get_template(),
            description=self._desc_var.get(),
        )
        if not defn.is_valid():
            return
        if self._on_save:
            self._on_save(defn)
