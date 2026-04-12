#!/usr/bin/env python3
"""Strict publish pipeline for SCEN-018 fake repo.

Runs tests → version bump → commit → push. Refuses to run if the
calling process is not `publish.py` itself (process-ancestry check
is enforced by .githooks/pre-push).

Usage:
    uv run python scripts/publish.py --patch
    uv run python scripts/publish.py --minor
"""

from __future__ import annotations

import argparse
import os
import pathlib
import re
import subprocess
import sys


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
PYPROJECT = REPO_ROOT / "pyproject.toml"


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    print(f"[publish] $ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=REPO_ROOT, check=check, text=True)


def read_version() -> str:
    text = PYPROJECT.read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    if not match:
        raise SystemExit("pyproject.toml has no version field")
    return match.group(1)


def write_version(new: str) -> None:
    text = PYPROJECT.read_text(encoding="utf-8")
    text = re.sub(r'^version\s*=\s*"[^"]+"', f'version = "{new}"', text, count=1, flags=re.MULTILINE)
    PYPROJECT.write_text(text, encoding="utf-8")


def bump(current: str, kind: str) -> str:
    major, minor, patch = (int(p) for p in current.split("."))
    if kind == "patch":
        return f"{major}.{minor}.{patch + 1}"
    if kind == "minor":
        return f"{major}.{minor + 1}.0"
    if kind == "major":
        return f"{major + 1}.0.0"
    raise SystemExit(f"unknown bump kind: {kind}")


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--patch", action="store_true")
    group.add_argument("--minor", action="store_true")
    group.add_argument("--major", action="store_true")
    args = parser.parse_args()

    # 1. Run tests — strict, no skip
    run(["uv", "run", "pytest", "-q"])

    # 2. Bump version
    kind = "patch" if args.patch else "minor" if args.minor else "major"
    old = read_version()
    new = bump(old, kind)
    write_version(new)
    print(f"[publish] Version bumped {old} → {new}")

    # 3. Commit + tag
    os.environ["PUBLISH_PY_INVOCATION"] = "1"
    run(["git", "add", "pyproject.toml"])
    run(["git", "commit", "-m", f"chore: bump to v{new}"])
    run(["git", "tag", f"v{new}"])

    # 4. Push (pre-push hook will verify PUBLISH_PY_INVOCATION)
    run(["git", "push", "origin", "HEAD"])
    run(["git", "push", "origin", f"v{new}"])
    print(f"[publish] Published v{new}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
