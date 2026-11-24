#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261124 (v2 variant).

Copies the pre-rendered front page (entry.png, next to this file) to
<output-dir>/entry.png. The output directory defaults to /output and
can be overridden with the first command-line argument.

Deterministic: a plain byte copy, so every run produces identical
output. Stdlib only; no network, no randomness.
"""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def main(argv):
    output_dir = argv[1] if len(argv) > 1 else "/output"
    target = Path(output_dir) / "entry.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, target)
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main(sys.argv)
