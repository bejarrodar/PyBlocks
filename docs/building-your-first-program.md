# Building Your First Program

We're going to build a number guessing game from scratch. This is also one of the included example projects, so if you want to see the finished version, open **example_projects/Number Guesser** from the File menu.

Here's what the finished program will do:
1. Pick a secret random number between 1 and 10
2. Ask you to guess it
3. Tell you if you're right or wrong, and if wrong, reveal the answer

The Python it generates will look like this:

```python
import random
secret = random.randint(1, 10)
guess = int(input("Guess a number between 1 and 10: "))
if guess == secret:
    print("You got it!")
else:
    print("Nope! The number was", secret)
```

Don't worry if that looks confusing right now. By the time we're done you'll understand every part of it.

---

## Step 1: Create a new project

Go to **File → New Project**, pick a location, and name it something like `NumberGuesser`. PyBlocks opens with an empty canvas.

---

## Step 2: Import the random module

Python doesn't have random number features built in by default — you have to load them first. In programming this is called an **import**.

1. In the Palette panel, expand the **Imports** category
2. Find the block labeled `import {module}`
3. Drag it onto the canvas

Click the `{module}` field on the block and type `random`. Press Enter.

Look at the Live Python panel on the right. You should see:
```python
import random
```

That's your first line of code. You just loaded Python's random number module.

---

## Step 3: Pick a secret number

Now we need to generate a random number and store it in a **variable**. A variable is just a named box that holds a value. We'll call ours `secret`.

1. Expand the **Random** category in the palette
2. Find the block labeled `{result} = random.randint({a}, {b})`
3. Drag it onto the canvas, below the import block

Fill in the fields:
- `{result}` → `secret`
- `{a}` → `1`
- `{b}` → `10`

The Live Python panel now shows:
```python
import random
secret = random.randint(1, 10)
```

`random.randint(1, 10)` means "pick a random whole number between 1 and 10 (including both)." The result gets stored in `secret`.

---

## Step 4: Ask the user for their guess

We need to ask the player to type a number. This uses two operations chained together:

- `input()` — shows a prompt and waits for the user to type something
- `int()` — converts what they typed into a number (because input always gives back text)

1. Expand **I/O** in the palette
2. Find `{result} = input({prompt})` and drag it onto the canvas

Fill in:
- `{result}` → `guess_text`
- `{prompt}` → `"Guess a number between 1 and 10: "` (include the quotes)

Then:

3. Expand **Type Casting**
4. Find `{result} = int({value})` and drag it below

Fill in:
- `{result}` → `guess`
- `{value}` → `guess_text`

The code panel now shows:
```python
import random
secret = random.randint(1, 10)
guess_text = input("Guess a number between 1 and 10: ")
guess = int(guess_text)
```

We stored the typed text in `guess_text`, then converted it to a number and stored that in `guess`. You could also combine these into one line later, but for learning, keeping them separate makes it clearer what's happening.

---

## Step 5: Check if they got it right

Now the logic. We need to compare `guess` to `secret` and print a different message depending on whether they match.

This is an **if/else** — one of the most fundamental ideas in all of programming. "If this is true, do this. Otherwise, do that."

1. Expand **Control** in the palette
2. Find the `if {condition}:` block and drag it onto the canvas

Fill in `{condition}` → `guess == secret`

The `==` means "is equal to." (One equals sign `=` means "store this value." Two equals signs `==` means "are these two things the same?")

Notice the block has a shaded area below it — that's the **body zone**. Anything you put in there runs when the condition is true.

3. Expand **Output** in the palette
4. Find the `print({value})` block and drag it **into the if block's body zone**

Fill in `{value}` → `"You got it!"` (include the quotes)

Now add the else:

5. In the **Control** category, find the `else:` block
6. Drag it onto the canvas, just below the if block (not inside it — it should snap next to it)

7. Add another `print` block inside the else body zone

Fill in `{value}` → `"Nope! The number was"`, `secret`

> Note: some print blocks accept multiple values separated by commas. If yours only has one field, you can type `"Nope! The number was", secret` as the whole value.

The full generated Python should now look like:

```python
import random
secret = random.randint(1, 10)
guess_text = input("Guess a number between 1 and 10: ")
guess = int(guess_text)
if guess == secret:
    print("You got it!")
else:
    print("Nope! The number was", secret)
```

---

## Step 6: Run it

Press **F5** or click the Run button.

The console panel at the bottom activates. You'll see the prompt:
```
Guess a number between 1 and 10: 
```

Type a number and press Enter. You'll get either:
```
You got it!
```
or
```
Nope! The number was 7
```

Run it a few times. The number is different every time because `random.randint` picks a new one each run.

---

## What just happened

You just wrote a real Python program. Every concept you used — imports, variables, functions, type conversion, if/else logic — is standard Python. Open the Live Python panel, select all the text, and paste it into a file called `guess.py`. Then run:

```bash
python guess.py
```

It works identically outside of PyBlocks.

---

## Ideas for extending it

Once the basic version works, try extending it:

- **Let them guess more than once** — wrap the input and if/else in a `while` loop that keeps going until they get it right
- **Count the guesses** — create a variable `attempts`, set it to 0, and add 1 inside the loop each time. Print how many guesses it took.
- **Give hints** — instead of just "nope", tell them if their guess was too high or too low. You'll need an `if/elif/else` with two conditions.
- **Bigger range** — change the 10 to 100 and see how the game feels

All of these use blocks you already know how to find in the palette.

---

## Next steps

- Look at the full [Block Reference](block-reference.md) to see everything available
- Open the **Snake** example project to see what a larger program looks like
- Learn about installing new packages in [Package Manager](package-manager.md)
- Build your own reusable blocks in [Custom Blocks](custom-blocks.md)
