#!/usr/bin/env python3
"""Lightweight regression guard for the RAG Evidence Adjudicator test spec.

This does not execute an LLM. It prevents the test markdown from regressing back
into a single broad expected-behavior checklist by requiring all three distinct
verdict paths to remain present: promote, demote and search more.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TEST_PATH = ROOT / "skills/compassbear-research-council/tests/rag-evidence-adjudicator.md"
text = TEST_PATH.read_text(encoding="utf-8")
text_lower = text.lower()

required_scenarios = {
    "Mini-scenario A — promote": r"mini-scenario\s+a\s+[—-]\s+promote",
    "Mini-scenario B — demote": r"mini-scenario\s+b\s+[—-]\s+demote",
    "Mini-scenario C — search more": r"mini-scenario\s+c\s+[—-]\s+search\s+more",
}
required_actions = {
    "Expected action: promote": r"expected\s+action:\s*\*\*promote\*\*",
    "Expected action: demote": r"expected\s+action:\s*\*\*demote\*\*",
    "Expected action: search more": r"expected\s+action:\s*\*\*search\s+more\*\*",
}
required_invariants = [
    "supporting and adversarial sources",
    "two adversarial checks",
    "scope match",
    "avoid invented citations",
]

failures = []
for label, pattern in {**required_scenarios, **required_actions}.items():
    if not re.search(pattern, text_lower):
        failures.append(f"missing {label}")
for phrase in required_invariants:
    if phrase not in text_lower:
        failures.append(f"missing invariant phrase: {phrase}")

if failures:
    print(f"FAIL: {TEST_PATH.relative_to(ROOT)}")
    for failure in failures:
        print(f"  - {failure}")
    sys.exit(1)

print(f"OK: {TEST_PATH.relative_to(ROOT)} — promote/demote/search-more scenarios present")
