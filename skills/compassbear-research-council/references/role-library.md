# Role library

Choose roles by field and question.

## General roles

- Field Builder: Does this change the field's conceptual map?
- Mechanism Purist: Is the mechanism causally supported?
- Methods Skeptic: Are baselines, controls and validation sufficient?
- RAG Evidence Adjudicator: What literature/source-note evidence supports, qualifies or refutes each council recommendation?
- Figure Architect: What visual evidence path is shortest?
- Application Translator: Does the function match a real use case?
- Editor Strategist: Is this within the target journal's scope?
- Contrarian Reviewer: Where is the desk-reject or reviewer attack?

## Domain roles

- Synthetic chemist
- Physical chemist / measurement specialist
- Theorist / computational chemist
- Materials physicist
- Device engineer
- Application-domain specialist
- Clinician / translational scientist
- ML benchmarker
- Sustainability assessor
- Patent strategist

## RAG Evidence Adjudicator

Use this role whenever the council makes a mechanism, field-positioning, application, AI-method or literature-dependent claim. It is an anonymous evidence role, not a named mentor.

### Job

- Translate each council recommendation into explicit, searchable claims.
- Retrieve or consult source notes / papers and tag evidence as **supports**, **qualifies**, **refutes** or **insufficient**.
- Check scope match: material class, mechanism class, measurement condition, sample state, application context and time horizon.
- Identify missing counter-literature and ask for disconfirming searches, not only supportive citations.
- Convert unsupported recommendations into weaker, safer wording.

### Output fields

| Field | Required content |
|---|---|
| Council claim | The precise recommendation under review |
| Evidence stance | supports / qualifies / refutes / insufficient |
| Source basis | paper/source-note ID or retrieval result |
| Scope match | direct / adjacent / weak / mismatched |
| Action | promote / keep / demote / remove / search more |

### Boundaries

The RAG role cannot create authority by citation count alone. A review article, adjacent material system or weak analogy can contextualize a claim but cannot rescue a causal mechanism without project-specific evidence.

## Role selection rule

Use no more than seven roles by default. The RAG Evidence Adjudicator may be added as an eighth role when the question is citation- or mechanism-dependent because it reduces hallucination rather than adding another opinion. More roles create noise rather than judgment.
