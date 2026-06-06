# Chat-Native RAG

Use this protocol when a claim needs literature support inside the conversation.

## Workflow

1. Extract the exact claim.
2. Search for support and at least one adversarial route when tools are available.
3. Separate search leads from evidence actually opened and read.
4. Judge stance: support, qualify, refute, or insufficient.
5. Repair the claim with safer scope and wording.

## Evidence Labels

| Label | Meaning |
|---|---|
| search lead | found by title/abstract/search result only |
| abstract-level | abstract supports only a provisional judgment |
| full-text-read | relevant passage has been inspected |
| user-provided source note | user supplied a source-backed summary or excerpt |

Do not call a topic novel from exact-keyword absence. Use synonyms, mechanism equivalents, application equivalents and seed-paper citation routes before making a blank-space claim.

## Output

Return:

- claim under review;
- sources opened or source leads;
- stance and scope;
- reviewer risk;
- safer wording;
- next cheapest evidence action.
