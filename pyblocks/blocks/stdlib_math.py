from pyblocks.blocks.definition import block

# ── Math Module ──────────────────────────────────────────────────────────

# Basic Operations

@block(label="{result} = math.sqrt({x})", category="Math", color="#f9e2af",
       description="Return the square root of a number.")
def mth_sqrt(result, x):
    return f"{result} = math.sqrt({x})"


@block(label="{result} = math.fabs({x})", category="Math", color="#f9e2af",
       description="Return the absolute value of a number as a float.")
def mth_fabs(result, x):
    return f"{result} = math.fabs({x})"


@block(label="{result} = math.hypot({x}, {y})", category="Math", color="#f9e2af",
       description="Return the Euclidean distance, sqrt(x*x + y*y).")
def mth_hypot(result, x, y):
    return f"{result} = math.hypot({x}, {y})"


# Rounding

@block(label="{result} = math.floor({x})", category="Math", color="#f9e2af",
       description="Return the floor of a number (largest integer <= x).")
def mth_floor(result, x):
    return f"{result} = math.floor({x})"


@block(label="{result} = math.ceil({x})", category="Math", color="#f9e2af",
       description="Return the ceiling of a number (smallest integer >= x).")
def mth_ceil(result, x):
    return f"{result} = math.ceil({x})"


@block(label="{result} = math.trunc({x})", category="Math", color="#f9e2af",
       description="Return the integer part of a number (truncate towards zero).")
def mth_trunc(result, x):
    return f"{result} = math.trunc({x})"


# Trigonometric Functions

@block(label="{result} = math.sin({x})", category="Math", color="#f9e2af",
       description="Return the sine of x (x is in radians).")
def mth_sin(result, x):
    return f"{result} = math.sin({x})"


@block(label="{result} = math.cos({x})", category="Math", color="#f9e2af",
       description="Return the cosine of x (x is in radians).")
def mth_cos(result, x):
    return f"{result} = math.cos({x})"


@block(label="{result} = math.tan({x})", category="Math", color="#f9e2af",
       description="Return the tangent of x (x is in radians).")
def mth_tan(result, x):
    return f"{result} = math.tan({x})"


# Inverse Trigonometric Functions

@block(label="{result} = math.asin({x})", category="Math", color="#f9e2af",
       description="Return the arc sine of x in radians.")
def mth_asin(result, x):
    return f"{result} = math.asin({x})"


@block(label="{result} = math.acos({x})", category="Math", color="#f9e2af",
       description="Return the arc cosine of x in radians.")
def mth_acos(result, x):
    return f"{result} = math.acos({x})"


@block(label="{result} = math.atan({x})", category="Math", color="#f9e2af",
       description="Return the arc tangent of x in radians.")
def mth_atan(result, x):
    return f"{result} = math.atan({x})"


@block(label="{result} = math.atan2({y}, {x})", category="Math", color="#f9e2af",
       description="Return the arc tangent of y/x in radians.")
def mth_atan2(result, y, x):
    return f"{result} = math.atan2({y}, {x})"


# Angle Conversion

@block(label="{result} = math.degrees({x})", category="Math", color="#f9e2af",
       description="Convert angle from radians to degrees.")
def mth_degrees(result, x):
    return f"{result} = math.degrees({x})"


@block(label="{result} = math.radians({x})", category="Math", color="#f9e2af",
       description="Convert angle from degrees to radians.")
def mth_radians(result, x):
    return f"{result} = math.radians({x})"


# Exponential and Logarithmic Functions

@block(label="{result} = math.exp({x})", category="Math", color="#f9e2af",
       description="Return e raised to the power of x.")
def mth_exp(result, x):
    return f"{result} = math.exp({x})"


@block(label="{result} = math.log({x})", category="Math", color="#f9e2af",
       description="Return the natural logarithm of x.")
def mth_log(result, x):
    return f"{result} = math.log({x})"


@block(label="{result} = math.log2({x})", category="Math", color="#f9e2af",
       description="Return the base-2 logarithm of x.")
def mth_log2(result, x):
    return f"{result} = math.log2({x})"


@block(label="{result} = math.log10({x})", category="Math", color="#f9e2af",
       description="Return the base-10 logarithm of x.")
