# Cribado en dos etapas (Fase 5)

**Protocolo de referencia:** `protocolo_estado_del_arte.md`, §7
**Fuentes de información:** `fuentes_informacion.md` (v1.2)
**Bitácora de ejecución:** `bitacora_busqueda.numbers`

## 7.1 Deduplicación — ✅ CONGELADA (2026-09-07, 2777 ítems finales)

**Antes:** 6761 ítems en Zotero ("Mi Biblioteca"), sumando las 21 colecciones
importadas en la Fase 4 (7 cadenas × 3 bases: Scopus, zbMATH Open, arXiv).

**Procedimiento ejecutado:**

1. **Fusión automática** (vista "Duplicados" de Zotero, agrupación por
   coincidencia de DOI/ISBN o título+autor+año) → **2852 ítems**.
2. **Resolución manual de grupos bloqueados por tipo de ítem distinto**
   (Zotero no fusiona ítems de tipos diferentes aunque los detecte como
   duplicados). Casos encontrados:
   - Conflictos entre **Artículo de revista / Ponencia / Sección de libro /
     Documento** (tipo genérico de Zotero para códigos RIS mal mapeados en
     la importación) — resueltos verificando qué campos estaban realmente
     rellenos (revista, congreso/actas, libro/editor) para determinar el
     tipo real, retipificando el ítem incorrecto y fusionando hacia la
     versión con metadatos más completos.
   - Pares **preprint (arXiv) vs. versión publicada** (Scopus/zbMATH) — se
     aplicó el criterio **E3**: se conserva la versión publicada como
     maestra; el identificador de arXiv se preservó en el campo "Extra" del
     ítem maestro antes de fusionar, como evidencia de que la cadena de
     arXiv también recuperó ese trabajo. Incluye al menos un caso de
     ponencia sin DOI propio pero indexada en Scopus (cumple I2 vía
     indexación, no requiere DOI) con contraparte en arXiv.
   - Preprints **sin contraparte publicada** en su grupo no se tocaron: son
     inclusión legítima por sí sola (I2 admite preprint de arXiv con
     calidad verificable).
   - Grupos donde el título sugería una versión distinta (p. ej. posible
     versión extendida, no una copia exacta) **no se fusionaron** —
     quedan para revisión en el cribado título/resumen (§7.2).
   → **2777 ítems** (conteo final tras esta fase).

**Después:** 2777 ítems.

**Duplicados eliminados: 3984** (58.9 % del total bruto importado).

## 7.2 Etapa 1 — Título y resumen (I1–I5, E1–E5) — pendiente

## 7.3 Etapa 2 — Texto completo — pendiente

## 7.4 Control de consistencia intra-evaluador / auditoría del director — pendiente
