#!/usr/bin/env python3
"""Zotero ⇄ CompassBear source-packs bridge.

Two modes:
  push   read a literature_rag.py evidence_matrix.json and create matching
         items in a Zotero collection so the human can read them in their
         normal workflow.
  pull   read items from a Zotero collection back into source-pack stubs.
         Tags drive the structured fields (stance / scope / action / claim
         link); a single child note provides the free-text summary. Only
         items tagged `cb/ready` are pulled.

Tag convention (set in Zotero UI; hierarchical tags via `/`):
  cb/stance/(supports|qualifies|refutes|insufficient)
  cb/scope/(direct|adjacent|weak|mismatched)
  cb/action/(promote|keep|demote|remove|search-more)
  cb/claim/<claim-id>         e.g. cb/claim/E2
  cb/from-rag                 auto-added by push; do not remove
  cb/ready                    user-applied; signals "ready to promote"

The Zotero Web API is documented at https://www.zotero.org/support/dev/web_api/v3/start
An API key is free at https://www.zotero.org/settings/keys
Your numeric user ID is shown on the same page.

Required environment variables (in .env or shell):
  ZOTERO_API_KEY
  ZOTERO_USER_ID                 numeric, e.g. 1234567
  ZOTERO_LIBRARY_TYPE            users | groups   (default: users)
  ZOTERO_COLLECTION_KEY          optional, narrow push/pull to a collection
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "CompassBear-Zotero-Sync/0.5.14 (mailto:local-user@example.com)"
ZOTERO_API = "https://api.zotero.org"

STANCE_VALUES = {"supports", "qualifies", "refutes", "insufficient"}
SCOPE_VALUES = {"direct", "adjacent", "weak", "mismatched"}
ACTION_VALUES = {"promote", "keep", "demote", "remove", "search-more"}


@dataclass
class ZoteroContext:
    api_key: str
    user_id: str
    library_type: str
    collection_key: Optional[str]

    @classmethod
    def from_env(cls) -> "ZoteroContext":
        load_dotenv()
        api_key = os.getenv("ZOTERO_API_KEY", "").strip()
        user_id = os.getenv("ZOTERO_USER_ID", "").strip()
        library_type = os.getenv("ZOTERO_LIBRARY_TYPE", "users").strip() or "users"
        coll = os.getenv("ZOTERO_COLLECTION_KEY", "").strip() or None
        missing = [k for k, v in [("ZOTERO_API_KEY", api_key), ("ZOTERO_USER_ID", user_id)] if not v]
        if missing:
            raise SystemExit(
                "ERROR: missing required env vars: " + ", ".join(missing) +
                ". Set them in .env at the skill root."
            )
        if library_type not in ("users", "groups"):
            raise SystemExit("ERROR: ZOTERO_LIBRARY_TYPE must be 'users' or 'groups'.")
        return cls(api_key=api_key, user_id=user_id, library_type=library_type, collection_key=coll)

    def base_url(self) -> str:
        return f"{ZOTERO_API}/{self.library_type}/{self.user_id}"

    def headers(self, write: bool = False) -> Dict[str, str]:
        h = {
            "Zotero-API-Key": self.api_key,
            "Zotero-API-Version": "3",
            "User-Agent": USER_AGENT,
        }
        if write:
            h["Content-Type"] = "application/json"
        return h


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


def http_request(method: str, url: str, *, headers: Dict[str, str],
                 payload: Optional[Any] = None, timeout: int = 30,
                 max_retries: int = 3) -> Tuple[int, str]:
    body = None
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
    last_exc: Optional[Exception] = None
    for attempt in range(max_retries):
        req = Request(url, data=body, headers=headers, method=method)
        try:
            with urlopen(req, timeout=timeout) as resp:
                return resp.status, resp.read().decode("utf-8", errors="replace")
        except HTTPError as exc:
            if exc.code in (429, 500, 502, 503, 504) and attempt < max_retries - 1:
                time.sleep(min(8, 1.0 * (2 ** attempt)))
                last_exc = exc
                continue
            msg = exc.read().decode("utf-8", errors="replace")[:500]
            return exc.code, msg
        except URLError as exc:
            last_exc = exc
            if attempt < max_retries - 1:
                time.sleep(1.0 * (2 ** attempt))
                continue
            raise RuntimeError(f"Network error for {url}: {exc}") from exc
    raise RuntimeError(f"Failed after {max_retries} retries: {last_exc}")


def slugify(text: str, max_len: int = 70) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return slug[:max_len].strip("-") or "source"


def parse_cb_tags(tags: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Extract structured fields from cb/ hierarchical tags. Returns dict with keys:
    stance, scope, action, claims (list), ready (bool), from_rag (bool).
    """
    out: Dict[str, Any] = {
        "stance": "", "scope": "", "action": "",
        "claims": [], "ready": False, "from_rag": False,
    }
    for t in tags or []:
        tag = (t.get("tag") if isinstance(t, dict) else str(t)).strip()
        if not tag.startswith("cb/"):
            continue
        rest = tag[3:]
        if rest == "ready":
            out["ready"] = True
        elif rest == "from-rag":
            out["from_rag"] = True
        elif rest.startswith("stance/"):
            v = rest.split("/", 1)[1].strip()
            if v in STANCE_VALUES:
                out["stance"] = v
        elif rest.startswith("scope/"):
            v = rest.split("/", 1)[1].strip()
            if v in SCOPE_VALUES:
                out["scope"] = v
        elif rest.startswith("action/"):
            v = rest.split("/", 1)[1].strip()
            if v in ACTION_VALUES:
                out["action"] = v
        elif rest.startswith("claim/"):
            v = rest.split("/", 1)[1].strip()
            if v:
                out["claims"].append(v)
    return out


