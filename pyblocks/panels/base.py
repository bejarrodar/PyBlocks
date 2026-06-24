from __future__ import annotations
import tkinter as tk
from tkinter import ttk


class Panel(tk.Frame):

    def __init__(self, root: tk.Tk, title: str, panel_id: str, **kwargs):
        super().__init__(root, **kwargs)
        self.panel_title = title
        self.panel_id = panel_id
        self._root = root
        self._is_floating = False
        self._is_hidden = False
        self._dock_container: tk.Misc = root
        self._build_header()
        self._content = ttk.Frame(self)
        self._content.pack(fill="both", expand=True)

    def _build_header(self):
        header = ttk.Frame(self, relief="raised")
        header.pack(fill="x")
        ttk.Label(header, text=self.panel_title).pack(side="left", padx=6)
        ttk.Button(header, text="⧉", width=2,
                   command=self._toggle_float).pack(side="right", padx=2)
        ttk.Button(header, text="✕", width=2,
                   command=self.hide).pack(side="right")

    def _toggle_float(self):
        if self._is_floating:
            self.dock(self._dock_container)
        else:
            self.float()

    def float(self):
        self.pack_forget()
        self.place_forget()
        self.tk.call('wm', 'manage', self._w)
        self.tk.call('wm', 'title', self._w, self.panel_title)
        cmd = self.register(self._on_float_close)
        self.tk.call('wm', 'protocol', self._w, 'WM_DELETE_WINDOW', cmd)
        self._is_floating = True

    def dock(self, container: tk.Misc):
        if self._is_floating:
            self.tk.call('wm', 'forget', self._w)
        self._dock_container = container
        self.pack_forget()
        self.pack(in_=container, fill="both", expand=True)
        self._is_floating = False
        self._is_hidden = False

    def hide(self):
        self.pack_forget()
        self._is_hidden = True

    def show(self):
        self.pack(in_=self._dock_container, fill="both", expand=True)
        self._is_hidden = False

    def _on_float_close(self):
        if self._is_floating:
            self.tk.call('wm', 'forget', self._w)
        self._is_floating = False
        self._is_hidden = True

    @property
    def is_floating(self) -> bool:
        return self._is_floating

    @property
    def is_hidden(self) -> bool:
        return self._is_hidden

    @property
    def content(self) -> ttk.Frame:
        return self._content

    def layout_state(self) -> dict:
        return {
            "floating": self._is_floating,
            "hidden": self._is_hidden,
        }
