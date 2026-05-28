#!/usr/bin/env python3
"""Guarded UI macro runner for repetitive WeChat export actions.

This script uses Windows user32 mouse/keyboard events and PowerShell clipboard
access. It does not read or modify the WeChat database. It only replays an
explicit user-provided macro and captures changed clipboard text into
outputs/wechat-capture/.

Use when WeChat's 100-message forwarding limit makes manual export too slow.
The first run should use a tiny loop count and visible pauses.
"""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CAPTURE_DIR = ROOT / "outputs" / "wechat-capture"
DEFAULT_CONFIG = ROOT / "private" / "wechat-ui-macro.example.json"

user32 = ctypes.windll.user32

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_WHEEL = 0x0800
KEYEVENTF_KEYUP = 0x0002

VK = {
    "ctrl": 0x11,
    "shift": 0x10,
    "alt": 0x12,
    "enter": 0x0D,
    "esc": 0x1B,
    "tab": 0x09,
    "space": 0x20,
    "a": 0x41,
    "c": 0x43,
    "v": 0x56,
    "x": 0x58,
    "f": 0x46,
    "up": 0x26,
    "down": 0x28,
    "left": 0x25,
    "right": 0x27,
    "home": 0x24,
    "end": 0x23,
    "pagedown": 0x22,
    "pageup": 0x21,
}


@dataclass
class CaptureRecord:
    index: int
    timestamp: str
    chars: int
    sha1: str
    path: str
    loop: int


def sleep(seconds: float) -> None:
    time.sleep(max(0.0, seconds))


def cursor_pos() -> Tuple[int, int]:
    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return int(pt.x), int(pt.y)


def move_to(x: int, y: int) -> None:
    user32.SetCursorPos(int(x), int(y))


def mouse_event(flag: int, data: int = 0) -> None:
    user32.mouse_event(flag, 0, 0, data, 0)


def click(x: int, y: int, button: str = "left") -> None:
    move_to(x, y)
    sleep(0.05)
    if button == "right":
        mouse_event(MOUSEEVENTF_RIGHTDOWN)
        sleep(0.05)
        mouse_event(MOUSEEVENTF_RIGHTUP)
    else:
        mouse_event(MOUSEEVENTF_LEFTDOWN)
        sleep(0.05)
        mouse_event(MOUSEEVENTF_LEFTUP)


def drag(start: List[int], end: List[int], duration: float = 0.6) -> None:
    sx, sy = int(start[0]), int(start[1])
    ex, ey = int(end[0]), int(end[1])
    move_to(sx, sy)
    sleep(0.05)
    mouse_event(MOUSEEVENTF_LEFTDOWN)
    steps = max(3, int(duration / 0.03))
    for i in range(1, steps + 1):
        x = sx + (ex - sx) * i / steps
        y = sy + (ey - sy) * i / steps
        move_to(int(x), int(y))
        sleep(duration / steps)
    mouse_event(MOUSEEVENTF_LEFTUP)


def scroll(amount: int) -> None:
    mouse_event(MOUSEEVENTF_WHEEL, int(amount))


def key_down(vk: int) -> None:
    user32.keybd_event(vk, 0, 0, 0)


def key_up(vk: int) -> None:
    user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)


def press(key: str) -> None:
    vk = VK.get(key.lower())
    if vk is None:
        raise ValueError(f"unsupported key: {key}")
    key_down(vk)
    sleep(0.04)
    key_up(vk)


def hotkey(keys: List[str]) -> None:
    vks = []
    for key in keys:
        vk = VK.get(key.lower())
        if vk is None:
            raise ValueError(f"unsupported key: {key}")
        vks.append(vk)
    for vk in vks:
        key_down(vk)
        sleep(0.03)
    for vk in reversed(vks):
        key_up(vk)
        sleep(0.03)


def get_clipboard_text() -> str:
    proc = subprocess.run(
        ["powershell", "-NoProfile", "-Command", "Get-Clipboard -Raw"],
        capture_output=True,
        timeout=10,
    )
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


def capture_clipboard(out_dir: Path, records: List[CaptureRecord], loop_index: int, min_chars: int) -> bool:
    manifest = out_dir / "manifest.json"
    existing = {r.sha1 for r in records}
    text = get_clipboard_text()
    if len(text) < min_chars:
        print(f"  capture skipped: clipboard has only {len(text)} char(s)")
        return False
    sha = digest(text)
    if sha in existing:
        print("  capture skipped: duplicate clipboard text")
        return False
    idx = len(records) + 1
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = out_dir / f"wechat-chunk-{idx:03d}-{ts}.md"
    path.write_text(text + "\n", encoding="utf-8")
    records.append(CaptureRecord(idx, ts, len(text), sha, str(path), loop_index))
    save_manifest(manifest, records)
    print(f"  captured chunk {idx}: {len(text)} chars")
    return True


