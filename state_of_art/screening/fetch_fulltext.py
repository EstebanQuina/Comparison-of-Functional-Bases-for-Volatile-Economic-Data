#!/usr/bin/env python3
"""Fetch and extract full-text excerpts (intro + methods-ish middle + tail)
for items flagged as_oa in oa_status.csv, ahead of Etapa 2 AI-assisted
full-text screening.

Never commits raw PDFs/HTML — only caches locally (gitignored) and, for
downstream classification, truncated plain-text excerpts.

Usage: python3 fetch_fulltext.py [--limit N] [--ids id1,id2,...]
Reads: oa_status.csv, library_enriched.json
Writes: fulltext_cache/<id>.txt (raw extracted text, gitignored)
        fulltext_status.csv (id, doi, url_used, status, n_chars, method)
"""
import csv
import io
import json
import re
import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

from pypdf import PdfReader
from bs4 import BeautifulSoup

CACHE_DIR = "fulltext_cache"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) thesis-review/1.0 (mailto:estebanquinia@gmail.com)"


def to_pdf_url(url, host_type):
    if not url:
        return url
    if "arxiv.org/abs/" in url:
        return url.replace("/abs/", "/pdf/")
    return url


def fetch_bytes(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        ctype = resp.headers.get("Content-Type", "")
        data = resp.read()
    return data, ctype


def extract_pdf_text(data):
    reader = PdfReader(io.BytesIO(data))
    parts = []
    for page in reader.pages:
        try:
            parts.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n".join(parts)


def extract_html_text(data):
    soup = BeautifulSoup(data, "lxml")
    for tag in soup(["script", "style", "nav", "header", "footer", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def process_one(item):
    rid, url, host_type = item
    pdf_url = to_pdf_url(url, host_type)
    try:
        data, ctype = fetch_bytes(pdf_url)
    except Exception as e:
        return rid, "error_fetch", str(e)[:200], 0, None

    is_pdf = "pdf" in ctype.lower() or data[:4] == b"%PDF"
    try:
        if is_pdf:
            text = extract_pdf_text(data)
            method = "pdf"
        else:
            text = extract_html_text(data)
            method = "html"
    except Exception as e:
        return rid, "error_parse", str(e)[:200], 0, None

    text = text.strip()
    if len(text) < 500:
        return rid, "too_short", None, len(text), method

    with open(f"{CACHE_DIR}/{rid}.txt", "w", encoding="utf-8") as f:
        f.write(text)
    return rid, "ok", None, len(text), method


def main():
    import os
    os.makedirs(CACHE_DIR, exist_ok=True)

    limit = None
    only_ids = None
    args = sys.argv[1:]
    if "--limit" in args:
        limit = int(args[args.index("--limit") + 1])
    if "--ids" in args:
        only_ids = set(int(x) for x in args[args.index("--ids") + 1].split(","))

    with open("oa_status.csv", newline="", encoding="utf-8") as f:
        oa_rows = [r for r in csv.DictReader(f) if r["is_oa"] == "True"]

    items = []
    for r in oa_rows:
        rid = int(r["id"])
        if only_ids and rid not in only_ids:
            continue
        if not r["oa_url"]:
            continue
        items.append((rid, r["oa_url"], r["host_type"]))

    if limit:
        items = items[:limit]

    print(f"Procesando {len(items)} ítems...")
    results = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(process_one, it): it[0] for it in items}
        done = 0
        for fut in as_completed(futs):
            rid, status, err, nchars, method = fut.result()
            results.append({"id": rid, "status": status, "error": err, "n_chars": nchars, "method": method})
            done += 1
            if done % 50 == 0:
                print(f"  {done}/{len(items)}")

    with open("fulltext_status.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "status", "error", "n_chars", "method"])
        w.writeheader()
        for r in sorted(results, key=lambda r: r["id"]):
            w.writerow(r)

    from collections import Counter
    print("\n=== RESUMEN ===")
    print(Counter(r["status"] for r in results))


if __name__ == "__main__":
    main()
