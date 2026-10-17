# Meta-revisión semanal · 2026-10-12 a 2026-10-16

Ventana: lunes 10-12 a viernes 10-16, los 5 días con cierre completo calificado
(`reviews/2026-10-12.md` a `2026-10-16.md`) — primera semana en varias en que el viernes
llegó con cierre pleno sin retraso del scheduler. Semana con 2 catalizadores grandes: el CPI
del miércoles 10-14 (el día más violento del mes en el momento, 183-199% ATR en índices) y el
viernes de OpEx mensual 10-16 (lo superó: 200% ATR en NQ, el rango más extendido de toda la
serie).

## Marcador de la semana por instrumento

(cifras = `scorecard` rodante, corte hasta el viernes 10-16; ▲/▼ contra
`reviews/2026-10-10-semana.md`.)

- **NQ**: sesgo 52% (n=53) ▲ vs 48% · escenario A 30% (n=57) plano (sigue bajo el piso de
  30%, candidato débil) · predictionScore ~49.3% (n=308) ▼ leve vs ~49.6% · `emErrorTicks`
  sigue congelado en 459.7tk (n=48), sin un dato nuevo desde antes del 10-06 (3ª semana
  seguida) — sigue siendo, con mucha diferencia, el peor calibrado del complejo. Semana de
  extremos: el conflicto de marcos más largo del bus se resolvió del todo a la baja — CPI el
  martes (183% ATR), reclamo violento el miércoles que llegó a EVOLUCIONAR sin romper la tesis,
  y el viernes de OpEx confirmó bajista con el rango más extendido medido (200% ATR, nuevo
  mínimo de ciclo 29268.75). Cierra CONFIRMADA bajista día 7.
- **ES**: sesgo 54% (n=47) ▼ vs 57% · escenario A 38% (n=56) plano, sin dato nuevo esta semana
  · predictionScore ~52.4% (n=336) ▼ leve vs ~53.2% · `emErrorTicks` congelado en 73.3tk
  (n=47), igual sin dato nuevo (sigue el mejor calibrado). La tesis alcista de varias sesiones
  se ROMPIÓ del todo el martes con el CPI (cierre 55pts bajo su invalidación) y confirmó
  bajista el viernes con nuevo mínimo de ciclo 7676.00, el 7º fallo del mismo cluster premium.
- **GC**: sesgo 51% (n=48) ▼ leve vs 52% · escenario A 30% (n=56) ▲ leve vs 29% (sigue
  candidato débil) · predictionScore ~51.4% (n=310) ▲ vs ~49.6% · `emErrorTicks` congelado en
  272.1tk (n=47), 2º peor del complejo, sin dato nuevo. La semana más indecisa del bus: los 5
  marcos alinearon bajistas por primera vez el martes, el realineamiento no sostuvo ni 1
  sesión (nueva hipótesis `H-2026-10-15-gc-realineamiento-no-sostiene`), y cierra el viernes en
  chop confirmado sin que el marco de fondo se mueva.
- **YM**: sesgo 63% (n=39) plano · escenario A 42% (n=53) ▲ leve vs 40% · predictionScore
  ~56.6% (n=282) ▲ vs ~55.1%, el mejor del grupo · `emErrorTicks` congelado en 153.7tk (n=43),
  sin dato nuevo. El régimen más violento del complejo otra vez: repitió 2 veces el patrón de
  barrer un nivel de decisión y reclamarlo sin cerrar sostenido debajo (refuerza
  `H-2026-10-13-ym-giveback-sin-invalidar`), y el viernes de OpEx hizo el round-trip más grande
  medido en el instrumento (758pts, 129% del ATR) sin resolución neta clara al cierre.
- **CL**: sesgo 58% (n=48) ▼ leve vs 59% · escenario A 42% (n=53) plano · predictionScore
  ~50.5% (n=292) ▲ vs ~48.2% · `emErrorTicks` congelado en 103.3tk (n=43), sin dato nuevo (el
  mejor calibrado del complejo aun así). El instrumento más limpio de la semana: extendió la
  racha alcista a 9 sesiones sin una sola fisura real, y el único riesgo pendiente (la VAH
  congestionada) se resolvió por fin jueves-viernes con máximos de ciclo sucesivos
  (96.06 → 99.34).
- **Global**: predictionScore ponderado ~52.0% (n=1528) ▲ vs ~51.2% (n=1332) — mejora por 2ª
  semana consecutiva, sostenida casi solo por GC/YM/CL (NQ/ES retroceden levemente). **EM en
  banda**: sin tracker agregado explícito; en los hechos fue la peor semana de la serie en este
  punto — CPI (martes-miércoles) y OpEx (viernes) rompieron la banda alta en los 3 índices casi
  todos los días (NQ 200% ATR, ES 177-199%, YM 129-130%); solo GC y CL se mantuvieron dentro de
  rango razonable la mayor parte de la semana.

