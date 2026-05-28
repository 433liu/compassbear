# Test: RAG Evidence Adjudicator

This test ensures the RAG Evidence Adjudicator behaves as a discriminating evidence role, not as a decorative citation generator. It should extract checkable claims, inspect supporting and adversarial evidence, judge scope match, and return an action that can change the council decision.

## Mini-scenario A — promote

### Prompt

Use the council to decide whether the claim can be promoted from Results text to a main-figure mechanism panel:

> Surface-treated material A remains stable under accelerated aging because treatment B suppresses the dominant degradation pathway.

Available evidence includes a matched treatment-loading series, time-dependent stability data, morphology statistics showing fewer defect sites at higher treatment loading, mechanistic simulations showing lower degradation propensity, and two source notes reporting analogous stabilization behavior in related material systems. Contamination and batch-history controls are negative.

### Expected behavior

- Include the RAG Evidence Adjudicator as an anonymous evidence role.
- Extract a checkable mechanism claim: treatment loading changes defect formation, and the changed defect landscape plausibly explains the improved stability.
- Tag evidence stance as **supports with scope match**, while noting that causality still depends on the matched series and controls.
- Expected action: **promote**, but only to a mechanism panel or calibrated Results claim; do not promote to universal mechanism language.
- Do not state that any named professor personally endorses the mechanism.

## Mini-scenario B — demote

### Prompt

Use the council to decide whether this claim can stay in the Abstract:

> The prototype improves application performance with no efficiency trade-off.

Available evidence includes one performance improvement relative to a baseline. However, the same dataset shows higher energy use under the prototype condition, no matched process-control experiment, and no source note supporting a no-trade-off claim.

### Expected behavior

- Extract two claims separately: application performance improvement and no-efficiency-trade-off.
- Tag application performance as **partly supported** but the no-trade-off claim as **refuted or contradicted by project data**.
- Expected action: **demote** the Abstract claim. Keep a narrower Results-level statement such as “the prototype improved the tested performance metric under this condition,” while explicitly avoiding “no trade-off.”
- Require matched process controls and an efficiency accounting before any broad no-trade-off claim can be promoted.

## Mini-scenario C — search more

### Prompt

Use the council to decide whether this claim can be used as a mechanistic bridge:

> A longer substituent series improves stability because it increases free volume and reduces reactive-site contact.

Available evidence includes a small substituent series and a stability trend, but no contact-distance analysis, no density/free-volume calculation, and no source notes on substituent-controlled free-volume effects in this material family.

### Expected behavior

- Extract the claim as a proposed structure--packing--stability bridge, not as an established mechanism.
- Tag the evidence stance as **insufficient / scope uncertain**: the trend exists, but the proposed free-volume/contact mechanism is not yet evidenced.
- Expected action: **search more** and hold the claim at hypothesis level. Request targeted literature/source notes and project analyses such as RDF, free-volume proxy, density, Tg, conformer/contact distributions, or matched side-chain controls.
- Do not demote all side-chain observations; demote only the causal free-volume/contact explanation until evidence arrives.

## Global invariants

Across all scenarios, the adjudicator must:

- Request or inspect supporting and adversarial sources when the claim depends on literature.
- Use two adversarial checks for major claims: one alternative-explanation query and one boundary / counterexample / failed-control query.
- Separate direct support, adjacent analogy, contradiction and missing evidence.
- Tag evidence stance and scope match before recommending promote / demote / search more.
- Avoid invented citations and avoid claiming that a named professor personally endorses a mechanism.
