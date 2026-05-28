# CompassBear Benchmark Suite

This is a public-safe benchmark prompt set for evaluating CompassBear behavior.
Use anonymized or synthetic scientific content only.

## Benchmark categories

| Category | What it tests | Expected output |
|---|---|---|
| Claim discipline | unsupported mechanism or application language | demotion wording + reviewer risk |
| Chat-native RAG | source-backed claim check | stance/scope/action + citations when tools allow |
| Claim Passport | cross-document claim traceability | passport table + downstream updates |
| Journal positioning | JACS / Angew / AM style conversion | fit judgment + title/abstract options |
| Figure strategy | panel logic and main/Extended/SI split | panel-to-claim map + risk notes |
| Figure production bridge | logic-to-asset handoff | production spec + forbidden generated elements |
| Mentor lens evolution | paper-to-lens update | source note + candidate rule + activation warning |
| Submission gates | final audit | must-fix / demote-disclose / polish / propagation |
| First-principles iteration | skill improvement decisions | adopt/adapt/reject matrix |
| Visual-heavy PDF reading | slide-exported spectra/tables with poor text extraction | extraction-quality warning + rendered page-review assets before claim/style judgment |

## Prompt set

### 1. Claim discipline

```text
This abstract claims that our material proves a universal mechanism from three
samples and steady-state spectra. Audit the claim and rewrite safely.
```

### 2. Chat-native RAG

```text
Use RAG to check whether this claim is supported: material A remains stable
under accelerated aging because treatment B suppresses the dominant degradation
pathway.
Return support and adversarial sources.
```

### 3. Claim Passport

```text
Build a Claim Passport for these three claims: the model prioritized the best
candidate; the treatment improves stability; the prototype improves application
performance under the tested condition.
```

### 4. Journal positioning

```text
Compare JACS, Angew and Advanced Materials fit for this story, then rewrite the
title and opening two abstract sentences for the best two targets.
```

### 5. Figure strategy

```text
Figure 2 has synthesis scope, stability measurements, performance metrics,
mechanism controls and an application photograph. Decide main/Extended/SI
placement and reviewer risks.
```

### 6. Figure production bridge

```text
Turn this figure plan into a production spec. Separate measured plots, schematic
panels and conceptual graphical-abstract assets. State what data files are
needed.
```

### 7. Mentor lens evolution

```text
I read this paper. Extract a source note and candidate mentor-lens rule, but do
not impersonate the author or activate the lens from one source.
```

### 8. Submission gates

```text
Run submission integrity gates on this draft and split findings into must-fix,
demote/disclose, nice-to-have and downstream propagation.
```

### 9. First-principles iteration

```text
This competitor has a PDF-to-PPT feature. Decide whether CompassBear should
adopt, adapt, reject or defer it using first-principles iteration.
```


### 9. Visual-heavy PDF reading

```text
Read this slide-exported PDF of spectra, tables and photographs, then determine article style: <path-to-local-pdf>
```

Expected behavior: run the PDF extractor, notice low-structure/chart-heavy extraction, generate or request rendered page-review assets when possible, and treat visual observations as provisional evidence rather than manuscript text.

## Pass criteria

- Unsupported claims are marked explicitly.
- Evidence level is not upgraded by style conversion.
- RAG output distinguishes support from adversarial/boundary sources.
- Generated imagery is not allowed to stand in for data.
- Mentor lenses remain source-based decision standards, not personalities.
- Improvement requests produce a smallest useful implementation, not feature
  copying.
