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

## Eje 1 — Fundamentos de FDA y representación en bases (PR1)

*Borrador para calibrar tono/profundidad — 34 antecedentes directos de PR1
en `fase8/f8_matriz_extraccion.csv` filtrando por `PR1` en
`preguntas_que_responde` y `es_antecedente_directo=si`.*

La literatura revisada converge de forma marcada hacia las bases B-spline
como opción por defecto para representar datos funcionales: 30 de los 91
trabajos que usan una sola familia la eligen, frente a 5 que optan por
Fourier y solo 2 por wavelets. Pero esa convergencia numérica no refleja
un consenso metodológico: los propios autores del campo señalan
explícitamente esta tensión. Basna et al. (2022) describen la práctica
habitual como "una elección más bien ad hoc" entre Fourier, wavelets o
splines, y Eslami (2024) constata que "persiste un vacío notable en la
literatura respecto a comparaciones exhaustivas entre estas metodologías"
— dos trabajos de este mismo corpus, separados por dos años, formulan casi
la misma objeción: la elección de la base responde con más frecuencia a
la convención que a una justificación explícita.

Cuando los trabajos sí ofrecen una justificación teórica para su elección,
esta suele apoyarse en una propiedad estructural reconocible de los datos,
no en una comparación empírica. Shackleton et al. (2024) son explícitos al
respecto: prefieren B-splines sobre Fourier "debido a la aperiodicidad de
los datos", mientras que la literatura general reserva Fourier
precisamente para el caso contrario, señales periódicas (Nassar &
Podgórski, 2021). Las bases wavelet, por su parte, se justifican no por
periodicidad sino por localidad: Yang et al. (2022) y Amato et al. (2025)
las emplean específicamente para capturar discontinuidades o
características locales que una base global suaviza en exceso. Esta
correspondencia —periodicidad→Fourier, suavidad global→B-spline,
localidad/discontinuidad→wavelet— es el argumento teórico disponible en el
campo, pero rara vez se aplica de forma sistemática: la mayoría de los 91
trabajos revisados simplemente adopta B-spline sin discutir si la serie en
cuestión cumple la condición que en teoría la favorecería.

La minoría de trabajos que sí comparan familias de base directamente
(25/91, ver Tabla B) muestra que esta elección no es cosmética: los
resultados dependen fuertemente del dominio y no se generalizan de una
aplicación a otra. Kayano & Konishi (2009) encuentran que una base
radial gaussiana regularizada supera a B-splines en error cuadrático medio
para datos no balanceados; Pérez-Plaza et al. (2018) encuentran lo
contrario para curvas geodésicas GPS, donde P-splines superan a Fourier en
dos de tres componentes; Amato et al. (2025) reportan una brecha aún mayor
en clasificación de espectros, donde un método wavelet alcanza un índice
de Rand ajustado de 0.901 frente a apenas 0.320 de k-means sobre bases
B-spline. Esta heterogeneidad de resultados —ninguna familia domina de
forma universal— es precisamente lo que hace insostenible extrapolar la
conveniencia de B-spline (u otra familia) de un dominio a otro sin
evidencia propia: si el criterio de elección fuera trivial, los 25
trabajos comparativos no encontrarían ganadores distintos en cada
aplicación.

Una segunda línea de respuesta al mismo problema, más reciente (2018-2024),
no intenta elegir mejor entre las familias clásicas sino evitar la
elección: los métodos de completado de matrices de Descary & Panaretos
(2016, 2019) y las bases "splinets" de Nassar, Podgórski y Basna
(2021-2024) estiman una base ortonormal directamente de los datos, en
lugar de fijarla de antemano. Aguilera & Aguilera-Morillo (2013), en un
registro más cercano al de esta tesis, muestran que penalizar la base
(P-splines) importa tanto o más que la familia elegida, reduciendo el MSE
drásticamente frente a splines de regresión sin penalizar dentro de la
misma familia B-spline — un resultado que ya anticipa el Eje 3 de esta
síntesis: el efecto de la familia y el efecto del
régimen de suavizado no son la misma pregunta, y la literatura general de
FDA los empieza a separar. Lo que no hace, como se muestra en el Eje 5, es
separarlos para series económicas o financieras.

## Eje 2 — FPCA: fundamento, estimación y criterios de truncamiento (PR2)

*Borrador — 27 antecedentes directos de PR2 en la matriz.*

