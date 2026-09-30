# Síntesis y detección del vacío (Fase 9)

**Protocolo de referencia:** `protocolo_estado_del_arte.md`, §11
**Conjunto de entrada:** `fase8/f8_matriz_extraccion.csv` (91 ítems + Padilla-Segarra
citado aparte; Ramsay & Silverman id 2118 como cita de apertura, ver `valoracion.md`)

## Tabla A — Antecedentes directos

**44/91 (48.4%)** ítems marcados `es_antecedente_directo=si` (Q3≥1 y Q4≥1).
Artefacto: `fase8/tabla_a_antecedentes_directos.csv`
(`id,clave_bibtex,autores,anio,familia_base,tipo_datos,dominio_aplicacion,metricas_reportadas,resultado_principal,limitacion_declarada,puntuacion_total`).

## Tabla B — Tabulación cruzada familia_base × criterio_seleccion_dimension

Los campos crudos de la matriz son demasiado granulares para una tabulación
legible (91 valores casi todos únicos en `familia_base` y en
`criterio_seleccion_dimension` — cada fila trae su propia variante textual).
Se normalizaron a categorías gruesas antes de tabular
(`fase8/_tabla_b_data.json`, generado por un script ad hoc, no versionado):

- **familia_base** → B-spline / P-spline / Fourier / wavelet / empírica
  (incluye FPCA/Karhunen-Loève) / RBF / otra / sin_dato, **más una categoría
  separada "MÚLTIPLE" para los ítems que comparan explícitamente ≥2 familias**
  (la señal más directa de Q4).
- **criterio_seleccion_dimension** → GCV / AIC-BIC-GIC / bayesiano /
  validación cruzada-bootstrap / umbral de varianza explicada / fijo-arbitrario-manual
  / no aplica / no reportado / otro criterio propio.

**Distribución de familia_base (normalizada, 91 ítems):**

| Categoría | n |
|---|---|
| B-spline (única) | 30 |
| **MÚLTIPLE (comparación explícita de ≥2 familias)** | **25** |
| empírica (única) | 12 |
| sin dato / no confirmado | 9 |
| otra | 5 |
| Fourier (única) | 5 |
| wavelet (única) | 2 |
| RBF (única) | 2 |
| P-spline (única) | 1 |

Tabla cruzada completa (familia × criterio, conteos) reproducible con el
script — la fila `MÚLTIPLE` se concentra en GCV (9), AIC/BIC/GIC (6) y
bayesiano (3): cuando un trabajo sí compara familias, casi siempre (18/25,
72%) también aplica un criterio formal de selección de dimensión, no un
valor fijo arbitrario.

## Verificación del vacío candidato (condición de validez, §11.3)

El protocolo exige comprobar el vacío contra la matriz antes de afirmarlo.
Se cruzó el grupo `MÚLTIPLE` (25 ítems) contra `preguntas_que_responde` y
`dominio_aplicacion`:

- **Solo 5/25 (20%) tocan PR5** (aplicación económica/financiera): ids 300
  (precios eléctricos, mercado italiano IPEX), 959 (epidemiología de aguas
  residuales — PR5 marginal), 1460 (flujos de gas natural, Alemania), 1562
  (FGARCH sobre retornos intradía del ETF SPY), 1840 (curvas forward de
  materias primas, índice S&P GSCI).
- **Ninguno de esos 5 aísla el efecto de la familia de bases del efecto del
  régimen de suavizado/penalización** como contribución metodológica
  explícita — reportan comparaciones o extensiones de modelo, no un diseño
  que controle ambos factores por separado.
- **El único ítem que sí separa explícitamente familia vs. método de
  estimación** (id 168, Beyaztas et al. — "compara sistemáticamente 3
  familias de base y 2 métodos de estimación") es sobre **datos climáticos
  semanales**, no económicos/financieros.
- **Ninguno de los 91 ítems aplica a datos latinoamericanos o ecuatorianos**
  — consistente con la escasez ya documentada en la búsqueda sistemática
  (Fase 4/5, cadenas C6).

**Conclusión de la verificación:** el vacío candidato del protocolo **se
sostiene, pero debe formularse con más precisión** — no es que la
comparación sistemática de bases sea inexistente en FDA (25/91, 27.5%, y al
menos un caso separa explícitamente familia de método), sino que esa
comparación **no se ha hecho para series económicas/financieras volátiles**,
y mucho menos con aislamiento del efecto de suavizado o con datos
latinoamericanos.

## Formulación del vacío en tres movimientos (borrador para revisión del usuario)

**1. Lo consolidado.** La representación de datos funcionales mediante
expansión en bases está bien establecida (B-spline domina con 30/91 usos
como familia única, seguida de bases empíricas/FPCA con 12/91), y los
criterios de selección de la dimensión de la base son maduros y de uso
extendido (GCV, AIC/BIC, validación cruzada aparecen en la mayoría de los
ítems que reportan un criterio).

**2. Lo fragmentario.** La comparación sistemática *entre* familias de
bases no es infrecuente en la literatura FDA general — 25/91 ítems (27.5%)
comparan explícitamente ≥2 familias, y al menos uno (id 168) aísla
formalmente el efecto de la familia de bases del efecto del método de
estimación. Pero esta literatura comparativa está concentrada en dominios
ajenos a la economía y las finanzas (clima, genética, espectroscopía,
geodesia, EEG): solo 5 de esos 25 trabajos tocan series económicas o
financieras, y ninguno de ellos separa el efecto de la familia del efecto
del régimen de suavizado.

**3. Lo ausente.** No existe, en la literatura revisada, una comparación
sistemática y controlada de familias de bases funcionales para la
representación por FPCA de series económicas o financieras volátiles que
aísle el efecto de la elección de base del efecto de la penalización o el
régimen de suavizado — y no existe ninguna aplicación de este tipo a datos
latinoamericanos o ecuatorianos. Este es precisamente el punto donde se
detuvo Padilla-Segarra et al. (el artículo que motiva esta tesis): usaron
únicamente B-splines sin comparación, sin penalización, y su propio trabajo
futuro propuesto pide explícitamente **"considering different approximation
basis"** — confirmación textual, desde dentro de la propia literatura del
campo, del vacío exacto que esta tesis atiende.

## Pendiente

1. **Redacción de los 5 ejes temáticos** (§11.1 del protocolo, uno por
   pregunta de revisión) — síntesis argumentativa en prosa a partir de la
   matriz, no un catálogo. Por definición del protocolo (§0.1, §12.2) esto
   es trabajo de argumentación que debe reflejar la voz del autor, no un
   listado generado automáticamente — pendiente de decidir con el usuario
   cómo dividir el trabajo (borrador completo para editar / esquema y
   evidencia para que el usuario escriba directamente / mixto por eje).
2. Revisión del usuario de las Tablas A y B y de la formulación del vacío
   arriba (borrador, no definitiva).
3. Después: Fase 10 (redacción final de la sección).
