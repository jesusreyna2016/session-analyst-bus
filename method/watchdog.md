# Watchdog · vigilante de datos del bus

Rutina mecánica, NO analítica. No opina de mercado. Solo comprueba que la
tubería que alimenta al Command Center y al Session Analyst sigue viva, y deja
el veredicto en `live/health.json` para que el Command Center lo pinte.

Corre cada 6 h (`0 */6 * * *` UTC). No escribe planes, no toca `state/`, no toca
`live/heartbeat.json` (ese es del Session Analyst). Su único artefacto es
`live/health.json` (+ el commit).

## Entrada

Solo el checkout del repo bus. Sin red a tradedadlog.com. Lee:

- `live/market.json` — `{ builtAt, feed.symbols.<SYM>.{orb,3reads,drbias,srzones,htfzones,command}, news }`.
  Lo escribe Netlify cada ~5 min; es el espejo de todo lo que recibe la web.
- `live/heartbeat.json` — `{ lastRun, runType, ok, note }`. Última corrida del Session Analyst.
- `state/sa-state.json` — solo para leer `scorecard`/nada crítico; NO lo reescribas.

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
  `receivedAt`, así que aplica el mismo corte. Además contrasta
  `orb.levels.{vah,poc,val,pdh,pdl}` con `command.raw.{vah,poc,val,pdh,pdl}`: si
  discrepan > 0.3 % → `frozen` (aunque la edad sea baja).
- **Webhook TradingView** (inferido, no se puede pinchar directo): mira el
  `updatedAt`/`receivedAt` más reciente de `orb` entre los 5 símbolos.
  - ≤ 15 min → `ok` · 15–60 → `lento` · > 60 día hábil → `silencioso` (el alert
    de TradingView probablemente caducó, como pasó una vez con el feed de CC).
- **`news`** (`live/market.json.news`): edad del evento/`fetchedAt` más reciente.
  > 180 min día hábil con calendario esperado → `stale`. Sin eventos y día con
  NFP/FOMC/EIA en agenda → `stale` también.
- **Corrida del Session Analyst atrasada**: si por el reloj ya pasó el cron de
  una corrida (`pre-asia` 21:05Z dom-jue · `pre-london` 06:25Z lun-vie · `pre-ny`
  12:55Z lun-vie) hace > 45 min y `heartbeat.lastRun` sigue siendo anterior a esa
  hora con otro `runType` → añade `"SA <runtype> atrasada (<n> min)"` a `issues`.
  (Ojo DST: en noviembre CT pasa a CST, los cron UTC se corren +1 h; da 60 min de
  gracia en la semana del cambio.)

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
