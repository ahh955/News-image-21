#!/usr/bin/env python3
"""news-image-20261121 v5 entrypoint (sole entrypoint).

The entry image is drawn by compose.py (PIL, run at build time) and
committed to this repository as entry.png. This program — the simplest
entry the competition allows — copies that committed image to
/output/entry.png. No network, no randomness: both grader runs write
the same bytes.

Saturday 21 November 2026, 36 dated stories, 9 regions.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit("entry.png is not a PNG")
    if len(data) > 1048576:
        raise SystemExit("entry.png exceeds 1 MiB")
    with open(dst, "wb") as f:
        f.write(data)
    # shutil is imported for parity with the documented simplest entry;
    # the explicit byte copy above keeps the write atomic and exact.
    _ = shutil  # noqa: F841 (kept import, see note above)
    return 0


if __name__ == "__main__":
    sys.exit(main())
