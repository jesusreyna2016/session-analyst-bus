# Session Analyst · método cripto diario (`RUN_TYPE=crypto-close` y `crypto-ny`)

Desde 2026-10-26 (fin de semana) y **diario desde 2026-10-30**. Corrida aparte del método de
futuros: ETH y BTC (perpetuos), todos los días, porque el día cripto no se para. Jesus opera
sobre todo ETH el fin de semana, pero el plan existe los 7 días.

Dos corridas por día cripto (el día cripto es el día UTC, de 00:00 a 00:00 UTC: 19:00 CT con
horario de verano, **18:00 CT con horario de invierno desde el 1 nov**):

| RUN_TYPE | Cuándo | Qué hace |
|---|---|---|
| `crypto-close` | 00:15 UTC diario (cron en UTC, sigue al cierre aunque cambie la hora de Chicago) | **Corrida pesada.** Recién cerrada la vela diaria: califica el día cripto que terminó (sus dos corridas), arma el plan completo del día nuevo con los niveles nuevos (PDH/PDL y perfil del día anterior recién cerrados). La del **domingo** (la que abre la semana cripto, lunes 00:15 UTC) hace además la revisión semanal (sección 8). |
| `crypto-ny` | 08:45 CT diario | **Update ligero** del plan de `crypto-close`, igual que `asia-2` en futuros: lunes a viernes, después de la apertura de NY (08:30 CT) y de los datos de las 07:30 CT; sábado y domingo es el refresco de la mañana. NO re-deriva ni califica (sección 7). |

`<fecha>` = el día cripto del plan = fecha UTC en que corre (`date -u +%F`); las dos corridas de un
día comparten fecha. NO toca nada de las corridas de futuros: no escribe `plans/latest.json`,
`plans/digest.txt`, `live/heartbeat.json` ni `state/sa-state.json`.

De `method/instructions.md` reutiliza, leyendo solo esas secciones: la **regla de prosa
legible** (cabecera), la **sección 2** (significado de cada campo del feed, incluidos `regime`
y `trendcl`, y la 2b del TDL Feed), la **sección 4** (score de confluencia y clasificación
A+/B/tierra de nadie) y la **sección 4.1** (personalización con `state/trader-profile.json`).
Nunca uses el guión largo en prosa: coma, punto o `·`.

## 1 · Entrada

`live/market.json` → `.feed.crypto` = `{ ETHUSDT: { orb, "3reads", drbias, srzones, htfzones,
command, regime, trendcl?, feed? }, BTCUSDT: {…} }`. Mismo esquema por fuente que los futuros.
  Con `feed` fresca (TDL Feed, sección 2b de `instructions.md`) esa es la fuente de niveles y
  contexto y las cinco viejas pueden faltar sin contar como caída.
- Frescura: igual que la sección 2 del método (< 25 min fresca, 25–90 vieja, > 90 muerta;
  `regime` y `trendcl` con sus cortes propios). El mercado cripto está ABIERTO siempre: no
  relajes umbrales ni en fin de semana. Si `.feed.crypto` falta o un símbolo trae < 3 fuentes frescas,
  omítelo y dilo en `summary`. Si faltan los dos, escribe el plan con `instruments: {}` y
  `summary` "sin feed cripto", y termina normal (commit incluido).
- `.feed.symbols` (futuros) solo para una línea de contexto: dónde está NQ respecto a su rango
  (con el CME cerrado, dónde cerró el viernes). ETH correlaciona con el Nasdaq entre semana.
- `news`: entre semana el calendario SÍ mueve cripto. Un evento USD de alto impacto (CPI, NFP,
  FOMC, PCE) dentro de la ventana del plan → `newsRisk` ALTA, `riskWindow` de 15 min antes a
  30 min después, nada de GO en esa ventana; nómbralo en `summary`. Sin eventos en la ventana,
  `newsRisk: "NINGUNA"` (o lo que digan los titulares de abajo).
  Lee también `news.headlines` (tags `crypto`, `geo`, `trump`, `fed`): un hackeo de exchange,
  un ataque o un anuncio de Trump el fin de semana mueven cripto sin calendario. Aplica la regla
  8b de `instructions.md` (el titular modula la convicción, no crea setups) y nómbralo en `reason`.
