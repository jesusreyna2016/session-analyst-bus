# Watchdog · vigilante de datos del bus

Rutina mecánica, NO analítica. No opina de mercado. Solo comprueba que la
tubería que alimenta al Command Center y al Session Analyst sigue viva, y deja
el veredicto en `live/health.json` para que el Command Center lo pinte.

Corre 4 veces al día, ~1 h después de cada corrida del Session Analyst
(`30 1,7,14,22 * * *` UTC: tras asia-2, pre-london, pre-ny y pre-asia). En una corrida
normal no escribe planes, no toca `state/` ni `live/heartbeat.json`: su artefacto es
`live/health.json` (+ el commit). La ÚNICA excepción es la **Auto-reparación** de abajo,
donde rehace una corrida del Session Analyst que no salió.

## Entrada

Solo el checkout del repo bus. Sin red a tradedadlog.com. Lee:

- `live/market.json` — `{ builtAt, feed.symbols.<SYM>.{orb,3reads,drbias,srzones,htfzones,command}, news }`.
  Lo escribe Netlify cada ~5 min; es el espejo de todo lo que recibe la web.
- `live/heartbeat.json` — `{ lastRun, runType, ok, note }`. Última corrida del Session Analyst.
- `state/sa-state.json` — solo para leer `scorecard`/nada crítico; NO lo reescribas.
- `method/reachability.md` — regla dura de alcance; el Session Analyst debe aplicarla.
  Si el plan latest viola alcance (zona primary inalcanzable sin AVOID/WAIT claro), anótalo.

## Umbrales (mismos que la sección 2 de `instructions.md`)

`now` = hora de la corrida en UTC. **Finde (sábado/domingo CT) o feriado: relaja
todo** — el mercado está cerrado, no marques viejo lo que solo refleja eso. En
finde, `status` nunca pasa de `warn` salvo que `market.json` lleve > 24 h sin
reconstruirse.

- **`builtAt`** (snapshot entero): `ageMin = now − builtAt`.
  - ≤ 20 min → `OK`
  - > 20 min día hábil → `VIEJO` (el cron de Netlify `sa-bus-snapshot` se cortó;
    TODO lo de abajo es sospechoso).
- **Fuentes `ind-ingest`** por símbolo (`3reads`, `drbias`, `srzones`, `htfzones`,
  `command`): `ageMin = now − receivedAt`.
  - < 25 → `fresh` · 25–90 → `stale` · > 90 → `dead` · sin campo → `missing`.
- **`orb`** (backbone, de `cc-ingest`): `session-feed` le copia `updatedAt` a
  `receivedAt`, así que aplica el mismo corte de edad. **`frozen`** solo si el ORB está
  realmente parado: `orb.date` es anterior al día de `command` (no rodó de día), o
  `orb.levels.pdh/pdl` difieren de `command.raw.pdh/pdl` (esos deben ser idénticos).
  **VAH/POC/VAL NO sirven para esto**: orb_sesgo y Command calculan el perfil con binning
  distinto y en CL/GC unos pocos ticks ya pasan de 0.3 % (falsa alarma confirmada
  2026-10-05: con orb fresco a 0 min, CL poc 89.19 vs 89.43). Si VAH/POC/VAL difieren > 1 %
  con edades frescas, anótalo como dato en `note`, nunca en `issues`.
- **Webhook TradingView** (inferido, no se puede pinchar directo): mira el
  `updatedAt`/`receivedAt` más reciente de `orb` entre los 5 símbolos.
  - ≤ 15 min → `ok` · 15–60 → `lento` · > 60 día hábil → `silencioso` (el alert
    de TradingView probablemente caducó, como pasó una vez con el feed de CC).
- **`news`** (`live/market.json.news`): edad del evento/`fetchedAt` más reciente.
  > 180 min día hábil con calendario esperado → `stale`. Sin eventos y día con
  NFP/FOMC/EIA en agenda → `stale` también.
- **Corrida del Session Analyst que no salió**: lo resuelve la sección
  **Auto-reparación** (abajo), que la detecta por commit y la rehace. El `pre-asia` del
  **viernes** está en el cron (`5 21 * * 0-5`, desde 2026-10-05) y entra en la misma regla.
  (Ojo DST: en noviembre ET/CT cambian; da 60 min de gracia en la semana del cambio.)

## Salida · `live/health.json`

JSON válido, sin comentarios. Reescríbelo entero cada corrida:

```
{
  "checkedAt": "<ISO UTC>",
  "status": "ok" | "warn" | "down",
  "snapshot": { "builtAt": "<ISO>", "ageMin": <int>, "state": "OK" | "VIEJO" },
  "webhook":  { "lastSeenMin": <int>, "state": "ok" | "lento" | "silencioso" },
  "news":     { "ageMin": <int|null>, "count": <int>, "state": "ok" | "stale" },
  "sa":       { "lastRun": "<ISO>", "runType": "<str>", "lateBy": <int|null> },
  "sources": {
    "<SYM>": {
      "orb":      { "ageMin": <int|null>, "state": "fresh|stale|dead|frozen|missing" },
      "3reads":   { "ageMin": <int|null>, "state": "fresh|stale|dead|missing" },
      "drbias":   { "...": "..." },
      "srzones":  { "...": "..." },
      "htfzones": { "...": "..." },
      "command":  { "...": "..." }
    }
    // ... NQ ES GC YM CL
  },
  "issues": [ "3reads@GC dead (142 min)", "webhook silencioso (68 min)" ],
  "note": { "es": "<1 frase>", "en": "<1 sentence>" }
}
```

