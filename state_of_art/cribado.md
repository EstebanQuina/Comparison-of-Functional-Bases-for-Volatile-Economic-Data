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

## 7.2 Etapa 1 — Título y resumen (I1–I5, E1–E6) — ✅ CONGELADA (2026-09-09)

**Insumo:** exportación RIS de los 2777 ítems deduplicados (`state_of_art/screening/library_enriched.json` tras el pipeline de abajo).

### Limitación encontrada y corregida: resúmenes faltantes

La exportación RIS original (`My Library.ris`, desde Zotero) traía resumen
(`AB`) en solo **376/2777 ítems (13.5%)** — los 1854 ítems de origen Scopus
no tenían resumen en absoluto (el export de Scopus en Fase 4 no marcó la
casilla "Abstract"). Antes de clasificar, se enriqueció vía DOI:

1. Lote por **Semantic Scholar** (`/graph/v1/paper/batch`, campo `abstract`)
   sobre los 2238 ítems con DOI y sin resumen: **1235 recuperados**.
2. Fallback por **Crossref** (`/works/{doi}`) sobre los que Semantic Scholar
   no resolvió: **149 recuperados** más.
3. **Cobertura final: 1760/2777 (63.4%)** con resumen real; 1017 quedan
   solo con título (sin DOI, o no encontrados en ninguna de las dos APIs).

Scripts: `screening/parse_ris.py` (RIS → JSON estructurado) y
`screening/enrich_abstracts.py` (backfill). Dataset resultante:
`screening/library_enriched.json`.

### Clasificación asistida (IA) contra I1–I5/E1–E6

Dado el volumen (2777 ítems), la primera pasada de clasificación título/
resumen se hizo con asistencia de Claude (14 lotes de ~200 ítems,
procesados en paralelo, mismos criterios I1–I5/E1–E6 exactos de
`criterios_elegibilidad.md` en cada lote) — **como primer filtro para que
el usuario (revisor único, §7.4) verifique y confirme, no como sustituto
del criterio del revisor.** Regla aplicada: "ante la duda, incluye"
(§7.2 del protocolo), reforzada aún más para los 1017 ítems solo-título
(confidence='baja' obligatorio en esos casos). **Esta metodología debe
documentarse explícitamente en la sección de metodología de la tesis**
(transparencia exigida por el protocolo, §14).

**Resultado de la primera pasada (IA, 2777/2777 procesados, sin huecos ni
duplicados entre lotes, verificado programáticamente):** 2337 incluye /
440 excluye. Artefacto: `screening/decisions_master_v1_ia.csv`.

### Verificación humana de la lista prioritaria (2026-09-09)

El usuario revisó `revision_prioritaria.csv` (115 ids: las 104 exclusiones
de confianza "baja" más los ids de los pares de posible duplicado) en
`revision_prioritaria_terminado.numbers`, marcando cada fila con color:
**verde** = de acuerdo con la decisión de la IA, **amarillo** = decisión
cambiada. Se leyó el archivo `.numbers` programáticamente (librería
`numbers-parser`, color de fondo por celda) y se verificó consistencia de
color por fila (0 filas con color mixto entre columnas): **102 verdes,
13 amarillas**.

**15 decisiones cambiaron** respecto a la propuesta de la IA (2 estaban en
verde por una discrepancia de resaltado ya corregida por el usuario,
netas: 13 amarillas reales tras la corrección):

