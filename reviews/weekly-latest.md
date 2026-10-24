# Meta-revisión semanal · 2026-10-19 a 2026-10-23

Ventana: lunes 10-19 a viernes 10-23. Primera vez en varias semanas en que
`reviews/<viernes>.md` llegó completo el mismo sábado sin el retraso habitual del
scheduler externo (ver nota en `method/instructions.md` sección 1) — el viernes 10-23 sí
disparó y cerró el día. Semana de resoluciones: NQ y ES rompieron el conflicto de marcos
más largo del bus (7+ días) para confirmar bajista, GC extendió su racha más limpia (día 5
sin fisura), YM resolvió con autoridad pero mal calibrado en magnitud, y CL resolvió un
conflicto de 12 días al alza sin ningún catalizador de calendario. El viernes además tuvo
un apagón del motor fusionado de ~24h en NQ/ES/GC/CL que forzó WAIT en los 5 instrumentos
las 3 corridas — costoso en `missedOps`, no en criterio.

## Marcador de la semana por instrumento

(`biasHitPct`/`scenarioAHitPct` = cifras rodantes de `scorecard`; ▲/▼ contra
`reviews/2026-10-17-semana.md`. Nota dura: ambos sub-objetos no recibieron un solo dato
nuevo esta semana — ver "Qué se repitió" — así que su ▲/▼ real es "plano, sin dato nuevo",
no una lectura de mercado.)

- **NQ**: sesgo 52% (n=53) plano, sin dato nuevo · escenario A 30% (n=57) plano, sin dato
  nuevo (sigue bajo el piso de 30%, candidato débil) · EM: fuera de banda la mayor parte de
  la semana (lunes corrió +227/+601/+1094 ticks sobre presupuesto en las 3 sesiones; viernes
  whipsaw real, el día más violento de los 5, tal como `whipsawRisk=0.5` de pre-ny
  anticipaba) · `predictionScore` ~53.9% (n=456) ▲ vs ~49.3% (n=308). El conflicto de marcos
  de 7+ días se rompió al alza el jueves (ROTA, día 1 corto) pero no sobrevivió ni una
  sesión: confirmó bajista jueves-viernes con 2 mechas fallidas seguidas sobre la
  invalidación escrita (29216) sin cierre sostenido — 2/2, vigilar una 3ª.
- **ES**: sesgo 54% (n=47) plano, sin dato nuevo · escenario A 38% (n=56) plano, sin dato
  nuevo · EM: overruns moderados (+202tk en NY el lunes) y un roce a medio tick de su propia
  invalidación el viernes sin romper banda con autoridad · `predictionScore` ~56.6% (n=475)
  ▲ vs ~52.4% (n=336). La continuación alcista de varias sesiones se rompió el jueves (ROTA,
  corto día 1) y confirmó bajista jueves-viernes con la misma mecánica de mecha-fallida que
  NQ (`R-ES-fragilidad-repetida-mismo-cluster`).
- **GC**: sesgo 51% (n=48) plano, sin dato nuevo · escenario A 30% (n=56) plano, sin dato
  nuevo (sigue candidato débil) · EM: el más disciplinado de la semana, sin fisura real en 5
  sesiones · `predictionScore` ~56.8% (n=440) ▲ vs ~51.4% (n=310). Cierra la semana en su
  racha más limpia: día 5 de tendencia bajista sin una sola fisura, con las 3 zonas A+
  (confluencia 6-7) del viernes reached+respected — `missedOps` puro, el verdict quedó en
  WAIT por el apagón del motor, no por falta de edge.
- **YM**: sesgo 63% (n=39) plano, sin dato nuevo (sigue el mejor del grupo) · escenario A
  42% (n=53) plano, sin dato nuevo · EM: la peor calibración de magnitud de la semana — el
  viernes "AGOTADO" al 97% del ATR con ~19pts de presupuesto restante terminó corriendo
  354pts extra (15x), nueva hipótesis abierta (`H-2026-10-23-agotado-no-frena-continuacion`)
  · `predictionScore` ~63.5% (n=414) ▲ vs ~56.6% (n=282), el mejor del grupo otra vez.
  Régimen más volátil del complejo: 3 reversas de tesis en 24h el jueves (round-trip 486pts,
  `extreme_range_unresolved`) antes de confirmar bajista el viernes con la magnitud mal
  leída.
