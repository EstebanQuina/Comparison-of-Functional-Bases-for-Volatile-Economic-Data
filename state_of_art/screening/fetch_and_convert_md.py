#!/usr/bin/env python3
"""Download the source document for each included item and convert it to
Markdown via Microsoft's markitdown, for Fase 7-9 (local-only, gitignored).

Usage: python3 fetch_and_convert_md.py <incluidos_csv> <out_dir>
Reads: incluidos_final_91.csv (id, title, authors, year, container, doi, enlace, origen)
Writes: <out_dir>/raw/<id>.<ext>, <out_dir>/md/<id>.md, <out_dir>/convert_status.csv
"""
import csv
import sys
import os
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

from markitdown import MarkItDown

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) thesis-review/1.0 (mailto:estebanquinia@gmail.com)"

JUNK_SIGNS = [
    "toggle navigation", "skip to main content", "communities and collections",
    "making sure you're not a bot", "anubis", "checking your browser",
    "just a moment...", "verify you are human", "captcha", "cookie",
    "sign in to view", "purchase this article", "institutional login",
]


def looks_like_landing_page(text):
    low = text.lower()
    hits = sum(1 for s in JUNK_SIGNS if s in low)
    return hits >= 2 or len(text) < 3000


def to_pdf_url(url):
    if url and "arxiv.org/abs/" in url:
        return url.replace("/abs/", "/pdf/")
    return url


def fetch_bytes(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        ctype = resp.headers.get("Content-Type", "")
        data = resp.read()
    return data, ctype


def process_one(item, raw_dir, md_dir):
    rid, title, authors, year, container, doi, url, origen = item
    url = to_pdf_url(url)
    try:
        data, ctype = fetch_bytes(url)
    except Exception as e:
        return rid, "error_fetch", str(e)[:200]

    is_pdf = "pdf" in ctype.lower() or data[:4] == b"%PDF"
    ext = "pdf" if is_pdf else "html"
    raw_path = f"{raw_dir}/{rid}.{ext}"
    with open(raw_path, "wb") as f:
        f.write(data)

    if len(data) < 2000:
        return rid, "too_short", None

    try:
        mdconv = MarkItDown()
        result = mdconv.convert(raw_path)
        text = result.text_content
    except Exception as e:
        return rid, "error_convert", str(e)[:200]

    if not text or len(text.strip()) < 500:
        return rid, "empty_conversion", None

    status = "landing_page_suspect" if looks_like_landing_page(text) else "ok"

    header = (
        f"# {title}\n\n"
        f"**Autores:** {authors}\n"
        f"**Año:** {year}  \n**Revista/fuente:** {container}  \n"
        f"**DOI:** {doi}  \n**URL origen:** {url}  \n**ID interno:** {rid}\n\n---\n\n"
    )
    with open(f"{md_dir}/{rid}.md", "w", encoding="utf-8") as f:
        f.write(header + text)

    return rid, status, None


def main():
    csv_path, out_dir = sys.argv[1], sys.argv[2]
    raw_dir = f"{out_dir}/raw"
    md_dir = f"{out_dir}/md"
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(md_dir, exist_ok=True)

    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    items = [
        (r["id"], r["title"], r["authors"], r["year"], r["container"], r["doi"], r["enlace"], r["origen"])
        for r in rows
    ]

    print(f"Procesando {len(items)} ítems...")
    results = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(process_one, it, raw_dir, md_dir): it[0] for it in items}
        done = 0
        for fut in as_completed(futs):
            rid, status, err = fut.result()
            results.append({"id": rid, "status": status, "error": err})
            done += 1
            if done % 20 == 0:
                print(f"  {done}/{len(items)}")

    with open(f"{out_dir}/convert_status.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "status", "error"])
        w.writeheader()
        for r in sorted(results, key=lambda r: r["id"]):
            w.writerow(r)

    from collections import Counter
    print("\n=== RESUMEN ===")
    print(Counter(r["status"] for r in results))


if __name__ == "__main__":
    main()
