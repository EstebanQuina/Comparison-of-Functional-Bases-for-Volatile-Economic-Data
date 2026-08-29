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

## C2 — PR3 — ✅ CONGELADA (2026-08-29, 137 resultados)

```
(all:"functional data analysis" OR all:"functional data" OR all:"functional principal component" OR all:FPCA) AND (all:basis OR all:spline OR all:Fourier OR all:wavelet) AND (all:smoothing OR all:"roughness penalty" OR all:penalized OR all:penalised OR all:"knot selection" OR all:"cross-validation" OR all:GCV OR all:"threshold selection" OR all:"dimension selection" OR all:regularization OR all:regularisation) AND submittedDate:[19970101000000 TO 20261231235959]
```

**Sin ancla en el conjunto oro**: se verificó directamente que **#9b no
está indexado en arXiv** (0 resultados en búsqueda por título exacto,
independiente de la cadena) — parece que ese trabajo de 2013 nunca se
subió a ningún repositorio. Validado por revisión manual de una muestra
de 15 títulos: perfil temático fuerte y coherente con PR3 (*"Fast
Bayesian Basis Selection for Functional Data Representation with
Correlated Errors"*, *"...allowing for dimension selection"*,
*"Semiparametric Functional Factor Models with Bayesian Rank Selection"*,
*"Trend Filtering for Functional Data"*). Sin filtro de volumen (bajo
600). Exportado vía `scripts/arxiv_export.py`: 137 registros, todos con
metadatos completos.

## C3 — PR4 — ✅ CONGELADA (2026-08-29, 10 resultados)

```
(all:wavelet OR all:"wavelet basis") AND (all:"functional data analysis" OR all:"functional data" OR all:"functional principal component" OR all:FPCA) AND (all:nonstationary OR all:"non-stationary" OR all:rough OR all:discontinuous OR all:"structural break" OR all:"non-smooth" OR all:nonsmooth OR all:irregular OR all:jump OR all:singularity OR all:heterogeneous OR all:"local feature" OR all:"abrupt change" OR all:"regime change" OR all:shock OR all:spike OR all:anomaly) AND submittedDate:[19970101000000 TO 20261231235959]
```

