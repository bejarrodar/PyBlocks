from __future__ import annotations
import re
import tkinter as tk
from tkinter import ttk, font as tkfont
from pyblocks.panels.base import Panel
from pyblocks import theme

_ID_MARKER = "# __pyblocks_id__:"
_HL_TAG = "hl_block"
_SCOPE_TAG = "scope_var"
_LINE_TAG_PREFIX = "line_"

# ── syntax highlighting ────────────────────────────────────────────────────────

_KEYWORDS = frozenset({
    "False", "None", "True", "and", "as", "assert", "async", "await",
    "break", "class", "continue", "def", "del", "elif", "else", "except",
    "finally", "for", "from", "global", "if", "import", "in", "is",
    "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try",
    "while", "with", "yield",
})

_BUILTINS = frozenset({
    "abs", "all", "any", "bin", "bool", "bytes", "callable", "chr",
    "dict", "dir", "divmod", "enumerate", "eval", "exec", "filter",
    "float", "format", "frozenset", "getattr", "globals", "hasattr",
    "hash", "help", "hex", "id", "input", "int", "isinstance", "issubclass",
    "iter", "len", "list", "locals", "map", "max", "min", "next", "object",
    "oct", "open", "ord", "pow", "print", "range", "repr", "reversed",
    "round", "set", "setattr", "slice", "sorted", "staticmethod", "str",
    "sum", "super", "tuple", "type", "vars", "zip",
})

_SYN_RE = re.compile(
    r'(?P<string>"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')'
    r'|(?P<comment>#[^\n]*)'
    r'|(?P<number>\b\d+\.?\d*\b)'
    r'|(?P<word>\b[A-Za-z_]\w*\b)',
)

# Catppuccin Mocha syntax colors
_SYN_COLORS = {
    "syn_keyword":  "#cba6f7",  # mauve
    "syn_string":   "#a6e3a1",  # green
    "syn_comment":  "#6c7086",  # overlay0
    "syn_number":   "#fab387",  # peach
    "syn_builtin":  "#89dceb",  # sky
    "syn_defname":  "#89b4fa",  # blue
}

# Camel-case check: at least one lowercase letter, then uppercase, then more letters
_CAMEL_RE = re.compile(r'\b([a-z]+[A-Z][A-Za-z0-9]*)\s*(?:=|:)')


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
            font=mono, bg=theme.BG, fg=theme.TEXT,
            insertbackground=theme.TEXT,
            selectbackground=theme.SURFACE2,
            relief="flat",
        )

        # Syntax tags — created before _HL_TAG/_SCOPE_TAG so those remain on top
        for tag, color in _SYN_COLORS.items():
            self._text.tag_configure(tag, foreground=color)

        self._text.tag_configure(_HL_TAG, background=theme.SURFACE, foreground="#f5c2e7")
        self._text.tag_configure(_SCOPE_TAG, foreground="#a6e3a1", underline=True)

        h_scroll = ttk.Scrollbar(frame, orient="horizontal", command=self._text.xview)
        v_scroll = ttk.Scrollbar(frame, orient="vertical", command=self._text.yview)
        self._text.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        self._text.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        # PEP 8 hint bar
        self._pep8_label = tk.Label(
            frame, text="", anchor="w", padx=6, pady=2,
            bg=theme.SURFACE, fg=theme.SUBTEXT,
            font=("Segoe UI", 8),
        )
        self._pep8_label.grid(row=2, column=0, columnspan=2, sticky="ew")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self._text.bind("<Button-1>", self._on_click)

    def set_code(self, code: str, id_map: dict[str, int]) -> None:
        self._id_map = id_map
        self._line_to_id = {v: k for k, v in id_map.items()}
        self._highlighted_id = None

        self._text.configure(state="normal")
        self._text.delete("1.0", "end")

        display_lines = []
        for line in code.splitlines():
            idx = line.find("  # __pyblocks_id__:")
            display_lines.append(line[:idx] if idx != -1 else line)
        display_text = "\n".join(display_lines)

        self._text.insert("1.0", display_text)
        self._text.configure(state="disabled")

        self._apply_syntax(display_text)
        self._check_pep8(display_text)

    # ── syntax highlighting ────────────────────────────────────────────────────

    def _apply_syntax(self, text: str) -> None:
        for tag in _SYN_COLORS:
            self._text.tag_remove(tag, "1.0", "end")

        prev_word: str | None = None
        for m in _SYN_RE.finditer(text):
            s = f"1.0+{m.start()}c"
            e = f"1.0+{m.end()}c"

            if m.group("string"):
                self._text.tag_add("syn_string", s, e)
                prev_word = None
            elif m.group("comment"):
                self._text.tag_add("syn_comment", s, e)
                prev_word = None
            elif m.group("number"):
                self._text.tag_add("syn_number", s, e)
                prev_word = None
            else:
                word = m.group("word")
                if prev_word in ("def", "class"):
                    self._text.tag_add("syn_defname", s, e)
                elif word in _KEYWORDS:
                    self._text.tag_add("syn_keyword", s, e)
                elif word in _BUILTINS:
                    self._text.tag_add("syn_builtin", s, e)
                prev_word = word

        # Keep block highlight and scope underline on top
        self._text.tag_raise(_HL_TAG)
        self._text.tag_raise(_SCOPE_TAG)

    # ── PEP 8 hints ───────────────────────────────────────────────────────────

    def _check_pep8(self, text: str) -> None:
        hint = ""
        for i, raw_line in enumerate(text.splitlines(), 1):
            line = raw_line.rstrip()
            if not line or line.lstrip().startswith("#"):
                continue

            if len(line) > 79:
                hint = f"✦  Line {i} is long ({len(line)} chars) — PEP 8 suggests ≤ 79"
                break

            m = _CAMEL_RE.search(line)
            if m and m.group(1) not in _KEYWORDS:
                name = m.group(1)
                snake = re.sub(r'([A-Z])', lambda x: f'_{x.group(1).lower()}', name)
                hint = f"✦  Line {i}: consider snake_case — `{name}` → `{snake}`"
                break

            if ";" in line:
                hint = f"✦  Line {i}: avoid `;` — use a separate line instead"
                break

        if hint:
            self._pep8_label.configure(text=hint, fg="#f9e2af")  # Catppuccin yellow
        else:
            self._pep8_label.configure(text="", fg=theme.SUBTEXT)

    # ── public API ─────────────────────────────────────────────────────────────

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
