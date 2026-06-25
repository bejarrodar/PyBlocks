from __future__ import annotations
import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pyblocks.logger import get_logger

log = get_logger("scanner")

# argv[1] = package name, argv[2] = path to write JSON result into
# Writing to a temp file (not stdout) means C extensions like SDL/pygame
# cannot corrupt the output by hijacking stdout at the Win32 handle layer.
_SCAN_SCRIPT = """
import sys, inspect, importlib, importlib.util, pkgutil, json, io, ast, time as _time

def scan_module(mod, modname):
    \"\"\"Scan a live imported module via inspect.\"\"\"
    entries = []
    for fname, obj in inspect.getmembers(mod, predicate=inspect.isroutine):
        if fname.startswith("_"):
            continue
        try:
            sig = inspect.signature(obj)
            params = [
                p for p, v in sig.parameters.items()
                if v.kind not in (inspect.Parameter.VAR_POSITIONAL,
                                  inspect.Parameter.VAR_KEYWORD)
                and p != "self"
            ]
        except (ValueError, TypeError):
            params = []
        entries.append({
            "qualname": f"{modname}.{fname}",
            "params": params,
            "submodule": modname,
        })
    return entries

def scan_module_ast(src_path, modname):
    \"\"\"Extract top-level functions from a .py file using AST — no code is executed.\"\"\"
    entries = []
    try:
        source = open(src_path, encoding="utf-8", errors="replace").read()
        tree = ast.parse(source, filename=src_path)
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name.startswith("_"):
                    continue
                params = [a.arg for a in node.args.args if a.arg != "self"]
                entries.append({
                    "qualname": f"{modname}.{node.name}",
                    "params": params,
                    "submodule": modname,
                })
    except Exception:
        pass
    return entries

def _silent_import(modname):
    _out, _err = sys.stdout, sys.stderr
    sys.stdout = sys.stderr = io.StringIO()
    try:
        return importlib.import_module(modname)
    finally:
        sys.stdout, sys.stderr = _out, _err

name = sys.argv[1]
out_path = sys.argv[2]

def _write(obj):
    with open(out_path, "w", encoding="utf-8") as _f:
        json.dump(obj, _f)

try:
    pkg = _silent_import(name)
except ImportError as e:
    _write({"error": str(e)})
    sys.exit(1)
except Exception as e:
    _write({"error": f"import failed: {e}"})
    sys.exit(1)

all_entries = []
try:
    all_entries.extend(scan_module(pkg, name))
except BaseException:
    pass

if hasattr(pkg, "__path__"):
    _deadline = _time.monotonic() + 90
    for _, modname, _ in pkgutil.walk_packages(pkg.__path__, prefix=name + "."):
        if _time.monotonic() > _deadline:
            break
        try:
            spec = importlib.util.find_spec(modname)
            origin = spec.origin if spec else None
            if origin and origin.endswith(".py"):
                # Safe: parse source AST without executing any code
                all_entries.extend(scan_module_ast(origin, modname))
            elif origin:
                # C extension — no module-level GUI code, safe to import
                mod = _silent_import(modname)
                all_entries.extend(scan_module(mod, modname))
        except BaseException:
            continue

seen = set()
deduped = []
for e in all_entries:
    if e["qualname"] not in seen:
        seen.add(e["qualname"])
        deduped.append(e)

_write(deduped)
"""


@dataclass
class CallableEntry:
    qualname: str
    params: list[str]
    submodule: str


class PackageScanner:

    @staticmethod
    def scan(package_name: str) -> list[CallableEntry] | None:
        entries, _err = PackageScanner.scan_with_error(package_name)
        return entries

    @staticmethod
    def scan_with_error(package_name: str) -> tuple[list[CallableEntry] | None, str]:
        log.info("Scanning package '%s'", package_name)
        tmp_fd, tmp_path = tempfile.mkstemp(suffix=".json", prefix="pyblocks_scan_")
        os.close(tmp_fd)
        try:
            return PackageScanner._run_scan(package_name, tmp_path)
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    @staticmethod
    def _run_scan(package_name: str, tmp_path: str) -> tuple[list[CallableEntry] | None, str]:
        try:
            result = subprocess.run(
                [sys.executable, "-c", _SCAN_SCRIPT, package_name, tmp_path],
                capture_output=True, text=True, timeout=120,
            )
        except subprocess.TimeoutExpired:
            log.error("Scan of '%s' timed out after 120 s", package_name)
            return None, "timed out after 120 s"
        except OSError as e:
            log.error("Scan of '%s' OS error: %s", package_name, e)
            return None, str(e)

        log.debug("Scan returncode=%d stderr_len=%d", result.returncode, len(result.stderr))
        if result.stderr.strip():
            log.debug("Scan stderr: %s", result.stderr.strip()[-500:])

        try:
            raw = open(tmp_path, encoding="utf-8").read().strip()
        except OSError:
            raw = ""

        if not raw:
            detail = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "no output"
            log.error("Scan of '%s' produced no output — %s", package_name, detail)
            return None, detail

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            log.error("Scan of '%s' returned non-JSON: %s", package_name, raw[:200])
            return None, f"unexpected output: {raw[:120]}"

        if isinstance(data, dict) and "error" in data:
            log.error("Scan of '%s' script error: %s", package_name, data["error"])
            return None, data["error"]

        try:
            entries = [CallableEntry(**e) for e in data]
            log.info("Scan of '%s' found %d callables", package_name, len(entries))
            return entries, ""
        except (TypeError, KeyError) as e:
            log.error("Scan of '%s' bad entry shape: %s", package_name, e)
            return None, str(e)