**Sin ancla en el conjunto oro** (mismo caso que en las otras bases).
Validada por revisión manual de los 10 títulos completos: 5–6 claramente
relevantes, incluyendo dos que ya habían aparecido como relevantes en la
muestra de C3 en zbMATH (*"Clustering nonstationary circadian rhythms
using locally stationary wavelet representations"*, *"Feature Extraction
for Functional Time Series: Theory and Application to NIR Spectroscopy
Data"*) — buena señal de consistencia entre bases. Resto es ruido
esperable (análisis de espectro de hardware, ajuste de redes). Sin filtro
de volumen (muy bajo 600). Exportado vía `scripts/arxiv_export.py`: 10
registros, todos con metadatos completos.

## C4 — PR2, PR4 — ✅ CONGELADA (2026-08-29, 85 resultados; confianza más baja)

```
(all:"functional data analysis" OR all:"functional data" OR all:"functional principal component" OR all:FPCA) AND (all:basis OR all:spline OR all:Fourier OR all:wavelet) AND (all:comparative OR all:compare OR all:comparison OR all:benchmark) AND submittedDate:[19970101000000 TO 20261231235959]
```

**Sin ancla en el conjunto oro.** Mismo patrón de confianza más baja que
en zbMATH C4: de una muestra de 15 títulos, solo ~4 son claramente sobre
comparación de familias de bases (*"Fast Bayesian Basis Selection for
Functional Data Representation..."*, *"...additive penalty in
P-splines"*, *"A wavelet-based method in aggregated functional data
analysis"*, *"Penalized likelihood estimation... using compositional
splines"*); el resto es FDA general donde `comparative/compare/comparison`
probablemente coincidió de forma genérica en el resumen. Se acepta con el
mismo criterio: sobre-incluir es menos riesgoso que sub-incluir, y el
volumen (85) es manejable para el cribado de la Fase 5. Exportado vía
`scripts/arxiv_export.py`: 85 registros, todos con metadatos completos.

## C5 — PR5 — ✅ CONGELADA (2026-08-29, 235 resultados)

```
(all:"functional data analysis" OR all:"functional data" OR all:"functional principal component" OR all:FPCA) AND (all:economic OR all:economics OR all:financial OR all:GDP OR all:"gross domestic product" OR all:volatility OR all:"time series") AND submittedDate:[19970101000000 TO 20261231235959]
```

**Sin ancla en el conjunto oro**, verificado directamente: #5 (Kokoszka &
Reimherr) no tiene el libro en arXiv (sí tienen 3 papers conjuntos, pero
no *Introduction to Functional Data Analysis*), y #8 (Padilla-Segarra)
solo devuelve el mismo homónimo de ecuaciones diferenciales ya detectado
en zbMATH — confirmado que el #8 real no está en arXiv. Validado por
revisión manual de una muestra de 20 títulos: al menos 5 claramente
económico-financieros (*"Dynamic functional time-series forecasts of
foreign exchange implied volatility surfaces"*, *"A Statistical Machine
Learning Approach to Yield Curve Forecasting"*, *"Inference for Model
Misspecification in Interest Rate Term Structure..."*, *"Bayesian Spatial
Homogeneity Pursuit of Functional Data: an Application to the U.S. Income
Distribution"*), con ruido esperable de otros dominios (astronomía,
ecología, medicina) donde "time series" coincidió genéricamente. Sin
filtro de volumen (bajo 600). Exportado vía `scripts/arxiv_export.py`:
235 registros, todos con metadatos completos.

## C6 — PR5 — ✅ CONGELADA (2026-08-29, 9 resultados)

```
(all:"functional data analysis" OR all:"functional data" OR all:"functional principal component" OR all:FPCA) AND (all:"Latin America" OR all:Ecuador OR all:"South America" OR all:Argentina OR all:Bolivia OR all:Brazil OR all:Chile OR all:Colombia OR all:"Costa Rica" OR all:Cuba OR all:"Dominican Republic" OR all:"El Salvador" OR all:Guatemala OR all:Haiti OR all:Honduras OR all:Mexico OR all:Nicaragua OR all:Panama OR all:Paraguay OR all:Peru OR all:Uruguay OR all:Venezuela) AND submittedDate:[19970101000000 TO 20261231235959]
```

**Sin ancla en el conjunto oro.** Volumen muy bajo, esperable (repositorio
de matemática/estadística/CS, poca aplicación regional). Validado por
revisión manual de los 9 títulos completos: un hallazgo claramente fuerte
(*"Modeling the Evolution of Infectious Diseases with Functional Data
Models: The Case of COVID-19 in Brazil"*), el mismo tipo de trabajo que
ya había aparecido como relevante en zbMATH C6 — buena consistencia entre
bases. El resto probablemente coincidió por mención de país como ejemplo
de aplicación en el resumen; un ítem parece ruido claro
("Towards proactive self-adaptive AI for non-stationary environments...").
Sin filtro de volumen (muy bajo 600). Exportado vía
`scripts/arxiv_export.py`: 9 registros, todos con metadatos completos.

## C7 — PR4, PR5 — ✅ CONGELADA (2026-08-29, 38 resultados)

```
(all:"functional time series" OR all:"functional ARCH" OR all:"functional GARCH" OR all:"functional version") AND (all:volatility OR all:economic OR all:financial OR all:heteroskedastic OR all:heteroscedastic) AND submittedDate:[19970101000000 TO 20261231235959]
```

**Ancla confirmada: #10 recuperado al 100%** (arXiv:1105.0343, título
"A Functional Version of the ARCH Model"). Traducción directa de la
sintaxis ya calibrada en Scopus/zbMATH, sin ajuste adicional necesario.
Sin filtro de volumen (bajo 600). Exportado vía `scripts/arxiv_export.py`:
38 registros, todos con metadatos completos.

## Con esto se completan las siete cadenas de arXiv

| Cadena | Resultados | Ancla | Confianza |
|---|---|---|---|
| C1 | 298 | {#9a} | Alta |
| C2 | 137 | Sin ancla, validada manualmente | Alta |
| C3 | 10 | Sin ancla, validada manualmente | Alta |
| C4 | 85 | Sin ancla, validada manualmente | **Baja** (ver nota en C4) |
| C5 | 235 | Sin ancla, validada manualmente | Alta |
| C6 | 9 | Sin ancla, validada manualmente | Alta |
| C7 | 38 | {#10} 100% | Alta |

**Total bruto: 812 registros** (con solapamiento esperado entre cadenas).
