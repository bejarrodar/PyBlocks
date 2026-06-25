# PyBlocks

**A visual coding environment that teaches you real Python.**

PyBlocks lets you build programs by dragging and connecting colored blocks — like assembling LEGO. As you place blocks, you can see the actual Python code being generated on screen in real time. Run your program with one click, and when something breaks, the error highlights the exact block that caused it.

The goal is simple: get from "I've never written a line of code" to "I understand what Python code actually does" as quickly and painlessly as possible.

---

## What is block-based programming?

If you've never coded before, here's the idea:

A computer program is a list of instructions. You could type those instructions in a text file — that's what most programmers do. But when you're just starting out, the hardest part isn't the logic — it's the syntax. Every comma, colon, and parenthesis has to be exactly right or nothing works, and the error messages aren't always helpful.

Block-based programming solves this by letting you pick your instructions from a menu and snap them together like puzzle pieces. The app handles the punctuation. You focus on the logic.

PyBlocks is different from most block-based tools because it doesn't hide the code from you. Everything you build is shown as real Python in a panel right next to the canvas. When you're ready to stop using blocks and write Python directly, you already know what it looks like — because you've been reading it the whole time.

---

## What you can build with it

Here's what's included to get you started:

| Example Project | What it does | Skills it teaches |
|---|---|---|
| **Number Guesser** | The computer picks a number 1–10. You guess. It tells you if you're right or wrong. | Variables, random numbers, user input, if/else logic |
| **Snake** | A full playable Snake game using the pygame library — move with arrow keys, eat food, grow longer | Game loops, keyboard events, lists, collision detection |

Both projects open with all their blocks already on the canvas. You can see exactly how they were built, change anything, and run them.

---

## Features

- **408 blocks** across 30+ categories — built-in Python operations plus the entire standard library
- **Live code preview** — the generated Python updates within 300ms of every change
- **Run and stop** — programs run in a separate process so a crash or infinite loop can't freeze the editor
- **Error highlighting** — when your program crashes, the block that caused it turns red
- **Click to navigate** — click any line in the code panel to jump to its block on the canvas; hover a block to highlight its code
- **Package Manager** — install any pip package and its functions automatically become blocks in the palette
- **Expansion packs** — drop a Python file into the `expansions/` folder and its blocks appear immediately
- **Custom block editor** — build your own reusable blocks without touching the source code
- **Dockable panels** — detach, resize, or hide any panel; layout saves per project
- **Challenge mode** — random project prompts with starter blocks to keep you moving
- **No installation** — runs on plain Python with no pip dependencies for the base app

---

## Requirements

- Python 3.10 or later
- `tkinter` (bundled with Python on Windows and macOS; on Linux: `sudo apt install python3-tk`)
- `psutil` — optional, enables memory monitoring for running programs

---

## Running PyBlocks

```bash
python -m pyblocks
```

That's it. No `pip install`, no virtual environment, no build step.

On Windows you can also double-click **PyBlocks.bat** in the project root.

---

## Documentation

| Guide | What it covers |
|---|---|
| [What is PyBlocks?](docs/what-is-pyblocks.md) | A longer introduction for complete beginners |
| [Getting Started](docs/getting-started.md) | The interface tour — every panel explained |
| [Building Your First Program](docs/building-your-first-program.md) | Step-by-step: build a number guessing game from zero |
| [Block Reference](docs/block-reference.md) | Every category and block, with what code it generates |
| [Package Manager](docs/package-manager.md) | Installing pip packages, using expansion packs |
| [Custom Blocks](docs/custom-blocks.md) | Writing your own blocks and expansion packs |

---

## Project structure

PyBlocks projects are plain folders. The generated Python file is always human-readable and can be run directly from the terminal without PyBlocks:

```
my_project/
  main.py              ← the real Python code PyBlocks generated
  .pyblocks/
    canvas.json        ← block positions and values
    layout.json        ← which panels are open and where
    project.json       ← project name and enabled packages
```

---

## Security

PyBlocks runs real Python code on your machine under your own user account. There is no sandbox. On first launch it shows a one-time warning explaining this. Only open projects from sources you trust.
