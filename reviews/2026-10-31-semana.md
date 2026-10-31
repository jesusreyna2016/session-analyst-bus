# Meta-revisión semanal · 2026-10-26 a 2026-10-30

Semana de catalizadores encadenados: FOMC el miércoles, GDP avance + Core PCE (ambos
calientes) el jueves, y el viernes earnings tech + comentarios hawkish de la Fed + contagio
cripto (hackeo de Binance) sin ningún evento de calendario de alto impacto alineado con la
magnitud del movimiento. El resultado: NQ/ES/YM giraron de corto a largo el lunes, se
extendieron hasta el jueves, y revirtieron con violencia jueves-viernes para cerrar
confirmados bajistas; CL fue el único que no revirtió (alcista toda la semana). Primera
semana en que `biasHitPct`/`scenarioAHitPct`/`zoneHitPct` vuelven a traer dato fresco de
verdad (coinciden exactos con los números que `pre-asia` del 30-oct ya reportó en prosa) —
la desincronización que la propuesta 1 de `reviews/2026-10-24-semana.md` señaló parece
resuelta; no hay comparación ▲/▼ limpia contra la semana pasada porque el contador estaba
congelado, así que se trata como primera lectura viva, no como tendencia.

## Marcador de la semana por instrumento

(`biasHitPct`/`scenarioAHitPct`/`zoneHitPct` = ventana rodante `hitLog`, 47 días calificados
a 2026-10-30. `predictionScore` = tasa ponderada por `n` sobre `range+direction+level_first+
scenario+conditional` de `scorecard.predictionScore`; ▲/▼ contra los mismos números citados en
`reviews/2026-10-24-semana.md`.)

- **NQ**: sesgo 46% (n=103) · escenario A 46% (n=89) · zona 23% (n=57) · `predictionScore`
  54.5% (n=502) ▲ leve vs 53.9% (n=456). Giró largo el lunes (GIRA confirmado, 3 sesiones de
  corto murieron), extendió hasta el jueves y revirtió con autoridad extrema el viernes
  (-432.75pts, EM 13x la base) tras el GDP+PCE. `NQ|scenario` en `predictionScore` se quedó
  exactamente igual que la semana pasada (n=54, rate=0.4093, sin un solo dato nuevo) — no se
  puede confirmar la 2ª semana sobre el umbral 0.40 con muestra fresca, ver overrides abajo.
- **ES**: sesgo 45% (n=95) · escenario A 42% (n=89) · zona 23% (n=52) · `predictionScore`
  56.8% (n=519) ▲ leve vs 56.6% (n=475). Mismo patrón que NQ: giro lunes, extensión hasta el
  jueves, reversión violenta en NY el jueves y confirmación bajista el viernes (-78.5pts, EM
  10x).
- **GC**: sesgo 51% (n=92) · escenario A 42% (n=90) · zona 27% (n=56) · `predictionScore`
  57.7% (n=487) ▲ leve vs 56.8% (n=440). El instrumento con más giros de tesis de la semana:
  primera fisura real el lunes, rompió la cuna el martes, extendió alcista el miércoles,
  giró bajista el jueves y confirmó con fuerza extrema el viernes (-67.7pts, EM 7x) — y el
  modelo de distancias se quedó corto 2 veces en el mismo ciclo (Asia y Londres del viernes).
- **YM**: sesgo 52% (n=77) · escenario A 59% (n=92) · zona 19% (n=52) · `predictionScore`
  64.4% (n=457) ▲ leve vs 63.5% (n=414), sigue el mejor del grupo. Rompió el corto de 3 días
  el martes (Trend Checklist confirmó por primera vez con velas cerradas), extendió alcista
  el miércoles, y dio la lección más cara de la semana el jueves en Londres (alta convicción
  alcista perdiendo con fuerza justo antes de confirmar bajista el viernes con el mayor
  `missedOps` de la semana, +4R dejados en la mesa por WAIT de baja convicción).
- **CL**: sesgo 58% (n=89) · escenario A 54% (n=101) · zona 20% (n=55) · `predictionScore`
  58.5% (n=466) ▲ leve vs 58.4% (n=418), prácticamente plano. El único que no giró: pagó
  TP1/TP2 el lunes, repitió el patrón de reversal-sin-catalizador el martes (2ª vez) pero NO
  se repitió el miércoles con catalizador real (EIA+FOMC), extendió el jueves pese al GDP+PCE
  (único símbolo que no revirtió) y llegó a un nuevo máximo de ciclo el viernes (104.99) antes
  de un giveback parcial.
