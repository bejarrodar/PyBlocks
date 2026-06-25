from pyblocks.blocks.definition import block

# ── Collections Module ───────────────────────────────────────────────────

# Counter

@block(label="{result} = collections.Counter({iterable})", category="Collections", color="#b4befe",
       description="Count the occurrences of each element in an iterable.")
def col_counter(result, iterable):
    return f"{result} = collections.Counter({iterable})"


@block(label="{result} = {c}.most_common({n})", category="Collections", color="#b4befe",
       description="Get the n most common elements and their counts.")
def col_counter_most_common(result, c, n):
    return f"{result} = {c}.most_common({n})"


@block(label="{c}.update({iterable})", category="Collections", color="#b4befe",
       description="Add counts from an iterable to the counter.")
def col_counter_update(c, iterable):
    return f"{c}.update({iterable})"


# Defaultdict

@block(label="{result} = collections.defaultdict({default_factory})", category="Collections", color="#b4befe",
       description="Create a dictionary that returns a default value for missing keys.")
def col_defaultdict(result, default_factory):
    return f"{result} = collections.defaultdict({default_factory})"


# Deque

@block(label="{result} = collections.deque({iterable})", category="Collections", color="#b4befe",
       description="Create a deque (double-ended queue) from an iterable.")
def col_deque(result, iterable):
    return f"{result} = collections.deque({iterable})"


@block(label="{result} = collections.deque({iterable}, maxlen={maxlen})", category="Collections", color="#b4befe",
       description="Create a deque with a maximum length.")
def col_deque_maxlen(result, iterable, maxlen):
    return f"{result} = collections.deque({iterable}, maxlen={maxlen})"


@block(label="{d}.appendleft({item})", category="Collections", color="#b4befe",
       description="Add an item to the left end of a deque.")
def col_appendleft(d, item):
    return f"{d}.appendleft({item})"


@block(label="{result} = {d}.popleft()", category="Collections", color="#b4befe",
       description="Remove and return an item from the left end of a deque.")
def col_popleft(result, d):
    return f"{result} = {d}.popleft()"


@block(label="{d}.rotate({n})", category="Collections", color="#b4befe",
       description="Rotate the deque n steps to the right.")
def col_rotate(d, n):
    return f"{d}.rotate({n})"


# OrderedDict

@block(label="{result} = collections.OrderedDict()", category="Collections", color="#b4befe",
       description="Create an OrderedDict that preserves insertion order.")
def col_ordereddict(result):
    return f"{result} = collections.OrderedDict()"


# Namedtuple

@block(label="{result} = collections.namedtuple({name}, {fields})", category="Collections", color="#b4befe",
       description="Create a named tuple class.")
def col_namedtuple(result, name, fields):
    return f"{result} = collections.namedtuple({name}, {fields})"


# ChainMap

@block(label="{result} = collections.ChainMap({maps})", category="Collections", color="#b4befe",
       description="Combine multiple dicts into a single view.")
def col_chainmap(result, maps):
    return f"{result} = collections.ChainMap({maps})"


# ── Itertools Module ─────────────────────────────────────────────────────

# Chain

@block(label="{result} = list(itertools.chain({iterables}))", category="Itertools", color="#fab387",
       description="Chain multiple iterables together.")
def it_chain(result, iterables):
    return f"{result} = list(itertools.chain({iterables}))"


@block(label="{result} = list(itertools.chain.from_iterable({iterable}))", category="Itertools", color="#fab387",
       description="Flatten one level of nesting.")
def it_chain_from_iterable(result, iterable):
    return f"{result} = list(itertools.chain.from_iterable({iterable}))"


# Cycle

@block(label="{result} = itertools.cycle({iterable})", category="Itertools", color="#fab387",
       description="Cycle through an iterable indefinitely.")
def it_cycle(result, iterable):
    return f"{result} = itertools.cycle({iterable})"


# Repeat

@block(label="{result} = list(itertools.repeat({obj}, {times}))", category="Itertools", color="#fab387",
       description="Repeat an object a given number of times.")
def it_repeat(result, obj, times):
    return f"{result} = list(itertools.repeat({obj}, {times}))"


# Count

@block(label="{result} = itertools.count({start}, {step})", category="Itertools", color="#fab387",
       description="Count up from start by step (infinite iterator).")
def it_count(result, start, step):
    return f"{result} = itertools.count({start}, {step})"


# Combinations

@block(label="{result} = list(itertools.combinations({iterable}, {r}))", category="Itertools", color="#fab387",
       description="Return all r-length combinations of elements.")
def it_combinations(result, iterable, r):
    return f"{result} = list(itertools.combinations({iterable}, {r}))"


@block(label="{result} = list(itertools.combinations_with_replacement({iterable}, {r}))", category="Itertools", color="#fab387",
       description="Return all r-length combinations with replacement of elements.")
def it_combinations_wr(result, iterable, r):
    return f"{result} = list(itertools.combinations_with_replacement({iterable}, {r}))"


# Permutations

@block(label="{result} = list(itertools.permutations({iterable}, {r}))", category="Itertools", color="#fab387",
       description="Return all r-length permutations of elements.")
