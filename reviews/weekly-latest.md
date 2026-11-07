# Meta-revisión semanal · 2026-11-02 a 2026-11-06

Semana de un solo catalizador dominando todo: la elección de medio término en EEUU (martes
3-nov). La reacción inicial fue contenida martes-miércoles (ES/GC/YM giraron a largo el
miércoles por la noche con 4+ horas de cierres de 1h sostenidos), pero el jueves llegó la
reacción tardía y violenta: derrota del oficialismo, VIX +69.7% en backwardation, selloff
histórico en los índices (NQ -6.89%/ES -4.83%/YM -4.05% en 24h) y CL +3.4% sin catalizador
propio (cobertura de cortos, COT crowded-short p10). El viernes fue el rebote post-crash más
violento del ciclo, sin reclamar los flips de 1h. Esta semana sí llegaron las 5
`reviews/<fecha>.md` completas (incluida la del viernes, calificada formal el mismo sábado de
madrugada): no hubo el hueco habitual del viernes.

## Marcador de la semana por instrumento

(`biasHitPct`/`scenarioAHitPct`/`zoneHitPct` = ventana rodante `hitLog`, 47 días a 2026-11-06;
"EM semana" = % de las 15 oportunidades sesión×día de esta semana específica dentro de banda,
de `grades/<fecha>.json`; ▲/▼ contra `reviews/2026-10-31-semana.md`.)

- **NQ**: sesgo 47% (n=106) ▲ vs 46% · escenario A 49% (n=88) ▲ vs 46% · zona 24% (n=58) ▲ vs
  23% · EM esta semana 53% (8/15) ▲▲ vs 31% (4/13) la semana pasada, el único que mejoró en EM.
  Giró de corto a rebote violento el viernes sin reclamar el flip 27701.50; cierra la semana en
  el día 8 de un corto que por fin tuvo la primera grieta real.
- **ES**: sesgo 44% (n=103) ▼ vs 45% · escenario A 45% (n=94) ▲ vs 42% · zona 26% (n=53) ▲ vs
  23% · EM esta semana 40% (6/15) ▼ vs 54%. El peor marcador de sesgo de los 5 (único bajo
  45%): giró a largo el miércoles y lo perdió con la misma autoridad el jueves, un día después.
- **GC**: sesgo 49% (n=99) ▼ vs 51% · escenario A 46% (n=97) ▲ vs 42% · zona 27% (n=60) flat ·
  EM esta semana 33% (5/15) ▼ vs 46%. El único instrumento que no se contagió del crash
  (+0.63% en 24h el jueves); hoy su propio checklist diario/4h giró a alcista.
- **YM**: sesgo 51% (n=88) ▼ vs 52% · escenario A 59% (n=100) flat · zona 19% (n=54) flat · EM
  esta semana 27% (4/15) ▼▼ vs 62%, la peor caída de los 5. El giro a largo del miércoles
  (perdió su propio ONH) se rompió el jueves con el reversal más violento del complejo
  (-2390pts en NY) y el viernes volvió a fallar con fuerza (+362pts, extreme_range_unresolved).
- **CL**: sesgo 57% (n=99) ▼ vs 58% · escenario A 52% (n=106) ▼ vs 54% · zona 20% (n=56) flat ·
  EM esta semana 27% (4/15) ▼ vs 54%. El más estable direccionalmente (corto de fondo confirmado
  toda la semana con autoridad extrema el lunes), pero el escenario A y el EM también se
  resintieron en una semana de volatilidad ajena a su propio ritmo.
- **Global**: `predictionScore` ponderado 57.6% (n=2535) ▼ leve vs 58.2% (n=2431). `errPctAtr`
  (nunca `emErrorTicks` en bruto): NQ 23.4% · ES 21.5% · GC 22.9% · YM 23.3% · CL 23.0%, pareja
  entre instrumentos y ▼ mejora vs el rango 24-28% de la semana pasada en la ventana rodante
  (aunque la semana puntual de EM, arriba, fue la peor en 4 de 5 símbolos: el error rodante se
  suaviza con muestra vieja, el error del día de shock fue mucho mayor).

## Dónde falló y lo que mejor paga

Blind spots con más muestra: `scenA|ALL|news=none` 39% (n=102, vs 50% promedio): el escenario A
rinde peor precisamente cuando NO hay noticia de alto impacto, quizás porque sin catalizador el
precio deambula más de lo que el escenario anticipa. `zone|ALL|whipsaw=low` 13% (n=67, vs 23%
promedio): las zonas con `whipsawRisk` bajo casi no funcionan, contraintuitivo (se esperaría
mejor hit-rate con menos chop). `bias|ES|calendar=major` 31% (n=51, vs 44% promedio): ES falla
más en semanas con calendario mayor, exactamente el tipo de semana que fue ésta. Mejores
fortalezas: `bias|CL|conviction=baja` 70% (n=52) y `bias|CL|calendar=normal` 68% (n=47), ambos
siguen siendo los más confiables del bus. Ninguno de estos tres blind spots coincide
textualmente con los de `reviews/2026-10-31-semana.md`; no dispara ningún `overrides` nuevo de
convicción esta semana.

