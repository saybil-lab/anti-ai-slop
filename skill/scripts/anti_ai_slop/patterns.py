"""Load AI-slop patterns from patterns*.json. Single source of truth."""
import json
import os
import re
from functools import lru_cache
from pathlib import Path

_DIR = Path(__file__).parent
_FILES = {"en": "patterns.json", "fr": "patterns_fr.json"}
LANGS = ("en", "fr", "all")
DEFAULT_LANG = os.environ.get("SLOP_LANG", "en")


def _read(lang: str) -> dict:
    with (_DIR / _FILES[lang]).open(encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=None)
def load(lang: str = "en"):
    """Return (all_terms, replacements, severity) for `en`, `fr` or `all`."""
    langs = list(_FILES) if lang == "all" else [lang]
    items = []
    for code in langs:
        data = _read(code)
        items += data.get("phrases", []) + data.get("words", [])
    all_terms = list(dict.fromkeys(item["text"] for item in items))
    # Skip null replacements.
    replacements = {
        item["text"]: item["replace"]
        for item in items
        if item.get("replace") is not None
    }
    severity = {item["text"]: item.get("severity", "medium") for item in items}
    return all_terms, replacements, severity


def term_regex(term: str):
    """Case-insensitive, word-boundary regex. Straight and curly apostrophes match each other."""
    prefix = r"\b" if term[0].isalnum() else ""
    suffix = r"\b" if term[-1].isalnum() else ""
    body = "['’]".join(re.escape(part) for part in re.split(r"['’]", term))
    return re.compile(prefix + body + suffix, re.IGNORECASE)


_DATA = _read("en")
PUNCTUATION = _DATA.get("punctuation", {})
PHRASES = _DATA.get("phrases", [])
WORDS = _DATA.get("words", [])

# English defaults, kept for backward compatibility.
ALL_TERMS, REPLACEMENTS, SEVERITY = load("en")

# Legacy aliases.
FORBIDDEN_WORDS = ALL_TERMS
EM_DASH = "—"
EN_DASH = "–"
EM_DASH_REPLACEMENT = PUNCTUATION.get(EM_DASH, ", ")
