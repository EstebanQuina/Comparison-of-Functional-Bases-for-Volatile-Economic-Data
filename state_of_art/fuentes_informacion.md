# Fuentes de información (Fase 2)

**Protocolo de referencia:** `protocolo_estado_del_arte.md`, §4
**Criterios de elegibilidad:** `criterios_elegibilidad.md`
**Estado:** v1.1 — acceso institucional real verificado; ámbito de búsqueda ajustado en consecuencia

## 4.1 Bases de datos primarias (búsqueda sistemática con registro)

**Limitación de acceso documentada (2026-08-29).** La biblioteca de Yachay
Tech solo ofrece acceso institucional directo a **Scopus** entre las bases
listadas originalmente en el protocolo. El resto de bases suscritas por la
biblioteca (CAS SciFinder, Digitalia Hispánica, EBSCO eBooks) no aparecen
en el protocolo porque no son pertinentes para este tema (SciFinder es de
química; Digitalia Hispánica es de humanidades en español; EBSCO eBooks es
una colección de libros electrónicos, no una base de artículos con
búsqueda booleana avanzada) o requieren solicitar credenciales adicionales
a la biblioteca por un trámite aparte, fuera del alcance de esta revisión.

En consecuencia, la búsqueda sistemática se ejecuta sobre las bases
efectivamente accesibles: **Scopus** (acceso institucional) y tres bases de
**acceso abierto sin necesidad de suscripción** — arXiv, zbMATH Open (de
acceso abierto desde 2021) e IDEAS/RePEc. MathSciNet, ScienceDirect,
SpringerLink, Project Euclid y JSTOR quedan **excluidas de la búsqueda
sistemática por falta de acceso institucional**, no por decisión
metodológica — esta distinción debe quedar explícita en la tesis (nota de
limitación en la sección de metodología o en el Anexo A).

| Fuente | Cobertura relevante | Prioridad | Acceso |
|---|---|---|---|
| Scopus | Amplia, multidisciplinar | Alta | ✅ Institucional (Yachay Tech) — completada |
| zbMATH Open | Matemática, acceso abierto | Alta | ✅ Abierta (desde 2021) |
| arXiv (math.ST, stat.ME, stat.AP) | Trabajo reciente no publicado | Media | ✅ Abierta |
| IDEAS/RePEc | Aplicaciones económicas | Media | ✅ Abierta |
| Web of Science (Core Collection) | Amplia, complementaria a Scopus | Alta | ❌ Sin acceso institucional |
| MathSciNet | Matemática y estadística teórica | Alta | ❌ Sin acceso institucional |
| ScienceDirect | Texto completo Elsevier (CSDA, JMVA) | Media | ❌ Sin acceso institucional |
| SpringerLink | Libros de referencia de FDA | Media | ❌ Sin acceso institucional |
| Project Euclid | Annals of Statistics y afines | Media | ❌ Sin acceso institucional |
| JSTOR | Cobertura general de estadística/econometría, 1997–2026 | Baja | ❌ Sin acceso institucional |

## 4.2 Fuentes regionales

**Eliminada.** Esta subsección existía en el borrador del protocolo para
sondear SciELO, Redalyc, Latindex, RRAAE y repositorios institucionales
(ESPE, EPN, USFQ, Yachay Tech) bajo el criterio de calidad sustitutivo para
fuentes regionales no indexadas (antiguo §3.3). Ese criterio ya no existe
(`criterios_elegibilidad.md`, E6): toda fuente regional debe satisfacer I2
por sí misma, por lo que cualquier trabajo latinoamericano relevante
aparecerá — si existe — en las bases de datos primarias de §4.1.

## 4.3 Búsqueda manual dirigida

Revisión de índices de los últimos ~10 años en:

- Computational Statistics & Data Analysis
- Journal of Multivariate Analysis
- Annals of Applied Statistics
- Journal of the Royal Statistical Society, Series B
- Statistical Papers
- Advances in Data Analysis and Classification
- Journal of Nonparametric Statistics
- Econometrics and Statistics

Justificación: las cadenas booleanas fallan cuando los autores usan
vocabulario distinto al tuyo. El barrido manual de revistas nucleares
captura lo que la búsqueda sistemática pierde.

## Cambios respecto al borrador del protocolo

- **JSTOR**: se mantuvo en §4.1, pero se redefinió su propósito. En el
  borrador original figuraba únicamente para recuperar fuentes históricas
  pre-1997 (Rao 1958), que ahora se excluyen del estado del arte
  (`criterios_elegibilidad.md`, §3.4) y se ubican en el Marco Teórico. Se
  conserva como fuente general de baja prioridad para literatura de
  estadística/econometría dentro de la ventana 1997–2026.
- **§4.2 (fuentes regionales)**: eliminada en su totalidad, como
  consecuencia directa de la exclusión de fuentes latinoamericanas no
  indexadas decidida en la Fase 1.
- **§4.3**: sin cambios respecto al borrador del protocolo.
- **§4.1 (v1.1)**: acotado a las bases con acceso real verificado (Scopus +
  tres de acceso abierto). Las demás quedan documentadas como excluidas
  por falta de acceso institucional, no por decisión metodológica.

## Historial de versiones

| Versión | Fecha | Cambio | Motivo |
|---|---|---|---|
| 1.0 | 2026-08-28 | Versión inicial: JSTOR conservado con propósito redefinido; §4.2 eliminada | Consistencia con los criterios de elegibilidad de la Fase 1 |
| 1.1 | 2026-08-29 | Verificado acceso institucional real de la biblioteca de Yachay Tech: solo Scopus. Ámbito de búsqueda sistemática acotado a Scopus + arXiv + zbMATH Open + IDEAS/RePEc (acceso abierto); WoS/MathSciNet/ScienceDirect/SpringerLink/Project Euclid/JSTOR documentadas como excluidas por falta de acceso, no por decisión metodológica | Transparencia exigida por el protocolo (§14) ante una limitación real de acceso, no una elección de diseño |
