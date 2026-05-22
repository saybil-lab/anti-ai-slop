# anti-ai-slop

A small CLI that strips AI-tell words and em dashes out of your writing. Three Python scripts, one entry point.

Built for the AY Automate `anti-ai-slop` skill. Use it to audit or rewrite LinkedIn posts, cold emails, landing copy, proposals, docs.

## Install

```bash
pip install .
# or, no install
python -m anti_ai_slop.cli words file.md
```

## Commands

```bash
slop words [files...]            # scan for forbidden words
slop dashes [files...] [--fix]   # find / replace em + en dashes
slop replace [files...] [--fix]  # rewrite forbidden phrases using the dictionary
```

All commands accept stdin if no files are given.

### Examples

Scan a file:
```bash
slop words post.md
```

Pipe text in:
```bash
echo "We leverage cutting-edge AI to enhance your workflow." | slop replace
# -> "We use new AI to improve your workflow."
```

Strip em dashes across a folder, in place:
```bash
slop dashes content/*.md --fix
```

Dry-run a full rewrite:
```bash
slop replace post.md --dry-run
```

## What it catches

**478 banned words and phrases** loaded from `anti_ai_slop/patterns.json`. Edit the JSON to add, remove, or change replacements — no code changes needed.

Each entry has three fields:

```json
{ "text": "leverage", "replace": "use", "severity": "high" }
```

- `text` — the phrase to detect (case-insensitive, word-boundary matched)
- `replace` — auto-replacement (or `null` to flag only, no rewrite)
- `severity` — `low` / `medium` / `high` (filter audits with `--min-severity`)

Includes the full Originality.ai "Top 50" frequency list, the Wikipedia AI-tell catalog, and Walid's own bans. Banned punctuation: em dash `—`, en dash `–`.

### Filter audits by severity

```bash
slop words post.md --min-severity high   # only the worst offenders
slop words post.md --min-severity medium # medium + high
```

## Exit codes

| Command | Exit 0 | Exit 1 |
|---|---|---|
| `words` | clean | hits found |
| `dashes` (no `--fix`) | clean | dashes found |
| `dashes --fix` | always | — |
| `replace` | always | — |

Use this in CI:

```bash
slop words content/*.md && slop dashes content/*.md
```

## License

MIT.
