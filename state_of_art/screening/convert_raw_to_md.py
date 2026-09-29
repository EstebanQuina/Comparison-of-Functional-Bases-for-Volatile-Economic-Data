#!/usr/bin/env python3
"""Convert already-downloaded raw documents (state_of_art/fulltext_md/raw/)
to Markdown: pymupdf4llm for PDFs (much cleaner tables/spacing than
markitdown's PDF backend), markitdown for HTML. Does not re-fetch anything.

Usage: python3 convert_raw_to_md.py <incluidos_csv> <fulltext_md_dir>
"""
import csv
import glob
import os
import sys

import pymupdf4llm
from markitdown import MarkItDown

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


def main():
    csv_path, base_dir = sys.argv[1], sys.argv[2]
    raw_dir = f"{base_dir}/raw"
    md_dir = f"{base_dir}/md"
    os.makedirs(md_dir, exist_ok=True)

    with open(csv_path, newline="", encoding="utf-8") as f:
        meta = {r["id"]: r for r in csv.DictReader(f)}

    raw_files = sorted(glob.glob(f"{raw_dir}/*"))
    print(f"{len(raw_files)} archivos crudos encontrados")

    results = []
    for path in raw_files:
        base = os.path.basename(path)
        rid, ext = os.path.splitext(base)
        ext = ext.lower().lstrip(".")

        try:
            if ext == "pdf":
                text = pymupdf4llm.to_markdown(path)
                method = "pymupdf4llm"
            elif ext == "html":
                result = MarkItDown().convert(path)
                text = result.text_content
                method = "markitdown_html"
            else:
                results.append({"id": rid, "status": "unknown_ext", "method": ext})
                continue
        except Exception as e:
            results.append({"id": rid, "status": "error_convert", "method": ext, "error": str(e)[:200]})
            continue

        if not text or len(text.strip()) < 500:
            results.append({"id": rid, "status": "empty_conversion", "method": method})
            continue

        status = "landing_page_suspect" if looks_like_landing_page(text) else "ok"

        e = meta.get(rid, {})
        header = (
            f"# {e.get('title', rid)}\n\n"
            f"**Autores:** {e.get('authors', '')}\n"
            f"**Año:** {e.get('year', '')}  \n**Revista/fuente:** {e.get('container', '')}  \n"
            f"**DOI:** {e.get('doi', '')}  \n**URL origen:** {e.get('enlace', '')}  \n**ID interno:** {rid}\n\n---\n\n"
        )
        with open(f"{md_dir}/{rid}.md", "w", encoding="utf-8") as f:
            f.write(header + text)

        results.append({"id": rid, "status": status, "method": method})

    with open(f"{base_dir}/convert_status.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "status", "method", "error"])
        w.writeheader()
        for r in sorted(results, key=lambda r: r["id"]):
            w.writerow({**{"error": ""}, **r})

    from collections import Counter
    print("\n=== RESUMEN ===")
    print(Counter(r["status"] for r in results))


if __name__ == "__main__":
    main()
