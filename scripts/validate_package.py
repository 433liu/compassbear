#!/usr/bin/env python3
"""Validate the public CompassBear skill package before release."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "README.md",
    "README.zh-CN.md",
    "INSTALL.md",
    "LICENSE",
    "SKILL.md",
    "commands",
    "agents",
    "skills",
    "scripts",
    "examples",
    "references",
    "evals",
    "evals/cases.jsonl",
]

SENSITIVE_PATTERNS = [
    re.compile(r"C:\\Users\\", re.IGNORECASE),
    re.compile(r"\b[A-Z]:\\(?:CodexProjects|Users|OneDrive|Desktop|Downloads|Documents)\\", re.IGNORECASE),
    re.compile(r"(^|[\\/])\.env($|[\\/])", re.IGNORECASE),
    re.compile(r"\bapi[_ -]?key\b", re.IGNORECASE),
    re.compile(r"\bsecret[_ -]?key\b", re.IGNORECASE),
    re.compile(r"\baccess[_ -]?token\b", re.IGNORECASE),
    re.compile(r"\bprivate-full\b", re.IGNORECASE),
    re.compile(r"(^|[\\/])private([\\/]|$)", re.IGNORECASE),
]

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".jsonl",
    ".yml",
    ".yaml",
    ".html",
    ".css",
    ".svg",
    ".py",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_required_paths() -> None:
    for rel in REQUIRED_PATHS:
        path = ROOT / rel
        if not path.exists():
            fail(f"missing required path: {rel}")


def check_skill_name() -> None:
    skill_text = read_text(ROOT / "SKILL.md")
    match = re.search(r"(?m)^name:\s*([A-Za-z0-9_-]+)\s*$", skill_text)
    if not match:
        fail("SKILL.md does not declare a name")
    if match.group(1) != "compass-bear":
        fail(f"SKILL.md name is {match.group(1)!r}, expected 'compass-bear'")


def check_markdown_links() -> None:
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    image_src_pattern = re.compile(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)
    for rel in ["README.md", "README.zh-CN.md", "INSTALL.md"]:
        path = ROOT / rel
        text = read_text(path)
        targets = [m.group(1) for m in link_pattern.finditer(text)]
        targets.extend(m.group(1) for m in image_src_pattern.finditer(text))
        for raw_target in targets:
            target = raw_target.strip()
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = target.split("#", 1)[0]
            if target.startswith("../"):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                fail(f"{rel} links outside package: {raw_target}")
            if not resolved.exists():
                fail(f"{rel} has missing link target: {raw_target}")


def check_command_files() -> None:
    command_files = sorted((ROOT / "commands").glob("*.md"))
    if not command_files:
        fail("commands/*.md is empty")


def check_skill_modules() -> None:
    skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if not skill_files:
        fail("skills/*/SKILL.md is empty")


def check_referenced_references() -> None:
    for path in [ROOT / "SKILL.md", *sorted((ROOT / "skills").glob("*/SKILL.md"))]:
        text = read_text(path)
        for match in re.finditer(r"(?:\.\./\.\./)?references/[A-Za-z0-9_.\-/]+", text):
            rel = match.group(0)
            resolved = (path.parent / rel).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                fail(f"{path.relative_to(ROOT)} references outside package: {rel}")
            if not resolved.exists():
                fail(f"{path.relative_to(ROOT)} references missing file: {rel}")


def check_evals() -> None:
    cases_path = ROOT / "evals" / "cases.jsonl"
    count = 0
    for line_no, line in enumerate(read_text(cases_path).splitlines(), 1):
        if not line.strip():
            continue
        try:
            json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"evals/cases.jsonl line {line_no} is invalid JSON: {exc}")
        count += 1
    if count == 0:
        fail("evals/cases.jsonl has no cases")


def iter_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        yield path


def check_sensitive_terms() -> None:
    for path in iter_text_files():
        rel = path.relative_to(ROOT)
        text = read_text(path)
        for pattern in SENSITIVE_PATTERNS:
            if pattern.search(text):
                fail(f"sensitive-looking term in {rel}: {pattern.pattern}")


def main() -> None:
    check_required_paths()
    check_skill_name()
    check_markdown_links()
    check_command_files()
    check_skill_modules()
    check_referenced_references()
    check_evals()
    check_sensitive_terms()
    print("OK: CompassBear public package passed validation.")


if __name__ == "__main__":
    main()
