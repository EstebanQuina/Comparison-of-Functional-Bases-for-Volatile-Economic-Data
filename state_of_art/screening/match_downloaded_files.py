#!/usr/bin/env python3
"""Match downloaded PDF/HTML files (arbitrary filenames) to the pending
ids by extracting text and fuzzy-matching titles.

Usage: python3 match_downloaded_files.py <downloads_dir> <pendientes_csv>
"""
import sys
import re
import csv
import glob
import os
import difflib

import fitz  # pymupdf


def normalize(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def extract_text_sample(path, max_chars=4000):
    ext = os.path.splitext(path)[1].lower()
    try:
        if ext == ".pdf":
            doc = fitz.open(path)
            text = ""
            for page in doc[:2]:
                text += page.get_text()
                if len(text) > max_chars:
                    break
            doc.close()
            return text[:max_chars]
        elif ext in (".html", ".htm"):
            with open(path, encoding="utf-8", errors="replace") as f:
                raw = f.read()
            text = re.sub(r"<[^>]+>", " ", raw)
            return text[:max_chars]
    except Exception as e:
        return f"[ERROR: {e}]"
    return ""


def main():
    downloads_dir, csv_path = sys.argv[1], sys.argv[2]

    with open(csv_path, newline="", encoding="utf-8") as f:
        pending = list(csv.DictReader(f))
    candidates = [(r["id"], r["title"]) for r in pending]
    candidates.append(("padilla_segarra", "Padilla-Segarra Gonzalez-Villacorte Amaro Infante"))

    files = sorted(glob.glob(f"{downloads_dir}/*"))
    print(f"{len(files)} archivos a procesar, {len(candidates)} candidatos\n")

    norm_titles = {cid: normalize(title) for cid, title in candidates}

    results = []
    for path in files:
        fname = os.path.basename(path)
        text = extract_text_sample(path)
        norm_text = normalize(text[:2000])

        scores = []
        for cid, ntitle in norm_titles.items():
            # score: ratio of title words found in text, weighted by SequenceMatcher on best window
            title_words = ntitle.split()
            if not title_words:
                continue
            hits = sum(1 for w in title_words if len(w) > 3 and w in norm_text)
            word_score = hits / max(1, sum(1 for w in title_words if len(w) > 3))
            scores.append((word_score, cid))

        scores.sort(reverse=True)
        best_score, best_id = scores[0] if scores else (0, None)
        second_score = scores[1][0] if len(scores) > 1 else 0

        results.append({
            "file": fname,
            "best_id": best_id,
            "best_score": round(best_score, 2),
            "second_score": round(second_score, 2),
            "ambiguous": (best_score - second_score) < 0.15 or best_score < 0.5,
        })

    print(f"{'archivo':60s} {'id':>6s} {'score':>6s} {'2do':>6s}  amb?")
    for r in results:
        flag = "  <-- REVISAR" if r["ambiguous"] else ""
        print(f"{r['file'][:60]:60s} {str(r['best_id']):>6s} {r['best_score']:>6.2f} {r['second_score']:>6.2f}{flag}")

    with open(f"{downloads_dir}/_match_results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["file", "best_id", "best_score", "second_score", "ambiguous"])
        w.writeheader()
        for r in results:
            w.writerow(r)


if __name__ == "__main__":
    main()