# ---------------------------------------------------------------------------
# Push: evidence_matrix.json → Zotero items
# ---------------------------------------------------------------------------

def get_existing_dois(ctx: ZoteroContext) -> Dict[str, str]:
    """Return {normalized_doi: item_key} for items already in the library/collection."""
    existing: Dict[str, str] = {}
    start = 0
    limit = 100
    while True:
        params = {"format": "json", "limit": limit, "start": start, "include": "data"}
        if ctx.collection_key:
            url = f"{ctx.base_url()}/collections/{ctx.collection_key}/items?{urlencode(params)}"
        else:
            url = f"{ctx.base_url()}/items?{urlencode(params)}"
        status, body = http_request("GET", url, headers=ctx.headers())
        if status >= 400:
            raise RuntimeError(f"Zotero list failed ({status}): {body[:200]}")
        items = json.loads(body)
        if not items:
            break
        for item in items:
            data = item.get("data") or {}
            doi = (data.get("DOI") or "").strip().lower()
            if doi:
                existing[doi] = item.get("key", "")
        if len(items) < limit:
            break
        start += limit
    return existing


def record_to_zotero_item(rec: Dict[str, Any]) -> Dict[str, Any]:
    """Map a literature_rag PaperRecord (dict form) to a Zotero journalArticle template."""
    authors_field = (rec.get("authors") or "").strip()
    creators: List[Dict[str, str]] = []
    if authors_field:
        for name in [a.strip() for a in authors_field.split(",") if a.strip()]:
            if name.lower().endswith("et al."):
                continue
            parts = name.rsplit(" ", 1)
            if len(parts) == 2:
                first, last = parts
            else:
                first, last = "", parts[0]
            creators.append({"creatorType": "author", "firstName": first, "lastName": last})
    item: Dict[str, Any] = {
        "itemType": "journalArticle",
        "title": rec.get("title", ""),
        "creators": creators,
        "abstractNote": rec.get("abstract", ""),
        "publicationTitle": rec.get("venue", ""),
        "date": rec.get("year", ""),
        "DOI": rec.get("doi", ""),
        "url": rec.get("url", ""),
        "tags": [
            {"tag": "cb/from-rag"},
            {"tag": f"cb/intent/{rec.get('retrieval_intent') or 'neutral'}"},
            {"tag": f"cb/provider/{rec.get('provider') or 'unknown'}"},
        ],
    }
    if rec.get("oa_pdf"):
        item["extra"] = f"OA PDF: {rec['oa_pdf']}"
    return item