def example_config() -> Dict[str, Any]:
    return {
        "description": "Example only. Calibrate coordinates on your screen before running.",
        "start_delay_seconds": 5,
        "min_clipboard_chars": 80,
        "loop_pause_seconds": 1.0,
        "actions": [
            {"action": "prompt", "message": "Open target WeChat chat and position the first export range. Press Enter to start this loop."},
            {"action": "drag", "start": [900, 760], "end": [900, 220], "duration": 0.8},
            {"action": "hotkey", "keys": ["ctrl", "c"]},
            {"action": "wait", "seconds": 0.8},
            {"action": "capture_clipboard"},
            {"action": "scroll", "amount": -5},
            {"action": "wait", "seconds": 0.5},
        ],
    }


def write_example(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(example_config(), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: wrote example macro config to {path}")
    print("Edit coordinates and actions before running.")


def execute_action(action: Dict[str, Any], out_dir: Path, records: List[CaptureRecord], loop_index: int, min_chars: int) -> None:
    kind = action.get("action")
    if kind == "wait":
        sleep(float(action.get("seconds", 1)))
    elif kind == "prompt":
        input(str(action.get("message", "Press Enter to continue...")) + " ")
    elif kind == "click":
        x, y = action["pos"]
        click(int(x), int(y), "left")
    elif kind == "right_click":
        x, y = action["pos"]
        click(int(x), int(y), "right")
    elif kind == "double_click":
        x, y = action["pos"]
        click(int(x), int(y), "left")
        sleep(0.08)
        click(int(x), int(y), "left")
    elif kind == "drag":
        drag(action["start"], action["end"], float(action.get("duration", 0.6)))
    elif kind == "scroll":
        scroll(int(action.get("amount", -5)) * 120)
    elif kind == "press":
        press(str(action["key"]))
    elif kind == "hotkey":
        hotkey([str(k) for k in action["keys"]])
    elif kind == "capture_clipboard":
        capture_clipboard(out_dir, records, loop_index, min_chars)
    else:
        raise ValueError(f"unknown action: {kind}")


def run_macro(config_path: Path, loops: int, out_dir: Path, min_chars_override: int, confirmed: bool) -> int:
    if not confirmed:
        raise SystemExit("ERROR: pass --i-understand-ui-automation-risk to run UI macro.")
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    out_dir.mkdir(parents=True, exist_ok=True)
    records = load_manifest(out_dir / "manifest.json")
    min_chars = int(min_chars_override or cfg.get("min_clipboard_chars", 80))
    start_delay = float(cfg.get("start_delay_seconds", 5))
    print("UI macro will start soon. Focus WeChat now.")
    print("Safety: keep terminal visible; Ctrl+C stops between actions.")
    sleep(start_delay)
    for loop_index in range(1, loops + 1):
        print(f"Loop {loop_index}/{loops}")
        for action in cfg.get("actions", []):
            execute_action(action, out_dir, records, loop_index, min_chars)
        sleep(float(cfg.get("loop_pause_seconds", 1.0)))
    print(f"Done. Captured chunks are in {out_dir}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Guarded WeChat UI macro runner.")
    sub = parser.add_subparsers(dest="mode", required=True)

    p = sub.add_parser("pos", help="Print current cursor position after a delay.")
    p.add_argument("--delay", type=float, default=3.0)

    p = sub.add_parser("init", help="Write an example macro config.")
    p.add_argument("--config", default=str(DEFAULT_CONFIG))

    p = sub.add_parser("run", help="Run a configured UI macro.")
    p.add_argument("--config", default=str(DEFAULT_CONFIG))
    p.add_argument("--loops", type=int, default=1)
    p.add_argument("--out-dir", default=str(DEFAULT_CAPTURE_DIR))
    p.add_argument("--min-chars", type=int, default=0)
    p.add_argument("--i-understand-ui-automation-risk", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mode == "pos":
        sleep(args.delay)
        x, y = cursor_pos()
        print(f"{x},{y}")
        return 0
    if args.mode == "init":
        write_example(Path(args.config))
        return 0
    if args.mode == "run":
        return run_macro(
            Path(args.config),
            max(1, int(args.loops)),
            Path(args.out_dir),
            int(args.min_chars),
            bool(args.i_understand_ui_automation_risk),
        )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
