# Submission Integrity Gates

Run these gates before final manuscript, cover letter, rebuttal or patent-facing
text. The goal is to catch reviewer ammunition early.

## Gate output

Return findings in this order:

1. **Must-fix before submission**
2. **Can proceed if demoted or disclosed**
3. **Nice-to-have polish**
4. **Downstream propagation**

Each finding should name the claim, evidence owner, risk, and fix.

## Gate 1: Claim Support

Fail if:

- the Abstract or title contains a claim not owned by a figure, table, method,
  dataset or source note;
- the strongest claim is supported only by background literature;
- mechanism language is based only on correlation;
- a universal claim is based on a narrow tested set.

Fix by adding evidence, narrowing scope, or demoting wording.

## Gate 2: Figure-Claim Match

Fail if:

- a main figure panel does not defend a necessary claim;
- a caption states more than the panel shows;
- visual hierarchy makes secondary evidence look primary;
- controls or baselines are buried where the main claim depends on them.

Fix by moving panels, rewriting captions, or changing the figure-level claim.

## Gate 3: Novelty and Priority

Fail if:

- "first", "unprecedented", "universal", "paradigm-shifting" or equivalent
  wording lacks direct literature support;
- the novelty is only a combination of known elements without a stated new
  principle, capability, mechanism or boundary;
- the cover letter overstates venue fit.

Fix by specifying the precise novelty class and boundary.

## Gate 4: Mechanism Standard

Fail if:

- the claim says mechanism but the data only show association;
- alternative explanations are not acknowledged or tested;
- missing controls would be obvious to a specialist reviewer;
- time, concentration, structural, perturbation or comparison evidence is needed
  but absent.

Fix by adding the experiment, demoting to a model, or moving speculation to
Discussion with explicit boundaries.

## Gate 5: Application and Translation

Fail if:

- a proof-of-concept is written as deployment;
- model, organism, device, field or operational conditions are not disclosed;
- sustainability, clinical, agricultural or industrial claims exceed the
  validation setting;
- performance comparisons use mismatched baselines.

Fix by narrowing the use case and stating the validation boundary.

## Gate 6: AI / Data-Driven Discovery

Fail if:

- AI is treated as the scientific contribution when the paper is not a methods
  paper;
- training data, search space, descriptors, baseline selection or validation
  split is unclear;
- active learning or LLM assistance is used as authority rather than as an
  auditable selection process;
- selected hits are not experimentally validated.

Fix by turning the AI element into a transparent evidence-routing component or,
if appropriate, upgrading it into a methods claim with proper benchmarks.

## Gate 7: Citation and Source Integrity

Fail if:

- a citation supports only background but is used to prove the paper's claim;
- a source is cited outside its material class, condition or model scope;
- literature is cherry-picked without adversarial checks;
- source notes are placeholders promoted as evidence.

Fix by adding source notes, replacing citations, or marking the claim as
qualified.

## Gate 8: Cross-Document Consistency

Fail if:

- title, Abstract, figures, captions, SI, Methods, cover letter or rebuttal use
  different claim scope;
- numbers, sample names, units or time windows drift;
- a demotion in one document is not propagated elsewhere.

Fix by running a consistency audit and updating downstream locations in the Claim
Passport.
