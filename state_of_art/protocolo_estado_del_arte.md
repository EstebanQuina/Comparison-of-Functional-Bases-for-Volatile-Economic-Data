# Protocolo metodológico para la construcción del estado del arte

**Tesis:** *Estudio comparativo de bases funcionales para series económicas volátiles*
**Documento:** Protocolo de revisión sistematizada de literatura (v1.0)
**Fecha de elaboración:** _______________
**Autor:** _______________
**Director/a:** _______________

---

## 0. Propósito y alcance de este documento

Este protocolo define, **antes de empezar a buscar**, cómo se localizará, seleccionará, evaluará, extraerá y sintetizará la literatura que sustenta el estado del arte de la tesis. Fijar el protocolo por adelantado es lo que distingue una revisión metodológicamente defendible de una acumulación oportunista de citas.

El protocolo cumple tres funciones:

1. **Operativa.** Te dice qué hacer cada semana y en qué orden.
2. **Probatoria.** Genera evidencia registrada de que la búsqueda fue exhaustiva y no sesgada. En la defensa, cuando te pregunten "¿por qué no citaste a X?", tendrás una respuesta documentada en lugar de una improvisación.
3. **Argumentativa.** El vacío de investigación que justifica tu tesis no puede ser una afirmación de fe. Debe emerger de una matriz de evidencia. Este protocolo la construye.

### 0.1 Distinción previa: estado del arte ≠ marco teórico

Es un error frecuente y costoso en tesis de matemática. Verifica el formato exigido por tu escuela, pero la distinción estándar es:

| | Marco teórico | Estado del arte |
|---|---|---|
| Objeto | Conceptos, definiciones, teoremas | Trabajos de investigación |
| Pregunta que responde | ¿Qué necesito saber para entender esto? | ¿Qué se ha hecho ya y qué falta? |
| Estructura | Lógico-deductiva | Temática y crítica |
| Función | Dar herramientas al lector | Justificar que tu tesis aporta algo |
| Ejemplo en tu caso | Definición de base de Riesz, descomposición de Karhunen-Loève, transformada wavelet discreta | Quiénes han comparado familias de bases en FPCA, con qué datos, con qué métricas y qué encontraron |

El estado del arte **no explica qué es un wavelet**. Explica quién los ha usado en FDA, para qué, y por qué ese conjunto de trabajos deja abierta tu pregunta. Si tu documento termina pareciendo un tutorial, te has salido del género.

---

## 1. Enfoque metodológico adoptado

Se adopta una **revisión sistematizada de tipo mapeo estructurado** (*structured mapping study*), adaptada de las guías de Kitchenham y Charters para revisiones sistemáticas en ingeniería de software, y de las directrices de Petersen et al. para estudios de mapeo, complementadas con el procedimiento de *snowballing* de Wohlin.

**Justificación de la elección.** No se adopta PRISMA en sentido estricto porque PRISMA está diseñado para síntesis de evidencia clínica con metaanálisis cuantitativo, escenario que no aplica a una revisión metodológico-matemática. Sin embargo, **sí se adopta la lógica de documentación de PRISMA**: registro de cadenas exactas, conteo de resultados en cada etapa y diagrama de flujo de selección. Esto aporta reproducibilidad sin pretender una formalidad clínica improcedente.

**Nota de verificación:** confirma en fuente las referencias metodológicas anteriores (Kitchenham & Charters 2007; Petersen et al. 2008 y su actualización de 2015; Wohlin 2014) antes de citarlas. Están mencionadas aquí de memoria.

---

## 2. Fase 0 — Formulación de las preguntas de revisión

Todo lo que sigue se subordina a estas preguntas. Si un artículo no ayuda a responder ninguna, no entra, por prestigioso que sea.

Propuesta de preguntas (ajústalas con tu director/a):

- **PR1.** ¿Qué familias de bases funcionales se han empleado para representar datos funcionales y bajo qué justificación teórica se elige cada una?
- **PR2.** ¿Cómo afecta la elección de la base a los resultados del FPCA (varianza explicada, estabilidad de las eigenfunciones, número de componentes retenidas)?
- **PR3.** ¿Qué criterios se han propuesto para seleccionar la dimensión de la base y el parámetro de suavizado, y cómo se separa su efecto del efecto de la familia de bases?
- **PR4.** ¿Qué evidencia existe sobre el desempeño de bases wavelet frente a bases polinómicas o trigonométricas en procesos no suaves o no estacionarios?
- **PR5.** ¿Qué aplicaciones de FDA existen sobre series económicas y financieras, y en particular sobre datos de América Latina y Ecuador?

