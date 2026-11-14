"""Load a strictly pinned public Auto runtime from the external checkout.

The private repository owns only book state, credentials and deployment config.
This adapter never fetches mutable main or executes unverified local code.
"""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import re
import runpy
import subprocess
import sys

STATE_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_ROOT = STATE_ROOT / ".public-auto-runtime"
LOCK_PATH = STATE_ROOT / "automation" / "runtime.lock.json"
PUBLIC_REPOSITORY = "tim8es/book-translator"
SHA = re.compile(r"[0-9a-f]{40}\Z")
MODULES = frozenset({"book_runner.py", "literary_context.py", "omniroute.py",
                     "job_monitor.py", "actions_failure_notifier.py",
                     "verify_changed_books.py"})


def pinned_revision() -> str:
    lock = json.loads(LOCK_PATH.read_text("utf-8"))
    if (not isinstance(lock, dict)
            or set(lock) != {"schema_version", "repository", "revision"}
            or lock["schema_version"] != 1
            or lock["repository"] != PUBLIC_REPOSITORY
            or not isinstance(lock["revision"], str)
            or not SHA.fullmatch(lock["revision"])):
        raise RuntimeError("invalid pinned public Auto runtime lock")
    return lock["revision"]


def verified_runtime(module_file: str) -> Path:
    if module_file not in MODULES:
        raise RuntimeError("unsupported public runtime module")
    revision = pinned_revision()
    engine = RUNTIME_ROOT.resolve()
    if not (engine / ".git").exists():
        raise RuntimeError(
            "pinned public runtime missing; checkout repository "
            + PUBLIC_REPOSITORY + " at " + revision
            + " into .public-auto-runtime before running Auto")
    run = subprocess.run(
        ["git", "-C", str(engine), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True, timeout=10,
    )
    if run.stdout.strip() != revision:
        raise RuntimeError("public Auto runtime revision differs from pinned lock")
    destination = (engine / "automation" / module_file).resolve()
    if not destination.is_relative_to(engine / "automation") or not destination.is_file():
        raise RuntimeError("verified public runtime module missing")
    return destination


def load_shared_module(name: str, module_file: str) -> None:
    path = verified_runtime(module_file)
    os.environ["BOOK_TRANSLATOR_STATE_ROOT"] = str(STATE_ROOT.resolve())
    library = str(path.parent)
    if library not in sys.path:
        sys.path.insert(0, library)
    if name == "__main__":
        runpy.run_path(str(path), run_name="__main__")
        return
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load verified public Auto module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)


if __name__ == "__main__":
    if sys.argv[1:] == ["--print-revision"]:
        print(pinned_revision())
    elif sys.argv[1:] == ["--verify"]:
        for module in sorted(MODULES):
            verified_runtime(module)
        print("Pinned public Auto runtime verified")
    else:
        raise SystemExit("usage: runtime_loader.py --print-revision | --verify")
