# RAG Evidence Adjudicator

This reference defines the anonymous retrieval-and-evidence role for CompassBear Research Council. It is designed to connect council opinions to traceable literature/source-note support and to actively search for counter-evidence.

## Identity

The RAG Evidence Adjudicator is not a professor persona. It is an evidence procedure. It can overrule or qualify any lens recommendation when the literature/source-note basis is weak, adjacent or contradictory.

## Evidence loop

1. **Claim extraction** — rewrite each recommendation as a compact claim that can be searched or checked.
2. **Support retrieval** — find sources that directly support the claim.
3. **Refutation retrieval** — find sources that contradict, limit or narrow the claim.
4. **Scope matching** — compare material class, structure, state, measurement condition, device/application context and time scale.
5. **Verdict** — assign supports / qualifies / refutes / insufficient.
6. **Language repair** — convert the claim to a defensible wording level.

## Integrated retrieval workflow

For ordinary literature support inside a conversation, use
`references/chat-native-rag.md` first. The default user experience should be:
claim extraction, support and adversarial search, visible citations,
stance/scope/action judgment, and wording repair in the chat.

Use the skill-local helper when the task needs batch retrieval, export, Zotero
handoff, source-note stub generation or reproducible audit:

```bash
python scripts/literature_rag.py \
  --claim "<claim under adjudication>" \
  --profile materials-mechanism \
  --with-html-review \
  --max-per-provider 5 \
  --source-note-dir source-packs/generated
```

The helper also accepts longer text and claim lists, then splits them into stable
claim segments and generates support, adversarial and background queries:

```bash
python scripts/literature_rag.py \
  --text-file manuscript-section.txt \
  --profile bio-application \
  --from-year 2015 \
  --with-html-review \
  --export ris \
  --source-note-dir source-packs/generated
```

Use `--claim-file claims.txt` when you already have one claim per line. Use manual
`--support-query`, `--adversarial-query` and `--query` only when the automatic
profile queries miss the concept.

## In-chat lite RAG

Use chat-native RAG for rapid council iteration and normal claim checking, not
for final source-pack promotion.

The full protocol is `references/chat-native-rag.md`. The short version is:

1. extract the claim;
2. search support, alternative explanation and boundary/counterexample
   directions when tools allow;
3. cite visible sources;
4. assign stance, scope match and action;
5. repair wording;
6. escalate to script RAG only for batch/export/Zotero/reproducibility needs.

### Mode A — query-plan only

Use this when the user wants to keep thinking in chat or network access is not
available. Output:

| Claim | Support query | Adversarial query 1 | Adversarial query 2 | Best profile | What would count as direct support |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

Adversarial query 1 should target alternative explanations. Adversarial query 2
should target boundary conditions, counterexamples, controls or failed
replications.

### Mode B — in-chat candidate check

Use this when the chat environment can browse or the user pastes candidate
papers/DOIs. Return a compact table:

| Claim | Candidate | Retrieval route | Provisional stance | Scope match | Use now? |
|---|---|---|---|---|---|
|  |  | support / adversarial / pasted DOI | supports / qualifies / refutes / insufficient | direct / adjacent / weak / mismatched | yes / no / read first |

Rules:

- keep candidates to the top 3-5 per claim;
- never promote `metadata-only` candidates;
- state when the result is only an abstract-level check;
- if a claim is being upgraded, require the full workflow or a promoted source-pack note.

The helper retrieves candidates across these providers:

| Provider | Cost | Strength | Key needed |
|---|---|---|---|
| `semantic_scholar` | free | broad chemistry / materials / methods coverage; citation counts | optional (higher rate) |
| `crossref` | free | canonical DOI metadata; venue + dates | mailto recommended |
| `openalex` | free | broadest scholarly index; OA links | mailto + optional key |
| `europepmc` | free | biomedical and life-science OA full-text subset | none |
| `arxiv` | free | ML methods (PolyBERT, ChemBERTa, equivariant nets); preprints | none |
| `serper` | paid | Google web fallback for non-indexed pages | `SERPER_API_KEY` |

After the metadata pass, the helper runs an **Unpaywall OA upgrade**: any DOI without an OA PDF link is queried at `api.unpaywall.org`, and the best open-access PDF link is folded back into the record. This requires `UNPAYWALL_EMAIL` in `.env`. Use `--no-unpaywall` to disable.

### Domain profiles

Profiles generate support, adversarial and background queries from each claim and
choose a provider backbone:

| Profile | Providers | Best for |
|---|---|---|
| `broad` | semantic_scholar, crossref, openalex, europepmc, arxiv, serper | unknown or mixed topics |
| `materials-mechanism` | semantic_scholar, openalex, crossref, serper | material structure-property mechanisms, stability claims and artefact checks |
| `computational-methods` | arxiv, semantic_scholar, openalex, crossref | scientific ML baselines, active learning and representation benchmarks |
| `bio-application` | europepmc, openalex, semantic_scholar, crossref, serper | biological or applied-performance claims with control and confounder checks |

