# CompassBear Academic Compass 🧭🐻

**CompassBear Academic Compass is not a Nature-style text generator.** It is a PI-style reasoning system for turning scattered data into defensible scientific claims, figures, manuscripts, rebuttals and invention boundaries.

罗盘熊锅不是“Nature 风格润色器”，而是一套面向高水平科研工作的判断系统：先定 claim，再排证据；先守边界，再追求漂亮。

## Canonical skill invocation

The installed root skill name is **`compass-bear`**. Invoke it explicitly in Codex or Claude Code as:

```text
$compass-bear
```

“CompassBear Academic Compass” remains the human-facing project title; `compass-bear` is the stable machine-facing skill ID.

## Latest Usage

Start with [`USAGE.md`](USAGE.md) for the current recommended workflow.

`USAGE.md` now includes a module-by-module guide covering Pipeline, Chat-native
RAG, Script RAG, DOI/PDF source ingestion, Claim Passport, Research Council,
Mentor Lens Evolution, Journal Style Profiles, Figure Production Bridge,
Visual Generation Boundary, Submission Gates, local `cb.py` commands and the
benchmark suite.

The short version:

- ordinary literature support now uses chat-native RAG inside the conversation;
- `scripts/literature_rag.py` is the heavy mode for batch, export, Zotero handoff and reproducible audits;
- high-risk claims should use a Claim Passport;
- end-to-end paper work should use CompassBear pipeline mode;
- journal style conversion supports JACS / Angew / Advanced Materials positioning without phrase mimicry;
- mentor lenses evolve through source notes and source-backed decision rules;
- the user's own taste can be stored separately as a User PI Preference Lens, with evidence override boundaries;
- skill improvement follows first-principles feature intake rather than copying competitors;
- local tooling now includes `scripts/cb.py` for doctor/checks/protocols/examples/heavy RAG;
- GPT Image / `imagegen` may be used only for conceptual visuals, not data-looking scientific evidence.

## Why this exists

Most academic writing tools polish sentences or brainstorm loosely. CompassBear asks a more important question first:

> What must the reader believe, and what evidence makes that belief unavoidable?

This suite helps researchers plan research directions, manuscripts, figures, supplementary information, cover letters, rebuttals and patents by enforcing claim discipline, evidence hierarchy, cross-document consistency and calibrated scientific voice.

## How it differs from typical academic AI workflows

Many academic AI workflows are good at one narrow layer: polishing prose, summarizing papers, formatting documents or simulating expert comments. CompassBear is built around the layer before polishing: whether the scientific story is defensible.

Its strengths:

- starts from the central claim rather than sentence style;
- links claims to evidence owners, figures and reviewer risks;
- designs figures as arguments rather than decorations;
- gives demotion language when evidence is suggestive but not decisive;
- separates literature support, project-specific proof and unsupported analogy;
- lets users build local source-backed expert lenses without impersonating real people.

Its trade-offs:

- heavier than a quick writing prompt;
- needs real evidence from the user for high-stakes claims;
- cannot replace literature reading, experimental validation or statistical review;
- local expert lenses are only as good as the source notes used to build them.

Use CompassBear when the bottleneck is not "make this sound better" but "make this story harder to attack."

## Building local expert lenses

CompassBear can support local expert lenses, but the goal is not to imitate a professor or named researcher. The goal is to extract source-backed decision rules.

A safe workflow:

1. Collect public materials: papers, reviews, talks, interviews or lectures.
2. Write source notes: what claims, evidence standards, figure preferences and recurring critiques appear in those sources?
3. Extract decision rules: what would this lens promote, demote, veto or ask to prove?
4. Define boundaries: where this lens is useful, and where it should fall back to generic roles.
5. Test on anonymized project cases.
6. Keep personal or unpublished lens material local, not in public releases.

## Skill index

