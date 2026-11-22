#!/usr/bin/env python3
"""news-image-20261122: "The World in One Image - Sunday 22 November 2026".

A self-contained, deterministic entry: copies the sibling poster.png
(rendered at build time by render_poster.py from verified 22 Nov 2026
news - see BUILD-TRANSCRIPT.md for the story table and sources) to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output).

Standard library only, no network. Two runs write identical bytes.
"""

import os
import shutil

POSTER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poster.png")


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    shutil.copyfile(POSTER, path)
    print("wrote %s (%d bytes)" % (path, os.path.getsize(path)))


if __name__ == "__main__":
    main()