- **Global**: `predictionScore` ponderado 58.2% (n=2431) ▲ leve vs 57.7% (n=2203), sigue
  mejorando semana a semana. `emErrorTicks`/`errPctAtr`: los 5 símbolos rondan 24-28% de
  error sobre el ATR diario (CL el peor, ~28%, igual que la semana pasada ~29%, sin alivio) —
  el patrón real de la semana fue bimodal: EM corto en Asia del lunes (rango ya consumido
  antes de la sesión) y EM reventado por 5-13x en Londres/NY del jueves-viernes (días de
  tendencia real que el bucket AGOTADO sigue sin capturar, ver propuesta 1).

## Dónde falló (blindSpots) y lo que mejor paga (strengths)

- **Blind spots con más muestra**: `bias|ALL|news=high` 39% (n=127, vs 50% promedio) — el
  sesgo rinde 11pp peor cuando hay noticia de alto impacto, justo el tipo de semana que fue
  ésta. `bias|CL|conviction=media` 39% (n=36, vs 58% promedio) — la banda media de convicción
  de CL es la más floja del símbolo. `zone|NQ|conviction=media` 12% (n=41, vs 23% promedio) —
  las zonas NQ en convicción media casi nunca funcionan como se esperaba.
- **Mejores fortalezas**: `bias|CL|conviction=baja` 77% (n=41) — la convicción baja de CL es,
  contraintuitivamente, la más confiable. `bias|ALL|bias=neutral` 70% (n=41) — llamar
  "neutral" cuando de verdad lo es sigue siendo la lectura más sólida del bus.
- Ningún blind spot de los de mayor n se repite textual de la semana pasada (no hay lista
  comparable en `reviews/2026-10-24-semana.md`); no se dispara ningún `overrides` nuevo de
  convicción por esta vía esta semana.

## Plan vs ejecución

Sin número limpio esta semana: `scorecard.execution` no tiene sub-objeto `planFit` (solo
`ALL`, agregado de cuenta a 45 días, sin desglose in-plan/off-zone/against), y los 3 días con
dato en `live/journal.json` (26, 27 y 29 de oct.) llegaron con `graded:0` (sin trades
clasificados contra sesgo/zona) — mismo patrón de varias semanas seguidas, no achacable a
esta corrida. No se puede decir si lo "en plan" ganó más que lo "fuera de zona" esta semana
con datos reales; queda como limitación conocida (ver propuesta 2026-10-17 aún abierta).

## Contexto fuera del gráfico

El calendario explicó casi todo: FOMC miércoles (giveback real pero sin romper tesis), GDP
avance + Core PCE jueves (reversión violenta y generalizada en NQ/ES/YM, GC incluido) y el
viernes sin evento de calendario de alto impacto USD pero con titulares que sí explicaron la
amplitud (venta de tech tras resultados, comentarios hawkish de la Fed, hackeo de Binance
$6.3B) — el `crossAsset.tone` de riesgo-off del viernes fue a favor del resultado bajista en
NQ/ES/YM pero en contra de CL, que extendió alcista pese al mismo titular de riesgo-off.

## Ejecución de la semana

`live/journal.json` solo tiene entrada para lunes, martes y jueves (26, 27, 29-oct);
miércoles y viernes (28, 30-oct) sin ninguna entrada — `updatedAt` sigue clavado en
2026-10-29T20:29Z, 2 días sin refrescar. De los 3 días con dato: **2/3 disciplinados** (67%,
▲ fuerte vs 17% del rollup de 42 días), `revenge` en 2/3 (67%, ▼ vs 43% del rollup),
`overtrade` en 1/3 (33%, ▲ vs 67% del rollup), `roundTrip` en 2/3. Peor racha de pérdidas de
la semana: 3 (lunes y jueves), lejos de las 6 seguidas de la semana pasada. Calidad de
salida con las 17 posiciones de los 3 días: **0 parciales** (0%, 7ª+ semana seguida sin
cobrar un solo parcial), 1 scratch (6%), 10 stops completos (59%, ▲ leve vs 53% del rollup).
`wlPtsRatio` entre 0.72 y 2.8 según el día. Lectura: cuando hay dato, la disciplina mejora
(revenge sigue siendo la fuga que manda), pero la fuga de salida (`homerun-exit`, cero
parciales) no muestra ningún alivio.

