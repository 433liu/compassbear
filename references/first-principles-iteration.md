# First-Principles Skill Iteration

Use this reference when improving CompassBear by studying other academic skills,
plugins, AI research assistants, journal tools, writing workflows or user
failures.

The goal is not to copy features. The goal is to identify the irreducible user
problem, then build the smallest CompassBear-native capability that improves
research judgment, evidence discipline or manuscript execution.

## North-star

CompassBear should become better at one thing:

> turning uncertain scientific material into defensible claims, evidence paths,
> figures, text, journal positioning and reviewer defense.

Every new feature must strengthen this loop or support it cleanly.

## First-principles filter

For any proposed feature, answer these questions before adding it:

1. **What user pain does this remove?**
   - Is it judgment pain, workflow friction, formatting labor, retrieval labor,
     or packaging labor?

2. **What primitive does it improve?**
   - claim clarity;
   - evidence retrieval;
   - evidence adjudication;
   - figure-as-argument;
   - journal fit;
   - writing calibration;
   - reviewer defense;
   - source traceability;
   - private mentor learning;
   - public/package usability.

3. **What is the failure mode if we add it badly?**
   - overclaim;
   - fake certainty;
   - decorative citations;
   - tool bloat;
   - private data leakage;
   - workflow complexity;
   - weak examples;
   - outputs that look polished but are scientifically unsafe.

4. **What is the smallest useful version?**
   - protocol only;
   - prompt/output template;
   - source-backed reference;
   - script;
   - checker;
   - example gallery;
   - full sub-skill.

5. **How will we know it works?**
   - realistic test prompt;
   - before/after example;
   - regression checker;
   - user workflow reduction;
   - fewer unsupported claims;
   - clearer journal fit decision.

## Feature intake table

Use this table when comparing a competitor or new idea:

| Candidate feature | Competitor/source | User pain | Primitive improved | CompassBear fit | Minimum implementation | Test |
|---|---|---|---|---|---|---|
|  |  |  |  | adopt / adapt / reject / later | protocol / template / script / sub-skill |  |

## Adopt / adapt / reject rules

**Adopt** when:

- the feature directly improves claim, evidence, figure, journal or rebuttal
  decisions;
- the user pain is frequent;
- the output can be made traceable and safe;
- it fits an existing CompassBear route.

**Adapt** when:

- another project solves workflow friction well, but its scientific guardrails
  are too loose;
- the idea is useful but should become a protocol or template rather than a
  tool;
- the same primitive already exists and only needs a better interface.

**Reject** when:

- it mainly creates impressive-looking output without stronger evidence;
- it encourages citation decoration or journal-style mimicry;
- it duplicates a mature external tool without adding CompassBear judgment;
- it increases private-data leakage risk;
- it solves a rare workflow at high complexity cost.

**Later** when:

- the idea is good but needs stable APIs, external accounts, institution access,
  or more examples before becoming reliable.

## Competitor lessons to keep

| Observed strength | CompassBear translation |
|---|---|
| full pipeline systems | keep CompassBear pipeline gates, but avoid bloated automation |
| multi-agent review | use research council only when decisions need competing lenses |
| citation/source audit | strengthen Chat-native RAG, source notes and Claim Passport |
| figure generation workflows | connect figure logic to tools, but never fabricate data-looking evidence |
| Office/PPT helpers | integrate only when they preserve claim/figure/rebuttal traceability |
| marketplace-style usability | improve USAGE, examples, test prompts and public/private split |
| journal-specific writing | convert positioning and evidence emphasis, not phrases |
| PDF/Zotero workflows | use handoff bridges instead of rebuilding reference managers badly |

## Iteration cadence

Run this loop after every meaningful user session or competitor review:

1. **Capture**
   - What friction did the user hit?
   - What did another tool do better?
   - What decision did CompassBear handle well or poorly?

2. **Decompose**
   - Convert the observation into primitives: claim, evidence, figure, source,
     journal, rebuttal, local lens or packaging.

3. **Decide**
   - adopt / adapt / reject / later;
   - public protocol or private configuration;
   - prompt-level change or code/script change.

4. **Implement small**
   - add the smallest protocol, template, example or route;
   - avoid adding a new sub-skill unless routing truly needs it.

5. **Test**
   - add or update one realistic prompt;
   - run existing static checks;
   - verify the new behavior does not weaken the north-star.

6. **Document**
   - update `USAGE.md`, `README.md` or examples if the user-facing behavior
     changes;
   - update `CHANGELOG.md`.

## Capability layers

Choose the lowest layer that solves the problem:

| Layer | Use when | Example |
|---|---|---|
| Response habit | one-line behavior change | always mark unsupported claims |
| Reference protocol | reusable decision logic | Claim Passport, Chat-native RAG |
| Example gallery | users need to see shape | council memo, style conversion |
| Template | structured recurring artifact | source note, lens card |
| Script | repeatable batch work | literature retrieval, checks |
| Sub-skill | distinct task family | writing, figure strategy, response |
| Private config | user/project-specific expertise | mentor lenses, project rosters |

## Quality bar for new features

A feature is not done until it has:

- a trigger condition;
- an output shape;
- guardrails;
- at least one realistic user prompt;
- a place in the routing table if it changes behavior;
- a note about when not to use it.

## Anti-bloat rule

If a feature does not improve a user's next scientific decision, it should not be
in the core skill. Put it in examples, private notes, an optional script, or the
backlog instead.

## Backlog ranking

Rank future work by:

1. Does it reduce unsupported claims?
2. Does it make evidence easier to verify?
3. Does it improve figure or journal decisions?
4. Does it preserve private/public separation?
5. Does it make the skill easier to use without hiding risk?
6. Does it have a realistic test?

## Output format for iteration reviews

When asked to improve CompassBear after seeing another tool, return:

1. **First-principles diagnosis**
2. **Feature intake table**
3. **Adopt / adapt / reject decisions**
4. **Smallest implementation plan**
5. **Risks and guardrails**
6. **Files to update**
7. **Test prompts**