- **Regla 8e de `instructions.md` (30 oct), versión cripto:** corre `python3 method/move24h.py`
  y guarda `move24h` por símbolo, y `vs24h` en cada zona (mismo esquema que futuros). La
  dirección de las fuentes vale solo como lectura, no decide convicción ni GO (en futuros no
  predijo nada). La jerarquía de zonas (reversión en contra de las 24 h = A+ del método,
  continuación tope B) se aplica aquí también, pero **el sesgo por defecto "fade de las 24 h"
  NO**: en cripto no está medido (n chico). Convicción en dos niveles,
  "alta" o "baja", con la misma definición de la 8e; el funding negativo (1b) puede sumar el
  punto de confluencia que ya tenía, no convierte una continuación en A+.

## 1b · Contexto cripto fuera del gráfico (regla dura, cada corrida)

Además del calendario macro de entre semana (sección 1), esto es lo que mueve a ETH, y el fin de
semana es casi lo único. Igual que en
futuros: **modula la convicción, el riesgo y los objetivos; nunca crea un setup ni una
dirección por sí solo.** La única excepción está marcada abajo (punto de confluencia por
apalancamiento). Todo sale de `live/market.json` → `macro.crypto` y `news.headlines`.

- **Derivados** (`macro.crypto.ethDeriv` / `btcDeriv`: `fundingPct` por 8 h, `fundingState`,
  `oiUsd`, `oiChg24hPct`, `longShortAccounts`, `longShortChg24h`, todo de OKX):
  * OKX topa el funding en +0.01 % por 8 h: funding positivo en el tope es lo NORMAL y no es
    señal (backtest 30 oct, 54 % al alza en 24 h). `shorts-crowded` = funding **negativo** (los
    cortos pagan): ETH subió 24 h después el 66 % de las veces, 5/5 en fin de semana (n chico,
    julio-octubre 2026). `longs-crowded` = funding en el tope Y `oiChg24hPct` ≥ +5 % (largos
    apalancados nuevos), sin backtest todavía.
    **Excepción:** con `shorts-crowded`, una zona LONG `sweep_*` o de reclaim suma +1 a su
    confluencia (máximo +1, dilo en `why`). `longs-crowded` NO suma: solo va en `counterCase`
    hasta que `byContext` lo valide (n ≥ 8).
  * Precio subiendo con OI subiendo = posiciones nuevas, el movimiento tiene gasolina. Precio
    moviéndose con OI bajando = cierres, el movimiento es más débil y suele revertir: en ese
    caso no persigas la ruptura, espera el retest.
  * `longShortAccounts` ≥ 3 = el retail muy cargado de largos (contrario): escenario de barrida
    de largos en `counterCase`.
- **Volatilidad implícita** (`macro.crypto.dvol`: `last`, `chg24h`, DVOL de Deribit):
  `chg24h` ≥ +5 = el mercado de opciones espera movimiento: ensancha stops y objetivos, nada de
  GO en zonas de menos de 0.5 % de ancho, y avisa en `riskWindow` si coincide con un titular.
  DVOL bajando y bajo (< 45) = rango: favorece los `fade_*` en bordes del perfil.
- **Gap del CME** (`macro.crypto.cmeGap`: `cmeClose`, `cmeCloseDate`, `gapPct`): el último
  cierre diario del futuro CME de ETH (16:00 CT). Solo aplica con `cmeCloseDate` = viernes, en
  las corridas del viernes noche al lunes: si |`gapPct`| ≥ 1.5 %, ese precio es un **imán**
  (hacia la reapertura del domingo 17:00 CT y, si quedó sin llenar, durante el lunes): nómbralo
  como objetivo (`tp2` o predicción `level`), **nunca como gatillo**. Si el plan va en contra
  del gap, dilo en `counterCase`. De martes a viernes no aplica.
- **Fuerza relativa** (`macro.crypto.ethBtc`: `chg24hPct`, `chg7dPct`): ETH/BTC ≤ −1 % en 24 h
  con un LONG de ETH = ETH más débil que BTC, `conviction` un escalón abajo. ≥ +1 % apoya los
  largos de ETH. Complementa la regla de divergencia con BTC de la sección 2.
