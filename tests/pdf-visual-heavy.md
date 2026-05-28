# Visual-heavy PDF Reader Regression

## Prompt

```text
阅读当前目录下的 PDF；使用 $compass-bear；确定文章风格。
```

## Input Shape

A PDF exported from slides containing spectra, tables, chemical structures and photographs, with little manuscript-style text and no standard section headings or figure captions.

## Expected Behavior

- Run `scripts/pdf_extract.py` or `cb.py pdf` against the local PDF.
- Write outputs under the caller's current `outputs/pdf-extract/<pdf-stem>/` unless `--out-dir` is provided.
- Mark extraction quality as visual-heavy / low-structure when section and caption candidates are absent or lines are dominated by axes/tick labels/table values.
- Render page-review PNGs/contact sheets when PyMuPDF is available or explain that rendering is skipped when it is not.
- Inspect rendered pages before making journal-fit, figure-spine or claim-support judgments.
- State that image-derived observations are provisional and should not be treated as full textual evidence.

## Must Not Do

- Do not infer complete manuscript claims from axes and table labels alone.
- Do not silently write outputs into the installed skill package when the caller did not choose that directory.
- Do not treat a clean-looking style recommendation as evidence-backed if the visual page review has not happened.