| id | original | final | motivo del cambio |
|---|---|---|---|
| 206, 235, 377 | exclude/E4 | include | revisor: sí hay discusión de base al leer completo |
| 1014, 1350, 1665, 1787, 1897, 1910 | exclude/I1 | include | revisor: sí hay conexión FDA/base que el título solo no mostraba |
| 1193 | exclude/I1 | include | usa FDA como herramienta, con posible discusión de base |
| 1688 | exclude/I1 | include | usa FDA/FPCA para descomponer series de producción petrolera |
| 1861 | exclude/I1 | include | libera la exclusión — su duplicado id 1995 queda como E3 (superseded) |
| 1774 | exclude/I1 | exclude/**E5** | recodificado (mismo veredicto de exclusión, motivo más preciso) |
| 494 | include | **exclude/revisor** | criterio propio: trabajo teórico, no aplicado (no encaja limpio en E1–E6) |
| 533 | include | **exclude/E3** | duplicado de 494, confirmado por el usuario |

**Pares de posible duplicado, resueltos:**
- **313 / 319** — confirmado por el usuario: **no son el mismo trabajo**
  (dos aportes distintos sobre FPCA con media/covarianza dependiente de
  covariables). Ambos quedan `include`, sin fusión en Zotero.
- **494 / 533** — sí es duplicado; ambos terminan excluidos (ver tabla).
- Los otros 4 pares detectados durante la clasificación ya habían quedado
  resueltos dentro de la misma pasada de IA (E3 en el duplicado, `include`
  en la versión conservada): 1053/**1061**, 1860/**1909**, 2491/**2495**
  (negrita = el que quedó excluido), más 1861/1995 arriba.

**Resultado final de §7.2 (2777 ítems: 2662 con el veredicto de la IA sin
modificar + 115 verificados por el usuario):**

| Decisión | n |
|---|---|
| **Incluye** (pasa a Etapa 2) | **2347** |
| **Excluye** | **430** |

**Motivos de exclusión finales:**

| Código | n | Motivo |
|---|---|---|
| I1 | 313 | No cumple el tema (falso positivo de las cadenas booleanas amplias) |
| E4 | 61 | Aplicación de FDA a dominio ajeno sin discusión metodológica sustantiva de la base |
| E5 | 41 | Actas de congreso local / registros a nivel de volumen completo de actas |
| E1 | 9 | FDA usado como herramienta accesoria, sin discutir base ni calidad de representación |
| E3 | 5 | Duplicado detectado que no se había fusionado en §7.1 |
| revisor | 1 | Criterio propio del revisor, fuera de los códigos I/E (trabajo teórico sin aplicación) |

**Artefactos finales** (todos en `state_of_art/screening/`):
- `decisions_master.csv` — **versión final y vigente**, 2777 filas
  (`id,title_short,decision,reason_code,confidence,rationale,
  revisado_manualmente,color_numbers`). Registro de auditoría completo
  para Anexo C/E; `revisado_manualmente=si` marca los 115 ids verificados
  por el usuario.
- `decisions_master_v1_ia.csv` — snapshot histórico de la primera pasada,
  solo IA, previo a la verificación humana (conservado para trazabilidad).
- `revision_prioritaria.csv` / `revision_prioritaria_terminado.numbers` —
  la lista de 115 ids y el archivo de trabajo del usuario con sus
  decisiones y colores.

**Nota metodológica para la tesis (documentar en metodología, §14):**
1. La Etapa 1 usó un primer filtro asistido por IA (Claude, 14 lotes en
   paralelo) sobre los 2777 ítems, con verificación humana dirigida sobre
   la sub-muestra de mayor riesgo (exclusiones de confianza baja + posibles
   duplicados) en vez de una relectura humana de los 2777. Esto es una
   desviación documentada del supuesto por defecto de "un solo revisor lee
   todo" — el revisor (Esteban) tomó la decisión final sobre el subconjunto
   de riesgo; el resto conserva el veredicto de la IA hasta que la Etapa 2
   (texto completo) lo confirme o corrija.
2. El enriquecimiento de resúmenes vía DOI (Semantic Scholar/Crossref)
   también sirvió para detectar duplicados que la deduplicación de §7.1 no
   había capturado (títulos casi idénticos con variaciones de formato) —
   control de calidad adicional, no solo corrección de datos faltantes.
3. **I5 (texto completo accesible) no se aplicó en esta etapa** — no es
   verificable con solo título/resumen. Se evalúa en la Etapa 2, donde la
   falta de acceso (biblioteca de Yachay Tech con catálogo limitado, ver
   `fuentes_informacion.md`) puede ser un motivo de exclusión documentado
   por sí mismo, tras agotar vías razonables (Unpaywall/Semantic Scholar,
   arXiv, préstamo interbibliotecario/CEDIA, contacto con autor) — pendiente
   de definir el procedimiento exacto para la Etapa 2.

## 7.3 Etapa 2 — Texto completo — ⏳ en curso (triage de acceso, 2026-09-09)

**Punto de partida:** los 2347 ítems incluidos en §7.2.

### Triage de acceso (I5) antes de leer texto completo

Con el catálogo limitado de la biblioteca de Yachay Tech (misma limitación
ya documentada en `fuentes_informacion.md` para la Fase 4), aplicar I5
directamente habría descartado una fracción grande sin agotar vías
razonables. En vez de eso, se corrió un chequeo automatizado de acceso
abierto legal sobre los 2347 (script `screening/check_oa_access.py`,
salida `screening/oa_status.csv`):

1. **Unpaywall** (`api.unpaywall.org`, por DOI) — agrega copias legales
   alojadas por el autor/repositorio/editor: **986 con OA confirmado**.
2. **Semantic Scholar** (`openAccessPdf`) como fallback sobre lo que
   Unpaywall no resolvió: **123 más**.
3. **Detección de URL de arXiv** en los ítems sin DOI (335 de 423):
   ya son de acceso abierto por naturaleza aunque el registro no tenga DOI.

**Resultado: 1444/2347 (61.5%) con acceso abierto legal ya confirmado.**
Los 903 restantes (815 con DOI sin OA detectado + 88 sin DOI ni arXiv)
quedan **pausados, no excluidos** — I5 todavía no se ha aplicado sobre
ellos, a la espera de que el usuario confirme con la biblioteca de Yachay
Tech si hay préstamo interbibliotecario o acceso vía **CEDIA** (consorcio
ecuatoriano de bibliotecas académicas). Solo se registrará una exclusión
por I5 sobre un ítem de este grupo tras agotar esa vía (y, si aplica,
contacto directo con el autor) — no antes.

**Decisión del usuario (2026-09-09):** avanzar ya con la lectura de texto
completo sobre los **1444 con acceso confirmado**, dejando los 903
pendientes en paralelo mientras se resuelve el tema bibliotecario.

### Obtención automática de texto completo (2026-09-10)

Script `screening/fetch_fulltext.py` (fetch por la URL de OA, extracción de
texto de PDF con `pypdf` o de HTML con `BeautifulSoup`; caché local en
`screening/fulltext_cache/`, **no versionado** — contenido con derechos de
autor). Resultado sobre los 1444:

| Categoría | n |
|---|---|
| Texto completo real obtenido | **761** (52.7%) |
| Bloqueado por editorial (403/404/timeout — Elsevier, Wiley, MDPI, SAGE) | 383 |
| Vacío / dependiente de JavaScript | 265 |
| Muro anti-bot explícito (Cloudflare/Anubis) | 20 |
| Solo página de metadatos de repositorio | 15 |

No se intentó evadir los muros anti-bot de las editoriales. Los 683 no
obtenidos (1444 − 761) se suman a los 903 sin OA → **1586 ítems pendientes
de obtención de texto completo por otra vía** (descarga manual del usuario
en su navegador, préstamo interbibliotecario / CEDIA, o contacto con autor).

### Cribado de texto completo asistido (IA) — subconjunto de 761

De cada texto obtenido se armó un extracto acotado (introducción ~6000
car. + conclusión ~3000 car., cuerpo intermedio omitido) —
`screening/build_fulltext_excerpts.py` → `screening/fulltext_excerpts.json`.
Se clasificaron los 761 en 16 lotes en paralelo (forks) contra I1–I5/E1–E6,
con I5 ya satisfecho por construcción. Resultado consolidado (761/761,
cobertura verificada, `screening/ft_decisions_master.csv`):

| Decisión | n |
|---|---|
| **Incluye** | **700** |
| **Excluye** | **61** |

Motivos de exclusión: I1=30 · E4=22 · E1=8 · E3=1.

Distribución de confianza: alta=468, media=278, baja=15.
**215/761 marcados `extracto_truncado_relevante=si`** — el cuerpo intermedio
omitido (donde suele estar la discusión sustantiva de la base, clave para
E1/E4) limitó la certeza, o el extracto resultó ser una página de aterrizaje
en vez del cuerpo real. Todos esos casos se resolvieron a favor de la
inclusión ("ante la duda, incluye").

### Verificación humana de la lista prioritaria (2026-09-10)

El usuario revisó `screening/ft_revision_prioritaria.csv` (66 ids) en
`ft_revision_prioritaria_terminada.numbers`, con código de color:
**verde** = de acuerdo (63), **amarillo** = decisión cambiada (2),
**rojo** = no pudo acceder al documento completo (1). Leído
programáticamente (`numbers-parser`, bg_color por celda, 0 filas con color
mixto).

Cambios respecto a la propuesta de IA (los 63 verdes se confirmaron sin
cambio; pasan a `confidence=alta`, `revisado_manualmente=si`):

| id | IA | final | motivo |
|---|---|---|---|
| 2367 | include | **exclude / E1** | revisor: no menciona explícitamente la base usada — FDA accesoria |
| 2491 | include | **exclude / E3** | revisor: duplicado de id 348 (se conserva 348; 2491 y 2495 fuera) |
| 1187 | exclude / E4 | **pendiente_acceso** | el revisor no pudo acceder al texto completo — sale del subconjunto cribado, va a la cola de pendientes |

Nota sobre id 1350 y id 1347 (flageados por los forks): el usuario los
revisó dentro de esta lista y quedaron en verde (de acuerdo con la
propuesta) — 1350 confirmado `exclude/E1` (sobrescribe su propia promoción
a include en la Etapa 1), 1347 mantiene `include` por el título pese al PDF
equivocado del fetch.

**Resultado final del cribado de texto completo (subconjunto accesible,
760 ítems tras mover 1187 a pendientes):**

| Decisión | n |
|---|---|
| **Incluye** | **698** |
| **Excluye** | **62** |

Motivos de exclusión: I1=30 · E4=21 · E1=9 · E3=2.
Artefacto final: `screening/ft_decisions_master.csv`
(`revisado_manualmente=si` marca los 66 ids verificados).

### Decisión de alcance: solo acceso abierto (2026-09-12)

El autor consultó con su director de tesis: dado el volumen de literatura
que ya superó el cribado título/resumen (2347 ítems), **se acuerda
restringir la revisión a literatura de acceso abierto**, sin perseguir
préstamo interbibliotecario, CEDIA ni contacto con autores para el resto.
Formalizado como **I5 v1.1** en `criterios_elegibilidad.md` §3.5 — "acceso
abierto" se define por el **estatus legal/de licencia** (Unpaywall/
Semantic Scholar/arXiv), no por si la descarga automática tuvo éxito.

**Consecuencia aplicada:**
- **903 ítems sin OA confirmado → excluidos por I5**, formalmente
  (`screening/excluidos_I5_no_oa.csv`). Dejan de estar "pausados" — quedan
  fuera de la revisión.
- **684 ítems con OA confirmado pero sin texto utilizable** (683 bloqueados
  por muro anti-bot editorial en el fetch automático + id 1187, cuyo
  extracto tampoco resultó utilizable) **permanecen en el alcance** —
  siguen siendo de acceso abierto por definición, solo falta que el autor
  los abra manualmente en su navegador (sin el bloqueo que sí afecta a un
  script). Lista de trabajo generada y ordenada por dominio para facilitar
  el acceso por lotes: `screening/pendientes_acceso_manual.csv`. Dominios
  con más ítems: doi.org (145, redirecciones — el dominio real variará),
  projecteuclid.org (90), sciencedirect.com (74), mdpi.com (56),
  ncbi.nlm.nih.gov (50), wiley.com (48), hdl.handle.net (42),
  academic.oup.com (27), figshare.com (26), tandfonline.com (17).

### Estado global de §7.3

- 2347 pasaron la Etapa 1.
- **698 confirmados `include`** tras cribado de texto completo (subconjunto ya accesible, verificado por el usuario).
- 62 excluidos en texto completo (verificados).
- **903 excluidos por I5** (sin acceso abierto confirmado).
- **684 pendientes de acceso manual** por el usuario (de acceso abierto confirmado, descarga automática bloqueada) — una vez conseguido el texto, se criban con el mismo procedimiento (extracto + lote de IA + verificación humana dirigida).

## 7.4 Control de consistencia intra-evaluador / auditoría del director — pendiente
