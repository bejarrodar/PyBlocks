from pyblocks.blocks.definition import block

# ── RE Module ────────────────────────────────────────────────────────────

@block(label="{result} = re.compile({pattern})", category="Regex", color="#eba0ac")
def rx_compile(result, pattern):
    return f"{result} = re.compile({pattern})"


@block(label="{result} = re.compile({pattern}, {flags})", category="Regex", color="#eba0ac")
def rx_compile_flags(result, pattern, flags):
    return f"{result} = re.compile({pattern}, {flags})"


@block(label="{result} = re.match({pattern}, {s})", category="Regex", color="#eba0ac",
       description="Match pattern at the start of the string.")
def rx_match(result, pattern, s):
    return f"{result} = re.match({pattern}, {s})"


@block(label="{result} = re.search({pattern}, {s})", category="Regex", color="#eba0ac",
       description="Search for pattern anywhere in the string.")
def rx_search(result, pattern, s):
    return f"{result} = re.search({pattern}, {s})"


@block(label="{result} = re.fullmatch({pattern}, {s})", category="Regex", color="#eba0ac",
       description="Match pattern against the entire string.")
def rx_fullmatch(result, pattern, s):
    return f"{result} = re.fullmatch({pattern}, {s})"


@block(label="{result} = re.findall({pattern}, {s})", category="Regex", color="#eba0ac",
       description="Find all non-overlapping matches.")
def rx_findall(result, pattern, s):
    return f"{result} = re.findall({pattern}, {s})"


@block(label="{result} = re.finditer({pattern}, {s})", category="Regex", color="#eba0ac",
       description="Find all matches as an iterator of match objects.")
def rx_finditer(result, pattern, s):
    return f"{result} = re.finditer({pattern}, {s})"


@block(label="{result} = re.sub({pattern}, {repl}, {s})", category="Regex", color="#eba0ac",
       description="Replace matches with a replacement string.")
def rx_sub(result, pattern, repl, s):
    return f"{result} = re.sub({pattern}, {repl}, {s})"


@block(label="{result} = re.subn({pattern}, {repl}, {s})", category="Regex", color="#eba0ac",
       description="Replace matches and return (new_string, count).")
def rx_subn(result, pattern, repl, s):
    return f"{result} = re.subn({pattern}, {repl}, {s})"


@block(label="{result} = re.split({pattern}, {s})", category="Regex", color="#eba0ac",
       description="Split string by the pattern.")
def rx_split(result, pattern, s):
    return f"{result} = re.split({pattern}, {s})"


@block(label="{result} = {m}.group()", category="Regex", color="#eba0ac",
       description="Get the matched string from a match object.")
def rx_group(result, m):
    return f"{result} = {m}.group()"


@block(label="{result} = {m}.groups()", category="Regex", color="#eba0ac",
       description="Get all captured groups from a match object.")
def rx_groups(result, m):
    return f"{result} = {m}.groups()"


# ── SYS Module ───────────────────────────────────────────────────────────

@block(label="{result} = sys.argv", category="Sys", color="#7f849c",
       description="Get command-line arguments as a list.")
def sy_argv(result):
    return f"{result} = sys.argv"


@block(label="{result} = sys.argv[{i}]", category="Sys", color="#7f849c")
def sy_argv_item(result, i):
    return f"{result} = sys.argv[{i}]"


@block(label="sys.exit({code})", category="Sys", color="#7f849c")
def sy_exit(code):
    return f"sys.exit({code})"


@block(label="{result} = sys.version", category="Sys", color="#7f849c")
def sy_version(result):
    return f"{result} = sys.version"


@block(label="{result} = sys.platform", category="Sys", color="#7f849c")
def sy_platform(result):
    return f"{result} = sys.platform"


@block(label="sys.path.append({p})", category="Sys", color="#7f849c",
       description="Add a directory to the module search path.")
def sy_path_append(p):
    return f"sys.path.append({p})"