def mth_log10(result, x):
    return f"{result} = math.log10({x})"


# Combinatorics and Number Theory

@block(label="{result} = math.factorial({n})", category="Math", color="#f9e2af",
       description="Return the factorial of n.")
def mth_factorial(result, n):
    return f"{result} = math.factorial({n})"


@block(label="{result} = math.gcd({a}, {b})", category="Math", color="#f9e2af",
       description="Return the greatest common divisor of a and b.")
def mth_gcd(result, a, b):
    return f"{result} = math.gcd({a}, {b})"


@block(label="{result} = math.lcm({a}, {b})", category="Math", color="#f9e2af",
       description="Return the least common multiple of a and b.")
def mth_lcm(result, a, b):
    return f"{result} = math.lcm({a}, {b})"


@block(label="{result} = math.comb({n}, {k})", category="Math", color="#f9e2af",
       description="Return the number of ways to choose k items from n items (combinations).")
def mth_comb(result, n, k):
    return f"{result} = math.comb({n}, {k})"


@block(label="{result} = math.perm({n}, {k})", category="Math", color="#f9e2af",
       description="Return the number of ways to arrange k items from n items (permutations).")
def mth_perm(result, n, k):
    return f"{result} = math.perm({n}, {k})"


# Special Value Checks

@block(label="{result} = math.isnan({x})", category="Math", color="#f9e2af",
       description="Check if x is NaN (not a number).")
def mth_isnan(result, x):
    return f"{result} = math.isnan({x})"


@block(label="{result} = math.isinf({x})", category="Math", color="#f9e2af",
       description="Check if x is infinity.")
def mth_isinf(result, x):
    return f"{result} = math.isinf({x})"


@block(label="{result} = math.isfinite({x})", category="Math", color="#f9e2af",
       description="Check if x is finite (not infinity and not NaN).")
def mth_isfinite(result, x):
    return f"{result} = math.isfinite({x})"


# Mathematical Constants

@block(label="{name} = math.pi", category="Math", color="#f9e2af",
       description="Assign the mathematical constant pi (π) to a variable.")
def mth_pi(name):
    return f"{name} = math.pi"


@block(label="{name} = math.e", category="Math", color="#f9e2af",
       description="Assign the mathematical constant e (Euler's number) to a variable.")
def mth_e(name):
    return f"{name} = math.e"


@block(label="{name} = math.tau", category="Math", color="#f9e2af",
       description="Assign the mathematical constant tau (2π) to a variable.")
def mth_tau(name):
    return f"{name} = math.tau"


@block(label="{name} = math.inf", category="Math", color="#f9e2af",
       description="Assign positive infinity to a variable.")
def mth_inf(name):
    return f"{name} = math.inf"


@block(label="{name} = math.nan", category="Math", color="#f9e2af",
       description="Assign NaN (not a number) to a variable.")
def mth_nan(name):
    return f"{name} = math.nan"


# ── Random Module ────────────────────────────────────────────────────────

# Generating Random Numbers

@block(label="{result} = random.random()", category="Random", color="#fab387",
       description="Return a random float between 0.0 and 1.0.")
def rnd_random(result):
    return f"{result} = random.random()"


@block(label="{result} = random.uniform({a}, {b})", category="Random", color="#fab387",
       description="Return a random float between a and b (inclusive).")
def rnd_uniform(result, a, b):
    return f"{result} = random.uniform({a}, {b})"


@block(label="{result} = random.randint({a}, {b})", category="Random", color="#fab387",
       description="Return a random integer between a and b (inclusive).")
def rnd_randint(result, a, b):
    return f"{result} = random.randint({a}, {b})"


@block(label="{result} = random.randrange({start}, {stop})", category="Random", color="#fab387",
       description="Return a random integer from start to stop-1.")
def rnd_randrange(result, start, stop):
    return f"{result} = random.randrange({start}, {stop})"


@block(label="{result} = random.gauss({mu}, {sigma})", category="Random", color="#fab387",
       description="Return a random number from a Gaussian (normal) distribution with mean mu and standard deviation sigma.")
def rnd_gauss(result, mu, sigma):
    return f"{result} = random.gauss({mu}, {sigma})"


