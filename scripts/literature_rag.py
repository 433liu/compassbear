#!/usr/bin/env python3
"""Integrated literature RAG helper for CompassBear.

This script retrieves candidate literature records for one or more claims,
separating support-oriented, adversarial and neutral queries. It is intentionally
conservative: it does not decide whether a paper truly supports a mechanism.
Instead it creates a traceable evidence matrix that the RAG Evidence
Adjudicator and active local lenses can use for support / qualify / refute /
insufficient decisions.

Providers (all free except where noted):
  - semantic_scholar  : Semantic Scholar Graph API. Optional API key for higher rate.
  - crossref          : Crossref REST API. Mailto strongly recommended for polite pool.
  - openalex          : OpenAlex API. Mailto optional; API key optional.
  - europepmc         : Europe PMC search. Free, no key. Strong biomedical / life-science coverage.
  - arxiv             : arXiv API. Free, no key. Strong ML / methods coverage.
  - serper            : Serper.dev Google wrapper. Requires SERPER_API_KEY. Optional.
  - unpaywall         : Post-processing step that upgrades any DOI to its OA PDF link if available.
                        Requires only UNPAYWALL_EMAIL. Runs automatically when email is set.

Note on institutional databases (Web of Science, Scopus, ScienceDirect, ACS,
Wiley etc.): these are IP-gated browser subscriptions by default. Only the
separate institutional API agreements (e.g. WoS Starter API, Elsevier TDM API)
can be plumbed in here. If your institution has such an API key, contribute a
provider following the same shape as `search_semantic_scholar`.

Typical use:
  python scripts/literature_rag.py \
    --claim "surface-treated material A remains stable under accelerated aging" \
    --profile materials-mechanism \
    --with-html-review \
    --max-per-provider 5
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import textwrap
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = ROOT / "outputs" / "literature-rag"
USER_AGENT = "CompassBear-Literature-RAG/0.5.14 (mailto:local-user@example.com)"

DEFAULT_PROVIDERS = "semantic_scholar,crossref,openalex,europepmc,arxiv,serper"
PROFILE_PROVIDERS = {
    "broad": DEFAULT_PROVIDERS,
    "materials-mechanism": "semantic_scholar,openalex,crossref,serper",
    "computational-methods": "arxiv,semantic_scholar,openalex,crossref",
    "bio-application": "europepmc,openalex,semantic_scholar,crossref,serper",
}
EXPORT_FORMAT_CHOICES = ("ris", "enw", "bib")


@dataclass
class QuerySpec:
    intent: str
    query: str
    segment_id: str = ""
    segment_text: str = ""

    def as_tuple(self) -> tuple[str, str]:
        return (self.intent, self.query)


@dataclass
class PaperRecord:
    provider: str
    retrieval_intent: str
    query: str
    title: str = ""
    year: str = ""
    venue: str = ""
    authors: str = ""
    doi: str = ""
    url: str = ""
    abstract: str = ""
    citation_count: Optional[int] = None
    is_open_access: Optional[bool] = None
    oa_pdf: str = ""
    raw_id: str = ""
    segment_id: str = ""
    segment_text: str = ""
    support_grade: str = "metadata-only"

    def key(self) -> str:
        doi = normalize_doi(self.doi)
        if doi:
            return f"doi:{doi}"
        return f"title:{normalize_title(self.title)}"


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


def request_json(url: str, *, method: str = "GET", headers: Optional[Dict[str, str]] = None,
                 payload: Optional[Dict[str, Any]] = None, timeout: int = 30,
                 max_retries: int = 3) -> Dict[str, Any]:
    """JSON request with simple exponential backoff for 429 / 5xx."""
    body = None
    merged_headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if headers:
        merged_headers.update(headers)
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        merged_headers["Content-Type"] = "application/json"
    last_exc: Optional[Exception] = None
    for attempt in range(max_retries):
        req = Request(url, data=body, headers=merged_headers, method=method)
        try:
            with urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8", errors="replace"))
        except HTTPError as exc:
            if exc.code in (429, 500, 502, 503, 504) and attempt < max_retries - 1:
                wait = min(8, 1.0 * (2 ** attempt))
                time.sleep(wait)
                last_exc = exc
                continue
            msg = exc.read().decode("utf-8", errors="replace")[:500]
            raise RuntimeError(f"HTTP {exc.code} for {url}: {msg}") from exc
        except URLError as exc:
            last_exc = exc
            if attempt < max_retries - 1:
                time.sleep(1.0 * (2 ** attempt))
                continue
            raise RuntimeError(f"Network error for {url}: {exc}") from exc
    raise RuntimeError(f"Failed after {max_retries} retries: {last_exc}")


def request_text(url: str, *, headers: Optional[Dict[str, str]] = None, timeout: int = 30,
                 max_retries: int = 3) -> str:
    """Plain-text request (for arXiv Atom XML)."""
    merged_headers = {"User-Agent": USER_AGENT}
    if headers:
        merged_headers.update(headers)
    last_exc: Optional[Exception] = None
    for attempt in range(max_retries):
        req = Request(url, headers=merged_headers)
        try:
            with urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except (HTTPError, URLError) as exc:
            last_exc = exc
            if attempt < max_retries - 1:
                time.sleep(1.0 * (2 ** attempt))
                continue
            raise RuntimeError(f"Failed text fetch from {url}: {exc}") from exc
    raise RuntimeError(f"Failed after {max_retries} retries: {last_exc}")


def normalize_doi(doi: str) -> str:
    doi = (doi or "").strip()
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi, flags=re.I)
    doi = re.sub(r"^doi:\s*", "", doi, flags=re.I)
    return doi.lower()


def normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (title or "").lower()).strip()


def slugify(text: str, max_len: int = 70) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return slug[:max_len].strip("-") or "source"


def split_text_into_segments(text: str, max_chars: int = 700) -> List[str]:
    """Split manuscript-like text into stable, citable claim segments."""
    text = re.sub(r"\r\n?", "\n", text or "").strip()
    if not text:
        return []
    raw_parts = [p.strip() for p in re.split(r"\n\s*\n+", text) if p.strip()]
    segments: List[str] = []
    heading_re = re.compile(r"^(abstract|introduction|results?|discussion|methods?|conclusion|references)\s*$", re.I)
    for part in raw_parts:
        if heading_re.match(part) or len(part) < 35:
            continue
        if len(part) <= max_chars:
            segments.append(re.sub(r"\s+", " ", part).strip())
            continue
        sentences = re.split(r"(?<=[.!?。！？])\s+", part)
        buf = ""
        for sent in sentences:
            sent = sent.strip()
            if not sent:
                continue
            if buf and len(buf) + len(sent) + 1 > max_chars:
                segments.append(re.sub(r"\s+", " ", buf).strip())
                buf = sent
            else:
                buf = f"{buf} {sent}".strip()
        if buf:
            segments.append(re.sub(r"\s+", " ", buf).strip())
    return segments


STOPWORDS = {
    "about", "above", "after", "again", "against", "also", "among", "because",
    "between", "could", "from", "have", "into", "more", "most", "such", "than",
    "that", "their", "these", "this", "through", "under", "using", "were", "when",
    "where", "which", "with", "without", "while", "there", "those", "show", "shows",
    "shown", "based", "result", "results", "study", "paper", "claim",
}


def keywords_for_query(text: str, max_terms: int = 10) -> str:
    words = re.findall(r"[A-Za-z][A-Za-z0-9\-]{2,}", text or "")
    kept: List[str] = []
    seen = set()
    for word in words:
        low = word.lower().strip("-")
        if low in STOPWORDS or low in seen:
            continue
        seen.add(low)
        kept.append(word)
        if len(kept) >= max_terms:
            break
    return " ".join(kept) or text[:140]


def generated_queries_for_claim(segment_id: str, claim: str, profile: str) -> List[QuerySpec]:
    core = keywords_for_query(claim)
    profile = profile or "broad"
    if profile == "materials-mechanism":
        rows = [
            ("support", f"{core} material structure property mechanism characterization"),
            ("support", f"{core} stability performance mechanism materials review"),
            ("adversarial", f"{core} artifact contamination degradation alternative explanation"),
            ("neutral", f"{core} materials mechanism review"),
        ]
    elif profile == "computational-methods":
        rows = [
            ("support", f"{core} scientific machine learning active learning property prediction"),
            ("support", f"{core} representation learning benchmark small data"),
            ("adversarial", f"{core} data leakage overfitting baseline distribution shift benchmark critique"),
            ("neutral", f"{core} computational discovery review"),
        ]
    elif profile == "bio-application":
        rows = [
            ("support", f"{core} biological application performance controlled study"),
            ("support", f"{core} applied material biological response review"),
            ("adversarial", f"{core} confounding factor dose response control no effect"),
            ("neutral", f"{core} application biology review"),
        ]
    else:
        rows = [
            ("support", core),
            ("adversarial", f"{core} limitation contradiction alternative explanation artifact"),
            ("neutral", f"{core} review"),
        ]
    return [QuerySpec(intent=intent, query=query, segment_id=segment_id, segment_text=claim) for intent, query in rows]


def support_grade_for_record(rec: PaperRecord) -> str:
    if rec.retrieval_intent == "adversarial":
        return "contradictory-or-limiting"
    haystack = normalize_title(" ".join([rec.title, rec.abstract, rec.venue]))
    terms = [t for t in normalize_title(rec.query).split() if len(t) > 3 and t not in STOPWORDS]
    if not terms:
        return "metadata-only"
    hits = sum(1 for term in terms[:10] if term in haystack)
    if rec.abstract and hits >= 5:
        return "direct-support"
    if rec.abstract and hits >= 3:
        return "partial-support"
    if hits >= 2:
        return "background-only"
    return "metadata-only"


def abstract_from_openalex_inverted(index: Optional[Dict[str, List[int]]]) -> str:
    if not index:
        return ""
    positions: Dict[int, str] = {}
    for word, offsets in index.items():
        for offset in offsets:
            positions[offset] = word
    return " ".join(positions[i] for i in sorted(positions))


def clean_author_list(authors: Iterable[Any], provider: str) -> str:
    names: List[str] = []
    for author in authors or []:
        if provider == "semantic_scholar":
            name = author.get("name", "") if isinstance(author, dict) else ""
        elif provider == "crossref":
            if not isinstance(author, dict):
                name = ""
            else:
                name = " ".join(x for x in [author.get("given", ""), author.get("family", "")] if x).strip()
        elif provider == "openalex":
            if isinstance(author, dict):
                name = author.get("author", {}).get("display_name", "")
            else:
                name = ""
        elif provider == "europepmc":
            name = author.get("fullName", "") if isinstance(author, dict) else ""
        else:
            name = ""
        if name:
            names.append(name)
    if len(names) > 6:
        return ", ".join(names[:6]) + " et al."
    return ", ".join(names)


def search_semantic_scholar(query: str, limit: int, intent: str) -> List[PaperRecord]:
    fields = "title,year,authors,venue,abstract,externalIds,url,citationCount,isOpenAccess,openAccessPdf"
    url = "https://api.semanticscholar.org/graph/v1/paper/search?" + urlencode({
        "query": query,
        "limit": limit,
        "fields": fields,
    })
    headers: Dict[str, str] = {}
    key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    if key:
        headers["x-api-key"] = key
    data = request_json(url, headers=headers)
    records: List[PaperRecord] = []
    for item in data.get("data", []) or []:
        ext = item.get("externalIds") or {}
        pdf = item.get("openAccessPdf") or {}
        records.append(PaperRecord(
            provider="semantic_scholar",
            retrieval_intent=intent,
            query=query,
            title=item.get("title") or "",
            year=str(item.get("year") or ""),
            venue=item.get("venue") or "",
            authors=clean_author_list(item.get("authors") or [], "semantic_scholar"),
            doi=normalize_doi(ext.get("DOI") or ""),
            url=item.get("url") or "",
            abstract=item.get("abstract") or "",
            citation_count=item.get("citationCount"),
            is_open_access=item.get("isOpenAccess"),
            oa_pdf=pdf.get("url") or "",
            raw_id=item.get("paperId") or "",
        ))
    return records


def search_crossref(query: str, limit: int, intent: str) -> List[PaperRecord]:
    params = {"query.bibliographic": query, "rows": limit}
    mailto = os.getenv("CROSSREF_MAILTO") or os.getenv("UNPAYWALL_EMAIL")
    if mailto:
        params["mailto"] = mailto
    url = "https://api.crossref.org/works?" + urlencode(params)
    data = request_json(url)
    records: List[PaperRecord] = []
    for item in (data.get("message") or {}).get("items", []) or []:
        title = " ".join(item.get("title") or [])
        container = " ".join(item.get("container-title") or [])
        date_parts = (((item.get("issued") or {}).get("date-parts") or [[]])[0])
        year = str(date_parts[0]) if date_parts else ""
        abstract = re.sub(r"<[^>]+>", " ", item.get("abstract") or "")
        records.append(PaperRecord(
            provider="crossref",
            retrieval_intent=intent,
            query=query,
            title=title,
            year=year,
            venue=container,
            authors=clean_author_list(item.get("author") or [], "crossref"),
            doi=normalize_doi(item.get("DOI") or ""),
            url=item.get("URL") or "",
            abstract=re.sub(r"\s+", " ", abstract).strip(),
            citation_count=item.get("is-referenced-by-count"),
            raw_id=item.get("DOI") or item.get("URL") or "",
        ))
    return records


def search_openalex(query: str, limit: int, intent: str) -> List[PaperRecord]:
    params = {"search": query, "per-page": limit}
    mailto = os.getenv("OPENALEX_MAILTO") or os.getenv("UNPAYWALL_EMAIL")
    if mailto:
        params["mailto"] = mailto
    key = os.getenv("OPENALEX_API_KEY")
    if key:
        params["api_key"] = key
    url = "https://api.openalex.org/works?" + urlencode(params)
    data = request_json(url)
    records: List[PaperRecord] = []
    for item in data.get("results", []) or []:
        loc = item.get("primary_location") or {}
        source = loc.get("source") or {}
        records.append(PaperRecord(
            provider="openalex",
            retrieval_intent=intent,
            query=query,
            title=item.get("title") or item.get("display_name") or "",
            year=str(item.get("publication_year") or ""),
            venue=source.get("display_name") or "",
            authors=clean_author_list(item.get("authorships") or [], "openalex"),
            doi=normalize_doi(item.get("doi") or ""),
            url=item.get("id") or "",
            abstract=abstract_from_openalex_inverted(item.get("abstract_inverted_index")),
            citation_count=item.get("cited_by_count"),
            is_open_access=(item.get("open_access") or {}).get("is_oa"),
            oa_pdf=(item.get("open_access") or {}).get("oa_url") or "",
            raw_id=item.get("id") or "",
        ))
    return records


def search_europepmc(query: str, limit: int, intent: str) -> List[PaperRecord]:
    """Europe PMC search. Free, no key required. Strong biomedical / life-science coverage.

    Returns title, abstract, year, journal, authors, DOI and an OA full-text URL when available.
    """
    params = {
        "query": query,
        "format": "json",
        "pageSize": limit,
        "resultType": "core",
    }
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urlencode(params)
    data = request_json(url)
    records: List[PaperRecord] = []
    result_list = (data.get("resultList") or {}).get("result", []) or []
    for item in result_list:
        doi = normalize_doi(item.get("doi") or "")
        pmcid = item.get("pmcid") or ""
        full_text_urls = ((item.get("fullTextUrlList") or {}).get("fullTextUrl")) or []
        oa_pdf = ""
        # Prefer the OA PDF link if Europe PMC returned one
        for entry in full_text_urls:
            if not isinstance(entry, dict):
                continue
            if (entry.get("availability") or "").lower().startswith("open access") and \
                    (entry.get("documentStyle") or "").lower() == "pdf":
                oa_pdf = entry.get("url") or ""
                break
        canonical_url = ""
        if doi:
            canonical_url = f"https://doi.org/{doi}"
        elif pmcid:
            canonical_url = f"https://europepmc.org/article/PMC/{pmcid}"
        records.append(PaperRecord(
            provider="europepmc",
            retrieval_intent=intent,
            query=query,
            title=item.get("title") or "",
            year=str(item.get("pubYear") or ""),
            venue=item.get("journalTitle") or item.get("bookOrReportDetails", {}).get("publisher", "") if isinstance(item.get("bookOrReportDetails"), dict) else item.get("journalTitle") or "",
            authors=clean_author_list((item.get("authorList") or {}).get("author") or [], "europepmc"),
            doi=doi,
            url=canonical_url,
            abstract=re.sub(r"\s+", " ", item.get("abstractText") or "").strip(),
            citation_count=item.get("citedByCount"),
            is_open_access=(item.get("isOpenAccess") == "Y"),
            oa_pdf=oa_pdf,
            raw_id=pmcid or item.get("id") or "",
        ))
    return records


def search_arxiv(query: str, limit: int, intent: str) -> List[PaperRecord]:
    """arXiv API search. Free, no key required. Strong ML / methods coverage.

    The arXiv API returns Atom XML; we parse the minimum we need.
    """
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": limit,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    url = "http://export.arxiv.org/api/query?" + urlencode(params)
    xml_text = request_text(url)
    records: List[PaperRecord] = []
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return records
    for entry in root.findall("atom:entry", ns):
        title_el = entry.find("atom:title", ns)
        summary_el = entry.find("atom:summary", ns)
        published_el = entry.find("atom:published", ns)
        doi_el = entry.find("arxiv:doi", ns)
        journal_el = entry.find("arxiv:journal_ref", ns)
        id_el = entry.find("atom:id", ns)
        authors_el = entry.findall("atom:author/atom:name", ns)
        author_names = [a.text or "" for a in authors_el if (a.text or "").strip()]
        if len(author_names) > 6:
            authors_str = ", ".join(author_names[:6]) + " et al."
        else:
            authors_str = ", ".join(author_names)
        year = (published_el.text or "")[:4] if published_el is not None else ""
        arxiv_id = (id_el.text or "") if id_el is not None else ""
        # arXiv PDF link follows a stable pattern.
        oa_pdf = ""
        if arxiv_id:
            oa_pdf = arxiv_id.replace("/abs/", "/pdf/")
            if not oa_pdf.endswith(".pdf"):
                oa_pdf = oa_pdf + ".pdf"
        records.append(PaperRecord(
            provider="arxiv",
            retrieval_intent=intent,
            query=query,
            title=re.sub(r"\s+", " ", title_el.text or "").strip() if title_el is not None else "",
            year=year,
            venue=(journal_el.text or "arXiv") if journal_el is not None else "arXiv",
            authors=authors_str,
            doi=normalize_doi(doi_el.text or "") if doi_el is not None else "",
            url=arxiv_id,
            abstract=re.sub(r"\s+", " ", summary_el.text or "").strip() if summary_el is not None else "",
            citation_count=None,
            is_open_access=True,
            oa_pdf=oa_pdf,
            raw_id=arxiv_id,
        ))
    return records


def search_serper(query: str, limit: int, intent: str) -> List[PaperRecord]:
    key = os.getenv("SERPER_API_KEY")
    if not key:
        return []
    data = request_json(
        "https://google.serper.dev/search",
        method="POST",
        headers={"X-API-KEY": key},
        payload={"q": query, "num": limit},
    )
    records: List[PaperRecord] = []
    for item in data.get("organic", []) or []:
        records.append(PaperRecord(
            provider="serper",
            retrieval_intent=intent,
            query=query,
            title=item.get("title") or "",
            venue=item.get("source") or "web",
            url=item.get("link") or "",
            abstract=item.get("snippet") or "",
            raw_id=item.get("link") or "",
        ))
    return records


def upgrade_with_unpaywall(records: List[PaperRecord], email: str, max_lookups: int = 30) -> int:
    """For each record with a DOI but no oa_pdf, query Unpaywall for the best OA PDF link.

    Returns the number of records actually upgraded. Caps lookups to avoid
    runaway requests on large result sets.
    """
    if not email:
        return 0
    upgraded = 0
    looked_up = 0
    for rec in records:
        if looked_up >= max_lookups:
            break
        doi = normalize_doi(rec.doi)
        if not doi or rec.oa_pdf:
            continue
        looked_up += 1
        try:
            data = request_json(
                f"https://api.unpaywall.org/v2/{doi}?{urlencode({'email': email})}",
            )
        except Exception:  # noqa: BLE001 - silent skip on per-DOI failure is correct here
            continue
        best = data.get("best_oa_location") or {}
        pdf_url = best.get("url_for_pdf") or best.get("url") or ""
        if pdf_url:
            rec.oa_pdf = pdf_url
            if rec.is_open_access is None:
                rec.is_open_access = True
            upgraded += 1
        time.sleep(0.2)
    return upgraded


def retrieve(queries: List[QuerySpec], providers: List[str], limit: int) -> List[PaperRecord]:
    funcs = {
        "semantic_scholar": search_semantic_scholar,
        "crossref": search_crossref,
        "openalex": search_openalex,
        "europepmc": search_europepmc,
        "arxiv": search_arxiv,
        "serper": search_serper,
    }
    all_records: List[PaperRecord] = []
    errors: List[str] = []
    for spec in queries:
        for provider in providers:
            func = funcs.get(provider)
            if not func:
                errors.append(f"unknown provider: {provider}")
                continue
            try:
                fetched = func(spec.query, limit, spec.intent)
                for rec in fetched:
                    rec.segment_id = spec.segment_id
                    rec.segment_text = spec.segment_text
                    rec.support_grade = support_grade_for_record(rec)
                all_records.extend(fetched)
                time.sleep(0.3)
            except Exception as exc:  # noqa: BLE001 - CLI should continue across providers
                errors.append(f"{provider} failed for query {spec.query!r}: {exc}")
    records = dedupe_records(all_records)
    if errors:
        print("Warnings:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
    return records


def filter_records(records: List[PaperRecord], from_year: int = 0, to_year: int = 0,
                   include_journals: Optional[List[str]] = None,
                   exclude_journals: Optional[List[str]] = None) -> List[PaperRecord]:
    include = [j.lower() for j in include_journals or [] if j]
    exclude = [j.lower() for j in exclude_journals or [] if j]
    kept: List[PaperRecord] = []
    for rec in records:
        year = int(rec.year) if str(rec.year).isdigit() else 0
        if from_year and year and year < from_year:
            continue
        if to_year and year and year > to_year:
            continue
        venue = (rec.venue or "").lower()
        if include and not any(j in venue for j in include):
            continue
        if exclude and any(j in venue for j in exclude):
            continue
        kept.append(rec)
    return kept


def dedupe_records(records: List[PaperRecord]) -> List[PaperRecord]:
    seen: Dict[str, PaperRecord] = {}
    for rec in records:
        key = f"{rec.segment_id}|{rec.key()}"
        if not rec.title:
            continue
        if key not in seen:
            seen[key] = rec
            continue
        # Prefer records with DOI, abstract, OA PDF and higher citation count.
        old = seen[key]
        old_score = (int(bool(old.doi)) + int(bool(old.abstract)) +
                     int(bool(old.oa_pdf)) + (old.citation_count or 0) / 100000)
        new_score = (int(bool(rec.doi)) + int(bool(rec.abstract)) +
                     int(bool(rec.oa_pdf)) + (rec.citation_count or 0) / 100000)
        if new_score > old_score:
            seen[key] = rec
    return list(seen.values())


def md_escape(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def render_markdown(records: List[PaperRecord], claim: str, queries: List[QuerySpec],
                    unpaywall_upgrades: int = 0) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: List[str] = []
    lines.append("# CompassBear Literature RAG Evidence Matrix")
    lines.append("")
    lines.append(f"Generated: {now}")
    if unpaywall_upgrades:
        lines.append(f"Unpaywall OA upgrades applied: {unpaywall_upgrades}")
    lines.append("")
    if claim:
        lines.append("## Claim under adjudication")
        lines.append("")
        lines.append(f"> {claim}")
        lines.append("")
    segment_map: Dict[str, str] = {}
    for spec in queries:
        if spec.segment_id and spec.segment_text:
            segment_map.setdefault(spec.segment_id, spec.segment_text)
    if segment_map:
        lines.append("## Claim segments")
        lines.append("")
        lines.append("| Segment | Claim text |")
        lines.append("|---|---|")
        for segment_id, segment_text in segment_map.items():
            lines.append(f"| {md_escape(segment_id)} | {md_escape(segment_text)} |")
        lines.append("")
    lines.append("## Retrieval queries")
    lines.append("")
    lines.append("| Segment | Intent | Query |")
    lines.append("|---|---|---|")
    for spec in queries:
        lines.append(f"| {md_escape(spec.segment_id)} | {spec.intent} | {md_escape(spec.query)} |")
    lines.append("")
    lines.append("## Retrieved candidates")
    lines.append("")
    lines.append("| # | Segment | Intent | Grade | Provider | Year | Title | Venue | DOI | OA PDF | Citations | URL |")
    lines.append("|---:|---|---|---|---|---|---|---|---|---|---:|---|")
    for i, rec in enumerate(records, 1):
        doi = normalize_doi(rec.doi)
        oa_flag = "yes" if rec.oa_pdf else ""
        lines.append(
            f"| {i} | {md_escape(rec.segment_id)} | {rec.retrieval_intent} | {rec.support_grade} | "
            f"{rec.provider} | {md_escape(rec.year)} | "
            f"{md_escape(rec.title)} | {md_escape(rec.venue)} | {md_escape(doi)} | "
            f"{oa_flag} | "
            f"{rec.citation_count if rec.citation_count is not None else ''} | {md_escape(rec.url)} |"
        )
    lines.append("")
    lines.append("## Abstract / snippet notes")
    lines.append("")
    for i, rec in enumerate(records, 1):
        snippet = textwrap.shorten(re.sub(r"\s+", " ", rec.abstract or ""), width=900, placeholder=" ...")
        lines.append(f"### {i}. {rec.title}")
        lines.append("")
        if rec.segment_id:
            lines.append(f"- Segment: {rec.segment_id}")
        lines.append(f"- Intent: {rec.retrieval_intent}")
        lines.append(f"- Provisional grade: {rec.support_grade}")
        lines.append(f"- Provider: {rec.provider}")
        if rec.doi:
            lines.append(f"- DOI: {normalize_doi(rec.doi)}")
        if rec.url:
            lines.append(f"- URL: {rec.url}")
        if rec.oa_pdf:
            lines.append(f"- OA PDF: {rec.oa_pdf}")
        lines.append(f"- Abstract/snippet: {snippet or '[no abstract returned]'}")
        lines.append("")
    lines.append("## RAG Evidence Adjudicator worksheet")
    lines.append("")
    lines.append("Fill this section after reading the retrieved records. Do not treat retrieval as proof.")
    lines.append("")
    lines.append("| Evidence item | Stance | Scope match | What it supports or challenges | Council action |")
    lines.append("|---|---|---|---|---|")
    lines.append("|  | supports / qualifies / refutes / insufficient | direct / adjacent / weak / mismatched |  | promote / keep with boundary / demote / remove / search more |")
    lines.append("")
    lines.append("## Required adversarial check")
    lines.append("")
    lines.append("Before upgrading a claim, verify that at least one adversarial query has been inspected and that counter-evidence or scope limitations have been recorded.")
    return "\n".join(lines) + "\n"


def write_source_notes(records: List[PaperRecord], out_dir: Path, claim: str, max_notes: int = 20) -> None:
    """Write STUB source notes for the human-in-the-loop reading step.

    These stubs are deliberately marked TBD for stance / scope / action /
    source_id. They live in a `generated/` or `from-zotero/` staging subdir
    and must be promoted out of staging (after the human reads the paper and
    fills the fields) before they count as a real source-pack note. The
    promotion gate is enforced by `scripts/check_source_pack_promotion.py`.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    for i, rec in enumerate(records[:max_notes], 1):
        slug = slugify(rec.title)
        path = out_dir / f"source-note-{i:02d}-{slug}.md"
        content = f"""---
source_id: TBD
stance: TBD
scope: TBD
action: TBD
segment_id: {rec.segment_id!r}
provisional_grade: {rec.support_grade!r}
retrieval_intent: {rec.retrieval_intent}
provider: {rec.provider}
title: {rec.title!r}
year: {rec.year!r}
venue: {rec.venue!r}
doi: {normalize_doi(rec.doi)!r}
url: {rec.url!r}
oa_pdf: {rec.oa_pdf!r}
---

# Source note (STUB — not yet promoted) — {rec.title}

> This stub was generated by `literature_rag.py`. Do not cite it until promoted
> per the human-in-the-loop step in
> `skills/compassbear-research-council/references/rag-evidence-adjudicator.md`.

## Claim under adjudication

> {rec.segment_text or claim or '[not specified]'}

## Bibliographic record

- Authors: {rec.authors or '[not returned]'}
- Year: {rec.year or '[not returned]'}
- Venue: {rec.venue or '[not returned]'}
- DOI: {normalize_doi(rec.doi) or '[not returned]'}
- URL: {rec.url or '[not returned]'}
- OA PDF: {rec.oa_pdf or '[not available — check institutional access]'}

## Why this source was retrieved

- Retrieval intent: {rec.retrieval_intent}
- Provisional retrieval grade: {rec.support_grade}
- Query: {rec.query}

## TODO before promotion

- [ ] Read the paper (or its OA full text, or arrange institutional access)
- [ ] Assign a stable `source_id` (e.g. `S1`, `S2`, ...) in the frontmatter
- [ ] Replace `stance: TBD` with one of `supports / qualifies / refutes / insufficient`
- [ ] Replace `scope: TBD` with one of `direct / adjacent / weak / mismatched`
- [ ] Replace `action: TBD` with one of `promote / keep / demote / remove / search-more`
- [ ] Add 1–3 sentence summary of the load-bearing finding in the Notes section below
- [ ] Move the file out of any `generated/` or `from-zotero/` staging subdir
      into `source-packs/` itself

## Abstract / snippet

{(rec.abstract or '[no abstract/snippet returned]').strip()}

## Notes (fill after reading)

[Write 1–3 sentences on what this paper actually shows that bears on the claim
under adjudication. Be specific about measurement, scope and any caveat the
abstract hides.]
"""
        path.write_text(content, encoding="utf-8")


