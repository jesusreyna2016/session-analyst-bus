# Session Analyst · método cripto de fin de semana (`RUN_TYPE=crypto-weekend`)

Desde 2026-10-26. Corrida aparte del método de futuros: ETH y BTC (perpetuos), solo sábado y
domingo, cuando los futuros CME están cerrados y Jesus opera sobre todo ETH. NO toca nada de
las corridas de futuros: no escribe `plans/latest.json`, `plans/digest.txt`,
`live/heartbeat.json` ni `state/sa-state.json`.

De `method/instructions.md` reutiliza, leyendo solo esas secciones: la **regla de prosa
legible** (cabecera), la **sección 2** (significado de cada campo del feed, incluidos `regime`
y `trendcl`), la **sección 4** (score de confluencia y clasificación A+/B/tierra de nadie) y
la **sección 4.1** (personalización con `state/trader-profile.json`). Nunca uses el guión largo
en prosa: coma, punto o `·`.

## 1 · Entrada

`live/market.json` → `.feed.crypto` = `{ ETHUSDT: { orb, "3reads", drbias, srzones, htfzones,
command, regime, trendcl? }, BTCUSDT: {…} }`. Mismo esquema por fuente que los futuros.
- Frescura: igual que la sección 2 del método (< 25 min fresca, 25–90 vieja, > 90 muerta;
  `regime` y `trendcl` con sus cortes propios). Aquí el mercado está ABIERTO: no relajes
  umbrales por fin de semana. Si `.feed.crypto` falta o un símbolo trae < 3 fuentes frescas,
  omítelo y dilo en `summary`. Si faltan los dos, escribe el plan con `instruments: {}` y
  `summary` "sin feed cripto", y termina normal (commit incluido).
- Ignora `.feed.symbols` (futuros cerrados) salvo para una línea de contexto: dónde cerró NQ
  el viernes respecto a su rango (ETH correlaciona con el Nasdaq entre semana).
- `news`: el fin de semana casi nunca hay macro. Si hay un evento con `ts` dentro de la
  ventana del plan, nómbralo; si no, `newsRisk: "NINGUNA"`.

## 2 · Lo que cambia frente a futuros

- **24/7, sin RTH**: no hay IB, overnight, gap de apertura ni sesiones CME. Los niveles
  diarios (PDH/PDL, DO, perfil VAH/POC/VAL) son los que mandan los indicadores con su propio
  corte de día (00:00 UTC en cripto). Úsalos tal cual, no los recalcules.
- **Liquidez fina de fin de semana**: mechas largas y barridas de los extremos del rango del
  sábado son lo normal. Prioriza zonas de tipo `sweep_*` + reclaim y `fade_*` en bordes del
  perfil; desconfía de rupturas sin volumen (pide `regime` BREAKOUT grado A o retest).
- **Domingo 17:00 CT** (reapertura de futuros CME): ventana de volatilidad. La corrida del
  domingo la marca como `riskWindow` y no da GO en la hora alrededor de esa apertura.
  **BTC**: el gap CME de BTC (cierre del viernes de futuros vs precio actual) suele actuar de
  imán; si lo puedes estimar con los niveles del feed, nómbralo como objetivo, nunca como
  gatillo.
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

Lee `plans/crypto-latest.json` (si existe) y califícalo con lo que el feed actual permite
comprobar (precio, hod/lod de `drbias`, toques de `command.touchlog`):
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
                 "bySym": { "ETHUSDT": {"n":n,"worked":n}, "BTCUSDT": {"n":n,"worked":n} } },
  "notes": [ "<aprendizaje corto, máx 10, el más nuevo primero>" ] }
```
Usa el `scorecard` como prior: si un tipo de zona o un lado lleva `n ≥ 8` con
`worked/n < 0.4`, baja su clasificación un escalón y dilo.

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
   (`<fecha>` = día CT `YYYY-MM-DD`, `<slot>` = `am` si la hora CT < 12, si no `pm`):
```
{ "schema": "crypto-plan-1", "runType": "crypto-weekend", "builtAt": "<ISO>",
  "date": "<fecha>", "slot": "am|pm", "validUntil": "<ISO, la próxima corrida o +12 h>",
  "dataHealth": { "snapshotAgeMin": n, "stale": [], "missing": [], "notes": [] },
  "summary": { "es": "...", "en": "..." },
  "focus": { "sym": "ETHUSDT", "setup": { "es": "...", "en": "..." } },
  "riskWindow": null | { "from": "<ISO>", "to": "<ISO>", "why": { "es": "...", "en": "..." } },
  "personal": { "patternId": "...", "note": {"es":"...","en":"..."}, "capLine": {"es":"...","en":"..."} },
  "instruments": {
    "ETHUSDT": {
      "price": n, "biasDay": "LONG|SHORT|NEUTRAL", "biasSession": "LONG|SHORT|NEUTRAL",
      "conviction": "alta|media|baja", "regime": "CHOP|BULL|BEAR|NEUTRAL",
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
