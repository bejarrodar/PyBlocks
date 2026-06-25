# Custom Blocks

PyBlocks lets you create your own blocks in two ways:

1. **Block Editor** — a built-in GUI, no coding required
2. **Expansion packs** — Python files with `@block` decorators, for more control

Both produce blocks that appear in the palette and work exactly like built-in blocks.

---

## Block Editor (GUI)

Open it from **Extras → Block Editor**.

The editor has these fields:

| Field | What it sets |
|---|---|
| **Name** | Internal identifier (no spaces) |
| **Label** | What the block displays — use `{fieldname}` for input fields |
| **Category** | Which palette group it appears in |
| **Color** | Block background color |
| **Code Template** | The Python code the block generates |

### Writing a label

The label is what users see on the block. Use curly braces `{like_this}` to mark where users can type values.

Example label:
```
{result} = {value1} + {value2}
```

This creates a block with three input fields: result, value1, and value2.

### Writing a code template

The code template uses the same `{fieldname}` placeholders. When PyBlocks generates code it substitutes the user's typed values.

Example code template matching the label above:
```python
{result} = {value1} + {value2}
```

For a block that wraps multi-line code (like an `if` or `for`), check the **Container** box. A container block gets a shaded body zone where other blocks can be nested inside it. In the code template, use `{body}` where the nested code should appear:

```python
for {item} in {iterable}:
    {body}
```

### Testing it

After clicking **Save**, the block appears immediately in the palette under the category you chose. Drag it onto the canvas and try it.

---

## Expansion Packs

An expansion pack is a plain Python file in the `expansions/` folder. Any function decorated with `@block` becomes a block.

### File location

```
your-pyblocks-project/
└── expansions/
    └── my_blocks.py
```

PyBlocks automatically scans the `expansions/` folder on launch and registers all `@block` functions it finds.

### The `@block` decorator

```python
from pyblocks.blocks import block

@block(
    label="{result} = double({value})",
    category="My Blocks",
    color="#a6e3a1"
)
def double_value(result, value):
    return f"{result} = {value} * 2"
```

The function returns a string of Python code. The parameter names must match the `{placeholders}` in the label.

### Decorator parameters

| Parameter | Required | Description |
|---|---|---|
| `label` | Yes | What the block displays, with `{field}` placeholders |
| `category` | Yes | Palette group name |
| `color` | No | Hex color (defaults to category color) |
| `indent` | No | Set to `True` for container blocks |

### Container blocks

Set `indent=True` to make a block that has a body zone for nesting other blocks inside it.

```python
@block(
    label="repeat {times} times:",
    category="My Blocks",
    color="#cba6f7",
    indent=True
)
def repeat_block(times, body=""):
    return f"for _ in range({times}):\n{body}"
```

The `body` parameter receives the indented code from whatever blocks are nested inside. Give it a default of `""` so the block works even when the body is empty.

### Multi-line code

Your function can return any valid Python, including multi-line strings:

```python
@block(
    label="clamp {value} between {low} and {high} → {result}",
    category="My Blocks"
)
def clamp(result, value, low, high):
    return (
        f"_v = {value}\n"
        f"{result} = {low} if _v < {low} else ({high} if _v > {high} else _v)"
    )
```

### Pack metadata

Add a docstring to your file to give the pack a name and description that shows in the Package Manager:

```python
"""
name: My Utility Blocks
description: Custom blocks for common calculations
"""

from pyblocks.blocks import block

@block(...)
def my_block(...):
    ...
```

### Enabling packs per project

Expansion packs are toggled per project from **Extras → Package Manager → Local Expansions**. Check or uncheck a pack to show or hide its blocks in the palette. The setting saves to `.pyblocks/project.json`.

---

## Sharing expansion packs

An expansion pack is a single Python file — share it by copying the file into anyone else's `expansions/` folder. No installation needed.

---

## Examples

### A greeting block

```python
@block(
    label='greet {name}',
    category="My Blocks",
    color="#89b4fa"
)
def greet(name):
    return f'print("Hello, " + str({name}) + "!")'
```

### A swap-variables block

```python
@block(
    label="swap {a} and {b}",
    category="My Blocks"
)
def swap(a, b):
    return f"{a}, {b} = {b}, {a}"
```

### A timed section (container)

```python
@block(
    label="time this section → {result}",
    category="My Blocks",
    indent=True
)
def timed_section(result, body=""):
    return (
        f"import time as _time\n"
        f"_start = _time.perf_counter()\n"
        f"{body}\n"
        f"{result} = _time.perf_counter() - _start"
    )
```
