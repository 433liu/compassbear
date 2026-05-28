# Production Suite Roadmap

This roadmap converts CompassBear's current shortboards into an implementation
plan. It should be used after competitor reviews or user feedback when the user
asks how to make the skill more tool-like without losing its judgment layer.

## First-principles diagnosis

CompassBear should not become a generic automation pile. It should become a
production suite for one loop:

`claim -> evidence -> figure -> text -> journal -> reviewer defense -> source traceability`

Tooling is valuable only when it makes this loop faster, more traceable or less
error-prone.

## Upgrade tracks

| Shortboard | Target state | Minimum useful implementation | Done signal |
|---|---|---|---|
| Tooling not mature | one local command surface for checks, RAG and protocol discovery | `scripts/cb.py` with `doctor`, `checks`, `protocols`, `examples`, `rag` | user no longer has to remember every script |
| Literature retrieval friction | chat-first RAG plus DOI/PDF/source-note handoff | `chat-native-rag.md`, `pdf-source-ingestion.md`, Zotero bridge | source can move from chat candidate to promoted note |
| Figure production weak | figure logic converts into production specs for matplotlib/SVG/PPT/imagegen | `figure-production-bridge.md` | each figure request yields claim map + asset spec |
| Few public examples | anonymized benchmark suite and output gallery | `examples/benchmark-suite.md`, output snapshots | new behavior can be tested by prompts |
| Not marketplace-like | public/private release gate and install surface | `public-private-split.md`, `USAGE.md`, package checklist | private files can be stripped safely |

## Capability map

| Layer | Current state | Next improvement |
|---|---|---|
| Chat UX | good for judgment, improving for RAG | add more copy-paste prompt recipes |
| CLI | fragmented scripts | use `scripts/cb.py` as unified local helper |
| RAG | provider script + chat protocol | add DOI/PDF ingestion and source-note promotion examples |
| Figures | logic strong, production weak | output production specs and code-ready data requirements |
| Examples | sparse | build benchmark suite with anonymized cases |
| Packaging | private fork | add release checklist and optional public package layout |

## Unified command surface

Use chat for normal work. Use the local command surface when repeatability is
needed:

```bash
python scripts/cb.py doctor
python scripts/cb.py protocols
python scripts/cb.py examples
python scripts/cb.py checks
python scripts/cb.py rag --claim "<claim>" --profile materials-mechanism --with-html-review
```

Do not turn every protocol into a command. A command is justified only when it
executes repeatable local work.

## Milestones

### M1: Usability hardening

- unified local helper;
- updated usage examples;
- benchmark prompt list;
- all current checks pass.

### M2: Literature handoff

- DOI/PDF/source-note workflow;
- pasted abstract/full-text pathway;
- Zotero pull/push examples;
- claim-to-source promotion examples.

### M3: Figure production bridge

- figure-spec output;
- matplotlib/SVG/PPT handoff prompts;
- visual-generation boundary preserved;
- example figure gallery with anonymized data placeholders.

### M4: Public package readiness

- private/public strip checklist;
- example gallery contains no project-private data;
- installation docs are current;
- release smoke test passes.

## Guardrails

- Keep chat-native judgment as the default.
- Keep generated visuals separate from measured data.
- Do not add commands that only wrap a prompt.
- Do not add public examples from private user material.
- Every new tool must preserve source traceability and claim demotion.