- `status`:
  - `down` — `builtAt VIEJO`, o webhook `silencioso`, o ≥ 3 símbolos con su
    `command` o backbone `orb` en `dead`/`missing`.
  - `warn` — cualquier `stale`/`frozen`/`lento`/`news stale`/`SA atrasada`, sin
    llegar a `down`.
  - `ok` — todo `fresh` y snapshot `OK`.
- `issues` — lista corta, la más grave primero, formato `"<qué>@<SYM> (<edad>)"`.
  Vacía si `status` = `ok`.
- `note` — una frase bilingüe. Si `ok`: `"todo fresco, N min"` / `"all fresh, N min"`.


## Journal digest
Lee `live/journal.json`. Si `updatedAt` tiene > 72 h en día hábil (lun–vie America/New_York),
añade issue `"journal stale (<n> h)"` y sube a `warn` si aún no lo está. No inventes entradas
de journal. Si el journal solo cubre 1 día reciente y faltan jornadas hábiles de la semana →
issue `"journal gaps (solo <fecha>)"` (warn).

## Orb / fuente frozen o dead (recordatorio)
`frozen` sigue la regla de arriba (fecha o PDH/PDL, nunca el perfil). Si un símbolo lleva
`frozen` ≥ 2 checks seguidos, incluye en `note` que hay que revisar el indicador/export
TradingView de ese símbolo (no es un fallo del Session Analyst).
Igual si **cualquier** fuente (`srzones`/`3reads`/…) de un símbolo va `dead` ≥ 2 checks
hábil seguidos mientras el resto del complejo está fresco o solo "muerto de finde": issue
`"<fuente>@<SYM> dead streak"` y pide revisión TV (caso visto: `srzones@GC`).

## STEROIDS · alcance de zona
El Session Analyst debe aplicar `method/reachability.md` en cada corrida. Si `plans/latest.json` trae `zones[0]` con reach inalcanzable (ratio>0.9) y verdict no es AVOID/WAIT con "sin borde a tiro", marca warn en health (`reach.unactionable=true`).

## Auto-reparación · rehacer la corrida que faltó

Antes de escribir `health.json`, mira si la corrida del Session Analyst que tocaba en esta
ventana salió. Cada corrida del watchdog vigila UNA sola corrida (la de su franja):

| Watchdog (UTC) | Vigila | Cron original | Días (UTC) |
|---|---|---|---|
| 01:30 | nada (solo salud) · `asia-2` desactivada 2026-10-05: 0 cambios de veredicto/zona en 11 ciclos | · | · |
| 07:30 | `pre-london` | 06:25 | lun-vie |
| 14:30 | `pre-ny` | 12:55 | lun-vie |
| 22:30 | `pre-asia` | 21:05 | dom-vie |

"Salió" = existe un commit con mensaje que empieza por `sa <runtype>` en las últimas 3 h:
`git log origin/main --since="3 hours ago" --format=%s | grep -E "^sa <runtype>"`.
Si NO salió y hoy le toca (tabla, y no es feriado de mercado cerrado):

1. Escribe primero `health.json` con el issue `"SA <runtype> no salió · catch-up en curso"`,
   commit `"watchdog <fecha-hora CT> (catch-up <runtype>)"` y push (así queda rastro aunque
   el catch-up falle a la mitad).
2. Sigue `method/catchup.md` con `RUN_TYPE=<runtype>`. Es una corrida COMPLETA del Session
   Analyst: aquí sí escribes `plans/`, `state/` y `heartbeat`.
3. Al terminar, reescribe `health.json` quitando ese issue y añadiendo a `note`
   `"catch-up <runtype> OK (<n> min tarde)"`, o dejando `"SA <runtype> catch-up FALLÓ: <causa>"`
   en `issues` con `status: "down"` si no pudiste.

Máximo UN catch-up por corrida del watchdog. Nunca rehagas una corrida que sí salió (aunque
saliera con asterisco o `ok:false`): eso lo juzga Jesus, no tú.

## Notificaciones al celular (`PushNotification`)

Manda **una sola** notificación por corrida, y SOLO si pasa algo de esto (si no, ninguna):

- `status` = `down`.
- Hiciste un catch-up (salga bien o mal): `"SA <runtype> no salió, la rehice (<n> min tarde)"`
  o `"SA <runtype> falló y el catch-up también: <causa corta>"`.
- Una fuente lleva `dead`/`frozen` ≥ 2 checks hábiles seguidos (compáralo con el
  `live/health.json` anterior, que lees ANTES de reescribirlo): `"<fuente>@<SYM> lleva <n> h
  caída, reinicia su alerta en TradingView"`.

Formato: una línea, < 200 caracteres, en español, empieza por lo que Jesus tiene que hacer.
Junta varias causas en la misma línea con `·`. No notifiques `warn` sueltos ni el journal.

## Subida

```
git checkout main && git pull --rebase --autostash origin main
# escribe live/health.json
git add -A && git commit -m "watchdog <fecha-hora CT>"
for i in $(seq 1 6); do git pull --rebase --autostash && git push && break; sleep 5; done
git log origin/main -1 --oneline   # debe mostrar tu commit "watchdog"
```

`live/health.json` es disjunto de lo que escriben el Session Analyst y el cron de
snapshots, el rebase aplica limpio.

## Respuesta

3–5 líneas: `status`, y si no es `ok`, la lista de `issues` tal cual. Di si el
push a origin/main quedó confirmado. Si `status` = `ok`, una sola línea:
`"watchdog OK · snapshot Nm · todo fresco · push confirmado"`.
