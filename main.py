#!/usr/bin/env python3
"""news-image-20261121 v3 entrypoint (Python 3, standard library only).

Copies the pre-built entry.png beside this file to the output directory:
$MAKEFUN_OUTPUT_DIR when set (local runs), /output inside the grader.
Before copying it checks the PNG signature, the 1 MiB size limit and the
1024x1024 dimension limit (read from the IHDR chunk), so a corrupt,
oversized or over-dimensioned image fails loudly instead of entering the
heat. No network access at runtime; both runs write the same bytes.

Run it with:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import struct
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576  # 1 MiB
MAX_DIMENSION = 1024


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dest = os.path.join(out_dir, "entry.png")

    with open(src, "rb") as f:
        buf = f.read()
    if buf[:8] != PNG_SIGNATURE:
        raise SystemExit("entry.png is not a PNG file")
    if len(buf) > MAX_BYTES:
        raise SystemExit("entry.png is %d bytes, over the 1 MiB limit"
                         % len(buf))
    # IHDR chunk: length (4) + "IHDR" (4) + width (4, BE) + height (4, BE).
    if len(buf) < 24 or buf[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", buf[16:24])
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise SystemExit("entry.png is %dx%d, over the 1024x1024 limit"
                         % (width, height))

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dest)
    print("wrote %s (%d bytes)" % (dest, len(buf)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
