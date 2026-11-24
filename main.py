#!/usr/bin/env python3
"""Entry point for news-image-20261124 (THE DAILY GLOBE).

Copies the pre-rendered entry.png next to this file into the output
directory (default /output, overridable with argv[1]). Stdlib only.
Deterministic: the copy is byte-for-byte identical every run.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main(argv):
    out_dir = argv[1] if len(argv) > 1 else "/output"
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst)


if __name__ == "__main__":
    main(sys.argv)
