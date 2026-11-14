# Meta-revision semanal · 2026-11-09 a 2026-11-13

Semana de 4 catalizadores reales en 5 dias, ninguno repetido: lunes NQ/ES giraron de corto a
largo con cierres de 1h sostenidos sobre su flip de invalidacion (el corto de 8-9 dias murio);
martes el CPI probo ese giro con una barrida bajo todos los marcos y el giro sobrevivio; miercoles
cambio el regimen de fondo y la tesis larga de 4 dias de GC se rompio sin que ninguna zona de la
tabla la capturara (cero de 14 zonas de reversion/continuacion pagaron ese dia); jueves la renuncia
sin aviso del CEO de Nvidia (~29% de caida en la accion) mas un titular de Trump sobre Iran movieron
todo el complejo, con un round-trip completo de NQ dentro de la misma sesion de NY; viernes el PPI
mas frio de lo esperado se vendio y rompio en la primera hora los giros largos de NQ/ES que venian
de jueves, el peor dia de sesgo de la ventana (2 aciertos de 12 llamadas). La hipotesis de que un
giro de tesis con `daysHeld<=2` es fragil frente a un shock real quedo confirmada 3/3 esta semana
(subida a `models.NQ` como `R-NQ-giro-de-un-dia-fragil`). El hallazgo operativo mas caro de la
semana no es de mercado: `live/journal.json` no trajo UN SOLO dia nuevo (0 de 5), 6 dias calendario
sin refrescar desde `2026-11-08T03:19Z` -- la semana entera queda ciega para medir ejecucion real.

## Marcador de la semana por instrumento

