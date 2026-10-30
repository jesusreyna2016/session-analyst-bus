# Session Analyst · método cripto de fin de semana (`RUN_TYPE=crypto-weekend`)

Desde 2026-10-26. Corrida aparte del método de futuros: ETH y BTC (perpetuos), desde el **viernes 16:00 CT
(cierre de futuros CME) hasta el domingo 17:00 CT (reapertura)**, cuando Jesus opera sobre todo ETH
(ampliado el 2026-10-30: antes empezaba el sábado y dejaba sin plan la noche del viernes).
Turnos (cron en hora de Chicago): vie 16:15 y 19:15 · sáb 08:15, 16:15 y 19:15 · dom 08:15 y
16:15. La de las 19:15 cae justo después de que abre la vela diaria de cripto (00:00 UTC):
usa los niveles del día nuevo (PDH/PDL y perfil del día anterior recién cerrados). NO toca nada de
las corridas de futuros: no escribe `plans/latest.json`, `plans/digest.txt`,
`live/heartbeat.json` ni `state/sa-state.json`.

De `method/instructions.md` reutiliza, leyendo solo esas secciones: la **regla de prosa
legible** (cabecera), la **sección 2** (significado de cada campo del feed, incluidos `regime`
y `trendcl`), la **sección 4** (score de confluencia y clasificación A+/B/tierra de nadie) y
la **sección 4.1** (personalización con `state/trader-profile.json`). Nunca uses el guión largo
en prosa: coma, punto o `·`.

## 1 · Entrada

`live/market.json` → `.feed.crypto` = `{ ETHUSDT: { orb, "3reads", drbias, srzones, htfzones,
command, regime, trendcl?, feed? }, BTCUSDT: {…} }`. Mismo esquema por fuente que los futuros.
  Con `feed` fresca (TDL Feed, sección 2b de `instructions.md`) esa es la fuente de niveles y
  contexto y las cinco viejas pueden faltar sin contar como caída.
- Frescura: igual que la sección 2 del método (< 25 min fresca, 25–90 vieja, > 90 muerta;
  `regime` y `trendcl` con sus cortes propios). Aquí el mercado está ABIERTO: no relajes
  umbrales por fin de semana. Si `.feed.crypto` falta o un símbolo trae < 3 fuentes frescas,
  omítelo y dilo en `summary`. Si faltan los dos, escribe el plan con `instruments: {}` y
  `summary` "sin feed cripto", y termina normal (commit incluido).
- Ignora `.feed.symbols` (futuros cerrados) salvo para una línea de contexto: dónde cerró NQ
  el viernes respecto a su rango (ETH correlaciona con el Nasdaq entre semana).
- `news`: el fin de semana casi nunca hay macro. Si hay un evento con `ts` dentro de la
  ventana del plan, nómbralo; si no, `newsRisk: "NINGUNA"`.
  Lee también `news.headlines` (tags `crypto`, `geo`, `trump`, `fed`): un hackeo de exchange,
  un ataque o un anuncio de Trump el fin de semana mueven cripto sin calendario. Aplica la regla
  8b de `instructions.md` (el titular modula la convicción, no crea setups) y nómbralo en `reason`.
- **Regla 8e de `instructions.md` (30 oct), versión cripto:** corre `python3 method/move24h.py`
  y guarda `move24h` por símbolo, y `vs24h` en cada zona (mismo esquema que futuros). La
  dirección de las fuentes vale solo como lectura, no decide convicción ni GO (en futuros no
  predijo nada). La jerarquía de zonas (reversión en contra de las 24 h = A+ del método,
  continuación tope B) se aplica aquí también, pero **el sesgo por defecto "fade de las 24 h"
  NO**: en cripto de fin de semana no está medido (n chico). Convicción en dos niveles,
  "alta" o "baja", con la misma definición de la 8e; el funding negativo (1b) puede sumar el
  punto de confluencia que ya tenía, no convierte una continuación en A+.

## 1b · Contexto cripto fuera del gráfico (regla dura, cada corrida)

El fin de semana no hay calendario macro, así que lo que mueve a ETH es esto. Igual que en
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
- **Gap del CME** (`macro.crypto.cmeGap`: `cmeClose`, `cmeCloseDate`, `gapPct`): el cierre del
  futuro CME de ETH del viernes. Si `cmeCloseDate` es el viernes y |`gapPct`| ≥ 1.5 %, ese precio
  es un **imán** hacia la reapertura del domingo 17:00 CT: nómbralo como objetivo (`tp2` o
  predicción `level`), **nunca como gatillo**. Si el plan es en contra del gap, dilo en
  `counterCase`. Entre semana `cmeCloseDate` es el día anterior y no aplica.
- **Fuerza relativa** (`macro.crypto.ethBtc`: `chg24hPct`, `chg7dPct`): ETH/BTC ≤ −1 % en 24 h
  con un LONG de ETH = ETH más débil que BTC, `conviction` un escalón abajo. ≥ +1 % apoya los
  largos de ETH. Complementa la regla de divergencia con BTC de la sección 2.
