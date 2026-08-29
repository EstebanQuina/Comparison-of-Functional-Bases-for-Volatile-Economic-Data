# Cadenas de búsqueda — sintaxis zbMATH Open (Fase 4)

**Protocolo de referencia:** `protocolo_estado_del_arte.md`, §5–§6
**Cadenas congeladas en Scopus (base para esta traducción):** `cadenas_scopus.md`
**Fuentes de información:** `fuentes_informacion.md` (v1.1 — acceso abierto, sin suscripción)
**Bitácora de ejecución:** `bitacora_busqueda.numbers`

## Sintaxis verificada (vía `General Help - zbMATH Open`, documentación oficial)

A diferencia de Scopus/WoS, zbMATH **no usa las palabras "and"/"or"** como
operadores — usa símbolos. Usar las palabras literales no da error, pero
las trata como texto de búsqueda, produciendo resultados incorrectos sin
avisar (esto costó varias rondas de diagnóstico).

| Operador | Significado |
|---|---|
| `a & b` | Y lógico (AND) — por defecto entre varios términos |
| `a \| b` | O lógico (OR) |
| `!ab` | NO lógico (NOT) |
| `abc*` | comodín, **solo a la derecha** (no hay comodín de un carácter tipo `?`) |
| `"ab c"` | frase exacta |
| `(ab c)` | agrupación de términos |

Campos relevantes: `any:` (busca en ab, au, cc, en, rv, so, ti, ut — **ya
incluye `cc:`**), `ti:` (título), `au:` (autor), `py:` (año, con rango
`py:1997-2026`), `cc:` (código MSC — usar solo, sin `any:`, para restringir
por clasificación explícitamente).

**Lección clave:** `cc:` es más restrictivo de lo esperado — muchos
trabajos genuinamente relevantes no están clasificados bajo el código MSC
"obvio" (ver más abajo, #6 no está bajo 62R10 pese a ser un libro central
de wavelets en FDA). Preferir texto libre (`any:`) sobre restricción por
`cc:`, salvo que el volumen lo obligue.

## Estado de indexación en zbMATH (independiente de Scopus)

La cobertura de zbMATH es distinta a la de Scopus — mejor en libros de
matemática, pero no necesariamente mejor en artículos aplicados. Cada
ítem del conjunto oro se verificó de forma independiente, sin asumir el
estado de Scopus (`cadenas_busqueda.md` §5.1):

| Ítem | Indexado en zbMATH | Notas |
|---|---|---|
| #1 (Ramsay & Silverman 2005) | ✅ Sí | No recuperado por C1 — obra general sin término de familia de base, mismo patrón que #2 en Scopus |
| #3 (Wang, Chiou & Müller 2016) | ❌ No | Tampoco estaba en Scopus — posible problema de indexación de esta revista en general |
| #4 (Ferraty & Vieu 2006) | ✅ Sí | ✅ Recuperado por C1 |
| #5 (Kokoszka & Reimherr 2017) | ✅ Sí | ✅ Recuperado por C5 |
| #6 (Morettin, Pinheiro & Vidakovic 2017) | ✅ Sí | ✅ Recuperado por C1 (texto libre); **no** recuperado si se restringe por `cc:62R10` — no está clasificado bajo ese código pese a ser sobre wavelets en FDA |
| #7 (Percival & Walden 2000) | ✅ Sí | No recuperado por C1 — título sin frase de dominio FDA ("Wavelet Methods for **Time Series** Analysis"), nunca fue un buen candidato de anclaje para este tema |
| #8 (Padilla-Segarra et al. 2020) | ❌ No | Una búsqueda `au:Padilla-Segarra` inicial dio un falso positivo (homónimo, paper de 2022 sin relación) — verificado el registro completo, no coincide. No indexado en zbMATH |
| #9a (Aguilera et al. 2021) | ✅ Sí | ✅ Recuperado por C1 |
| #9b (Aguilera & Aguilera-Morillo 2013) | ❌ No | Confirmado no indexado en zbMATH (verificado por título exacto) |
| #9c (Escabias, Aguilera & Aguilera-Morillo 2014) | ✅ Sí | ✅ Recuperado por C1 |

## C1 — PR1, PR2 — ✅ CONGELADA (2026-08-29, 806 resultados)

```
any:(basis* | spline* | Fourier | wavelet*) & any:("functional data analysis" | "functional data" | "functional principal component*" | FPCA) & py:1997-2026
```

