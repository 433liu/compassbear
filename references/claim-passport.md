# Claim Passport

Use a Claim Passport when a project has multiple figures, lenses, claims, or
submission documents that must stay synchronized.

The passport is a traceability record. It prevents a strong sentence in the
Abstract from being supported only by a weak panel, background citation, or
mentor preference.

## Minimal passport

| Field | Meaning |
|---|---|
| Claim ID | Stable short ID, e.g. `C1`, `M2`, `A1` |
| Claim text | Exact current wording |
| Claim level | paper / section / figure / panel / sentence |
| Evidence owner | figure, table, method, dataset, source note or experiment |
| Evidence strength | decisive / supportive / suggestive / contextual / missing / contradicted |
| Scope | material class, condition, model, organism, dataset, time window or context |
| Reviewer attack | most likely objection |
| Demotion wording | safer wording if evidence is insufficient |
| Downstream locations | title, abstract, figure caption, cover letter, SI, rebuttal, patent claim |
| Status | locked / open / demote / needs evidence / remove |

## Full passport

| Claim ID | Claim | Level | Evidence owner | Strength | Scope | Source basis | Reviewer attack | Demotion wording | Downstream locations | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| C1 |  | paper |  |  |  |  |  |  |  | open |

## Evidence strength rules

- **Decisive**: directly tests the claim and rules out the main alternative.
- **Supportive**: strongly supports the claim but leaves some boundary or
  mechanism uncertainty.
- **Suggestive**: points in the claimed direction but needs independent support.
- **Contextual**: helps the story but does not prove the claim.
- **Missing**: the claim is not yet supported by the supplied material.
- **Contradicted**: supplied evidence or literature pushes against the claim.

## Claim demotion ladder

Use the weakest honest verb that still preserves the scientific point:

| Over-strong wording | Demote to |
|---|---|
| proves | supports / is consistent with |
| establishes mechanism | suggests a possible mechanism / supports a mechanistic model |
| universal / general | observed across the tested set / under the tested conditions |
| enables application | demonstrates a proof-of-concept for |
| AI discovered | AI-guided prioritization identified / accelerated selection of |
| sustainable / green | potentially more sustainable under the stated assumptions |

## Passport workflow

1. Extract or draft claims.
2. Assign each claim an evidence owner.
3. Tag evidence strength and scope.
4. Add the most plausible reviewer attack.
5. Write the demotion wording before final prose.
6. Propagate any claim change to downstream documents.

## Output rule

When the user asks for a high-stakes rewrite, final check, cover letter or
rebuttal, return a compact passport for the load-bearing claims before or after
the prose if claim drift is likely.