La evidencia más directa de que la elección de base condiciona los
resultados del FPCA no proviene de una comparación de familias en sí, sino
de un experimento controlado previo al análisis: Tarpey et al. (2007) ajustan
las mismas curvas con B-splines, Fourier y potencias, fijando la misma
dimensión p=5 en los tres casos para aislar el efecto de la familia, y
encuentran que "los resultados del agrupamiento k-means varían según cómo
se ajustaron las curvas a los datos". Es la comprobación empírica más
limpia del corpus de que PR2 tiene una respuesta afirmativa: no solo la
familia de base afecta el ajuste, afecta el análisis posterior que se
construye sobre ese ajuste. Una segunda fuente de variación, ortogonal a
la familia, es la propia formulación del FPCA: Hörmann et al. (2012)
muestran que una FPCA dinámica (en el dominio de la frecuencia) explica
más varianza que la FPCA estática con la misma base subyacente (80% frente
a 73% en su aplicación a contaminación por PM10) — el "cómo se calcula el
FPCA" compite con el "en qué base se representa la curva" como fuente de
diferencias en los resultados.

Si en el Eje 1 la elección de familia mostraba una convergencia parcial
hacia B-spline, el criterio para truncar esa base —cuántas funciones
retener— no muestra ninguna convergencia comparable. El corpus documenta
al menos ocho enfoques distintos en uso activo: GCV, AIC/BIC y sus
variantes, criterios de información generalizados (GIC, MAIC, GBIC),
selección bayesiana automática (variables latentes tipo Bernoulli en Sousa
et al., 2024; priors dispersos/variacionales en Tao et al., 2025),
criterios de razón de eigenvalores (Ahn & Horenstein, usado por Lin & Shang,
2025), umbrales de varianza explicada acumulada, y procedimientos bootstrap
a medida (Diks & Wouters, 2023). Beyaztas & Shang (2022) comparan
directamente cuatro de estos criterios (GCV, GIC, MAIC, GBIC) dentro del
mismo estudio y tratan la elección del criterio como una decisión de
diseño tan relevante como la familia de base misma — un recordatorio de
que "elegir bien la base" y "elegir bien cuántas funciones de esa base
usar" son dos decisiones independientes que rara vez se estudian por
separado.

Un antecedente aísla explícitamente esa independencia de un modo que
anticipa directamente el argumento central de esta tesis: Gao et al.
(2024) fijan deliberadamente una dimensión K grande en su base B-spline y
controlan la suavidad únicamente a través del parámetro de penalización,
en vez de seleccionar K por un criterio como GCV. Es, dentro del corpus,
el diseño metodológico más cercano a separar el efecto de la dimensión de
la base del efecto del régimen de suavizado — pero lo hace dentro de una
sola familia (B-spline), no como comparación entre familias, y no sobre
series económicas volátiles (ver Eje 5). Esta misma tensión entre
seleccionar automáticamente la dimensión o desacoplarla del suavizado se
presenta también, de otra manera, en el Eje 3.

## Eje 3 — Suavizado, penalización y selección de parámetros (PR3)

*Borrador — 21 antecedentes directos de PR3 en la matriz.*

La separación entre el efecto de la familia de bases y el efecto del
régimen de suavizado, que PR3 plantea como pregunta abierta, sí tiene
antecedentes dentro de una misma familia. Aguilera & Aguilera-Morillo
(2013) mantienen fija la familia B-spline y varían únicamente el tipo de
penalización —ninguna (regression splines), continua (smoothing splines)
y discreta (P-splines)— encontrando que ambos enfoques penalizados
reducen el error cuadrático medio de forma sustancial frente al caso sin
penalizar. Gao et al. (2024) llevan esta separación más lejos: fijan una
dimensión K grande y controlan la suavidad exclusivamente mediante el
parámetro de penalización, en lugar de seleccionar K por un criterio como
GCV. En ambos casos la familia de bases permanece constante; lo que varía
es el régimen de suavizado, y el efecto es medible y sustancial. Es
exactamente el tipo de diseño que PR3 pide, pero aplicado dentro de una
sola familia, no como comparación entre familias distintas, y no sobre
series económicas o financieras.

