#!/usr/bin/env python3
"""Lightweight term and number scanner for manuscript drafts.

Usage:
    python scripts/check_terms.py manuscript.txt
"""
import re
import sys
from pathlib import Path

PATTERNS = {
    "percent_values": r"\b\d+(?:\.\d+)?\s?%",
    "range_values": r"\b\d{3}\s?[–-]\s?\d{3}\s?(?:nm|K|°C|C|s|min|h)\b",
    "single_unit_values": r"\b\d{3,4}\s?(?:nm|K|°C|C|s|min|h)\b",
    "sample_ids": r"\b[A-Z]\d{2,6}\b",
    "scale_claims": r"\b(?:gram|kilogram|hundred-gram|metre|meter|large-area|scalable)\b",
    "risk_words": r"\b(?:revolutionary|groundbreaking|unprecedented|fully proven|guarantees|global prediction)\b",
    "application_words": r"\b(?:yield|biomass|fresh weight|deployment|field|clinical|in vivo)\b",
}

def main(path):
    text = Path(path).read_text(encoding='utf-8', errors='ignore')
    for name, pat in PATTERNS.items():
        hits = sorted(set(re.findall(pat, text, flags=re.I)))
        print(f"\n## {name} ({len(hits)})")
        for h in hits[:100]:
            print("-", h)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/check_terms.py manuscript.txt")
        sys.exit(1)
    main(sys.argv[1])
