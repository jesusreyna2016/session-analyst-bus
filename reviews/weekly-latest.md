# Meta-revision semanal · 2026-11-16 a 2026-11-20

Semana de cinco catalizadores reales, uno por dia: lunes risk-off amplio sin evento de
calendario (VIX +24% en backwardation real, aceptacion del nombramiento de Warsh en la Fed)
dejo a los 5 instrumentos en corto, con el fade clasico de Asia fallando en los 5; martes GC
rompio su largo de 4 dias con un reclamo real del PWL, hizo una doble barrida sin autoridad y
recien en NY reinstalo un corto limpio (dia 1 de ciclo nuevo), mientras un titular de escalada
en el estrecho de Ormuz le gano una sesion al corto estructural de CL; miercoles las minutas
halconas del FOMC mas el desplome de NVDA tras resultados dieron el dia mas limpio del mes
(sesgo acertado en 12 de 15 sesiones, 80%) y, en paralelo, la peor racha de ejecucion
registrada hasta ahora (14 perdidas seguidas); jueves una cumbre Trump-Putin-Xi dio un salto
risk-on de hasta 6.9 ATR en NQ que la sesion de NY revirtio por completo, confirmando el corto
de fondo; viernes (OpEx) fue liquidacion generalizada sin catalizador de calendario claro, con
GC fallando como refugio (cayo junto a los indices) y CL como unica excepcion, revirtiendo con
autoridad desde un minimo de ciclo nuevo. El hallazgo operativo mas relevante de la semana: el
journal se reconecto el lunes tras 8 dias calendario ciego (sin refrescar desde 2026-11-08),
trayendo dato de disciplina los 5 dias por primera vez en semanas, aunque todavia sin fills con
precio (no se puede refrescar plan-vs-ejecucion a nivel de posicion).

## Marcador de la semana por instrumento

