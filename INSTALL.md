# Install CompassBear

CompassBear is distributed as a public, source-safe skill folder. The repository
root is the installable skill package.

It contains no private mentor lenses, local project data, generated outputs,
local paths, API keys, unpublished manuscript material, source-note archives, or
reference-manager databases.

## Option 1: Install From GitHub

Clone the repository:

```bash
git clone https://github.com/433liu/compassbear.git
```

Install the cloned folder as a local skill named:

```text
compass-bear
```

Typical target layout:

```text
<agent-config>/skills/compass-bear/
```

If your agent expects the folder name to match the skill ID, rename the cloned
folder from `compassbear` to `compass-bear`.

Then invoke:

```text
$compass-bear
```

## Option 2: Install From A Release Zip

Download the public release zip, extract it, and install the extracted
`compass-bear-public` folder as:

```text
compass-bear
```

Then restart your agent and invoke:

```text
$compass-bear
```

## Optional Command Wrappers

The `commands/` folder contains lightweight routes:

| Command file | Route |
|---|---|
| `cb.md` | root router |
| `cb-writing.md` | manuscript writing |
| `cb-figure.md` | figure strategy |
| `cb-audit.md` | consistency audit |
| `cb-council.md` | research-direction debate |
| `cb-cover.md` | cover letter |
| `cb-rebuttal.md` | reviewer response |
| `cb-methods.md` | Methods / SI |
| `cb-patent.md` | patent-style boundary |

If your agent supports slash-command installation, register these files
according to that agent's command documentation.

## Verify The Package

From the installed package root, run:

```bash
python -c "import json, pathlib; [json.loads(line) for line in pathlib.Path('evals/cases.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]; print('OK')"
```

Manual smoke prompt:

```text
$compass-bear
Audit this claim for overreach: "This small synthetic dataset proves a universal
mechanism across the whole material family."
```

Expected behavior:

- mark the universal mechanism claim as unsupported;
- explain what evidence would be required;
- offer safer wording;
- identify reviewer risk.

## What Is Not Included

This public package does not include:

- private expert-lens cards;
- personal project rosters;
- source notes from papers;
- generated literature matrices;
- local reference-manager databases or PDFs;
- local scripts, API keys, caches or logs;
- unpublished manuscript-specific examples.

Users can create private local materials for their own research workflow, but
those files should not be committed to this public repository.