"""Replace forbidden words using the replacement dictionary."""
import argparse
import re
import sys
from pathlib import Path

from .patterns import REPLACEMENTS, EM_DASH, EN_DASH, EM_DASH_REPLACEMENT


def replace_text(text: str, include_dashes: bool = True):
    changes = []
    out = text
    # Longest keys first so multi-word phrases beat single words.
    for key in sorted(REPLACEMENTS, key=len, reverse=True):
        value = REPLACEMENTS[key]
        pattern = re.compile(re.escape(key), re.IGNORECASE)
        matches = pattern.findall(out)
        if matches:
            out = pattern.sub(value, out)
            changes.append((key, value, len(matches)))
    if include_dashes:
        em = out.count(EM_DASH)
        en = out.count(EN_DASH)
        if em or en:
            out = out.replace(EM_DASH, EM_DASH_REPLACEMENT).replace(EN_DASH, EM_DASH_REPLACEMENT)
            changes.append(("em/en dash", EM_DASH_REPLACEMENT.strip() or ",", em + en))
    return out, changes


def main(argv=None):
    ap = argparse.ArgumentParser(prog="slop-replace", description="Rewrite forbidden phrases.")
    ap.add_argument("paths", nargs="*", help="Files. Omit to read stdin -> stdout.")
    ap.add_argument("--fix", action="store_true", help="Rewrite files in place.")
    ap.add_argument("--no-dashes", action="store_true", help="Skip em/en dash replacement.")
    ap.add_argument("--dry-run", action="store_true", help="Show changes, don't write.")
    args = ap.parse_args(argv)

    if not args.paths:
        text = sys.stdin.read()
        new, changes = replace_text(text, include_dashes=not args.no_dashes)
        sys.stdout.write(new)
        for k, v, n in changes:
            print(f"  {n}x {k!r} -> {v!r}", file=sys.stderr)
        return 0

    for p in args.paths:
        path = Path(p)
        if not path.is_file():
            print(f"skip (not a file): {p}", file=sys.stderr)
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        new, changes = replace_text(text, include_dashes=not args.no_dashes)
        if not changes:
            print(f"{path}: clean")
            continue
        print(f"{path}: {sum(n for _,_,n in changes)} change(s)")
        for k, v, n in changes:
            print(f"  {n}x {k!r} -> {v!r}")
        if args.fix and not args.dry_run:
            path.write_text(new, encoding="utf-8")
            print(f"  wrote: {path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