(`biasHitPct`/`scenarioAHitPct`/`zoneHitPct` = ventana rodante `hitLog`, 47 dias a 2026-11-20;
"EM semana" = de las 15 oportunidades sesion x dia de esta semana especifica, agregadas desde
`hitLog`; `/\` contra `reviews/2026-11-14-semana.md`.)

- **NQ**: sesgo 55% (n=111) sube vs 50% (n=107) · escenario A 51% (n=88) baja leve vs 52%
  (n=86) · zona 25% (n=67) sube leve vs 24% (n=62) · EM esta semana 53.3% (8/15) baja fuerte
  vs 73.3% (11/15) la pasada, el EM mas flojo de los 5 junto con GC. Tendencia bajista
  confirmada toda la semana, sin giro, cerrando en minimo de ciclo nuevo el viernes.
- **ES**: sesgo 53% (n=106) sube vs 48% (n=100) · escenario A 46% (n=90) igual vs 46% (n=95) ·
  zona 28% (n=53) baja vs 30% (n=56) · EM esta semana 60% (9/15) sube vs 53.3% (8/15). Mismo
  guion que NQ, un escalon detras.
- **GC**: sesgo 56% (n=104) sube vs 53% (n=101) · escenario A 51% (n=96) sube vs 49% (n=97) ·
  zona 27% (n=63) baja leve vs 28% (n=61) · EM esta semana 53.3% (8/15) sube vs 46.7% (7/15).
  El marcador rodante mejora pero el viernes volvio a quedar "sobre banda" dos veces (Asia y
  NY): sigue siendo el peor calibrado de EM del complejo.
- **YM**: sesgo 54% (n=91) sube vs 50% (n=86) · escenario A 57% (n=102) baja leve vs 58%
  (n=104) · zona 19% (n=59) sube vs 17% (n=59) · EM esta semana 60% (9/15) sube fuerte vs
  53.3% (8/15). Por fin resolvio la caja de 5-6 sesiones el miercoles, hacia abajo, y confirmo
  el resto de la semana.
- **CL**: sesgo 52% (n=103) baja leve vs 53% (n=97) · escenario A 54% (n=110) igual vs 54%
  (n=111) · zona 25% (n=64) sube vs 21% (n=63) · EM esta semana 60% (9/15) sube fuerte vs 40%
  (6/15). Giro de tesis el lunes (largo a corto) sostenido hasta el viernes, cuando dio la
  primera vela de reversion alcista limpia desde el reinicio (COT crowded-short extremo de
  combustible).
- **Global**: `predictionScore` ponderado 57.5% (n=2721) practicamente igual vs 57.5%
  (n=2670). Nota de calibracion: `scorecard.emCalibration` ya no trae `errPctAtr` en sus
  celdas "auto" (solo en el bloque congelado `_hand` de 2026-10-29), asi que esta semana no se
  puede comparar la calibracion de EM entre instrumentos con esa metrica como exige esta
  seccion; se deja como propuesta de metodo abajo en vez de forzar la comparacion con
  `emErrorTicks` en bruto.

## Donde fallo y lo que mejor paga

Blind spots con mas muestra: `bias|ES|calendar=major` 38% (n=48, vs 53% promedio), 3ra semana
seguida en la lista (31% n=51 hace 2 semanas, 34% n=47 la pasada, 38% n=48 esta semana): ES
sigue fallando el sesgo en semanas de calendario mayor, con muestra creciendo cada semana.
`scenA|ALL|crossAsset=mixed` 40% (n=40, vs 52% promedio): cuando el tono cruzado de activos
viene mixto, el escenario A falla casi 6 de cada 10 veces en todo el bus. `bias|CL|
conviction=media` 40% (n=35, vs 52% promedio): mismo blind spot de la semana pasada, sin
muestra fresca (n igual), sigue sin poder confirmarse una segunda semana con dato nuevo. Como
`bias|ES|calendar=major` ya lleva 3 semanas y no hay clase segura de `overrides` que lo cubra,
se mantiene como propuesta estructural abajo, ahora con mas fuerza. Mejores fortalezas: `bias|
ES|calendar=normal` 66% (n=58) y `bias|ALL|macro=medium` 67% (n=57), las de mayor muestra del
bus esta semana.

## Expectativa en R

`python3 method/weekly_r.py`: plan -0.03R (n=33, 30% ganan), mejora por tercera semana
consecutiva (-0.25R n=24 17% hace 2 semanas, -0.12R n=41 20% la pasada, -0.03R n=33 30% esta
semana), aunque sigue sin cruzar a positivo. Ejecucion: sin posiciones con precio en el
journal (`live/journal.json` trae disciplina/overtrade por dia los 5 dias, pero sus `fills`
siguen vacios, `[]`, en todos los `byDay` de la semana); sincroniza fills desde
mywhyjournal.com para poder medir la brecha plan-vs-ejecucion en R. Plan cripto +0.09R (n=16,
69% ganan), aparte, tambien mejora vs +0.03R (n=7, 86% ganan) la semana pasada en expectativa
aunque baja en tasa de acierto.

## Plan vs ejecucion

`method/plan_vs_exec.py` reporta "no fills yet in live/journal.json": el acumulado de
posiciones con precio sigue fechado al 2026-11-07 (144 posiciones, scorecard.execution.
planFit), 2da semana seguida sin poder refrescarlo aunque el journal ya trae dato diario de
disciplina. Ese acumulado sigue mostrando que operar "against" el plan (33 trades NQ, 39.4%
acierto, +17.46pts medios) gana mas que operar "off-zone" (59 trades NQ, 33.9%, +2.17pts): el
patron de que incluso ir en contra del plan paga mejor que jugar tierra de nadie se mantiene
sin dato nuevo que lo confirme o lo rompa esta semana especificamente.

## Contexto fuera del grafico

Cinco motores reales, casi ninguno repetido: risk-off generico sin calendario el lunes (VIX
+24%, Warsh), la ruptura estructural de GC el martes (sin evento detras) mas el titular de
Ormuz en CL, el combo FOMC-halcon + NVDA el miercoles (el unico dia con calendario mayor real,
y el mas limpio de sesgo del mes), la cumbre geopolitica Trump-Putin-Xi el jueves (risk-on
revertido dentro de la misma sesion) y la liquidacion generalizada sin catalizador de
calendario el viernes (OpEx). El tono de riesgo fue mayormente CON el resultado neto bajista de
los indices toda la semana salvo el salto del jueves (que se revirtio en la misma sesion de
NY) y el viernes en CL (unico instrumento donde el tono termino EN CONTRA del corto de fondo,
con una reversion alcista real desde el minimo).

## Ejecucion de la semana

El journal se reconecto esta semana (`live/journal.json` `updatedAt` 2026-11-21T03:22Z): dato
real los 5 dias por primera vez en mas de un mes. 217 trades en la semana (25/67/50/34/41 por
dia, promedio 43.4/dia, por encima del promedio de 36.8/dia de la ventana de 45 dias). 0 de 5
dias disciplinados (0%, igual que el 0% de la ventana de 45 dias), `overtrade` y `revenge` los
5 dias (100%). `outsideEdgeRate` 100% (217/217 trades calificados fuera de zona del plan); el
journal sigue sin poder etiquetar a favor/en contra del sesgo (`withBias`/`againstBias` en 0
los 5 dias). Racha de perdidas peor: 14 seguidas el miercoles 18-nov, record de la ventana
medida (antes el peor dato eran 6). `fullStopRate` de la semana 44.7% (97/217), peor que el
39% de la ventana de 45 dias; `partialRate` y `scratchRate` en 0% los 5 dias (sin un solo
parcial o scratch, mismo patron cronico de siempre, la fuga homerun-exit sigue intacta). Sin
dato de `positions`/`wlPtsRatio` por precio para cruzar con el plan (ver seccion anterior).

## Perfil del trader

`state/trader-profile.json` bloque `observed` reescrito: ventana 2026-11-16..2026-11-20, 5 de
5 dias con dato real (el journal se reconecto el lunes tras 8 dias calendario ciego).
`disciplinedPct` 0%, `outsideEdgeRate` 100%, `againstBiasRate` no clasificable (el journal no
etiqueta sesgo esta ventana, 0 trades con `withBias` o `againstBias` marcado, no es un 0% real
de contra-sesgo). `exitQuality`: `partialRate` 0%, `scratchRate` 0%, `fullStopRate` 44.7%
(peor que el 39% de la ventana de 45 dias). `exitBaseline` refrescado desde
`../scalp-cc-bus/exit-baseline.json` (asOf 2026-11-15, `generatedAt` 2026-11-15T02:29Z): NQ
n=10956 (antes 10950, +6 muestras), hit1R 33.6% (sin cambio), stoppedOut 47.4% (sin cambio),
reachedTP2 5.3% (sin cambio), practicamente el mismo tono de siempre, sin cambio real de
fondo. La ejecucion de esta semana confirma el patron cronico declarado en `patterns[]`
(`homerun-exit`, 0 parciales) y el de operar fuera de zona, pero no aporta evidencia de precio
para confirmar o contradecir `size-escalation`/`revenge-after-sl` especificamente: se deja
`patterns[]` sin tocar.

## Que se repitio

1. **`bias|ES|calendar=major` lleva 3 semanas seguidas en la lista de blind spots** (31%
   n=51, 34% n=47, 38% n=48), sin clase segura de `overrides` que lo cubra todavia: ya
   justifica definir la clase nueva (ver propuesta abajo).
2. **Operar fuera de zona sigue pagando peor que incluso ir en contra del plan**
   (acumulado sin dato nuevo esta semana: "against" NQ 39.4%/+17.46pts vs "off-zone" NQ
   33.9%/+2.17pts), ya varias semanas con la misma lectura.
3. **GC sigue siendo el peor calibrado de EM del bus** (sobre banda dos veces el viernes,
   Asia y NY), consistente con semanas anteriores pese a la correccion automatica del `mult`.
4. **El journal vuelve a traer dato pero sin fills con precio**: 2da semana seguida sin poder
   refrescar `plan_vs_exec`/`weekly_r` del lado de ejecucion real en puntos, aunque ya se
   pueda medir disciplina/overtrade/revenge dia por dia.

## Cambios de la semana

### Cambios aplicados

Ninguno esta semana: se revisaron las dos condiciones de `overrides.predictionSkip` activas y
ninguna cruzo un umbral nuevo.

- `overrides.predictionSkip["NQ|direction"]` se mantiene (rate=0.4143, n=35, SIN muestra
  fresca, mismo n que hace 2-3 semanas: no se puede confirmar una segunda semana consecutiva
  sobre 0.40 porque no hay dato nuevo que calificar).
- `overrides.predictionSkip["GC|range"]` se mantiene (rate=0.3707, n=58, sube de muestra desde
  56 pero sigue bajo 0.40, sin cambio).
- `overrides.zonePriors` sigue bloqueado, 5ta semana igual: `state.zones` sigue sin guardar el
  conteo crudo pre-encogimiento por arquetipo puro, no se puede calcular el `winRate` agregado
  real por tipo (solo por `tipo|vs24h`) sin ese dato.

### Propuestas de metodo

1. **Definir `overrides.convictionCap["ES|calendar=major"]`** (clase nueva, no auto-aplicable
   todavia). Evidencia: `bias|ES|calendar=major` 38% (n=48) vs 53% promedio, 3ra semana
   consecutiva en la lista de blind spots con muestra creciendo cada semana (31% n=51, 34%
   n=47, 38% n=48). Campo: `method/instructions.md` seccion 6.1 (clases auto-aplicables) y
   `state/sa-state.json` (schema de `overrides`).
2. **`method/update_scorecard.py` no escribe `errPctAtr` en las celdas "auto" de
   `scorecard.emCalibration`** (solo existe en el bloque congelado `_hand`, fijo desde
   2026-10-29). La seccion 6.1 pide comparar la calibracion de EM entre instrumentos con
   `errPctAtr`, nunca con `emErrorTicks` en ticks crudos, pero ese campo ya no se genera para
   los datos vivos: esta semana no se pudo hacer esa comparacion. Campo:
   `method/update_scorecard.py` (la funcion que construye `cal[key]`, linea ~124, necesitaria
   `atrD` por sesion para calcular `errPctAtr = meanErrTk * tick / atrD * 100`).

## Leccion de la semana

Primera semana del mes con dato de ejecucion real los 5 dias (el journal se reconecto el
lunes) y lo que confirma, sin sorpresa, es el mismo patron cronico: 0% disciplinado, 100%
fuera de zona, con una racha record de 14 perdidas seguidas justo el dia mas limpio de sesgo
del mes (80%, FOMC+NVDA); el problema sigue sin ser el metodo (el acumulado muestra que incluso
operar en contra del plan paga mejor que jugar tierra de nadie), es no usar los niveles que ya
estan en el plan.

## Regimen: como entro y como sale cada instrumento

- **NQ**: entro la semana en corto, dia 1 (roto el viernes anterior con el PPI), confirmo
  tendencia bajista con autoridad lunes a viernes sin ningun giro real, sobrevivio el salto
  risk-on del jueves sin romper la tesis, y cerro la semana en minimo de ciclo nuevo con cierre
  en el 20-24% de su rango. Sale en corto, dia 7, estirado.
- **ES**: mismo guion que NQ un escalon detras toda la semana. Sale en corto, dia 7.
- **GC**: entro la semana todavia en el largo de 4 dias (roto el lunes en NY), vivio una doble
  barrida sin autoridad el martes antes de reinstalar un corto limpio esa misma noche (dia 1
  del ciclo nuevo), y confirmo bajista el resto de la semana con el peor calibrado de EM del
  bus. Sale en corto, dia 4, confirmado pero con la banda de EM todavia sin ajustar del todo.
- **YM**: entro la semana todavia sin resolver la caja de 5-6 sesiones, la rompio por fin el
  miercoles hacia abajo con autoridad (rompiendo el PDL 52081) y confirmo jueves y viernes.
  Sale en corto, confirmado, el indice que tardo mas en resolver esta racha.
- **CL**: entro la semana girando de largo a corto el lunes (sin catalizador de calendario,
  rotura estructural pura), sostuvo el corto toda la semana con un desvio por el titular de
  Ormuz el martes, y cerro el viernes con la primera vela de reversion alcista real desde el
  reinicio (minimo de ciclo nuevo revertido, cierre en el 85% de su rango, COT crowded-short
  extremo de combustible). Sale EVOLUCIONANDO, sin romper la invalidacion dura todavia pero
  pidiendo vigilancia real la semana que entra.
