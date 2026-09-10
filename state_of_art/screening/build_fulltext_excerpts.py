#!/usr/bin/env python3
"""Build bounded excerpts (head + tail) from cached full texts for
AI-assisted full-text screening (Etapa 2), plus merge in the item's
existing metadata (title, doi, Etapa-1 abstract).

Usage: python3 build_fulltext_excerpts.py
Reads: fulltext_status.csv (status==ok), fulltext_cache/<id>.txt,
       library_enriched.json, decisions_master.csv
Writes: fulltext_excerpts.json
"""
import csv
import json
import re

HEAD_CHARS = 6000
TAIL_CHARS = 3000


def clean(text):
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main():
    with open("fulltext_status.csv", newline="", encoding="utf-8") as f:
        ok_ids = [int(r["id"]) for r in csv.DictReader(f) if r["status"] == "ok"]

    with open("library_enriched.json", encoding="utf-8") as f:
        library = {e["id"]: e for e in json.load(f)}

    with open("decisions_master.csv", newline="", encoding="utf-8") as f:
        etapa1 = {int(r["id"]): r for r in csv.DictReader(f)}

    out = []
    for rid in ok_ids:
        with open(f"fulltext_cache/{rid}.txt", encoding="utf-8") as f:
            text = clean(f.read())

        if len(text) <= HEAD_CHARS + TAIL_CHARS:
            excerpt = text
        else:
            excerpt = (
                text[:HEAD_CHARS]
                + "\n\n[... omitido el cuerpo intermedio del documento ...]\n\n"
                + text[-TAIL_CHARS:]
            )

        e = library.get(rid, {})
        e1 = etapa1.get(rid, {})
        out.append(
            {
                "id": rid,
                "title": e.get("title"),
                "doi": e.get("doi"),
                "abstract_etapa1": e.get("abstract"),
                "etapa1_reason": e1.get("reason_code"),
                "etapa1_rationale": e1.get("rationale"),
                "fulltext_excerpt": excerpt,
                "excerpt_n_chars": len(excerpt),
                "full_n_chars": len(text),
            }
        )

    with open("fulltext_excerpts.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print(f"{len(out)} excerptos escritos -> fulltext_excerpts.json")
    total_chars = sum(o["excerpt_n_chars"] for o in out)
    print(f"tamaño total de excerptos: {total_chars:,} caracteres (~{total_chars//4:,} tokens aprox.)")


if __name__ == "__main__":
    main()
