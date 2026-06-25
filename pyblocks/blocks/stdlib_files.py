from pyblocks.blocks.definition import block

# ── JSON Module ──────────────────────────────────────────────────────────

@block(label="{result} = json.loads({s})", category="JSON", color="#94e2d5",
       description="Parse a JSON string into a Python object.")
def js_loads(result, s):
    return f"{result} = json.loads({s})"


@block(label="{result} = json.dumps({obj})", category="JSON", color="#94e2d5",
       description="Convert a Python object to a JSON string.")
def js_dumps(result, obj):
    return f"{result} = json.dumps({obj})"


@block(label="{result} = json.dumps({obj}, indent={indent})", category="JSON", color="#94e2d5",
       description="Convert a Python object to a formatted JSON string.")
def js_dumps_indent(result, obj, indent):
    return f"{result} = json.dumps({obj}, indent={indent})"


@block(label="{result} = json.load({f})", category="JSON", color="#94e2d5",
       description="Load JSON from an open file object.")
def js_load(result, f):
    return f"{result} = json.load({f})"


@block(label="json.dump({obj}, {f})", category="JSON", color="#94e2d5",
       description="Write a Python object as JSON to an open file.")
def js_dump(obj, f):
    return f"json.dump({obj}, {f})"


@block(label="json.dump({obj}, {f}, indent={indent})", category="JSON", color="#94e2d5",
       description="Write a Python object as formatted JSON to an open file.")
def js_dump_indent(obj, f, indent):
    return f"json.dump({obj}, {f}, indent={indent})"


# ── OS Module ────────────────────────────────────────────────────────────

@block(label="{result} = os.getcwd()", category="OS", color="#94e2d5")
def os_getcwd(result):
    return f"{result} = os.getcwd()"


@block(label="{result} = os.listdir({path})", category="OS", color="#94e2d5")
def os_listdir(result, path):
    return f"{result} = os.listdir({path})"


@block(label="os.makedirs({path}, exist_ok=True)", category="OS", color="#94e2d5",
       description="Create directory and all parent directories.")
def os_makedirs(path):
    return f"os.makedirs({path}, exist_ok=True)"


@block(label="os.remove({path})", category="OS", color="#94e2d5")
def os_remove(path):
    return f"os.remove({path})"


@block(label="os.rename({src}, {dst})", category="OS", color="#94e2d5")
def os_rename(src, dst):
    return f"os.rename({src}, {dst})"


@block(label="{result} = os.getenv({key})", category="OS", color="#94e2d5")
def os_getenv(result, key):
    return f"{result} = os.getenv({key})"


@block(label="{result} = os.getenv({key}, {default})", category="OS", color="#94e2d5")
def os_getenv_default(result, key, default):
    return f"{result} = os.getenv({key}, {default})"


@block(label="os.chdir({path})", category="OS", color="#94e2d5")
def os_chdir(path):
    return f"os.chdir({path})"


@block(label="{result} = os.scandir({path})", category="OS", color="#94e2d5")
def os_scandir(result, path):
    return f"{result} = os.scandir({path})"


@block(label="os.rmdir({path})", category="OS", color="#94e2d5")
def os_rmdir(path):
    return f"os.rmdir({path})"


# ── OS.Path Module ───────────────────────────────────────────────────────

@block(label="{result} = os.path.join({a}, {b})", category="OS Path", color="#94e2d5")
def os_path_join(result, a, b):
    return f"{result} = os.path.join({a}, {b})"


@block(label="{result} = os.path.exists({path})", category="OS Path", color="#94e2d5")
def os_path_exists(result, path):
    return f"{result} = os.path.exists({path})"


@block(label="{result} = os.path.isfile({path})", category="OS Path", color="#94e2d5")
def os_path_isfile(result, path):
    return f"{result} = os.path.isfile({path})"


@block(label="{result} = os.path.isdir({path})", category="OS Path", color="#94e2d5")
def os_path_isdir(result, path):
    return f"{result} = os.path.isdir({path})"


@block(label="{result} = os.path.basename({path})", category="OS Path", color="#94e2d5")
def os_path_basename(result, path):
    return f"{result} = os.path.basename({path})"


@block(label="{result} = os.path.dirname({path})", category="OS Path", color="#94e2d5")
def os_path_dirname(result, path):
    return f"{result} = os.path.dirname({path})"


@block(label="{result} = os.path.splitext({path})", category="OS Path", color="#94e2d5",
       description="Split path into (root, ext) tuple.")
