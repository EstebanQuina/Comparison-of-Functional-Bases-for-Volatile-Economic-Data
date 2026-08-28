# Preguntas de revisión (Fase 0)

**Protocolo de referencia:** `protocolo_estado_del_arte.md`, §2
**Estado:** v1.0 — borrador listo para validación con director/a

Todo el trabajo de las fases siguientes (criterios de elegibilidad, cadenas
de búsqueda, matriz de extracción, síntesis) se subordina a estas cinco
preguntas. Cada una ancla uno de los objetivos específicos de la tesis
(`manuscript/.../chapters/introduction.tex`).

| # | Pregunta de revisión | Objetivo específico que ancla |
|---|---|---|
| **PR1** | ¿Qué familias de bases funcionales se han empleado para representar datos funcionales y bajo qué justificación teórica se elige cada una? | Obj. 2 — implementar B-spline, Fourier y wavelet bajo un pipeline común |
| **PR2** | ¿Cómo afecta la elección de la base a los resultados del FPCA (varianza explicada, estabilidad de las eigenfunciones, número de componentes retenidas), y generaliza esta comparación más allá de una sola familia de bases? | Obj. 5 — efecto de la elección de base en la parsimonia e interpretabilidad del FPCA |
| **PR3** | ¿Qué criterios se han propuesto para seleccionar la dimensión de la base y el parámetro de suavizado, y cómo se separa su efecto del efecto de la familia de bases? | Obj. 3 — métricas de comparación a niveles equivalentes de calidad de reconstrucción |
| **PR4** | ¿Qué evidencia existe sobre el desempeño de las familias de bases wavelet frente a bases polinómicas o trigonométricas en procesos no suaves o no estacionarios? | Obj. 4 — preservación de episodios de crisis y estructura de volatilidad por familia de base |
| **PR5** | ¿Qué aplicaciones de FDA existen sobre series económicas y financieras, y en particular sobre datos de América Latina y Ecuador? | Obj. 1 — extensión del panel de PIB de América Latina de Padilla-Segarra et al. |

## Cambios respecto al borrador del protocolo

- **PR2**: se añadió la cláusula "y generaliza esta comparación más allá de
  una sola familia de bases" para evitar que la pregunta se lea como el
  efecto de *una* base fija en vez de la comparación *entre* bases.
- **PR4**: se especificó "familias de bases wavelet" (plural) para reflejar
  que la tesis compara tres familias (Haar, DB2, Sym4) y no trata wavelets
  como un bloque monolítico.

## Historial de versiones

| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-08-28 | Versión inicial, con los dos ajustes de PR2 y PR4 | Alinear con los objetivos específicos de la tesis antes de congelar |
