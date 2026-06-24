import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from pathlib import Path
from pyblocks.panels import Panel, PanelManager
from pyblocks.panels.files_panel import FileExplorerPanel
from pyblocks.panels.canvas_panel import CanvasPanel
from pyblocks.panels.live_python_panel import LivePythonPanel
from pyblocks.panels.palette_panel import PalettePanel
from pyblocks.panels.console_panel import ConsolePanel
from pyblocks.project import Project, ProjectIO
from pyblocks.codegen.generator import CodeGenerator
from pyblocks.codegen.debounce import DebouncedWriter
from pyblocks.codegen.error_mapper import ErrorMapper
from pyblocks.runner import ProgramRunner
from pyblocks.blocks.editor.model import CustomBlockDef
import pyblocks.blocks.builtins  # registers built-in blocks into the registry


class PyBlocksApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PyBlocks")
        self.geometry("1280x800")
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._project: Project | None = None
        self._panel_manager: PanelManager | None = None
        self._has_unsaved = False
        self._canvas_panel: CanvasPanel | None = None
        self._live_panel: LivePythonPanel | None = None
        self._debounce: DebouncedWriter | None = None
        self._palette_panel: PalettePanel | None = None
        self._custom_block_defns: list[CustomBlockDef] = []
        self._runner: ProgramRunner | None = None


        self._build_menu()
        self._build_toolbar()
        self._build_layout()
        self._bind_keys()

    # ── menu ──────────────────────────────────────────────────────────
    def _build_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Project...", command=self._new_project)
        file_menu.add_command(label="Open Project...", command=self._open_project)
        file_menu.add_separator()
        file_menu.add_command(label="Save", accelerator="Ctrl+S",
                              command=self._save)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_close)
        menubar.add_cascade(label="File", menu=file_menu)
        self.bind_all("<Control-s>", lambda _: self._save())

        run_menu = tk.Menu(menubar, tearoff=0)
        run_menu.add_command(label="Run", accelerator="F5",
                             command=lambda: None)
        run_menu.add_command(label="Stop", command=lambda: None)
        menubar.add_cascade(label="Run", menu=run_menu)
        self.bind_all("<F5>", lambda _: None)

        self._view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=self._view_menu)

        extras_menu = tk.Menu(menubar, tearoff=0)
        self._extras_menu = extras_menu
        self._extras_menu.add_command(label="Package Manager",
                                      command=self._open_package_manager)
        self._extras_menu.add_command(label="Block Editor",
                                      command=self._open_block_editor)
        self._extras_menu.add_separator()
        self._extras_menu.add_command(label="Get a Challenge",
                                      command=self._show_challenge,
                                      accelerator="Ctrl+Shift+C")
        menubar.add_cascade(label="Extras", menu=extras_menu)

    # ── toolbar ───────────────────────────────────────────────────────
    def _build_toolbar(self):
        toolbar = ttk.Frame(self, relief="raised")
        toolbar.pack(side="top", fill="x")
        self._run_btn = ttk.Button(toolbar, text="▶ Run", command=self._run)
        self._run_btn.pack(side="left", padx=4, pady=2)
        self._stop_btn = ttk.Button(toolbar, text="■ Stop", command=self._stop,
                                     state="disabled")
        self._stop_btn.pack(side="left", padx=4, pady=2)
        self._unsaved_label = ttk.Label(toolbar, text="")
        self._unsaved_label.pack(side="right", padx=8)

    # ── main layout ───────────────────────────────────────────────────
    def _build_layout(self):
        # Main vertical split: content (top) | console (bottom)
        self._main_pane = ttk.PanedWindow(self, orient="vertical")
        self._main_pane.pack(fill="both", expand=True)

        # Outer paned: left sidebar | center (horizontal)
        self._outer_pane = ttk.PanedWindow(self._main_pane, orient="horizontal")
        self._main_pane.add(self._outer_pane, weight=4)

        # Left sidebar: Files (top) + Palette (bottom) stacked
        self._left_pane = ttk.PanedWindow(self._outer_pane, orient="vertical")
        self._outer_pane.add(self._left_pane, weight=1)

        # Center paned: canvas | live python (horizontal)
        self._center_pane = ttk.PanedWindow(self._outer_pane, orient="horizontal")
        self._outer_pane.add(self._center_pane, weight=5)

        # Placeholder panels — replaced by real panels in later plans
        self._files_panel = None  # created when a project loads — see _load_panels()
        self._files_placeholder = ttk.LabelFrame(self._left_pane, text="① Files (no project)")
        self._left_pane.add(self._files_placeholder, weight=1)

        self._palette_placeholder = ttk.LabelFrame(self._left_pane, text="② Palette")
        self._left_pane.add(self._palette_placeholder, weight=2)

        self._canvas_placeholder = ttk.LabelFrame(self._center_pane, text="③ Canvas")
        self._center_pane.add(self._canvas_placeholder, weight=3)

        self._code_placeholder = ttk.LabelFrame(self._center_pane, text="④ Live Python")
        self._center_pane.add(self._code_placeholder, weight=2)

        # Console at bottom — in its own frame so the sash between content and console is draggable
        self._console_frame = ttk.Frame(self._main_pane)
        self._main_pane.add(self._console_frame, weight=1)
        self._console_panel = ConsolePanel(self._console_frame, on_error_block=self._on_error_block)
        self._console_panel.pack(fill="both", expand=True)

        if self._panel_manager:
            self._panel_manager.register(self._console_panel)
        self._view_menu.add_checkbutton(
            label="⑤ Console",
            command=lambda: self._panel_manager.toggle("console")
        )

    def mark_unsaved(self):
        self._has_unsaved = True
        self._unsaved_label.config(text="● unsaved changes")

    def mark_saved(self):
        self._has_unsaved = False
        self._unsaved_label.config(text="")

    def _load_panels(self):
        # Register console panel now that _panel_manager exists
        if "console" not in self._panel_manager.panels:
            self._panel_manager.register(self._console_panel)

        # Remove placeholder (guarded — may already be gone on second project load)
        try:
            self._left_pane.forget(self._files_placeholder)
        except Exception:
            pass

        # Files panel
        self._files_panel = FileExplorerPanel(self, project=self._project)
        self._left_pane.add(self._files_panel, weight=1)
        if self._panel_manager:
            self._panel_manager.register(self._files_panel)

        # Canvas panel
        try:
            self._center_pane.forget(self._canvas_placeholder)
        except Exception:
            pass
        canvas_model = ProjectIO.load_canvas(self._project)
        self._canvas_panel = CanvasPanel(self, canvas_model=canvas_model,
                                            on_change=self._on_canvas_change)
        self._center_pane.add(self._canvas_panel, weight=3)
        if self._panel_manager:
            self._panel_manager.register(self._canvas_panel)
        self._view_menu.add_checkbutton(
            label="③ Canvas",
            command=lambda: self._panel_manager.toggle("canvas")
        )

        # Live Python panel
        try:
            self._center_pane.forget(self._code_placeholder)
        except Exception:
            pass
        self._live_panel = LivePythonPanel(
            self,
            on_line_click=self._on_live_line_click,
        )
        self._center_pane.add(self._live_panel, weight=2)
        if self._panel_manager:
            self._panel_manager.register(self._live_panel)
        self._view_menu.add_checkbutton(
            label="④ Live Python",
            command=lambda: self._panel_manager.toggle("live_python")
        )

        # Palette panel
        try:
            self._left_pane.forget(self._palette_placeholder)
        except Exception:
            pass
        self._palette_panel = PalettePanel(self, on_palette_drag=self._on_palette_drop)
        self._left_pane.add(self._palette_panel, weight=2)
        if self._panel_manager:
            self._panel_manager.register(self._palette_panel)
        self._view_menu.add_checkbutton(
            label="② Palette",
            command=lambda: self._panel_manager.toggle("palette")
        )

        # Wire on-change pipeline
        self._debounce = DebouncedWriter(delay=0.3, callback=self._write_generated_file)
        self._canvas_panel.renderer._on_select = self._on_canvas_select

        # Populate live panel with current canvas state
        self._write_generated_file()


    # ── project actions ───────────────────────────────────────────────
    def _new_project(self):
        folder = filedialog.askdirectory(title="Choose parent folder for new project")
        if not folder:
            return
        name = simpledialog.askstring("Project Name", "Enter project name:")
        if not name:
            return
        root = Path(folder) / name
        self._project = ProjectIO.create(name=name, root=root)
        self._panel_manager = PanelManager(self, self._project)
        self.title(f"PyBlocks — {name}")
        self._load_panels()
        self._load_enabled_expansions()
        self._load_enabled_packages()
        self._load_custom_blocks()
        self.mark_saved()


    def _open_project(self):
        folder = filedialog.askdirectory(title="Open PyBlocks Project")
        if not folder:
            return
        try:
            self._project = ProjectIO.load(Path(folder))
            self._panel_manager = PanelManager(self, self._project)
            self._panel_manager.restore_layout()
            self.title(f"PyBlocks — {self._project.name}")
            self._load_panels()
            self._load_enabled_expansions()
            self._load_enabled_packages()
            self._load_custom_blocks()
            self.mark_saved()
        except FileNotFoundError:
            messagebox.showerror("Not a PyBlocks project",
                                 f"{folder} does not contain a .pyblocks folder.")

    def _save(self):
        if self._project:
            ProjectIO.save(self._project)
            if self._panel_manager:
                self._panel_manager.save_layout()
            if self._canvas_panel:
                ProjectIO.save_canvas(self._project, self._canvas_panel.renderer._model)
            self.mark_saved()

    def _on_canvas_change(self) -> None:
        """Called whenever a block is added/moved/deleted on the canvas."""
        if self._palette_panel and self._canvas_panel:
            from pyblocks.canvas.variables import VariableTracker, FunctionTracker
            model = self._canvas_panel.renderer._model
            var_names = VariableTracker.scan(model)
            self._palette_panel.sync_user_variables(var_names)
            fn_names = FunctionTracker.scan(model)
            self._palette_panel.sync_user_functions(fn_names)
        self.mark_unsaved()
        if self._debounce:
            self._debounce.schedule()

    def _on_palette_drop(self, defn) -> None:
        if not self._canvas_panel:
            return
        from pyblocks.canvas.model import Block
        new_block = Block(
            type=defn.name,
            label_template=defn.label,
            color=defn.color,
            indent=defn.indent,
            inputs={k: "" for k in defn.inputs},
        )
        self._canvas_panel.renderer._model.blocks.append(new_block)
        self._canvas_panel.renderer.redraw()
        self._on_canvas_change()

    def _write_generated_file(self) -> None:
        if not self._project or not self._canvas_panel:
            return
        model = self._canvas_panel.renderer._model
        code, id_map = CodeGenerator.generate_with_map(model)
        from pyblocks.codegen.auto_import import AutoImporter
        import_lines = AutoImporter.compute_imports(model, self._project.root)
        if import_lines:
            offset = len(import_lines) + 1  # blank separator line
            id_map = {k: v + offset for k, v in id_map.items()}
            code = "\n".join(import_lines) + "\n\n" + code
        active_file = self._project.root / "main.py"
        active_file.write_text(code)
        if self._live_panel:
            self._live_panel.set_code(code, id_map)

    def _open_block_editor(self) -> None:
        if not self._project:
            return
        from pyblocks.panels.block_editor_panel import BlockEditorPanel
        panel = BlockEditorPanel(self, on_save=self._on_custom_block_save)
        panel.float()

    def _on_custom_block_save(self, defn: CustomBlockDef) -> None:
        existing = {d.name: i for i, d in enumerate(self._custom_block_defns)}
        if defn.name in existing:
            self._custom_block_defns[existing[defn.name]] = defn
        else:
            self._custom_block_defns.append(defn)
        from pyblocks.blocks.editor.file_writer import BlockFileWriter
        from pyblocks.blocks.editor.loader import CustomBlockLoader
        BlockFileWriter.write(self._project.root, self._custom_block_defns)
        loader = CustomBlockLoader(self._project.root)
        loader.load_or_reload()
        if self._palette_panel:
            self._palette_panel._populate()

    def _load_custom_blocks(self) -> None:
        from pyblocks.blocks.editor.loader import CustomBlockLoader
        loader = CustomBlockLoader(self._project.root)
        try:
            loader.load_or_reload()
        except RuntimeError:
            pass

    def _run(self) -> None:
        if not self._project:
            return
        script = self._project.root / "main.py"
        if not script.exists():
            return
        if self._console_panel:
            self._console_panel.clear()
            self._console_panel.set_running(True)
        self._run_btn.configure(state="disabled")
        self._stop_btn.configure(state="normal")
        self._runner = ProgramRunner(
            on_stdout=self._on_run_stdout,
            on_stderr=self._on_run_stderr,
            on_exit=self._on_run_exit,
        )
        self._runner.start(script)
        if self._console_panel:
            self._console_panel.set_input_callback(self._runner.send_input)

    def _stop(self) -> None:
        if self._runner:
            self._runner.stop()

    def _on_run_stdout(self, text: str) -> None:
        if self._console_panel:
            self.after(0, lambda t=text: self._console_panel.append_stdout(t))

    def _on_run_stderr(self, line: str) -> None:
        if self._console_panel:
            self.after(0, lambda l=line: self._console_panel.append_stderr(l))

    def _on_run_exit(self, code: int) -> None:
        def _finish():
            self._run_btn.configure(state="normal")
            self._stop_btn.configure(state="disabled")
            if self._console_panel:
                self._console_panel.set_running(False)
                self._console_panel.set_input_callback(None)
            if code != 0:
                self._map_error_to_block()
        self.after(0, _finish)

    def _map_error_to_block(self) -> None:
        if not self._console_panel or not self._project:
            return
        stderr = self._console_panel.get_stderr()
        script = self._project.root / "main.py"
        if not script.exists():
            return
        source = script.read_text()
        block_id = ErrorMapper.map(stderr, source)
        if block_id and self._canvas_panel:
            self._canvas_panel.renderer.select(block_id)
            if self._live_panel:
                self._live_panel.highlight_block(block_id)

    def _on_canvas_select(self, block_id: str) -> None:
        if self._live_panel:
            self._live_panel.highlight_block(block_id)
            if self._canvas_panel:
                from pyblocks.canvas.scope import ScopeAnalyzer
                model = self._canvas_panel.renderer._model
                scope_vars = ScopeAnalyzer.in_scope_at(model, block_id)
                self._live_panel.highlight_scope(scope_vars)

    def _open_package_manager(self) -> None:
        if not self._project:
            return
        from pyblocks.expansions.loader import ExpansionLoader
        from pyblocks.project.io import ProjectIO
        from pyblocks.panels.package_manager_panel import PackageManagerPanel
        loader = ExpansionLoader(self._project.root)
        packs = loader.discover()
        enabled = ProjectIO.load_expansions(self._project)
        enabled_pkgs = {n: True for n in self._project.enabled_packages}
        panel = PackageManagerPanel(
            self, packs=packs, enabled=enabled,
            on_toggle=lambda name, val: self._on_expansion_toggle(
                name, val, loader, packs, enabled),
            enabled_packages=enabled_pkgs,
            on_toggle_package=self._on_package_toggle,
        )
        panel.float()

    def _on_expansion_toggle(self, name, value, loader, packs, enabled):
        enabled[name] = value
        from pyblocks.project.io import ProjectIO
        ProjectIO.save_expansions(self._project, enabled)
        if value:
            pack = next((p for p in packs if p.name == name), None)
            if pack:
                loader.load(pack)
        # Refresh palette
        if self._palette_panel:
            self._palette_panel._populate()

    def _show_challenge(self) -> None:
        """Loads a random challenge and shows the ChallengePopup."""
        if not self._project:
            return

        from pyblocks.challenges.bank import ChallengeBank
        from pyblocks.ui.challenge_popup import ChallengePopup

        bank = ChallengeBank.load()
        challenge = bank.random()
        ChallengePopup(self, challenge=challenge, on_accept=self._apply_starter_block)

    def _apply_starter_block(self, challenge) -> None:
        """Adds a comment block with the challenge's starter comment."""
        if not self._project or not self._canvas_panel:
            return

        from pyblocks.canvas.model import Block
        # Assuming comment_block is a valid type or we create a generic one
        new_block = Block(
            id=f"starter_{len(self._canvas_panel.renderer._model.blocks)}",
            type="comment_block",
            label_template=challenge.starter_comment,
            color="#45475a"
        )

        self._canvas_panel.renderer._model.blocks.append(new_block)
        self._canvas_panel.renderer.redraw()
        self._on_canvas_change()


    def _load_enabled_expansions(self) -> None:
        if not self._project:
            return
        from pyblocks.expansions.loader import ExpansionLoader
        from pyblocks.project.io import ProjectIO
        loader = ExpansionLoader(self._project.root)
        packs = loader.discover()
        enabled = ProjectIO.load_expansions(self._project)
        for pack in packs:
            if enabled.get(pack.name):
                try:
                    loader.load(pack)
                except RuntimeError:
                    pass

    def _load_enabled_packages(self) -> None:
        if not self._project:
            return
        from pyblocks.expansions.package_loader import PackageLoader
        PackageLoader.load_enabled(self._project.enabled_packages)

    def _on_package_toggle(self, name: str, enabled: bool) -> None:
        if not self._project:
            return
        pkgs = list(self._project.enabled_packages)
        if enabled and name not in pkgs:
            pkgs.append(name)
        elif not enabled and name in pkgs:
            pkgs.remove(name)
        self._project.enabled_packages = pkgs
        from pyblocks.project.io import ProjectIO
        ProjectIO.save(self._project)
        if self._palette_panel:
            self._palette_panel._populate()

    def _on_error_block(self, block_id: str) -> None:
        if self._canvas_panel:
            self._canvas_panel.renderer.select(block_id)
        if self._live_panel:
            self._live_panel.highlight_block(block_id)

    def _on_live_line_click(self, block_id: str) -> None:
        if self._canvas_panel:
            self._canvas_panel.renderer.select(block_id)

    def _on_close(self) -> None:
        if self._has_unsaved:
            if messagebox.askyesno("Unsaved changes", "Save before closing?"):
                self._save()
        if self._runner:
            self._runner.stop()
        self.destroy()

    def _bind_keys(self):
        self.bind("<Control-Shift-c>", lambda _e: self._show_challenge())
        self.bind("<Control-Shift-C>", lambda _e: self._show_challenge())
