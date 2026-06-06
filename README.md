# CompassBear

![Version](https://img.shields.io/badge/version-0.5.18--public-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Focus](https://img.shields.io/badge/focus-claim--first%20research%20workflow-purple)

> **For researchers using Claude Code or Codex** - audit overclaims, defend
> figures, plan rebuttals, and position manuscripts before polishing prose.

![CompassBear before and after demo](examples/compassbear-before-after.svg)

**CompassBear is a claim-first research skill for making scientific stories harder to attack.**

Most academic AI tools start with the visible layer: polish the prose, summarize
papers, format a document, or draft a generic review. CompassBear starts one
layer earlier:

> What must the reader believe, and what evidence makes that belief unavoidable?

Use it when the bottleneck is not "make this sound better", but:

- "is this claim defensible?";
- "does this figure prove what the caption says?";
- "will reviewers attack this mechanism?";
- "which journal framing is honest?";
- "should we read more papers or stop this direction now?"

## Quick Start

```bash
git clone https://github.com/433liu/compassbear.git
```

Install the folder as a local skill named `compass-bear`, then ask:

```text
$compass-bear
Audit this abstract for overclaiming and reviewer risk.
```

## Why It Is Different

CompassBear is designed as a low-token PI judgment layer before expensive
workflows such as full-paper reading, local RAG, figure rendering, or Word/PDF
editing.

It does three things that ordinary writing prompts usually miss:

| Layer | CompassBear behavior | Output you get |
|---|---|---|
| Claim discipline | separates central claims, section claims, and figure claims | claim hierarchy + safer wording |
| Evidence pressure | asks what evidence actually owns each claim | support / qualify / demote decisions |
| Reviewer defense | turns likely attacks into repair actions | risk table + rebuttal-ready language |

The result is not just nicer text. It is a clearer argument with fewer unsupported
claims, cleaner figure logic, and better editor-facing positioning.

## What You Can Ask It To Do

```text
$compass-bear
Audit this abstract for overclaiming, AI rhythm, and reviewer-risk language.
```

```text
$compass-bear
Build a claim-first figure map for Figure 2. Decide which panels belong in the
main figure, Extended Data, or SI.
```

```text
$compass-bear
Compare JACS, Angew, Advanced Materials, and Nature-family positioning for this
story. What is the claim ceiling for each target?
```

```text
$compass-bear
Do a token-lean scout before full-paper reading. Is this direction crowded,
promising, or too weak to pursue?
```

```text
$compass-bear
Turn these reviewer comments into an action map and a point-by-point response
strategy.
```

## Capability Map

| Module | Use it for |
|---|---|
| `compassbear-writing` | Abstract, Introduction, Results, Conclusion rebuilding |
| `compassbear-figure-strategy` | Panel order, figure narrative, captions, graphical abstract logic |
| `compassbear-consistency-audit` | Number, term, claim, title, figure, and SI consistency |
| `compassbear-research-council` | Role-based project direction debate and decision memos |
| `compassbear-cover-letter` | Editor-facing cover letters and reviewer suggestions |
| `compassbear-response` | Reviewer-response strategy and traceable replies |
| `compassbear-si-methods` | Methods, SI, data availability, reproducibility cleanup |
| `compassbear-patent` | Patent-style claim boundaries and embodiment planning |

## Core Protocols

| Protocol | What it prevents |
|---|---|
| `claim-passport` | claims drifting beyond evidence |
| `chat-native-rag` | treating search leads as proven evidence |
| `token-lean-direction-scouting` | wasting context on directions that first need triage |
| `journal-style-profiles` | imitating journal style without matching journal logic |
| `figure-production-bridge` | making attractive figures that do not defend claims |
| `submission-integrity-gates` | polishing before fixing numbers, terms, and unsupported claims |

## Public Package

```text
compass-bear-public/
├── README.md
├── LICENSE
├── INSTALL.md
├── SKILL.md
├── commands/
├── agents/
├── skills/
├── examples/
├── references/
└── evals/
```

This public build contains only generic, source-safe workflow logic. It does
not include private expert lenses, personal project rosters, source notes from
papers, generated outputs, API keys, local paths, reference-manager databases,
unpublished manuscript material, or user-specific preferences.

## Install

Read [INSTALL.md](INSTALL.md), or use the short version:

```bash
git clone https://github.com/433liu/compassbear.git
```

Install the cloned folder as a local skill named `compass-bear`, then invoke:

```text
$compass-bear
```

## Examples And Evals

- [examples/benchmark-suite.md](examples/benchmark-suite.md) gives synthetic
  prompts and pass criteria.
- [examples/token-economy-demo.md](examples/token-economy-demo.md) defines how
  to measure scout-vs-full-reader efficiency without exaggerating savings.
- [examples/compassbear-output-gallery.md](examples/compassbear-output-gallery.md)
  shows the expected output shapes.
- [evals/cases.jsonl](evals/cases.jsonl) provides regression cases for the
  public package.

## Design Boundary

CompassBear does not replace literature reading, statistical review,
experimental validation, legal counsel, final journal formatting, or human
scientific responsibility.

Its job is narrower and useful: decide what is worth claiming, reading, drawing,
demoting, defending, or submitting before heavier tools spend the context.

## Repository Description

For the GitHub "About" field:

```text
Claim-first research workflow skill for defensible manuscripts, figures,
rebuttals, cover letters, journal positioning, and token-lean project scouting.
```
