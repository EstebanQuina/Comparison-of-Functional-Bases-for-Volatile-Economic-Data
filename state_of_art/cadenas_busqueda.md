# Cadenas de búsqueda (Fase 3)

**Protocolo de referencia:** `protocolo_estado_del_arte.md`, §5
**Criterios de elegibilidad:** `criterios_elegibilidad.md`
**Fuentes de información:** `fuentes_informacion.md`
**Estado:** v1.0 — aprobado con modificaciones respecto al borrador del protocolo

## 5.1 Conjunto oro (*gold standard set*)

Conjunto de trabajos que deben aparecer al ejecutar las cadenas de
búsqueda; sirve para calibrar su sensibilidad (§5.4). Verificar cada uno en
fuente antes de usarlo para citar.

1. Ramsay & Silverman, *Functional Data Analysis*, 2.ª ed., Springer, 2005.
2. Ramsay, Hooker & Graves, *Functional Data Analysis with R and MATLAB*, Springer, 2009.
3. Wang, Chiou & Müller, "Review of Functional Data Analysis", *Annual Review of Statistics and Its Application*, 2016.
4. Ferraty & Vieu, *Nonparametric Functional Data Analysis*, Springer, 2006.
5. Kokoszka & Reimherr, *Introduction to Functional Data Analysis*, CRC, 2017.
6. Morettin, Pinheiro & Vidakovic, *Wavelets in Functional Data Analysis*, Springer, 2017.
7. Percival & Walden, *Wavelet Methods for Time Series Analysis*, Cambridge, 2000.
8. Padilla-Segarra, González-Villacorte, Amaro & Infante, "Brief Review of Functional Data Analysis: a Case Study on Regional Demographic and Economic Data", *Information and Communication Technologies* (Springer CCIS), 2020. — artículo que motiva la tesis; verificado como venue indexado (Springer CCIS), no requiere excepción regional.
9. Trabajo(s) de Aguilera y Aguilera-Morillo sobre comparación de enfoques de bases en FDA — **por localizar y verificar**.
10. Hörmann, Horváth & Reeder, sobre modelos funcionales de volatilidad — **por verificar**.

## 5.2 Estructura de las cadenas

Bloques conceptuales combinados con `AND`, sinónimos internos con `OR`:

- **Bloque A (dominio):** `"functional data analysis"` OR `"functional data"` OR `"functional principal component*"` OR FPCA
- **Bloque B (base):** `"basis function*"` OR `"basis system"` OR `"basis expansion"` OR `"basis selection"` OR `B-spline*` OR `"P-spline*"` OR `spline*` OR `Fourier` OR `wavelet*`
- **Bloque C (suavizado):** `smoothing` OR `"roughness penalty"` OR `"penalized"` OR `"knot selection"` OR `"generalized cross-validation"` OR GCV
- **Bloque D (aplicación):** `econom*` OR `financ*` OR `GDP` OR `"gross domestic product"` OR `volatil*` OR `"time series"`
- **Bloque E (región):** `"Latin America*"` OR Ecuador OR `"South America*"`

Nota: el Bloque E es un filtro temático sobre las bases de datos indexadas
de `fuentes_informacion.md` §4.1 — encuentra trabajos indexados *sobre* la
región, lo cual es independiente de la exclusión de fuentes regionales *no
indexadas* decidida en la Fase 1.

## 5.3 Cadenas concretas por pregunta de revisión

| ID | Pregunta | Cadena (adaptar sintaxis a cada base) |
|---|---|---|
| C1 | PR1, PR2 | `A AND B` |
| C2 | PR3 | `A AND B AND C` |
| C3 | PR4 | `A AND (wavelet* OR "wavelet basis") AND (nonstationary OR "non-stationary" OR rough OR discontinu*)` |
| C4 | PR2, PR4 | `A AND B AND (compar* OR "comparative study" OR benchmark*)` |
| C5 | PR5 | `A AND D` |
| C6 | PR5 | `A AND E` |
| C7 | PR4, PR5 | `("functional time series" OR "functional ARCH" OR "functional GARCH") AND (volatil* OR econom*)` |

Ajusta operadores de truncamiento y comillas según cada base (Scopus usa
`TITLE-ABS-KEY( )`; MathSciNet tiene su propia sintaxis de campos; zbMATH
usa `au:`, `ti:`, `cc:` con códigos MSC — aprovecha los códigos **62R10**,
**62H25**, **62M10**, **62G08**).

## 5.4 Procedimiento de calibración

1. Ejecuta cada cadena en Scopus.
2. Comprueba qué proporción del conjunto oro recupera.
3. Si la recuperación es < 80%, amplía sinónimos y repite.
4. Si una cadena devuelve más de ~600 resultados, restringe por campo
   (título/resumen/palabras clave en lugar de texto completo) o por área
   temática.
5. **Congela** las cadenas y anota la fecha. Toda ejecución posterior usa
   las cadenas congeladas.

## Cambios respecto al borrador del protocolo

- **§5.1**: se eliminaron dos candidatos del conjunto oro por caer fuera de
  la ventana 1997–2026 sin excepción (`criterios_elegibilidad.md`, I3):
  Eilers & Marx (1996) y Donoho & Johnstone (1994). Ambos se conservan como
  citas del Marco Teórico, fuera del alcance de esta calibración.
- **#8 (Padilla-Segarra et al. 2020)**: se verificó contra la exclusión de
  fuentes regionales no indexadas (E6) — publicado en actas indexadas de
  Springer (CCIS), por lo que satisface I2 directamente y no depende de
  ninguna excepción regional.
- **§5.2–§5.4**: sin cambios respecto al borrador del protocolo.

## Historial de versiones

| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-08-28 | Versión inicial: conjunto oro reducido de 12 a 10 candidatos; verificación de venue para #8 | Consistencia con los criterios de elegibilidad de la Fase 1 |