- **CL**: sesgo 58% (n=48) plano, sin dato nuevo · escenario A 42% (n=53) plano, sin dato
  nuevo · EM: el peor calibrado reciente por `errPctAtr` (~29% de error promedio
  asia/ny/london) y 3ª sesión seguida rompiendo la banda alta sin catalizador (el próximo
  EIA cae el miércoles que entra) · `predictionScore` ~58.4% (n=418) ▲ vs ~50.5% (n=292). El
  conflicto de marcos de 12 días (el más largo medido en el bus) se resolvió al fin al alza
  jueves-viernes sin ningún catalizador de calendario, extendiendo con autoridad — 2 zonas
  A+ más de `missedOps` el viernes.
- **Global**: `predictionScore` ponderado ~57.7% (n=2203) ▲ fuerte vs ~52.0% (n=1528) — la
  mejor semana medida del bus, sostenida por resoluciones de tesis limpias en los 5
  instrumentos a la vez. Pero el apagón del motor fusionado del viernes (~24h en
  NQ/ES/GC/CL) costó oportunidades reales medidas (`missedOps`: GC×3, CL×2, confluencia
  6-7) — el criterio de "convicción tope baja sin motor" protegió de pérdidas pero dejó
  ≥1R en la mesa varias veces; ver propuesta 2 abajo.

## Ejecución de la semana

Semana con hueco de datos real: `live/journal.json` solo tiene entrada para lunes-miércoles
(10-19, 10-20, 10-21); jueves y viernes (10-22, 10-23) no tienen ninguna entrada —
`updatedAt` del journal sigue clavado en `2026-10-21T09:14Z`, ahora 3 días sin refrescar. Es
un retroceso: la semana pasada fue la primera en varias con los 5 días cubiertos.

De los 3 días con dato: **0/3 disciplinados** (0%, ▼ vs 1/5 la semana pasada), `revenge` en
los 3 (100%), `overtrade` en 2/3, `roundTrip` en 2/3, con la peor racha de pérdidas en
semanas el miércoles (6 seguidas). Ningún día trajo trades `graded` por sesgo/zona esta
semana (`graded:0` los 3 días), así que no se puede medir contra-sesgo/fuera-de-zona
específico de la ventana — solo la ventana rodante (37 días, hasta 10-21): disciplinado
14% ▼ leve vs 15%, contra-sesgo 33% =, fuera-de-zona 52% =.

Calidad de salida con muestra parcial (17 posiciones en los 3 días con dato): **0
parciales** (0%, 6ª+ semana seguida sin cobrar un solo parcial), 0 scratches, 9 stops
completos (53%), `wlPtsRatio` entre 1.11 y 1.72 según el día. La ventana rodante de 37 días
confirma el mismo patrón: `partialRate` 2% =, `scratchRate` 4% =, `fullStopRate` 51% ▲ leve
vs 49% — la fuga `homerun-exit` sigue sin alivio y la racha de pérdidas del miércoles
(revenge+overtrade+6 seguidas) es la peor marca de disciplina de las últimas semanas.

**Perfil del trader** (`state/trader-profile.json`, bloque `observed`): reescrito con la
ventana rodante de 37 días y la nota del hueco jueves-viernes. `exitBaseline` refrescado
desde `../scalp-cc-bus/exit-baseline.json` (asOf 2026-10-24): NQ n=6702 (antes 5960),
hit1R 32.9% (≈ igual), stoppedOut 47.4% (+0.2pp), reachedTP2 4.2% (≈ igual) — mismo tono,
el home run sigue siendo raro y el parcial temprano sigue siendo la palanca que falta.

## Qué se repitió

