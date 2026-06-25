# Block Reference

PyBlocks ships with **408 blocks** across 30+ categories. This page lists every category and describes what's in it. The blocks are split into two groups: **Built-ins** (149 blocks) cover core Python operations, and **Standard Library** (259 blocks) cover Python's built-in modules.

---

## How to read this reference

Each block in the palette has a **label** that shows its template. Words in `{curly braces}` are input fields you fill in. For example:

```
{result} = random.randint({a}, {b})
```

means: put the output variable name in `{result}`, the low end of the range in `{a}`, and the high end in `{b}`. If you fill in `n`, `1`, `10` you get `n = random.randint(1, 10)`.

---

## Built-in blocks

These cover the core Python language — no imports needed.

### Output

Printing things to the console.

| Block label | What it does |
|---|---|
| `print({value})` | Print a value |
| `print({value}, sep={sep})` | Print with a custom separator |
| `print({value}, end={end})` | Print with a custom ending (default is newline) |
| `print(f"{text}")` | Print an f-string (embed variables directly in text) |

### Variables

Creating and updating variables.

| Block label | What it does |
|---|---|
| `{name} = {value}` | Assign a value to a variable |
| `{name} += {value}` | Add to a variable (e.g. score += 1) |
| `{name} -= {value}` | Subtract from a variable |
| `{name} *= {value}` | Multiply a variable |
| `{name} /= {value}` | Divide a variable |
| `global {name}` | Declare a variable as global inside a function |
| `{name} = None` | Set a variable to nothing |
| `__name__ == "__main__"` | The standard "run as script" guard |

### Control

Logic and flow control — the backbone of any program.

| Block label | What it does |
|---|---|
| `if {condition}:` | Run the body if condition is true |
| `elif {condition}:` | Alternative condition (chain after if) |
| `else:` | Run the body if no earlier condition was true |
| `for {var} in {iterable}:` | Loop over each item in a list, range, etc. |
| `while {condition}:` | Keep looping while condition is true |
| `break` | Exit the current loop immediately |
| `continue` | Skip to the next loop iteration |
| `pass` | Do nothing (placeholder for empty blocks) |
| `match {expr}:` | Start a match/case statement (Python 3.10+) |
| `case {pattern}:` | A case inside a match |
| `case _:` | The default/wildcard case |
| `with {expr} as {var}:` | Context manager (used for opening files) |

### Functions & Classes

Defining reusable code.

| Block label | What it does |
|---|---|
| `def {name}({params}):` | Define a function |
| `return {value}` | Return a value from a function |
| `yield {value}` | Yield a value from a generator |
| `lambda {params}: {expr}` | Create an anonymous function |
| `class {name}:` | Define a class |
| `class {name}({parent}):` | Define a class that inherits from another |
| `@{name}` | Apply a decorator |
| `@{name}({args})` | Apply a decorator with arguments |

### Error Handling

Catching and handling errors.

| Block label | What it does |
|---|---|
| `try:` | Start a try block |
| `except {error}:` | Catch a specific error type |
| `except {error} as {e}:` | Catch an error and name it |
| `except:` | Catch any error |
| `finally:` | Always run this, error or not |
| `raise {error}` | Throw an error |
| `raise {error}({msg})` | Throw an error with a message |
| `assert {condition}` | Crash if condition is false |
| `assert {condition}, {msg}` | Crash with a message if false |

### Imports

Loading Python modules.

| Block label | What it does |
|---|---|
| `import {module}` | Import a module |
| `from {module} import {name}` | Import one thing from a module |
| `import {module} as {alias}` | Import with a shorter name |
| `from {module} import *` | Import everything from a module |

### I/O

Reading and writing files.

| Block label | What it does |
|---|---|
| `{result} = input({prompt})` | Ask the user to type something |
| `{result} = open({path}, {mode})` | Open a file |
| `{result} = {f}.read()` | Read the entire file contents |
| `{result} = {f}.readline()` | Read one line |
| `{result} = {f}.readlines()` | Read all lines into a list |
| `{f}.write({text})` | Write text to a file |
| `{f}.close()` | Close a file |

### Type Casting

Converting between types.

| Block label | What it does |
|---|---|
| `{result} = int({value})` | Convert to integer |
| `{result} = float({value})` | Convert to decimal number |
| `{result} = str({value})` | Convert to string/text |
| `{result} = bool({value})` | Convert to True/False |
| `{result} = list({value})` | Convert to list |
| `{result} = tuple({value})` | Convert to tuple |
| `{result} = set({value})` | Convert to set |
| `{result} = dict({value})` | Convert to dictionary |
| `{result} = bytes({value})` | Convert to bytes |
| `{result} = chr({value})` | Integer to character (65 → 'A') |
| `{result} = ord({value})` | Character to integer ('A' → 65) |
| `{result} = bin({value})` | Integer to binary string |
| `{result} = hex({value})` | Integer to hex string |

