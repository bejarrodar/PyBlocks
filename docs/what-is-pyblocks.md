# What is PyBlocks?

## Programs are just instructions

A computer program is nothing more than a list of instructions that a computer follows in order. Something like:

1. Ask the user to type a number
2. Multiply that number by 2
3. Print the result

That's a real program. Writing those instructions in Python looks like this:

```python
number = int(input("Type a number: "))
result = number * 2
print(result)
```

Python is just a specific language for writing instructions that a computer can run. Like any language, it has rules about how you write things — what words to use, where to put parentheses, when to indent. Those rules are called **syntax**.

Learning syntax is honestly the most annoying part of learning to program. The logic comes naturally. "Ask for a number, multiply it, print it" — that's obvious. But why does `input()` need parentheses? Why do I need to wrap it in `int()`? Why does Python care about spaces? These questions distract from the actual thinking.

## What PyBlocks does

PyBlocks lets you express those same instructions by dragging colored blocks onto a canvas instead of typing text. Each block represents one instruction. Snap them together in order and you've written a program.

Here's what that looks like for the program above:

```
┌─────────────────────────────────┐
│  number = input( "Type a number" ) │   ← Ask user for input
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│  result = number × 2            │   ← Multiply
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│  print( result )                │   ← Show the answer
└─────────────────────────────────┘
```

But here's the key difference from other visual tools: **PyBlocks shows you the real Python code it's generating, right next to the canvas, as you build.** There's no hidden translation. What you see in the code panel is exactly what will run.

## Why bother with blocks at all?

Because the hardest part of learning to code isn't understanding loops or if-statements — it's getting over the intimidation of a blank text file and cryptic error messages.

With PyBlocks:
- You can't make a syntax error. The blocks always generate valid Python.
- You can see immediately what each instruction looks like in code.
- When something breaks, the app highlights the exact block that caused it.
- You can experiment freely — drag things around, change values, run it again.

Once you understand what the code does and why, you're ready to write it yourself. At that point you can copy the generated Python right out of the code panel and start editing it in any text editor. You've been reading Python the whole time without having to type it.

## What PyBlocks is not

PyBlocks is not a production tool. It's not designed for building apps people ship to customers. The blocks cover a huge range of Python but they don't cover everything, and at some point you'll want to write Python directly.

That's the goal. Use PyBlocks until you don't need it anymore.

## The example projects

PyBlocks comes with two complete example projects to show what's possible:

### Number Guesser

A classic beginner project. The computer picks a random number between 1 and 10. You type your guess. It tells you if you got it right.

Open it and you'll see about a dozen blocks on the canvas — a `random.randint` block, some variable blocks, an `input` block, and a few `if/else` blocks. Run it, play with it, change the range from 10 to 100 and see what breaks.

### Snake

A fully playable Snake game built with the **pygame** library. The snake moves across a grid, eats food (red squares), and grows longer. Hit a wall or yourself and it's game over.

This one is more complex — about 60 lines of generated Python — and it shows what PyBlocks looks like at scale. It also demonstrates how to use an installed third-party library (pygame) through the Package Manager.

To run Snake you need pygame installed:
```bash
pip install pygame
```

Then open the Snake project in PyBlocks and hit Run.