def push_records(ctx: ZoteroContext, records: List[Dict[str, Any]], dry_run: bool) -> Tuple[int, int]:
    if dry_run:
        existing: Dict[str, str] = {}
    else:
        existing = get_existing_dois(ctx)
    to_create: List[Dict[str, Any]] = []
    skipped = 0
    for rec in records:
        doi = (rec.get("doi") or "").strip().lower()
        if doi and doi in existing:
            skipped += 1
            continue
        item = record_to_zotero_item(rec)
        if ctx.collection_key:
            item["collections"] = [ctx.collection_key]
        to_create.append(item)
    if dry_run:
        print(f"DRY RUN: would create {len(to_create)} item(s), skip {skipped} duplicate(s).")
        if to_create:
            print("First payload preview:")
            print(json.dumps(to_create[0], indent=2, ensure_ascii=False))
        return len(to_create), skipped
    # Zotero accepts up to 50 items per POST.
    created = 0
    for batch_start in range(0, len(to_create), 50):
        batch = to_create[batch_start:batch_start + 50]
        status, body = http_request(
            "POST", f"{ctx.base_url()}/items",
            headers=ctx.headers(write=True), payload=batch,
        )
        if status >= 400:
            print(f"WARN: Zotero create failed ({status}): {body[:300]}", file=sys.stderr)
            continue
        result = json.loads(body)
        # `successful` keys are stringified indices; count successes.
        created += len(result.get("successful") or {})
        failed = result.get("failed") or {}
        if failed:
            print(f"WARN: {len(failed)} item(s) failed: {json.dumps(failed)[:300]}", file=sys.stderr)
    print(f"Pushed: created {created}, skipped {skipped} duplicate(s).")
    return created, skipped


# ---------------------------------------------------------------------------
# Pull: Zotero items → source-pack stubs (only items tagged cb/ready)
# ---------------------------------------------------------------------------

def list_collection_items(ctx: ZoteroContext) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    start = 0
    limit = 100
    while True:
        params = {"format": "json", "limit": limit, "start": start}
        if ctx.collection_key:
            url = f"{ctx.base_url()}/collections/{ctx.collection_key}/items?{urlencode(params)}"
        else:
            url = f"{ctx.base_url()}/items?{urlencode(params)}"
        status, body = http_request("GET", url, headers=ctx.headers())
        if status >= 400:
            raise RuntimeError(f"Zotero list failed ({status}): {body[:200]}")
        batch = json.loads(body)
        if not batch:
            break
        items.extend(batch)
        if len(batch) < limit:
            break
        start += limit
    return items


def get_child_notes(ctx: ZoteroContext, item_key: str) -> List[str]:
    url = f"{ctx.base_url()}/items/{item_key}/children?format=json"
    status, body = http_request("GET", url, headers=ctx.headers())
    if status >= 400:
        return []
    notes: List[str] = []
    for child in json.loads(body):
        data = child.get("data") or {}
        if data.get("itemType") == "note":
            note_html = data.get("note") or ""
            # Strip HTML for readability in the stub.
            note_text = re.sub(r"<[^>]+>", " ", note_html)
            note_text = re.sub(r"\s+", " ", note_text).strip()
            if note_text:
                notes.append(note_text)
    return notes