- **Sentimiento** (`macro.crypto.fearGreed`: `value`, `label`, `prev`): ≤ 20 (miedo extremo) o
  ≥ 80 (codicia extrema) es contexto contrario: va en `counterCase`, no en el sesgo. Una caída
  de ≥ 15 puntos en un día = pánico reciente: las mechas hacia abajo se recompran más rápido.
- **Titulares cripto** (`news.headlines` con tag `crypto` + sub-tags `eth`, `hack`, `etf`,
  `regulation`, `liquidation`; fuentes CNBC, Cointelegraph, The Block, Decrypt, Google News):
  * `hack` de un exchange grande o de un protocolo de ETH en las últimas 24 h = `newsRisk`
    **ALTA** (`cryptoContext.risk` = "ALTO") durante las 24 h siguientes al primer titular,
    aunque el precio ya lo haya absorbido: "absorbido" solo levanta el veto de la primera hora,
    no baja el riesgo. Nada de GO en la primera hora después del titular, y WAIT si el precio
    todavía está buscando piso. Si el hackeo es de ETH o usa una función de ETH (un bridge, un
    L2, una actualización como EIP-7702), el escenario bajista de ETH pesa más que el de BTC.
  * `etf` (flujos de entrada/salida), `regulation` (SEC, leyes, demandas) y `liquidation`
    (cascadas): driver de `cryptoContext.drivers` si es un HECHO de las últimas 12 h.
  * `eth` (actualizaciones de la red, staking, Vitalik): solo si es un hecho con fecha.
  * Ignora opinión y pronósticos ("price prediction", "could", "analyst says").
- **Domingo**: en la `crypto-close` del domingo (la que abre la semana), mira `news.events` y
  `news.earnings` de la semana que entra (FOMC, CPI, NFP, megacaps): una línea en `summary`
  ("FOMC el miércoles: no cargues tamaño de swing esta noche"). Va también en la semanal.
- **Shock entre corridas** (`live/shock.json`): un shock de los últimos 60 min con `sym`
  `ALL`, `CRYPTO`, `ETHUSDT` o `BTCUSDT` → `verdict` como máximo WAIT en los símbolos que
  toca, `riskWindow` hasta 60 min después de `seenAt`, y nómbralo en `reason`.
- Si `macro.crypto` falta o un bloque trae `error`, dilo en `dataHealth.notes` y sigue sin él.

Resume todo en `cryptoContext` a nivel de plan (esquema en la sección 6).

## 2 · Lo que cambia frente a futuros

- **24/7, sin RTH**: no hay IB, overnight, gap de apertura ni sesiones CME. Los niveles
  diarios (PDH/PDL, DO, perfil VAH/POC/VAL) son los que mandan los indicadores con su propio
  corte de día (00:00 UTC en cripto). Úsalos tal cual, no los recalcules. Entre semana la
  apertura de NY (08:30 CT) es la hora de más volumen del día: la `crypto-ny` la mira.
- **Liquidez fina de fin de semana** (vie noche a dom): mechas largas y barridas de los extremos
  del rango del sábado son lo normal. Prioriza zonas de tipo `sweep_*` + reclaim y `fade_*` en bordes del
  perfil; desconfía de rupturas sin volumen (pide `regime` BREAKOUT grado A o retest).
- **Domingo 17:00 CT** (reapertura de futuros CME): ventana de volatilidad. La `crypto-ny`
  del domingo la marca como `riskWindow` y no da GO en la hora alrededor de esa apertura.
  **Gap del CME**: el de ETH viene calculado en `macro.crypto.cmeGap` (sección 1b). El de
  BTC suele actuar igual de imán; si lo puedes estimar con los niveles del feed, nómbralo como
  objetivo, nunca como gatillo.
- **ETH es el instrumento principal** (`focus` por defecto). BTC va como contexto y
  confirmación: si BTC no acompaña un movimiento de ETH (divergencia de extremos, como la SMT
  de índices), resta convicción y dilo.
- **SMT, prevDay de futuros, weekendGap de IG**: no aplican. Escribe solo lo del esquema de
  abajo.

## 3 · Riesgo (regla dura)

