#!/usr/bin/env python3
"""Check open-access availability (Unpaywall, then Semantic Scholar
openAccessPdf as fallback) for the included items of Etapa 1, ahead of
Etapa 2 (texto completo) full-text acquisition.

Usage: python3 check_oa_access.py
Reads: decisions_master.csv (decision==include), library_enriched.json (doi)
Writes: oa_status.csv
"""
import csv
import json
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

CONTACT_EMAIL = "estebanquinia@gmail.com"


def unpaywall_check(doi):
    url = f"https://api.unpaywall.org/v2/{urllib.request.quote(doi)}?email={CONTACT_EMAIL}"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                d = json.load(resp)
            best = d.get("best_oa_location") or {}
            return {
                "is_oa": d.get("is_oa", False),
                "oa_url": best.get("url_for_pdf") or best.get("url"),
                "host_type": best.get("host_type"),
                "version": best.get("version"),
            }
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return {"is_oa": False, "oa_url": None, "host_type": None, "version": None}
            time.sleep(3 * (attempt + 1))
        except Exception:
            time.sleep(2 * (attempt + 1))
    return {"is_oa": None, "oa_url": None, "host_type": None, "version": None}


def s2_batch_oa(dois):
    result = {}
    for i in range(0, len(dois), 500):
        chunk = dois[i : i + 500]
        ids = [f"DOI:{d}" for d in chunk]
        req = urllib.request.Request(
            "https://api.semanticscholar.org/graph/v1/paper/batch?fields=isOpenAccess,openAccessPdf",
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
                print(f"  S2 batch HTTP {e.code}, waiting {wait}s")
                time.sleep(wait)
            except Exception as e:
                time.sleep(10 * (attempt + 1))
        if data is None:
            data = [None] * len(chunk)
        for doi, item in zip(chunk, data):
            if item:
                pdf = item.get("openAccessPdf") or {}
                result[doi] = {"is_oa": item.get("isOpenAccess"), "oa_url": pdf.get("url")}
            else:
                result[doi] = {"is_oa": None, "oa_url": None}
        print(f"  S2 OA batch {i}-{i+len(chunk)}: done")
        time.sleep(4)
    return result


def main():
    with open("decisions_master.csv", newline="", encoding="utf-8") as f:
        decisions = {int(r["id"]): r for r in csv.DictReader(f)}
    included_ids = [i for i, r in decisions.items() if r["decision"] == "include"]
    print(f"Ítems incluidos (Etapa 1): {len(included_ids)}")

    with open("library_enriched.json", encoding="utf-8") as f:
        library = {e["id"]: e for e in json.load(f)}

    with_doi = [(i, library[i]["doi"]) for i in included_ids if library.get(i) and library[i].get("doi")]
    without_doi = [i for i in included_ids if not (library.get(i) and library[i].get("doi"))]
    print(f"Con DOI: {len(with_doi)} | sin DOI: {len(without_doi)}")

    print("\nConsultando Unpaywall (concurrente, 10 workers)...")
    up_results = {}
    dois = [d for _, d in with_doi]
    with ThreadPoolExecutor(max_workers=10) as ex:
        futs = {ex.submit(unpaywall_check, d): d for d in dois}
        done = 0
        for fut in as_completed(futs):
            d = futs[fut]
            up_results[d] = fut.result()
            done += 1
            if done % 200 == 0:
                print(f"  Unpaywall {done}/{len(dois)}")

    unpaywall_misses = [d for d in dois if not up_results[d]["is_oa"]]
    print(f"\nUnpaywall: {len(dois) - len(unpaywall_misses)} OA / {len(unpaywall_misses)} no-OA o desconocido")

    print("\nFallback Semantic Scholar sobre los misses de Unpaywall...")
    s2_results = s2_batch_oa(list(dict.fromkeys(unpaywall_misses)))

    rows = []
    n_oa_up = n_oa_s2 = n_no_oa = 0
    for i, doi in with_doi:
        up = up_results[doi]
        if up["is_oa"]:
            rows.append({"id": i, "doi": doi, "is_oa": True, "source": "unpaywall", "oa_url": up["oa_url"], "host_type": up["host_type"]})
            n_oa_up += 1
        else:
            s2 = s2_results.get(doi, {})
            if s2.get("is_oa"):
                rows.append({"id": i, "doi": doi, "is_oa": True, "source": "semantic_scholar", "oa_url": s2.get("oa_url"), "host_type": None})
                n_oa_s2 += 1
            else:
                rows.append({"id": i, "doi": doi, "is_oa": False, "source": None, "oa_url": None, "host_type": None})
                n_no_oa += 1

    for i in without_doi:
        rows.append({"id": i, "doi": None, "is_oa": False, "source": None, "oa_url": None, "host_type": "sin_doi"})

    with open("oa_status.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "doi", "is_oa", "source", "oa_url", "host_type"])
        w.writeheader()
        for r in sorted(rows, key=lambda r: r["id"]):
            w.writerow(r)

    total = len(included_ids)
    total_oa = n_oa_up + n_oa_s2
    print(f"\n=== RESUMEN ===")
    print(f"Total incluidos: {total}")
    print(f"OA vía Unpaywall: {n_oa_up}")
    print(f"OA vía Semantic Scholar (fallback): {n_oa_s2}")
    print(f"Total con acceso abierto legal detectado: {total_oa} ({100*total_oa/total:.1f}%)")
    print(f"Sin DOI: {len(without_doi)}")
    print(f"Requieren otra vía (no-OA detectado, con DOI): {n_no_oa}")


if __name__ == "__main__":
    main()
