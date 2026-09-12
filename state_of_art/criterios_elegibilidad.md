# Criterios de elegibilidad (Fase 1)

**Protocolo de referencia:** `protocolo_estado_del_arte.md`, §3
**Preguntas de revisión:** `preguntas_revision.md` (PR1–PR5)
**Estado:** v1.1 — aprobado con modificaciones respecto al borrador del protocolo

## 3.1 Criterios de inclusión

- **I1.** El trabajo aborda representación de datos funcionales mediante
  sistemas de bases, análisis de componentes principales funcionales, o
  aplicación de FDA a series económicas/financieras.
- **I2.** Publicado en revista con revisión por pares, capítulo de libro
  académico, libro de referencia, actas de congreso indexado, o preprint en
  arXiv con calidad verificable.
- **I3.** Ventana temporal: **1997–2026, sin excepciones.**
- **I4.** Idiomas: inglés, español, portugués, francés.
- **I5.** Texto completo de **acceso abierto** (ver nota v1.1 abajo).

## 3.2 Criterios de exclusión

- **E1.** Trabajos que usan FDA como herramienta accesoria sin discutir la
  elección de base ni la calidad de la representación.
- **E2.** Material divulgativo, entradas de blog, notas de curso sin
  revisión, contenido de IA generativa sin autoría verificable.
- **E3.** Duplicados (se conserva la versión de registro: publicación en
  revista sobre preprint).
- **E4.** Trabajos cuyo único aporte es una aplicación de FDA a un dominio
  ajeno (medicina, meteorología), salvo que contengan una discusión
  metodológica sustantiva sobre la base empleada.
- **E5.** Actas de congreso local sin revisión por pares documentada.
- **E6.** Fuentes latinoamericanas no indexadas (SciELO, Redalyc,
  repositorios institucionales) que no satisfagan I2 por sí mismas — ver
  §3.3.

## 3.3 Tratamiento de la literatura latinoamericana no indexada

**Se excluye totalmente.** No se aplica un criterio de calidad sustitutivo
para fuentes regionales: toda fuente, incluidas las latinoamericanas, debe
satisfacer I2 (revisión por pares / libro académico / actas indexadas /
preprint de calidad verificable) igual que cualquier otra. No se usa la
etiqueta `indexacion = regional` en la matriz de extracción.

**Consecuencia para PR5.** La cobertura del contexto regional (América
Latina y Ecuador) dependerá exclusivamente de literatura indexada. Si esta
resulta escasa, esa escasez pasa a formar parte del argumento del vacío de
investigación (§11.3, "lo ausente") en lugar de completarse con fuentes no
indexadas.

## 3.4 Tratamiento de trabajos fundacionales pre-1997

Los trabajos fundacionales anteriores a 1997 (Grenander 1950; Rao 1958;
Karhunen; Loève; Daubechies 1988/1992; Donoho & Johnstone 1994; Eilers &
Marx 1996) **no se incluyen en la revisión del estado del arte.** Se ubican
en el Marco Teórico (`chapters/fundamentals.tex`), donde corresponden
conceptualmente.

## 3.5 Restricción de I5 a acceso abierto (v1.1)

**I5 se restringe a acceso abierto legal** (Unpaywall/Semantic Scholar
confirmando `is_oa=true`, o preprint de arXiv): dado el volumen de
literatura ya disponible tras la Fase 5 §7.2 (2347 ítems que superaron el
cribado título/resumen, muy por encima de lo manejable en una tesis de
pregrado), el autor y su director acordaron **no perseguir texto completo
por vías de acceso restringido** (préstamo interbibliotecario, CEDIA,
contacto con autores) — la biblioteca de Yachay Tech ya tiene cobertura
limitada (`fuentes_informacion.md`), y la literatura de acceso abierto
alcanza para sustentar la revisión.

**Precisión importante:** "acceso abierto" se define por el **estatus
legal/de licencia** del trabajo (confirmado por Unpaywall/Semantic
Scholar/arXiv), no por si la descarga automatizada tuvo éxito. Un ítem OA
cuya descarga automática falló por un muro anti-bot editorial (Elsevier,
Wiley, MDPI, SAGE, etc. — ver `cribado.md` §7.3) sigue siendo elegible;
simplemente requiere que el autor lo abra manualmente en su navegador. Solo
los ítems sin estatus de acceso abierto confirmado se excluyen por I5.

**Consecuencia para el cribado ya ejecutado:** los 903 ítems de §7.3 sin
OA detectado quedan excluidos por I5. Los 683 ítems con OA confirmado pero
bloqueados en la descarga automática (más el id 1187, con el mismo
estatus) permanecen en alcance, pendientes de acceso manual por el autor.
Detalle completo en `cribado.md` §7.3.

## Cambios respecto al borrador del protocolo

- **I3**: se eliminó la excepción para trabajos fundacionales pre-1997; la
  ventana 1997–2026 se aplica sin excepción dentro del estado del arte.
- **§3.3**: se reemplazó la regla de criterio de calidad sustitutivo por
  exclusión total de fuentes latinoamericanas no indexadas.
- **E6** (nuevo): codifica explícitamente la exclusión de §3.3 para que
  quede registrada en el cribado (Fase 5) con su propio código de motivo.
- **I5** (v1.1): restringido a acceso abierto legal, no a "accesible por
  cualquier vía" — ver §3.5.

## Historial de versiones

| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-08-28 | Versión inicial, adaptada del protocolo con dos modificaciones (I3 sin excepciones; exclusión total de fuentes regionales no indexadas) | Decisión del autor: separar fundamentos teóricos del estado del arte, y restringir el estado del arte a literatura indexada |
| 1.1 | 2026-09-12 | I5 restringido a acceso abierto legal (no persigue préstamo interbibliotecario/CEDIA/contacto con autores) | Decisión conjunta del autor y su director de tesis, dado el gran volumen de literatura ya disponible tras §7.2 (2347 ítems) |
