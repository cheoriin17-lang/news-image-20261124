#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261124.

Copies the pre-rendered front page (entry.png, next to this file) to
<output-dir>/entry.png. The output directory defaults to /output and
can be overridden with the first command-line argument.

Deterministic: the same input bytes are copied on every run, so two
runs produce byte-identical output. Stdlib only; no network, no
randomness, no timestamps in the output.
"""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def copy_entry(output_dir):
    """Copy entry.png into output_dir and return the destination path."""
    destination = Path(output_dir) / "entry.png"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, destination)
    return destination


def main(argv):
    output_dir = argv[1] if len(argv) > 1 else "/output"
    written = copy_entry(output_dir)
    print(f"wrote {written} ({written.stat().st_size} bytes)")


if __name__ == "__main__":
    main(sys.argv)
