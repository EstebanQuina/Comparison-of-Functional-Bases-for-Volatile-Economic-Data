# Cadenas de búsqueda — sintaxis arXiv (Fase 4)

**Protocolo de referencia:** `protocolo_estado_del_arte.md`, §5–§6
**Cadenas congeladas en Scopus (base para esta traducción):** `cadenas_scopus.md`
**Fuentes de información:** `fuentes_informacion.md` (v1.2)
**Bitácora de ejecución:** `bitacora_busqueda.numbers`

## Sintaxis y herramienta

arXiv tiene una **API pública** bien documentada
(`http://export.arxiv.org/api/query`), a diferencia de IDEAS/RePEc.
Sintaxis de `search_query`:

- Campos: `ti:` (título), `abs:` (resumen), `au:` (autor), `cat:`
  (categoría arXiv, ej. `stat.ME`, `math.ST`, `econ.EM`), `all:` (cualquier
  campo — equivalente a `TITLE-ABS-KEY`/`any:`).
- Operadores: `AND`, `OR`, `ANDNOT` (mayúsculas).
- Frase exacta: comillas `"..."`.
- Filtro de fecha: `submittedDate:[AAAAMMDD000000 TO AAAAMMDD235959]`.
- Paginación: `start` y `max_results` (recomendado ≤100 por solicitud;
  arXiv pide no más de 1 solicitud cada 3 segundos).

**Nota importante sobre cobertura:** arXiv es un repositorio de
*preprints*, no de libros ni de todas las revistas. Es esperable que las
obras de referencia general del conjunto oro (#1, #4, #6, #7 — todos
libros) **no** aparezcan aquí, independientemente de la cadena. Los
artículos de revista sí pueden tener versión preprint en arXiv, pero no
siempre — que un ítem no aparezca no implica automáticamente un problema
de la cadena, hay que verificar primero si el autor sube ese trabajo
específico a arXiv en absoluto.

Script reutilizable: [`scripts/arxiv_export.py`](scripts/arxiv_export.py)
— mismo patrón que `scripts/zbmath_export.py`, produce un `.ris` listo
para importar a Zotero. A diferencia de zbMATH, arXiv no tiene
restricciones de licencia sobre los metadatos — todos los registros
exportados vienen completos.

## C1 — PR1, PR2 — ✅ CONGELADA (2026-08-29, 298 resultados)

```
(all:"functional data analysis" OR all:"functional data" OR all:"functional principal component" OR all:FPCA) AND (all:basis OR all:spline OR all:Fourier OR all:wavelet) AND submittedDate:[19970101000000 TO 20261231235959]
```

**Ancla confirmada: #9a recuperado** (mismo título exacto verificado en
Scopus/zbMATH: "Homogeneity problem for basis expansion of functional
data with applications to resistive memories" — nota: la fecha de envío a
arXiv, 2024, difiere de la fecha de publicación en la revista, 2021; esto
es normal, no un conflicto). #1, #4, #6, #7 no verificados individualmente
en esta primera cadena — esperable que estén ausentes por ser libros (ver
nota de cobertura arriba). #9b y #9c no aparecieron en una revisión rápida
de los resultados por autor. Sin filtro de volumen (bajo 600). Exportado
vía `scripts/arxiv_export.py`: 298 total, todos con metadatos completos
(sin restricciones de licencia, a diferencia de zbMATH).

## C2–C7

Pendientes. Mismo procedimiento: probar vía `scripts/arxiv_export.py`,
revisar recall contra el subconjunto arXiv-específico (verificando
primero cobertura — libros ausentes por diseño del repositorio), ajustar,
y congelar.
