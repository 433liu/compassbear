# Council Retrospective Template

Run this only after the Council Consensus Card is finalized and only when the
session produced real conflict, an evidence-based overrule or a missing-lens
gap. It is not part of the default council output.

The goal is not to re-debate the decision. The goal is to extract what each
lens learned and turn it into reviewable patches to the lens cards themselves.

## When to run

- After a council session that involved real conflict.
- After the RAG Evidence Adjudicator overruled or qualified a named lens.
- After a session exposed a repeated concern that no active lens owned.

Skip it for routine writing-polish sessions where no lens was challenged.

## 1. What changed in the manuscript / decision

Three lines maximum. State what the council decided that the user did not
already believe going in. If nothing changed, keep the retrospective short.

## 2. Per-lens learning patches

| Lens ID | Was overruled? | By what evidence | Proposed patch |
|---|---|---|---|
|  |  |  |  |

Each proposed patch must be specific enough to apply: rule number or section,
current wording, proposed wording and reason. Do not write vague patches such
as "be more careful about mechanism".

## 3. Cross-pollination notes

Each lens may import at most two questions from a different lens, only when the
question repeatedly fired in this session. Keep imported questions tagged with
the source lens so the original specialty is not erased.

| Lens importing | Question imported from | Question text | Why it fits this lens |
|---|---|---|---|
|  |  |  |  |

## 4. New lens gap

Do not activate a new lens in retrospective. A new named lens requires source
notes under `private-named-lens-protocol.md`.

| Concern | Fired N times | Currently routed to | Should be its own lens? |
|---|---:|---|---|
|  |  |  |  |

## 5. RAG retrieval gap

| Claim that needed counter-evidence | Why retrieval missed it | Fix |
|---|---|---|
|  |  |  |

## 6. Patch application checklist

- [ ] Lens-rule patches reviewed by user.
- [ ] Source basis rows updated with new source IDs.
- [ ] Cross-pollination questions tagged with origin.
- [ ] Retrospective filed at `council-notes/YYYY-MM-DD_<topic>_retro.md`.
- [ ] Consensus card link added at top of retrospective.

## Anti-patterns

- Do not write this as "Claude reflects on its own performance"; it is a
  lens-card maintenance document.
- Do not let a lens import another lens's question to dilute its specialty.
- Do not auto-merge patches. Lens-card changes require explicit human review.
- Do not skip retrospective when RAG overruled anyone.