## Expectativa en R

Primera lectura limpia (`python3 method/weekly_r.py`): plan -0.25R (n=24, winRate 17%) · tú
+1.91R (n=36, winRate 36%) · brecha -2.16R, invertida: esta semana la ejecución real superó al
plan de zonas, que tuvo un mal ciclo de disparos (muchas zonas golpeadas/rotas en el crash sin
pagar). Partido por clase: contra-sesgo +3.95R (n=10, 40% ganador) · fuera de zona +1.12R (n=26,
35% ganador) · cero trades dentro de una zona real del plan esta semana. Sin número de la
semana pasada para comparar (llegó sin dato limpio): se toma como primera referencia, no como
tendencia todavía.

## Plan vs ejecución

De `method/plan_vs_exec.py` sobre esta ventana: 36 posiciones reales, todas en NQ (vía índice
NAS100). 0 posiciones in-plan, 26 fuera de zona (36% ganador, +2.07pts promedio), 10 contra el
sesgo del plan (40% ganador, +43.49pts promedio). Dicho simple: lo contra-sesgo ganó más que lo
fuera de zona esta semana, y nada estuvo dentro de una zona real del plan: no hay con qué medir
si "en plan" paga más, porque esta semana no hubo ningún trade en plan.

## Contexto fuera del gráfico

El calendario explicó casi todo con un solo evento: la elección de medio término (martes
3-nov). Reacción inicial contenida martes-miércoles, reacción tardía y violenta el jueves
(derrota del oficialismo, selloff histórico, VIX +69.7%) y rebote post-crash el viernes (con
NFP de fondo, sin romper el extremo). El `crossAsset.tone` de riesgo-off del jueves fue a favor
del resultado bajista en NQ/ES/YM pero GC no se contagió y CL extendió su propio rally de Irán
sin relación con la elección.

## Ejecución de la semana

`live/journal.json` solo trae dato para lunes-martes-miércoles (2026-11-02/03/04); jueves y
viernes, justo el día del crash y el del rebote más violento, siguen sin refrescar desde
2026-11-04T15:21Z. De los 3 días con dato: **0/3 disciplinados** (▼ feo vs 2/3 la semana
pasada), contra-sesgo 42% (10/24 graded) ▲ vs 33% la semana pasada y 32% del rollup, sin
trades clasificados con edge (0/0). Overtrade 2/3 (▲ vs 1/3) y revenge 2/3 (igual). Peor racha
de pérdidas: 8 (lunes), muy por encima de las 3 de la semana pasada. Calidad de salida: **0
parciales** de 36 posiciones (9ª+ semana seguida sin cobrar un solo parcial), `fullStopRate`
58% (21/36) ▲ vs 53% del rollup de 45 días. Lectura: la disciplina empeoró con fuerza esta
semana, revenge y overtrade mandan, y faltan justo los dos días más caros del ciclo (el crash
del jueves y el rebote del viernes) para saber si de verdad fue tan malo como luce.

## Perfil del trader

`state/trader-profile.json` bloque `observed` reescrito con la ventana de esta semana (ver
abajo). `exitBaseline` refrescado desde `../scalp-cc-bus/exit-baseline.json` (asOf
2026-11-07): NQ n=9620 (antes 8485), hit1R 33.1% (igual), stoppedOut 47.6% (-0.2pp),
reachedTP2 5.0% (+0.1pp), mismo tono, sin cambio real. La ejecución de la semana no contradice
ningún `patterns[]` existente (overtrade-chop y revenge-after-sl siguen siendo exactamente las
fugas que se vieron); no hay patrón nuevo que proponer en `## Propuestas de método`.

## Qué se repitió

1. **0 parciales cobrados**, ya 9+ semanas seguidas: `homerun-exit` sigue sin ningún alivio.
2. **El bucket AGOTADO sigue sin limitar el EM en días de shock real**: el jueves del crash,
   NQ/ES/YM volaron 1.9x-2.8x el techo de banda en NY, el mismo patrón generalizado a varios
   símbolos el mismo día que ya se vio la semana pasada (30-oct). 2ª semana consecutiva con
   la misma forma de fallo.
3. **GC volvió a ser el instrumento más resiliente**, 3ª semana seguida en que se destaca por
   no seguir al resto del complejo en el movimiento dominante.

## Cambios de la semana

### Auto-aplicables

Sin cambios nuevos esta semana:
- `predictionSkip`: `NQ|direction` (rate=0.4143, n=35) y `NQ|scenario` (rate=0.4085, n=59)
  quedaron por primera vez ARRIBA de 0.40 con muestra fresca (antes `NQ|direction` estaba en
  0.3971 n=34, y `NQ|scenario` llevaba 2 semanas con el mismo n sin dato nuevo). Falta
  confirmar una 2ª semana consecutiva de muestra fresca sobre el umbral para retirar el
  override; se mantiene una semana más en los dos casos. `GC|range` (rate=0.3558, n=52) sigue
  bajo el umbral, sin cambio.