Cada pregunta se convertirá en un eje de la síntesis (§ 9) y en un bloque de la redacción (§ 11). La correspondencia debe ser explícita.

---

## 3. Fase 1 — Criterios de elegibilidad

Redáctalos ahora, no después. Cambiarlos a mitad de camino es legítimo, pero debe quedar registrado en el historial de versiones del protocolo (§ 13).

### 3.1 Criterios de inclusión

- **I1.** El trabajo aborda representación de datos funcionales mediante sistemas de bases, **o** análisis de componentes principales funcionales, **o** aplicación de FDA a series económicas/financieras.
- **I2.** Publicado en revista con revisión por pares, capítulo de libro académico, libro de referencia, actas de congreso indexado, o preprint en arXiv con calidad verificable.
- **I3.** Ventana temporal: 1997–2026 (desde la primera edición de Ramsay & Silverman). **Excepción documentada:** trabajos fundacionales anteriores admitidos por su carácter seminal (Grenander 1950; Rao 1958; Karhunen; Loève; Daubechies 1988/1992; Donoho & Johnstone 1994; Eilers & Marx 1996).
- **I4.** Idiomas: inglés, español, portugués, francés.
- **I5.** Texto completo accesible.

### 3.2 Criterios de exclusión

- **E1.** Trabajos que usan FDA como herramienta accesoria sin discutir la elección de base ni la calidad de la representación.
- **E2.** Material divulgativo, entradas de blog, notas de curso sin revisión, contenido de IA generativa sin autoría verificable.
- **E3.** Duplicados (se conserva la versión de registro: publicación en revista sobre preprint).
- **E4.** Trabajos cuyo único aporte es una aplicación de FDA a un dominio ajeno (medicina, meteorología) **salvo** que contengan una discusión metodológica sustantiva sobre la base empleada. Esta excepción es importante: buena parte de la mejor discusión sobre selección de bases está en literatura aplicada de otros campos.
- **E5.** Actas de congreso local sin revisión por pares documentada.

### 3.3 Tratamiento diferenciado de literatura latinoamericana

La producción regional relevante (incluido el artículo que motiva tu tesis) suele estar fuera de Scopus y WoS. Excluirla por indexación sesgaría tu sección de contexto local, que es justamente donde argumentas pertinencia.

**Regla:** para fuentes regionales no indexadas se aplica un criterio de calidad sustitutivo — revisión por pares declarada por la revista, DOI o repositorio institucional verificable, y afiliación institucional identificable. Estas fuentes se marcan en la matriz con `indexacion = regional` y se usan preferentemente para la PR5, no para sustentar afirmaciones metodológicas centrales. Documenta esta regla en la tesis; es una decisión defendible siempre que sea explícita.

---

## 4. Fase 2 — Fuentes de información

### 4.1 Bases de datos primarias (búsqueda sistemática con registro)

| Fuente | Cobertura relevante | Prioridad |
|---|---|---|
| Scopus | Amplia, multidisciplinar | Alta |
| Web of Science (Core Collection) | Amplia, complementaria a Scopus | Alta |
| MathSciNet | Matemática y estadística teórica | Alta |
| zbMATH Open | Matemática, acceso abierto | Alta |
| ScienceDirect | Texto completo Elsevier (CSDA, JMVA) | Media |
| SpringerLink | Libros de referencia de FDA | Media |
| Project Euclid | Annals of Statistics y afines | Media |
| JSTOR | Fuentes históricas (Rao 1958) | Baja |
| arXiv (math.ST, stat.ME, stat.AP) | Trabajo reciente no publicado | Media |
| IDEAS/RePEc | Aplicaciones económicas | Media |

### 4.2 Fuentes regionales

SciELO, Redalyc, Latindex, RRAAE (Repositorio de Recursos de Acceso Abierto del Ecuador), repositorios institucionales de ESPE, EPN, USFQ, Yachay Tech.

### 4.3 Búsqueda manual dirigida