def it_permutations(result, iterable, r):
    return f"{result} = list(itertools.permutations({iterable}, {r}))"


# Product

@block(label="{result} = list(itertools.product({iterables}))", category="Itertools", color="#fab387",
       description="Cartesian product of iterables.")
def it_product(result, iterables):
    return f"{result} = list(itertools.product({iterables}))"


# Islice

@block(label="{result} = list(itertools.islice({iterable}, {stop}))", category="Itertools", color="#fab387",
       description="Get a slice of an iterable from 0 to stop.")
def it_islice(result, iterable, stop):
    return f"{result} = list(itertools.islice({iterable}, {stop}))"


@block(label="{result} = list(itertools.islice({iterable}, {start}, {stop}))", category="Itertools", color="#fab387",
       description="Get a slice of an iterable from start to stop.")
def it_islice_start(result, iterable, start, stop):
    return f"{result} = list(itertools.islice({iterable}, {start}, {stop}))"


# Zip longest

@block(label="{result} = list(itertools.zip_longest({iterables}))", category="Itertools", color="#fab387",
       description="Zip iterables together, filling missing values with None.")
def it_zip_longest(result, iterables):
    return f"{result} = list(itertools.zip_longest({iterables}))"


# Accumulate

@block(label="{result} = list(itertools.accumulate({iterable}))", category="Itertools", color="#fab387",
       description="Compute running totals.")
def it_accumulate(result, iterable):
    return f"{result} = list(itertools.accumulate({iterable}))"


# Groupby

@block(label="{result} = itertools.groupby({iterable}, {key})", category="Itertools", color="#fab387",
       description="Group consecutive elements by a key function.")
def it_groupby(result, iterable, key):
    return f"{result} = itertools.groupby({iterable}, {key})"


# Takewhile

@block(label="{result} = list(itertools.takewhile({predicate}, {iterable}))", category="Itertools", color="#fab387",
       description="Take elements while predicate is True.")
def it_takewhile(result, predicate, iterable):
    return f"{result} = list(itertools.takewhile({predicate}, {iterable}))"


# Dropwhile

@block(label="{result} = list(itertools.dropwhile({predicate}, {iterable}))", category="Itertools", color="#fab387",
       description="Drop elements while predicate is True.")
def it_dropwhile(result, predicate, iterable):
    return f"{result} = list(itertools.dropwhile({predicate}, {iterable}))"


# Filterfalse

@block(label="{result} = list(itertools.filterfalse({predicate}, {iterable}))", category="Itertools", color="#fab387",
       description="Keep elements where predicate is False.")
def it_filterfalse(result, predicate, iterable):
    return f"{result} = list(itertools.filterfalse({predicate}, {iterable}))"


# Starmap

@block(label="{result} = list(itertools.starmap({func}, {iterable}))", category="Itertools", color="#fab387",
       description="Apply a function to arguments unpacked from tuples in an iterable.")
def it_starmap(result, func, iterable):
    return f"{result} = list(itertools.starmap({func}, {iterable}))"


# ── Functools Module ────────────────────────────────────────────────────

# Reduce

@block(label="{result} = functools.reduce({func}, {iterable})", category="Functools", color="#f9e2af",
       description="Apply a function cumulatively to reduce an iterable to a single value.")
def fn_reduce(result, func, iterable):
    return f"{result} = functools.reduce({func}, {iterable})"


@block(label="{result} = functools.reduce({func}, {iterable}, {initializer})", category="Functools", color="#f9e2af",
       description="Apply a function cumulatively with an initial value.")
def fn_reduce_init(result, func, iterable, initializer):
    return f"{result} = functools.reduce({func}, {iterable}, {initializer})"


# Partial

@block(label="{result} = functools.partial({func}, {args})", category="Functools", color="#f9e2af",
       description="Create a new function with some arguments pre-filled.")
def fn_partial(result, func, args):
    return f"{result} = functools.partial({func}, {args})"


# LRU Cache

@block(label="@functools.lru_cache(maxsize={n})", category="Functools", color="#f9e2af",
       description="Cache the results of a function (decorator).")
def fn_lru_cache(n):
    return f"@functools.lru_cache(maxsize={n})"


# Cache

@block(label="@functools.cache", category="Functools", color="#f9e2af",
       description="Unlimited cache for function results (decorator).")
def fn_cache():
    return "@functools.cache"


# Wraps

@block(label="@functools.wraps({wrapped})", category="Functools", color="#f9e2af",
       description="Preserve function metadata when writing decorators.")
def fn_wraps(wrapped):
    return f"@functools.wraps({wrapped})"


# Total ordering

@block(label="@functools.total_ordering", category="Functools", color="#f9e2af",
       description="Fill in missing comparison methods from __eq__ and one other.")
def fn_total_ordering():
    return "@functools.total_ordering"


# Cmp to key

@block(label="{result} = functools.cmp_to_key({func})", category="Functools", color="#f9e2af",
       description="Convert a comparison function to a key function for sorting.")
def fn_cmp_to_key(result, func):
    return f"{result} = functools.cmp_to_key({func})"
