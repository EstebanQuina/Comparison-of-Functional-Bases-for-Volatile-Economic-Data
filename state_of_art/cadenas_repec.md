# Cadenas de búsqueda — sintaxis IDEAS/RePEc (Fase 4)

**⏸ EXCLUIDA (2026-08-29):** IDEAS/RePEc queda fuera de la búsqueda
sistemática — sin API pública ni herramienta de exportación masiva o
individual (verificado en IDEAS y en su sitio hermano EconPapers), a
diferencia de zbMATH Open. Se probó C1 (376 resultados) antes de tomar
esta decisión; ver `fuentes_informacion.md` v1.2 para el detalle completo
de la exclusión. Este archivo queda como referencia por si en el futuro
aparece una vía de exportación viable.

**Protocolo de referencia:** `protocolo_estado_del_arte.md`, §5–§6
**Cadenas congeladas en Scopus (base para esta traducción):** `cadenas_scopus.md`
**Fuentes de información:** `fuentes_informacion.md` (v1.2 — IDEAS/RePEc excluida)
**Bitácora de ejecución:** `bitacora_busqueda.numbers`

## Aviso importante: sin API, sin exportación masiva

A diferencia de zbMATH Open, **IDEAS/RePEc no tiene una API pública** para
exportación automatizada. Además, al momento de preparar esto (2026-08-29)
el sitio está mostrando el aviso *"IDEAS is struggling with massive bot
traffic, please be patient"* — está limitando activamente el tráfico
automatizado. Por ambas razones, **no se debe intentar automatizar/scrapear
este sitio** (a diferencia de zbMATH, cuya API está pensada explícitamente
para uso programático). Las búsquedas y cualquier exportación deben hacerse
manualmente desde la interfaz web.

## Sintaxis verificada (vía el tutorial oficial del blog de RePEc)

Muy distinta a Scopus/WoS/zbMATH:

| Elemento | Sintaxis |
|---|---|
| AND | espacio entre palabras (implícito) |
| OR | `\|` (pipe), con paréntesis para agrupar: `(a \| b \| c)` |
| NOT / excluir | `~palabra` |
| Frase exacta | `"frase exacta"` |
| Comodines | **No existen** (`spline*` no funciona). En su lugar, IDEAS usa
  *stemming* algorítmico automático: buscar `count` también encuentra
  `counts`, `counting`, etc. — no es infalible, así que ante la duda usa
  `\|` para listar variantes en vez de confiar solo en el stemming. |
| Sinónimos | Diccionario propio de términos económicos (ej. `ML` también
  busca `maximum likelihood`) — no hace falta replicarlo a mano. |

**Filtros de la búsqueda avanzada** (`https://ideas.repec.org/search.html`):
tipo de documento (papers, articles, books, chapters, software, o todos),
campo de búsqueda (resumen, palabras clave, título, autor, o "whole record"
— el equivalente a `TITLE-ABS-KEY`/`any:`), año de inicio, año de fin.

## Cadenas propuestas (para pegar en el cuadro de búsqueda)

Sin comodines, confiando en el stemming automático para plurales
(`spline`→`splines`, `wavelet`→`wavelets`, etc.), y sin bloque de año en la
cadena misma — usar los selectores de año de la búsqueda avanzada
(1997–2026) en vez de escribirlo en el texto.

**C1 — PR1, PR2:**
```
("functional data analysis" | "functional data" | "functional principal component" | FPCA) (basis | spline | Fourier | wavelet)
```

**C2 — PR3:**
```
("functional data analysis" | "functional data" | "functional principal component" | FPCA) (basis | spline | Fourier | wavelet) (smoothing | "roughness penalty" | penalized | penalised | "knot selection" | "cross-validation" | GCV | "threshold selection" | "dimension selection" | regularization | regularisation)
```

**C3 — PR4:**
```
(wavelet | "wavelet basis") ("functional data analysis" | "functional data" | "functional principal component" | FPCA) (nonstationary | "non-stationary" | rough | discontinuous | "structural break" | "non-smooth" | irregular | jump | singularity | heterogeneous | "local feature" | "abrupt change" | "regime change" | shock | spike | anomaly)
```

**C4 — PR2, PR4:**
```
("functional data analysis" | "functional data" | "functional principal component" | FPCA) (basis | spline | Fourier | wavelet) (comparative | compare | comparison | benchmark)
```

**C5 — PR5:**
```
("functional data analysis" | "functional data" | "functional principal component" | FPCA) (economic | economics | financial | GDP | "gross domestic product" | volatility | "time series")
```
Nota: dado que IDEAS es una base específicamente de economía, esta cadena
podría dar un volumen alto en relación con las demás — es la más natural
para este repositorio.

**C6 — PR5:**
```
("functional data analysis" | "functional data" | "functional principal component" | FPCA) ("Latin America" | Ecuador | "South America" | Argentina | Bolivia | Brazil | Chile | Colombia | "Costa Rica" | Cuba | "Dominican Republic" | "El Salvador" | Guatemala | Haiti | Honduras | Mexico | Nicaragua | Panama | Paraguay | Peru | Uruguay | Venezuela)
```

**C7 — PR4, PR5:**
```
("functional time series" | "functional ARCH" | "functional GARCH") (volatility | economic | financial | heteroskedastic | heteroscedastic)
```

## Procedimiento de ejecución

1. Ve a `https://ideas.repec.org/search.html` (búsqueda avanzada), pega
   una cadena a la vez, selecciona campo de búsqueda "Whole record" y años
   1997–2026.
2. Revisa el recall del subconjunto relevante del conjunto oro para esa
   cadena (mapeo corregido en `cadenas_busqueda.md` §5.5) — verificando
   primero si cada ítem está indexado en RePEc en absoluto (RePEc indexa
   principalmente *working papers* y artículos de economía, así que es
   esperable que varios ítems del conjunto oro, centrados en estadística
   pura, no estén aquí).
3. Sin comodín de un carácter ni truncamiento — si el stemming automático
   no alcanza, amplía con `|` en vez de intentar un comodín.
4. Exporta manualmente (no hay API): revisa si la página de resultados o
   de cada ítem individual ofrece un botón de cita en BibTeX/RIS — RePEc
   normalmente lo ofrece por ítem individual en la página de cada
   documento, no en bloque desde los resultados de búsqueda.
5. Registra cada ejecución en `bitacora_busqueda.numbers` con
   `base_de_datos = IDEAS/RePEc`.