(`biasHitPct`/`scenarioAHitPct`/`zoneHitPct` = ventana rodante `hitLog`, 47 dias a 2026-11-13;
"EM semana" = de las 15 oportunidades sesion x dia de esta semana especifica dentro de banda, de
`grades/<fecha>.json`; `/\` contra `reviews/2026-11-07-semana.md`.)

- **NQ**: sesgo 50% (n=107) sube vs 47% (n=106) · escenario A 52% (n=86) sube vs 49% (n=88) ·
  zona 24% (n=62) igual vs 24% (n=58) · EM esta semana 73.3% (11/15) sube fuerte vs 53% (8/15), el
  mejor EM de los 5 esta semana. El instrumento con el giro mas sostenido (sobrevivio CPI el martes,
  se rompio otra vez viernes con el PPI).
- **ES**: sesgo 48% (n=100) sube vs 44% (n=103) · escenario A 46% (n=95) sube vs 45% (n=94) ·
  zona 30% (n=56) sube vs 26% (n=53) · EM esta semana 53.3% (8/15) sube vs 40% (6/15). Mismo guion
  que NQ un escalon detras toda la semana.
- **GC**: sesgo 53% (n=101) sube vs 49% (n=99) · escenario A 49% (n=97) sube vs 46% (n=97) ·
  zona 28% (n=61) sube vs 27% (n=60) · EM esta semana 46.7% (7/15) sube vs 33% (5/15). El marcador
  rodante mejora pero esconde el evento real: la tesis larga de 4 dias se rompio el miercoles y dos
  GO de conviccion alta en rebotes de POC fallaron (jueves y viernes).
- **YM**: sesgo 50% (n=86) baja vs 51% (n=88) · escenario A 58% (n=104) baja vs 59% (n=100) ·
  zona 17% (n=59) baja vs 19% (n=54) · EM esta semana 53.3% (8/15) sube fuerte vs 27% (4/15). Sigue
  siendo el indice mas fragil del complejo para un giro reciente (rompio y devolvio la ruptura en la
  misma noche del martes).
- **CL**: sesgo 53% (n=97) baja vs 57% (n=99) · escenario A 54% (n=111) sube vs 52% (n=106) ·
  zona 21% (n=63) sube vs 20% (n=56) · EM esta semana 40.0% (6/15) sube vs 27% (4/15). El corto de
  fondo se reafirmo toda la semana con un techo 89.15-89.64 repetido tres dias.
- **Global**: `predictionScore` ponderado 57.5% (n=2670) practicamente igual vs 57.6% (n=2535).
  `errPctAtr` (nunca `emErrorTicks` en bruto, promedio ponderado por sesion): NQ 20.8% mejora vs
  23.4% · ES 19.9% mejora vs 21.5% · GC 30.9% empeora fuerte vs 22.9% (el `mult` de 2.18 no bastó el
  jueves, EM se fue "over" en Londres) · YM 21.7% mejora vs 23.3% · CL 24.6% empeora leve vs 23.0%.
  GC es el unico que se calibra peor esta semana a pesar de mejorar su hit-rate rodante.

## Donde fallo y lo que mejor paga

Blind spots con mas muestra: `bias|ES|calendar=major` 34% (n=47, vs 48% promedio) -- 2a semana
seguida en la lista (semana pasada 31%, n=51): ES sigue fallando el sesgo justo en semanas con
calendario mayor. `bias|CL|conviction=media` 40% (n=35, vs 53% promedio): la conviccion media de CL
rinde peor que la baja, contraintuitivo. `bias|ES|news=high` 30% (n=33, vs 48% promedio): mismo
patron que calendar=major, ES sufre con ruido de alto impacto. Como `bias|ES|calendar=major` repite
2 semanas y no hay clase segura de `overrides` que lo cubra (no es un `kind` de `predictionSkip` ni
un arquetipo de `zonePriors`), se deja como propuesta estructural abajo, no como cambio aplicado.
Mejores fortalezas: `bias|CL|conviction=baja` 65% (n=53) y `bias|GC|frame=aligned` 65% (n=51), los
mas confiables con muestra real del bus.

## Expectativa en R

`python3 method/weekly_r.py`: plan -0.12R (n=41, 20% ganan) -- mejora vs -0.25R (n=24, 17%) la
semana pasada, aunque sigue en negativo (semana de zonas golpeadas/rotas, no de reversion limpia).
Ejecucion sin datos: `live/journal.json` no trajo ninguna posicion nueva para 2026-11-09..13,
sincroniza el journal desde mywhyjournal.com. Sin ejecucion no hay brecha que medir esta semana
(semana pasada fue +1.91R invertida; sin dato para saber si el patron se repitio). Plan cripto
+0.03R (n=7, 86% ganan), aparte.

## Plan vs ejecucion

`method/plan_vs_exec.py` no tiene ninguna posicion nueva en la ventana: el acumulado sigue fechado
al 2026-11-07 (144 posiciones, 0 in-plan en NQ, 59 off-zone NQ 34% ganador +2.17pts, 33 against NQ
39% ganador +17.46pts). Sin trades nuevos no se puede decir si "en plan" paga mas esta semana
especificamente; el acumulado sigue sin ningun trade NQ dentro de una zona real del plan.

## Contexto fuera del grafico

Cuatro motores reales, ninguno repetido: el giro de tesis del lunes (sin catalizador de calendario,
puro cierre de estructura), el CPI del martes (confirmo el giro con una barrida violenta), la
renuncia sin aviso del CEO de Nvidia el jueves (VIX +8%, regla dura de EM activada, US10Y +2.1%,
DXY +0.26%, BTC -3.46%) junto con un titular de Trump sobre Iran que movio el petroleo, y el PPI
frio pero vendido del viernes (10 anos rompiendo maximo en 5.15%). El tono de riesgo fue
mayormente en contra del resultado neto de la semana en indices: el jueves el shock empujo a la
baja pero NY se recupero dentro de la misma sesion (fakeout), y el viernes el dato "bueno" se
vendio igual, el patron mas dificil de leer con reglas de reaccion estandar.

## Ejecucion de la semana

0 de 5 dias con dato en `live/journal.json` (peor que el 0/3 de la semana pasada: esta vez no hubo
NINGUN dia, ni siquiera parcial). El journal no se ha refrescado desde `2026-11-08T03:19Z`, mas de
6 dias calendario sin un solo `byDay` nuevo (el ultimo sigue siendo 2026-11-07), ya marcado como
atraso en `live/health.json`. No hay disciplina, contra-sesgo ni calidad de salida que medir de
ESTA semana. El rollup de 45 dias (que no cambio porque no hay entrada nueva) sigue leyendo
disciplinado 4%, contra-sesgo 32%, fuera de edge 27%, 28/45 dias de sobre-operar y 19/45 de
revenge, `partialRate` 1%, `fullStopRate` 54% -- son los mismos numeros de hace una semana, no una
lectura fresca. Sin saber si la disciplina mejoro o empeoro esta semana especifica: la fuga que
manda sigue siendo la misma de siempre (homerun-exit, 0 parciales en todo el rollup) pero no hay
como confirmarlo con dato de estos 5 dias.

## Perfil del trader

`state/trader-profile.json` bloque `observed` reescrito: ventana 2026-11-09..2026-11-13 con 0 de
5 dias de dato real (journal sin refrescar desde 2026-11-08T03:19Z); `disciplinedPct`,
`againstBiasRate`, `outsideEdgeRate` y `exitQuality` en null, sin lectura fresca posible.
`exitBaseline` refrescado desde `../scalp-cc-bus/exit-baseline.json` (asOf 2026-11-14): NQ n=10950
(antes 9620), hit1R 33.6% (+0.5pp), stoppedOut 47.4% (-0.2pp), reachedTP2 5.3% (+0.3pp), mismo tono
de siempre, sin cambio real de fondo. La falta de dato de ejecucion esta semana no permite
confirmar ni contradecir ningun `patterns[]` existente: se deja todo igual, sin propuesta nueva de
patron.

## Que se repitio

1. **El journal dejo de sincronizar por completo**, ya 2a semana con cobertura cayendo (3/5 ->
   0/5): si esto sigue, la medicion de ejecucion real queda ciega indefinidamente, no es ya un
   problema de muestra chica sino de pipeline roto.
2. **Un giro de tesis reciente (`daysHeld<=2`) sigue siendo fragil frente a un shock real**:
   `H-2026-11-05-giro-reciente-se-rompe-con-shock` llego a 3/3 esta semana (NQ formado el 11-12,
   roto el 11-13 con el PPI) y se subio a `models.NQ` como regla provisional. Es la 2a semana que
   se propone capar la conviccion de un giro reciente (ver abajo, ahora con mas evidencia).
3. **Las zonas de reversion A FAVOR de las ultimas 24h siguen fallando mientras las de
   continuacion EN CONTRA pagan** (regla 8e): 0/4 reversion-con-24h el jueves (bounce_val,
   golden_zone) vs 2/2 continuacion-contra-24h (retest_break) el mismo dia; ya 2 semanas seguidas
   con el mismo patron confirmado con mas muestra.
4. **GC con conviccion "alta" en rebotes de POC fallo 2 veces esta semana** (jueves y viernes,
   ambos -1R) en un contexto de dolar/rendimientos rompiendo maximos: el oro en tendencia bajista
   con viento macro en contra no esta dando rebotes operables en Londres.

## Cambios de la semana

### Cambios aplicados

- `overrides.predictionSkip["NQ|scenario"]` **retirado**: `predictionScore["NQ|scenario"].rate`
  llevaba 2 semanas consecutivas con muestra fresca sobre el umbral de 0.40 (semana pasada
  rate=0.4085 n=59 primera vez arriba; esta semana rate=0.421 n=62, +3 de muestra fresca, sigue
  arriba). Antes: skip activo desde 2026-09-12 (evidencia original n=29, rate=0.33). Despues: NQ
  vuelve a pedir prediccion de `scenario` en cada corrida.
- Sin cambios en el resto: `overrides.predictionSkip["NQ|direction"]` se mantiene (rate=0.4143,
  n=35, SIN muestra fresca esta semana, mismo n que la semana pasada: no se puede confirmar la 2a
  semana consecutiva todavia). `overrides.predictionSkip["GC|range"]` se mantiene (rate=0.3839,
  n=56, sube de muestra pero sigue bajo 0.40, sin cambio). `overrides.zonePriors` sigue bloqueado,
  4a semana igual: `state.zones` sigue sin guardar el conteo crudo pre-encogimiento por arquetipo
  puro, no se puede calcular el `winRate` agregado real por tipo sin ese dato.

### Propuestas de metodo

1. **Capar la conviccion de un giro de tesis reciente (`daysHeld<=2`) a "media" como maximo hasta
   que resista una prueba real.** Evidencia ahora en 3/3 (`H-2026-11-05-giro-reciente-se-rompe-con-shock`,
   confirmada esta semana con el ciclo NQ 11-12/11-13, subida a `models.NQ` como
   `R-NQ-giro-de-un-dia-fragil`), repetida de las dos semanas anteriores con mas fuerza. Campo:
   `method/instructions.md` seccion 3 (frameConflict/convictionCalibration) y
   `state.scorecard.convictionCalibration`. No se aplica todavia (no hay clase segura de
   `overrides` definida para esto), pero la evidencia ya justifica que Jesus la revise.
2. **GC necesita un tope de conviccion para rebotes de POC/reversion cuando el fondo macro
   (dolar + rendimientos) va en contra del largo.** Evidencia: 2/2 GO "alta" fallidos esta semana
   (jueves rebote POC Londres -1R, viernes rebote POC Londres -1R), ambos con DXY y US10Y
   rompiendo maximos en la misma ventana. Campo: `method/instructions.md` seccion 4 (score de
   confluencia / conviccion de zonas) para GC especificamente.
3. **`bias|ES|calendar=major` repite 2 semanas como blind spot sin clase segura que lo cubra**
   (34% n=47 esta semana, 31% n=51 la pasada, vs 48% promedio). Como no hay override existente
   para un tope de conviccion condicionado a `calendar=major` por simbolo, se propone definir esa
   clase nueva en `state.overrides` (p. ej. `overrides.convictionCap["ES|calendar=major"]`) para
   que una futura semana pueda auto-aplicarla. Campo: `method/instructions.md` seccion 6.1 (clases
   auto-aplicables) y `state/sa-state.json` (schema de `overrides`).

## Leccion de la semana

Cuatro catalizadores distintos en cinco dias (giro sin calendario, CPI, shock de un solo nombre
mas titular geopolitico, dato macro vendido al reves) dejaron el marcador de prediccion mejor que
la semana pasada en casi todo el bus, pero el dato mas caro no fue de mercado: el journal de
ejecucion lleva 6 dias sin refrescar y la semana completa queda sin forma de medir si Jesus
siguio el plan o la fuga de siempre. Sin ese dato, mejorar el modelo de prediccion no sirve de
nada si no se puede confirmar que se traduce en mejor ejecucion real.

## Regimen: como entro y como sale cada instrumento

- **NQ**: entro la semana todavia en el corto de 8-9 dias, giro a largo el lunes con cierres de 1h
  sostenidos sobre el flip, sobrevivio la prueba del CPI el martes, aguanto el shock de Nvidia del
  jueves (incluso con un round-trip completo dentro de la misma sesion de NY) y se rompio otra vez
  el viernes con el PPI vendido. Sale la semana en corto, dia 1, con el patron de giro fragil ya
  confirmado como regla provisional.
- **ES**: mismo guion que NQ un escalon detras toda la semana, giro a largo el lunes, sobrevivio
  martes y jueves, se rompio el viernes con la misma causa. Sale en corto, dia 1.
- **GC**: entro la semana en el dia 4 de un largo de perfil (align), extendio el martes hasta
  tocar el borde de su propia invalidacion con el CPI, perdio esa invalidacion el miercoles
  (narrativa rota, la tesis de 5 dias murio) y pasa el resto de la semana confirmando el corto con
  dolar y rendimientos en contra, fallando dos rebotes de conviccion alta en el camino. Sale
  confirmada bajista, con la calibracion de EM mas floja de los 5 esta semana.
- **YM**: entro con el margen mas estrecho de la racha (12pts de sobrevivir su propia
  invalidacion el lunes), rompio y devolvio la ruptura completa con el CPI el martes (el giro mas
  fragil del complejo), paso el miercoles en rango bajo (15-25% del ADR) y cerro la semana
  confirmando el corto reinstalado bajo 52293. Sale en corto, el indice con el regimen mas
  indeciso de los 5.
- **CL**: entro con la primera grieta real del corto de 6 dias el lunes, la vio desmentirse el
  martes con el CPI (corto reafirmado con autoridad), acumulo evidencia de un giro posible el
  miercoles (barrida+reclamo del PWL) pero cerro la semana con un techo 89.15-89.64 repetido tres
  dias y la invalidacion todavia intacta. Sale confirmado bajista, el mas estable
  direccionalmente de los 5 pese a la prueba del miercoles.