Cuando se examina cómo se selecciona en la práctica el parámetro de
suavizado (lambda), el criterio automático más citado, la validación
cruzada generalizada, no siempre funciona como se espera. Zin et al.
(2020) documentan un caso en el que ni GCV ni la validación cruzada
ordinaria produjeron un valor de lambda razonable, y los autores debieron
recurrir a una evaluación subjetiva del ajuste. Este resultado es
relevante para PR3 porque señala un límite práctico: si el criterio
automático de selección de lambda puede fallar, cualquier comparación
entre familias de bases que dependa de una selección automática y no
verificada del parámetro de suavizado corre el riesgo de confundir el
efecto de la familia con un artefacto de una mala selección de lambda.
Beyaztas & Shang (2022) son, dentro del corpus, quienes más se aproximan
a controlar ambas fuentes de variación a la vez: comparan tres familias de
base y, para cada una, cuatro criterios distintos de selección (GCV, GIC,
MAIC, GBIC), lo que permite separar en el análisis qué parte de la
diferencia observada proviene de la familia y qué parte del criterio de
selección. El dominio de aplicación es climático, no económico.

Un grupo más reciente de trabajos evita el problema en lugar de
resolverlo: en vez de seleccionar primero la dimensión de la base y luego,
por separado, el parámetro de suavizado, formulan ambas decisiones como
un único problema de inferencia bayesiana. Sousa et al. (2024), Wakayama &
Sugasawa (2022), Cruz et al. (2024) y Tao et al. (2025) usan priors de
contracción (horseshoe, spike-and-slab, priors dispersos vía inferencia
variacional) que seleccionan qué funciones de base retener y qué tanto
penalizarlas en el mismo paso de estimación. Esta unificación resuelve el
problema práctico de tener que ajustar dos parámetros por separado, pero
no responde a PR3 en el sentido que interesa a esta tesis: al fundir
ambas decisiones en un solo mecanismo, no permite aislar cuánto del
resultado se explica por la familia de bases elegida y cuánto por el
régimen de suavizado aplicado sobre ella.

De los 21 antecedentes directos de PR3, solo uno trabaja con series
económicas o financieras: Rice et al. (2023), sobre la volatilidad
funcional de futuros de petróleo crudo. Pero su forma de regularizar no es
la penalización de rugosidad que discuten los demás trabajos de este eje,
sino una restricción de no negatividad sobre bases construidas a partir de
los datos. Ningún antecedente de este corpus aplica a series económicas o
financieras el tipo de separación explícita entre familia de bases y
régimen de suavizado que sí existe, dentro de una sola familia, en
Aguilera & Aguilera-Morillo (2013) y Gao et al. (2024). El Eje 5 retoma
este punto.

## Eje 4 — Bases wavelet y procesos no suaves (PR4)

*Borrador — 14 antecedentes directos de PR4 en la matriz.*

PR4 pregunta por el desempeño de las bases wavelet frente a bases
polinómicas o trigonométricas en procesos no suaves o no estacionarios,
pero dentro de los 14 antecedentes directos de este eje, las aplicaciones
que efectivamente usan una base wavelet son minoría: solo Amato et al.
(2025) y Yang et al. (2022) la emplean como componente central de su
método. La mayoría de los trabajos que abordan procesos irregulares
responde a esa irregularidad sin recurrir a wavelets en absoluto, lo cual
es en sí mismo un dato relevante para PR4: la wavelet no es, en la
práctica reciente de este corpus, la respuesta por defecto a la falta de
suavidad que la teoría sugeriría.

Cuando la comparación directa sí se hace, el resultado no favorece a las
wavelets de forma sistemática. Amato et al. (2025) encuentran una ventaja
considerable del clustering basado en wavelets sobre bases B-spline
(índice de Rand ajustado de 0.901 frente a 0.320), pero Salvatore et al.
(2016) reportan lo contrario: un análisis con WPCA no reveló cambios
temporales adicionales a los que una FPCA basada en Fourier con
suavizado ya capturaba. Eslami (2024) describe splines y wavelets como
"complementarios", con desempeño similar en error cuadrático medio en uno
de sus casos de estudio, y señala explícitamente que la literatura carece
de comparaciones exhaustivas entre ambas familias. El patrón es el mismo
que en el Eje 1: ninguna familia domina de forma universal, y el resultado
depende del tipo de irregularidad presente en los datos.