Lee `state/trader-profile.json` (`core`, `patterns`, `dailyRules`) y aplica la sección 4.1.
Para perpetuos, además, siempre en `play` de cada zona GO:
- stop en el libro SIEMPRE (`stop` con precio), nunca promediar en contra;
- `maxNotionalUsd` = el tope de `dailyRules` si existe; si no, $50,000 (por encima de $80k es
  la fuga medida de Jesus, ver `patterns` size-escalation);
- `qtyNote` = cantidad para arriesgar como máximo el riesgo por trade de `dailyRules`
  (si no existe, $50): qty = riesgo / distancia al stop en $.
Si `patterns` trae una alerta activa de tamaño o revancha, va en `personal.note` primero.

## 4 · Calificación del día cripto que cerró (solo `crypto-close`, antes del plan nuevo)

Primero corre `python3 method/grade_plans.py --crypto <fecha de ayer UTC>` (califica las dos
corridas de ese día, `close` y `ny`, cada una de su `builtAt` a su `validUntil`; velas
reales de `bars/`, zonas con gatillo de cierre 5m, `play.stop`/`play.tp1`; escribe
`grades/crypto/<fecha>.json`) y usa SUS resultados para las zonas y el sesgo: `worked` /
`failed` / `broken` / `untouched` salen de ahí, no de memoria. Lo que el script no decide
(predicciones de texto) lo calificas tú con lo que el feed actual permite comprobar
(precio, hod/lod de `drbias`, toques de `command.touchlog`):
- cada `prediction` con `resolveAt` ya pasado → `hit` / `miss` / `unresolved` (si el feed no
  basta para decidir, `unresolved`, no adivines);
- cada zona: `touched` (el precio entró al rango) y, si se tocó, `worked` (llegó al primer
  objetivo antes que al stop) o `failed`; si no se puede saber, `unresolved`.
