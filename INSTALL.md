# CompassBear Public Installation Guide

This package is the sanitized public build of `compass-bear`.

It does not include:

- `.env` or any real API keys;
- generated outputs;
- personal project rosters or source notes;
- personal mentor lens cards and related private routing references.

It does include the reusable skill, sub-skills, references, scripts, public examples, tests and blank templates under `templates/`.

## 1. Install from GitHub clone

This repository now contains the full public skill package. You can install it directly from GitHub.

Codex Desktop on Windows:

```powershell
git clone https://github.com/433liu/compassbear.git "$env:TEMP\compassbear"
$destRoot = "$env:USERPROFILE\.codex\skills"
New-Item -ItemType Directory -Force -Path $destRoot | Out-Null
Copy-Item -Recurse -Force "$env:TEMP\compassbear" "$destRoot\compass-bear"
```

Claude Code:

```bash
git clone https://github.com/433liu/compassbear.git /tmp/compassbear
mkdir -p ~/.claude/skills
cp -R /tmp/compassbear ~/.claude/skills/compass-bear
```

Restart the app after copying. Invoke the skill with:

```text
$compass-bear
```

## 2. Install from Release zip

Unzip the package and keep the folder name as:

```text
compass-bear
```

If the extracted folder is named `compass-bear-v0.5.14-public`, rename it to `compass-bear` when installing into a skills directory.

## 3. Install release zip for Codex Desktop on Windows

Create the Codex skills folder if it does not exist, then copy the extracted folder into it:

```powershell
$destRoot = "$env:USERPROFILE\.codex\skills"
New-Item -ItemType Directory -Force -Path $destRoot | Out-Null
Copy-Item -Recurse -Force "C:\path\to\compass-bear-v0.5.14-public" "$destRoot\compass-bear"
```

Restart Codex Desktop. Invoke the skill with:

```text
$compass-bear
```

## 4. Install release zip for Claude Code

Global install:

```bash
mkdir -p ~/.claude/skills
cp -R /path/to/compass-bear-v0.5.14-public ~/.claude/skills/compass-bear
```

Project-level install:

```bash
mkdir -p .claude/skills
cp -R /path/to/compass-bear-v0.5.14-public .claude/skills/compass-bear
```

Restart Claude Code after copying.

## 5. Optional environment file

Most chat-first use does not require API keys.

Only create `.env` if you want the heavy script workflows such as batch literature retrieval or Zotero handoff:

```bash
cp .env.example .env
```

Then fill only the keys you actually need. Leave unused fields blank. Do not share `.env`.

Useful optional fields:

- `UNPAYWALL_EMAIL`: enables Unpaywall open-access PDF lookup.
- `SEMANTIC_SCHOLAR_API_KEY`: optional higher Semantic Scholar rate limits.
- `OPENALEX_API_KEY`: optional higher OpenAlex rate limits.
- `SERPER_API_KEY`: optional paid Google-style fallback search.
- `ZOTERO_API_KEY` and `ZOTERO_USER_ID`: optional Zotero push/pull handoff.

## 6. Verify installation

From the installed folder:

```bash
python scripts/cb.py doctor
python scripts/cb.py checks
```

Then test in Codex or Claude Code:

```text
$compass-bear
Help me audit this abstract for claim discipline, evidence hierarchy and AI rhythm.
```

The answer should focus on defensible claims, evidence boundaries, figure logic and reviewer risk rather than only sentence polishing.

## 7. Using local templates

The public build has no personal mentor cards. To create your own local source-backed lens or source pack, start from:

- `templates/expert-lens-template.md`
- `templates/source-note-template.md`
- `templates/project-roster-template.md`
- `templates/user-preference-template.md`

Keep personal or unpublished material out of any package you plan to share.

## 8. Common issues

If the skill does not trigger, confirm the installed directory is named exactly `compass-bear` and restart the app.

If script checks fail because Python is missing, install Python 3.10+ and rerun the commands.

If RAG or Zotero scripts fail due missing keys, either fill `.env` for those optional workflows or use the default chat-native workflow instead.

