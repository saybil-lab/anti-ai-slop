"""Scan files or stdin for forbidden AI-slop words. Read-only audit."""
import argparse
import re
import sys
from pathlib import Path

from .patterns import FORBIDDEN_WORDS


def scan_text(text: str):
    hits = []
    for word in FORBIDDEN_WORDS:
        pattern = re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)
        for match in pattern.finditer(text):
            line_no = text.count("\n", 0, match.start()) + 1
            line_start = text.rfind("\n", 0, match.start()) + 1
            line_end = text.find("\n", match.end())
            if line_end == -1:
                line_end = len(text)
            line = text[line_start:line_end].strip()
            hits.append((line_no, word, match.group(0), line))
    return hits


def format_hits(hits, source: str):
    if not hits:
        return f"{source}: clean\n"
    out = [f"{source}: {len(hits)} hit(s)"]
    for line_no, word, found, line in hits:
        out.append(f"  L{line_no} [{word}] -> {found!r} :: {line}")
    return "\n".join(out) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="slop-words", description="Find AI-slop words.")
    ap.add_argument("paths", nargs="*", help="Files to scan. Omit to read stdin.")
    ap.add_argument("--quiet", action="store_true", help="Only print files with hits.")
    args = ap.parse_args(argv)

    total = 0
    if not args.paths:
        text = sys.stdin.read()
        hits = scan_text(text)
        total += len(hits)
        sys.stdout.write(format_hits(hits, "<stdin>"))
    else:
        for p in args.paths:
            path = Path(p)
            if not path.is_file():
                print(f"skip (not a file): {p}", file=sys.stderr)
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            hits = scan_text(text)
            total += len(hits)
            if hits or not args.quiet:
                sys.stdout.write(format_hits(hits, str(path)))

    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