Automatic grades in the matrix (`direct-support`, `partial-support`,
`background-only`, `contradictory-or-limiting`, `metadata-only`) are retrieval
triage labels, not final evidence verdicts. `metadata-only` must never be cited
as support without checking the abstract or full text.

The helper writes:

- `outputs/literature-rag/evidence_matrix.md`
- `outputs/literature-rag/evidence_matrix.json`
- optional `outputs/literature-rag/evidence_review.html` with a browsable claim-to-candidate table
- optional `outputs/literature-rag/references.ris`, `.enw` or `.bib` when `--export` is used
- optional source-note **stubs** under `source-packs/generated/`. Stubs carry `TBD` placeholders and a TODO checklist; they are not citable until promoted (see next section).

Retrieval is not proof: after the matrix is generated, the adjudicator must still read the candidates, assess scope match and assign a verdict.

## Human-in-the-loop step

`literature_rag.py` deliberately stops at metadata + abstract. Reading the full text and judging whether a paper actually supports or refutes a claim is a human task. The skill's job is to make that handoff structured and reversible, not to automate it away.

The full pipeline is a one-way relay across three discrete stages:

| Stage | Who | Tool |
|---|---|---|
| 1. Retrieve | machine | `scripts/literature_rag.py` → stubs land in `source-packs/generated/` |
| 2a. Stage in Zotero (optional) | machine | `scripts/zotero_sync.py push` → items land in your Zotero collection |
| 2b. Read & tag | human | Zotero (download full text via institutional access; read; tag; write one child note) |
| 2c. Pull tagged items back (optional) | machine | `scripts/zotero_sync.py pull` → updated stubs land in `source-packs/from-zotero/` |
| 3. Promote | human | Move the finished stub out of any `generated/` or `from-zotero/` staging subdir into `source-packs/` itself, assign a stable `source_id`, fill stance / scope / action / 1–3 sentence summary |
| 4. Validate | machine | `scripts/check_source_pack_promotion.py` → fails if any promoted stub still has `TBD` placeholders |

A source-pack note may only be cited by a lens card or the council voting map after stage 4 passes. Staging subdirs (`generated/`, `from-zotero/`) are explicitly exempt from the validator so unfinished work can live there without breaking CI.

### Promotion checklist (mirrored in every generated stub)

- [ ] Read the paper (or its OA full text, or arrange institutional access)
- [ ] Assign a stable `source_id` (`S1`, `S2`, ...) in the frontmatter
- [ ] Replace `stance: TBD` with `supports / qualifies / refutes / insufficient`
- [ ] Replace `scope: TBD` with `direct / adjacent / weak / mismatched`
- [ ] Replace `action: TBD` with `promote / keep / demote / remove / search-more`
- [ ] Add 1–3 sentences on the load-bearing finding in the Notes section
- [ ] Move the file out of any `generated/` or `from-zotero/` staging subdir into `source-packs/`

## Zotero handoff

Zotero is the practical bridge between machine retrieval and human reading. The `scripts/zotero_sync.py` helper has two modes:

```bash
# After literature_rag.py finishes:
python scripts/zotero_sync.py push --from-json outputs/literature-rag/evidence_matrix.json

# Read in Zotero, download full text, apply cb/ tags, write a child note,
# then add the cb/ready tag to items you want to graduate. When ready:
python scripts/zotero_sync.py pull --out-dir source-packs/from-zotero
```

Requires `ZOTERO_API_KEY` and `ZOTERO_USER_ID` in `.env`. A free key is issued at https://www.zotero.org/settings/keys; your numeric user ID is on the same page.

### Tag convention

The pull step reads Zotero tags to fill the structured fields in the source-pack stub. Use hierarchical tags via `/` — Zotero's UI supports this natively.

| Tag | Meaning | Maps to stub field |
|---|---|---|
| `cb/from-rag` | item came from `literature_rag.py` push | filter only |
| `cb/intent/(support\|adversarial\|neutral)` | original retrieval intent | informational |
| `cb/provider/(semantic_scholar\|openalex\|europepmc\|...)` | who returned it | informational |
| `cb/stance/(supports\|qualifies\|refutes\|insufficient)` | your evidence judgment | `stance` |
| `cb/scope/(direct\|adjacent\|weak\|mismatched)` | scope match to the claim | `scope` |
| `cb/action/(promote\|keep\|demote\|remove\|search-more)` | council action | `action` |
| `cb/claim/<id>` | the claim this evidence bears on (e.g. `cb/claim/E2`) | `claims` list |
| `cb/ready` | item is ready to be pulled into a source-pack stub | gate for pull |