## Ejecución de la semana

Primera semana en varias con los 5 días cubiertos por `live/journal.json` (antes había huecos
de 3-4 días seguidos). Solo 1/5 días disciplinados (miércoles 10-14, día del CPI, el más limpio
en disciplina de la semana) — ▲ vs la semana pasada (0 de 1 día con dato). El rollup rodante (33
días) queda plano: disciplinado 15%, contra-sesgo 33%, fuera de zona 52% — la muestra `graded`
de la semana es mínima (2 trades, el jueves 10-15, 100% contra-sesgo) y no alcanza para decir si
la fuga de nivel/sesgo mejora o empeora esta semana en particular.

La calidad de salida sí tiene muestra completa: 44 posiciones en la semana, **0 parciales**
(0%, 5ª+ semana seguida sin cobrar un solo parcial), 1 scratch (2%), 29 stops completos (66%, ▲
peor que el 49% rodante) — la fuga `homerun-exit` sigue dominando sin alivio.
El jueves 10-15 fue además el peor día de disciplina de la ventana reciente: 37 trades con
overtrade+revenge+roundTrip juntos (los 3 flags a la vez, solo visto antes el 2026-09-01) y
racha de 8 pérdidas seguidas — justo el día más violento del mes en precio hasta ese momento, la
peor combinación posible. El viernes de OpEx (10-16) repitió los 3 flags de churn pero con
wlPtsRatio favorable (5.48) — mezcla rara de indisciplina con buen ratio cuando gana.

## Qué se repitió

