from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from typing import Callable
from pyblocks.challenges.model import Challenge

_DIFFICULTY_COLORS = {
    "beginner": "#a6e3a1",
    "intermediate": "#f9e2af",
    "advanced": "#f38ba8",
}

class ChallengePopup(tk.Toplevel):

    def __init__(self, parent, challenge: Challenge,
                 on_accept: Callable[[Challenge], None] | None = None,
                 **kwargs) -> None:
        super().__init__(parent, **kwargs)
        self._challenge = challenge
        self._on_accept = on_accept
        self.title("PyBlocks Challenge")
        self.resizable(False, False)
        self._build()
        self.grab_set()
        self.focus_set()
        self.protocol("WM_DELETE_WINDOW", self.dismiss)

    def _build(self) -> None:
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        title_lbl = ttk.Label(frame, text=self._challenge.title,
                                font=("Segoe UI", 14, "bold"), wraplength=400)
        title_lbl.pack(anchor="w")
        self._title_lbl = title_lbl

        diff_color = _DIFFICULTY_COLORS.get(
            self._challenge.difficulty, "#cdd6f4")
        diff_lbl = tk.Label(frame, text=self._challenge.difficulty.capitalize(),
                             bg=diff_color, fg="#1e1e2e",
                             font=("Segoe UI", 9, "bold"),
                             padx=8, pady=2)
        diff_lbl.pack(anchor="w", pady=(4, 12))

        desc = tk.Text(frame, wrap="word", height=6, width=50,
                       relief="flat", state="disabled",
                       font=("Segoe UI", 10))
        desc.config(state="normal")
        desc.insert("1.0", self._challenge.description)
        desc.config(state="disabled")
        desc.pack(fill="both", expand=True, pady=(0, 16))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="Accept Challenge",
                   command=self.accept).pack(side="right", padx=(8, 0))
        ttk.Button(btn_frame, text="Maybe Later",
                   command=self.dismiss).pack(side="right")

    def get_title_text(self) -> str:
        return self._title_lbl.cget("text")

    def accept(self) -> None:
        if self._on_accept:
            self._on_accept(self._challenge)
        self.dismiss()

    def dismiss(self) -> None:
        self.grab_release()
        self.destroy()