Revisión de índices de los últimos ~10 años en: *Computational Statistics & Data Analysis*, *Journal of Multivariate Analysis*, *Annals of Applied Statistics*, *Journal of the Royal Statistical Society Series B*, *Statistical Papers*, *Advances in Data Analysis and Classification*, *Journal of Nonparametric Statistics*, *Econometrics and Statistics*.

Justificación: las cadenas booleanas fallan cuando los autores usan vocabulario distinto al tuyo. El barrido manual de revistas nucleares captura lo que la búsqueda sistemática pierde.

---

## 5. Fase 3 — Construcción y calibración de cadenas de búsqueda

### 5.1 Conjunto oro (*gold standard set*)

Antes de diseñar las cadenas, fija un conjunto de 8–12 trabajos que **sabes con certeza que deben aparecer**. Sirve para validar la sensibilidad de tus cadenas: si una cadena no recupera a un miembro del conjunto oro, la cadena está mal construida.

Candidatos iniciales (verifica cada uno en fuente antes de fijarlo):

1. Ramsay & Silverman, *Functional Data Analysis*, 2.ª ed., Springer, 2005.
2. Ramsay, Hooker & Graves, *Functional Data Analysis with R and MATLAB*, Springer, 2009.
3. Wang, Chiou & Müller, "Review of Functional Data Analysis", *Annual Review of Statistics and Its Application*, 2016.
4. Ferraty & Vieu, *Nonparametric Functional Data Analysis*, Springer, 2006.
5. Kokoszka & Reimherr, *Introduction to Functional Data Analysis*, CRC, 2017.
6. Eilers & Marx, "Flexible Smoothing with B-splines and Penalties", *Statistical Science*, 1996.
7. Morettin, Pinheiro & Vidakovic, *Wavelets in Functional Data Analysis*, Springer, 2017.
8. Percival & Walden, *Wavelet Methods for Time Series Analysis*, Cambridge, 2000.
9. Donoho & Johnstone, "Ideal Spatial Adaptation by Wavelet Shrinkage", *Biometrika*, 1994.
10. Padilla-Segarra, González-Villacorte, Amaro & Infante (artículo que motiva la tesis).
11. Trabajo(s) de Aguilera y Aguilera-Morillo sobre comparación de enfoques de bases en FDA (**localizar y verificar**).
12. Hörmann, Horváth & Reeder, sobre modelos funcionales de volatilidad (**verificar**).

### 5.2 Estructura de las cadenas

Bloques conceptuales combinados con `AND`, sinónimos internos con `OR`:

- **Bloque A (dominio):** `"functional data analysis"` OR `"functional data"` OR `"functional principal component*"` OR FPCA
- **Bloque B (base):** `"basis function*"` OR `"basis system"` OR `"basis expansion"` OR `"basis selection"` OR `B-spline*` OR `"P-spline*"` OR `spline*` OR `Fourier` OR `wavelet*`
- **Bloque C (suavizado):** `smoothing` OR `"roughness penalty"` OR `"penalized"` OR `"knot selection"` OR `"generalized cross-validation"` OR GCV
- **Bloque D (aplicación):** `econom*` OR `financ*` OR `GDP` OR `"gross domestic product"` OR `volatil*` OR `"time series"`
- **Bloque E (región):** `"Latin America*"` OR Ecuador OR `"South America*"`

### 5.3 Cadenas concretas por pregunta de revisión

| ID | Pregunta | Cadena (adaptar sintaxis a cada base) |
|---|---|---|
| C1 | PR1, PR2 | `A AND B` |
| C2 | PR3 | `A AND B AND C` |
| C3 | PR4 | `A AND (wavelet* OR "wavelet basis") AND (nonstationary OR "non-stationary" OR rough OR discontinu*)` |
| C4 | PR2, PR4 | `A AND B AND (compar* OR "comparative study" OR benchmark*)` |
| C5 | PR5 | `A AND D` |
| C6 | PR5 | `A AND E` |
| C7 | PR4, PR5 | `("functional time series" OR "functional ARCH" OR "functional GARCH") AND (volatil* OR econom*)` |

Ajusta operadores de truncamiento y comillas según cada base (Scopus usa `TITLE-ABS-KEY( )`; MathSciNet tiene su propia sintaxis de campos; zbMATH usa `au:`, `ti:`, `cc:` con códigos MSC — aprovecha los códigos **62R10**, **62H25**, **62M10**, **62G08**).

