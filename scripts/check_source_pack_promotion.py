#!/usr/bin/env python3
"""Promotion gate for source-packs/.

Stubs land in `source-packs/from-zotero/` (or other subdirs) with `TBD`
placeholders for `stance`, `scope`, `action` and `source_id`. Once the human
has read the paper and tagged it in Zotero (or filled the stub by hand), the
stub graduates by being moved out of any subfolder marked `from-zotero/` /
`generated/` into the top-level `source-packs/` directory.

This script enforces the gate:

- Stubs anywhere under `source-packs/` (excluding the staging subdirs
  `from-zotero/` and `generated/`) must NOT contain `TBD` placeholders for
  stance/scope/action/source_id.
- Stubs in staging subdirs are exempt; that is where unfinished work lives.
- The `_SOURCE_NOTE_TEMPLATE.md` is exempt by name.

This is a static QA check; it does not call Zotero or any external service.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PACKS_DIR = ROOT / "source-packs"
STAGING_DIRS = {"from-zotero", "generated"}
EXEMPT_FILENAMES = {"_SOURCE_NOTE_TEMPLATE.md", "README.md"}

REQUIRED_FIELDS = ["source_id", "stance", "scope", "action"]
PLACEHOLDER_PATTERN = re.compile(r":\s*TBD\b", re.IGNORECASE)


def main() -> int:
    if not PACKS_DIR.exists():
        print(f"OK: {PACKS_DIR.relative_to(ROOT)} does not exist yet; nothing to validate.")
        return 0

    failures = []
    checked = 0
    for path in sorted(PACKS_DIR.rglob("*.md")):
        rel = path.relative_to(PACKS_DIR)
        # Skip staging subdirs and exempt files.
        if rel.parts and rel.parts[0] in STAGING_DIRS:
            continue
        if path.name in EXEMPT_FILENAMES:
            continue
        checked += 1
        text = path.read_text(encoding="utf-8")
        # Promoted stubs must have non-TBD values for the required frontmatter keys.
        for field in REQUIRED_FIELDS:
            field_re = re.compile(rf"^{field}:\s*(.+)$", re.MULTILINE)
            m = field_re.search(text)
            if not m:
                failures.append(f"{path.relative_to(ROOT)}: missing frontmatter key '{field}'")
                continue
            value = m.group(1).strip().strip("'\"")
            if not value or value.upper() == "TBD":
                failures.append(f"{path.relative_to(ROOT)}: '{field}' still TBD; finish before promoting")
        # Catch any residual placeholder lines.
        for n, line in enumerate(text.splitlines(), 1):
            if PLACEHOLDER_PATTERN.search(line):
                failures.append(f"{path.relative_to(ROOT)}:{n}: contains TBD placeholder; finish before promoting")

    if failures:
        print(f"FAIL: {len(failures)} issue(s) in promoted source-pack stubs")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print(f"OK: {checked} promoted source-pack stub(s) clean (no TBD placeholders).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
