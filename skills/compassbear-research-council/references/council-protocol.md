# Council protocol

Use a three-round structure plus a final consensus card when local named lenses
or explicit council voting are used.

## Round 0 — Intake

Collect or infer:

- field and target audience;
- central uncertainty;
- evidence already available;
- possible paper angles;
- target journal or venue;
- constraints such as time, experiments, data access or IP.

If input is incomplete, state assumptions and proceed.

## Round 1 — Independent diagnosis

Each role provides:

- strongest asset;
- weakest claim;
- likely reviewer concern;
- recommended framing.

Keep each diagnosis short.

## Evidence hearing — RAG check

When the decision depends on literature, run the RAG Evidence Adjudicator before cross-examination. For each major recommendation, assign:

- evidence stance: supports / qualifies / refutes / insufficient;
- scope match: direct / adjacent / weak / mismatched;
- action: promote / keep / demote / remove / search more.

The evidence hearing can demote a lens recommendation, but it cannot invent project data.

For major mechanism, application, AI-discovery or journal-positioning claims,
run or draft at least two adversarial queries:

1. an alternative-explanation query;
2. a boundary / counterexample / failed-control query.

If the user is iterating in chat and does not want to switch to the terminal,
use the lite RAG modes in `rag-evidence-adjudicator.md`: query-plan mode or
in-chat candidate mode. Lite RAG is for iteration only; it does not replace the
full `literature_rag.py` + Zotero/source-pack promotion workflow.

## Round 2 — Cross-examination

Identify tensions:

- mechanism vs application;
- model novelty vs material novelty;
- strong result vs weak generality;
- exciting claim vs insufficient evidence;
- main figure vs Extended/SI allocation.

## Round 3 — Convergence

Return a decision:

- keep as main claim;
- demote to support;
- move to SI;
- collect evidence;
- remove or postpone.

The final answer must be a decision memo, not a transcript.

## Consensus card

When local named-lens mode, active lens IDs or explicit council voting is
used, end with a Council Consensus Card. Follow
`references/council-consensus-card.md`.

The card is the only section allowed to say "the council decided". Earlier
rounds are advisory diagnoses unless they are signed into the card.

Every major decision row must show:

- proposed by;
- signed by;
- dissented by;
- overruled by / tiebreaker;
- downstream effect.

If disagreement remains unresolved, preserve it in the conflicts table instead
of smoothing it into a false consensus.

Round 4 retrospective is optional and should be used only after conflict,
RAG-overrule or missing-lens sessions. Do not force it into routine council
answers.
