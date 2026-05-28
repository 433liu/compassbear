#!/usr/bin/env python3
"""Read local Zotero metadata and attachment paths without modifying Zotero.

This helper opens the local Zotero SQLite database in read-only mode, searches
titles/authors/DOIs, resolves stored PDF attachment paths under Zotero storage,
and writes result reports into the CompassBear project outputs directory.

It never writes to zotero.sqlite and never moves attachments. Optional PDF copy
copies files into the project outputs directory, leaving Zotero storage intact.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sqlite3
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List, Optional


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = ROOT / "outputs" / "zotero-local"


@dataclass
class Attachment:
    key: str
    title: str
    path_raw: str
    resolved_path: str
    exists: bool
    content_type: str = ""


@dataclass
class ZoteroItem:
    item_id: int
    key: str
    item_type: str
    title: str
    authors: str
    year: str
    venue: str
    doi: str
    url: str
    abstract: str
    attachments: List[Attachment]


def load_dotenv() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def default_zotero_dir() -> Path:
    configured = os.getenv("ZOTERO_DATA_DIR", "").strip()
    if configured:
        return Path(configured)
    return Path.home() / "Zotero"


def connect_readonly(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        raise SystemExit(f"ERROR: Zotero database not found: {db_path}")
    uri = f"file:{db_path.as_posix()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def table_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return {str(r["name"]) for r in rows}


def get_field_value(conn: sqlite3.Connection, item_id: int, field_name: str) -> str:
    row = conn.execute(
        """
        SELECT v.value
        FROM itemData d
        JOIN fields f ON f.fieldID = d.fieldID
        JOIN itemDataValues v ON v.valueID = d.valueID
        WHERE d.itemID = ? AND f.fieldName = ?
        LIMIT 1
        """,
        (item_id, field_name),
    ).fetchone()
    return str(row["value"]) if row and row["value"] is not None else ""


def get_authors(conn: sqlite3.Connection, item_id: int) -> str:
    creators_cols = table_columns(conn, "creators")
    if "creatorDataID" in creators_cols:
        rows = conn.execute(
            """
            SELECT cd.firstName, cd.lastName
            FROM itemCreators ic
            JOIN creators c ON c.creatorID = ic.creatorID
            JOIN creatorData cd ON cd.creatorDataID = c.creatorDataID
            WHERE ic.itemID = ?
            ORDER BY ic.orderIndex
            """,
            (item_id,),
        ).fetchall()
    else:
        rows = conn.execute(
            """
            SELECT c.firstName, c.lastName
            FROM itemCreators ic
            JOIN creators c ON c.creatorID = ic.creatorID
            WHERE ic.itemID = ?
            ORDER BY ic.orderIndex
            """,
            (item_id,),
        ).fetchall()
    names = []
    for row in rows:
        first = str(row["firstName"] or "").strip()
        last = str(row["lastName"] or "").strip()
        name = " ".join(x for x in [first, last] if x)
        if name:
            names.append(name)
    if len(names) > 8:
        return ", ".join(names[:8]) + " et al."
    return ", ".join(names)


def resolve_attachment_path(storage_dir: Path, attachment_key: str, raw_path: str) -> Path:
    raw_path = raw_path or ""
    if raw_path.startswith("storage:"):
        filename = raw_path.split(":", 1)[1]
        return storage_dir / attachment_key / filename
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return storage_dir / attachment_key / raw_path


def get_attachments(conn: sqlite3.Connection, storage_dir: Path, parent_item_id: int) -> List[Attachment]:
    rows = conn.execute(
        """
        SELECT ai.key, ia.path, ia.contentType, ia.title
        FROM itemAttachments ia
        JOIN items ai ON ai.itemID = ia.itemID
        WHERE ia.parentItemID = ?
        ORDER BY ai.dateAdded
        """,
        (parent_item_id,),
    ).fetchall()
    out: List[Attachment] = []
    for row in rows:
        raw = str(row["path"] or "")
        key = str(row["key"] or "")
        resolved = resolve_attachment_path(storage_dir, key, raw)
        content_type = str(row["contentType"] or "")
        if not raw.lower().endswith(".pdf") and content_type != "application/pdf":
            continue
        out.append(
            Attachment(
                key=key,
                title=str(row["title"] or ""),
                path_raw=raw,
                resolved_path=str(resolved),
                exists=resolved.exists(),
                content_type=content_type,
            )
        )
    return out


def all_regular_items(conn: sqlite3.Connection, storage_dir: Path) -> Iterable[ZoteroItem]:
    rows = conn.execute(
        """
        SELECT i.itemID, i.key, it.typeName AS itemType
        FROM items i
        JOIN itemTypes it ON it.itemTypeID = i.itemTypeID
        WHERE it.typeName NOT IN ('attachment', 'note')
        ORDER BY i.dateModified DESC
        """
    ).fetchall()
    for row in rows:
        item_id = int(row["itemID"])
        date_value = get_field_value(conn, item_id, "date")
        year = date_value[:4] if date_value else ""
        yield ZoteroItem(
            item_id=item_id,
            key=str(row["key"] or ""),
            item_type=str(row["itemType"] or ""),
            title=get_field_value(conn, item_id, "title"),
            authors=get_authors(conn, item_id),
            year=year,
            venue=get_field_value(conn, item_id, "publicationTitle") or get_field_value(conn, item_id, "conferenceName"),
            doi=get_field_value(conn, item_id, "DOI"),
            url=get_field_value(conn, item_id, "url"),
            abstract=get_field_value(conn, item_id, "abstractNote"),
            attachments=get_attachments(conn, storage_dir, item_id),
        )


def item_matches(item: ZoteroItem, query: str) -> bool:
    q = query.lower().strip()
    haystack = " ".join([item.title, item.authors, item.doi, item.venue, item.year]).lower()
    return all(part in haystack for part in q.split())


def search_items(conn: sqlite3.Connection, storage_dir: Path, query: str, limit: int) -> List[ZoteroItem]:
    results: List[ZoteroItem] = []
    for item in all_regular_items(conn, storage_dir):
        if item_matches(item, query):
            results.append(item)
            if len(results) >= limit:
                break
    return results


def md_escape(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def render_markdown(items: List[ZoteroItem], query: str, db_path: Path, storage_dir: Path) -> str:
    lines = [
        "# CompassBear Local Zotero Search",
        "",
        f"- Query: `{query}`",
        f"- Database: `{db_path}`",
        f"- Storage: `{storage_dir}`",
        "- Mode: read-only; Zotero database and attachments were not modified.",
        "",
        "## Items",
        "",
        "| # | Key | Year | Title | Authors | Venue | DOI | PDFs |",
        "|---:|---|---|---|---|---|---|---|",
    ]
    for i, item in enumerate(items, 1):
        pdfs = "<br>".join(
            f"{'OK' if att.exists else 'MISSING'}: `{att.resolved_path}`" for att in item.attachments
        ) or ""
        lines.append(
            f"| {i} | {md_escape(item.key)} | {md_escape(item.year)} | {md_escape(item.title)} | "
            f"{md_escape(item.authors)} | {md_escape(item.venue)} | {md_escape(item.doi)} | {pdfs} |"
        )
    lines.extend(
        [
            "",
            "## Source-note handoff",
            "",
            "For any item you want to use as evidence, read the PDF or relevant excerpt, then assign:",
            "",
            "| Item key | Stance | Scope match | Council action | Candidate lens rule |",
            "|---|---|---|---|---|",
            "|  | supports / qualifies / refutes / insufficient | direct / adjacent / weak / mismatched | promote / keep / demote / remove / search-more |  |",
        ]
    )
    return "\n".join(lines) + "\n"


def copy_pdfs(items: List[ZoteroItem], out_dir: Path) -> int:
    pdf_dir = out_dir / "pdfs"
    pdf_dir.mkdir(parents=True, exist_ok=True)
    copied = 0
    for item in items:
        safe_key = item.key or f"item-{item.item_id}"
        for att in item.attachments:
            src = Path(att.resolved_path)
            if not src.exists():
                continue
            dst = pdf_dir / f"{safe_key}-{src.name}"
            shutil.copy2(src, dst)
            copied += 1
    return copied


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read local Zotero metadata and PDF paths in read-only mode.")
    parser.add_argument("--query", required=True, help="Search title, author, DOI, venue and year.")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--zotero-dir", default="", help="Zotero data directory. Defaults to ZOTERO_DATA_DIR or ~/Zotero.")
    parser.add_argument("--db", default="", help="Path to zotero.sqlite. Defaults to <zotero-dir>/zotero.sqlite.")
    parser.add_argument("--storage", default="", help="Path to Zotero storage. Defaults to <zotero-dir>/storage.")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--copy-pdfs", action="store_true", help="Copy matched PDFs into outputs/zotero-local/pdfs without changing Zotero.")
    return parser.parse_args()


def main() -> int:
    load_dotenv()
    args = parse_args()
    zotero_dir = Path(args.zotero_dir) if args.zotero_dir else default_zotero_dir()
    db_path = Path(args.db) if args.db else zotero_dir / "zotero.sqlite"
    storage_dir = Path(args.storage) if args.storage else zotero_dir / "storage"
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    conn = connect_readonly(db_path)
    try:
        items = search_items(conn, storage_dir, args.query, args.limit)
    finally:
        conn.close()

    out_json = out_dir / "zotero_search.json"
    out_md = out_dir / "zotero_search.md"
    out_json.write_text(json.dumps([asdict(i) for i in items], ensure_ascii=False, indent=2), encoding="utf-8")
    out_md.write_text(render_markdown(items, args.query, db_path, storage_dir), encoding="utf-8")

    copied = copy_pdfs(items, out_dir) if args.copy_pdfs else 0
    print(f"OK: found {len(items)} item(s). Wrote {out_md} and {out_json}.")
    if args.copy_pdfs:
        print(f"OK: copied {copied} PDF(s) into {out_dir / 'pdfs'} without modifying Zotero.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
