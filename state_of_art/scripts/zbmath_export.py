#!/usr/bin/env python3
"""
Bulk-export zbMATH Open search results to RIS (for direct Zotero import)
plus a separate DOI/arXiv list for records whose metadata is licence-
restricted on the open API (those import better via Zotero's
"Add Item(s) by Identifier" using the DOI/arXiv ID directly).

Usage:
    python3 zbmath_export.py "<search_string>" <output_prefix>

Example:
    python3 zbmath_export.py 'any:(basis* | spline* | Fourier | wavelet*) & any:("functional data analysis" | "functional data" | "functional principal component*" | FPCA) & py:1997-2026' C1_zbmath
"""
import sys
import time
import json
import urllib.request
import urllib.parse

API = "https://api.zbmath.org/v1/document/_search"
REDACTED = "zbMATH Open Web Interface contents unavailable due to conflicting licenses."
DT_MAP = {"j": "JOUR", "b": "BOOK", "a": "CHAP", "p": "UNPB"}


def fetch_page(search_string, page, per_page=100):
    url = API + "?" + urllib.parse.urlencode(
        {"search_string": search_string, "page": page, "results_per_page": per_page}
    )
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def get_doi(doc):
    for link in doc.get("links") or []:
        if link.get("type") == "doi":
            return link.get("identifier")
    return None


def get_arxiv(doc):
    for link in doc.get("links") or []:
        if link.get("type") == "arxiv":
            return link.get("identifier")
    return None


def ris_entry(doc):
    title = doc["title"]["title"]
    year = doc.get("year") or ""
    doc_type = (doc.get("document_type") or {}).get("code", "j")
    ty = DT_MAP.get(doc_type, "GEN")
    src = doc.get("source") or {}
    series = (src.get("series") or [{}])[0]
    journal = series.get("title") or ""
    volume = series.get("volume") or ""
    issue = series.get("issue") or ""
    pages = src.get("pages") or ""
    sp, ep = "", ""
    if "-" in pages:
        parts = pages.replace("~p.", "").split("-")
        if len(parts) == 2:
            sp, ep = parts[0].strip(), parts[1].strip()
    doi = get_doi(doc)
    arxiv = get_arxiv(doc)

    lines = [f"TY  - {ty}"]
    for author in (doc.get("contributors") or {}).get("authors", []):
        name = author.get("name")
        if name and name != REDACTED:
            lines.append(f"AU  - {name}")
    lines.append(f"TI  - {title}")
    if year:
        lines.append(f"PY  - {year}")
    if journal:
        lines.append(f"JO  - {journal}")
    if volume:
        lines.append(f"VL  - {volume}")
    if issue:
        lines.append(f"IS  - {issue}")
    if sp:
        lines.append(f"SP  - {sp}")
    if ep:
        lines.append(f"EP  - {ep}")
    if doi:
        lines.append(f"DO  - {doi}")
    if arxiv:
        lines.append(f"UR  - https://arxiv.org/abs/{arxiv}")
    lines.append("N1  - Source: zbMATH Open (zbmath.org), id " + str(doc.get("id")))
    lines.append("ER  - ")
    return "\n".join(lines)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    search_string, prefix = sys.argv[1], sys.argv[2]

    clean, redacted_dois, redacted_arxiv, redacted_no_id = [], [], [], []
    page = 0
    total = None
    while True:
        data = fetch_page(search_string, page)
        status = data["status"]
        if not status["execution_bool"]:
            print("API error:", status)
            sys.exit(1)
        total = status["nr_total_results"]
        results = data.get("result") or []
        if not results:
            break
        for doc in results:
            title_redacted = doc["title"]["title"] == REDACTED
            if title_redacted:
                doi = get_doi(doc)
                arxiv = get_arxiv(doc)
                if doi:
                    redacted_dois.append(doi)
                elif arxiv:
                    redacted_arxiv.append(arxiv)
                else:
                    redacted_no_id.append(str(doc.get("id")))
            else:
                clean.append(ris_entry(doc))
        print(f"  page {page}: +{len(results)} (total so far: {len(clean) + len(redacted_dois) + len(redacted_arxiv) + len(redacted_no_id)} / {total})")
        page += 1
        if page * 100 >= total:
            break
        time.sleep(0.3)

    ris_path = f"{prefix}.ris"
    with open(ris_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(clean))

    ids_path = f"{prefix}_ids_para_importar_por_DOI.txt"
    with open(ids_path, "w", encoding="utf-8") as f:
        f.write("# DOIs (pegar en Zotero: Add Item(s) by Identifier)\n")
        f.write("\n".join(redacted_dois))
        if redacted_arxiv:
            f.write("\n\n# arXiv IDs (pegar en Zotero: Add Item(s) by Identifier)\n")
            f.write("\n".join(f"arXiv:{a}" for a in redacted_arxiv))
        if redacted_no_id:
            f.write("\n\n# Sin DOI ni arXiv, sin metadatos disponibles via API (revisar manualmente en zbmath.org):\n")
            f.write("\n".join(redacted_no_id))

    print()
    print(f"Total en zbMATH: {total}")
    print(f"Con metadatos completos -> {ris_path} ({len(clean)} registros)")
    print(f"Restringidos por licencia, con DOI -> {len(redacted_dois)}")
    print(f"Restringidos por licencia, con arXiv ID -> {len(redacted_arxiv)}")
    print(f"Restringidos, sin identificador -> {len(redacted_no_id)}")
    print(f"Lista de identificadores -> {ids_path}")


if __name__ == "__main__":
    main()
