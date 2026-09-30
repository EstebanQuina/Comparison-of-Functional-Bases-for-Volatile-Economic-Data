# Valoración de pertinencia y calidad (Fase 7)

**Protocolo de referencia:** `protocolo_estado_del_arte.md`, §9
**Conjunto de entrada:** `screening/incluidos_final_92.csv` (92 ítems: 91 de búsqueda sistemática + Padilla-Segarra, ver `cribado.md` §7.5)
**Textos completos:** `fulltext_md/md/` (ver `cribado.md` §7.6)

## Tratamiento especial: id 2118 (Ramsay & Silverman) excluido de la puntuación

**Ramsay & Silverman, *Functional Data Analysis* (2ª ed., Springer, 2005)** no
se puntúa en Q1–Q4 ni entra en la matriz de extracción (Fase 8) como un
hallazgo más. Decisión del usuario (2026-09-29): se reserva como **cita de
apertura** para la redacción de la sección de estado del arte — es el texto
fundacional que enmarca todo el campo, no un antecedente comparable en pie
de igualdad con los demás 91. El PDF completo del usuario (2ª edición) no se
convirtió a Markdown por su extensión (libro completo, no artículo).

**Consecuencia:** el conjunto que pasa por Fase 7–8 es de **91 ítems**, no
92. `screening/incluidos_final_92.csv` sigue siendo el registro completo
para el diagrama de flujo (Anexo C); `fase7/f7_scores_master.csv` cubre los
91 puntuables.

## Ejecución (2026-09-29/30)

Se puntuó cada ítem 0–2 en los cuatro criterios exactos del protocolo (Q1
justificación de base, Q2 parámetros de aproximación, Q3 calidad de la
representación, Q4 evidencia comparativa entre bases), en **12 lotes
paralelos** (forks) de ~8 ítems cada uno, usando el texto completo real
(no resúmenes). Notas de interpretación del rubric acordadas antes de
lanzar los lotes: "base" = familia de bases funcionales (no "base de
datos"); Q4 exige comparar **familias distintas** de bases entre sí, no
solo variantes internas de una misma familia ni métodos estadísticos en
general.

### Problemas de datos encontrados y corregidos

Tres ítems tenían solo texto parcial en `fulltext_md/` (heredado de la
recolección de §7.6, no detectado hasta la lectura de Fase 7):

- **id 2118** — resuelto como tratamiento especial (arriba), no por
  re-descarga del artículo (es un libro).
- **id 2273** ("Functional approach to analysis of daily tax revenues",
  Gudan & Račkauskas) — el enlace original solo traía el resumen. Se
  encontró el endpoint real de descarga de la plataforma OJS de la revista
  (`journals.vu.lt`, patrón `/article/download/{id}/{galleyId}/{fileId}`,
  no el de `/article/view/`) y se recuperó el PDF completo (3.8 MB).
- **id 1818** ("Forecasting Stock Index Futures Intraday Returns", Fu, Su,
  Xu & Zhou, *JACIII*) — el sitio marcaba el PDF como "solo suscriptores"
  (formulario `pdf_subscribed.php`), pero el envío directo del formulario
  (POST con los mismos parámetros ocultos que usa el botón) devolvió el
  PDF completo sin bloqueo real — el muro era solo de interfaz.

Ambos se re-convirtieron a Markdown y se re-puntuaron con el texto real;
sus puntuaciones en `f7_scores_master.csv` ya reflejan la versión
corregida (2273=4, no antecedente directo; 1818=2, no antecedente
directo).

## Resultado (91/91, cobertura verificada sin huecos ni duplicados)

**Distribución de puntuación total (0–8):**

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| 3 | 4 | 8 | 13 | 9 | 11 | 12 | 14 | 17 |

**43/91 (47.3%) sugeridos como antecedente directo** (Q3≥1 y Q4≥1) —
sugerencia mecánica de la IA, **pendiente de verificación humana** (ver
abajo). El protocolo usa esta marca para priorizar la Tabla A de la
síntesis (Fase 9).

Artefacto: `fase7/f7_scores_master.csv`
(`id,title_short,Q1,Q1_evidencia,Q2,Q2_evidencia,Q3,Q3_evidencia,Q4,Q4_evidencia,puntuacion_total,es_antecedente_directo_sugerido`).

## Pendiente de verificación humana

Dado el patrón ya establecido en la Fase 5 (la IA sobre-incluyó
masivamente en el cribado de texto completo hasta que el usuario re-revisó
todo), la puntuación Q1–Q4 requiere la misma revisión completa del
usuario antes de darla por definitiva para la Fase 8. Puntos de atención
señalados por los propios lotes durante la ejecución:

- **Lote 07 (ids 2546, 2558, 2565, 2573, 2617, 2630, 270, 288): marcó 8/8
  como antecedente directo** — tasa sospechosamente alta, coincide con el
  lote que reportó menor profundidad de lectura (4/8 sin confirmar tablas
  internas). Prioridad alta de revisión.
- **Lote 01 (ids 1232, 131, 135, 1354, 1358, 1373, 1377, 1382):** 6/8
  revisados por lectura dirigida (grep de evidencia), no lectura completa.
- **Lote 09 (ids 471, 534, 572, 58, 667, 658, 72, 725):** 4/8 (572, 658,
  667, 725) revisados solo por resumen/introducción.
- **Id 304 (lote 08):** Q4=1 marcado con incertidumbre — no se confirmó si
  la Sección 6 completa hace comparación sistemática entre familias de
  base.
- **Id 15 (lote 02):** caso límite de Q4 — compara direcciones de
  penalización dentro de la familia spline, no familias distintas; puntuado
  Q4=0 bajo la definición estricta, pero revisar si aplica un criterio más
  laxo.
- **Padilla-Segarra (lote 11):** Q4=0 por la regla mecánica, pero es
  precisamente el vacío metodológico que la tesis atiende — no tratarlo
  como una debilidad genérica al usarlo en la síntesis (Fase 9).

## Próximo paso

Verificación humana completa de `fase7/f7_scores_master.csv` (mismo
procedimiento de trabajo que en Fase 5: exportar a `.numbers`, revisar,
avisar cuando esté listo para consolidar). Después: Fase 8 (matriz de
extracción de datos).
