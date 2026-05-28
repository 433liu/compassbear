---
name: compassbear-pdf-reader
description: Read local scientific PDFs into CompassBear workflows. Use for extracting PDF text, section/caption candidates, source-note drafts, RAG adjudication inputs and mentor-lens source updates.
---

# CompassBear PDF Reader

## Inherits from CompassBear

Use the CompassBear north-star: **if forced to choose between sounding impressive and being defensible, choose defensible.**

This skill reads PDF content as source material. It does not treat extracted text
as interpreted evidence until the relevant claim, method, figure or limitation
has been checked.

## Trigger calibration

Trigger on: read PDF, parse PDF, extract PDF, PDF source note, read this paper,
Zotero PDF, 文献 PDF, 读这篇文章, 从 PDF 提炼 source note, 从 PDF 更新导师 lens.

## Output-first contract

Return something immediately useful:

- extracted title/section/caption candidates when available;
- source-note worksheet;
- stance/scope/action if a claim is supplied;
- candidate mentor-lens rules only after reading relevant content;
- warning when the PDF extractor lacks a backend or extraction is poor.

## Workflow

1. Identify the PDF path, usually from user input or local Zotero lookup.
2. Extract text using `scripts/pdf_extract.py`.
3. Check extraction quality warnings. If the PDF is slide-like, chart-heavy, scanned or has no section/caption candidates, inspect rendered page-review PNGs/contact sheets before making scientific judgments.
4. Identify section headers, abstract-like text and figure/table caption candidates from text plus rendered pages.
5. Ask or infer the claim under adjudication.
5. Convert relevant passages into source-note fields:
   - stance;
   - scope match;
   - action;
   - load-bearing finding;
   - caveat/boundary.
6. If the user asks to update a mentor lens, propose candidate lens rules but do
   not activate them unless source thresholds are met.

## Local command

```bash
python scripts/cb.py pdf "path/to/paper.pdf"
```

Direct helper:

```bash
python scripts/pdf_extract.py "path/to/paper.pdf"
```

For chart-heavy or slide-exported PDFs, force visual review assets:

```bash
python scripts/pdf_extract.py --render-pages always --render-scale 0.8 "path/to/paper.pdf"
```

Outputs land in the current working directory by default:

```text
outputs/pdf-extract/<pdf-stem>/
```

The Markdown scaffold reports extraction quality, warnings, page PNGs and contact sheets when available.

## Guardrails

- PDF extraction quality varies; bad extraction is not evidence.
- For visual-heavy PDFs, do not infer article style or claim support from extracted text alone; inspect rendered pages and mark image-derived observations as provisional.
- Metadata, title or abstract alone is provisional unless the claim is only
  background-level.
- Do not invent missing methods, controls, figures or conclusions.
- Do not create mentor-lens veto rules from one paper unless the rule is narrow
  and labeled candidate.
- Do not copy private PDFs into public examples.

## Reference routing

- PDF/source handoff: `../../references/pdf-source-ingestion.md`
- Local Zotero read-only: `../../references/local-zotero-read.md`
- Mentor lens evolution: `../../references/mentor-lens-evolution.md`
