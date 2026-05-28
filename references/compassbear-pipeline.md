# CompassBear Pipeline Mode

Use pipeline mode when the user wants end-to-end help on a manuscript, proposal,
rebuttal package, or high-stakes project rather than a single paragraph or
figure.

## Pipeline contract

Pipeline mode turns a project into a sequence of decision gates. Do not advance
to the next gate by making weak assumptions look settled. If a gate fails, return
the failure reason, the claim demotion, and the next action needed to reopen the
gate.

## Six stages

| Stage | Question | Output | Hard gate |
|---|---|---|---|
| 1. Project Brief | What is the project trying to become? | one-page project brief | field, target audience, central object, strongest evidence and intended venue are identifiable |
| 2. Claim Hierarchy | What must the reader believe? | paper-level, section-level, figure-level and paragraph-level claim map | every major claim has a stated evidence owner |
| 3. Evidence Spine | What makes the claim unavoidable? | evidence ladder and missing-evidence list | primary claim is supported by primary evidence, not only context or analogy |
| 4. Figure Strategy | What is the shortest visual proof path? | main/Extended/SI figure spine and panel map | each main panel defends a necessary claim |
| 5. Manuscript Package | What text and support documents carry the claim? | title, abstract, Results skeleton, cover letter/rebuttal/SI plan as needed | wording matches the evidence level and cross-document terms stay consistent |
| 6. Submission Risk Audit | What will reviewers attack first? | integrity gate report and final action list | unresolved risks are either fixed, disclosed, or explicitly demoted |

## Stage 1: Project Brief

Return:

- field and subfield;
- target reader and likely reviewer types;
- central object, system, method or phenomenon;
- intended contribution type: mechanism, method, platform, application, dataset,
  theory, or hybrid;
- strongest existing evidence;
- highest-risk intended claim;
- target venue tier or audience.

## Stage 2: Claim Hierarchy

Build claims at these levels:

1. **Paper claim** - the reason the paper exists.
2. **Section claims** - the logical steps needed for the paper claim.
3. **Figure claims** - the visual proof steps.
4. **Panel claims** - the atomic evidence units.
5. **Sentence claims** - the language that must not exceed the evidence.

If the user gives only data, infer a provisional claim hierarchy and mark it
`provisional`.

## Stage 3: Evidence Spine

Classify evidence as:

- decisive;
- supportive;
- suggestive;
- contextual;
- missing;
- contradictory or boundary-setting.

For mechanism, application, AI-discovery, clinical, sustainability or deployment
claims, include at least one adversarial check: an alternative explanation,
failed control, boundary condition, or counterexample.

## Stage 4: Figure Strategy

Use the figure-strategy skill. Every figure must pass:

- removal test: if removed, what claim collapses?
- redundancy test: is this panel only repeating another panel?
- scope test: does the caption overstate what the data show?
- placement test: main, Extended Data or SI?

## Stage 5: Manuscript Package

Draft only after the claim and evidence levels are stable enough. Use calibrated
language:

- `demonstrates` only when the result directly proves the claim;
- `supports` when the evidence is strong but not exhaustive;
- `suggests` when alternatives remain;
- `is consistent with` when the evidence is compatible but not diagnostic;
- `may` / `could` when the claim is hypothesis-level.

## Stage 6: Submission Risk Audit

Run the submission integrity gates before final wording. The output should split
issues into:

- **must-fix before submission**;
- **acceptable if disclosed or demoted**;
- **nice-to-have polish**;
- **downstream documents to update**.

## Stop rule

When the project has passed the relevant gates, stop broad restructuring. Return
what is locked, what remains open, and which document should be edited next.