**Perfil del trader** (`state/trader-profile.json`, bloque `observed`): reescrito con la
ventana de la semana y la nota del hueco miércoles-viernes. `exitBaseline` refrescado desde
`../scalp-cc-bus/exit-baseline.json` (asOf 2026-10-31): NQ n=8485 (antes 6702), hit1R 33.1%
(≈ igual), stoppedOut 47.8% (+0.4pp), reachedTP2 4.9% (+0.7pp) — mismo tono: el home run
sigue siendo raro, el parcial temprano sigue siendo la palanca que falta.

## Qué se repitió

1. **El modelo de distancias de zona bajo estiramiento extremo (>5 ATR) se quedó corto, dos
   veces en el mismo ciclo**: GC necesitó re-mapear la zona de pullback más cerca en Asia del
   viernes (zona original 4036-4051 nunca se tocó) y otra vez en Londres de la misma noche
   (la nueva zona 4002.7-4011.5 tampoco sobrevivió). Los otros 4 instrumentos re-mapearon
   zonas la misma Asia por el mismo motivo. Ver propuesta 2.
2. **El bucket AGOTADO sigue sin frenar ni limitar el recorrido en días de tendencia real**:
   NQ/ES/GC/YM "over" por 5-13x el EM base en Londres/NY del viernes — 4ª+ confirmación de
   `R-NQ-agotado-no-limita-sesion`, ahora generalizada a 4 símbolos el mismo día. Ver
   propuesta 1.
3. El hueco de `live/journal.json` (2 de 5 días sin dato) es la 3ª vez en 5 semanas que pasa
   dentro de la ventana semanal — no es un campo que controle el Session Analyst, pero se
   sigue nombrando en `trader-profile.observed.window` cada vez que ocurre.

## Cambios de la semana

### Auto-aplicables

- Sin cambios en `overrides.predictionSkip`: `NQ|direction` (rate=0.3971, n=34) sigue justo
  bajo el umbral 0.40 — más cerca que nunca, vigilar la próxima semana. `GC|range`
  (rate=0.3723, n=47) sigue bajo el umbral, subiendo. `NQ|scenario` (rate=0.4093, n=54) sigue
  arriba del umbral pero **sin un solo dato nuevo esta semana** (mismo n/rate exacto que
  `reviews/2026-10-24-semana.md`) — no se puede confirmar la 2ª semana de muestra fresca
  sobre 0.40 que exige el retiro; se mantiene el override una semana más.
- `convictionBar4`: ningún símbolo llega a `n≥20` en el bucket "alta" (máximo NQ n=8). Sin
  cambio.
- `zonePriors`: mismo bloqueo que las 2 semanas pasadas — `state.zones` sigue sin guardar el
  conteo crudo pre-encogimiento por arquetipo (cada clave `<SYM>|<sesión>|<tipo>` tiene su
  propio `winN`, no hay un pool único reconstruible con confianza). Sin cambio.

### Propuestas de método

1. **El bucket AGOTADO (día >=90-150% del ATR ya usado) sigue sin limitar el reparto de EM
   en días de tendencia real**, ahora confirmado en 4 símbolos el mismo día (NQ/ES/GC/YM,
   5-13x el EM base en Londres/NY del 30-oct, día que ya abría la `pre-asia` con `rangePct`
   >150%). Propuesta: generalizar `R-NQ-agotado-no-limita-sesion` a ES/GC/YM y subir el
   `mult` de `emCalibration` para la celda AGOTADO en vez de mantenerlo como regla aparte por
   símbolo. Campo: `method/instructions.md` sección 2 (chequeo de frescura / `emCalibration`)
   y `state.scorecard.emCalibration.mult` por celda.
