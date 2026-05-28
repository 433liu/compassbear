#!/usr/bin/env python3
"""Prepare WeChat chat-note chunks for CompassBear distillation.

This script does not access the WeChat database. It reads exported/pasted text
chunks, merges them, removes exact duplicate lines, and writes a cleaned Markdown
file plus a distillation worksheet under outputs/wechat-distill/.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = ROOT / "outputs" / "wechat-distill"


@dataclass
class ChunkInfo:
    source: str
    original_chars: int
    cleaned_chars: int
    line_count: int


def read_text_file(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "gb18030"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def iter_input_files(paths: List[str]) -> Iterable[Path]:
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.suffix.lower() in {".txt", ".md"} and child.is_file():
                    yield child
        elif path.is_file():
            yield path
        else:
            raise SystemExit(f"ERROR: input path not found: {path}")


def normalize_chunk(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\u200b", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    # Common low-information WeChat note lines. Keep conservative; do not remove
    # user content that merely looks unusual.
    drop_patterns = [
        r"^\s*以下为聊天记录\s*$",
        r"^\s*聊天记录\s*$",
        r"^\s*合并转发.*$",
        r"^\s*微信笔记\s*$",
        r"^\s*\[图片\]\s*$",
        r"^\s*\[视频\]\s*$",
        r"^\s*\[语音\]\s*$",
        r"^\s*\[表情\]\s*$",
        r"^\s*-{3,}\s*$",
    ]
    kept = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            kept.append("")
            continue
        if any(re.match(p, line, flags=re.I) for p in drop_patterns):
            continue
        kept.append(line)
    cleaned = "\n".join(kept)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    return cleaned


def line_key(line: str) -> str:
    compact = re.sub(r"\s+", " ", line.strip())
    return hashlib.sha1(compact.encode("utf-8", errors="ignore")).hexdigest()


def merge_chunks(chunks: List[tuple[str, str]], dedupe: bool) -> str:
    seen = set()
    out: List[str] = []
    for i, (source, text) in enumerate(chunks, 1):
        out.append(f"\n\n## Chunk {i}: {source}\n")
        for line in text.splitlines():
            if dedupe and line.strip():
                key = line_key(line)
                if key in seen:
                    continue
                seen.add(key)
            out.append(line)
    merged = "\n".join(out)
    return re.sub(r"\n{3,}", "\n\n", merged).strip() + "\n"


def render_worksheet(project: str, topic: str, merged_path: Path) -> str:
    return f"""# WeChat Distillation Worksheet

Project: {project or "[not specified]"}
Topic: {topic or "[not specified]"}
Cleaned transcript: `{merged_path}`

## How to use

Ask CompassBear:

```text
Distill this WeChat transcript into decisions, claims, evidence gaps, action
items, User PI Preference updates, and mentor-lens candidate rules.
```

## Distillation targets

| Category | Extracted content | Confidence | Action |
|---|---|---|---|
| Project decision |  | high / medium / low | keep / revisit |
| Claim candidate |  | high / medium / low | Claim Passport / remove |
| Evidence gap |  | high / medium / low | experiment / RAG / source note |
| Figure idea |  | high / medium / low | main / Extended / SI / discard |
| Writing preference |  | high / medium / low | update User PI Preference Lens |
| Mentor-lens candidate |  | high / medium / low | source note needed |
| To-do |  | high / medium / low | assign / schedule |

## Claim Passport candidates

| Claim | Evidence mentioned | Missing evidence | Risk | Demotion wording |
|---|---|---|---|---|
|  |  |  |  |  |

## User PI Preference updates

| Preference | Evidence from chat | Boundary / evidence override |
|---|---|---|
|  |  |  |

## Mentor lens candidates

| Candidate rule | Source in chat | Needs paper/source note? | Activate? |
|---|---|---|---|
|  |  | yes / no | no until sourced |

## Action list

| Action | Owner | Due / next step | Dependency |
|---|---|---|---|
|  |  |  |  |
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge WeChat note chunks for CompassBear distillation.")
    parser.add_argument("--input", action="append", default=[], help="Text/Markdown file or directory. Can be repeated.")
    parser.add_argument("--stdin", action="store_true", help="Read one chunk from stdin.")
    parser.add_argument("--project", default="")
    parser.add_argument("--topic", default="")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--no-dedupe", action="store_true", help="Keep duplicate lines.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.input and not args.stdin:
        raise SystemExit("ERROR: provide --input <file-or-dir> or --stdin")

    chunks: List[tuple[str, str]] = []
    infos: List[ChunkInfo] = []
    for path in iter_input_files(args.input):
        raw = read_text_file(path)
        cleaned = normalize_chunk(raw)
        chunks.append((str(path), cleaned))
        infos.append(
            ChunkInfo(
                source=str(path),
                original_chars=len(raw),
                cleaned_chars=len(cleaned),
                line_count=len(cleaned.splitlines()),
            )
        )
    if args.stdin:
        raw = sys.stdin.read()
        cleaned = normalize_chunk(raw)
        chunks.append(("stdin", cleaned))
        infos.append(
            ChunkInfo(
                source="stdin",
                original_chars=len(raw),
                cleaned_chars=len(cleaned),
                line_count=len(cleaned.splitlines()),
            )
        )

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    merged = merge_chunks(chunks, dedupe=not args.no_dedupe)
    merged_path = out_dir / "wechat_cleaned.md"
    worksheet_path = out_dir / "wechat_distill_worksheet.md"
    manifest_path = out_dir / "wechat_chunks.json"
    merged_path.write_text(merged, encoding="utf-8")
    worksheet_path.write_text(render_worksheet(args.project, args.topic, merged_path), encoding="utf-8")
    manifest_path.write_text(json.dumps([asdict(i) for i in infos], ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: merged {len(chunks)} chunk(s) into {merged_path}")
    print(f"OK: wrote worksheet {worksheet_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
