# Cadenas de búsqueda — sintaxis Scopus (Fase 4)

**Protocolo de referencia:** `protocolo_estado_del_arte.md`, §5–§6
**Cadenas conceptuales (Bloques A–E):** `cadenas_busqueda.md`
**Bitácora de ejecución:** `bitacora_busqueda.numbers`

Instanciación de las siete cadenas conceptuales (C1–C7) en sintaxis de
Scopus Advanced Search (`TITLE-ABS-KEY`), listas para pegar. Todas incluyen
el filtro de ventana temporal 1997–2026 (`criterios_elegibilidad.md`, I3,
sin excepciones).

## C1 — PR1, PR2 — ✅ CONGELADA (2026-08-28, 871 resultados)

```
TITLE-ABS-KEY(("functional data analysis" OR "functional data" OR "functional principal component*" OR FPCA) AND ("basis function*" OR "basis system" OR "basis expansion" OR "basis selection" OR "B-spline*" OR "P-spline*" OR spline* OR Fourier OR wavelet*)) AND PUBYEAR > 1996 AND PUBYEAR < 2027
```

**Filtros adicionales aplicados en Scopus (fuera de la cadena de texto):**
- Subject area: Mathematics; Economics, Econometrics and Finance; Decision Sciences
- Document type: Article, Review, Conference Paper, Book Chapter, Book

**Historial de calibración:** 1243 (sin filtros) → 876 (+ área temática) → 871
(+ tipo de documento). Recuperación del subconjunto relevante del conjunto
oro (#6, #9a–c) confirmada al 100% en las dos primeras ejecuciones. Se
acepta 871 pese a superar el umbral orientativo de ~600 (§5.4): el filtro
de tipo de documento solo retiró 5 registros, señal de que el volumen no
es ruido editorial sino el alcance real y esperado de la cadena más amplia
del conjunto (A AND B, sin restricción adicional). El recorte adicional se
delega al cribado título/resumen de la Fase 5. Ver `bitacora_busqueda.numbers`
filas 1–3 para el detalle completo.

## C2 — PR3

```
TITLE-ABS-KEY(("functional data analysis" OR "functional data" OR "functional principal component*" OR FPCA) AND ("basis function*" OR "basis system" OR "basis expansion" OR "basis selection" OR "B-spline*" OR "P-spline*" OR spline* OR Fourier OR wavelet*) AND (smoothing OR "roughness penalty" OR penalized OR "knot selection" OR "generalized cross-validation" OR GCV)) AND PUBYEAR > 1996 AND PUBYEAR < 2027
```

## C3 — PR4

```
TITLE-ABS-KEY(("functional data analysis" OR "functional data" OR "functional principal component*" OR FPCA) AND (wavelet* OR "wavelet basis") AND (nonstationary OR "non-stationary" OR rough OR discontinu*)) AND PUBYEAR > 1996 AND PUBYEAR < 2027
```

## C4 — PR2, PR4

```
TITLE-ABS-KEY(("functional data analysis" OR "functional data" OR "functional principal component*" OR FPCA) AND ("basis function*" OR "basis system" OR "basis expansion" OR "basis selection" OR "B-spline*" OR "P-spline*" OR spline* OR Fourier OR wavelet*) AND (compar* OR "comparative study" OR benchmark*)) AND PUBYEAR > 1996 AND PUBYEAR < 2027
```

## C5 — PR5

```
TITLE-ABS-KEY(("functional data analysis" OR "functional data" OR "functional principal component*" OR FPCA) AND (econom* OR financ* OR GDP OR "gross domestic product" OR volatil* OR "time series")) AND PUBYEAR > 1996 AND PUBYEAR < 2027
```

## C6 — PR5

```
TITLE-ABS-KEY(("functional data analysis" OR "functional data" OR "functional principal component*" OR FPCA) AND ("Latin America*" OR Ecuador OR "South America*")) AND PUBYEAR > 1996 AND PUBYEAR < 2027
```

## C7 — PR4, PR5

```
TITLE-ABS-KEY(("functional time series" OR "functional ARCH" OR "functional GARCH") AND (volatil* OR econom*)) AND PUBYEAR > 1996 AND PUBYEAR < 2027
```

## Procedimiento de ejecución

1. Pega una cadena a la vez en Scopus Advanced Search.
2. Verifica qué proporción del conjunto oro (`cadenas_busqueda.md` §5.1)
   recupera la cadena. Si es menor al 80%, amplía sinónimos en el bloque
   correspondiente y repite antes de congelar.
3. Si una cadena devuelve más de ~600 resultados, restringe por área
   temática en el panel lateral de Scopus (el campo de búsqueda ya está
   limitado a título/resumen/palabras clave por `TITLE-ABS-KEY`).
4. Exporta en formato RIS (botón "Export" → RIS, **no** "Citation" ni
   "Plain text") únicamente la **versión congelada** de cada cadena — las
   ejecuciones de calibración (sin filtro, con filtros parciales) no se
   exportan, solo se registran en la bitácora para dejar constancia del
   proceso de calibración.
5. Registra cada ejecución en `bitacora_busqueda.numbers`: cadena exacta
   pegada, campo (`TITLE-ABS-KEY`), filtros aplicados, número de
   resultados, número exportado, y el nombre del archivo RIS generado.