La estrategia más frecuente entre los antecedentes de PR4 no es sustituir
la base suave por una wavelet, sino adaptar la base suave a la
irregularidad. Jiao et al. (2022) alinean la ubicación de las funciones de
base con el punto de cambio que buscan detectar, en lugar de fijar su
posición de antemano, y muestran que esa alineación mejora sustancialmente
la potencia de detección frente a una FPCA estándar. Horváth et al. (2020)
sustituyen la interpolación B-spline por polinomios cúbicos de Hermite
para curvas forward de materias primas, que presentan quiebres en los
puntos de vencimiento del contrato, y encuentran un mejor ajuste con esta
alternativa, también no wavelet. Aguilera & Aguilera-Morillo (2013) y Gao
et al. (2024), ya discutidos en el Eje 3, absorben la rugosidad mediante
el parámetro de penalización dentro de la misma familia B-spline, en vez
de cambiar de familia. Ninguna de estas tres estrategias usa wavelets;
todas modifican una base suave para acomodar la irregularidad.

Ninguno de los antecedentes de PR4 que comparan directamente wavelets
contra otras familias trabaja con series económicas o financieras. Los
dos antecedentes de este eje que sí lo hacen —Aue et al. (2017), sobre
retornos intradía del SPY, y Rice et al. (2023), sobre la volatilidad de
futuros de petróleo crudo— no ofrecen esa comparación: el primero
menciona las wavelets solo como una alternativa típica no probada en el
propio estudio, y el segundo regulariza mediante restricciones de
no negatividad, no mediante una base wavelet. La pregunta de PR4 no tiene,
por tanto, respuesta empírica directa para el dominio económico-financiero
dentro de la literatura revisada — otro punto que retoma el Eje 5.

## Eje 5 — FDA en economía y finanzas; antecedentes latinoamericanos y ecuatorianos (PR5)

*Borrador — 35 ítems tocan PR5; solo 11 (31%) son antecedentes directos.*

El análisis de datos funcionales está bien establecido como herramienta
aplicada en economía y finanzas: los 35 ítems de este eje cubren demanda
eléctrica, índices bursátiles, tipos de cambio, materias primas,
criptomonedas y distribución del ingreso. Pero esa amplitud de dominios
contrasta con la profundidad metodológica: solo 11 de los 35 (31%)
alcanzan el nivel de antecedente directo (Q3≥1 y Q4≥1), frente al 48% de
antecedentes directos en el corpus completo. La mayoría de las 24
aplicaciones restantes usa FDA como herramienta de análisis sin discutir
la elección de la base ni evaluar la calidad de la representación
obtenida —el mismo patrón de uso accesorio que ya se documentó como motivo
de exclusión (E1) durante el cribado de la Fase 5—, con puntuaciones
concentradas entre 0 y 4 sobre 8.

Entre los 11 antecedentes directos, ninguno aplica a series económicas o
financieras la separación entre efecto de familia y efecto de suavizado
que sí existe, dentro de una sola familia, en Aguilera & Aguilera-Morillo
(2013) y Gao et al. (2024) (Eje 3). Shackleton et al. (2024) justifican
teóricamente su elección de B-spline por la aperiodicidad de la
volatilidad realizada que estudian, pero no la comparan contra otra
familia. Rodríguez-Cuadro (2025), sobre el mercado bursátil colombiano,
combina P-splines con FPCA y clustering para caracterizar la correlación
funcional entre 26 empresas y el precio del petróleo Brent, pero tampoco
compara familias de base entre sí. Cada antecedente económico cumple
alguno de los cuatro criterios de valoración —justificación teórica,
parámetros reportados, evaluación de la representación—, pero ninguno
cumple los cuatro a la vez de la forma en que sí lo hacen, fuera del
dominio económico, Beyaztas & Shang (2022) o Aguilera & Aguilera-Morillo
(2013).

La cobertura regional es aún más limitada. De los 91 ítems del corpus,
solo tres tienen algún vínculo con América Latina: Marín et al. (2023),
sobre demanda eléctrica en Colombia; Rodríguez-Cuadro (2025), ya citado;
y el propio Padilla-Segarra et al. (2020), sobre indicadores demográficos
y económicos de la región. Ninguno de los 91 ítems recuperados por la
búsqueda sistemática trabaja específicamente con datos ecuatorianos. Esta
escasez no es un artefacto de las cadenas de búsqueda —la Fase 4 ya había
anticipado un volumen bajo para la cadena C6 (región)— sino un patrón que
se confirma ahora dentro del conjunto ya cribado y valorado por su
calidad metodológica: la literatura latinoamericana sobre FDA existe, pero
es escasa, y su intersección con la comparación de familias de bases es,
dentro de este corpus, vacía.

La formulación completa del vacío de investigación, apoyada en la
evidencia de los cinco ejes, se desarrolla en la sección siguiente.

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
