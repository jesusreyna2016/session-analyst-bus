# Meta-revision semanal · 2026-11-23 a 2026-11-27

Semana de whipsaw real, resuelta solo el viernes. Lunes un titular (Trump "convencio" a Nvidia
de reinstalar a Huang) disparo un short-covering real que rompio los cortos de 8-10 dias de
NQ/ES/YM y el de GC (giro a largo de madrugada, reclamo de la vieja VAH), con el VIX cayendo
-25.6% y CL como unico instrumento limpio, corto las 3 sesiones, ajeno al squeeze de indices.
Martes fue digestion tranquila en Asia (NQ/ES casi planos). Miercoles devolvio TODO en un
round-trip violento en los 5 instrumentos (barrido de un extremo nuevo y cierre en el tercio
alto del rango), con YM haciendo un doble giro completo en la misma sesion de NY: el conflicto
de marcos (diario bajista contra 1h/4h alcistas) quedo abierto el resto de la semana. Jueves fue
Thanksgiving completo, sin una sola vela de Londres/NY (solo Asia calificable). Viernes (Black
Friday, cierre anticipado) el VIX se desinflo otro -11.16% y los 4 indices/metal rompieron con
autoridad el techo semanal que la tesis de cada uno pedia para girar a largo, cerrando el
conflicto de marcos a favor del largo en los 4; CL hizo lo contrario, el squeeze de cortos llego
a 86.60 tal como la tesis anticipaba pero NY lo devolvio TODO sin ningun EIA en curso, cerrando
en el tercio bajo. La ejecucion real quedo casi sin dato: `live/journal.json` no trae entrada
para lunes, martes ni miercoles (23, 24 y 25 de noviembre); solo jueves (1 trade) y viernes (18
trades, racha de 15 perdidas seguidas, nuevo record) tienen algo, y ambos llegaron sin
clasificar sesgo/zona (`src:"mfp"`).

## Marcador de la semana por instrumento

