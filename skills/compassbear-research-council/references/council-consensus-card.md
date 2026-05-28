# Council Consensus Card

The final card from any local named-lens council session. It is the only
output that is allowed to make a "council decided X" claim. Without this card,
individual lens recommendations remain advisory.

## Signature rule

Every major recommendation must record:

- proposer: the lens or anonymous role that introduced the recommendation;
- signed by: lenses or roles that accept the wording/action;
- dissented by: lenses or roles that reject or narrow it, with the reason;
- overruled by: evidence, veto rule or editor decision that changed the outcome;
- downstream effect: manuscript, figure, title, claim hierarchy, cover letter or rebuttal.

Do not write "the council agrees" unless the signers and dissenters are visible.

## Header

- Session ID: `YYYY-MM-DD_<topic-slug>`
- Roster active: list of lens IDs plus anonymous roles
- Decision question: one sentence
- Evidence basis: link to `outputs/literature-rag/evidence_matrix.json` if RAG was run, plus load-bearing source-pack IDs

## Joint decisions

For each major decision, record signers and dissenters. Unanimous is fine.
Split decisions are also fine when the conflict is traceable.

| Decision | Wording adopted | Proposed by | Signed by | Dissented by | Overruled by / tiebreaker |
|---|---|---|---|---|---|
| Central claim | "..." |  |  |  |  |
| Title framing | "..." |  |  |  |  |
| Figure spine | "..." |  |  |  |  |
| Claim demotion | adopt demoted wording |  |  |  |  |
| AI loop visibility | "model-assisted prioritization", not "autonomous discovery" |  |  |  |  |

## Conflicts not yet resolved

Leave this table populated when the session stops. Unresolved conflict is
honest; default "all agreed" is a routing failure.

| Conflict | Lens A position | Lens B position | Evidence that would break the tie | Owner | Due |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Veto log

Any veto exercised this session must be logged with the reason and source-card
rule.

| Lens / role | Vetoed | Reason | Source rule |
|---|---|---|---|
|  |  |  |  |

## Promotions and demotions

| Claim | From level | To level | Triggered by |
|---|---|---|---|
|  |  |  |  |

Levels follow `references/debate-to-decision.md`:
title/abstract -> main-text -> discussion -> SI -> drop.

## Next actions

Use a one-week horizon unless the user asks for a longer project plan.

| Action | Owner | Lens that demanded it | Done when |
|---|---|---|---|
|  |  |  |  |

## Signature line

This card is binding for downstream documents until a later card with a newer
session ID supersedes it.

- Generated: `<timestamp>`
- Roster hash: `<activated lens IDs, sorted and joined by +>`
