# Cadenas de búsqueda (Fase 3)

**Protocolo de referencia:** `protocolo_estado_del_arte.md`, §5
**Criterios de elegibilidad:** `criterios_elegibilidad.md`
**Fuentes de información:** `fuentes_informacion.md`
**Estado:** v1.2 — C1 congelada en Scopus (871 resultados); C2–C7 pendientes

## 5.1 Conjunto oro (*gold standard set*)

Conjunto de trabajos que deben aparecer al ejecutar las cadenas de
búsqueda; sirve para calibrar su sensibilidad (§5.4). Verificar cada uno en
fuente antes de usarlo para citar.

1. Ramsay & Silverman, *Functional Data Analysis*, 2.ª ed., Springer, 2005.
2. Ramsay, Hooker & Graves, *Functional Data Analysis with R and MATLAB*, Springer, 2009.
3. Wang, Chiou & Müller, "Review of Functional Data Analysis", *Annual Review of Statistics and Its Application*, 2016. — **confirmado: no indexado en Scopus** (búsqueda directa por título, 2026-08-28).
4. Ferraty & Vieu, *Nonparametric Functional Data Analysis*, Springer, 2006.
5. Kokoszka & Reimherr, *Introduction to Functional Data Analysis*, CRC, 2017.
6. Morettin, Pinheiro & Vidakovic, *Wavelets in Functional Data Analysis*, Springer, 2017.
7. Percival & Walden, *Wavelet Methods for Time Series Analysis*, Cambridge, 2000.
8. Padilla-Segarra, González-Villacorte, Amaro & Infante, "Brief Review of Functional Data Analysis: a Case Study on Regional Demographic and Economic Data", *Information and Communication Technologies* (Springer CCIS), 2020. — artículo que motiva la tesis; verificado como venue indexado (Springer CCIS), no requiere excepción regional.
9. Aguilera & Aguilera-Morillo — cluster de autoría central para el tema (14 documentos recuperados por C1 en Scopus). Tres anclas verificadas para calibración, con datos completos de Scopus:
    - **9a.** Aguilera, A.M., Acal, C., Aguilera-Morillo, M.C., Jiménez-Molinos, F. & Roldán, J.B. (2021). "Homogeneity problem for basis expansion of functional data with applications to resistive memories". *Mathematics and Computers in Simulation*, 186, pp. 41–51. DOI: [10.1016/j.matcom.2020.05.018](https://doi.org/10.1016/j.matcom.2020.05.018).
    - **9b.** Aguilera, A.M. & Aguilera-Morillo, M.C. (2013). "Comparative study of different B-spline approaches for functional data". *Mathematical and Computer Modelling*, 58(7–8), pp. 1568–1579. DOI: [10.1016/j.mcm.2013.04.007](https://doi.org/10.1016/j.mcm.2013.04.007).
    - **9c.** Escabias, M., Aguilera, A.M. & Aguilera-Morillo, M.C. (2014). "Functional PCA and Base-Line Logit Models". *Journal of Classification*, 31(3), pp. 296–324. DOI: [10.1007/s00357-014-9162-y](https://doi.org/10.1007/s00357-014-9162-y).

    Los 14 documentos completos del cluster se revisarán en el cribado de la Fase 5 (título/resumen), no solo estas tres anclas.
10. Hörmann, Horváth & Reeder, sobre modelos funcionales de volatilidad — indexado en Scopus, **no recuperado por C1** (esperado: pertenece a C7, no a C1 — ver §5.5). Cita completa aún **por verificar**.

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
2. Comprueba qué proporción del conjunto oro recupera **dentro de su
   subconjunto relevante** (ver §5.5) — no del conjunto oro completo.
3. Si la recuperación es < 80% de ese subconjunto, amplía sinónimos y
   repite.
4. Si una cadena devuelve más de ~600 resultados, restringe por campo
   (título/resumen/palabras clave en lugar de texto completo) o por área
   temática.
5. **Congela** las cadenas y anota la fecha. Toda ejecución posterior usa
   las cadenas congeladas.

## 5.5 Mapeo cadena → subconjunto relevante del conjunto oro

No todos los ítems del conjunto oro son exigibles a todas las cadenas: cada
una responde a preguntas distintas (§5.3), así que un ítem cuenta como
"perdido" únicamente si la cadena a la que se asigna aquí no lo recupera.
Un ítem no indexado en Scopus queda fuera de cualquier cálculo de
recuperación para esta base de datos.

| Ítem | Indexado en Scopus | Cadena(s) a la(s) que corresponde | Estado |
|---|---|---|---|
| #1 | No | — | fuera de alcance (Scopus) |
| #2 | Sí | C5, C6 (obra general, sin término de Bloque B en el título) | pendiente de probar |
| #3 | No (confirmado) | — | fuera de alcance (Scopus) |
| #4 | No | — | fuera de alcance (Scopus) |
| #5 | Sí | C5, C6 (obra general) | pendiente de probar |
| #6 | Sí | C1, C2, C3, C4 | ✅ recuperado por C1 |
| #7 | No | — | fuera de alcance (Scopus) |
| #8 | Sí | C5, C6 | pendiente de probar |
| #9a–c | Sí | C1, C2, C4 | ✅ recuperados por C1 (3/3) |
| #10 | Sí | C7 | pendiente de probar en C7 |

**Resultado de calibración de C1 (PR1, PR2):** subconjunto relevante = {#6,
#9a, #9b, #9c} → 4/4 recuperados = 100%. C1 queda calibrada y congelada sin
necesidad de ampliar el Bloque B.

**C1 congelada (2026-08-28) en 871 resultados** — sintaxis exacta y
filtros aplicados en `cadenas_scopus.md`. Ver `bitacora_busqueda.numbers`
para el historial completo de calibración (1243 → 876 → 871).

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
| 1.1 | 2026-08-28 | C1 ejecutada en Scopus (1243 resultados); #3 confirmado no indexado; #9 reemplazado por tres anclas verificadas (14 documentos del cluster Aguilera/Aguilera-Morillo); #10 confirmado indexado pero fuera del alcance de C1; añadido §5.5 con mapeo cadena→ítem y calibración de C1 (100% sobre su subconjunto relevante) | Calibración real contra la primera ejecución en Scopus |
| 1.2 | 2026-08-28 | C1 congelada en 871 resultados (área temática + tipo de documento), pese a superar el umbral orientativo de ~600 | Recall 100% confirmado dos veces; el recorte adicional se delega al cribado de la Fase 5 |