1. **`biasHitPct` y `scenarioAHitPct` (y, por el mismo patrón, `scenarioABHitPct` y
   `zoneHitPct`) llevan exactamente 1 semana sin un solo dato nuevo**: los 5 símbolos
   muestran el mismo `n`/`hits`/`pct` que en `reviews/2026-10-17-semana.md`, mientras
   `predictionScore` sí creció (p.ej. NQ 308→456, +148) y `emCalibration` sí se actualizó
   (`_lastDate` 2026-10-23) en el mismo periodo con los mismos 5 días de reviews calificando
   sesgo y escenario A en prosa cada día. Es el mismo síntoma que la propuesta 1 de la
   semana pasada identificó para `emErrorTicks` (ya resuelto, ahora derivado de
   `emCalibration`) — generalizado a 4 sub-objetos más que quedaron atrás. Ver propuesta 1.
2. **Hueco de `live/journal.json`**: 2ª vez en 3 semanas que el journal deja 2+ días sin
   entrada dentro de la ventana semanal (jueves-viernes esta vez), justo tras la primera
   semana con cobertura completa. No es un campo que el Session Analyst controle (el journal
   lo publica Jesús), así que no entra como propuesta de método — pero merece que
   `trader-profile.observed.window` lo nombre explícito cada vez que ocurra, como se hizo
   aquí.
3. **Mecha-sobre-invalidación-sin-cierre**: NQ y ES repitieron la misma mecánica de riesgo
   (mechar justo sobre la invalidación escrita, fallar sin cierre sostenido, revertir con
   fuerza) 2 veces cada uno esta semana — la regla ya está anotada (`R-NQ-mecha-...`,
   patrón nuevo en ES); si ocurre una 3ª vez con confirmación cruzada del trío, el corto de
   NQ/ES debería tratarse como roto, no como otra mecha.

## Cambios de la semana

### Cambios aplicados

- **Retirado** `overrides.predictionSkip["CL|range"]`: la condición que lo mantenía
  aplicado (`rate < 0.40`, `n≥20`) dejó de cumplirse 2 semanas seguidas — semana pasada
  `rate=0.40` exacto (n=30, primera semana en vigilancia), esta semana `rate=0.425` (n=32).
  Antes: aplicado desde 2026-09-12 (`n=21, rate=0.33`). Después: sin override, predicciones
  `range` de CL vuelven a ser obligatorias.
- **Retirado** `overrides.predictionSkip["YM|range"]`: misma regla — semana pasada
  `rate=0.4184` (n=49), esta semana `rate=0.4269` (n=52), 2ª semana seguida sobre el umbral.
  Antes: aplicado desde 2026-09-19 (`n=36, rate=0.3889`). Después: sin override,
  predicciones `range` de YM vuelven a ser obligatorias.
- **En vigilancia (no retirado todavía)**: `NQ|scenario` cruzó sobre 0.40 por primera vez
  esta semana (`rate=0.3922→0.4093`, `n=51→54`). Si se repite sobre 0.40 la próxima semana,
  se retira. `NQ|direction` (`rate=0.3788`, `n=33`) y `GC|range` (`rate=0.35`, `n=40`) siguen
  firmemente bajo el umbral, sin cambio.
- `zonePriors`: mismo bloqueo que la semana pasada — `state.zones` sigue sin guardar el
  conteo crudo pre-encogimiento, así que el agregado real de `bounce_val`/`golden_zone`/
  `retest_break` no se puede reconstruir con confianza (ver propuesta 2026-10-17 #3, aún sin
  resolver). Sin cambio.
- `convictionBar4`: ningún símbolo llega a `n≥20` en el bucket "alta" (máximo GC/NQ n=7).
  Sin cambio.

### Propuestas de método

1. **`biasHitPct`/`scenarioAHitPct`/`scenarioABHitPct`/`zoneHitPct` se desincronizaron de
   `predictionScore`/`emCalibration`**: los 4 primeros no recibieron un solo dato nuevo esta
   semana (mismo `n` exacto que hace 1 semana) mientras `predictionScore` creció con los
   mismos 5 días de reviews. Propuesta: la misma solución que ya funcionó para
   `emErrorTicks` (derivarlo de un sub-objeto que sí se actualiza) — que `biasHitPct` y
   `scenarioAHitPct` se deriven de `predictionScore["<SYM>|direction"]` y
   `predictionScore["<SYM>|scenario"]` respectivamente en vez de mantener un contador
   paralelo, para que no puedan quedar atrás otra vez. Campo: `method/instructions.md`
   sección 6 / `state.scorecard.biasHitPct` y `scenarioAHitPct`.