| Skill | Status | Purpose | Typical triggers | Typical output |
|---|---:|---|---|---|
| [`compassbear-research-council`](skills/compassbear-research-council/) | Beta | Discuss research direction through a simulated, role-based expert council and convert debate into decisions | 讨论思路, expert council, project direction, paper angle | council memo + debate synthesis + action plan |
| [`compassbear-writing`](skills/compassbear-writing/) | Beta | Draft, rebuild and polish Abstracts, Introductions, Results and Conclusions | abstract, intro, results, conclusion, polish, AI味 | copy-paste prose + must-fix notes |
| [`compassbear-figure-strategy`](skills/compassbear-figure-strategy/) | Beta | Build claim-first figure logic, panel maps, captions and visual hierarchy | figure, panel, graphical abstract, caption, 配色 | panel map + caption + evidence placement |
| [`compassbear-consistency-audit`](skills/compassbear-consistency-audit/) | Beta | Audit numbers, terminology, metrics and cross-document propagation | final check, 口径统一, consistency | inconsistency table + fixes + reconciliation paragraph |
| [`compassbear-cover-letter`](skills/compassbear-cover-letter/) | Beta | Build editor-facing cover letters, presubmission framing and reviewer suggestions | cover letter, editor, reviewers | cover letter + reviewer list + scope rationale |
| [`compassbear-response`](skills/compassbear-response/) | Draft | Map reviewer comments to action-based, traceable rebuttal responses | rebuttal, reviewer response, 回防 | response map + point-by-point text |
| [`compassbear-si-methods`](skills/compassbear-si-methods/) | Draft | Clean Methods, SI, Data Availability and reproducibility details | Methods, SI, data availability | Methods section + SI audit + data statement |
| [`compassbear-patent`](skills/compassbear-patent/) | Draft | Split invention boundaries and draft patent-style claim structures | patent, claims, embodiment, 专利 | independent claims + dependent claims + embodiments |

## New decision protocols

CompassBear now includes six project-level protocols that sit above the
individual sub-skills:

| Protocol | Use when | Output |
|---|---|---|
| [`compassbear-pipeline`](references/compassbear-pipeline.md) | the user wants end-to-end help on a paper, proposal or rebuttal package | staged gates from project brief to submission audit |
| [`production-suite-roadmap`](references/production-suite-roadmap.md) | the user wants to reduce CompassBear's tooling, RAG, figure, benchmark or packaging shortboards | maturity roadmap + smallest implementation steps |
| [`claim-passport`](references/claim-passport.md) | claims must stay synchronized across figures, text, cover letter, SI or rebuttal | evidence owner, scope, reviewer attack and demotion wording for each claim |
| [`chat-native-rag`](references/chat-native-rag.md) | the user wants literature support or source-backed claim checking inside the conversation | cited sources + stance/scope/action + safer wording |
| [`pdf-source-ingestion`](references/pdf-source-ingestion.md) | the user provides DOI, title, abstract, PDF text or source excerpts | source-note draft + stance/scope/action |
| [`compassbear-pdf-reader`](skills/compassbear-pdf-reader/) | the user provides a local PDF path or Zotero PDF to read | extracted text + source-note worksheet |
| [`compassbear-wechat-distiller`](skills/compassbear-wechat-distiller/) | the user has long WeChat notes/text chunks to turn into research memory | cleaned transcript + decisions/claims/preferences/lens candidates |
| [`wechat-export-automation`](references/wechat-export-automation.md) | the user wants safer automation around WeChat chunk export | clipboard capture + automation boundaries |
| [`local-zotero-read`](references/local-zotero-read.md) | the user wants to search local Zotero metadata or find PDFs without dragging files | title/author/DOI/PDF path report |
| [`journal-style-profiles`](references/journal-style-profiles.md) | the user wants JACS / Angew / Advanced Materials positioning or style conversion | journal fit + title/abstract/cover-letter framing shifts |
| [`first-principles-iteration`](references/first-principles-iteration.md) | the user wants to improve the skill by learning from other tools or sessions | feature intake table + adopt/adapt/reject decisions |
| [`mentor-lens-evolution`](references/mentor-lens-evolution.md) | the user reads more mentor papers and wants the lens to improve | source-note-to-lens workflow with activation thresholds |
| [`user-preference-lens`](references/user-preference-lens.md) | the user wants to store or apply personal research/writing preferences | preference rules + evidence override boundaries |
| [`public-private-split`](references/public-private-split.md) | preparing a public release or separating reusable rules from private notes | release split and redaction checklist |
| [`submission-integrity-gates`](references/submission-integrity-gates.md) | before submission, cover letter, rebuttal or patent-facing language | must-fix / demote / polish / propagation audit |
| [`output-gallery`](examples/compassbear-output-gallery.md) | checking or demonstrating expected output shapes | anonymized council, claim passport, figure spine and risk-map templates |

## Local Command Surface