### 5.4 Procedimiento de calibración

1. Ejecuta cada cadena en Scopus.
2. Comprueba qué proporción del conjunto oro recupera.
3. Si la recuperación es < 80 %, amplía sinónimos y repite.
4. Si una cadena devuelve más de ~600 resultados, restringe por campo (título/resumen/palabras clave en lugar de texto completo) o por área temática.
5. **Congela** las cadenas y anota la fecha. Toda ejecución posterior usa las cadenas congeladas.

---

## 6. Fase 4 — Ejecución y bitácora de búsqueda

Crea una hoja `bitacora_busqueda` con estas columnas:

`id_ejecucion` · `fecha` · `base_de_datos` · `cadena_exacta` · `campos_de_busqueda` · `filtros_aplicados` · `n_resultados` · `n_exportados` · `archivo_ris_generado` · `observaciones`

**Reglas de oro:**

- Copia la cadena **exacta**, tal como la ejecutaste, incluyendo paréntesis y operadores de campo.
- Registra la fecha: las bases cambian y tu número de resultados no será reproducible sin ella.
- Exporta en RIS/BibTeX inmediatamente; no confíes en volver a encontrar los resultados.
- Nunca modifiques una cadena "sobre la marcha" sin registrar la nueva como ejecución independiente.

---

## 7. Fase 5 — Cribado en dos etapas

### 7.1 Deduplicación

Importa todo a Zotero. Usa la función de detección de duplicados y verifica manualmente por DOI. Registra el conteo antes y después.

### 7.2 Etapa 1 — Título y resumen

Aplica I1–I5 y E1–E5 sobre título y resumen. Ante la duda, **incluye**: es más barato descartar en la etapa 2 que perder un trabajo relevante.

Cada exclusión se registra con **el código del criterio** que la motivó (`E1`, `E2`, …). Esto es lo que te permitirá construir el diagrama de flujo.

### 7.3 Etapa 2 — Texto completo

Lectura de introducción, metodología y conclusiones. Misma lógica de registro. Los excluidos en esta etapa deben listarse en un anexo con su motivo — es una exigencia habitual de los tribunales exigentes y una señal de rigor.

### 7.4 Control de consistencia con un solo evaluador

Una tesis de pregrado tiene un solo revisor, de modo que el acuerdo entre evaluadores no es aplicable. Dos sustitutos aceptables:

- **Consistencia intra-evaluador.** Toma una muestra aleatoria del 10 % de los registros cribados en la Etapa 1, guárdala aparte y vuelve a cribarla a ciegas dos o tres semanas después. Calcula el porcentaje de acuerdo (o el κ de Cohen). Un acuerdo bajo indica que tus criterios están mal definidos, no que seas descuidado; corrígelos y vuelve a cribar.
- **Auditoría del director/a.** Pídele que cribe una muestra del 10 % y contrasta. Documenta las discrepancias y cómo se resolvieron.

Cualquiera de las dos, reportada en la tesis, eleva notablemente la percepción de rigor.

---

## 8. Fase 6 — Snowballing

La búsqueda booleana sola tiene cobertura incompleta. Complétala con dos pasadas, partiendo del conjunto de incluidos tras la Etapa 2:

- **Hacia atrás:** revisa las listas de referencias de cada trabajo incluido; identifica candidatos no capturados.
- **Hacia adelante:** en Scopus, WoS o Google Scholar, revisa quién cita a cada trabajo incluido, con especial atención a lo publicado desde 2020.

Itera hasta que una pasada completa no aporte trabajos nuevos (**saturación**). Registra el número de iteraciones y los hallazgos de cada una. Alcanzar la saturación es un argumento fuerte de exhaustividad.

---

## 9. Fase 7 — Valoración de pertinencia y calidad

No todos los incluidos pesan igual. Puntúa cada trabajo de 0 a 2 en cuatro criterios:

| Criterio | 0 | 1 | 2 |
|---|---|---|---|
| **Q1.** ¿Justifica la elección de base? | No la menciona | La menciona sin justificar | Justifica con argumento teórico o empírico |
| **Q2.** ¿Reporta parámetros de aproximación? | No | Parcialmente | Completo y reproducible |
| **Q3.** ¿Evalúa la calidad de la representación? | No | Solo varianza explicada | Múltiples métricas o validación cruzada |
| **Q4.** ¿Aporta evidencia comparativa entre bases? | No | Comparación informal | Comparación sistemática |