@block(label="{result} = sys.stdin.read()", category="Sys", color="#7f849c")
def sy_stdin_read(result):
    return f"{result} = sys.stdin.read()"


@block(label="sys.stdout.write({s})", category="Sys", color="#7f849c")
def sy_stdout_write(s):
    return f"sys.stdout.write({s})"


@block(label="sys.stderr.write({s})", category="Sys", color="#7f849c")
def sy_stderr_write(s):
    return f"sys.stderr.write({s})"


@block(label="{result} = sys.maxsize", category="Sys", color="#7f849c",
       description="Get the maximum integer value.")
def sy_maxsize(result):
    return f"{result} = sys.maxsize"


# ── COPY Module ──────────────────────────────────────────────────────────

@block(label="{result} = copy.copy({obj})", category="Copy", color="#a6e3a1",
       description="Make a shallow copy of an object.")
def cp_copy(result, obj):
    return f"{result} = copy.copy({obj})"


@block(label="{result} = copy.deepcopy({obj})", category="Copy", color="#a6e3a1",
       description="Make a deep copy of an object (copies nested objects too).")
def cp_deepcopy(result, obj):
    return f"{result} = copy.deepcopy({obj})"


# ── PPRINT Module ────────────────────────────────────────────────────────

@block(label="pprint.pprint({obj})", category="Output", color="#cba6f7",
       description="Pretty-print an object.")
def pp_pprint(obj):
    return f"pprint.pprint({obj})"


@block(label="pprint.pprint({obj}, depth={depth})", category="Output", color="#cba6f7",
       description="Pretty-print an object up to a given depth.")
def pp_pprint_depth(obj, depth):
    return f"pprint.pprint({obj}, depth={depth})"


@block(label="{result} = pprint.pformat({obj})", category="Output", color="#cba6f7",
       description="Get a pretty-printed string representation.")
def pp_pformat(result, obj):
    return f"{result} = pprint.pformat({obj})"


# ── LOGGING Module ───────────────────────────────────────────────────────

@block(label="logging.basicConfig(level={level})", category="Logging", color="#f9e2af",
       description="Configure basic logging (e.g. level=logging.DEBUG).")
def lg_basicconfig(level):
    return f"logging.basicConfig(level={level})"


@block(label="logging.basicConfig(level={level}, format={fmt})", category="Logging", color="#f9e2af")
def lg_basicconfig_format(level, fmt):
    return f"logging.basicConfig(level={level}, format={fmt})"


@block(label="logging.debug({msg})", category="Logging", color="#f9e2af")
def lg_debug(msg):
    return f"logging.debug({msg})"


@block(label="logging.info({msg})", category="Logging", color="#f9e2af")
def lg_info(msg):
    return f"logging.info({msg})"


@block(label="logging.warning({msg})", category="Logging", color="#f9e2af")
def lg_warning(msg):
    return f"logging.warning({msg})"


@block(label="logging.error({msg})", category="Logging", color="#f9e2af")
def lg_error(msg):
    return f"logging.error({msg})"


@block(label="logging.critical({msg})", category="Logging", color="#f9e2af")
def lg_critical(msg):
    return f"logging.critical({msg})"


@block(label="{result} = logging.getLogger({name})", category="Logging", color="#f9e2af")
def lg_getlogger(result, name):
    return f"{result} = logging.getLogger({name})"


@block(label="logging.exception({msg})", category="Logging", color="#f9e2af",
       description="Log an error message with exception traceback.")
def lg_exception(msg):
    return f"logging.exception({msg})"


# ── CSV Module ───────────────────────────────────────────────────────────

@block(label="{result} = csv.reader({f})", category="CSV", color="#94e2d5")
def csv_reader(result, f):
    return f"{result} = csv.reader({f})"


@block(label="{result} = csv.writer({f})", category="CSV", color="#94e2d5")
def csv_writer(result, f):
    return f"{result} = csv.writer({f})"


@block(label="{result} = csv.DictReader({f})", category="CSV", color="#94e2d5")
def csv_dictreader(result, f):
    return f"{result} = csv.DictReader({f})"