- **Sentimiento** (`macro.crypto.fearGreed`: `value`, `label`, `prev`): ≤ 20 (miedo extremo) o
  ≥ 80 (codicia extrema) es contexto contrario: va en `counterCase`, no en el sesgo. Una caída
  de ≥ 15 puntos en un día = pánico reciente: las mechas hacia abajo se recompran más rápido.
- **Titulares cripto** (`news.headlines` con tag `crypto` + sub-tags `eth`, `hack`, `etf`,
  `regulation`, `liquidation`; fuentes CNBC, Cointelegraph, The Block, Decrypt, Google News):
  * `hack` de un exchange grande o de un protocolo de ETH en las últimas 24 h = `newsRisk`
    **ALTA**: nada de GO en la primera hora después del titular, y WAIT si el precio todavía
    está buscando piso. Si el hackeo es de ETH (o de un bridge/L2), el escenario bajista de ETH
    pesa más que el de BTC.
  * `etf` (flujos de entrada/salida), `regulation` (SEC, leyes, demandas) y `liquidation`
    (cascadas): driver de `cryptoContext.drivers` si es un HECHO de las últimas 12 h.
  * `eth` (actualizaciones de la red, staking, Vitalik): solo si es un hecho con fecha.
  * Ignora opinión y pronósticos ("price prediction", "could", "analyst says").
- **Domingo**: en la corrida pm del domingo, mira `news.events` y `news.earnings` de la semana
  que entra (FOMC, CPI, NFP, megacaps): una línea en `summary` ("FOMC el miércoles: no cargues
  tamaño de swing esta noche").
- **Shock entre corridas** (`live/shock.json`): un shock de los últimos 60 min con `sym`
  `ALL`, `CRYPTO`, `ETHUSDT` o `BTCUSDT` → `verdict` como máximo WAIT en los símbolos que
  toca, `riskWindow` hasta 60 min después de `seenAt`, y nómbralo en `reason`.
- Si `macro.crypto` falta o un bloque trae `error`, dilo en `dataHealth.notes` y sigue sin él.

Resume todo en `cryptoContext` a nivel de plan (esquema en la sección 6).

## 2 · Lo que cambia frente a futuros

- **24/7, sin RTH**: no hay IB, overnight, gap de apertura ni sesiones CME. Los niveles
  diarios (PDH/PDL, DO, perfil VAH/POC/VAL) son los que mandan los indicadores con su propio
  corte de día (00:00 UTC en cripto). Úsalos tal cual, no los recalcules.
- **Liquidez fina de fin de semana**: mechas largas y barridas de los extremos del rango del
  sábado son lo normal. Prioriza zonas de tipo `sweep_*` + reclaim y `fade_*` en bordes del
  perfil; desconfía de rupturas sin volumen (pide `regime` BREAKOUT grado A o retest).
- **Domingo 17:00 CT** (reapertura de futuros CME): ventana de volatilidad. La corrida del
  domingo la marca como `riskWindow` y no da GO en la hora alrededor de esa apertura.
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

## 4 · Calificación de la corrida anterior (siempre, antes del plan nuevo)

Primero corre `python3 method/grade_plans.py --crypto <fecha de la corrida anterior>` (velas
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
  "runs": [ { "plan": "<fecha>-<slot>", "graded": { "predictions": {"hit":n,"miss":n,"unresolved":n},
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
   (`<fecha>` = día CT `YYYY-MM-DD`, `<slot>` = `am` si la hora CT < 12, `pm` si 12:00-17:59, `eve` si ≥ 18:00):
```
{ "schema": "crypto-plan-1", "runType": "crypto-weekend", "builtAt": "<ISO>",
  "date": "<fecha>", "slot": "am|pm|eve", "validUntil": "<ISO, la próxima corrida o +12 h>",
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
      "tcl": { "v": -1|0|1, "flip": n } | null,
      "context": { "es": "...", "en": "..." },
      "levels": { "vah": n, "poc": n, "val": n, "pdh": n, "pdl": n, "dayOpen": n, "vwap": n, "pwh": n, "pwl": n },
      "zones": [ { "range": [lo, hi], "dir": "LONG|SHORT", "type": "<tipos de la sección 4>",
                   "confluence": n, "grade": "A+|B", "tcl": "favor|contra|null",
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
  "graded": { "plan": "<fecha>-<slot> anterior | null", "line": { "es": "...", "en": "..." } }
}
```
2. `plans/crypto-digest.txt`: 4–8 líneas planas para el móvil: una por símbolo (sesgo +
   verdict + zona principal con precio), `foco: ETH ...`, la ventana de riesgo si hay, la línea
   de calificación de la corrida anterior, y `precisión: X/N predicciones · zonas W/N`.
3. `state/crypto-state.json` (sección 4).

Valida el JSON antes del commit (`python3 -c "import json;json.load(open('plans/crypto-latest.json'))"`).
