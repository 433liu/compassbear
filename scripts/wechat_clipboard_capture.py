#!/usr/bin/env python3
"""Capture WeChat note/text chunks from the Windows clipboard.

This helper does not automate WeChat clicks and does not read the WeChat
database. It watches the clipboard and saves each new text chunk as a Markdown
file under outputs/wechat-capture/ so long chats can be collected without manual
file dragging.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import List


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = ROOT / "outputs" / "wechat-capture"


@dataclass
class CaptureRecord:
    index: int
    timestamp: str
    chars: int
    sha1: str
    path: str


def get_clipboard_text() -> str:
    cmd = ["powershell", "-NoProfile", "-Command", "Get-Clipboard -Raw"]
    proc = subprocess.run(cmd, capture_output=True, timeout=10)
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or b"Get-Clipboard failed").decode("utf-8", errors="replace")
        raise RuntimeError(err.strip())
    return proc.stdout.decode("utf-8", errors="replace").replace("\r\n", "\n").strip()


def digest(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()


def load_manifest(path: Path) -> List[CaptureRecord]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return [CaptureRecord(**row) for row in data]


def save_manifest(path: Path, records: List[CaptureRecord]) -> None:
    path.write_text(json.dumps([asdict(r) for r in records], ensure_ascii=False, indent=2), encoding="utf-8")


def save_chunk(out_dir: Path, text: str, records: List[CaptureRecord]) -> CaptureRecord:
    idx = len(records) + 1
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    sha = digest(text)
    path = out_dir / f"wechat-chunk-{idx:03d}-{ts}.md"
    path.write_text(text.strip() + "\n", encoding="utf-8")
    rec = CaptureRecord(index=idx, timestamp=ts, chars=len(text), sha1=sha, path=str(path))
    records.append(rec)
    return rec


def capture_once(out_dir: Path, min_chars: int) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = out_dir / "manifest.json"
    records = load_manifest(manifest)
    existing = {r.sha1 for r in records}
    text = get_clipboard_text()
    if len(text) < min_chars:
        print(f"SKIP: clipboard has only {len(text)} char(s).")
        return 1
    sha = digest(text)
    if sha in existing:
        print("SKIP: clipboard text already captured.")
        return 0
    rec = save_chunk(out_dir, text, records)
    save_manifest(manifest, records)
    print(f"OK: captured chunk {rec.index} ({rec.chars} chars) -> {rec.path}")
    return 0


def watch(out_dir: Path, min_chars: int, interval: float) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = out_dir / "manifest.json"
    records = load_manifest(manifest)
    existing = {r.sha1 for r in records}
    print(f"Watching clipboard. Save dir: {out_dir}")
    print("Copy each WeChat note/chunk. Press Ctrl+C here to stop.")
    last_sha = ""
    try:
        while True:
            try:
                text = get_clipboard_text()
            except Exception as exc:  # noqa: BLE001
                print(f"WARN: {exc}", file=sys.stderr)
                time.sleep(interval)
                continue
            sha = digest(text) if text else ""
            if text and len(text) >= min_chars and sha != last_sha and sha not in existing:
                rec = save_chunk(out_dir, text, records)
                existing.add(sha)
                save_manifest(manifest, records)
                print(f"OK: captured chunk {rec.index} ({rec.chars} chars)")
            last_sha = sha
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped.")
        return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture WeChat chunks from clipboard.")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--once", action="store_true", help="Capture current clipboard once.")
    parser.add_argument("--watch", action="store_true", help="Watch clipboard until Ctrl+C.")
    parser.add_argument("--min-chars", type=int, default=80)
    parser.add_argument("--interval", type=float, default=1.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    out_dir = Path(args.out_dir)
    if args.once:
        return capture_once(out_dir, args.min_chars)
    if args.watch:
        return watch(out_dir, args.min_chars, args.interval)
    raise SystemExit("ERROR: pass --once or --watch")


if __name__ == "__main__":
    raise SystemExit(main())
