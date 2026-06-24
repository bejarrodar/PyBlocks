from __future__ import annotations
import tkinter as tk
from tkinter import ttk, font as tkfont
from pyblocks.panels.base import Panel


class ConsolePanel(Panel):

    def __init__(self, root: tk.Tk, on_error_block=None, **kwargs):
        super().__init__(root, title="⑤ Console", panel_id="console", **kwargs)
        self._on_error_block = on_error_block
        self._on_input = None
        self._running = False
        self._stderr_buf: list[str] = []
        self._build_console()

    def _build_console(self) -> None:
        frame = self.content

        # Input bar must be packed BEFORE the notebook so pack gives it space first
        input_frame = ttk.Frame(frame)
        input_frame.pack(side="bottom", fill="x")
        self._input_entry = ttk.Entry(input_frame, state="disabled")
        self._input_entry.pack(side="left", fill="x", expand=True, padx=2, pady=2)
        self._send_btn = ttk.Button(input_frame, text="Send",
                                    command=self._send_input, state="disabled")
        self._send_btn.pack(side="right", padx=2, pady=2)
        self._input_entry.bind("<Return>", lambda _: self._send_input())

        # Notebook fills remaining space above the input bar
        self._notebook = ttk.Notebook(frame)
        self._notebook.pack(fill="both", expand=True)

        mono = tkfont.Font(family="Consolas", size=9)
        self._tabs: dict[str, tk.Text] = {}
        for tab_id, label in [("all", "All"), ("subprocess", "Subprocess"),
                                ("errors", "Errors")]:
            f = ttk.Frame(self._notebook)
            self._notebook.add(f, text=label)
            text = tk.Text(f, wrap="word", state="disabled", font=mono,
                           bg="#1e1e2e", fg="#cdd6f4", relief="flat")
            scroll = ttk.Scrollbar(f, command=text.yview)
            text.configure(yscrollcommand=scroll.set)
            text.pack(side="left", fill="both", expand=True)
            scroll.pack(side="right", fill="y")
            text.tag_configure("error", foreground="#f38ba8")
            self._tabs[tab_id] = text

    def _append(self, tab_id: str, text: str, tag: str = "") -> None:
        widget = self._tabs[tab_id]
        widget.configure(state="normal")
        if tag:
            widget.insert("end", text + "\n", tag)
        else:
            widget.insert("end", text + "\n")
        widget.see("end")
        widget.configure(state="disabled")

    def append_stdout(self, text: str) -> None:
        for tab_id in ("all", "subprocess"):
            widget = self._tabs[tab_id]
            widget.configure(state="normal")
            widget.insert("end", text)
            widget.see("end")
            widget.configure(state="disabled")

    def append_stderr(self, line: str) -> None:
        self._stderr_buf.append(line)
        for tab_id in ("all", "errors"):
            widget = self._tabs[tab_id]
            widget.configure(state="normal")
            widget.insert("end", line + "\n", "error")
            widget.see("end")
            widget.configure(state="disabled")

    def clear(self) -> None:
        self._stderr_buf.clear()
        for widget in self._tabs.values():
            widget.configure(state="normal")
            widget.delete("1.0", "end")
            widget.configure(state="disabled")

    def set_input_callback(self, cb) -> None:
        self._on_input = cb

    def _send_input(self) -> None:
        text = self._input_entry.get()
        if not text or not self._on_input:
            return
        self._on_input(text)
        self._append("all", f"> {text}")
        self._input_entry.delete(0, "end")

    def set_running(self, running: bool) -> None:
        self._running = running
        state = "normal" if running else "disabled"
        self._input_entry.configure(state=state)
        self._send_btn.configure(state=state)

    def get_stderr(self) -> str:
        return "\n".join(self._stderr_buf)

    def _get_tab_content(self, tab_id: str) -> str:
        return self._tabs[tab_id].get("1.0", "end")
