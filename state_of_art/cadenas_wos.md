# Cadenas de búsqueda — sintaxis Web of Science (Fase 4)

**Protocolo de referencia:** `protocolo_estado_del_arte.md`, §5–§6
**Cadenas congeladas en Scopus (base para esta traducción):** `cadenas_scopus.md`
**Bitácora de ejecución:** `bitacora_busqueda.numbers`

Traducción de sintaxis de las siete cadenas ya congeladas en Scopus a
Web of Science Advanced Search (`TS=`), lista para pegar. **Estas
cadenas están listas para PROBAR, no para asumir como congeladas** — cada
base de datos tiene cobertura distinta, así que hay que repetir el ciclo
de calibración completo (§5.4, y el registro de decisiones ya tomadas en
`cadenas_busqueda.md` §5.5) para cada una en WoS: ejecutar, revisar recall
del conjunto oro, ajustar filtros de volumen si hace falta, congelar y
recién ahí registrar en la bitácora y exportar.

Diferencias de sintaxis respecto a Scopus:
- `TS=` (Topic: título + resumen + palabras clave de autor + Keywords Plus)
  en vez de `TITLE-ABS-KEY( )`. Keywords Plus puede traer resultados
  adicionales que Scopus no tiene, porque se genera de las referencias
  citadas, no del propio resumen.
- `PY=1997-2026` en vez de `PUBYEAR > 1996 AND PUBYEAR < 2027`.
- Comodines iguales: `*` (truncamiento), `?` (un carácter exacto — sigue
  sirviendo para `regulari?ation`).
- Para filtro de volumen, la categorización de WoS ("Web of Science
  Categories") no es la misma taxonomía que las "Subject areas" de Scopus.
  Categorías candidatas equivalentes a probar si una cadena supera el
  umbral de ~600: **Mathematics, Applied**; **Mathematics**;
  **Statistics & Probability**; **Economics**; **Business, Finance**.

## C1 — PR1, PR2

```
TS=(("functional data analysis" OR "functional data" OR "functional principal component*" OR FPCA) AND ("basis function*" OR "basis system" OR "basis expansion" OR "basis selection" OR "B-spline*" OR "P-spline*" OR spline* OR Fourier OR wavelet*)) AND PY=1997-2026
```

## C2 — PR3

```
TS=(("functional data analysis" OR "functional data" OR "functional principal component*" OR FPCA) AND ("basis function*" OR "basis system" OR "basis expansion" OR "basis selection" OR "B-spline*" OR "P-spline*" OR spline* OR Fourier OR wavelet*) AND (smoothing OR "roughness penalty" OR penalized OR penalised OR "knot selection" OR "generalized cross-validation" OR "generalised cross-validation" OR GCV OR "cross-validation" OR "threshold selection" OR "wavelet threshold*" OR "dimension selection" OR "number of basis functions" OR regulari?ation)) AND PY=1997-2026
```

## C3 — PR4

```
TS=(("functional data analysis" OR "functional data" OR "functional principal component*" OR FPCA) AND (wavelet* OR "wavelet basis") AND (nonstationary OR "non-stationary" OR rough OR discontinu* OR "structural break*" OR "non-smooth" OR nonsmooth OR irregular* OR jump* OR singularit* OR heterogeneous OR "local feature*" OR "abrupt change*" OR "regime change*" OR shock* OR spike* OR anomal*)) AND PY=1997-2026
```

## C4 — PR2, PR4

```
TS=(("functional data analysis" OR "functional data" OR "functional principal component*" OR FPCA) AND ("basis function*" OR "basis system" OR "basis expansion" OR "basis selection" OR "B-spline*" OR "P-spline*" OR spline* OR Fourier OR wavelet*) AND (compar* OR "comparative study" OR benchmark*)) AND PY=1997-2026
```

## C5 — PR5

```
TS=(("functional data analysis" OR "functional data" OR "functional principal component*" OR FPCA) AND (econom* OR financ* OR GDP OR "gross domestic product" OR volatil* OR "time series")) AND PY=1997-2026
```

## C6 — PR5

```
TS=(("functional data analysis" OR "functional data" OR "functional principal component*" OR FPCA) AND ("Latin America*" OR Ecuador OR "South America*" OR Argentina OR Bolivia OR Brazil OR Chile OR Colombia OR "Costa Rica" OR Cuba OR "Dominican Republic" OR "El Salvador" OR Guatemala OR Haiti OR Honduras OR Mexico OR Nicaragua OR Panama OR Paraguay OR Peru OR Uruguay OR Venezuela)) AND PY=1997-2026
```

## C7 — PR4, PR5

```
TS=(("functional time series" OR "functional ARCH" OR "functional GARCH" OR "functional version") AND (volatil* OR econom* OR financ* OR heteroskedastic* OR heteroscedastic*)) AND PY=1997-2026
```

## Procedimiento de ejecución

1. Pega una cadena a la vez en Web of Science Advanced Search.
2. Verifica el recall del subconjunto relevante del conjunto oro para esa
   cadena, usando el mapeo ya corregido en `cadenas_busqueda.md` §5.5 (no
   el mapeo original del protocolo — ya se corrigió con evidencia real de
   Scopus). Ten en cuenta que la indexación de WoS es distinta a la de
   Scopus: un ítem no indexado en Scopus podría estarlo en WoS, y
   viceversa — vuelve a verificar cada uno, no asumas los resultados de
   Scopus.
3. Si el recall es bajo, sigue el mismo diagnóstico que en Scopus: primero
   sospecha de error de mapeo (¿el ítem falló también en varias cadenas de
   Scopus?) antes de ampliar vocabulario a ciegas.
4. Si una cadena supera ~600 resultados, restringe por categoría de WoS
   (ver equivalencias arriba) — verificando recall de nuevo después de
   filtrar.
5. Exporta en formato RIS (o BibTeX) únicamente la versión congelada de
   cada cadena, hacia una colección de Zotero nombrada `C{n}_WoS_{conteo}`.
6. Registra cada ejecución en `bitacora_busqueda.numbers` con
   `base_de_datos = Web of Science`.
