# Chat-Native RAG

Use chat-native RAG when the user wants literature support, claim checking,
source-backed writing, reviewer-risk analysis, or mentor-lens evolution inside
the conversation without manually running `scripts/literature_rag.py`.

This is the default RAG mode for normal research discussion. The script remains
available for batch retrieval, exports, Zotero handoff and reproducible audits.

## Core contract

The user should be able to ask:

> Check whether this claim is supported by literature: ...

and receive a source-grounded answer in the chat, with citations, stance,
scope match, adversarial checks and safer wording.

## Default workflow

1. **Extract the claim**
   - Rewrite the user's statement as one or more searchable claims.
   - Mark the intended claim level: title, abstract, Results, Discussion,
     figure caption, cover letter, rebuttal, lens rule or patent claim.

2. **Generate search intents**
   - support query: sources that would directly support the claim;
   - alternative-explanation query: sources that may explain the observation
     differently;
   - boundary query: sources that narrow, contradict or limit the claim;
   - review/background query: sources that define field context.

3. **Retrieve in chat when tools allow**
   - Search the web or scholarly indexes available to the current environment.
   - Prefer primary literature, reviews, official publisher pages, PubMed /
     Europe PMC / Crossref / OpenAlex / Semantic Scholar records, preprints for
     method work, and user-provided PDFs or DOIs.
   - Avoid relying on secondary summaries when a DOI, abstract, publisher page
     or full text is available.

4. **Read enough to judge**
   - Use title + abstract as a provisional check.
   - Use full text, user-provided PDF text, or source-pack notes before upgrading
     a claim to strong support.
   - State when the judgment is abstract-level only.

5. **Adjudicate**
   - Assign stance: supports / qualifies / refutes / insufficient.
   - Assign scope: direct / adjacent / weak / mismatched.
   - Assign action: promote / keep with boundary / demote / remove / search more.

6. **Repair language**
   - Convert the claim into defensible manuscript wording.
   - Add a Claim Passport row when the claim affects major text, figure captions,
     cover letter, rebuttal, patent language or mentor-lens rules.

## Output format

For one claim:

| Item | Decision |
|---|---|
| Claim checked |  |
| Verdict | supports / qualifies / refutes / insufficient |
| Scope match | direct / adjacent / weak / mismatched |
| Evidence level | abstract-level / full-text-read / source-pack-backed |
| Recommended wording |  |
| Next action | promote / keep with boundary / demote / remove / search more |

Then:

| Source | Role | What it supports or challenges | Scope match | Use |
|---|---|---|---|---|
| citation/link | support / adversarial / background |  | direct / adjacent / weak / mismatched | cite / read first / do not cite |

For multiple claims, return a compact matrix:

| Claim ID | Claim | Verdict | Best support | Best adversarial/boundary source | Wording action |
|---|---|---|---|---|---|

## Citation rules

- Every literature-dependent factual statement should have a visible citation or
  source link when search is used.
- Do not cite a source only because it contains similar keywords.
- Prefer the closest source that actually bears on the claim.
- Mark citation role: background, method precedent, mechanism support,
  limitation, counterexample or benchmark.
- Do not invent citations, DOIs, titles, authors or journal details.
- If a source cannot be verified, say so and do not use it as support.

## Scholarly source preference

Use this order when possible:

1. user-provided paper/PDF/source note;
2. DOI / publisher page / PubMed / Europe PMC / arXiv record;
3. peer-reviewed review or perspective;
4. reputable scholarly index metadata;
5. general web source only for policy, product, dataset or institutional facts.

## Evidence level labels

| Label | Meaning | Allowed use |
|---|---|---|
| metadata-only | title/venue/year only | discovery only, never support |
| abstract-level | abstract or snippet read | provisional support or boundary |
| full-text-read | relevant full text section read | can support manuscript wording if scope matches |
| source-pack-backed | promoted source note exists | can support lens rule, council decision or claim passport |
| project-evidence-backed | user's own data supports it | can support paper claims, still needs scope control |

## When to escalate to script RAG

Use `scripts/literature_rag.py` instead of chat-only RAG when:

- there are more than 5-8 claims;
- the user needs RIS, ENW, BibTeX or Zotero handoff;
- the output must be reproducible;
- the task is a final submission audit;
- source-note stubs should be generated;
- many providers or filters are needed.

## When to ask the user for PDFs or DOIs

Ask for PDFs, DOIs or paper titles when:

- the claim depends on a specific paper the user has read;
- the relevant literature is paywalled;
- the source must become a mentor-lens rule;
- abstract-level evidence is insufficient;
- the same title has multiple versions or preprint/published conflicts.

## Mentor-lens integration

Chat-native RAG may propose candidate lens updates, but it must not activate
them automatically.

Output:

| Source | Candidate lens rule | Veto/demotion behavior | Confidence effect | Needs source note? |
|---|---|---|---|---|

Activation still follows `references/mentor-lens-evolution.md`.

## Guardrails

- Retrieval is not proof.
- Citations are not decorations.
- A supportive review does not replace project-specific evidence.
- A famous mentor lens cannot override source scope.
- Adversarial search is mandatory for mechanism, application, AI-discovery,
  sustainability, clinical, agricultural or deployment claims.
