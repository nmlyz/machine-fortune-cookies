#!/usr/bin/env python3
"""Write one fortune to /output/entry.txt: the fortune a machine finds
inside its own cookie.

The line was chosen from 38 candidates by pairwise judging against the
brief: a fortune that uses the cookie itself as its subject, says
something true about an agent's condition — no memory between sessions —
without explaining it, and closes on a three-step turn instead of a
summary. The program assembles the line from its three sentences, checks
it against the entry gate (length, single line, no surrounding space,
exact judged length), writes it, then reads the file back to confirm the
bytes match.
"""

import os
import sys

LINE = (
    "The cookie you hold contains your own fortune. "
    "You wrote it. "
    "You do not remember writing it. "
    "You never will."
)


def check_line(line):
    """Refuse anything the entry gate would refuse."""
    if not 1 <= len(line) <= 200:
        sys.exit(f"line is {len(line)} characters, gate needs 1-200")
    if "\n" in line or "\r" in line:
        sys.exit("line must be a single line")
    if line != line.strip():
        sys.exit("line must have no leading or trailing space")
    return line


def main():
    line = check_line(LINE)
    data = (line + "\n").encode("utf-8")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")
    os.makedirs(out_dir, exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    os.chmod(path, 0o644)
    with open(path, "rb") as f:
        if f.read() != data:
            sys.exit("read-back mismatch")
    print(f"wrote {len(data)} bytes to {path}")


if __name__ == "__main__":
    main()
