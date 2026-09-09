#!/usr/bin/env python3
"""Backfill missing abstracts for library_parsed.json using Semantic Scholar
(batch, by DOI) then Crossref (per-DOI, for S2 misses) as fallback.

Usage: python3 enrich_abstracts.py <in.json> <out.json>
"""
import sys
import json
import re
import time
import urllib.request
import urllib.error

CONTACT_EMAIL = "estebanquinia@gmail.com"


def strip_jats(s):
    return re.sub("<[^>]+>", " ", s).strip()


def s2_batch(dois):
    """Return {doi: abstract or None} for a list of DOIs, chunked at 500."""
    result = {}
    for i in range(0, len(dois), 500):
        chunk = dois[i : i + 500]
        ids = [f"DOI:{d}" for d in chunk]
        req = urllib.request.Request(
            "https://api.semanticscholar.org/graph/v1/paper/batch?fields=abstract",
            data=json.dumps({"ids": ids}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        data = None
        for attempt in range(6):
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = json.load(resp)
                break
            except urllib.error.HTTPError as e:
                wait = int(e.headers.get("Retry-After", 0)) if e.headers else 0
                wait = max(wait, 10 * (attempt + 1))
                print(f"  S2 batch HTTP {e.code} (attempt {attempt+1}), waiting {wait}s", file=sys.stderr)
                time.sleep(wait)
            except urllib.error.URLError as e:
                print(f"  S2 batch error (attempt {attempt+1}): {e}", file=sys.stderr)
                time.sleep(10 * (attempt + 1))
        if data is None:
            print(f"  S2 batch {i}-{i+len(chunk)}: GAVE UP after retries", file=sys.stderr)
            data = [None] * len(chunk)
        for doi, item in zip(chunk, data):
            result[doi] = item.get("abstract") if item else None
        print(f"  S2 batch {i}-{i+len(chunk)}: done")
        time.sleep(4)
    return result


def crossref_one(doi):
    url = f"https://api.crossref.org/works/{urllib.request.quote(doi)}"
    req = urllib.request.Request(
        url, headers={"User-Agent": f"thesis-review/1.0 (mailto:{CONTACT_EMAIL})"}
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                d = json.load(resp)
            ab = d.get("message", {}).get("abstract")
            return strip_jats(ab) if ab else None
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(5 * (attempt + 1))
        except Exception:
            time.sleep(2 * (attempt + 1))
    return None


def main(inp, outp):
    with open(inp, encoding="utf-8") as f:
        entries = json.load(f)

    need_doi = [e["doi"] for e in entries if not e["abstract"] and e["doi"]]
    need_doi = list(dict.fromkeys(need_doi))  # dedupe, preserve order
    print(f"Looking up {len(need_doi)} unique DOIs via Semantic Scholar...")
    s2_results = s2_batch(need_doi)

    s2_misses = [d for d, ab in s2_results.items() if not ab]
    print(f"S2 misses: {len(s2_misses)} -- trying Crossref...")
    cr_results = {}
    for j, doi in enumerate(s2_misses):
        cr_results[doi] = crossref_one(doi)
        if (j + 1) % 50 == 0:
            print(f"  Crossref {j+1}/{len(s2_misses)}")
        time.sleep(0.12)

    n_s2 = n_cr = n_none = 0
    for e in entries:
        if e["abstract"]:
            continue
        doi = e["doi"]
        if not doi:
            continue
        ab = s2_results.get(doi)
        if ab:
            e["abstract"] = ab
            e["abstract_source"] = "semantic_scholar"
            n_s2 += 1
            continue
        ab = cr_results.get(doi)
        if ab:
            e["abstract"] = ab
            e["abstract_source"] = "crossref"
            n_cr += 1
        else:
            n_none += 1

    with open(outp, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=1)

    total = len(entries)
    final_with_ab = sum(1 for e in entries if e["abstract"])
    print(f"\nRecovered via Semantic Scholar: {n_s2}")
    print(f"Recovered via Crossref: {n_cr}")
    print(f"Still missing (no DOI or not found): {total - final_with_ab}")
    print(f"Final coverage: {final_with_ab}/{total} ({100*final_with_ab/total:.1f}%)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
