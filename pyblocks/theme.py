from __future__ import annotations
import tkinter as tk
from tkinter import ttk

# Catppuccin Mocha
BG      = "#1e1e2e"
SURFACE = "#313244"
SURFACE2 = "#45475a"
OVERLAY = "#6c7086"
TEXT    = "#cdd6f4"
SUBTEXT = "#a6adc8"
ACCENT  = "#cba6f7"  # mauve


def apply(root: tk.Tk) -> None:
    style = ttk.Style(root)
    style.theme_use("clam")
    root.configure(bg=BG)

    style.configure(".",
        background=BG, foreground=TEXT,
        troughcolor=SURFACE, bordercolor=SURFACE2,
        focuscolor=SURFACE2,
        selectforeground=TEXT, selectbackground=SURFACE2,
    )

    style.configure("TFrame", background=BG)
    style.configure("TLabel", background=BG, foreground=TEXT)

    style.configure("TLabelframe", background=BG, bordercolor=SURFACE2)
    style.configure("TLabelframe.Label", background=BG, foreground=SUBTEXT)

    style.configure("TButton",
        background=SURFACE, foreground=TEXT,
        bordercolor=SURFACE2, lightcolor=SURFACE, darkcolor=SURFACE,
        padding=[6, 3],
    )
    style.map("TButton",
        background=[("active", SURFACE2), ("pressed", OVERLAY)],
        relief=[("pressed", "sunken")],
    )

    style.configure("TEntry",
        fieldbackground=SURFACE, foreground=TEXT,
        insertcolor=TEXT, bordercolor=SURFACE2,
        selectbackground=SURFACE2, selectforeground=TEXT,
    )

    style.configure("Treeview",
        background=BG, foreground=TEXT, fieldbackground=BG,
        borderwidth=0, rowheight=28, font=("Segoe UI", 10),
    )
    style.map("Treeview",
        background=[("selected", SURFACE2)],
        foreground=[("selected", TEXT)],
    )
    style.configure("Treeview.Heading",
        background=SURFACE, foreground=TEXT,
        font=("Segoe UI", 10, "bold"),
    )

    style.configure("TScrollbar",
        background=SURFACE, troughcolor=BG,
        bordercolor=BG, arrowcolor=TEXT, arrowsize=12,
    )
    style.map("TScrollbar",
        background=[("active", SURFACE2)],
    )

    style.configure("TPanedwindow", background=SURFACE2)
    style.configure("Sash", sashthickness=5, sashrelief="flat")
