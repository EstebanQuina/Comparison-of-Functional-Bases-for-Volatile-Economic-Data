#!/usr/bin/env python3
"""Normalize the free-text familia_base / criterio_seleccion_dimension
fields of the extraction matrix into the coarse categories the protocol
expects, and build Tabla B (§11.2) as a cross-tab.

Usage: python3 build_tabla_b.py
Reads: f8_matriz_extraccion.csv
Writes: tabla_b_normalizada.csv (long format: familia,criterio,n),
        _tabla_b_data.json (raw counters + list of multi-family items)
"""
import csv
import json
from collections import Counter


def normalize_family(s):
    low = s.lower()
    if low.startswith("n/a") or low.startswith("no reportad") or low.startswith("no confirmad"):
        return set(), "sin_dato"
    found = set()
    if "b-spline" in low or "bspline" in low:
        found.add("B-spline")
    if "p-spline" in low:
        found.add("P-spline")
    if "fourier" in low:
        found.add("Fourier")
    if "wavelet" in low:
        found.add("wavelet")
    if "empíric" in low or "empiric" in low or "karhunen" in low or "fpca" in low:
        found.add("empírica")
    if "rbf" in low or "gaussian" in low or "radial" in low:
        found.add("RBF")
    if "spline" in low and not found & {"B-spline", "P-spline"}:
        found.add("B-spline")
    if not found:
        return set(), "otra"
    return found, ("multi" if len(found) > 1 else "unica")


def normalize_criterio(s):
    low = s.lower()
    if "gcv" in low:
        return "GCV"
    if "aic" in low or "bic" in low or "fpe" in low or "gic" in low:
        return "AIC/BIC/GIC"
    if any(k in low for k in ("bayesian", "bayesiano", "mcmc", "vem", "gibbs", "posterior", "prior")):
        return "bayesiano"
    if any(k in low for k in ("validaci", "cruzada", " cv", "bootstrap")):
        return "validación cruzada / bootstrap"
    if "varianza" in low or "cpv" in low:
        return "umbral de varianza explicada"
    if "no aplica" in low:
        return "no aplica"
    if "no reportado" in low or "no confirmado" in low:
        return "no reportado/confirmado"
    if any(k in low for k in ("fijo", "arbitrari", "manual", "visual")):
        return "fijo/arbitrario/manual"
    return "otro criterio propio"


def main():
    with open("f8_matriz_extraccion.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    fam_counter, crit_counter, tabla_b = Counter(), Counter(), Counter()
    multi_fam_items = []

    for r in rows:
        fams, kind = normalize_family(r["familia_base"])
        crit = normalize_criterio(r["criterio_seleccion_dimension"])
        crit_counter[crit] += 1
        if kind == "multi":
            multi_fam_items.append((r["id"], r["clave_bibtex"], sorted(fams)))
            label = "MÚLTIPLE (comparación explícita)"
        elif kind == "unica":
            label = list(fams)[0]
        else:
            label = kind
        fam_counter[label] += 1
        tabla_b[(label, crit)] += 1

    with open("tabla_b_normalizada.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["familia_base", "criterio_seleccion_dimension", "n"])
        for (fam, crit), n in sorted(tabla_b.items(), key=lambda x: -x[1]):
            w.writerow([fam, crit, n])

    with open("_tabla_b_data.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "fam_counter": dict(fam_counter),
                "crit_counter": dict(crit_counter),
                "tabla_b": {f"{k[0]}||{k[1]}": v for k, v in tabla_b.items()},
                "multi_fam_items": multi_fam_items,
            },
            f,
            ensure_ascii=False,
            indent=1,
        )

    print("Distribución familia_base:")
    for k, v in fam_counter.most_common():
        print(f"  {k:35s} {v}")
    print(f"\n{len(multi_fam_items)} ítems con comparación múltiple de familias")


if __name__ == "__main__":
    main()