def os_path_splitext(result, path):
    return f"{result} = os.path.splitext({path})"


@block(label="{result} = os.path.abspath({path})", category="OS Path", color="#94e2d5")
def os_path_abspath(result, path):
    return f"{result} = os.path.abspath({path})"


@block(label="{result} = os.path.getsize({path})", category="OS Path", color="#94e2d5",
       description="Get the size of a file in bytes.")
def os_path_getsize(result, path):
    return f"{result} = os.path.getsize({path})"


@block(label="{result} = os.path.expanduser({path})", category="OS Path", color="#94e2d5",
       description="Expand ~ to the user's home directory.")
def os_path_expanduser(result, path):
    return f"{result} = os.path.expanduser({path})"


# ── Pathlib Module ───────────────────────────────────────────────────────

@block(label="{result} = pathlib.Path({s})", category="Pathlib", color="#cba6f7",
       description="Create a Path object from a string.")
def pl_path(result, s):
    return f"{result} = pathlib.Path({s})"


@block(label="{result} = pathlib.Path.home()", category="Pathlib", color="#cba6f7")
def pl_home(result):
    return f"{result} = pathlib.Path.home()"


@block(label="{result} = pathlib.Path.cwd()", category="Pathlib", color="#cba6f7")
def pl_cwd(result):
    return f"{result} = pathlib.Path.cwd()"


@block(label="{result} = {p}.exists()", category="Pathlib", color="#cba6f7")
def pl_exists(result, p):
    return f"{result} = {p}.exists()"


@block(label="{result} = {p}.is_file()", category="Pathlib", color="#cba6f7")
def pl_is_file(result, p):
    return f"{result} = {p}.is_file()"


@block(label="{result} = {p}.is_dir()", category="Pathlib", color="#cba6f7")
def pl_is_dir(result, p):
    return f"{result} = {p}.is_dir()"


@block(label="{p}.mkdir(parents=True, exist_ok=True)", category="Pathlib", color="#cba6f7",
       description="Create the directory and all parents.")
def pl_mkdir(p):
    return f"{p}.mkdir(parents=True, exist_ok=True)"


@block(label="{p}.unlink()", category="Pathlib", color="#cba6f7",
       description="Delete the file.")
def pl_unlink(p):
    return f"{p}.unlink()"


@block(label="{result} = {p}.read_text()", category="Pathlib", color="#cba6f7")
def pl_read_text(result, p):
    return f"{result} = {p}.read_text()"


@block(label="{p}.write_text({text})", category="Pathlib", color="#cba6f7")
def pl_write_text(p, text):
    return f"{p}.write_text({text})"


@block(label="{result} = {p}.read_bytes()", category="Pathlib", color="#cba6f7")
def pl_read_bytes(result, p):
    return f"{result} = {p}.read_bytes()"


@block(label="{p}.write_bytes({data})", category="Pathlib", color="#cba6f7")
def pl_write_bytes(p, data):
    return f"{p}.write_bytes({data})"


@block(label="{result} = {p}.name", category="Pathlib", color="#cba6f7",
       description="Get the final component of the path.")
def pl_name(result, p):
    return f"{result} = {p}.name"


@block(label="{result} = {p}.stem", category="Pathlib", color="#cba6f7",
       description="Get the filename without its suffix.")
def pl_stem(result, p):
    return f"{result} = {p}.stem"


@block(label="{result} = {p}.suffix", category="Pathlib", color="#cba6f7",
       description="Get the file extension.")
def pl_suffix(result, p):
    return f"{result} = {p}.suffix"


@block(label="{result} = {p}.parent", category="Pathlib", color="#cba6f7",
       description="Get the parent directory.")
def pl_parent(result, p):
    return f"{result} = {p}.parent"


@block(label="{result} = list({p}.iterdir())", category="Pathlib", color="#cba6f7",
       description="List all files and directories in this directory.")
def pl_iterdir(result, p):
    return f"{result} = list({p}.iterdir())"


@block(label="{result} = list({p}.glob({pattern}))", category="Pathlib", color="#cba6f7",
       description="Find all files matching the glob pattern.")
def pl_glob(result, p, pattern):
    return f"{result} = list({p}.glob({pattern}))"


@block(label="{result} = {p} / {other}", category="Pathlib", color="#cba6f7",
       description="Join paths using the / operator.")
def pl_joinpath(result, p, other):
    return f"{result} = {p} / {other}"
