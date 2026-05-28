#!/usr/bin/env python3
"""Naive claim-like sentence extractor for review, not automated truth checking."""
import re, sys
from pathlib import Path

CLAIM_VERBS = r"(show|shows|demonstrate|demonstrates|indicate|indicates|suggest|suggests|establish|establishes|reveal|reveals|enable|enables|confirm|confirms)"

def split_sentences(text):
    return re.split(r"(?<=[.!?])\s+", text)

def main(path):
    text = Path(path).read_text(encoding='utf-8', errors='ignore')
    for s in split_sentences(text):
        if re.search(CLAIM_VERBS, s, re.I):
            print("-", s.strip())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/extract_claims.py manuscript.txt")
        sys.exit(1)
    main(sys.argv[1])
