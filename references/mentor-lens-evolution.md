# Mentor Lens Evolution Protocol

Use this protocol when the user wants to improve a private mentor or professor
lens after reading papers, reviews, talks, interviews, grant summaries, lab
statements or other public source materials.

The goal is not to imitate a real person. The goal is to convert source reading
into traceable decision standards.

If the user wants to record their own personal taste or PI-style preferences,
use `references/user-preference-lens.md` instead. Personal preference is useful,
but it is not a source-backed mentor lens and should not be mixed with scholar
source notes.

If the user asks to use papers already stored in local Zotero, use
`references/local-zotero-read.md` to find title/author/DOI/PDF paths in read-only
mode, then convert the read paper or excerpt into source notes before updating
the mentor lens.

## Core rule

Evolve a mentor lens only through source-backed rules:

`source note -> reusable lens rule -> veto or demotion rule -> optional roster activation`

Do not add personal preferences, private opinions, writing quirks, jokes, or
unverified claims about a scholar.

## Source note step

For each source, create or update a note under `source-packs/` using
`_SOURCE_NOTE_TEMPLATE.md`.

The note should capture:

- what question the source tries to answer;
- what evidence it treats as decisive;
- what evidence it treats as suggestive;
- what controls, comparisons or baselines it relies on;
- how the source defines novelty;
- how the source limits scope;
- what reusable rule can be extracted.

## Promotion threshold

| Lens status | Minimum source basis | Allowed use |
|---|---|---|
| Seed | named idea only, no source notes | do not use as named lens |
| Draft | 1-2 source notes | can inform background thinking, no decisive vote |
| Provisional | at least 3 source notes for a narrow lens | may join council with low-confidence tag |
| Ready | at least 3 strong source notes for narrow lens, 5-8 for broad lens | may sign, dissent or veto within its scope |
| Mature | multiple source types and tested council memos | may be a lead lens for its axis |

## Lens update fields

Every active lens should maintain:

- `last_updated`;
- `source_note_count`;
- `confidence`: low / medium / high;
- `scope`: narrow / medium / broad;
- `active_status`: seed / draft / provisional / ready / mature;
- `calibration_notes`;
- `evolution_log`.

## Rule quality test

A lens rule is usable only if it passes all tests:

1. It is traceable to one or more source IDs.
2. It states a decision consequence, not only a topic preference.
3. It can demote, redirect or request evidence.
4. It does not claim private knowledge.
5. It has a use boundary.

Weak rule:

> This lens likes strong mechanisms.

Usable rule:

> This lens demotes a mechanism claim to a correlation claim unless the manuscript
> includes a perturbation, comparison, or time-resolved/control experiment that
> distinguishes the proposed pathway from the main alternative. Supported by:
> S1, S3.

## Evolution workflow

1. Add source note.
2. Extract 1-3 candidate rules.
3. Map each rule to claim-demotion or signature-figure demand.
4. Update the lens card's source basis and evolution log.
5. Re-run the local lens checker.
6. If the lens becomes ready, update the project roster.

## Council behavior

When an evolved lens is used in private council:

- label it as a source-based lens;
- name the rule or source basis behind any veto;
- let the RAG Evidence Adjudicator challenge it;
- expose signers and dissenters in the Council Consensus Card when decisions
  affect manuscript, cover letter, rebuttal or patent text.

## Anti-patterns

Do not:

- write in the professor's voice;
- invent unpublished preferences;
- treat a single paper as a broad worldview;
- use a famous name to bypass evidence;
- let a lens override data without explaining the source-backed rule.