Los trabajos con puntuación alta en Q3 y Q4 son tus **antecedentes directos**: los que más se parecen a lo que vas a hacer, y frente a los cuales debes posicionarte con más cuidado. Los de puntuación baja pueblan tu argumento de vacío: si la mayoría puntúa 0 en Q4, ya tienes evidencia cuantificada de que la comparación sistemática de bases está poco atendida.

Esta puntuación no descarta trabajos; los ordena.

---

## 10. Fase 8 — Matriz de extracción de datos

Una fila por trabajo incluido. Hoja `matriz_extraccion` con estas columnas:

**Identificación**
`id` · `clave_bibtex` · `autores` · `anio` · `titulo` · `fuente` · `tipo` (artículo/libro/capítulo/actas/preprint) · `indexacion` (Scopus/WoS/MathSciNet/regional/preprint) · `doi`

**Contenido metodológico**
`preguntas_que_responde` (PR1–PR5) · `familia_base` (B-spline / P-spline / Fourier / wavelet / empírica / RBF / otra / N/A) · `orden_grado` · `dimension_base` · `criterio_seleccion_dimension` · `penalizacion` (sí/no/cuál) · `criterio_seleccion_lambda` (GCV/AIC/manual/no aplica) · `tecnica_principal` (FPCA / clustering / regresión funcional / FCCA / otra)

**Datos y evaluación**
`tipo_datos` (simulados / reales) · `dominio_aplicacion` · `n_curvas` · `n_puntos_por_curva` · `frecuencia_muestreo` · `metricas_reportadas` · `resultado_principal`

**Valoración**
`Q1` · `Q2` · `Q3` · `Q4` · `puntuacion_total` · `es_antecedente_directo` (sí/no) · `limitacion_declarada` · `trabajo_futuro_propuesto` · `cita_textual_clave` (≤ 20 palabras, con página) · `nota_personal`

**Advertencia sobre la columna `cita_textual_clave`:** limítate a fragmentos muy breves y siempre con página. En la redacción, **parafrasea**; las citas textuales extensas de fuentes con derechos son un riesgo real de plagio, aun con comillas y atribución.

**Uso posterior:** las columnas `limitacion_declarada` y `trabajo_futuro_propuesto` alimentan directamente tu argumento de vacío. Las columnas `familia_base`, `criterio_seleccion_dimension` y `Q4` producen, tabuladas de forma cruzada, la evidencia de que la separación entre efecto-de-base y efecto-de-suavizado está poco documentada — que es la contribución metodológica que has identificado en el artículo de partida.

---

## 11. Fase 9 — Síntesis y detección del vacío

### 11.1 Ejes de síntesis

Organiza el material por ejes temáticos, **nunca** por autor ni por orden cronológico ("Fulano dijo… Mengano dijo…" es la forma más común de reprobar esta sección).

- **Eje 1.** Fundamentos de FDA y representación en bases → PR1
- **Eje 2.** FPCA: fundamento, estimación y criterios de truncamiento → PR2
- **Eje 3.** Suavizado, penalización y selección de parámetros → PR3
- **Eje 4.** Bases wavelet y procesos no suaves → PR4
- **Eje 5.** FDA en economía y finanzas; antecedentes latinoamericanos y ecuatorianos → PR5

### 11.2 Tablas comparativas

Genera al menos dos tablas de síntesis a partir de la matriz. Son el corazón visual de la sección:

- **Tabla A.** Antecedentes directos: autor/año, familia(s) de base comparada(s), tipo de datos, métricas de evaluación, hallazgo principal, limitación.
- **Tabla B.** Tabulación cruzada `familia_base` × `criterio_seleccion_dimension`, con conteos. Las celdas vacías o casi vacías **son** el vacío de investigación, mostrado en lugar de afirmado.

### 11.3 Formulación del vacío

Redáctalo en tres movimientos:

1. **Lo consolidado.** Qué está bien establecido y no discutes.
2. **Lo fragmentario.** Qué se ha explorado de forma parcial, dispersa o sin sistematicidad.
3. **Lo ausente.** Qué nadie ha hecho, y por qué importa hacerlo.