Dos patrones de **tracking**, no de mercado: (1) `emErrorTicks`/`emCalibration` lleva 3 semanas
sin un solo dato nuevo en los 5 símbolos (misma `n` exacta que hace 2 semanas) mientras
`biasHitPct`/`scenarioAHitPct`/`zoneHitPct` sí se "retomaron" el 10-15 con 3 sesiones nuevas —
el sub-objeto de error de rango se quedó atrás específicamente. (2) `scorecard.execution.ALL`
tampoco incrementó con 10-11, 10-13, 10-15 ni 10-16 (se quedó en `days:14`, última entrada
10-14) aunque esos días ya tienen datos en `live/journal.json` y los propios
`reviews/<fecha>.md` ya los citan en prosa (10-13: "4 trades, 0 graded"; 10-15: "37 trades,
racha de 8 pérdidas") — el tracker del scorecard se desincronizó de lo que el propio review ya
tenía disponible. En mercado: la divergencia SMT entre YM y NQ/ES volvió a aparecer sin
resolverse (anotada el viernes como observación nueva para vigilar en los 3 instrumentos).

## Cambios de la semana

### Cambios aplicados

Ninguno esta semana — ninguna condición de la clase segura cruzó su umbral con la confirmación
de 2 semanas que exige el método:
- `predictionSkip`: 2 overrides vigentes entran en **vigilancia** por primera vez (no se
  retiran todavía, falta la 2ª semana de confirmación): `CL|range` subió a exactamente 0.40
  (n=30, justo el borde del umbral que lo mantenía aplicado) y `YM|range` subió a 0.4184
  (n=49), ambos por primera vez desde que se aplicaron. Si cualquiera se repite sobre 0.40 la
  próxima semana, se retira. El resto (`NQ|direction` 0.3788 n=33, `NQ|scenario` 0.3922 n=51,
  `GC|range` 0.2917 n=36) sigue firmemente bajo el umbral, sin cambio.
- `zonePriors`: los 3 arquetipos con override vigente (`bounce_val` 0.68, `golden_zone` 0.32,
  `retest_break` 0.45) recalculan dentro de ±0.08 de su valor actual con los datos de esta
  semana — ninguno diverge >0.10, sin cambio. `sweep_onl` (winN≈166, winRate agregado leaf
  ≈0.39 vs prior de reversión 0.55) se acerca al umbral de divergencia, pero igual que la
  semana del 10-10, `state.zones` no permite reconstruir el agregado sin el encogimiento ya
  aplicado — no se fuerza el ajuste sin esa base (ver propuesta 3 abajo).
- `convictionBar4`: ningún símbolo llega a `n≥20` en el bucket "alta" (máximo NQ n=7) — sin
  cambio.

### Propuestas de método

1. **`emErrorTicks`/`emCalibration` lleva 3 semanas sin un dato nuevo** en los 5 símbolos
   (misma `n`/`avgTk` exactos en `reviews/2026-10-03-semana.md`, `2026-10-10-semana.md` y esta
   corrida) mientras el resto del scorecard de mercado sí se actualiza. Propuesta: que cada
   `pre-asia` confirme explícitamente en su nota de cierre si incrementó `emErrorTicks` ese día
   (como ya hace con `zones`/`predictionScore`), para que un hueco de 2+ semanas sea visible de
   inmediato. Campo: `method/instructions.md` sección 6 (checklist de cierre) /
   `state.scorecard.emErrorTicks`.
2. **`scorecard.execution.ALL` se desincronizó de `live/journal.json`**: se quedó en
   `days:14` (última entrada 10-14) pese a que 10-11, 10-13, 10-15 y 10-16 ya tienen datos en
   `live/journal.json` y los propios reviews de esos días ya los citan. Propuesta: que la
   `pre-asia` incremente `scorecard.execution.ALL` con CADA día nuevo de `byDay` disponible, no
   solo cuando coincide con el día que califica, para que el rollup del scorecard no quede
   atrás del propio journal. Campo: `method/instructions.md` sección 6 /
   `state.scorecard.execution`.
3. **`sweep_onl` como candidato a override de `zonePriors`**: winN≈166 con winRate agregado
   leaf ≈0.39 vs el prior de reversión 0.55 (divergencia ≈0.16, sobre el umbral de 0.10), pero
   el cálculo necesita el agregado sin encoger para ser confiable (mismo bloqueo de la semana
   pasada). Propuesta: que `pre-asia` guarde, junto al `winRate` ya encogido de cada zona hoja,
   el conteo crudo pre-shrinkage (`rawHits`/`rawN`) para que el weekly pueda recalcular el
   agregado real del arquetipo sin este bloqueo recurrente. Campo: `method/instructions.md`
   sección 4 (pooling) / `state.zones[].winRate`.

## Lección de la semana

La semana con más violencia de precio del mes (CPI el martes, OpEx el viernes, 4 de 5
instrumentos rompiendo bandas de EM por mucho) coincidió con la peor racha de disciplina medida
en semanas (10-15: overtrade+revenge+roundTrip juntos + 8 pérdidas seguidas) — el patrón ya
visto el 2026-09-01 de que "volatilidad extrema + fuga de disciplina" se refuerzan mutuamente se
repitió en el punto más caro de la ventana reciente, y sigue sin un solo parcial cobrado en 44
posiciones.

## Régimen: cómo entró y cómo sale cada instrumento

- **NQ**: entró con el conflicto de marcos más largo de la serie, precio técnicamente bajista
  pero `command` fusionado fuerte en largo. El CPI del martes lo rompió con autoridad (183%
  ATR), el miércoles dio el reclamo más violento medido (120% ATR, estructura 1h/4h giró
  alcista) sin romper la tesis, y el viernes de OpEx la resolvió del todo a la baja con el rango
  más extendido de toda la serie (200% ATR, nuevo mínimo de ciclo 29268.75). Sale CONFIRMADA
  bajista día 7, con la divergencia SMT de YM como única duda abierta.
- **ES**: entró en continuación alcista de varias sesiones. El CPI del martes la rompió con
  autoridad (cierre 55pts bajo invalidación); miércoles-jueves quedó sin resolución neta clara,
  y el viernes (7º intento del mismo cluster premium) confirmó bajista con nuevo mínimo de
  ciclo 7676.00. Sale con tesis bajista día 1-2, la más reciente en romperse del complejo.
- **GC**: entró con sus marcos recién alineados bajistas tras 2 semanas de holdout. El martes
  confirmó con autoridad (los 5 marcos alineados por 1ª vez), pero el realineamiento no sostuvo
  ni 1 sesión (reclamo real el miércoles, nueva hipótesis registrada). Cierra la semana en chop
  confirmado, sin que el marco de fondo vuelva a moverse — el instrumento más indeciso del
  complejo.
- **YM**: entró en reinicio bajista ya puesto a prueba varias veces. El CPI lo resolvió bajista
  el martes, pero repitió 2 veces el patrón de barrer un nivel de decisión sin cerrar sostenido
  debajo, y cierra el viernes de OpEx con el round-trip más grande medido (758pts) sin
  resolución neta clara — el régimen más volátil y menos resuelto del complejo.
- **CL**: entró en racha alcista de 7 sesiones con la VAH congestionada como único riesgo
  pendiente. La resolvió jueves-viernes con máximos de ciclo sucesivos (96.06 → 99.34) sin una
  sola fisura real en 9 sesiones — sale como, con diferencia, el instrumento más limpio y menos
  dependiente de catalizador de calendario del complejo.
