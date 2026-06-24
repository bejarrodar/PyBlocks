# PyBlocks

A drag-and-drop Python learning environment for people who already think like programmers. Every block you place generates real, visible, runnable Python — no hidden magic, no walled garden.

---

## What it is

PyBlocks sits between Scratch and a text editor. You drag blocks onto a canvas; the right panel shows the Python they produce, live. Run it with one click, see the output stream in the console, and when something breaks the error highlights the block that caused it.

The goal isn't to replace writing code — it's to make the mental model of "code = instructions" concrete before you have to worry about syntax.

---

## Features

- **Live code preview** — the generated `.py` file updates as you drag and edit blocks (debounced 300ms). Click any line to jump to its block; hover any block to highlight its lines.
- **~100 built-in blocks** across 17 categories covering the full Python standard library
- **Indented container blocks** — `if`, `for`, `while`, `def`, `class`, `try/except`, `match/case` all open body zones that children drop into, generating properly indented code
- **Custom block editor** — build your own blocks in-app without touching the source
- **Expansion packs** — drop a Python package into `expansions/` and its blocks appear in the palette automatically. Enable/disable per project.
- **Class handling** — import any `.py` file with a class and get method blocks for it, with three-tier method discovery (AST → inspect subprocess → stdlib cache)
- **Challenge mode** — random project prompts accessible via menu or keyboard shortcut
- **Dockable panels** — every panel can be detached, repositioned, or hidden; layout is saved per project
- **No pip required** — base install uses only the Python standard library (`tkinter`, `subprocess`, `ast`, `inspect`, `json`, `pathlib`)

---

## Requirements

- Python 3.10 or later (match/case blocks require 3.10+)
- tkinter (included with most Python installers)
- `psutil` — optional, enables subprocess memory monitoring

---

## Running

```bash
python -m pyblocks
```

That's it. No install step, no virtual environment required for the base app.

---

## Block categories

| Category | What's in it |
|---|---|
| Output | `print`, `print` with sep/end |
| Variables | assignment, `global`, preset dunders |
| Control | `if`/`elif`/`else`, `for`, `while`, `break`, `continue`, `pass`, `match`/`case` |
| Functions & Classes | `def`, `class`, `return`, `yield`, `lambda`, decorators |
| Error Handling | `try`/`except`/`finally`, `raise`, `assert` |
| Imports | `import`, `from … import`, `import as` |
| I/O | `input`, `open`, `read`, `write`, `close`, context manager |
| Type Casting | `int`, `float`, `str`, `bool`, `list`, `tuple`, `set`, `dict`, `bytes` |
| Math | `abs`, `round`, `pow`, `divmod`, `min`, `max`, `sum`, `hash`, `id` |
| Sequences | `len`, `range`, `enumerate`, `zip`, `map`, `filter`, `sorted`, `reversed`, `any`, `all`, `next`, `slice` |
| Lists | `append`, `extend`, `insert`, `remove`, `pop`, `sort`, `reverse`, `index`, `count`, `copy`, `clear` |
| Dictionaries | `get`, `keys`, `values`, `items`, `update`, `pop`, `setdefault`, `copy`, `clear`, `fromkeys` |
| Sets | `add`, `remove`, `discard`, `union`, `intersection`, `difference`, `issubset`, `issuperset` |
| Inspection | `type`, `isinstance`, `issubclass`, `callable`, `hasattr`, `getattr`, `setattr`, `delattr`, `dir`, `vars`, `globals`, `locals` |
| Iteration | `iter`, `next` (with default), async `aiter`/`anext` |
| Advanced | `eval`, `exec`, `compile`, `breakpoint`, `super`, `property`, `staticmethod`, `classmethod`, `memoryview`, `slice` |

---

## Project structure

Projects are plain folders. The generated `.py` files are always human-readable and runnable outside PyBlocks.

```
my_project/
  main.py              ← generated Python (run this directly any time)
  player.py            ← other files in your project
  .pyblocks/
    canvas.json        ← block positions and connections
    layout.json        ← panel dock states
    project.json       ← project metadata
```

---

## Adding custom blocks

The fastest way is the in-app Block Editor (menu → Blocks → New Block). For anything more structured, drop a `.py` file with `@block`-decorated functions into your project or into `expansions/`:

```python
from pyblocks.blocks.definition import block

@block(
    label="GREET {name}",
    category="Output",
    color="#fab387",
    description="Print a greeting."
)
def greet(name):
    return f'print(f"Hello, {name}!")'
```

- `{param}` tokens in the label become inline input fields on the block.
- `indent=True` makes the block open an indented body zone (for container blocks like `if` or `def`).
- No `@block` decorator is required — any function in a loaded file gets a generic block auto-generated from its name and signature.

---

## Expansion packs

Drop a package into `expansions/` and restart (or hit Refresh in the Package Manager panel):

```
expansions/
  my_pack/
    __init__.py        ← pack name, version, description
    blocks/
      my_blocks.py     ← @block decorated functions
```

The pack appears as its own collapsible group in the palette. Enable or disable it per project via the Package Manager panel.

---

## Running the tests

```bash
python -m pytest
```

The test suite is stdlib-only (`pytest` is the only dev dependency).

---

## Security note

PyBlocks runs real Python code on your machine under your own user account. There is no sandbox. On first launch, the app shows a one-time warning before opening. Only run projects you trust.

---

## Design principles

- Every block produces visible, copyable, runnable Python — no black boxes
- Flat canvas, no forced scaffolding — the user decides the structure
- Expanding the block library never requires touching core code
- The app ships with an example project that reproduces parts of PyBlocks itself using PyBlocks blocks