Tu vacío candidato, según lo detectado hasta ahora: la comparación sistemática de familias de bases en FPCA aplicada a series económicas volátiles está poco documentada, y los estudios existentes rara vez **aíslan** el efecto de la familia de bases del efecto del régimen de suavizado. Este es el punto exacto donde el artículo de Padilla-Segarra et al. quedó abierto — y no solo por no probar Fourier o wavelets, sino por haber usado bases saturadas sin penalización, confundiendo ambos factores.

**Condición de validez:** este vacío solo es defendible si la matriz lo respalda. Si al llenarla descubres tres trabajos que ya hicieron exactamente eso, no fuerces el argumento: reformula el vacío hacia lo que sigue sin resolverse (por ejemplo, la ausencia de evidencia sobre datos latinoamericanos de baja frecuencia, o la interacción entre densidad de muestreo y ventaja relativa de la base). Un vacío reformulado con honestidad es mejor tesis que un vacío defendido contra la evidencia.

---

## 12. Fase 10 — Redacción

### 12.1 Estructura de embudo

```
1. Panorama: FDA como marco (breve; el detalle va al marco teórico)
2. Representación en bases: el problema de la elección          [Eje 1]
3. FPCA y su dependencia de la representación                    [Eje 2]
4. Suavizado y penalización: el factor confundido                [Eje 3]
5. Bases wavelet frente a procesos no suaves                     [Eje 4]
6. FDA en datos económicos; antecedentes regionales              [Eje 5]
7. Síntesis crítica y formulación del vacío
8. Posicionamiento de esta tesis
```

### 12.2 Regla de escritura por párrafo

Cada párrafo debe **argumentar**, no resumir. Contrasta:

> ✗ *Ramsay y Silverman (2005) explican las bases B-spline y sus propiedades.*

> ✓ *La literatura asume mayoritariamente que las curvas subyacentes son suaves, supuesto que las bases B-spline explotan de manera eficiente (Ramsay & Silverman, 2005), pero que las series de crecimiento del PIB violan de forma sistemática por la presencia de shocks localizados.*

El segundo enunciado hace trabajo argumentativo: establece un supuesto compartido y anticipa por qué falla en tu caso.

### 12.3 Densidad y proporción de citas

- Toda afirmación sustantiva sobre el campo lleva respaldo.
- Ninguna cita sin función argumentativa.
- Proporción orientativa: 60 % del texto en síntesis y comparación entre trabajos, 40 % en descripción de trabajos individuales. Si se invierte, has escrito un catálogo.

### 12.4 Extensión orientativa

Para una tesis de pregrado en matemática: 12–20 páginas, 60–90 referencias. Verifica el reglamento de tu escuela; estos números son referenciales.

---

## 13. Control de versiones del protocolo

Anexa esta tabla al final del protocolo y actualízala cada vez que modifiques un criterio:

| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | | Versión inicial | — |

Modificar criterios a mitad de proceso es normal y aceptable. Modificarlos **sin registrarlo** convierte una revisión sistematizada en una selección oportunista.

---

## 14. Gestión bibliográfica

- **Zotero** con el conector de navegador, sincronización activa y respaldo periódico de la carpeta de datos.
- Colecciones espejo de los ejes: `01_Fundamentos`, `02_FPCA`, `03_Suavizado`, `04_Wavelets`, `05_Economia_LatAm`, `99_Descartados`.
- Etiquetas: `antecedente-directo`, `conjunto-oro`, `por-verificar`, `pendiente-texto-completo`.
- Exportación a `referencias.bib` mediante Better BibTeX, con claves estables de formato `apellido_palabraclave_anio`.
- **Nunca** cites de segunda mano. Si Padilla-Segarra et al. citan a Ullah & Finch, lee a Ullah & Finch antes de citarlo. Los errores de citación se propagan y los tribunales los detectan.
- Verifica cada DOI. Las referencias generadas por modelos de lenguaje —incluidas las sugerencias que has recibido en esta conversación— **deben comprobarse una a una en la fuente original** antes de entrar en el `.bib`.

---

## 15. Cronograma orientativo

