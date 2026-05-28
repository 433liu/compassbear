#!/usr/bin/env python3
"""Static QA guard for the integrated literature RAG + Zotero handoff helpers."""
from pathlib import Path
import py_compile
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/literature_rag.py"
ZOTERO_SCRIPT = ROOT / "scripts/zotero_sync.py"
PROMOTION_SCRIPT = ROOT / "scripts/check_source_pack_promotion.py"
RAG_REF = ROOT / "skills/compassbear-research-council/references/rag-evidence-adjudicator.md"
ROOT_SKILL = ROOT / "SKILL.md"
ENV_EXAMPLE = ROOT / ".env.example"

failures = []
for path in [SCRIPT, ZOTERO_SCRIPT, PROMOTION_SCRIPT]:
    if not path.exists():
        failures.append(f"required script missing: {path.relative_to(ROOT)}")
        continue
    try:
        py_compile.compile(str(path), doraise=True)
    except Exception as exc:  # noqa: BLE001
        failures.append(f"{path.relative_to(ROOT)} does not compile: {exc}")

script_text = SCRIPT.read_text(encoding="utf-8") if SCRIPT.exists() else ""
zotero_text = ZOTERO_SCRIPT.read_text(encoding="utf-8") if ZOTERO_SCRIPT.exists() else ""
rag_text = RAG_REF.read_text(encoding="utf-8")
skill_text = ROOT_SKILL.read_text(encoding="utf-8")
env_text = ENV_EXAMPLE.read_text(encoding="utf-8") if ENV_EXAMPLE.exists() else ""

required_script_terms = [
    "semantic_scholar", "crossref", "openalex", "europepmc", "arxiv", "serper",
    "upgrade_with_unpaywall",
    "--support-query", "--adversarial-query", "--no-unpaywall",
    "evidence_matrix.md",
    # stub TODO checklist must be present so the human-in-the-loop step is explicit
    "TODO before promotion",
    "stance: TBD",
]
required_zotero_terms = [
    "ZOTERO_API_KEY", "ZOTERO_USER_ID",
    "cb/stance/", "cb/scope/", "cb/action/", "cb/ready",
    "parse_cb_tags",
    "push", "pull",
]
required_env_terms = [
    "SEMANTIC_SCHOLAR_API_KEY", "OPENALEX_API_KEY", "UNPAYWALL_EMAIL", "SERPER_API_KEY",
    "ZOTERO_API_KEY", "ZOTERO_USER_ID", "ZOTERO_LIBRARY_TYPE",
]

# Orphan-key guard: LENS_API_KEY is exposed but not wired up — must be flagged as such.
if "LENS_API_KEY" in env_text and "not used" not in env_text.lower():
    failures.append(".env.example exposes LENS_API_KEY without a 'not used' note (orphan key)")

for term in required_script_terms:
    if term not in script_text:
        failures.append(f"literature_rag.py missing term: {term}")
for term in required_zotero_terms:
    if term not in zotero_text:
        failures.append(f"zotero_sync.py missing term: {term}")
for term in required_env_terms:
    if term not in env_text:
        failures.append(f".env.example missing term: {term}")

if "Integrated retrieval workflow" not in rag_text or "scripts/literature_rag.py" not in rag_text:
    failures.append("RAG adjudicator reference does not describe integrated retrieval workflow")
if "Human-in-the-loop step" not in rag_text:
    failures.append("RAG adjudicator reference does not document the Human-in-the-loop step")
if "scripts/zotero_sync.py" not in rag_text:
    failures.append("RAG adjudicator reference does not document the Zotero handoff")
if "Literature-grounded claim check" not in skill_text or "scripts/literature_rag.py" not in skill_text:
    failures.append("root SKILL.md does not route literature-grounded claim checks to literature_rag.py")

# Document the school-database limitation somewhere visible.
if not any("institutional API" in t or "TDM" in t for t in (env_text, rag_text)):
    failures.append("school-database / institutional API limitation is not documented anywhere")

if failures:
    print("FAIL: integrated literature RAG + Zotero handoff QA")
    for failure in failures:
        print(f"  - {failure}")
    sys.exit(1)

print("OK: literature RAG + Zotero handoff helpers present and statically valid")