### Math

Basic math operations.

| Block label | What it does |
|---|---|
| `{result} = abs({value})` | Absolute value |
| `{result} = round({value}, {ndigits})` | Round to N decimal places |
| `{result} = pow({base}, {exp})` | Raise to a power |
| `{result} = divmod({a}, {b})` | Division and remainder together |
| `{result} = min({iterable})` | Smallest value |
| `{result} = max({iterable})` | Largest value |
| `{result} = sum({iterable})` | Sum all values |

### Sequences

Operations that work on lists, strings, tuples, or any ordered collection.

| Block label | What it does |
|---|---|
| `{result} = len({seq})` | Count items |
| `{result} = range({stop})` | Numbers from 0 to stop-1 |
| `{result} = range({start}, {stop})` | Numbers from start to stop-1 |
| `{result} = range({start}, {stop}, {step})` | With a step size |
| `{result} = {seq}[{index}]` | Get item at index |
| `{result} = {seq}[{start}:{stop}]` | Get a slice |
| `{result} = sorted({iterable})` | Return a sorted copy |
| `{result} = reversed({iterable})` | Return in reverse order |
| `{result} = enumerate({iterable})` | Loop with index and value |
| `{result} = zip({a}, {b})` | Pair up two iterables |
| `{result} = map({func}, {iterable})` | Apply a function to every item |
| `{result} = filter({func}, {iterable})` | Keep items where function is true |
| `{result} = any({iterable})` | True if at least one item is truthy |
| `{result} = all({iterable})` | True if every item is truthy |

### Lists

Creating and modifying lists.

| Block label | What it does |
|---|---|
| `{name} = []` | Create an empty list |
| `{name} = [{values}]` | Create a list with initial values |
| `{name}.append({value})` | Add to the end |
| `{name}.insert({index}, {value})` | Add at a position |
| `{name}.pop({index})` | Remove and return item at index |
| `{name}.remove({value})` | Remove first occurrence of a value |
| `{name}.extend({other})` | Add all items from another list |
| `{name}.sort()` | Sort in place |
| `{name}.reverse()` | Reverse in place |
| `{name}.clear()` | Remove all items |
| `{result} = {name}.index({value})` | Find the index of a value |
| `{result} = {name}.count({value})` | Count occurrences |
| `{result} = {name}.copy()` | Make a copy |

### Dictionaries

Creating and working with key-value pairs.

| Block label | What it does |
|---|---|
| `{name} = dict()` | Create an empty dictionary |
| `{name}[{key}] = {value}` | Set a key |
| `{result} = {name}[{key}]` | Get a value by key |
| `{result} = {name}.get({key}, {default})` | Get with a fallback |
| `del {name}[{key}]` | Delete a key |
| `{result} = {name}.keys()` | Get all keys |
| `{result} = {name}.values()` | Get all values |
| `{result} = {name}.items()` | Get all key-value pairs |
| `{name}.update({other})` | Merge in another dictionary |

### Sets

Unordered collections of unique values.

| Block label | What it does |
|---|---|
| `{name} = set()` | Create an empty set |
| `{name}.add({value})` | Add a value |
| `{name}.remove({value})` | Remove a value |
| `{result} = {a} \| {b}` | Union (everything in either) |
| `{result} = {a} & {b}` | Intersection (only in both) |
| `{result} = {a} - {b}` | Difference (in a but not b) |

### Inspection

Finding out information about objects and variables.

| Block label | What it does |
|---|---|
| `{result} = type({value})` | What type is this? |
| `{result} = isinstance({obj}, {classinfo})` | Is this an instance of a type? |
| `{result} = callable({obj})` | Is this something you can call? |
| `{result} = hasattr({obj}, {name})` | Does this object have this attribute? |
| `{result} = getattr({obj}, {name})` | Get an attribute by name |
| `{result} = dir({obj})` | List all attributes and methods |

### Iteration

Manual control of iterators.

| Block label | What it does |
|---|---|
| `{result} = iter({obj})` | Get an iterator from an object |
| `{result} = next({iterator})` | Get the next value from an iterator |
| `{result} = next({iterator}, {default})` | Next with a fallback when done |

### Advanced

Less common operations for more complex programs.

| Block label | What it does |
|---|---|
| `{result} = eval({expr})` | Evaluate a string as Python |
| `exec({code})` | Execute a string as Python statements |
| `breakpoint()` | Pause and open the Python debugger |
| `{result} = super()` | Call the parent class |
| `{name} = property({fget})` | Define a property |
| `{name} = staticmethod({func})` | Wrap as a static method |
| `{name} = classmethod({func})` | Wrap as a class method |

