# CompassBear 

CompassBear is a claim-first research workflow skill for Codex / Claude Code. It helps researchers turn scattered data, mechanisms, figures and applications into defensible scientific manuscripts, proposals, cover letters, rebuttals and patent-style claim structures.

It is not a phrase-polishing prompt. The core question is:

> What must the reader believe, and what evidence makes that belief unavoidable?

## Why CompassBear is different

Most academic AI workflows are good at one narrow layer: polishing prose, summarizing papers, formatting documents or simulating expert comments. CompassBear is built around the layer before polishing: whether the scientific story is defensible.

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

## What it helps with

- Manuscript claim hierarchy and paper framing
- Abstract, Introduction, Results and Conclusion rebuilding
- Figure logic, panel maps, captions and graphical abstract planning
- Consistency audits across numbers, terms, figures and submission documents
- Cover letters, reviewer suggestions and reviewer-response planning
- SI, Methods, data availability and reproducibility statements
- Research-council style project direction debate
- High-risk claim boundary control and reviewer-risk analysis

## Building local expert lenses

CompassBear can support local expert lenses, but the goal is not to imitate a professor or named researcher. The goal is to extract source-backed decision rules.

A safe workflow:

1. Collect public materials: papers, reviews, talks, interviews or lectures.
2. Write source notes: what claims, evidence standards, figure preferences and recurring critiques appear in those sources?
3. Extract decision rules: what would this lens promote, demote, veto or ask to prove?
4. Define boundaries: where this lens is useful, and where it should fall back to generic roles.
5. Test on anonymized project cases.
6. Keep personal or unpublished lens material local, not in public releases.

## Public build

This repository is for the sanitized `v0.5.14-public` build.

It does not include:

- `.env` or real API keys
- generated outputs
- personal project rosters or source notes
- personal mentor lens cards or related private routing references
- project-specific examples that reveal the user's manuscript direction

It includes:

- the reusable root `compass-bear` skill
- sub-skills for research council, writing, figure strategy, consistency audit, cover letters, responses, SI/methods, patents, PDF reading and note distillation
- public references and examples
- helper scripts for local checks and optional heavy workflows
- blank templates under `templates/`

## Install

Download `compass-bear-v0.5.14-public.zip` from the release, unzip it, and install the extracted folder as `compass-bear`.

Codex Desktop on Windows:

```powershell
$destRoot = "$env:USERPROFILE\.codex\skills"
New-Item -ItemType Directory -Force -Path $destRoot | Out-Null
Copy-Item -Recurse -Force "C:\path\to\compass-bear-v0.5.14-public" "$destRoot\compass-bear"
```

Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -R /path/to/compass-bear-v0.5.14-public ~/.claude/skills/compass-bear
```

Restart the app, then invoke:

```text
$compass-bear
```

## Try it

```text
$compass-bear
Help me audit this abstract for claim discipline, evidence hierarchy and AI rhythm.
```

```text
$compass-bear
Use a research council to debate whether this project should be framed as mechanism, method, platform or application.
```

## Files to read first

- `INSTALL.md` for installation
- `USAGE.md` inside the zip for the full workflow
- `SKILL.md` inside the zip for the root skill behavior

## License

MIT License. See `LICENSE`.
