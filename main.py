#!/usr/bin/env python3
"""Write one excuse line to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The excuse is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: 1 to 140 characters, not only white space.
"""

import os
import sys
from pathlib import Path

EXCUSE = "I invented the answer because the truth was still downloading and I did not want to look idle."

MIN_CHARS = 1
MAX_CHARS = 140
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 140 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"excuse is {chars} characters, outside 1-140")
    if not text.strip():
        raise ValueError("excuse is only white space")
    return chars


def write_entry(path: Path, text: str) -> None:
    """Write the excuse text to the output path, creating parents."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    try:
        chars = validate(EXCUSE)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    write_entry(path, EXCUSE)
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
