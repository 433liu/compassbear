# Local Zotero Read-Only Workflow

Use this protocol when the user asks to inspect local Zotero literature without
dragging files into the workspace.

Supported requests:

- "Look in my Zotero for papers about XXX."
- "Find a PDF under `C:\\Users\\<you>\\Zotero\\storage`."
- "Read title / authors / DOI from my Zotero database."
- "Use Zotero papers about XXX to update a mentor lens."

## Safety contract

Local Zotero access is read-only by default.

Allowed:

- read `zotero.sqlite`;
- read `storage/`;
- resolve PDF attachment paths;
- copy PDFs into `outputs/zotero-local/pdfs/` if the user asks;
- write search reports into the current CompassBear project.

Not allowed without explicit confirmation:

- modify `zotero.sqlite`;
- move, rename or delete Zotero attachments;
- write tags into the local Zotero database;
- reorganize Zotero collections;
- bulk-copy private PDFs into a public package.

## Default local paths

The default Zotero data directory is:

```text
C:\Users\<you>\Zotero
```

The helper also respects:

```text
ZOTERO_DATA_DIR=
```

in `.env` if the library lives elsewhere.

## Local helper

Use:

```bash
python scripts/zotero_local_read.py --query "catalyst stability screening"
```

or via the unified command surface:

```bash
python scripts/cb.py zotero --query "catalyst stability screening"
```

To copy matched PDFs into the current project without touching Zotero:

```bash
python scripts/cb.py zotero --query "catalyst stability screening" --copy-pdfs
```

Outputs:

- `outputs/zotero-local/zotero_search.md`
- `outputs/zotero-local/zotero_search.json`
- optional copied PDFs under `outputs/zotero-local/pdfs/`

To read one matched PDF after finding it:

```bash
python scripts/cb.py pdf "C:\Users\<you>\Zotero\storage\<KEY>\<file>.pdf"
```

or, if copied:

```bash
python scripts/cb.py pdf "outputs/zotero-local/pdfs/<file>.pdf"
```

## Mentor-lens handoff

When using Zotero papers to update a mentor lens:

1. Search local Zotero.
2. Choose the relevant item/PDF.
3. Read the abstract or PDF excerpt.
4. Draft a source note with stance, scope and action.
5. Propose candidate lens rules.
6. Do not activate the lens rule unless the mentor-lens source threshold is met.

## Output shape

| Item | Title | Authors | DOI | PDF path | Evidence use |
|---|---|---|---|---|---|
|  |  |  |  |  | read first / source-note candidate / not relevant |

Then:

| Source | Candidate lens rule | Veto/demotion behavior | Needs more sources? |
|---|---|---|---|

## Guardrails

- Zotero metadata alone is not evidence.
- A PDF path alone is not a source note.
- Read the relevant paper section before creating a claim-demotion rule.
- Keep copied PDFs in private outputs, not public examples.
