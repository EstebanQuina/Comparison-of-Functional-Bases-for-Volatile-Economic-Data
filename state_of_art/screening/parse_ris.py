#!/usr/bin/env python3
"""Parse the deduplicated Zotero RIS export into structured JSON records.

Usage: python3 parse_ris.py <input.ris> <output.json>
"""
import sys
import json

FIELD_MAP = {
    "TY": "type",
    "TI": "title",
    "T2": "container",
    "PY": "year",
    "DO": "doi",
    "DB": "source_db",
    "UR": "url",
    "AB": "abstract",
    "KW": "keywords",
    "N1": "notes",
    "AU": "authors",
    "SN": "isbn_issn",
}


def parse(path):
    entries = []
    cur = None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("TY  -"):
                cur = {
                    "type": line[6:].strip(),
                    "title": None,
                    "container": None,
                    "year": None,
                    "doi": None,
                    "source_db": None,
                    "url": None,
                    "abstract": None,
                    "abstract_source": None,
                    "keywords": [],
                    "notes": [],
                    "authors": [],
                    "isbn_issn": None,
                }
            elif cur is None:
                continue
            elif line.startswith("ER  -"):
                if cur["abstract"]:
                    cur["abstract_source"] = "original_ris"
                entries.append(cur)
                cur = None
            else:
                tag = line[:2]
                val = line[6:].strip() if len(line) > 6 else ""
                field = FIELD_MAP.get(tag)
                if field is None:
                    continue
                if field in ("keywords", "notes", "authors"):
                    cur[field].append(val)
                elif field == "abstract":
                    cur[field] = (cur[field] + " " + val) if cur[field] else val
                else:
                    if cur[field] is None:
                        cur[field] = val
    return entries


if __name__ == "__main__":
    inp, outp = sys.argv[1], sys.argv[2]
    entries = parse(inp)
    for i, e in enumerate(entries):
        e["id"] = i
    with open(outp, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=1)
    print(f"Parsed {len(entries)} entries -> {outp}")
    with_ab = sum(1 for e in entries if e["abstract"])
    with_doi = sum(1 for e in entries if e["doi"])
    print(f"With abstract (original RIS): {with_ab}")
    print(f"With DOI: {with_doi}")
