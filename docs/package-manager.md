# Package Manager

The Package Manager is how you extend PyBlocks beyond its built-in 408 blocks. It does two things:

1. **Install pip packages** — type a package name, click Install, and PyBlocks installs it and turns its functions into blocks automatically
2. **Manage expansion packs** — toggle local expansion packs (custom block files) on or off per project

Open it from the **Extras menu → Package Manager**, or from the toolbar.

---

## Installing a pip package

### What this means

Python has a massive ecosystem of third-party packages — libraries that other people have written and published for anyone to use. Examples:

- **pygame** — build games with graphics, sound, and keyboard input
- **requests** — download web pages and talk to APIs
- **pillow** — manipulate images
- **numpy** — fast math with large arrays of numbers
- **pandas** — work with tables of data

Normally you'd install these by typing `pip install pygame` in a terminal. The PyBlocks Package Manager does this for you and then does something extra: it scans the package to find all its public functions and turns them into drag-and-drop blocks.

### How to install

1. Open the Package Manager (**Extras → Package Manager**)
2. In the **Install Package** section at the top, type the package name (e.g. `pygame`)
3. Click **Install**
4. Watch the status label:
   - `Installing…` — pip is downloading and installing the package
   - `Scanning…` — PyBlocks is reading the package to discover its functions
   - `Done — N blocks added` — success, the blocks are now in the palette
   - `Failed: <error>` — something went wrong (usually a typo in the package name)

Once installed, the package appears in the **Scanned Packages** section with its version number.

### Finding the new blocks

After installation, new category groups appear in the Palette panel. For pygame, you'd see:

- `Pygame` — top-level functions
- `Pygame: draw` — drawing functions
- `Pygame: display` — display management
- `Pygame: font` — text rendering
- and more...

Each package gets a consistent color across all its blocks so you can spot them at a glance.

### Enabling/disabling packages per project

Each project remembers which packages are enabled. If you have pygame installed but you're working on a non-game project, you can uncheck it in the Scanned Packages list to hide its blocks from the palette and keep the palette manageable.

The checkbox state saves to your project's `.pyblocks/project.json` file.

### Rescanning a package

If you upgrade a package (`pip install --upgrade pygame`) and want PyBlocks to pick up new functions, click **Rescan** next to that package. This re-runs the discovery process and updates the cached block list.

---

## Running the Snake example (requires pygame)

The included Snake example project uses pygame. To run it:

1. Open Package Manager
2. Type `pygame` in the Install Package field and click Install
3. Wait for "Done" status
4. Close Package Manager
5. Open **example_projects/Snake** from File → Open Project
6. Press F5 to run

You should see a Snake game window appear. Use arrow keys to move.

---

## Local expansion packs

Expansion packs are Python files containing custom block definitions that you've written yourself (or downloaded). They live in the `expansions/` folder in the PyBlocks project root.

The **Local Expansions** section at the bottom of the Package Manager lists all detected expansion packs with:
- Pack name and description
- A checkbox to enable/disable it for the current project

When you toggle an expansion pack, the palette refreshes immediately. The enabled/disabled state is per-project — different projects can use different packs.

See [Custom Blocks](custom-blocks.md) for how to create your own expansion packs.

---

## How the scanning works (for the curious)

When PyBlocks scans a package it:

1. Imports the package in a separate subprocess (so a broken package can't crash the editor)
2. Walks all submodules using `pkgutil.walk_packages`
3. Calls `inspect.getmembers()` on each submodule to find public functions
4. Reads each function's signature with `inspect.signature()` to get parameter names
5. Turns each function into a block: `{result} = package.module.function({param1}, {param2})`

The results are cached to `~/.pyblocks/packages/packagename_version.json`. Future launches load from cache instantly — the slow subprocess scan only runs once per version.

If a package contains C extensions (common in scientific packages), `inspect.signature()` sometimes can't read the parameters. In that case the block is still created, just with no input fields — you'd call it as `result = numpy.something()` and fill in the arguments manually.
