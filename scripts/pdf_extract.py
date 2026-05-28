#!/usr/bin/env python3
"""Extract readable text and visual review assets from PDFs for CompassBear.

The extractor tries common Python PDF backends in this order:
  1. PyMuPDF (`fitz`)
  2. pypdf
  3. PyPDF2
  4. pdfplumber

No dependency is vendored in this package. If none is installed, the script exits
with a clear message. By default it writes outputs under the current working
directory at `outputs/pdf-extract/<pdf-stem>/`, avoiding writes into the installed
skill package.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable, List, Optional, Tuple


@dataclass
class PageText:
    page: int
    text: str


@dataclass
class ExtractResult:
    pdf: str
    backend: str
    pages: int
    text_chars: int
    extraction_quality: str
    warnings: List[str]
    sections: List[str]
    figure_caption_candidates: List[str]
    rendered_pages: List[str]
    contact_sheets: List[str]


def normalize_text(text: str) -> str:
    text = (text or "").replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_with_fitz(pdf_path: Path) -> Optional[List[PageText]]:
    try:
        import fitz  # type: ignore
    except Exception:
        return None
    pages: List[PageText] = []
    doc = fitz.open(str(pdf_path))
    try:
        for i, page in enumerate(doc, 1):
            pages.append(PageText(page=i, text=normalize_text(page.get_text("text"))))
    finally:
        doc.close()
    return pages


def extract_with_pypdf(pdf_path: Path) -> Optional[List[PageText]]:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        return None
    reader = PdfReader(str(pdf_path))
    pages: List[PageText] = []
    for i, page in enumerate(reader.pages, 1):
        pages.append(PageText(page=i, text=normalize_text(page.extract_text() or "")))
    return pages


def extract_with_pypdf2(pdf_path: Path) -> Optional[List[PageText]]:
    try:
        from PyPDF2 import PdfReader  # type: ignore
    except Exception:
        return None
    reader = PdfReader(str(pdf_path))
    pages: List[PageText] = []
    for i, page in enumerate(reader.pages, 1):
        pages.append(PageText(page=i, text=normalize_text(page.extract_text() or "")))
    return pages


def extract_with_pdfplumber(pdf_path: Path) -> Optional[List[PageText]]:
    try:
        import pdfplumber  # type: ignore
    except Exception:
        return None
    pages: List[PageText] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            pages.append(PageText(page=i, text=normalize_text(page.extract_text() or "")))
    return pages


BACKENDS: List[tuple[str, Callable[[Path], Optional[List[PageText]]]]] = [
    ("fitz", extract_with_fitz),
    ("pypdf", extract_with_pypdf),
    ("PyPDF2", extract_with_pypdf2),
    ("pdfplumber", extract_with_pdfplumber),
]


def extract_pdf(pdf_path: Path, preferred_backend: str = "auto") -> tuple[str, List[PageText]]:
    if not pdf_path.exists():
        raise SystemExit(f"ERROR: PDF not found: {pdf_path}")
    backends = BACKENDS
    if preferred_backend != "auto":
        backends = [b for b in BACKENDS if b[0].lower() == preferred_backend.lower()]
        if not backends:
            raise SystemExit(f"ERROR: unsupported backend: {preferred_backend}")
    errors: List[str] = []
    for name, func in backends:
        try:
            pages = func(pdf_path)
            if pages is None:
                continue
            return name, pages
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{name}: {exc}")
    msg = [
        "ERROR: no PDF extraction backend is available.",
        "Install one of: PyMuPDF (`pip install pymupdf`), pypdf, PyPDF2, or pdfplumber.",
        "For visual-heavy PDFs, PyMuPDF is preferred because it can render page review assets.",
    ]
    if errors:
        msg.append("Backend errors:")
        msg.extend(f"  - {e}" for e in errors)
    raise SystemExit("\n".join(msg))


def split_sections(text: str) -> List[str]:
    candidates = []
    section_re = re.compile(
        r"(?im)^(abstract|introduction|results?|discussion|conclusions?|methods?|experimental|references|acknowledg(e)?ments|supporting information)\b.*$"
    )
    for match in section_re.finditer(text):
        candidates.append(match.group(0).strip())
    seen = []
    for c in candidates:
        if c not in seen:
            seen.append(c)
    return seen


def figure_caption_candidates(text: str, limit: int = 30) -> List[str]:
    pattern = re.compile(r"(?is)\b(Fig\.|Figure|Scheme|Table)\s+\d+[A-Za-z]?[.:]?\s+.{40,900}?(?=\n\s*\n|\b(?:Fig\.|Figure|Scheme|Table)\s+\d+|$)")
    out: List[str] = []
    for match in pattern.finditer(text):
        caption = normalize_text(match.group(0))
        caption = re.sub(r"\s+", " ", caption)
        out.append(caption[:1200])
        if len(out) >= limit:
            break
    return out


def page_blocks(pages: Iterable[PageText]) -> str:
    chunks: List[str] = []
    for p in pages:
        chunks.append(f"\n\n--- Page {p.page} ---\n\n{p.text}")
    return normalize_text("\n".join(chunks))


def default_out_dir(pdf_path: Path) -> Path:
    safe_stem = re.sub(r"[^A-Za-z0-9_.-]+", "-", pdf_path.stem).strip("-_") or "pdf"
    return Path.cwd() / "outputs" / "pdf-extract" / safe_stem


def classify_extraction(full_text: str, page_count: int, sections: List[str], captions: List[str]) -> Tuple[str, List[str]]:
    warnings: List[str] = []
    chars_per_page = len(full_text) / max(page_count, 1)
    numericish_lines = 0
    nonempty_lines = 0
    for line in full_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        nonempty_lines += 1
        tokens = re.findall(r"[A-Za-z]+|\d+(?:\.\d+)?|[%/°µηλ−-]", stripped)
        numeric_tokens = sum(1 for token in tokens if re.search(r"\d|[%/°µηλ−-]", token))
        if tokens and numeric_tokens / len(tokens) >= 0.55:
            numericish_lines += 1
    numericish_ratio = numericish_lines / max(nonempty_lines, 1)

    if chars_per_page < 500:
        warnings.append("Low extracted text per page; this may be scanned, image-heavy or chart-heavy.")
    if not sections:
        warnings.append("No standard manuscript section headings detected.")
    if not captions:
        warnings.append("No figure/table captions detected; figures may be embedded as slide graphics or images.")
    if numericish_ratio > 0.45:
        warnings.append("Many extracted lines look like axes, tick labels or table values; inspect rendered pages before adjudicating claims.")

    if chars_per_page < 500 or (not sections and not captions) or numericish_ratio > 0.45:
        return "visual-heavy / low-structure", warnings
    if sections or captions:
        return "structured text", warnings
    return "plain text", warnings


def should_render_pages(mode: str, quality: str) -> bool:
    if mode == "always":
        return True
    if mode == "never":
        return False
    return quality.startswith("visual-heavy")


def render_review_assets(pdf_path: Path, out_dir: Path, scale: float, per_sheet: int = 6) -> Tuple[List[str], List[str], List[str]]:
    warnings: List[str] = []
    try:
        import fitz  # type: ignore
    except Exception:
        return [], [], ["Page rendering skipped because PyMuPDF (`fitz`) is not installed."]

    pages_dir = out_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    rendered_pages: List[str] = []
    contact_sheets: List[str] = []
    doc = fitz.open(str(pdf_path))
    try:
        matrix = fitz.Matrix(scale, scale)
        for i, page in enumerate(doc, 1):
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            image_path = pages_dir / f"page-{i:02d}.png"
            pix.save(str(image_path))
            rendered_pages.append(str(image_path))
    finally:
        doc.close()

    try:
        from PIL import Image, ImageDraw  # type: ignore
    except Exception:
        warnings.append("Contact sheets skipped because Pillow is not installed; individual page PNGs were still rendered.")
        return rendered_pages, contact_sheets, warnings

    opened = [(idx + 1, Image.open(path).convert("RGB")) for idx, path in enumerate(rendered_pages)]
    try:
        cols = 3
        for sheet_idx in range(math.ceil(len(opened) / per_sheet)):
            chunk = opened[sheet_idx * per_sheet : (sheet_idx + 1) * per_sheet]
            if not chunk:
                continue
            cell_w = max(img.width for _, img in chunk)
            cell_h = max(img.height for _, img in chunk)
            rows = math.ceil(len(chunk) / cols)
            label_h = 34
            sheet = Image.new("RGB", (cell_w * cols, (cell_h + label_h) * rows), "white")
            draw = ImageDraw.Draw(sheet)
            for j, (page_number, img) in enumerate(chunk):
                x = (j % cols) * cell_w
                y = (j // cols) * (cell_h + label_h)
                draw.text((x + 8, y + 8), f"Page {page_number}", fill=(0, 0, 0))
                sheet.paste(img, (x, y + label_h))
            contact_path = out_dir / f"contact-{sheet_idx + 1}.png"
            sheet.save(contact_path)
            contact_sheets.append(str(contact_path))
    finally:
        for _, img in opened:
            img.close()

    return rendered_pages, contact_sheets, warnings


def render_markdown(result: ExtractResult, full_text: str, max_chars: int) -> str:
    preview = full_text[:max_chars]
    lines = [
        "# CompassBear PDF Extract",
        "",
        f"- PDF: `{result.pdf}`",
        f"- Backend: `{result.backend}`",
        f"- Pages: {result.pages}",
        f"- Extracted characters: {result.text_chars}",
        f"- Extraction quality: {result.extraction_quality}",
        "",
        "## Warnings",
        "",
    ]
    if result.warnings:
        lines.extend(f"- {warning}" for warning in result.warnings)
    else:
        lines.append("- [none]")
    lines.extend(["", "## Rendered page-review assets", ""])
    if result.contact_sheets:
        lines.append("Contact sheets:")
        lines.extend(f"- `{path}`" for path in result.contact_sheets)
    if result.rendered_pages:
        lines.append("")
        lines.append("Individual pages:")
        lines.extend(f"- `{path}`" for path in result.rendered_pages[:12])
        if len(result.rendered_pages) > 12:
            lines.append(f"- ... {len(result.rendered_pages) - 12} more")
    if not result.contact_sheets and not result.rendered_pages:
        lines.append("- [not rendered]")
    lines.extend(["", "## Section candidates", ""])
    if result.sections:
        lines.extend(f"- {s}" for s in result.sections)
    else:
        lines.append("- [none detected]")
    lines.extend(["", "## Figure / table caption candidates", ""])
    if result.figure_caption_candidates:
        for i, caption in enumerate(result.figure_caption_candidates, 1):
            lines.append(f"{i}. {caption}")
    else:
        lines.append("- [none detected]")
    lines.extend(
        [
            "",
            "## Source-note worksheet",
            "",
            "| Field | Value |",
            "|---|---|",
            "| Claim under adjudication |  |",
            "| Stance | supports / qualifies / refutes / insufficient |",
            "| Scope match | direct / adjacent / weak / mismatched |",
            "| Council action | promote / keep / demote / remove / search-more |",
            "| Load-bearing finding |  |",
            "| Caveat / boundary |  |",
            "| Candidate mentor-lens rule |  |",
            "",
            "## Text preview",
            "",
            "```text",
            preview,
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract PDF text and review assets for CompassBear workflows.")
    parser.add_argument("pdf", help="Path to a PDF file.")
    parser.add_argument("--out-dir", default="", help="Defaults to ./outputs/pdf-extract/<pdf-stem> in the current working directory.")
    parser.add_argument("--backend", default="auto", help="auto, fitz, pypdf, PyPDF2, or pdfplumber")
    parser.add_argument("--max-preview-chars", type=int, default=12000)
    parser.add_argument(
        "--render-pages",
        choices=["auto", "always", "never"],
        default="auto",
        help="Render page PNGs/contact sheets. Auto renders visual-heavy or low-structure PDFs when PyMuPDF is available.",
    )
    parser.add_argument("--render-scale", type=float, default=0.45, help="Scale used for page-review PNGs; increase for higher-resolution inspection.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pdf_path = Path(args.pdf).expanduser().resolve()
    backend, pages = extract_pdf(pdf_path, args.backend)
    full_text = page_blocks(pages)
    sections = split_sections(full_text)
    captions = figure_caption_candidates(full_text)
    quality, warnings = classify_extraction(full_text, len(pages), sections, captions)
    out_dir = Path(args.out_dir).expanduser() if args.out_dir else default_out_dir(pdf_path)
    out_dir.mkdir(parents=True, exist_ok=True)

    rendered_pages: List[str] = []
    contact_sheets: List[str] = []
    if should_render_pages(args.render_pages, quality):
        rendered_pages, contact_sheets, render_warnings = render_review_assets(pdf_path, out_dir, args.render_scale)
        warnings.extend(render_warnings)

    result = ExtractResult(
        pdf=str(pdf_path),
        backend=backend,
        pages=len(pages),
        text_chars=len(full_text),
        extraction_quality=quality,
        warnings=warnings,
        sections=sections,
        figure_caption_candidates=captions,
        rendered_pages=rendered_pages,
        contact_sheets=contact_sheets,
    )
    (out_dir / "pdf_text.txt").write_text(full_text, encoding="utf-8")
    (out_dir / "pdf_pages.json").write_text(json.dumps([asdict(p) for p in pages], ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "pdf_extract.json").write_text(json.dumps(asdict(result), ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "pdf_extract.md").write_text(render_markdown(result, full_text, args.max_preview_chars), encoding="utf-8")
    print(f"OK: extracted {len(pages)} page(s) with {backend}. Wrote {out_dir / 'pdf_extract.md'}")
    if rendered_pages:
        print(f"OK: rendered {len(rendered_pages)} page-review PNG(s).")
    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
