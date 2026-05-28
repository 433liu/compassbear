# DOI / PDF / Source Ingestion

Use this protocol when the user provides a DOI, paper title, abstract, pasted
full-text excerpt, PDF text, or asks to turn a paper into a source note or mentor
lens update.

The goal is to make literature support easier without pretending metadata is
evidence.

## Modes

| Input | Best workflow | Output |
|---|---|---|
| DOI or title | chat-native lookup first | citation candidate + stance/scope if abstract is available |
| abstract pasted by user | in-chat candidate check | provisional source-note fields |
| full-text excerpt pasted | source-note draft | stronger stance/scope/action |
| PDF file path | `skills/compassbear-pdf-reader/` + `scripts/pdf_extract.py` | extracted text + source-note worksheet |
| PDF text provided | source-note draft + candidate lens rules | source-backed rules if scope matches |
| local Zotero query | `references/local-zotero-read.md` | title/author/DOI/PDF path report + source-note candidates |
| many DOI/title candidates | script RAG or Zotero handoff | batch stubs |

## Default chat workflow

1. Identify the claim the source is supposed to support or challenge.
2. Extract bibliographic information from DOI/title/pasted source.
3. Read the available abstract or user-provided text.
4. Assign:
   - stance: supports / qualifies / refutes / insufficient;
   - scope: direct / adjacent / weak / mismatched;
   - action: promote / keep / demote / remove / search-more.
5. Produce a source-note draft when the user wants persistent memory.
6. If the source updates a mentor lens, propose candidate lens rules but do not
   activate them without enough source basis.

## Source-note output

| Field | Value |
|---|---|
| Source ID | S_ |
| Citation / DOI |  |
| Claim under adjudication |  |
| Stance | supports / qualifies / refutes / insufficient |
| Scope match | direct / adjacent / weak / mismatched |
| Action | promote / keep / demote / remove / search-more |
| Load-bearing finding |  |
| Caveat / boundary |  |
| Candidate lens rule |  |

## Escalate to Zotero when

- the paper is paywalled and the user needs institutional PDF access;
- multiple papers must be read and tagged;
- citation export is needed;
- a source should become part of a formal source pack.

## Guardrails

- DOI metadata alone is never support.
- Abstract-level evidence must be labeled provisional.
- Full-text excerpts supplied by the user can support a source note if the
  excerpt contains the relevant evidence, method or limitation.
- Do not invent article details if a DOI/title lookup is incomplete.
- Do not create mentor-lens veto rules from one isolated paper unless the scope
  is explicitly narrow.