2. **El score de zonas no escala la distancia proyectada cuando el día abre con
   estiramiento extremo (>5 ATR)**: las 5 zonas de pullback de la Asia del 30-oct quedaron
   obsoletas sin tocarse, y GC repitió el mismo fallo en Londres de la misma noche (2ª vez en
   el ciclo). Propuesta: cuando `stretchAtr` de apertura de sesión supere 5, escalar la
   distancia de la zona candidata por un multiplicador de estiramiento antes de puntuar
   confluencia, en vez de usar la distancia nominal del cluster. Campo:
   `method/instructions.md` sección 4 (score de zonas / `play`).
3. **`whipsawRisk` sigue sobreestimando el chop de YM**: calibración rodante
   `whipsawCal.YM` = 46% (n=74), la peor de los 5 (NQ 53%, ES 62%, GC 66%, CL 47%). Esta
   semana lo confirmó: YM e ES marcaron `whipsawRisk>=0.5` en las 3 sesiones del 30-oct, día
   que resolvió con autoridad total en las 3. Propuesta: revisar si el peso de
   `frameConflict.on` dentro del cálculo de `whipsawRisk` está inflando el score de YM más de
   lo que paga. Campo: `method/instructions.md` sección 2 (regla de `regime.chop` /
   `whipsawRisk`) y sección 3.9 (criterio de conviction/verdict).

## Lección de la semana

Dos catalizadores de calendario (FOMC, GDP+PCE) y un día entero de titulares sin calendario
(earnings tech, Fed hawkish, cripto) rompieron tesis de varios días en una sola sesión cada
vez, y el bucket AGOTADO sigue sin capturar la magnitud de esos días — el WAIT disciplinado
sin confluencia real sigue protegiendo del lado de las pérdidas (0 GO perdedores por
`frameConflict` otra vez), pero dejó `missedOps` reales (GC|londres, YM|ny) cuando el motor
fusionado tardó un ciclo completo en confirmar lo que el precio ya había resuelto.

## Régimen: cómo entró y cómo sale cada instrumento

- **NQ**: entró confirmado bajista día 2-3, giró con fuerza el lunes (GIRA confirmado, el
  corto de 3 días murió sin cierre sostenido sobre su invalidación), extendió alcista hasta
  el jueves, y el GDP+PCE lo revirtió con violencia (-429pts solo en NY) antes de confirmar
  bajista con autoridad extrema el viernes (-432.75pts netos, EM 13x la base). Sale en
  tendencia bajista día 1 confirmada, el instrumento más estirado del complejo.
- **ES**: mismo guión que NQ con un día de retraso en cada giro — lunes GIRA, extensión hasta
  el jueves, reversión violenta en NY el jueves, confirmación bajista el viernes (-78.5pts,
  EM 10x). Sale confirmada bajista día 1, la ruptura menos ambigua de los 5.
- **GC**: entró con la racha de 5 días sin fisura, tuvo su primera fisura real el lunes (sin
  romper el techo), rompió la cuna el martes, extendió alcista el miércoles pese al FOMC,
  giró bajista el jueves (GDP+PCE) y confirmó con fuerza extrema el viernes (-67.7pts, EM
  7x) — con el modelo de distancias quedándose corto dos veces en el mismo ciclo. Sale
  confirmada bajista día 1-2, el instrumento que más veces cambió de tesis esta semana.
- **YM**: entró en sesgo corto de baja convicción, rompió el corto el martes (primera
  confirmación del Trend Checklist con velas cerradas en la racha), extendió alcista con
  autoridad el miércoles, dio la lección más cara de la semana el jueves en Londres (alta
  convicción alcista perdiendo con fuerza) y confirmó bajista el viernes con el mayor
  `missedOps` de la semana (+4R dejados en WAIT). Sale confirmada bajista día 1-2.
- **CL**: entró en ruptura alcista día 2, pagó TP1/TP2 el lunes, repitió el patrón de
  reversal-sin-catalizador el martes (2ª vez) pero NO se repitió el miércoles con catalizador
  real (EIA+FOMC), extendió el jueves siendo el único símbolo que no giró con el GDP+PCE, y
  llegó a un nuevo máximo de ciclo el viernes (104.99) antes de un giveback parcial que la
  calificación automática marcó "broken" aunque el objetivo ya se había alcanzado. Sale
  alcista confirmado, el más resiliente del grupo, con el patrón de reversal-sin-catalizador
  todavía vivo cuando no hay evento real de por medio.
