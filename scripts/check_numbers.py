#!/usr/bin/env python3
"""Extract repeated numerical claims for manual consistency audit."""
import re, sys
from collections import Counter
from pathlib import Path

NUM = re.compile(r"\b\d+(?:\.\d+)?\s?(?:%|nm|g|kg|mg|mL|µL|uL|days?|h|°C|K|wt%|mol%)?", re.I)

def main(path):
    text = Path(path).read_text(encoding='utf-8', errors='ignore')
    vals = [m.group(0).strip() for m in NUM.finditer(text)]
    counts = Counter(vals)
    for val, n in counts.most_common():
        if n > 1:
            print(f"{val}\t{n}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/check_numbers.py manuscript.txt")
        sys.exit(1)
    main(sys.argv[1])
