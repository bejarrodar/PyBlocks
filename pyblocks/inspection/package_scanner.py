from __future__ import annotations
import json
import subprocess
import sys
from dataclasses import dataclass

_SCAN_SCRIPT = """
import sys, inspect, importlib, pkgutil, json

def scan_module(mod, modname):
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

name = sys.argv[1]
try:
    pkg = importlib.import_module(name)
except ImportError as e:
    print(json.dumps({"error": str(e)}))
    sys.exit(1)

all_entries = scan_module(pkg, name)

if hasattr(pkg, "__path__"):
    for _, modname, _ in pkgutil.walk_packages(pkg.__path__, prefix=name + "."):
        try:
            mod = importlib.import_module(modname)
            all_entries.extend(scan_module(mod, modname))
        except Exception:
            continue

seen = set()
deduped = []
for e in all_entries:
    if e["qualname"] not in seen:
        seen.add(e["qualname"])
        deduped.append(e)

print(json.dumps(deduped))
"""


@dataclass
class CallableEntry:
    qualname: str
    params: list[str]
    submodule: str


class PackageScanner:

    @staticmethod
    def scan(package_name: str) -> list[CallableEntry] | None:
        try:
            result = subprocess.run(
                [sys.executable, "-c", _SCAN_SCRIPT, package_name],
                capture_output=True, text=True, timeout=60,
            )
        except (subprocess.TimeoutExpired, OSError):
            return None

        raw = result.stdout.strip()
        if not raw:
            return None
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return None

        if isinstance(data, dict) and "error" in data:
            return None

        try:
            return [CallableEntry(**e) for e in data]
        except (TypeError, KeyError):
            return None
