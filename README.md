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

Banned words (case-insensitive): `Additionally`, `leverage`, `delve`, `crucial`, `pivotal`, `showcase`, `underscore`, `emphasize`, `enhance`, `empower`, `foster`, `garner`, `comprehensive`, `holistic`, `seamlessly`, `robust solution`, `cutting-edge`, `game-changer`, `intricate`, `tapestry`, `landscape`, `vibrant`, `enduring`, `testament`, `serves as`, `stands as`, `It is worth noting`, `In conclusion`, `In summary`, `Let's explore`, `Here is your`, `As we can see`, and more.

Banned punctuation: em dash `—`, en dash `–`.

Full list lives in `anti_ai_slop/patterns.py`.

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
