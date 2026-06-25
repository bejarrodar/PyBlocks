from __future__ import annotations
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import ttk
from typing import Callable
from pyblocks.panels.base import Panel
from pyblocks.expansions.pack import ExpansionPack
from pyblocks.inspection.package_cache import PackageCache
from pyblocks.inspection.package_scanner import PackageScanner
from pyblocks.inspection.block_factory import package_color
from importlib.metadata import version as pkg_version
from pyblocks.logger import get_logger

log = get_logger("package_manager")


class PackageManagerPanel(Panel):
    panel_id = "package_manager"
    panel_title = "Package Manager"

    def __init__(
        self,
        parent,
        packs: list[ExpansionPack],
        enabled: dict[str, bool],
        on_toggle: Callable[[str, bool], None] | None = None,
        enabled_packages: dict[str, bool] | None = None,
        on_toggle_package: Callable[[str, bool], None] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(parent, title=self.panel_title, panel_id=self.panel_id, **kwargs)
        self._packs = packs
        self._enabled = dict(enabled)
        self._on_toggle = on_toggle
        self._enabled_packages: dict[str, bool] = dict(enabled_packages or {})
        self._on_toggle_package = on_toggle_package
        self._vars: dict[str, tk.BooleanVar] = {}
        self._pkg_vars: dict[str, tk.BooleanVar] = {}
        self._pkg_frame: ttk.Frame | None = None
        self._status_var: tk.StringVar | None = None
        self._entry_var: tk.StringVar | None = None
        self._build()

    def _build(self) -> None:
        self._build_install_section()
        self._build_scanned_section()
        self._build_expansions_section()

    def _build_install_section(self) -> None:
        ttk.Label(self.content, text="Install Package",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=8, pady=(8, 4))
        row = ttk.Frame(self.content)
        row.pack(fill="x", padx=8, pady=(0, 4))
        self._entry_var = tk.StringVar()
        ttk.Entry(row, textvariable=self._entry_var).pack(side="left", fill="x", expand=True)
        ttk.Button(row, text="Install", command=self._start_install).pack(side="left", padx=(4, 0))
        self._status_var = tk.StringVar(value="Ready")
        ttk.Label(self.content, textvariable=self._status_var,
                  foreground="#585b70").pack(anchor="w", padx=8)

    def _build_scanned_section(self) -> None:
        ttk.Label(self.content, text="Scanned Packages",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=8, pady=(12, 4))
        self._pkg_frame = ttk.Frame(self.content)
        self._pkg_frame.pack(fill="both", padx=8)
        self._refresh_scanned()

    def _build_expansions_section(self) -> None:
        ttk.Label(self.content, text="Local Expansions",
                  font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=8, pady=(12, 4))
        frame = ttk.Frame(self.content)
        frame.pack(fill="both", expand=True, padx=8)
        for pack in self._packs:
            var = tk.BooleanVar(value=self._enabled.get(pack.name, False))
            self._vars[pack.name] = var
            cb = ttk.Checkbutton(
                frame, text=pack.display_name, variable=var,
                command=lambda n=pack.name, v=var: self._toggle(n, v.get()),
            )
            cb.pack(anchor="w", pady=2)
            if pack.description:
                ttk.Label(frame, text=pack.description,
                          foreground="#585b70").pack(anchor="w", padx=(20, 0))

    def _refresh_scanned(self) -> None:
        if self._pkg_frame is None:
            return
        for child in self._pkg_frame.winfo_children():
            child.destroy()
        self._pkg_vars.clear()
        for item in PackageCache.list_cached():
            name, ver = item["package"], item["version"]
            var = tk.BooleanVar(value=self._enabled_packages.get(name, False))
            self._pkg_vars[name] = var
            row = ttk.Frame(self._pkg_frame)
            row.pack(fill="x", pady=2)
            ttk.Checkbutton(
                row, variable=var,
                command=lambda n=name, v=var: self._toggle_package(n, v.get()),
            ).pack(side="left")
            ttk.Label(row, text=f"{name} {ver}").pack(side="left")
            ttk.Button(
                row, text="Rescan",
                command=lambda n=name, v=ver: self._rescan(n, v),
            ).pack(side="right")

    def _start_install(self) -> None:
        name = (self._entry_var.get() if self._entry_var else "").strip()
        if not name:
            return
        self._set_status("Installing…")
        threading.Thread(target=self._do_install, args=(name,), daemon=True).start()

    def _do_install(self, name: str) -> None:
        log.info("Installing package '%s' via pip", name)
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", name],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            err = result.stderr.strip()
            log.error("pip install '%s' failed (code %d): %s", name, result.returncode, err[-500:])
            self.content.after(0, self._set_status, f"Failed: {err[:120]}")
            return
        log.info("pip install '%s' succeeded", name)
        self.content.after(0, self._set_status, "Scanning…")
        try:
            ver = pkg_version(name)
        except Exception:
            ver = "unknown"
        log.debug("Package '%s' version: %s", name, ver)
        color = package_color(name)
        entries, scan_err = PackageScanner.scan_with_error(name)
        if entries is None:
            msg = f"Failed: {scan_err}" if scan_err else f"Failed: could not scan {name}"
            log.error("Scan of '%s' failed: %s", name, scan_err)
            self.content.after(0, self._set_status, msg)
            return
        PackageCache.write(name, ver, color, [
            {"qualname": e.qualname, "params": e.params, "submodule": e.submodule}
            for e in entries
        ])
        log.info("Cached %d blocks for '%s' %s", len(entries), name, ver)
        self.content.after(0, self._refresh_scanned)
        self.content.after(0, self._set_status, f"Done — {len(entries)} blocks added")

    def _rescan(self, name: str, version: str) -> None:
        log.info("Rescanning package '%s' %s", name, version)
        PackageCache.delete(name, version)
        self._set_status(f"Rescanning {name}…")
        threading.Thread(target=self._do_install, args=(name,), daemon=True).start()

    def _set_status(self, text: str) -> None:
        if self._status_var is not None:
            try:
                self._status_var.set(text)
            except Exception:
                pass

    def _toggle(self, name: str, value: bool) -> None:
        self._enabled[name] = value
        if self._on_toggle:
            self._on_toggle(name, value)

    def _toggle_package(self, name: str, value: bool) -> None:
        self._enabled_packages[name] = value
        if self._on_toggle_package:
            self._on_toggle_package(name, value)

    # ── public helpers (for tests / callers) ──────────────────────────────────

    def pack_names(self) -> list[str]:
        return [p.display_name for p in self._packs]

    def is_checked(self, name: str) -> bool:
        return self._vars[name].get() if name in self._vars else False

    def set_checked(self, name: str, value: bool) -> None:
        if name in self._vars:
            self._vars[name].set(value)
            self._toggle(name, value)

    def is_package_checked(self, name: str) -> bool:
        return self._pkg_vars[name].get() if name in self._pkg_vars else False

    def list_scanned_packages(self) -> list[dict]:
        """Return cached package list (delegates to PackageCache)."""
        return PackageCache.list_cached()