2. **El criterio "conviction tope baja sin motor fusionado" costó ≥1R real 5 veces esta
   semana** (GC×3, CL×2, confluencia 6-7, con las 4 fuentes técnicas crudas vivas y
   alineadas) durante el apagón del viernes. Propuesta: permitir GO (no solo WAIT con
   `missedOps` liberado) cuando ≥4 fuentes técnicas crudas están frescas y alineadas, aunque
   `command` esté caído — el motor fusionado es una síntesis, no la única fuente válida.
   Campo: `method/instructions.md` sección 2 (regla dura de frescura) / sección 3.9
   (criterio de conviction/verdict).
3. **Sin novedad en `sweep_onl`** (propuesta de 2026-10-17 #3, sigue bloqueada por falta de
   `rawHits`/`rawN` pre-encogimiento en `state.zones`): no se repite aquí en detalle, sigue
   vigente sin resolver.

## Lección de la semana

Dos conflictos de marcos de los más largos medidos en el bus (NQ/ES 7+ días, CL 12 días) se
resolvieron la misma semana, y los 3 compartieron el mismo patrón de resolución: no un
cambio gradual, sino una ruptura que no sobrevivió un día (NQ/ES) o una ruptura tardía sin
ningún catalizador de calendario (CL) — el fondo partido no se "derrite", se rompe de golpe
cuando por fin cede, y hasta que eso pasa el `WAIT` sostenido sigue siendo la única salida
que protege sin perder (0 GO perdedores por `frameConflict` esta semana, de nuevo).

## Régimen: cómo entró y cómo sale cada instrumento

- **NQ**: entró con el conflicto de marcos más largo del bus (7+ días) sin ceder, día 3-4 de
  whipsaw real (3ª reversión récord el lunes). El jueves por fin rompió al alza, pero no
  sobrevivió ni una sesión: confirmó bajista jueves-viernes con 2 mechas fallidas seguidas
  sobre la invalidación 29216 sin cierre sostenido. Sale confirmada bajista día 2-3, con la
  divergencia SMT de YM como única duda abierta y el patrón de mecha-fallida en vigilancia
  para una 3ª vez.
- **ES**: entró en continuación alcista extendida, sosteniendo el holdout contra el semanal
  +3 por una sesión más (miércoles, cierre sobre el árbitro 7800.50). El jueves se rompió en
  una sola sesión y confirmó bajista jueves-viernes con la misma mecánica de mecha-fallida
  que NQ. Sale confirmada bajista día 2-3, la más reciente del complejo en resolverse.
- **GC**: entró con una fisura real abierta (día 3 de tendencia, primera duda en semanas) y
  la resolvió del todo: 5 sesiones seguidas sin ninguna fisura, la racha más limpia y extrema
  del bus, cerrando la semana en un nuevo mínimo de ciclo. Sale como el instrumento más
  disciplinado, con 3 zonas A+ de la última sesión sin cobrar por el apagón del motor, no
  por falta de edge.
- **YM**: entró en el patrón de tesis-de-un-día ya puesto a prueba, con whipsaw real
  lunes-martes (trampas de ruptura en ambas direcciones). El miércoles dio el mejor día de
  calibración del bus (5/5 condicionales), pero el jueves volvió a girar 3 veces en 24h antes
  de confirmar bajista el viernes con una magnitud 15x lo estimado. Sale confirmada bajista
  día 2, pero como el instrumento menos calibrado en magnitud de la semana.
- **CL**: entró en el día del EIA (miércoles) con el conflicto de marcos más largo del bus
  (12 días) todavía sin resolver, absorbiendo un 2º round-trip extremo (100.40/96.26) que
  dejó la racha alcista viva por el margen más estrecho medido. Jueves-viernes resolvió por
  fin al alza sin ningún catalizador, extendiendo con autoridad y rompiendo su propia banda
  de EM 3 sesiones seguidas. Sale en ruptura alcista confirmada día 2, el conflicto más largo
  del bus finalmente roto.