@block(label="{result} = csv.DictWriter({f}, fieldnames={fieldnames})", category="CSV", color="#94e2d5")
def csv_dictwriter(result, f, fieldnames):
    return f"{result} = csv.DictWriter({f}, fieldnames={fieldnames})"


@block(label="{w}.writerow({row})", category="CSV", color="#94e2d5")
def csv_writerow(w, row):
    return f"{w}.writerow({row})"


@block(label="{w}.writerows({rows})", category="CSV", color="#94e2d5")
def csv_writerows(w, rows):
    return f"{w}.writerows({rows})"


@block(label="{w}.writeheader()", category="CSV", color="#94e2d5",
       description="Write the header row to a DictWriter.")
def csv_writeheader(w):
    return f"{w}.writeheader()"


# ── THREADING Module ─────────────────────────────────────────────────────

@block(label="{result} = threading.Thread(target={target})", category="Threading", color="#fab387")
def th_thread(result, target):
    return f"{result} = threading.Thread(target={target})"


@block(label="{result} = threading.Thread(target={target}, args={args})", category="Threading", color="#fab387")
def th_thread_args(result, target, args):
    return f"{result} = threading.Thread(target={target}, args={args})"


@block(label="{t}.start()", category="Threading", color="#fab387")
def th_start(t):
    return f"{t}.start()"


@block(label="{t}.join()", category="Threading", color="#fab387",
       description="Wait for a thread to finish.")
def th_join(t):
    return f"{t}.join()"


@block(label="{result} = threading.Lock()", category="Threading", color="#fab387")
def th_lock(result):
    return f"{result} = threading.Lock()"


@block(label="{lock}.acquire()", category="Threading", color="#fab387")
def th_lock_acquire(lock):
    return f"{lock}.acquire()"


@block(label="{lock}.release()", category="Threading", color="#fab387")
def th_lock_release(lock):
    return f"{lock}.release()"


@block(label="{result} = threading.current_thread()", category="Threading", color="#fab387")
def th_current_thread(result):
    return f"{result} = threading.current_thread()"


@block(label="{result} = threading.active_count()", category="Threading", color="#fab387",
       description="Get the number of currently active threads.")
def th_active_count(result):
    return f"{result} = threading.active_count()"


# ── SUBPROCESS Module ────────────────────────────────────────────────────

@block(label="{result} = subprocess.run({args})", category="Subprocess", color="#89dceb",
       description="Run a command and wait for it to complete.")
def sp_run(result, args):
    return f"{result} = subprocess.run({args})"


@block(label="{result} = subprocess.run({args}, capture_output=True, text=True)", category="Subprocess", color="#89dceb",
       description="Run a command and capture its output as text.")
def sp_run_capture(result, args):
    return f"{result} = subprocess.run({args}, capture_output=True, text=True)"


@block(label="{result} = subprocess.check_output({args}, text=True)", category="Subprocess", color="#89dceb",
       description="Run a command and return its output as a string.")
def sp_check_output(result, args):
    return f"{result} = subprocess.check_output({args}, text=True)"


@block(label="{result} = subprocess.call({args})", category="Subprocess", color="#89dceb",
       description="Run a command and return its exit code.")
def sp_call(result, args):
    return f"{result} = subprocess.call({args})"


@block(label="{result} = subprocess.Popen({args})", category="Subprocess", color="#89dceb",
       description="Start a process and return a Popen object.")
def sp_popen(result, args):
    return f"{result} = subprocess.Popen({args})"


@block(label="{stdout}, {stderr} = {proc}.communicate()", category="Subprocess", color="#89dceb",
       description="Communicate with a process and get its output.")
def sp_communicate(stdout, stderr, proc):
    return f"{stdout}, {stderr} = {proc}.communicate()"


@block(label="{result} = {proc}.returncode", category="Subprocess", color="#89dceb")
def sp_returncode(result, proc):
    return f"{result} = {proc}.returncode"
