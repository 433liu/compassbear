# CompassBear Academic Compass

CompassBear is a claim-first research workflow skill for Codex / Claude Code. It helps researchers turn scattered data, mechanisms, figures and applications into defensible scientific manuscripts, proposals, cover letters, rebuttals and patent-style claim structures.

It is not a phrase-polishing prompt. The core question is:

> What must the reader believe, and what evidence makes that belief unavoidable?

## What it helps with

- Manuscript claim hierarchy and paper framing
- Abstract, Introduction, Results and Conclusion rebuilding
- Figure logic, panel maps, captions and graphical abstract planning
- Consistency audits across numbers, terms, figures and submission documents
- Cover letters, reviewer suggestions and reviewer-response planning
- SI, Methods, data availability and reproducibility statements
- Research-council style project direction debate
- High-risk claim boundary control and reviewer-risk analysis

## Public-share build

This repository is for the sanitized public-share build `v0.5.14-public-share`.

It does not include:

- `.env` or real API keys
- generated outputs
- personal project rosters or source notes
- personal mentor lens cards or related private routing references

It includes:

- the reusable root `compass-bear` skill
- sub-skills for research council, writing, figure strategy, consistency audit, cover letters, responses, SI/methods, patents, PDF reading and note distillation
- public references and examples
- helper scripts for local checks and optional heavy workflows
- blank templates under `templates/`

## Install

Download the public-share package from the release, unzip it, and install the extracted folder as `compass-bear`.

Codex Desktop on Windows:

```powershell
$destRoot = "$env:USERPROFILE\.codex\skills"
New-Item -ItemType Directory -Force -Path $destRoot | Out-Null
Copy-Item -Recurse -Force "C:\path\to\compass-bear-v0.5.14-public-share" "$destRoot\compass-bear"
```

Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -R /path/to/compass-bear-v0.5.14-public-share ~/.claude/skills/compass-bear
```

Restart the app, then invoke:

```text
$compass-bear
```

## Verify

From the installed folder:

```bash
python scripts/cb.py doctor
python scripts/cb.py checks
```

## Try it

```text
$compass-bear
Help me audit this abstract for claim discipline, evidence hierarchy and AI rhythm.
```

```text
$compass-bear
Use a research council to debate whether this project should be framed as mechanism, method or application.
```

## Files to read first

- `INSTALL.md` for installation
- `USAGE.md` for the full workflow
- `SKILL.md` for the root skill behavior

## License

MIT License. See `LICENSE`.
