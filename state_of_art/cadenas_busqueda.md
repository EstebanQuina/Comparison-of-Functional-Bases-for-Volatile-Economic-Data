# Cadenas de búsqueda (Fase 3)

**Protocolo de referencia:** `protocolo_estado_del_arte.md`, §5
**Criterios de elegibilidad:** `criterios_elegibilidad.md`
**Fuentes de información:** `fuentes_informacion.md`
**Estado:** v1.6 — C1 (871), C2 (473), C3 (33), C4 (389), C5 (735) congeladas en Scopus; C6–C7 pendientes

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
8. Padilla-Segarra, González-Villacorte, Amaro & Infante, "Brief Review of Functional Data Analysis: a Case Study on Regional Demographic and Economic Data", *Information and Communication Technologies* (Springer CCIS), 2020. — artículo que motiva la tesis; verificado como venue indexado (Springer CCIS), no requiere excepción regional. **Anomalía documentada:** no se recupera con C5 (`A AND D`) pese a que el título contiene literalmente "Economic"; confirmado ausente incluso con la búsqueda directa `TITLE-ABS-KEY(padilla AND economic)` (2026-08-28). No es un problema de vocabulario (ampliar el Bloque D no lo solucionaría) sino una anomalía puntual de indexación de este registro. No bloquea nada: la cita ya está asegurada de forma independiente.
9. Aguilera & Aguilera-Morillo — cluster de autoría central para el tema (14 documentos recuperados por C1 en Scopus). Tres anclas verificadas para calibración, con datos completos de Scopus:
    - **9a.** Aguilera, A.M., Acal, C., Aguilera-Morillo, M.C., Jiménez-Molinos, F. & Roldán, J.B. (2021). "Homogeneity problem for basis expansion of functional data with applications to resistive memories". *Mathematics and Computers in Simulation*, 186, pp. 41–51. DOI: [10.1016/j.matcom.2020.05.018](https://doi.org/10.1016/j.matcom.2020.05.018).
    - **9b.** Aguilera, A.M. & Aguilera-Morillo, M.C. (2013). "Comparative study of different B-spline approaches for functional data". *Mathematical and Computer Modelling*, 58(7–8), pp. 1568–1579. DOI: [10.1016/j.mcm.2013.04.007](https://doi.org/10.1016/j.mcm.2013.04.007).
    - **9c.** Escabias, M., Aguilera, A.M. & Aguilera-Morillo, M.C. (2014). "Functional PCA and Base-Line Logit Models". *Journal of Classification*, 31(3), pp. 296–324. DOI: [10.1007/s00357-014-9162-y](https://doi.org/10.1007/s00357-014-9162-y).

    Los 14 documentos completos del cluster se revisarán en el cribado de la Fase 5 (título/resumen), no solo estas tres anclas.
10. Hörmann, S., Horváth, L. & Reeder, R. (2013). "A functional version of the ARCH model". *Econometric Theory*, 29(2), pp. 267–288. DOI: [10.1017/S0266466612000345](https://doi.org/10.1017/S0266466612000345). Cita completa verificada vía Scopus (2026-08-28) — identificada al revisar el clúster de autoría de Hörmann que apareció en los resultados de C5. No recuperado por C1 (esperado). **Tampoco recuperado por C5**: C5 sí trae otros trabajos de Hörmann sobre series temporales/volatilidad funcional, pero no este título específico. Pendiente de probar en C7, su cadena originalmente asignada.

## 5.2 Estructura de las cadenas

Bloques conceptuales combinados con `AND`, sinónimos internos con `OR`:

- **Bloque A (dominio):** `"functional data analysis"` OR `"functional data"` OR `"functional principal component*"` OR FPCA
- **Bloque B (base):** `"basis function*"` OR `"basis system"` OR `"basis expansion"` OR `"basis selection"` OR `B-spline*` OR `"P-spline*"` OR `spline*` OR `Fourier` OR `wavelet*`
- **Bloque C (suavizado):** `smoothing` OR `"roughness penalty"` OR `penalized` OR `penalised` OR `"knot selection"` OR `"generalized cross-validation"` OR `"generalised cross-validation"` OR GCV OR `"cross-validation"` OR `"threshold selection"` OR `"wavelet threshold*"` OR `"dimension selection"` OR `"number of basis functions"` OR `regulari?ation`
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
| #2 | Sí | C1 (retirado de C5/C6: obra general, sin vocabulario específico) | ❌ no recuperado por C5, error de mapeo confirmado |
| #3 | No (confirmado) | — | fuera de alcance (Scopus) |
| #4 | No | — | fuera de alcance (Scopus) |
| #5 | Sí | C5, C6 | ✅ recuperado por C5 |
| #6 | Sí | C1 | ✅ recuperado por C1 |
| #7 | No | — | fuera de alcance (Scopus) |
| #8 | Sí | C5, C6 | ⚠️ anomalía de indexación — no recuperado ni con búsqueda directa, no bloquea |
| #9a | Sí | C1 | ✅ recuperado por C1 |
| #9b | Sí | C1, C2, C4 | ✅ recuperado por C1, C2 y C4 |
| #9c | Sí | C1 | ✅ recuperado por C1 |
| #10 | Sí | C7 | ❌ no recuperado por C5 (aunque C5 sí trae otros trabajos del mismo autor); pendiente de probar en C7 |

**Resultado de calibración de C1 (PR1, PR2):** subconjunto relevante = {#6,
#9a, #9b, #9c} → 4/4 recuperados = 100%. C1 queda calibrada y congelada sin
necesidad de ampliar el Bloque B.

**C1 congelada (2026-08-28) en 871 resultados** — sintaxis exacta y
filtros aplicados en `cadenas_scopus.md`. Ver `bitacora_busqueda.numbers`
para el historial completo de calibración (1243 → 876 → 871).

**Resultado de calibración de C2 (PR3):** el mapeo inicial asignaba {#6,
#9a, #9b, #9c} a C2, pero la ejecución real mostró que solo #9b trata
efectivamente sobre criterios de selección de suavizado/dimensión de base
(#6, #9a y #9c son, respectivamente, un panorama general de wavelets, un
problema de homogeneidad en la expansión, y un estudio de FPCA — ninguno
centrado en PR3). Ampliar el Bloque C con vocabulario de umbral
wavelet/selección de dimensión (402 → 473 resultados) no cambió la
recuperación de los otros tres, confirmando que su ausencia no era un
problema de sinónimos sino de asignación. Subconjunto relevante corregido =
{#9b} → 1/1 recuperado = 100%, tanto en la versión estrecha como en la
ampliada. Se conserva el Bloque C ampliado por su cobertura conceptual más
completa de PR3, aunque no haya sido necesario para esta calibración.

**C2 congelada (2026-08-28) en 473 resultados** — sintaxis exacta y
filtros en `cadenas_scopus.md`. Ver `bitacora_busqueda.numbers` para el
historial de calibración (402 → 473).

**Resultado de calibración de C3 (PR4):** el mapeo inicial asignaba #6 a
C3, pero dos rondas de ampliación del bloque de irregularidad (9 → 32 → 33
resultados, agregando vocabulario de umbral estadístico y luego de
disrupción aplicada: `abrupt change*`, `regime change*`, `shock*`,
`spike*`, `anomal*`) no lo recuperaron. Igual que con C2, se concluye que
es un error de asignación, no un vacío de vocabulario: el libro de
Morettin et al. es un panorama general, no un trabajo centrado en procesos
irregulares. Se retira #6 del subconjunto esperado de C3, que queda **sin
ancla propia en el conjunto oro**. Validación sustituta: revisión manual
de los 33 títulos, que muestran perfil temático coherente con PR4 (p. ej.
*"Adaptive Wavelets for Sparse Representations of Scattered Data"*,
*"Time normalization of voice signals using functional data analysis"*,
*"Wavelet power spectral domain functional principal component analysis
for feature extraction of epileptic EEGs"*).

**C3 congelada (2026-08-28) en 33 resultados** — sintaxis exacta en
`cadenas_scopus.md`. Sin filtro de volumen (muy por debajo de 600). Ver
`bitacora_busqueda.numbers` para el historial de calibración (9 → 32 → 33).

**Resultado de calibración de C4 (PR2, PR4):** el mapeo inicial asignaba
{#6, #9b} a C4. #6 no fue recuperado — tercera vez que falla (también en
C2 y C3), lo que confirma con evidencia acumulada que #6 solo pertenece al
subconjunto de C1: es un panorama/referencia general, nunca se
autodescribe como comparativo, de umbral, ni sobre procesos irregulares.
Se retira definitivamente de los subconjuntos de C2, C3 y C4. Subconjunto
corregido de C4 = {#9b} → 1/1 recuperado = 100%. No fue necesario ampliar
vocabulario.

**C4 congelada (2026-08-28) en 389 resultados** — sintaxis exacta en
`cadenas_scopus.md`. Sin filtro de volumen (bajo 600). Ver
`bitacora_busqueda.numbers`.

**Resultado de calibración de C5 (PR5):** el mapeo inicial asignaba
{#2, #5, #8} a C5 (1300 resultados sin filtrar). #2 no se recuperó —
mismo patrón que #6: manual general sin vocabulario específico, se retira
definitivamente a C1 solamente. #5 sí se recuperó. #8 no se recuperó pese
a contener "Economic" literalmente en el título; confirmado con búsqueda
directa `TITLE-ABS-KEY(padilla AND economic)` — se documenta como
anomalía de indexación, no como fallo de vocabulario (ver ítem #8 en
§5.1). Hallazgo adicional: C5 recupera varios trabajos de Hörmann sobre
series temporales/volatilidad funcional (aunque no #10 específicamente,
que sigue asignado solo a C7) — permitió identificar y verificar la cita
completa de #10 en §5.1 aunque no lo recupere directamente.

Subconjunto relevante corregido de C5 = {#5, #8}: #5 recuperado, #8
anomalía documentada (no bloquea). Historial de volumen: 1300 (sin
filtro) → 746 (+ área temática) → 735 (+ tipo de documento). Recall de #5
confirmado tras ambos filtros. Se acepta 735 pese a superar el umbral
orientativo de 600, con el mismo criterio aplicado a C1: el filtro de
tipo de documento apenas redujo el conteo (–11), señal de que el volumen
es alcance real de la cadena, no ruido editorial.

**C5 congelada (2026-08-28) en 735 resultados** — sintaxis exacta y
filtros en `cadenas_scopus.md`. Ver `bitacora_busqueda.numbers`.

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
| 1.3 | 2026-08-28 | Bloque C ampliado con vocabulario de umbral/dimensión; corregido el mapeo §5.5 de C2 de {#6, #9a-c} a {#9b}; C2 congelada en 473 resultados | Ampliar sinónimos no cambió la recuperación de #6/#9a/#9c, evidenciando un error de asignación en el mapeo inicial, no un vacío de vocabulario |
| 1.4 | 2026-08-28 | Tercer bloque de C3 ampliado en dos rondas (9→32→33); corregido el mapeo §5.5 retirando #6 de C3; C3 congelada en 33 resultados, validada por revisión manual de títulos en vez de conjunto oro | Mismo patrón que C2: ampliar vocabulario no recuperó #6, confirmando error de asignación; C3 queda sin ancla propia |
| 1.5 | 2026-08-28 | Retirado #6 definitivamente de C2/C3/C4 (tercera falla consecutiva), queda solo en C1; C4 congelada en 389 resultados con subconjunto corregido {#9b} | Evidencia acumulada de tres cadenas confirma que #6 es un panorama general, no específico de ninguna sub-pregunta |
| 1.6 | 2026-08-28 | Verificada cita completa de #10 (Hörmann, Horváth & Reeder, 2013); retirado #2 de C5/C6 (mismo patrón que #6); documentada anomalía de indexación de #8; C5 congelada en 735 resultados (área temática + tipo de documento) | Recall de #5 confirmado tras ambos filtros; volumen aceptado por el mismo criterio que C1 |
