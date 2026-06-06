# RAG Evidence Adjudicator

The adjudicator judges whether opened sources actually support a claim.

## Inputs

- claim;
- source titles or links;
- relevant passages when available;
- user-provided source notes when available.

## Stance

| Stance | Meaning |
|---|---|
| support | source directly supports the scoped claim |
| qualify | source supports a narrower or conditional version |
| refute | source conflicts with the claim |
| insufficient | source is only adjacent or too weak |

## Scope Check

Check population, material, mechanism, method, timescale, performance metric and application context. A source that supports one scope does not automatically support a broader one.

## Output

Return:

- evidence matrix;
- stance;
- scope mismatch if any;
- reviewer risk;
- safer wording;
- next source action.

Do not treat search results, abstracts or tool output as final proof unless the relevant source content has been inspected.
