# Matriz de extracción de datos (Fase 8)

**Protocolo de referencia:** `protocolo_estado_del_arte.md`, §10
**Conjunto de entrada:** 91 ítems puntuados en Fase 7 (`fase7/f7_scores_master.csv`) —
Ramsay & Silverman (id 2118) queda fuera, ver `valoracion.md` §"Tratamiento especial".

## Ejecución (2026-09-30)

Se completaron los campos de identificación (ya disponibles de fases previas),
metodológicos y de datos/evaluación del protocolo (§10) para los 91 ítems, en
12 lotes paralelos (forks) de ~8 ítems, usando el texto completo real. Los
campos de identificación (`autores`, `anio`, `fuente`, `tipo`, `indexacion`,
`doi`) y de valoración (`Q1`-`Q4`, `puntuacion_total`, `es_antecedente_directo`)
se copiaron literalmente de Fase 7 — no se recalcularon.

**Simplificación del campo `indexacion`** (documentada como limitación
metodológica, acordada antes de empezar): en vez de la granularidad
Scopus/WoS/MathSciNet del borrador del protocolo — no recuperable tras la
fusión de duplicados de §7.1 — se usa **"indexado"** (DOI + publicación con
revisión por pares) vs. **"preprint"** (solo arXiv, sin versión publicada).

## Control de calidad

- **Verificación de cobertura:** 91/91 ids, sin huecos ni duplicados entre
  los 12 lotes (`f8_matriz_extraccion.csv`).
- **Verificación de integridad:** se comprobó que los campos de identificación
  y valoración de cada fila coinciden exactamente con `f7_scores_master.csv`
  (no fueron alterados por los lotes de extracción). Se encontraron y
  corrigieron errores de formato CSV (comas sin escapar en el texto libre)
  en 7 de los 91 registros (ids 15, 31, 45, 58, 74 del lote 00; 1354, 1373 del
  lote 06) — el conteo de columnas era correcto pero el contenido de varios
  campos cualitativos había quedado desplazado. Se reconstruyó manualmente el
  contenido correcto de cada campo para esos 7 registros, verificando contra
  el texto fuente.

- **Nota importante — id 74 (Shamshoian et al., "Bayesian analysis of
  longitudinal and multidimensional functional data"):** durante la
  extracción se detectó que `fulltext_md/md/74.md` estaba dañado (solo
  navegación del sitio de PMC, sin cuerpo real del artículo) y se corrigió
  re-descargando el texto completo real desde PMC. **La puntuación Q1–Q4 de
  este ítem en Fase 7 pudo haberse calculado sobre el texto dañado** — no hay
  forma de confirmar retroactivamente qué versión vio el lote de Fase 7 que
  lo puntuó. Los campos cualitativos de este registro en la matriz sí reflejan
  el texto completo correcto (ya corregido). **Se recomienda que el usuario
  verifique manualmente la puntuación Q1–Q4 de este ítem específico** al
  revisar la matriz, en vez de asumirla como definitiva sin más.

## Resultado

**91/91 registros completos.** Artefacto: `fase8/f8_matriz_extraccion.csv`
(34 columnas: identificación, contenido metodológico, datos y evaluación,
valoración — `cita_textual_clave` con cita literal verificable y
`cita_pagina`; `nota_personal` no se incluyó, queda para que el usuario la
complete directamente si lo desea, es un campo de uso personal).

Distribución de `familia_base` (top): B-spline 28, empírica (FPCA) 19,
otra 9, Fourier 8, N/A 6, combinaciones (B-spline y Fourier) 4, wavelet 3,
P-spline 2. **44/91 (48.4%) antecedentes directos** (tras la corrección de
los ids 74 y 1731 documentada abajo).

- **Nota adicional — id 1731 (Yu & Sibbertsen, "Mapping price dynamics
  across electricity market designs"):** el lote que lo procesó encontró
  en el texto completo una justificación empírica explícita de la
  elección de base ("we chose Fourier basis over B-splines primarily
  because they yield smoother residuals for our type of data") que, bajo
  el rubric de Fase 7, correspondería a Q1=2, no Q1=0 como quedó
  puntuado originalmente.

**Corrección aplicada (2026-09-30):** se re-puntuaron los ids 74 y 1731
con lectura completa dirigida (ver `valoracion.md`, sección de
corrección). Resultado: 74 pasa de total=4 a **total=5** (Q1: 1→2);
1731 pasa de total=1 a **total=6** (Q1: 0→2, Q2: 0→2, Q4: 0→1) y **ahora
es antecedente directo**. Ambos valores ya están actualizados en
`f8_matriz_extraccion.csv` y `fase7/f7_scores_master.csv`. Total de
antecedentes directos: **44/91**, no 43.

## Pendiente

Verificación humana completa de la matriz por el usuario, con atención
prioritaria a:
1. El caso del id 74 señalado arriba.
2. El caso del id 1731 señalado arriba.
3. Los 7 registros reconstruidos manualmente tras el problema de formato CSV
   (ids 15, 31, 45, 58, 74, 1354, 1373) — mismo contenido derivado del texto
   fuente, pero vale la pena una doble verificación dado el origen del
   problema.

Después: Fase 9 (síntesis y detección del vacío), §11 del protocolo — Tabla A
(antecedentes directos), Tabla B (tabulación cruzada familia_base ×
criterio_seleccion_dimension) y formulación del vacío en tres movimientos.