def html_escape(text: str) -> str:
    return (text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def render_html(records: List[PaperRecord], claim: str, queries: List[QuerySpec]) -> str:
    rows = []
    for i, rec in enumerate(records, 1):
        abstract = textwrap.shorten(re.sub(r"\s+", " ", rec.abstract or ""), width=520, placeholder=" ...")
        doi = normalize_doi(rec.doi)
        link = rec.url or (f"https://doi.org/{doi}" if doi else "")
        rows.append(
            "<tr>"
            f"<td>{i}</td>"
            f"<td>{html_escape(rec.segment_id)}</td>"
            f"<td>{html_escape(rec.retrieval_intent)}</td>"
            f"<td>{html_escape(rec.support_grade)}</td>"
            f"<td>{html_escape(rec.provider)}</td>"
            f"<td>{html_escape(rec.year)}</td>"
            f"<td><strong>{html_escape(rec.title)}</strong><br><span>{html_escape(abstract or '[no abstract returned]')}</span></td>"
            f"<td>{html_escape(rec.venue)}</td>"
            f"<td>{html_escape(doi)}</td>"
            f"<td>{'<a href=\"' + html_escape(rec.oa_pdf) + '\">PDF</a>' if rec.oa_pdf else ''}</td>"
            f"<td>{'<a href=\"' + html_escape(link) + '\">link</a>' if link else ''}</td>"
            "</tr>"
        )
    query_rows = []
    for spec in queries:
        query_rows.append(
            f"<tr><td>{html_escape(spec.segment_id)}</td><td>{html_escape(spec.intent)}</td>"
            f"<td>{html_escape(spec.query)}</td></tr>"
        )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>CompassBear Literature RAG Review</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 24px; line-height: 1.45; color: #1f2933; }}
table {{ border-collapse: collapse; width: 100%; margin: 16px 0 28px; font-size: 13px; }}
th, td {{ border: 1px solid #d5dce3; padding: 7px 8px; vertical-align: top; }}
th {{ background: #eef3f7; text-align: left; position: sticky; top: 0; }}
td span {{ color: #4b5563; }}
.note {{ background: #fff7d6; border: 1px solid #ead384; padding: 10px 12px; margin: 12px 0 20px; }}
</style>
</head>
<body>
<h1>CompassBear Literature RAG Review</h1>
<div class="note">Retrieval is discovery, not proof. Promote a source only after reading enough of the paper to judge stance, scope and limitations.</div>
{f'<h2>Claim</h2><p>{html_escape(claim)}</p>' if claim else ''}
<h2>Queries</h2>
<table><thead><tr><th>Segment</th><th>Intent</th><th>Query</th></tr></thead><tbody>
{''.join(query_rows)}
</tbody></table>
<h2>Candidates</h2>
<table><thead><tr><th>#</th><th>Segment</th><th>Intent</th><th>Grade</th><th>Provider</th><th>Year</th><th>Title / abstract</th><th>Venue</th><th>DOI</th><th>OA</th><th>URL</th></tr></thead><tbody>
{''.join(rows)}
</tbody></table>
</body>
</html>
"""


def ris_type(rec: PaperRecord) -> str:
    venue = (rec.venue or "").lower()
    if rec.provider == "arxiv" or "arxiv" in venue:
        return "JOUR"
    return "JOUR"


def first_author_lastname(authors: str) -> str:
    if not authors:
        return "unknown"
    first = authors.split(",", 1)[0].strip()
    return re.sub(r"[^A-Za-z0-9]+", "", first.split()[-1] if first.split() else first) or "unknown"


def export_records(records: List[PaperRecord], fmt: str) -> str:
    fmt = fmt.lower()
    chunks: List[str] = []
    if fmt == "ris":
        for rec in records:
            chunks.extend([
                f"TY  - {ris_type(rec)}",
                f"TI  - {rec.title}",
                f"JO  - {rec.venue}",
                f"PY  - {rec.year}",
            ])
            for author in [a.strip() for a in rec.authors.split(",") if a.strip()]:
                chunks.append(f"AU  - {author}")
            if rec.doi:
                chunks.append(f"DO  - {normalize_doi(rec.doi)}")
            if rec.url:
                chunks.append(f"UR  - {rec.url}")
            if rec.abstract:
                chunks.append(f"AB  - {rec.abstract}")
            chunks.extend(["ER  -", ""])
    elif fmt == "enw":
        for rec in records:
            chunks.extend([
                "%0 Journal Article",
                f"%T {rec.title}",
                f"%J {rec.venue}",
                f"%D {rec.year}",
            ])
            for author in [a.strip() for a in rec.authors.split(",") if a.strip()]:
                chunks.append(f"%A {author}")
            if rec.doi:
                chunks.append(f"%R {normalize_doi(rec.doi)}")
            if rec.url:
                chunks.append(f"%U {rec.url}")
            if rec.abstract:
                chunks.append(f"%X {rec.abstract}")
            chunks.append("")
    elif fmt == "bib":
        for rec in records:
            key = f"{first_author_lastname(rec.authors)}{rec.year or 'nd'}{slugify(rec.title, 18).replace('-', '')}"
            fields = [
                f"  title = {{{rec.title}}}",
                f"  journal = {{{rec.venue}}}",
                f"  year = {{{rec.year}}}",
            ]
            if rec.authors:
                fields.append(f"  author = {{{' and '.join(a.strip() for a in rec.authors.split(',') if a.strip())}}}")
            if rec.doi:
                fields.append(f"  doi = {{{normalize_doi(rec.doi)}}}")
            if rec.url:
                fields.append(f"  url = {{{rec.url}}}")
            chunks.append("@article{" + key + ",\n" + ",\n".join(fields) + "\n}\n")
    else:
        raise ValueError(f"Unsupported export format: {fmt}")
    return "\n".join(chunks)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retrieve literature candidates for CompassBear RAG adjudication.")
    parser.add_argument("--claim", default="", help="Claim under adjudication.")
    parser.add_argument("--text", default="", help="Long manuscript text to split into citable claim segments.")
    parser.add_argument("--text-file", default="", help="Read long manuscript text from a file and split into claim segments.")
    parser.add_argument("--claim-file", default="", help="Read one claim per non-empty line.")
    parser.add_argument("--profile", choices=sorted(PROFILE_PROVIDERS), default="broad",
                        help="Domain profile for automatic query expansion and provider defaults.")
    parser.add_argument("--support-query", action="append", default=[], help="Support-oriented query. Can be repeated.")
    parser.add_argument("--adversarial-query", action="append", default=[], help="Counter-evidence / limitation query. Can be repeated.")
    parser.add_argument("--query", action="append", default=[], help="Neutral query. Can be repeated.")
    parser.add_argument("--providers", default="",
                        help="Comma-separated providers. Defaults to the selected --profile provider set.")
    parser.add_argument("--max-per-provider", type=int, default=5, help="Maximum records per query per provider.")
    parser.add_argument("--from-year", type=int, default=0, help="Drop records older than this year when year metadata exists.")
    parser.add_argument("--to-year", type=int, default=0, help="Drop records newer than this year when year metadata exists.")
    parser.add_argument("--include-journal", action="append", default=[],
                        help="Keep only venues containing this text. Can be repeated.")
    parser.add_argument("--exclude-journal", action="append", default=[],
                        help="Drop venues containing this text. Can be repeated.")
    parser.add_argument("--no-unpaywall", action="store_true",
                        help="Skip Unpaywall OA upgrade pass even when UNPAYWALL_EMAIL is set.")
    parser.add_argument("--out-md", default=str(DEFAULT_OUT_DIR / "evidence_matrix.md"), help="Markdown output path.")
    parser.add_argument("--out-json", default=str(DEFAULT_OUT_DIR / "evidence_matrix.json"), help="JSON output path.")
    parser.add_argument("--with-html-review", action="store_true", help="Write a browsable HTML review table.")
    parser.add_argument("--out-html", default=str(DEFAULT_OUT_DIR / "evidence_review.html"), help="HTML review output path.")
    parser.add_argument("--export", choices=EXPORT_FORMAT_CHOICES, default="", help="Optional reference export format.")
    parser.add_argument("--out-export", default="", help="Optional reference export path. Defaults to outputs/literature-rag/references.<format>.")
    parser.add_argument("--source-note-dir", default="", help="Optional directory for generated source-note stubs.")
    return parser.parse_args()


def collect_claim_segments(args: argparse.Namespace) -> List[tuple[str, str]]:
    claims: List[str] = []
    if args.claim:
        claims.append(args.claim.strip())
    if args.text:
        claims.extend(split_text_into_segments(args.text))
    if args.text_file:
        claims.extend(split_text_into_segments(Path(args.text_file).read_text(encoding="utf-8")))
    if args.claim_file:
        for line in Path(args.claim_file).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                claims.append(line)
    return [(f"S{i:03d}", claim) for i, claim in enumerate(claims, 1) if claim]


def main() -> int:
    load_dotenv()
    args = parse_args()
    provider_string = args.providers or PROFILE_PROVIDERS.get(args.profile, DEFAULT_PROVIDERS)
    providers = [p.strip() for p in provider_string.split(",") if p.strip()]
    segments = collect_claim_segments(args)
    queries: List[QuerySpec] = []
    for segment_id, segment_text in segments:
        queries.extend(generated_queries_for_claim(segment_id, segment_text, args.profile))
    manual_segment = segments[0] if segments else ("S001", args.claim)
    queries.extend(QuerySpec("support", q, manual_segment[0], manual_segment[1]) for q in args.support_query)
    queries.extend(QuerySpec("adversarial", q, manual_segment[0], manual_segment[1]) for q in args.adversarial_query)
    queries.extend(QuerySpec("neutral", q, manual_segment[0], manual_segment[1]) for q in args.query)
    if not queries and args.claim:
        queries.append(QuerySpec("neutral", args.claim, "S001", args.claim))
        queries.append(QuerySpec("adversarial", f"alternative explanation limitation impurity artifact {args.claim}", "S001", args.claim))
    if not queries:
        print("ERROR: provide --claim, --text, --text-file, --claim-file or at least one manual query", file=sys.stderr)
        return 2

    records = retrieve(queries, providers, args.max_per_provider)
    records = filter_records(records, args.from_year, args.to_year, args.include_journal, args.exclude_journal)

    # Optional Unpaywall OA upgrade pass.
    unpaywall_upgrades = 0
    unpaywall_email = os.getenv("UNPAYWALL_EMAIL", "").strip()
    if unpaywall_email and not args.no_unpaywall:
        unpaywall_upgrades = upgrade_with_unpaywall(records, unpaywall_email)
        if unpaywall_upgrades:
            print(f"Unpaywall: upgraded {unpaywall_upgrades} record(s) with OA PDF link", file=sys.stderr)

    out_md = Path(args.out_md)
    out_json = Path(args.out_json)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(render_markdown(records, args.claim, queries, unpaywall_upgrades), encoding="utf-8")
    out_json.write_text(json.dumps([asdict(r) for r in records], ensure_ascii=False, indent=2), encoding="utf-8")
    if args.with_html_review:
        out_html = Path(args.out_html)
        out_html.parent.mkdir(parents=True, exist_ok=True)
        out_html.write_text(render_html(records, args.claim, queries), encoding="utf-8")
    if args.export:
        out_export = Path(args.out_export) if args.out_export else DEFAULT_OUT_DIR / f"references.{args.export}"
        out_export.parent.mkdir(parents=True, exist_ok=True)
        out_export.write_text(export_records(records, args.export), encoding="utf-8")
    if args.source_note_dir:
        write_source_notes(records, Path(args.source_note_dir), args.claim)
    print(f"OK: wrote {len(records)} records to {out_md} and {out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