---

## Standard library blocks

These cover Python's built-in modules. Most require an `import` block at the top of your program — the category name tells you which module to import.

### Strings (import: none — these are methods on string variables)

34 blocks covering string operations. A few highlights:

| Block label | What it does |
|---|---|
| `{result} = {s}.split({sep})` | Split into a list |
| `{result} = {sep}.join({iterable})` | Join a list into a string |
| `{result} = {s}.strip()` | Remove leading/trailing whitespace |
| `{result} = {s}.replace({old}, {new})` | Replace all occurrences |
| `{result} = {s}.upper()` | Convert to uppercase |
| `{result} = {s}.lower()` | Convert to lowercase |
| `{result} = {s}.startswith({prefix})` | Does it start with this? |
| `{result} = {s}.format({args})` | Format a string |
| `{result} = {s}.find({sub})` | Find index of substring |

### Math (import: `math`)

32 blocks covering mathematical functions. Highlights:

| Block label | What it does |
|---|---|
| `{result} = math.sqrt({x})` | Square root |
| `{result} = math.floor({x})` | Round down |
| `{result} = math.ceil({x})` | Round up |
| `{result} = math.sin({x})` | Sine (in radians) |
| `{result} = math.log({x})` | Natural logarithm |
| `{result} = math.factorial({n})` | Factorial (5! = 120) |
| `{result} = math.pi` | The constant π (3.14159…) |
| `{result} = math.e` | Euler's number (2.71828…) |

### Random (import: `random`)

10 blocks for generating random values.

| Block label | What it does |
|---|---|
| `{result} = random.random()` | Random float between 0.0 and 1.0 |
| `{result} = random.randint({a}, {b})` | Random integer between a and b |
| `{result} = random.choice({seq})` | Random item from a list |
| `{result} = random.shuffle({seq})` | Shuffle a list in place |
| `{result} = random.sample({seq}, {k})` | k random items without repeats |

### Statistics (import: `statistics`)

13 blocks for statistical calculations.

| Block label | What it does |
|---|---|
| `{result} = statistics.mean({data})` | Average |
| `{result} = statistics.median({data})` | Middle value |
| `{result} = statistics.mode({data})` | Most common value |
| `{result} = statistics.stdev({data})` | Standard deviation |
| `{result} = statistics.variance({data})` | Variance |

### Time (import: `time`)

10 blocks for time operations.

| Block label | What it does |
|---|---|
| `time.sleep({seconds})` | Pause for a number of seconds |
| `{result} = time.time()` | Current time as seconds since 1970 |
| `{result} = time.monotonic()` | High-precision timer (for measuring elapsed time) |
| `{result} = time.perf_counter()` | High-resolution performance counter |
| `{result} = time.strftime({fmt}, {t})` | Format a time as a string |

### DateTime (import: `datetime`)

18 blocks for working with dates and times.

| Block label | What it does |
|---|---|
| `{result} = datetime.datetime.now()` | Current date and time |
| `{result} = datetime.date.today()` | Today's date |
| `{result} = datetime.timedelta(...)` | A duration (e.g. 3 days, 2 hours) |
| `{result} = {dt}.strftime({fmt})` | Format a datetime as a string |
| `{result} = {dt}.year` / `.month` / `.day` | Extract parts |

### JSON (import: `json`)

6 blocks for reading and writing JSON data.

| Block label | What it does |
|---|---|
| `{result} = json.loads({s})` | Parse a JSON string |
| `{result} = json.dumps({obj})` | Convert to JSON string |
| `{result} = json.load({f})` | Read JSON from a file |
| `json.dump({obj}, {f})` | Write JSON to a file |

### OS (import: `os`)

10 blocks for working with the operating system.

| Block label | What it does |
|---|---|
| `{result} = os.getcwd()` | Current working directory |
| `{result} = os.listdir({path})` | List files in a directory |
| `os.makedirs({path}, exist_ok=True)` | Create a directory (and parents) |
| `os.remove({path})` | Delete a file |
| `{result} = os.getenv({key})` | Read an environment variable |

### OS Path (import: `os`)

10 blocks for file path operations.

| Block label | What it does |
|---|---|
| `{result} = os.path.join({a}, {b})` | Build a file path safely |
| `{result} = os.path.exists({path})` | Does this path exist? |
| `{result} = os.path.isfile({path})` | Is it a file? |
| `{result} = os.path.isdir({path})` | Is it a directory? |
| `{result} = os.path.basename({path})` | Get the filename part |
| `{result} = os.path.dirname({path})` | Get the directory part |

### Pathlib (import: `pathlib`)

19 blocks for modern file path handling.

