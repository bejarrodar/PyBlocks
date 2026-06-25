# Getting Started

## Running PyBlocks

From the project root:

```bash
python -m pyblocks
```

On Windows you can also double-click **PyBlocks.bat**.

The first time you launch, PyBlocks shows a one-time security notice explaining that it runs real Python code on your machine. Click OK to continue.

---

## Opening a project

PyBlocks organizes your work into **projects** — each project is a folder on your computer.

On the startup screen:
- **New Project** — choose a folder location, give it a name, and you're in
- **Open Project** — browse to an existing PyBlocks project folder
- **Example Projects** — open one of the included examples (Number Guesser or Snake)

You can also go to **File → New Project** or **File → Open Project** at any time.

---

## The interface

PyBlocks has five main areas visible when you open a project:

```
┌─────────────┬────────────────────────────┬─────────────────┐
│             │                            │                 │
│  Files      │         Canvas             │   Live Python   │
│  Panel      │   (drag blocks here)       │   (code panel)  │
│             │                            │                 │
│  Palette    │                            │                 │
│  Panel      │                            │                 │
│             │                            │                 │
├─────────────┴────────────────────────────┴─────────────────┤
│                     Console Panel                          │
└────────────────────────────────────────────────────────────┘
```

### Files Panel (top left)

Shows the files in your project folder. Click any `.py` file to view its generated code. This is where you'll see `main.py` — the Python file that PyBlocks generates from your blocks.

### Palette Panel (bottom left)

The full library of available blocks, organized into categories. Click a category name to expand or collapse it. You can also search by typing in the search box at the top.

Each block is color-coded by its category — for example, all string blocks are green, all math blocks are yellow, all file blocks are teal.

To use a block, **click and drag it from the palette onto the canvas**.

### Canvas (center)

This is where you build your program. Drag blocks here from the palette, arrange them top to bottom, and fill in their values.

**Key interactions:**
- **Drag** — click and hold a block to move it
- **Click a field** — click any highlighted text field on a block to edit its value
- **Nesting** — some blocks (like `if`, `for`, `while`, `def`) open a shaded body zone when you drop them. Drag child blocks into that zone to put them inside.
- **Right-click** — delete a block or cut/copy/paste it
- **Scroll** — scroll wheel to pan up and down; hold middle mouse or Ctrl+scroll to zoom

Blocks are run in order from top to bottom when you hit Run.

### Live Python Panel (right)

Shows the Python code that your canvas is generating, updated live as you work. You don't have to do anything to keep this in sync — it just updates.

**Navigation:**
- Hover over any block to highlight its corresponding lines in the code panel
- Click any line in the code panel to jump to and select the block that generated it

This panel is read-only — you can copy code out of it, but you can't type in it. To edit your program you work on the canvas.

### Console Panel (bottom)

When you run your program, output appears here. `print()` statements, input prompts, and error messages all show up in the console.

If your program crashes, the error message appears in red and PyBlocks tries to highlight the block that caused it.

---

## Running your program

Click the **Run** button in the toolbar (or press **F5**).

Your program runs in a separate process in the background so a crash or infinite loop can't freeze the editor. Click **Stop** to terminate a running program.

---

## Saving

Press **Ctrl+S** or go to **File → Save**. The toolbar shows a `*` next to the project name when you have unsaved changes.

PyBlocks saves two things when you save:
- The canvas block layout (positions, values, connections) to `.pyblocks/canvas.json`
- The generated `main.py` — which is already there because it updates as you work

---

## Other panels and tools

These open on demand from the **Extras** menu or the toolbar:

### Package Manager

Opens a floating window with three sections:
1. **Install Package** — type any pip package name (like `pygame` or `requests`) and click Install. PyBlocks installs it, scans its public functions, and makes them available as blocks in the palette.
2. **Scanned Packages** — shows packages you've already installed through PyBlocks, with version info and a Rescan button.
3. **Local Expansions** — toggle any expansion packs (custom block files in the `expansions/` folder) on or off for this project.

See [Package Manager](package-manager.md) for full details.

### Block Editor

Build your own blocks without editing source code. Give it a name, write a label with `{fields}` in curly braces, pick a category and color, write the Python code it should generate. The block appears in the palette immediately.

See [Custom Blocks](custom-blocks.md) for full details.

### Challenge Mode

Opens a popup with a random project idea and a difficulty level. Accept a challenge and a starter comment block appears on the canvas. Press **Ctrl+Shift+C** to get a new challenge any time.

---

## Keyboard shortcuts

| Shortcut | Action |
|---|---|
| F5 | Run program |
| Ctrl+S | Save project |
| Ctrl+Shift+C | New challenge |
| Ctrl+Z | Undo (canvas) |

---

## Next steps

Ready to build something? Follow the [Building Your First Program](building-your-first-program.md) tutorial — it walks you through creating a number guessing game from scratch, explaining every block along the way.