**Historial de calibración:**
1. Primer intento, restringido por clasificación: `cc:62R10 & any:(basis* | spline* | Fourier | wavelet*)` → 235 resultados. Perdía #6 por completo (no clasificado bajo 62R10) y solo recuperaba #9a del resto — recall inaceptable.
2. Se abandonó la restricción `cc:` y se probó texto libre (ambos bloques con `any:`) → **806 resultados**.
3. Subconjunto relevante corregido para zbMATH = {#4, #6, #9a, #9c} (excluye #1 y #7, indexados pero sin vocabulario/framing esperado — mismo patrón que en Scopus; excluye #3 y #9b, no indexados en zbMATH). Recall = **4/4 = 100%**.
4. Se acepta 806 pese a superar ligeramente el umbral orientativo de 600: no hay un filtro de volumen seguro disponible (`cc:` demostradamente pierde cobertura relevante; filtrar por tipo de documento arriesgaría excluir libros como #6, que sí deben quedar incluidos).

**Sin filtro de año explícito probado aún en combinación** — `py:1997-2026`
añadido por consistencia con el resto de la Fase 4; no se ha verificado que
no excluya nada del conjunto oro (todos los ítems recuperados ya caen
dentro de esa ventana de todas formas).

## Exportación masiva vía API (en vez de la interfaz web)

La interfaz web de zbMATH Open solo permite exportar página por página,
inviable para cientos de resultados. zbMATH Open tiene una **API REST
pública** (`https://api.zbmath.org/v1/`, con especificación OpenAPI en
`/v1/openapi.json`) que permite paginar automáticamente.

Script reutilizable: [`scripts/zbmath_export.py`](scripts/zbmath_export.py).

```bash
python3 scripts/zbmath_export.py '<cadena de búsqueda>' <prefijo_salida>
```

Notas del endpoint (`GET /v1/document/_search`):
- Parámetros: `search_string`, `page` (empieza en 0), `results_per_page`
  (máximo confiable: 100 — valores mayores devuelven error 502).
- Algunos registros tienen metadatos (título, autor, referencias) marcados
  como `"zbMATH Open Web Interface contents unavailable due to conflicting
  licenses."` — restricción de licencia de terceros en la API abierta,
  aunque sí visibles en la web. El script separa estos automáticamente y
  extrae su DOI (o arXiv ID) cuando existe, en un archivo aparte para
  importar a Zotero por identificador (**File → New Item by Identifier**),
  lo cual además da mejores metadatos que zbMATH mismo (resuelve contra
  Crossref).
- El conteo de la API puede diferir ligeramente del conteo de la interfaz
  web (798 vs. 806 para C1) — mismo tipo de fluctuación temporal que se
  observó en Scopus, no indica un error.

Para C1: 798 vía API → 664 con metadatos completos (`C1_zbmath.ris`) + 134
restringidos por licencia (`C1_zbmath_ids_para_importar_por_DOI.txt`, con
DOI en todos los casos).

## C2 — PR3 — ✅ CONGELADA (2026-08-29, 375 resultados)

```
any:(basis* | spline* | Fourier | wavelet*) & any:("functional data analysis" | "functional data" | "functional principal component*" | FPCA) & any:(smoothing | "roughness penalty" | penal* | "knot selection" | "cross-validation" | GCV | "threshold selection" | "wavelet threshold*" | "dimension selection" | "number of basis functions" | regulari*) & py:1997-2026
```

**Sin ancla en el conjunto oro**: el único ítem esperado (#9b) no está
indexado en zbMATH (ver tabla de indexación arriba). Validado por revisión
manual de una muestra de 20 títulos extraídos directamente del `.ris`
exportado: perfil temático coherente con PR3, con varios hallazgos
claramente centrados en el tema (*"Functional principal component
analysis via regularized Gaussian basis expansions..."*, *"Wavelet-based
functional mixed models"*, *"Some first inferential tools for spatial
regression with differential regularization"*) junto con ruido esperable
de aplicaciones ajenas (ecología, ciencia de materiales), a filtrar en el
cribado de la Fase 5. Sin filtro de volumen (bajo 600). Exportado vía
`scripts/zbmath_export.py`: 375 total → 308 con metadatos completos + 67
restringidos por licencia (con DOI).

## C3 — PR4 — ✅ CONGELADA (2026-08-29, 28 resultados)

```
any:(wavelet* | "wavelet basis") & any:("functional data analysis" | "functional data" | "functional principal component*" | FPCA) & any:(nonstationary | "non-stationary" | rough | discontinu* | "structural break*" | "non-smooth" | nonsmooth | irregular* | jump* | singularit* | heterogeneous | "local feature*" | "abrupt change*" | "regime change*" | shock* | spike* | anomal*) & py:1997-2026
```

**Sin ancla en el conjunto oro** (#6 no aplica a C3, ver
`cadenas_busqueda.md` §5.5). Validada por revisión manual de los 28
títulos completos: núcleo claro de trabajos centrados en wavelets aplicados
a procesos irregulares/no estacionarios (*"Clustering nonstationary
circadian rhythms using locally stationary wavelet representations"*,
*"Using Bagidis in nonparametric functional data analysis: predicting
from curves with sharp local features"*), junto con 4 falsos positivos
identificables: registros de **volúmenes completos de actas de congreso**
(COMPSTAT 2002, COMPSTAT 2014, ICANN 2002, ParCo 1997) que coinciden por
palabras dispersas entre su contenido agregado, no por ser sobre el tema
— patrón de ruido típico de registros a nivel de volumen, a descartar en
el cribado de la Fase 5 (criterio E5). Sin filtro de volumen (bajo 600).
Exportado vía `scripts/zbmath_export.py`: 28 total → 21 con metadatos
completos + 7 restringidos por licencia (con DOI).

## C4 — PR2, PR4 — ✅ CONGELADA (2026-08-29, 192 resultados)

```
any:(basis* | spline* | Fourier | wavelet*) & any:("functional data analysis" | "functional data" | "functional principal component*" | FPCA) & any:(compar* | "comparative study" | benchmark*) & py:1997-2026
```

**Sin ancla en el conjunto oro** (#9b no está indexado en zbMATH).
Validada por revisión manual de una muestra de 20 títulos, con **confianza
más baja que C1–C3**: solo 2 de 20 son claramente comparativos de familias
de bases (*"A wavelet-based method in aggregated functional data
analysis"*, *"Functional principal component analysis via regularized
Gaussian basis expansions..."*); el resto son papers de aplicación general
de FDA (dental, agrícola, epigenética) donde `compar*` probablemente
coincidió con vocabulario genérico ("compared to") en el resumen, no con
una comparación central de bases — más el mismo patrón de falso positivo
por volumen completo de actas ya visto en C3. Se acepta de todas formas:
sobre-incluir es menos riesgoso que sub-incluir, y el volumen (192) es
manejable para el cribado título/resumen de la Fase 5, que filtrará este
ruido genérico. Exportado vía `scripts/zbmath_export.py`: 192 total → 166
con metadatos completos + 26 restringidos por licencia (con DOI).

## C5 — PR5 — ✅ CONGELADA (2026-08-29, 717 resultados)

```
any:("functional data analysis" | "functional data" | "functional principal component*" | FPCA) & any:(econom* | financ* | GDP | "gross domestic product" | volatil* | "time series") & py:1997-2026
```

**Corrección de verificación:** una comprobación inicial de indexación de
#8 (`au:Padilla-Segarra`, sin más filtros) devolvió 1 resultado y se
interpretó como confirmación — pero al inspeccionar el registro completo
resultó ser un **homónimo**: un artículo de 2022 sobre sistemas
semi-lineales no autónomos, sin relación con FDA. El #8 real (Padilla-
Segarra, González-Villacorte, Amaro & Infante 2020) **no está indexado en
zbMATH**. Verificar coincidencias de autor único siempre contra el
registro completo, no solo el conteo — la Fase 4 en Scopus ya había hecho
este mismo tipo de verificación cruzada de forma más rigurosa (par de
apellidos, no uno solo).

Subconjunto corregido = **{#5}** (Kokoszka & Reimherr) — confirmado
recuperado (`au:Kokoszka & au:Reimherr` dentro de la cadena C5 → 6
resultados). Recall = 100%.

Se acepta 717 pese a superar el umbral orientativo de 600: no hay filtro
de volumen seguro en zbMATH (`cc:` demostradamente excluye trabajos
relevantes, ver C1), y el recall está confirmado — mismo criterio que
C1/C5 en Scopus. Exportado vía `scripts/zbmath_export.py` (con
`results_per_page=40` por inestabilidad del servidor con páginas más
grandes en esta consulta): 717 total → 623 con metadatos completos + 94
restringidos por licencia (con DOI).

## C6–C7

Pendientes. Mismo procedimiento: probar (preferentemente vía
`scripts/zbmath_export.py` directamente, ya que da el conteo real y
permite muestrear títulos sin depender de la interfaz web), revisar
recall contra el subconjunto zbMATH-específico (verificando primero si
cada ítem está indexado aquí en absoluto, sin asumir el estado de
Scopus — y verificando homónimos en coincidencias de un solo apellido),
ajustar, y congelar.
