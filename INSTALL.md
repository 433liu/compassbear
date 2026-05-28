# CompassBear Public-Clean Installation Guide

This package is the sanitized public-clean build of `compass-bear`.

It does not include:

- `.env` or any real API keys;
- generated outputs;
- personal project rosters or source notes;
- personal mentor lens cards and related private routing references;
- project-specific examples that reveal the user's manuscript direction.

It includes the reusable skill, sub-skills, references, scripts, public examples, tests and blank templates under `templates/`.

## 1. Download and unzip

Download `compass-bear-v0.5.14-public-clean.zip` from the GitHub release.

Unzip it and keep the installed folder name as:

```text
compass-bear
```

If the extracted folder is named `compass-bear-v0.5.14-public-clean`, rename it to `compass-bear` when installing into a skills directory.

## 2. Install for Codex Desktop on Windows

```powershell
$destRoot = "$env:USERPROFILE\.codex\skills"
New-Item -ItemType Directory -Force -Path $destRoot | Out-Null
Copy-Item -Recurse -Force "C:\path\to\compass-bear-v0.5.14-public-clean" "$destRoot\compass-bear"
```

Restart Codex Desktop. Invoke the skill with:

```text
$compass-bear
```

## 3. Install for Claude Code

Global install:

```bash
mkdir -p ~/.claude/skills
cp -R /path/to/compass-bear-v0.5.14-public-clean ~/.claude/skills/compass-bear
```

Project-level install:

```bash
mkdir -p .claude/skills
cp -R /path/to/compass-bear-v0.5.14-public-clean .claude/skills/compass-bear
```

Restart Claude Code after copying.

## 4. Optional environment file

Most chat-first use does not require API keys.

Only create `.env` if you want heavy script workflows such as batch literature retrieval or Zotero handoff:

```bash
cp .env.example .env
```

Fill only the keys you actually need. Leave unused fields blank. Do not share `.env`.

## 5. Verify installation

From the installed folder:

```bash
python scripts/cb.py doctor
python scripts/cb.py checks
```

Then test:

```text
$compass-bear
Help me audit this abstract for claim discipline, evidence hierarchy and AI rhythm.
```

## 6. Build your own local lenses

The public-clean build has no personal mentor cards. To create your own local source-backed lens or source pack, start from:

- `templates/expert-lens-template.md`
- `templates/source-note-template.md`
- `templates/project-roster-template.md`
- `templates/user-preference-template.md`

Keep personal or unpublished material out of any package you plan to share.