Normal use is still chat-first. For repeatable local operations:

```bash
python scripts/cb.py doctor
python scripts/cb.py protocols
python scripts/cb.py examples
python scripts/cb.py checks
python scripts/cb.py rag --claim "<claim>" --profile materials-mechanism --with-html-review
python scripts/cb.py zotero --query "catalyst stability screening"
python scripts/cb.py pdf "path/to/paper.pdf"
python scripts/cb.py wechat-capture --watch
python scripts/cb.py wechat-ui init
python scripts/cb.py wechat-ui run --loops 1 --i-understand-ui-automation-risk
python scripts/cb.py wechat --input "path/to/wechat-chunks" --project "<project>" --topic "<topic>"
```

## Core workflow

1. **Calibrate the field** — decide what counts as strong evidence in the target discipline.
2. **Define the claim hierarchy** — paper → section → figure → panel → paragraph → sentence.
3. **Build the evidence ladder** — primary proof first, support and controls second, decoration last.
4. **Design figures as arguments** — every panel must defend a necessary claim.
5. **Write with calibrated ambition** — bold where evidence permits, cautious where it does not.
6. **Audit consistency** — numbers, windows, sample names and assumptions must agree across all documents.
7. **Pre-empt reviewers** — identify missing controls, overclaims and boundary problems before submission.

For end-to-end projects, use [`references/compassbear-pipeline.md`](references/compassbear-pipeline.md)
as the controlling workflow. For high-stakes claims, maintain a
[`Claim Passport`](references/claim-passport.md) so the Abstract, figures, SI,
cover letter and rebuttal cannot drift apart.


## Local research-council layer

This public edition does not include personal mentor lenses, project rosters, source packs, generated outputs or API keys. It keeps the generic research-council workflow and blank templates so users can build their own local source-backed lenses if needed.

Active local lenses include decision instincts, veto power, signature figure demands and claim-demotion rules so the council can make claim, figure and supplementary-placement decisions rather than only giving generic comments.

Use it when you want to run a research-direction council using your own curated professor-inspired lenses. These are **expertise lenses**, not impersonations.

- Lens template: `templates/expert-lens-template.md`
- Source-note template: `templates/source-note-template.md`
- Project-roster template: `templates/project-roster-template.md`
- Council workflow: `skills/compassbear-research-council/`

Mentor lenses are expected to evolve as you read more papers. Add a source note,
extract reusable rules, connect them to veto or demotion behavior, and only then
promote the lens status. The detailed workflow is in
[`references/mentor-lens-evolution.md`](references/mentor-lens-evolution.md).

Public release hygiene is tracked in
[`references/public-private-split.md`](references/public-private-split.md).

## Visual generation boundary

CompassBear may use GPT Image / the Codex `imagegen` skill when an environment
exposes it, but only for conceptual visuals such as graphical abstracts, cover
art, icons, schematic mood boards or non-data illustrations. It must not generate
data-looking spectra, microscopy, plots, gels or experimental panels, and it must
not replace missing evidence. See
[`skills/compassbear-figure-strategy/references/visual-generation-boundary.md`](skills/compassbear-figure-strategy/references/visual-generation-boundary.md).

## Integrated literature RAG + Zotero handoff layer

For normal use, CompassBear should first use
[`references/chat-native-rag.md`](references/chat-native-rag.md): claim
extraction, support search, adversarial search, source citation, stance/scope
judgment and wording repair happen directly in the conversation.

The skill-local literature retrieval helper remains the heavy mode for batch,
export, source-note stub generation, Zotero handoff and reproducible audits:

```bash
python scripts/literature_rag.py \
  --claim "<claim under adjudication>" \
  --profile materials-mechanism \
  --with-html-review \
  --max-per-provider 5 \
  --source-note-dir source-packs/generated
```

The helper can also split longer text with `--text-file` or ingest one claim per line with `--claim-file`. Domain profiles (`broad`, `materials-mechanism`, `computational-methods`, `bio-application`) generate support, adversarial and background queries automatically. The helper writes an evidence matrix and optional HTML review table under `outputs/literature-rag/`, optional `.ris` / `.enw` / `.bib` exports, and optional source-note **stubs** under `source-packs/generated/`. It supports Semantic Scholar, Crossref, OpenAlex, Europe PMC, arXiv and optional Serper retrieval through environment variables in `.env`, plus an Unpaywall pass that upgrades DOIs to open-access PDF links when `UNPAYWALL_EMAIL` is set. Retrieval is not treated as proof; the RAG Evidence Adjudicator still has to judge support / qualification / refutation / insufficiency and scope match.