def stub_for_item(item: Dict[str, Any], notes: List[str], parsed_tags: Dict[str, Any]) -> str:
    data = item.get("data") or {}
    title = (data.get("title") or "").strip()
    creators = data.get("creators") or []
    authors = []
    for c in creators:
        first = (c.get("firstName") or "").strip()
        last = (c.get("lastName") or "").strip()
        full = (first + " " + last).strip()
        if full:
            authors.append(full)
    if len(authors) > 6:
        authors_str = ", ".join(authors[:6]) + " et al."
    else:
        authors_str = ", ".join(authors)
    doi = (data.get("DOI") or "").strip().lower()
    year = (data.get("date") or "")[:4] if data.get("date") else ""
    venue = (data.get("publicationTitle") or "").strip()
    url = (data.get("url") or "").strip()
    abstract = (data.get("abstractNote") or "").strip()
    extra = (data.get("extra") or "").strip()
    oa_pdf = ""
    m = re.search(r"OA PDF:\s*(\S+)", extra)
    if m:
        oa_pdf = m.group(1)

    claims_str = ", ".join(parsed_tags.get("claims") or []) or "[not tagged]"

    body_notes = "\n\n".join(f"- {n}" for n in notes) if notes else "[no child note in Zotero — add one and re-pull]"

    return f"""---
source_id: TBD
zotero_key: {item.get('key', '')}
title: {title!r}
authors: {authors_str!r}
year: {year!r}
venue: {venue!r}
doi: {doi!r}
url: {url!r}
oa_pdf: {oa_pdf!r}
stance: {parsed_tags.get('stance') or 'TBD'}
scope: {parsed_tags.get('scope') or 'TBD'}
action: {parsed_tags.get('action') or 'TBD'}
claims: {claims_str}
---

# Source note — {title}

## Claims this note serves

{claims_str}

## Bibliographic record

- Authors: {authors_str or '[missing]'}
- Year: {year or '[missing]'}
- Venue: {venue or '[missing]'}
- DOI: {doi or '[missing]'}
- URL: {url or '[missing]'}
- OA PDF: {oa_pdf or '[check institutional access]'}

## Evidence stance tags

- Stance (cb/stance/...): {parsed_tags.get('stance') or 'TBD — add tag in Zotero'}
- Scope match (cb/scope/...): {parsed_tags.get('scope') or 'TBD — add tag in Zotero'}
- Council action (cb/action/...): {parsed_tags.get('action') or 'TBD — add tag in Zotero'}

## Notes from Zotero

{body_notes}

## Abstract

{abstract or '[no abstract in Zotero metadata]'}
"""


def pull_to_stubs(ctx: ZoteroContext, out_dir: Path, only_ready: bool, dry_run: bool) -> int:
    items = list_collection_items(ctx)
    out_dir.mkdir(parents=True, exist_ok=True)
    written = 0
    skipped = 0
    for item in items:
        data = item.get("data") or {}
        if data.get("itemType") in ("attachment", "note"):
            continue
        parsed = parse_cb_tags(data.get("tags") or [])
        if only_ready and not parsed.get("ready"):
            skipped += 1
            continue
        notes = [] if dry_run else get_child_notes(ctx, item.get("key", ""))
        stub = stub_for_item(item, notes, parsed)
        slug = slugify(data.get("title") or "source")
        path = out_dir / f"zotero-{item.get('key', 'noid')}-{slug}.md"
        if dry_run:
            print(f"DRY RUN: would write {path}")
        else:
            path.write_text(stub, encoding="utf-8")
        written += 1
    print(f"Pull: {'would write' if dry_run else 'wrote'} {written} stub(s); skipped {skipped} (no cb/ready tag).")
    return written


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Zotero ⇄ CompassBear source-packs bridge.")
    sub = parser.add_subparsers(dest="mode", required=True)

    p_push = sub.add_parser("push", help="Push literature_rag.py evidence matrix to a Zotero collection.")
    p_push.add_argument("--from-json", required=True, help="Path to evidence_matrix.json from literature_rag.py.")
    p_push.add_argument("--dry-run", action="store_true", help="Print what would be created, no API write.")

    p_pull = sub.add_parser("pull", help="Pull Zotero items back into source-pack stubs.")
    p_pull.add_argument("--out-dir", default="source-packs/from-zotero",
                        help="Target directory for stubs.")
    p_pull.add_argument("--all", action="store_true",
                        help="Pull all items, not just those tagged cb/ready (advanced).")
    p_pull.add_argument("--dry-run", action="store_true", help="List what would be written, no file output.")

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ctx = ZoteroContext.from_env()
    if args.mode == "push":
        json_path = Path(args.from_json)
        if not json_path.exists():
            print(f"ERROR: {json_path} not found. Run literature_rag.py first.", file=sys.stderr)
            return 2
        records = json.loads(json_path.read_text(encoding="utf-8"))
        if not isinstance(records, list):
            print("ERROR: input JSON must be a list of records (as produced by literature_rag.py).", file=sys.stderr)
            return 2
        push_records(ctx, records, dry_run=args.dry_run)
        return 0
    if args.mode == "pull":
        pull_to_stubs(ctx, Path(args.out_dir), only_ready=not args.all, dry_run=args.dry_run)
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