A child note attached to the item provides the free-text summary that lands in the stub's "Notes from Zotero" section. Keep it short (1–3 sentences) — what does this paper actually show that bears on the claim, including any caveat the abstract hides.

### Why Zotero (and not a custom annotation UI)

Zotero already does PDF storage, annotation, search, deduplication and citation export. Recreating any of that inside CompassBear would duplicate it badly. The bridge keeps responsibilities clean:

- `literature_rag.py` finds candidates
- Zotero stores PDFs, captures human reading, holds tags + notes
- `zotero_sync.py` translates between the two stores
- `check_source_pack_promotion.py` enforces that nothing half-finished gets cited

## Institutional access boundary

Web of Science, Scopus, ScienceDirect, ACS, RSC, Wiley, Springer Nature, CNKI and similar institutional database subscriptions are **browser-only IP-gated access** by default. They cannot be plumbed into this script.

To use an institutional database programmatically, the institution must hold a **separate API agreement** — for example WoS Starter API, Scopus API, Elsevier TDM API, or Wiley TDM. Browser subscriptions do not include these. Check with the library reference desk specifically about "API access" or "Text and Data Mining (TDM) agreement"; most institutions do not have them.

If you obtain an institutional API key, add a `search_<provider>` function in `scripts/literature_rag.py` mirroring the existing providers, and register it in the `funcs` dict inside `retrieve()`. Respect TDM license rate caps and the institution's terms.

For paywalled full text, the practical workflow remains:

1. Run `literature_rag.py` to find candidates and DOIs.
2. Push them to Zotero with `zotero_sync.py push`.
3. Open each candidate in a browser via institutional access (campus IP, VPN, CARSI); download the PDF.
4. Drag the PDF onto its Zotero item; read; tag with `cb/` tags; add child note; mark `cb/ready`.
5. Pull back with `zotero_sync.py pull`, then promote out of the staging directory.

Unpaywall covers the gold/green OA fraction of the literature, which is often substantial — start there before assuming a paper is paywalled.

## Evidence strength ladder

| Grade | Meaning | Allowed claim level |
|---|---|---|
| A | Project-specific evidence plus directly matching external literature | title / abstract possible |
| B | Project-specific evidence plus adjacent literature | main-text claim with boundary |
| C | Literature analogy only or project evidence only | cautious Results / Discussion wording |
| D | Contradictory, weak or scope-mismatched evidence | remove or frame as hypothesis |

## Mandatory adversarial query

For each major claim, run at least two search or source-note checks that try to disprove it:

1. an alternative-explanation query;
2. a boundary / counterexample / failed-control query.

Examples:

- contamination or batch-history artefact vs intrinsic material behavior;
- measured property shift vs mechanism-level explanation;
- model-assisted prioritization vs autonomous discovery;
- application benefit vs efficiency or dose-response trade-off;
- sustainability wording vs actual lifetime, recycling or degradation data.

### Adversarial query patterns that work

Patterns observed to actually surface counter-evidence in practice:

- **"Counter-mechanism + physical quantity + target word"**: e.g. *prototype energy penalty efficiency trade-off* — pairs the proposed effect with the physical penalty mechanism. Surfaces engineering trade-off papers that pure topic queries miss.
- **"Alternative explanation + artefact + class"**: e.g. *material performance contamination batch-history artefact* — surfaces the intrinsic-vs-artefact debate.
- **"Scope opposite + same outcome variable"**: e.g. *energy saving cover yield reduction cultivar season* — surfaces papers where the same intervention class had the *opposite* outcome.
- **"Strong-claim word + boundary word"**: e.g. *autonomous closed-loop boundary critique* — surfaces methodological critiques of overclaim language.

## Provider routing heuristics

Different claims need different providers. Pick the right backbone before adding the others:

| Claim type | Primary providers | Why |
|---|---|---|
| Materials mechanism | semantic_scholar, openalex, crossref | broad chemistry / materials coverage |
| ML method comparison | arxiv, semantic_scholar | many ML baselines are arXiv-first |
| Biological or applied-performance claim | europepmc, openalex | strong life-science and OA full-text coverage |
| Synthesis / catalysis | semantic_scholar, crossref | strong chemistry coverage |
| Sustainability / circularity claim | europepmc, openalex, crossref | mix of environmental + materials venues |
| Patent landscape | (Lens.org wiring not yet implemented) | use browser for now |

## Council behavior

When another lens recommends a strong claim, the RAG Evidence Adjudicator must return one of:

- **Promote** — literature and project evidence align directly.
- **Keep with boundary** — evidence supports the core but scope is narrower.
- **Demote** — evidence is plausible but indirect.
- **Remove** — evidence contradicts the claim or the claim depends on missing data.
- **Search more** — the evidence base is too thin to decide.

## Writing rule

Never use RAG output as decorative citations. Every citation must do work: define the field, support a mechanism, set a limitation, justify a method or identify a counterexample.
