# CompassBear Output Gallery

These are compact, anonymized output shapes for testing and demonstration. They
show the expected structure, not field-specific truth.

## Council memo shape

**Decision question:** Should the project be framed as a mechanism paper, method
paper, platform paper, or application paper?

| Lens / role | Verdict | Strongest asset | Biggest risk |
|---|---|---|---|
| Field Builder | platform-first | connects scattered observations into a design rule | novelty may look incremental without a rule |
| Mechanism Purist | demote mechanism | trend is interesting but alternatives remain | mechanism language invites specialist attack |
| Methods Skeptic | method-secondary | workflow is useful as selection support | insufficient benchmark for methods-first claim |
| Figure Architect | rebuild Figure 2 | a clean proof path is possible | current main figure mixes proof and decoration |

**Synthesis:** Frame as a material-platform paper with a bounded mechanistic
model. Keep the discovery workflow as an enabling route, not the central claim.

## Claim passport shape

| Claim ID | Claim | Evidence owner | Strength | Reviewer attack | Demotion wording | Status |
|---|---|---|---|---|---|---|
| C1 | tested systems show tunable response under condition X | Fig. 2a-c | supportive | only three examples | observed across the tested set | open |
| M1 | behavior arises from pathway Y | Fig. 3 + source notes | suggestive | alternative pathway not excluded | is consistent with pathway Y | demote |

## Figure spine shape

| Figure | Figure-level claim | Main panels | Extended/SI support | Risk |
|---|---|---|---|---|
| Fig. 1 | defines the system and design space | schematic, library map, selection logic | full synthetic table | schematic may overstate generality |
| Fig. 2 | demonstrates performance trend | core measurements and controls | replicate traces | control placement must be visible |
| Fig. 3 | tests mechanism model | perturbation, comparison, orthogonal readout | additional controls | mechanism wording must stay bounded |

## Reviewer-risk map shape

| Attack | Where it hits | Severity | Response |
|---|---|---:|---|
| mechanism is inferred from correlation | Abstract, Fig. 3, Discussion | high | demote wording or add discriminating control |
| AI workflow is under-benchmarked | Methods, cover letter | medium | present it as prioritization, not as a standalone method |
| application claim exceeds validation | title, conclusion | high | narrow to proof-of-concept under tested conditions |

## Submission gate shape

**Must-fix before submission**

| Claim | Risk | Fix |
|---|---|---|
| universal design rule | tested set is too narrow | demote to "design principle for the tested family" |

**Downstream propagation**

| Change | Update locations |
|---|---|
| mechanism -> mechanistic model | title, Abstract sentence 3, Fig. 3 caption, cover letter paragraph 2 |
