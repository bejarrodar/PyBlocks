from __future__ import annotations
import tkinter as tk
from tkinter import ttk, font as tkfont
from pyblocks.panels.base import Panel

_ID_MARKER = "# __pyblocks_id__:"
_HL_TAG = "hl_block"
_SCOPE_TAG = "scope_var"
_LINE_TAG_PREFIX = "line_"


class LivePythonPanel(Panel):

    def __init__(self, root: tk.Tk, on_line_click=None, **kwargs):
        super().__init__(root, title="④ Live Python", panel_id="live_python", **kwargs)
        self._on_line_click = on_line_click
        self._id_map: dict[str, int] = {}
        self._line_to_id: dict[int, str] = {}
        self._highlighted_id: str | None = None
        self._build_text()

    def _build_text(self):
        frame = self.content
        mono = tkfont.Font(family="Consolas", size=10)
        self._text = tk.Text(
            frame, wrap="none", state="disabled",
            font=mono, bg="#1e1e2e", fg="#cdd6f4",
            insertbackground="#cdd6f4",
            selectbackground="#45475a",
            relief="flat",
        )
        self._text.tag_configure(_HL_TAG, background="#313244", foreground="#f5c2e7")
        self._text.tag_configure(_SCOPE_TAG, foreground="#a6e3a1", underline=True)
        h_scroll = ttk.Scrollbar(frame, orient="horizontal",
                                  command=self._text.xview)
        v_scroll = ttk.Scrollbar(frame, orient="vertical",
                                  command=self._text.yview)
        self._text.configure(xscrollcommand=h_scroll.set,
                              yscrollcommand=v_scroll.set)
        self._text.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self._text.bind("<Button-1>", self._on_click)

    def set_code(self, code: str, id_map: dict[str, int]) -> None:
        self._id_map = id_map
        self._line_to_id = {v: k for k, v in id_map.items()}
        self._highlighted_id = None
        self._text.configure(state="normal")
        self._text.delete("1.0", "end")
        # Strip __pyblocks_id__ comments for display
        display_lines = []
        for line in code.splitlines():
            idx = line.find("  # __pyblocks_id__:")
            display_lines.append(line[:idx] if idx != -1 else line)
        self._text.insert("1.0", "\n".join(display_lines))
        self._text.configure(state="disabled")

    def clear_highlight(self) -> None:
        self._highlighted_id = None
        self._text.tag_remove(_HL_TAG, "1.0", "end")

    def highlight_block(self, block_id: str) -> None:
        self._highlighted_id = block_id
        self._text.tag_remove(_HL_TAG, "1.0", "end")
        line_idx = self._id_map.get(block_id)
        if line_idx is not None:
            line_no = line_idx + 1
            self._text.tag_add(_HL_TAG, f"{line_no}.0", f"{line_no}.end")
            self._text.see(f"{line_no}.0")

    def highlight_scope(self, var_names: set[str]) -> None:
        """Underline all occurrences of in-scope variable names in the code."""
        self._text.tag_remove(_SCOPE_TAG, "1.0", "end")
        for name in var_names:
            start = "1.0"
            while True:
                pos = self._text.search(name, start, stopindex="end",
                                        nocase=False, regexp=False)
                if not pos:
                    break
                end = f"{pos}+{len(name)}c"
                self._text.tag_add(_SCOPE_TAG, pos, end)
                start = end

    def clear_scope(self) -> None:
        self._text.tag_remove(_SCOPE_TAG, "1.0", "end")

    def _on_click(self, event: tk.Event) -> None:
        index = self._text.index(f"@{event.x},{event.y}")
        line_no = int(index.split(".")[0])
        self._handle_line_click(line_no - 1)

    def _handle_line_click(self, line_index: int) -> None:
        block_id = self._line_to_id.get(line_index)
        if block_id and self._on_line_click:
            self._on_line_click(block_id)
