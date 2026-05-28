#!/usr/bin/env python3
"""Small CompassBear command surface.

This is not meant to replace the chat-first workflow. It gives repeatable local
entry points for checks, protocol discovery and heavy RAG runs when a user wants
tooling rather than conversation.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PROTOCOLS = [
    ("pipeline", "references/compassbear-pipeline.md", "end-to-end paper/project gates"),
    ("claim-passport", "references/claim-passport.md", "claim traceability and demotion wording"),
    ("chat-rag", "references/chat-native-rag.md", "in-chat literature support workflow"),
    ("journal-style", "references/journal-style-profiles.md", "JACS / Angew / AM positioning"),
    ("mentor-evolution", "references/mentor-lens-evolution.md", "source-note-backed mentor lens updates"),
    ("user-preference", "references/user-preference-lens.md", "private user taste and evidence override rules"),
    ("local-zotero", "references/local-zotero-read.md", "read local Zotero metadata and PDF paths"),
    ("pdf-reader", "skills/compassbear-pdf-reader/SKILL.md", "extract PDF text into source-note workflows"),
    ("wechat-distiller", "skills/compassbear-wechat-distiller/SKILL.md", "merge WeChat chunks into research memory"),
    ("wechat-export", "references/wechat-export-automation.md", "safe WeChat clipboard/export automation boundary"),
    ("figure-production", "references/figure-production-bridge.md", "figure logic to production assets"),
    ("pdf-source", "references/pdf-source-ingestion.md", "DOI/PDF/source-note handoff"),
    ("benchmarks", "examples/benchmark-suite.md", "public examples and regression prompts"),
    ("iteration", "references/first-principles-iteration.md", "feature intake and adopt/adapt/reject"),
]

CHECKS = [
    "scripts/check_literature_rag_integration.py",
    "scripts/check_source_pack_promotion.py",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def run(cmd: list[str]) -> int:
    return subprocess.call(cmd, cwd=ROOT)


def cmd_protocols(_: argparse.Namespace) -> int:
    print("CompassBear protocols:")
    for name, path, note in PROTOCOLS:
        exists = "OK" if (ROOT / path).exists() else "MISSING"
        print(f"- {name:18} {exists:7} {path} - {note}")
    return 0


def cmd_doctor(_: argparse.Namespace) -> int:
    print(f"CompassBear root: {ROOT}")
    required = ["SKILL.md", "README.md", "USAGE.md", "scripts/literature_rag.py", "scripts/zotero_sync.py", "scripts/zotero_local_read.py", "scripts/pdf_extract.py", "scripts/wechat_distill.py", "scripts/wechat_clipboard_capture.py", "scripts/wechat_ui_macro.py"]
    failures = []
    for item in required:
        path = ROOT / item
        status = "OK" if path.exists() else "MISSING"
        print(f"- {status:7} {item}")
        if not path.exists():
            failures.append(item)
    env = ROOT / ".env"
    print(f"- {'OK' if env.exists() else 'OPTIONAL'} .env")
    for key in ["UNPAYWALL_EMAIL", "ZOTERO_API_KEY", "ZOTERO_USER_ID"]:
        state = "set" if os.getenv(key) else "not set"
        print(f"- env {key}: {state}")
    return 1 if failures else 0


def cmd_checks(_: argparse.Namespace) -> int:
    for script in CHECKS:
        path = ROOT / script
        if not path.exists():
            print(f"FAIL: missing {script}", file=sys.stderr)
            return 1
        code = run([sys.executable, str(path)])
        if code != 0:
            return code
    return 0


def cmd_rag(args: argparse.Namespace) -> int:
    rag = ROOT / "scripts/literature_rag.py"
    cmd = [
        sys.executable,
        str(rag),
        "--claim",
        args.claim,
        "--profile",
        args.profile,
        "--max-per-provider",
        str(args.max_per_provider),
    ]
    if args.with_html_review:
        cmd.append("--with-html-review")
    if args.export:
        cmd.extend(["--export", args.export])
    if args.source_notes:
        cmd.extend(["--source-note-dir", "source-packs/generated"])
    for query in args.support_query or []:
        cmd.extend(["--support-query", query])
    for query in args.adversarial_query or []:
        cmd.extend(["--adversarial-query", query])
    return run(cmd)

def cmd_zotero(args: argparse.Namespace) -> int:
    script = ROOT / "scripts/zotero_local_read.py"
    cmd = [sys.executable, str(script), "--query", args.query, "--limit", str(args.limit)]
    if args.zotero_dir:
        cmd.extend(["--zotero-dir", args.zotero_dir])
    if args.copy_pdfs:
        cmd.append("--copy-pdfs")
    return run(cmd)

def cmd_pdf(args: argparse.Namespace) -> int:
    script = ROOT / "scripts/pdf_extract.py"
    cmd = [sys.executable, str(script), args.pdf]
    if args.out_dir:
        cmd.extend(["--out-dir", args.out_dir])
    if args.backend:
        cmd.extend(["--backend", args.backend])
    if args.render_pages:
        cmd.extend(["--render-pages", args.render_pages])
    if args.render_scale:
        cmd.extend(["--render-scale", str(args.render_scale)])
    return run(cmd)

def cmd_wechat(args: argparse.Namespace) -> int:
    script = ROOT / "scripts/wechat_distill.py"
    cmd = [sys.executable, str(script)]
    for path in args.input or []:
        cmd.extend(["--input", path])
    if args.stdin:
        cmd.append("--stdin")
    if args.project:
        cmd.extend(["--project", args.project])
    if args.topic:
        cmd.extend(["--topic", args.topic])
    if args.out_dir:
        cmd.extend(["--out-dir", args.out_dir])
    if args.no_dedupe:
        cmd.append("--no-dedupe")
    return run(cmd)

def cmd_wechat_capture(args: argparse.Namespace) -> int:
    script = ROOT / "scripts/wechat_clipboard_capture.py"
    cmd = [sys.executable, str(script)]
    if args.once:
        cmd.append("--once")
    else:
        cmd.append("--watch")
    if args.out_dir:
        cmd.extend(["--out-dir", args.out_dir])
    cmd.extend(["--min-chars", str(args.min_chars), "--interval", str(args.interval)])
    return run(cmd)

def cmd_wechat_ui(args: argparse.Namespace) -> int:
    script = ROOT / "scripts/wechat_ui_macro.py"
    cmd = [sys.executable, str(script), args.mode]
    if args.mode == "pos":
        cmd.extend(["--delay", str(args.delay)])
    elif args.mode == "init":
        if args.config:
            cmd.extend(["--config", args.config])
    elif args.mode == "run":
        if args.config:
            cmd.extend(["--config", args.config])
        cmd.extend(["--loops", str(args.loops)])
        if args.out_dir:
            cmd.extend(["--out-dir", args.out_dir])
        if args.min_chars:
            cmd.extend(["--min-chars", str(args.min_chars)])
        if args.i_understand_ui_automation_risk:
            cmd.append("--i-understand-ui-automation-risk")
    return run(cmd)


def cmd_examples(_: argparse.Namespace) -> int:
    prompts = [
        "Use RAG to check whether this claim is supported by literature: <claim>",
        "Turn these claims into a Claim Passport and mark demotion wording.",
        "Compare JACS, Angew and Advanced Materials fit for this abstract.",
        "Use research council to decide mechanism vs platform vs application framing.",
        "Convert this paper into a figure spine with main/Extended/SI allocation.",
        "Update a mentor lens from this paper without imitating personal voice.",
        "Look in my local Zotero for papers about <topic> and draft source-note candidates.",
        "Read this PDF and turn it into a source-note worksheet: <path>",
        "Distill these WeChat chunks into decisions, claims, preferences and mentor-lens candidates.",
        "Watch clipboard while I copy WeChat notes, then distill captured chunks.",
        "Run a calibrated WeChat UI macro to repeat export/copy/capture for many chunks.",
        "Run first-principles iteration on this competitor feature.",
    ]
    for prompt in prompts:
        print(f"- {prompt}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CompassBear local helper")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("protocols", help="List key protocols and files")
    p.set_defaults(func=cmd_protocols)

    p = sub.add_parser("doctor", help="Check local setup basics")
    p.set_defaults(func=cmd_doctor)

    p = sub.add_parser("checks", help="Run CompassBear static checks")
    p.set_defaults(func=cmd_checks)

    p = sub.add_parser("examples", help="Print useful test prompts")
    p.set_defaults(func=cmd_examples)

    p = sub.add_parser("rag", help="Run heavy literature RAG")
    p.add_argument("--claim", required=True)
    p.add_argument("--profile", default="broad", choices=["broad", "materials-mechanism", "computational-methods", "bio-application"])
    p.add_argument("--max-per-provider", type=int, default=5)
    p.add_argument("--with-html-review", action="store_true")
    p.add_argument("--source-notes", action="store_true", help="Write generated source-note stubs")
    p.add_argument("--export", choices=["ris", "enw", "bib"], default="")
    p.add_argument("--support-query", action="append", default=[])
    p.add_argument("--adversarial-query", action="append", default=[])
    p.set_defaults(func=cmd_rag)

    p = sub.add_parser("zotero", help="Read local Zotero metadata/PDF paths without modifying Zotero")
    p.add_argument("--query", required=True)
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--zotero-dir", default="", help="Defaults to ZOTERO_DATA_DIR or ~/Zotero")
    p.add_argument("--copy-pdfs", action="store_true", help="Copy matched PDFs into outputs/zotero-local/pdfs")
    p.set_defaults(func=cmd_zotero)

    p = sub.add_parser("pdf", help="Extract text and review assets from a local PDF into ./outputs/pdf-extract/<pdf-stem>")
    p.add_argument("pdf")
    p.add_argument("--out-dir", default="")
    p.add_argument("--backend", default="auto", help="auto, fitz, pypdf, PyPDF2, or pdfplumber")
    p.add_argument("--render-pages", choices=["auto", "always", "never"], default="auto")
    p.add_argument("--render-scale", type=float, default=0.45)
    p.set_defaults(func=cmd_pdf)

    p = sub.add_parser("wechat", help="Merge WeChat note/text chunks into a distillation worksheet")
    p.add_argument("--input", action="append", default=[], help="Text/Markdown file or directory. Can repeat.")
    p.add_argument("--stdin", action="store_true")
    p.add_argument("--project", default="")
    p.add_argument("--topic", default="")
    p.add_argument("--out-dir", default="")
    p.add_argument("--no-dedupe", action="store_true")
    p.set_defaults(func=cmd_wechat)

    p = sub.add_parser("wechat-capture", help="Capture copied WeChat note chunks from clipboard")
    group = p.add_mutually_exclusive_group()
    group.add_argument("--once", action="store_true")
    group.add_argument("--watch", action="store_true")
    p.add_argument("--out-dir", default="")
    p.add_argument("--min-chars", type=int, default=80)
    p.add_argument("--interval", type=float, default=1.0)
    p.set_defaults(func=cmd_wechat_capture)

    p = sub.add_parser("wechat-ui", help="Run guarded calibrated UI macro for repetitive WeChat export")
    p.add_argument("mode", choices=["pos", "init", "run"])
    p.add_argument("--config", default="")
    p.add_argument("--delay", type=float, default=3.0)
    p.add_argument("--loops", type=int, default=1)
    p.add_argument("--out-dir", default="")
    p.add_argument("--min-chars", type=int, default=0)
    p.add_argument("--i-understand-ui-automation-risk", action="store_true")
    p.set_defaults(func=cmd_wechat_ui)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