(`biasHitPct`/`scenarioAHitPct`/`zoneHitPct` = ventana rodante `hitLog`, 47 dias a 2026-11-27;
"EM semana" = de las oportunidades sesion x dia de esta semana especifica agregadas desde
`hitLog` (10 de las 15 habituales: jueves solo calibro Asia por el feriado y viernes no trajo
`em` por ser calificacion manual sin velas); `/\` contra `reviews/2026-11-21-semana.md`.)

- **NQ**: sesgo 54% (n=107) baja leve vs 55% (n=111) · escenario A 57% (n=86) sube vs 51%
  (n=88) · zona 26% (n=70) sube leve vs 25% (n=67) · EM esta semana 70% (7/10) sube fuerte vs
  53.3% (8/15). Rompio el corto de 8 dias el lunes con el squeeze, lo devolvio el miercoles y
  lo reconfirmo largo el viernes con autoridad: el sesgo de sesion (rolling) bajo justo la
  semana que el mercado giro de verdad.
- **ES**: sesgo 50% (n=102) baja vs 53% (n=106) · escenario A 49% (n=83) sube vs 46% (n=90) ·
  zona 27% (n=55) baja leve vs 28% (n=53) · EM esta semana 40% (4/10) baja vs 60% (9/15), el
  peor EM de los 5 esta semana. Mismo guion que NQ, un escalon detras.
- **GC**: sesgo 55% (n=102) baja leve vs 56% (n=104) · escenario A 51% (n=90) igual vs 51%
  (n=96) · zona 26% (n=57) baja leve vs 27% (n=63) · EM esta semana 70% (7/10) sube fuerte vs
  53.3% (8/15). Unico que cierra la semana con el conflicto de marcos todavia abierto (4h sin
  confirmar), aunque el precio ya rompio con autoridad.
- **YM**: sesgo 52% (n=89) baja leve vs 54% (n=91) · escenario A 60% (n=97) sube vs 57%
  (n=102) · zona 17% (n=54) baja vs 19% (n=59) · EM esta semana 60% (6/10) igual vs 60% (9/15).
  Doble round-trip completo el miercoles en la misma sesion de NY, el mas violento de los 5.
- **CL**: sesgo 55% (n=99) sube vs 52% (n=103) · escenario A 56% (n=104) sube vs 54% (n=110) ·
  zona 27% (n=63) sube vs 25% (n=64) · EM esta semana 60% (6/10) igual vs 60% (9/15). El unico
  de los 5 que no giro a largo el viernes: confirma `R-CL-reversal-completo-sin-catalizador`
  con su primera reversion COMPLETA de verdad (squeeze a 86.60, devuelto entero en NY).
- **Global**: `predictionScore` ponderado 57.5% (n=2812) practicamente igual vs 57.5% (n=2721).

## Donde fallo y lo que mejor paga

Blind spots con mas muestra: `bias|ES|calendar=major` 39% (n=46, vs 50% promedio), 4ta semana
seguida en la lista, pero la brecha cae a 11 puntos por primera vez (antes 15, 19, 22 puntos
las 3 semanas anteriores), justo bajo el umbral de 12 que sostiene su `overrides.convictionCap`:
se vigila, si vuelve a caer bajo 12 la semana que entra se retira. `scenA|ES|frame=aligned` 39%
(n=33, vs 49% promedio): nuevo en la lista esta semana, cuando el marco diario y el de 1h de ES
coinciden el escenario A falla casi 6 de cada 10 veces, sin muestra repetida todavia para
proponer nada. `zone|CL|calendar=major` 16% (n=31, vs 27% promedio): las zonas de CL fallan el
doble de lo normal en dias de calendario mayor. Mejores fortalezas: `bias|ALL|macro=medium` 67%
(n=61) y `bias|CL|calendar=normal` 66% (n=50), las de mayor muestra del bus esta semana.

## Expectativa en R

`python3 method/weekly_r.py`: plan -0.09R (n=16, 25% ganan), rompe la racha de 3 semanas de
mejora (-0.25R n=24, -0.12R n=41, -0.03R n=33 las 3 semanas anteriores), consistente con una
semana de whipsaw donde el escenario A fallo mas de lo normal. Ejecucion -0.45R (n=19, 5%
ganan): primera semana con fills de precio reales para medir la brecha (las ultimas 2 semanas
no tenian), partida en contra del plan -0.55R (n=5, 0% ganan) y fuera de zona -0.41R (n=14, 7%
ganan), SIN ningun trade dentro del plan esta semana. Brecha +0.36R por trade a favor del plan.
Plan cripto -0.33R (n=10, 50% ganan), unica linea que empeora en expectativa aunque mantiene
tasa de acierto razonable.

## Plan vs ejecucion

`python3 method/plan_vs_exec.py` (acumulado, ya con los fills de esta semana dentro): operar
dentro del plan en NQ sigue ganando mas que fuera de el: in-plan 37% de acierto y +22.87pts
medios (n=35) contra off-zone 31% y -3.76pts (n=706) y against 29% y -9.50pts (n=613). Los 19
trades nuevos de esta semana (todos NQ y ETHUSDT) cayeron enteros en off-zone/against, ninguno
in-plan, reforzando el mismo patron acumulado sin excepcion.

## Contexto fuera del grafico

Lunes fue el motor mas real de la semana sin estar en el calendario (titular Huang/Nvidia, VIX
-25.6%), miercoles fue el unico dia sin motor claro (reversion pura, round-trip violento sin
catalizador de calendario ni titular), y viernes el VIX se desinflo otro -11.16% confirmando el
rally de los 4 indices/metal aunque el plan lo habia etiquetado `crossAsset` como mixto: el tono
cruzado fue mas util el viernes de lo que el plan esperaba y el mas inutil el miercoles.

## Ejecucion de la semana

Guarda de datos fuerte esta semana: `live/journal.json` no trae entrada `byDay` para lunes,
martes ni miercoles (23, 24 y 25 de noviembre), 3 de los 5 dias de la ventana sin dato alguno,
no solo sin clasificar. Jueves (Thanksgiving) trae 1 trade, disciplinado, sin overtrade ni
revenge. Viernes (Black Friday) trae 18 trades, overtrade y revenge, racha de perdidas de 15
seguidas (nuevo record de la ventana medida, supera las 14 del miercoles pasado), 13 de 18 en
SL completo (72%, `wlPtsRatio` 2.62). Con solo 2 de 5 dias con dato (19 trades en total, muy por
debajo del promedio de 36.8/dia de la ventana de 45 dias) no se puede hablar de disciplina ni
de contra-sesgo de la SEMANA, solo de esos 2 dias puntuales: el jueves limpio, el viernes con la
peor racha medida hasta ahora. `zones/report.md` (ventana rodante de 20 dias, no especifica de
esta semana) sigue mostrando 1599 trades de Mi Mesa, 567 armados, 66% de acierto, E[R] 0.646,
sin cambio relevante.

## Perfil del trader

`state/trader-profile.json` bloque `observed` reescrito con la ventana 2026-11-23..2026-11-27,
pero con la mitad de la semana sin dato (ver seccion anterior): `disciplinedPct` 50% (1 de los 2
dias CON dato, muestra minima, no representa la semana completa), `againstBiasRate` y
`outsideEdgeRate` no medibles (los 2 dias disponibles llegaron sin clasificar sesgo ni zona,
`src:"mfp"`). `exitQuality`: `scratchRate` 0%, `fullStopRate` 68.4% (13 de 19, peor que el 39%
de la ventana de 45 dias y que el 44.7% de la semana pasada), `partialRate` no disponible (sin
dato en ninguno de los 2 dias). `exitBaseline` refrescado desde `../scalp-cc-bus/exit-baseline.json`
(asOf 2026-11-22, `generatedAt` 2026-11-22T02:51:47Z): NQ n=12843 (antes 10956, +1887 muestras),
hit1R 33.8% (antes 33.6%), stoppedOut 47.6% (antes 47.4%), reachedTP2 5.3% (sin cambio),
practicamente el mismo tono de siempre. La ejecucion de esta semana (la poca que hay) no aporta
ni confirma ni contradice `patterns[]`: se deja sin tocar.

## Que se repitio

1. **Operar fuera de zona o en contra del plan sigue sin pagar**, confirmado otra vez esta
   semana con dato nuevo de precio: against -0.55R (0% acierto) y off-zone -0.41R (7%) contra
   0 trades dentro del plan, consistente con el acumulado (in-plan NQ 37%/+22.87pts vs
   off-zone 31%/-3.76pts vs against 29%/-9.50pts).
2. **`bias|ES|calendar=major` lleva 4 semanas seguidas en blind spots**, pero por primera vez
   la brecha (11 puntos) cae bajo el umbral de 12 que sostiene su `overrides.convictionCap`:
   se vigila para posible retiro la semana que entra si se repite.
3. **`zonePriors.bounce_val` sigue divergiendo del prior**, 2da semana consecutiva de ajuste a
   la baja (0.68 -> 0.63 -> 0.58).
4. **GC: "mantengo pero degrado" vuelve a quedarse corto** ante un contra-caso que ya nombraba
   el catalizador real en marcha (ruptura 1h confirmada, 4h sin confirmar): 2/2 veces ahora
   (nota de `models.GC` del 2026-10-02 y el viernes 2026-11-27, peor Brier del dia, 0.52, en
   `direction` de GC).

## Cambios de la semana

### Cambios aplicados

- `overrides.zonePriors["bounce_val"]`: 0.63 -> **0.58** (winRate agregado 0.521, winN=48,
  diverge -0.109 vs prior 0.63, > 0.10 con winN >= 30, method/zone_type_rates.py).
- `overrides.predictionSkip["GC|range"]` se mantiene (rate 0.3852, n=61, sin cambio de
  condicion).
- `overrides.convictionCap["ES|calendar=major"]` se mantiene activo (sin retiro todavia: la
  condicion de 12 puntos bajo promedio cayo a 11 esta semana, primera vez que no se cumple
  estrictamente, pero se necesitan 2 semanas seguidas fallando para retirarlo).

### Propuestas de metodo

1. **GC: forzar GIRA en vez de dejar "mantengo pero degrado" como salida valida cuando el
   contra-caso ya nombra el catalizador real en marcha y hay un cierre 1h de ruptura confirmado
   contra un 4h sin confirmar.** Evidencia: 2/2 veces confirmado (nota de `models.GC` del
   2026-10-02, y el viernes 2026-11-27: GC siguio con "mantengo pero degrado" en direction pese
   a la ruptura 1h real, peor Brier del dia 0.52). Campo: `method/instructions.md` (regla del
   contra-caso, las 3 salidas) y `state/sa-state.json` `models.GC`.
2. **El weekly no tiene un campo que marque cuantos dias de los 5 de la ventana faltan por
   completo en `live/journal.json` byDay** (distinto de "classified:false"): esta semana 3 de 5
   dias (23, 24, 25-nov) no tienen entrada alguna, y el metodo solo lo nota en prosa. Evidencia:
   3 de 5 dias sin entrada. Campo: `method/update_scorecard.py` y `method/weekly_r.py` (agregar
   un conteo explicito de dias faltantes en la ventana, no solo de dias no clasificados).

## Leccion de la semana

La semana fue un whipsaw resuelto solo el viernes (corto roto el lunes, devuelto el miercoles,
reconfirmado largo el viernes con autoridad), y el sesgo de sesion (rolling) bajo en 4 de 5
instrumentos justo la semana que el mercado giro de verdad, mientras la ejecucion real, la poca
medible (19 trades en 2 de 5 dias), sigue perdiendo fuera de zona y en contra sin un solo trade
dentro del plan.

## Regimen: como entro y como sale cada instrumento

- **NQ**: entro en corto (dia 8), lo rompio el lunes con el squeeze de Nvidia/Huang (dia 1 de
  ciclo nuevo), lo devolvio por completo el miercoles, y lo reconfirmo el viernes rompiendo con
  autoridad el techo semanal. Sale LARGO, dia 1 confirmado, estirado.
- **ES**: mismo guion que NQ, un escalon detras toda la semana. Sale largo, dia 1.
- **GC**: entro todavia en el corto reinstalado la semana pasada, giro a largo de madrugada el
  lunes (reclamo de la vieja VAH), confirmo con BOS real el miercoles, y sostuvo el largo el
  resto de la semana pese a que su 4h nunca confirmo. Sale LARGO, dia 5, con el conflicto de
  marcos todavia abierto.
- **YM**: entro en corto confirmado, vivio el round-trip mas violento de los 5 el miercoles
  (giro bajista de madrugada deshecho por completo en la misma sesion de NY), y cerro la semana
  largo el viernes junto al resto del complejo. Sale LARGO, dia 1, el que mas vueltas dio para
  llegar ahi.
- **CL**: entro en corto estructural confirmado, el unico que no se movio con el squeeze de
  indices del lunes, sostuvo el corto toda la semana hasta el squeeze del viernes que llego a
  86.60 tal como la tesis anticipaba (COT crowded-short extremo), pero NY lo devolvio TODO sin
  catalizador, cerrando en el tercio bajo del dia. Sale en CORTO, reconfirmado con autoridad, el
  unico de los 5 que no giro a largo.
