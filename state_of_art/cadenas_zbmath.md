# Cadenas de búsqueda — sintaxis zbMATH Open (Fase 4)

**Protocolo de referencia:** `protocolo_estado_del_arte.md`, §5–§6
**Cadenas congeladas en Scopus (base para esta traducción):** `cadenas_scopus.md`
**Fuentes de información:** `fuentes_informacion.md` (v1.1 — acceso abierto, sin suscripción)
**Bitácora de ejecución:** `bitacora_busqueda.numbers`

## Sintaxis verificada (vía `General Help - zbMATH Open`, documentación oficial)

A diferencia de Scopus/WoS, zbMATH **no usa las palabras "and"/"or"** como
operadores — usa símbolos. Usar las palabras literales no da error, pero
las trata como texto de búsqueda, produciendo resultados incorrectos sin
avisar (esto costó varias rondas de diagnóstico).

| Operador | Significado |
|---|---|
| `a & b` | Y lógico (AND) — por defecto entre varios términos |
| `a \| b` | O lógico (OR) |
| `!ab` | NO lógico (NOT) |
| `abc*` | comodín, **solo a la derecha** (no hay comodín de un carácter tipo `?`) |
| `"ab c"` | frase exacta |
| `(ab c)` | agrupación de términos |

Campos relevantes: `any:` (busca en ab, au, cc, en, rv, so, ti, ut — **ya
incluye `cc:`**), `ti:` (título), `au:` (autor), `py:` (año, con rango
`py:1997-2026`), `cc:` (código MSC — usar solo, sin `any:`, para restringir
por clasificación explícitamente).

**Lección clave:** `cc:` es más restrictivo de lo esperado — muchos
trabajos genuinamente relevantes no están clasificados bajo el código MSC
"obvio" (ver más abajo, #6 no está bajo 62R10 pese a ser un libro central
de wavelets en FDA). Preferir texto libre (`any:`) sobre restricción por
`cc:`, salvo que el volumen lo obligue.

## Estado de indexación en zbMATH (independiente de Scopus)

La cobertura de zbMATH es distinta a la de Scopus — mejor en libros de
matemática, pero no necesariamente mejor en artículos aplicados. Cada
ítem del conjunto oro se verificó de forma independiente, sin asumir el
estado de Scopus (`cadenas_busqueda.md` §5.1):

| Ítem | Indexado en zbMATH | Notas |
|---|---|---|
| #1 (Ramsay & Silverman 2005) | ✅ Sí | No recuperado por C1 — obra general sin término de familia de base, mismo patrón que #2 en Scopus |
| #3 (Wang, Chiou & Müller 2016) | ❌ No | Tampoco estaba en Scopus — posible problema de indexación de esta revista en general |
| #4 (Ferraty & Vieu 2006) | ✅ Sí | ✅ Recuperado por C1 |
| #6 (Morettin, Pinheiro & Vidakovic 2017) | ✅ Sí | ✅ Recuperado por C1 (texto libre); **no** recuperado si se restringe por `cc:62R10` — no está clasificado bajo ese código pese a ser sobre wavelets en FDA |
| #7 (Percival & Walden 2000) | ✅ Sí | No recuperado por C1 — título sin frase de dominio FDA ("Wavelet Methods for **Time Series** Analysis"), nunca fue un buen candidato de anclaje para este tema |
| #9a (Aguilera et al. 2021) | ✅ Sí | ✅ Recuperado por C1 |
| #9b (Aguilera & Aguilera-Morillo 2013) | ❌ No | Confirmado no indexado en zbMATH (verificado por título exacto) |
| #9c (Escabias, Aguilera & Aguilera-Morillo 2014) | ✅ Sí | ✅ Recuperado por C1 |

## C1 — PR1, PR2 — ✅ CONGELADA (2026-08-29, 806 resultados)

```
any:(basis* | spline* | Fourier | wavelet*) & any:("functional data analysis" | "functional data" | "functional principal component*" | FPCA) & py:1997-2026
```

**Historial de calibración:**
1. Primer intento, restringido por clasificación: `cc:62R10 & any:(basis* | spline* | Fourier | wavelet*)` → 235 resultados. Perdía #6 por completo (no clasificado bajo 62R10) y solo recuperaba #9a del resto — recall inaceptable.
2. Se abandonó la restricción `cc:` y se probó texto libre (ambos bloques con `any:`) → **806 resultados**.
3. Subconjunto relevante corregido para zbMATH = {#4, #6, #9a, #9c} (excluye #1 y #7, indexados pero sin vocabulario/framing esperado — mismo patrón que en Scopus; excluye #3 y #9b, no indexados en zbMATH). Recall = **4/4 = 100%**.
4. Se acepta 806 pese a superar ligeramente el umbral orientativo de 600: no hay un filtro de volumen seguro disponible (`cc:` demostradamente pierde cobertura relevante; filtrar por tipo de documento arriesgaría excluir libros como #6, que sí deben quedar incluidos).

**Sin filtro de año explícito probado aún en combinación** — `py:1997-2026`
añadido por consistencia con el resto de la Fase 4; no se ha verificado que
no excluya nada del conjunto oro (todos los ítems recuperados ya caen
dentro de esa ventana de todas formas).

## C2–C7

Pendientes. Mismo procedimiento: probar, revisar recall contra el
subconjunto zbMATH-específico (verificando primero si cada ítem está
indexado aquí en absoluto, sin asumir el estado de Scopus), ajustar, y
congelar.