# Sequence Operations

@block(label="{result} = random.choice({seq})", category="Random", color="#fab387",
       description="Return a random element from the sequence.")
def rnd_choice(result, seq):
    return f"{result} = random.choice({seq})"


@block(label="{result} = random.choices({seq}, k={k})", category="Random", color="#fab387",
       description="Return a list of k random elements from the sequence (with replacement).")
def rnd_choices(result, seq, k):
    return f"{result} = random.choices({seq}, k={k})"


@block(label="{result} = random.sample({seq}, {k})", category="Random", color="#fab387",
       description="Return a list of k unique random elements from the sequence (without replacement).")
def rnd_sample(result, seq, k):
    return f"{result} = random.sample({seq}, {k})"


@block(label="random.shuffle({lst})", category="Random", color="#fab387",
       description="Shuffle a list in place (modify the original list).")
def rnd_shuffle(lst):
    return f"random.shuffle({lst})"


# Seeding and State

@block(label="random.seed({n})", category="Random", color="#fab387",
       description="Set the random seed to n for reproducible random numbers.")
def rnd_seed(n):
    return f"random.seed({n})"


# ── Statistics Module ────────────────────────────────────────────────────

# Central Tendency

@block(label="{result} = statistics.mean({data})", category="Statistics", color="#f9e2af",
       description="Return the arithmetic mean of data.")
def sta_mean(result, data):
    return f"{result} = statistics.mean({data})"


@block(label="{result} = statistics.median({data})", category="Statistics", color="#f9e2af",
       description="Return the median (middle value) of data.")
def sta_median(result, data):
    return f"{result} = statistics.median({data})"


@block(label="{result} = statistics.median_high({data})", category="Statistics", color="#f9e2af",
       description="Return the high median (upper of two middle values) of data.")
def sta_median_high(result, data):
    return f"{result} = statistics.median_high({data})"


@block(label="{result} = statistics.median_low({data})", category="Statistics", color="#f9e2af",
       description="Return the low median (lower of two middle values) of data.")
def sta_median_low(result, data):
    return f"{result} = statistics.median_low({data})"


@block(label="{result} = statistics.mode({data})", category="Statistics", color="#f9e2af",
       description="Return the mode (most common value) of data.")
def sta_mode(result, data):
    return f"{result} = statistics.mode({data})"


@block(label="{result} = statistics.multimode({data})", category="Statistics", color="#f9e2af",
       description="Return a list of modes (all most common values) in data.")
def sta_multimode(result, data):
    return f"{result} = statistics.multimode({data})"


@block(label="{result} = statistics.fmean({data})", category="Statistics", color="#f9e2af",
       description="Return the fast arithmetic mean of data (as float).")
def sta_fmean(result, data):
    return f"{result} = statistics.fmean({data})"


@block(label="{result} = statistics.geometric_mean({data})", category="Statistics", color="#f9e2af",
       description="Return the geometric mean of data.")
def sta_geometric_mean(result, data):
    return f"{result} = statistics.geometric_mean({data})"


@block(label="{result} = statistics.harmonic_mean({data})", category="Statistics", color="#f9e2af",
       description="Return the harmonic mean of data.")
def sta_harmonic_mean(result, data):
    return f"{result} = statistics.harmonic_mean({data})"


# Dispersion

@block(label="{result} = statistics.stdev({data})", category="Statistics", color="#f9e2af",
       description="Return the sample standard deviation of data.")
def sta_stdev(result, data):
    return f"{result} = statistics.stdev({data})"


@block(label="{result} = statistics.pstdev({data})", category="Statistics", color="#f9e2af",
       description="Return the population standard deviation of data.")
def sta_pstdev(result, data):
    return f"{result} = statistics.pstdev({data})"


@block(label="{result} = statistics.variance({data})", category="Statistics", color="#f9e2af",
       description="Return the sample variance of data.")
def sta_variance(result, data):
    return f"{result} = statistics.variance({data})"


@block(label="{result} = statistics.pvariance({data})", category="Statistics", color="#f9e2af",
       description="Return the population variance of data.")
def sta_pvariance(result, data):
    return f"{result} = statistics.pvariance({data})"