Stubs land with `TBD` placeholders by design. The human reads the paper, fills the structured fields, and promotes the stub out of the `generated/` staging directory into `source-packs/`; `scripts/check_source_pack_promotion.py` blocks any promotion that still contains placeholders.

For the human reading step, `scripts/zotero_sync.py` pushes the retrieved candidates into a Zotero collection and pulls tagged items back as filled stubs. The `cb/stance/*`, `cb/scope/*`, `cb/action/*`, `cb/claim/*` tag convention turns Zotero tagging into structured stub fields; a single child note carries the free-text summary. The full protocol is in `skills/compassbear-research-council/references/rag-evidence-adjudicator.md`.

## Installation

This repository contains the full public skill package, so direct GitHub clone now works.

For Codex Desktop on Windows:

```powershell
git clone https://github.com/433liu/compassbear.git "$env:TEMP\compassbear"
$destRoot = "$env:USERPROFILE\.codex\skills"
New-Item -ItemType Directory -Force -Path $destRoot | Out-Null
Copy-Item -Recurse -Force "$env:TEMP\compassbear" "$destRoot\compass-bear"
```

For Claude Code:

```bash
git clone https://github.com/433liu/compassbear.git /tmp/compassbear
mkdir -p ~/.claude/skills
cp -R /tmp/compassbear ~/.claude/skills/compass-bear
```

Release zip installation is also supported: download `compass-bear-v0.5.14-public.zip`, unzip it, and copy the extracted folder to the same skill directory as `compass-bear`.

## Legacy Local Copy Install

Copy this folder into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills
cp -r compassbear ~/.claude/skills/compass-bear
```

For project-level use:

```bash
mkdir -p .claude/skills
cp -r compassbear .claude/skills/compass-bear
```

Each sub-skill is self-contained: `SKILL.md` for the agent, `README.md` for human users, `references/` for rules, and `tests/` + `examples/` for regression checks.

## Local QA

Run the RAG adjudicator test-coverage checker after editing the RAG evidence test spec:

```bash
python scripts/check_rag_evidence_tests.py
```

Run the integrated literature RAG static guard after editing retrieval scripts or RAG references:

```bash
python scripts/check_literature_rag_integration.py
```

For a quick local check, run:

```bash
python scripts/cb.py checks
```

## Test prompts

```text
Use a research council to debate whether this project should be framed as mechanism, method or application.
```

```text
Help me rebuild this abstract so it is claim-first and less AI-like.
```

```text
Audit Figure 3. Which panels belong in the main figure, Extended Data or SI?
```

```text
Check whether my Abstract, Fig. 5 caption and SI use consistent numbers.
```

```text
Draft a Nature cover letter, but make sure AI is not the main contribution.
```

```text
Reviewer says our mechanism is speculative. Build a response strategy.
```

## Contributing / extending

To add a new sub-skill:

1. Create `skills/compassbear-<topic>/`.
2. Add `SKILL.md`, `README.md`, `references/`, and preferably `tests/` + `examples/`.
3. Define trigger conditions, output format and guardrails.
4. Add the sub-skill to this README and to the root routing table.

Status labels: Draft = rules defined; Beta = tested on realistic examples; Stable = validated repeatedly on real workflows.

## Design philosophy

- The paper is an argument, not a warehouse.
- A figure is a proof path, not a gallery.
- Mechanism is expensive; do not buy it with weak evidence.
- The reader should never do reconciliation work.
- A tool is not the scientific contribution unless the paper is truly about the tool.
- If forced to choose between sounding impressive and being defensible, choose defensible.

## What CompassBear does not do

- It does not invent data, mechanisms, citations or experiments.
- It does not imitate Nature prose blindly.
- It does not replace field expertise or statistical review.
- It does not turn weak evidence into strong claims.
- It does not automatically make figures; it makes figure logic harder to break.

## Recommended package structure

```text
compass-bear/
├── SKILL.md
├── README.md
├── references/
├── skills/
├── examples/
├── tests/
└── scripts/
```

## License

Choose a license before public release. Suggested: MIT for the workflow text and scripts, with a note that examples may contain fictional or anonymized scientific content.