| Semana | Actividad | Producto |
|---|---|---|
| 1 | Fases 0–1: preguntas y criterios; validación con director/a | Protocolo v1.0 aprobado |
| 2 | Fase 2–3: fuentes, conjunto oro, calibración de cadenas | Cadenas congeladas |
| 3 | Fase 4: ejecución en todas las bases | Bitácora + biblioteca Zotero |
| 4 | Fase 5: deduplicación y cribado etapa 1 | Conteos por criterio |
| 5–6 | Fase 5: cribado etapa 2 (texto completo) | Conjunto de incluidos |
| 7 | Fase 6: snowballing hasta saturación | Incluidos ampliados |
| 8–9 | Fases 7–8: valoración y matriz de extracción | Matriz completa |
| 10 | Fase 9: síntesis, tablas A y B, formulación del vacío | Esquema argumentado |
| 11–12 | Fase 10: redacción | Borrador |
| 13 | Revisión, verificación de citas, diagrama de flujo | Versión para director/a |

Total: unas 13 semanas a dedicación parcial. Comprímelo si tu calendario aprieta, pero no elimines las fases 6 y 8: el snowballing y la matriz son las que producen el argumento.

---

## 16. Instrumentos a producir (anexos de la tesis)

1. **Anexo A.** Protocolo de revisión (este documento, con su historial de versiones).
2. **Anexo B.** Bitácora de búsqueda completa.
3. **Anexo C.** Diagrama de flujo de selección, en formato PRISMA:

```
Registros identificados en bases de datos (n = ___)
        │
        ├──> Duplicados eliminados (n = ___)
        ▼
Registros cribados por título y resumen (n = ___)
        │
        ├──> Excluidos (n = ___)   [E1: ___ · E2: ___ · E3: ___ · E4: ___ · E5: ___]
        ▼
Textos completos evaluados (n = ___)
        │
        ├──> Excluidos (n = ___)   [motivos en Anexo E]
        ▼
Incluidos por búsqueda sistemática (n = ___)
        │
        ├──> Añadidos por snowballing (n = ___)
        ▼
Estudios incluidos en la síntesis (n = ___)
```

4. **Anexo D.** Matriz de extracción.
5. **Anexo E.** Listado de exclusiones en texto completo con motivo.

---

## 17. Errores frecuentes a evitar

| Error | Consecuencia | Prevención |
|---|---|---|
| Escribir por autor y no por tema | Catálogo sin argumento | Ejes temáticos definidos antes de escribir |
| Confundir estado del arte con marco teórico | Sección redundante | § 0.1 |
| Citar de segunda mano | Errores propagados, riesgo de citar mal | Verificación en fuente |
| Afirmar el vacío sin evidencia | Objeción directa en la defensa | Matriz + Tabla B |
| No registrar las cadenas de búsqueda | Irreproducible | Bitácora |
| Sobredimensionar la sección de wavelets | Desequilibrio entre ejes | Distribución proporcional al peso argumentativo |
| Incluir referencias no verificadas | Referencia inexistente en la bibliografía | Verificación de DOI una a una |
| Citar textualmente en exceso | Riesgo de plagio | Parafrasear; citas breves y con página |
| Ignorar literatura aplicada de otros campos | Perder la mejor discusión sobre bases | Criterio E4 con su excepción |

---

## 18. Lista de verificación final

Antes de entregar la sección a tu director/a:

- [ ] Cada pregunta de revisión (PR1–PR5) tiene su bloque correspondiente en el texto
- [ ] Cada afirmación sustantiva sobre el campo está respaldada
- [ ] Cada referencia fue verificada en su fuente original
- [ ] Todos los DOI resuelven correctamente
- [ ] La bitácora está completa y con fechas
- [ ] El diagrama de flujo cuadra aritméticamente
- [ ] La matriz de extracción está completa para todos los incluidos
- [ ] Las tablas A y B están generadas y referenciadas en el texto
- [ ] El vacío está formulado en tres movimientos y respaldado por la matriz
- [ ] El posicionamiento de la tesis frente a los antecedentes directos es explícito
- [ ] La afirmación sobre lo que propone el artículo de Padilla-Segarra et al. es textualmente exacta (no les atribuyas Fourier ni wavelets)
- [ ] No hay párrafos que expliquen conceptos en lugar de discutir trabajos
- [ ] Se ejecutó una actualización de búsqueda en el último mes antes de la defensa

---

*Fin del protocolo.*