| Block label | What it does |
|---|---|
| `{result} = pathlib.Path({s})` | Create a Path from a string |
| `{result} = pathlib.Path.home()` | Your home directory |
| `{result} = {p}.read_text()` | Read a file as text |
| `{p}.write_text({text})` | Write text to a file |
| `{result} = list({p}.iterdir())` | List directory contents |
| `{result} = list({p}.glob({pattern}))` | Find files by pattern |
| `{result} = {p} / {other}` | Join paths with the / operator |

### Collections (import: `collections`)

12 blocks for advanced container types.

| Block label | What it does |
|---|---|
| `{result} = collections.Counter({iterable})` | Count occurrences of each item |
| `{result} = {c}.most_common({n})` | Top N most frequent items |
| `{result} = collections.defaultdict({default_factory})` | Dictionary with automatic defaults |
| `{result} = collections.deque({iterable})` | Double-ended queue |
| `{result} = collections.namedtuple({name}, {fields})` | Tuple with named fields |

### Itertools (import: `itertools`)

18 blocks for advanced iteration.

| Block label | What it does |
|---|---|
| `{result} = list(itertools.chain({iterables}))` | Flatten multiple iterables |
| `{result} = list(itertools.combinations({iterable}, {r}))` | All combinations of r items |
| `{result} = list(itertools.permutations({iterable}, {r}))` | All orderings of r items |
| `{result} = list(itertools.product({iterables}))` | Cartesian product |
| `{result} = itertools.groupby({iterable}, {key})` | Group by a key function |

### Functools (import: `functools`)

8 blocks for function tools.

| Block label | What it does |
|---|---|
| `{result} = functools.reduce({func}, {iterable})` | Cumulatively apply a function |
| `{result} = functools.partial({func}, {args})` | Pre-fill some arguments |
| `@functools.lru_cache(maxsize={n})` | Cache function results |
| `@functools.wraps({wrapped})` | Preserve metadata in decorators |

### Regex (import: `re`)

12 blocks for pattern matching in text.

| Block label | What it does |
|---|---|
| `{result} = re.match({pattern}, {s})` | Match at the start of the string |
| `{result} = re.search({pattern}, {s})` | Find pattern anywhere |
| `{result} = re.findall({pattern}, {s})` | Find all matches |
| `{result} = re.sub({pattern}, {repl}, {s})` | Replace matches |
| `{result} = re.split({pattern}, {s})` | Split by pattern |

### Sys (import: `sys`)

10 blocks for system-level operations.

| Block label | What it does |
|---|---|
| `{result} = sys.argv` | Command-line arguments |
| `sys.exit({code})` | Exit the program |
| `{result} = sys.version` | Python version string |
| `{result} = sys.platform` | Operating system name |

### Logging (import: `logging`)

9 blocks for structured logging.

| Block label | What it does |
|---|---|
| `logging.basicConfig(level={level})` | Set up logging |
| `logging.debug({msg})` | Log a debug message |
| `logging.info({msg})` | Log an info message |
| `logging.warning({msg})` | Log a warning |
| `logging.error({msg})` | Log an error |

### CSV (import: `csv`)

7 blocks for reading and writing CSV files.

| Block label | What it does |
|---|---|
| `{result} = csv.reader({f})` | Read CSV rows |
| `{result} = csv.writer({f})` | Write CSV rows |
| `{result} = csv.DictReader({f})` | Read rows as dictionaries |
| `{w}.writerow({row})` | Write one row |

### Threading (import: `threading`)

9 blocks for running code in parallel.

| Block label | What it does |
|---|---|
| `{result} = threading.Thread(target={target})` | Create a thread |
| `{t}.start()` | Start a thread |
| `{t}.join()` | Wait for a thread to finish |
| `{result} = threading.Lock()` | Create a lock |

### Subprocess (import: `subprocess`)

7 blocks for running external programs.

| Block label | What it does |
|---|---|
| `{result} = subprocess.run({args})` | Run a command |
| `{result} = subprocess.run({args}, capture_output=True, text=True)` | Run and capture output |
| `{result} = subprocess.check_output({args}, text=True)` | Get output as string |
| `{result} = subprocess.Popen({args})` | Start a process |

### Copy (import: `copy`)

2 blocks for copying objects.

| Block label | What it does |
|---|---|
| `{result} = copy.copy({obj})` | Shallow copy |
| `{result} = copy.deepcopy({obj})` | Deep copy (copies nested objects too) |

---

## Adding more blocks

Beyond the 408 built-in blocks, you can add more through:

- **Package Manager** — install any pip package and its functions become blocks automatically
- **Expansion packs** — drop a Python file with `@block` decorators into `expansions/`
- **Block Editor** — build custom blocks in-app with a GUI

See [Package Manager](package-manager.md) and [Custom Blocks](custom-blocks.md) for details.