- `convictionBar4`: ningún símbolo llega a `n≥20` en el bucket "alta" (máximo NQ n=8). Sin
  cambio.
- `zonePriors`: mismo bloqueo que las 2 semanas pasadas (3ª semana igual): `state.zones` sigue
  sin guardar el conteo crudo pre-encogimiento por arquetipo puro. Sin cambio.

### Propuestas de método

1. **El bucket AGOTADO sigue sin limitar el reparto de EM en días de shock real**, reforzado
   esta semana (NQ 1.9x, ES 2.8x, YM 2.5x el techo de banda en NY del jueves 11-05), 2ª semana
   consecutiva con el mismo patrón en varios símbolos el mismo día. Propuesta (repetida de
   `reviews/2026-10-31-semana.md`, ahora con más evidencia): subir el `mult` de
   `emCalibration` para la celda AGOTADO en vez de dejarlo como excepción por símbolo. Campo:
   `method/instructions.md` sección 2 y `state.scorecard.emCalibration.mult`.
2. **Un giro de tesis reciente (≤2 días) resultó muy frágil frente a un shock opuesto igual de
   fuerte**: ES e YM rompieron su giro alcista del 11-04 (formado con 4+ horas de cierres de
   1h) con la misma autoridad el 11-05. Evidencia todavía fina (n=1 ciclo, hipótesis
   `H-2026-11-05-giro-reciente-se-rompe-con-shock` abierta). Propuesta: capar la convicción de
   cualquier giro con `daysHeld≤2` a "media" como máximo hasta que resista una prueba real.
   Campo: `method/instructions.md` sección 3.1 (`frameConflict`/`convictionCalibration`). No
   aplicar todavía, vigilar la próxima ocurrencia.
3. **ES necesita más peso a su propio SMT cuando diverge del extremo de NQ**: 2 instancias
   esta semana (11-03 Londres/NY y 11-06 completo) donde el SMT propio de ES ya avisaba y el
   plan no le dio suficiente peso, coincidiendo con el peor marcador de sesgo de los 5 esta
   semana (44%). Campo: `method/instructions.md` sección 3 (lectura de sesgo/SMT por
   instrumento).

## Lección de la semana

Una sola elección rompió 2 tesis de varios días (ES, YM) con un día de retraso, y el bucket
AGOTADO más la banda de EM otra vez se quedaron cortos en el día de mayor estiramiento del
ciclo; GC volvió a ser el único resiliente. La ejecución real, sin embargo, ganó más que el
propio plan esta semana (+1.91R vs -0.25R), con 0% de disciplina de fondo y sin un solo trade
dentro de zona: el gap no siempre corre en contra de Jesus, pero la fuga de comportamiento
(revenge, overtrade, cero parciales) sigue intacta debajo del resultado en puntos.

## Régimen: cómo entró y cómo sale cada instrumento

- **NQ**: entró en el día 6-7 de un corto de máxima autoridad, lo extendió con un día de
  tendencia completo el lunes, probó una ruptura alcista martes-miércoles sin reclamo
  sostenido, confirmó con el crash del jueves (el estiramiento mayor del ciclo) y el viernes
  montó el rebote más violento del tramo sin reclamar el flip de 1h 27701.50. Sale en CHOP
  tras el reversal, la primera pausa real del corto.
- **ES**: mismo guion con un día de retraso, giró a largo el miércoles rompiendo su invalidación
  de 5 días con autoridad, lo perdió en un solo día con el crash del jueves (reinicia el corto,
  `daysHeld=1`) y el viernes volvió a fallar el sesgo las 3 sesiones, la peor tarjeta de la
  semana. Sale en CHOP tras el reversal, sin reclamo todavía.
- **GC**: entró con la racha de resiliencia, rompió a largo el miércoles, fue el único que no
  participó del crash del jueves (+0.63% en 24h) y el viernes su propio checklist diario/4h
  giró a alcista. Sale la semana el más resiliente del grupo, en balance más que en tendencia.
- **YM**: entró en sesgo corto, rompió su propio ONH el miércoles con la mayor autoridad del
  complejo, lo perdió el jueves con el reversal más violento (-2390pts en NY) y el viernes
  volvió a fallar con fuerza (+362pts). Sale en `extreme_range_unresolved`, el instrumento más
  volátil sin resolución neta clara.
- **CL**: entró confirmando el corto de fondo con autoridad extrema el lunes (titular de paz de
  Irán rompiendo el soporte semanal), extendió con fuerza el martes y se mantuvo ajeno al drama
  electoral toda la semana, enfriando el rally de Irán el viernes. Sale confirmado bajista, el
  más estable direccionalmente de los 5, aunque su escenario A y su EM también se resintieron
  esta semana.
