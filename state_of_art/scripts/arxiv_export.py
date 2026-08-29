#!/usr/bin/env python3
"""
Bulk-export arXiv search results to RIS (for direct Zotero import),
using arXiv's public Atom API (export.arxiv.org/api/query).

Usage:
    python3 arxiv_export.py "<search_query>" <output_prefix>

Example:
    python3 arxiv_export.py '(all:"functional data analysis" OR all:"functional data" OR all:"functional principal component" OR all:FPCA) AND (all:basis OR all:spline OR all:Fourier OR all:wavelet) AND submittedDate:[19970101000000 TO 20261231235959]' C1_arxiv
"""
import sys
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

API = "http://export.arxiv.org/api/query"
NS = {
    "a": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
    "opensearch": "http://a9.com/-/spec/opensearch/1.1/",
}


def fetch_page(search_query, start, max_results=100, retries=6):
    url = API + "?" + urllib.parse.urlencode(
        {"search_query": search_query, "start": start, "max_results": max_results}
    )
    last_err = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return ET.fromstring(r.read())
        except Exception as e:
            last_err = e
            time.sleep(2 * (attempt + 1))
    raise last_err


def author_ris(name):
    parts = name.strip().split()
    if len(parts) < 2:
        return name
    return f"{parts[-1]}, {' '.join(parts[:-1])}"


def ris_entry(entry):
    title = (entry.findtext("a:title", default="", namespaces=NS) or "").strip().replace("\n", " ")
    summary = (entry.findtext("a:summary", default="", namespaces=NS) or "").strip().replace("\n", " ")
    published = entry.findtext("a:published", default="", namespaces=NS) or ""
    year = published[:4]
    arxiv_id = entry.findtext("a:id", default="", namespaces=NS).rsplit("/", 1)[-1]
    journal_ref = entry.findtext("arxiv:journal_ref", default=None, namespaces=NS)
    doi = entry.findtext("arxiv:doi", default=None, namespaces=NS)
    authors = [
        a.findtext("a:name", default="", namespaces=NS)
        for a in entry.findall("a:author", NS)
    ]

    ty = "JOUR" if journal_ref else "UNPB"
    lines = [f"TY  - {ty}"]
    for name in authors:
        if name:
            lines.append(f"AU  - {author_ris(name)}")
    lines.append(f"TI  - {title}")
    if year:
        lines.append(f"PY  - {year}")
    if journal_ref:
        lines.append(f"JO  - {journal_ref}")
    if doi:
        lines.append(f"DO  - {doi}")
    lines.append(f"UR  - https://arxiv.org/abs/{arxiv_id}")
    if summary:
        lines.append(f"AB  - {summary}")
    lines.append(f"N1  - Source: arXiv ({arxiv_id})")
    lines.append("ER  - ")
    return "\n".join(lines)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    search_query, prefix = sys.argv[1], sys.argv[2]

    entries_ris = []
    start = 0
    per_page = 100
    total = None
    while True:
        root = fetch_page(search_query, start, per_page)
        if total is None:
            total = int(root.findtext("opensearch:totalResults", default="0", namespaces=NS))
        entries = root.findall("a:entry", NS)
        if not entries:
            break
        for entry in entries:
            entries_ris.append(ris_entry(entry))
        print(f"  start {start}: +{len(entries)} (total so far: {len(entries_ris)} / {total})")
        start += per_page
        if start >= total:
            break
        time.sleep(3)  # arXiv API etiquette: no more than 1 request per 3 seconds

    ris_path = f"{prefix}.ris"
    with open(ris_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(entries_ris))

    print()
    print(f"Total en arXiv: {total}")
    print(f"Exportado -> {ris_path} ({len(entries_ris)} registros)")


if __name__ == "__main__":
    main()