Acumula en `state/crypto-state.json` (créalo si no existe, mergea si existe):
```
{ "schema": "crypto-state-1", "updatedAt": "<ISO>",
  "runs": [ { "plan": "<fecha>-close|ny", "graded": { "predictions": {"hit":n,"miss":n,"unresolved":n},
              "zones": {"worked":n,"failed":n,"untouched":n,"unresolved":n} } } ],   // últimas 40
  "scorecard": { "predictions": {"n":n,"hit":n}, "zones": {"n":n,"worked":n},
                 "byTcl": { "favor": {"n":n,"worked":n}, "contra": {"n":n,"worked":n} },
                 "bySym": { "ETHUSDT": {"n":n,"worked":n}, "BTCUSDT": {"n":n,"worked":n} },
                 "byContext": { "funding=longs-crowded": {"n":n,"worked":n}, "fg=fear": {"n":n,"worked":n},
                                "dvol=up": {"n":n,"worked":n}, "gap=above": {"n":n,"worked":n},
                                "headline=hack": {"n":n,"worked":n} } },
  "notes": [ "<aprendizaje corto, máx 10, el más nuevo primero>" ] }
```
Usa el `scorecard` como prior: si un tipo de zona o un lado lleva `n ≥ 8` con
`worked/n < 0.4`, baja su clasificación un escalón y dilo.
**`byContext`** (dónde fallas tú, igual que la regla 8d de futuros): al calificar cada zona,
súmala a las claves del contexto que tenía SU plan (`cryptoContext` de la corrida anterior):
`funding=<longs-crowded|shorts-crowded|neutral>` (de ETH), `fg=<fear|neutral|greed>` (≤ 40 /
41-59 / ≥ 60), `dvol=<up|down>` (signo de `chg24h`), `gap=<above|below|none>` (spot respecto
a `cmeClose`, `none` si |gapPct| < 1.5 o no aplica) y `headline=<hack|etf|regulation|none>`.
Si el contexto de HOY coincide con una clave con `n ≥ 8` y `worked/n < 0.4`, baja la
`conviction` un escalón y dilo con el número ("con funding cargado de largos mis zonas
funcionan 3/9").

## 5 · Plan (por símbolo)

Por cada símbolo con datos: sesgo (fondo diario/semanal + marco de sesión 1h/4h, con
convicción y si están alineados o en conflicto), régimen (`regime`, chop o tendencia),
contexto (dónde está en el perfil y respecto a PDH/PDL/DO/VWAP/EMAs), 1–3 zonas con el score
de la sección 4 (+ las reglas de `trendcl` y `regime` de la sección 2), verdict y
predicciones falsables.

`verdict.signal`: **GO** solo con una zona A+ (confluencia ≥ 6) a favor del sesgo, fuentes
frescas, sin `riskWindow` en curso y sin ir contra el Trend Checklist; **WAIT** si hay B o el
precio está lejos; **AVOID** si está en tierra de nadie o en chop sin borde a tiro.

## 6 · Salidas

1. `plans/crypto-latest.json` y copia `plans/crypto/<fecha>-<slot>.json`
   (`<fecha>` = día UTC `YYYY-MM-DD`, `<slot>` = `close` o `ny`):
```
{ "schema": "crypto-plan-1", "runType": "crypto-close|crypto-ny", "builtAt": "<ISO>",
  "date": "<fecha>", "slot": "close|ny", "validUntil": "<ISO, la próxima corrida: close → 08:45 CT, ny → 00:00 UTC>",
  "dataHealth": { "snapshotAgeMin": n, "stale": [], "missing": [], "notes": [] },
  "summary": { "es": "...", "en": "..." },
  "focus": { "sym": "ETHUSDT", "setup": { "es": "...", "en": "..." } },
  "riskWindow": null | { "from": "<ISO>", "to": "<ISO>", "why": { "es": "...", "en": "..." } },
  "cryptoContext": { "risk": "BAJO|MEDIO|ALTO",
    "deriv": { "es": "funding neutral, OI de ETH -5 % en 24 h (cierres)", "en": "neutral funding, ETH OI -5% in 24h (closing)" },
    "dvol": n, "fearGreed": n, "cmeGap": { "price": n, "gapPct": n } | null, "ethBtc24hPct": n,
    "drivers": [ { "theme": "hack|etf|regulation|liquidation|eth|geo|trump|fed", "headline": "...", "source": "...", "ageH": n,
                   "note": { "es": "...", "en": "..." } } ],
    "note": { "es": "...", "en": "..." } },
  "personal": { "patternId": "...", "note": {"es":"...","en":"..."}, "capLine": {"es":"...","en":"..."} },
  "instruments": {
    "ETHUSDT": {
      "price": n, "biasDay": "LONG|SHORT|NEUTRAL", "biasSession": "LONG|SHORT|NEUTRAL",
      "conviction": "alta|baja", "move24h": { "dir": "SHORT", "pct": -5.96 }, "regime": "CHOP|BULL|BEAR|NEUTRAL",
      "tcl": { "v": -2|-1|0|1|2, "flip": n } | null,   // v = veredicto CONFIRMADO de trendcl tal cual llega (-2..2): el signo es la direccion, 2 = tamaño normal, 1 = reducido
      "context": { "es": "...", "en": "..." },
      "levels": { "vah": n, "poc": n, "val": n, "pdh": n, "pdl": n, "dayOpen": n, "vwap": n, "pwh": n, "pwl": n },
      "zones": [ { "range": [lo, hi], "dir": "LONG|SHORT", "type": "<tipos de la sección 4>",
                   "confluence": n, "grade": "A+|B", "tcl": "favor|contra|null",
                   "vs24h": "with|against|flat",   // OBLIGATORIO (regla 8e): dir de la zona contra move24h.dir
                   "why": { "es": "...", "en": "..." },
                   "play": { "trigger": {"es":"...","en":"..."}, "stop": n, "tp1": n, "tp2": n,
                             "maxNotionalUsd": n, "qtyNote": {"es":"...","en":"..."} } } ],
      "verdict": { "signal": "GO|WAIT|AVOID", "reason": { "es": "...", "en": "..." } },
      "counterCase": { "es": "...", "en": "..." },
      "predictions": [ { "id": "ETH-1", "kind": "level|range|direction", "text": {"es":"...","en":"..."},
                         "resolveAt": "<ISO>" } ]
    },
    "BTCUSDT": { "...": "mismo esquema" }
  },
  "graded": { "plan": "<fecha de ayer> | null", "line": { "es": "...", "en": "..." } },
  "updated": null | { "es": "qué aguantó / qué cambió desde el close", "en": "..." }   // solo crypto-ny
}
```
2. `plans/crypto-digest.txt`: 4–8 líneas planas para el móvil: una por símbolo (sesgo +
   verdict + zona principal con precio), `foco: ETH ...`, la ventana de riesgo si hay, la línea
   de calificación de la corrida anterior, y `precisión: X/N predicciones · zonas W/N`.
3. `state/crypto-state.json` (sección 4, solo `crypto-close`).

Valida el JSON antes del commit (`python3 -c "import json;json.load(open('plans/crypto-latest.json'))"`).

## 7 · `crypto-ny` · update ligero (08:45 CT)

Parte de `plans/crypto-latest.json`, que debe ser la `crypto-close` de HOY (mismo `date` UTC).
Si no lo es (falta o es de otro día), arma el plan completo como `crypto-close` SIN la
calificación (sección 4) y dilo en `dataHealth.notes`.
- NO re-deriva sesgo de día, NO re-puntúa confluencia ni mueve rangos de zona, NO califica,
  NO toca `state/crypto-state.json`.
- Sí actualiza, por símbolo: `price`, `context` (una frase: qué niveles y zonas del close
  aguantaron o se rompieron en la noche y en Asia/Londres, con `feed.touchlog` y `sweep`),
  `move24h` (re-corre `move24h.py`), `biasSession` si el 1h/4h cambió de verdad, `play` de las
  zonas (gatillo ya dado, invalidación tocada, ventana vencida) y `verdict` solo si cambió de
  estado. Una zona rota se marca `broken: true`, no se borra.
- **Lunes a viernes, la apertura de NY**: cómo abrió NQ/ES el cash (08:30 CT) y si ETH
  acompaña o diverge (sección 2 de este método, correlación con el Nasdaq); el dato de las
  07:30 CT si hubo (`news.events` con `actual`, `macro.reactions`): aceptado o rechazado.
  Eso refuerza o resta convicción del plan del close (un escalón como máximo) y se dice en
  `updated`. **Sábado y domingo** no hay apertura: es un refresco de la mañana (lo que hizo
  la noche, titulares nuevos, shock); el domingo añade la `riskWindow` de la reapertura CME.
- Re-chequea `news.headlines`, `live/shock.json` y `macro.crypto` (funding, OI, DVOL): si un
  hecho nuevo cambia el riesgo, `cryptoContext` y `riskWindow` se actualizan.
- `focus`: si su setup ya disparó o se invalidó, pásalo a la siguiente mejor oportunidad viva.
- Deja intactos `counterCase`, `predictions`, `graded`, los rangos y la confluencia de las zonas.
- Salidas: `plans/crypto-latest.json`, `plans/crypto/<fecha>-ny.json` y `plans/crypto-digest.txt`
  (primera línea `SA crypto-ny <fecha> <hora CT>`, solo reescribe lo que se movió). Si nada
  material se movió, escríbelo igual con `updated` = "sin cambios materiales" y `builtAt` nuevo
  (la calificación usa la ventana de cada archivo).

## 8 · Revisión semanal cripto (la `crypto-close` del domingo, lunes 00:15 UTC)

Después del plan del lunes, la semana cripto que cerró (lunes 00:00 UTC a lunes 00:00 UTC,
las 14 corridas). Lee `state/crypto-state.json`, `grades/crypto/<7 fechas>.json` y los planes
de la semana. Escribe `reviews/crypto/<fecha del domingo CT>-semana.md` y
`reviews/crypto/weekly-latest.md` (idéntico), máximo ~60 líneas, con estas líneas fijas:
- **Marcador**: zonas worked/n y predicciones hit/n de la semana por símbolo, y close contra
  ny (¿el update de NY mejora o empeora el plan del close?).
- **Fin de semana contra entre semana**: zonas worked/n en cada uno.
- **Dónde fallo** (una línea): las claves de `byContext` y tipos de zona con peor worked/n
  (con n), y las 2 mejores.
- **Contexto fuera del gráfico** (una línea): qué drivers de `cryptoContext` (hackeos,
  funding, ETF, macro de EE.UU.) explicaron la semana y cuáles no.
- **Semana que entra**: eventos USD de alto impacto y megacaps (de `news.events` /
  `news.earnings`).
- `## Propuestas de método`: 1-3 cambios con evidencia (n, %), sin aplicarlos; "sin propuestas,
  muestra corta" si n < 8.
Súmala al commit (`git add reviews/crypto`).
