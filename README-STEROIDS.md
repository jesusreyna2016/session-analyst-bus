# Session Analyst · STEROIDS v2

Upgrade drop-in del bus público
[`jesusreyna2016/session-analyst-bus`](https://github.com/jesusreyna2016/session-analyst-bus).

El bus ya transporta método, state, live feeds y planes. **No** traía el overlay Pine ni el
Command Center (viven en TradingView + tradedadlog.com). Este paquete los mete al bus como
artefactos first-class y refuerza el método para emitir el contrato compartido.

## Arquitectura

```
                    ┌─────────────────────────────┐
   live/market.json │  Session Analyst (cloud)    │
   state/sa-state   │  method/instructions.md     │──► plans/latest.json
   heartbeat/health │  (+ §6.2 tvPayload)         │    plans/digest.txt (TV …)
                    └─────────────┬───────────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              ▼                   ▼                   ▼
     hud/tv-payload.js   overlay/sa_plan_overlay_v2   hud/command-center-2.html
     scripts/build-…mjs  (TradingView Pine v6)        (static HUD 2.0)
              │                   │                   │
              └──────── same key=value payload ───────┘
```

## Qué añade

| Pieza | Rol |
|-------|-----|
| `method/instructions.md` | Método base **reforzado** (español, estructura intacta) + Overlay v2 + checklist mandatorio |
| `method/payload-schema.md` | Spec de claves classic + v2 |
| `method/watchdog.md` | Warn opcional si falta `tvPayload` post-steroids |
| `overlay/sa_plan_overlay_v2.pine` | Dibuja AZ/BZ/NT/FVG/INVAL/STOP/T1/T2 + panel + alerts |
| `hud/command-center-2.html` | HUD oscuro: health strip, timeline, heat GO/WAIT/AVOID, drill-down, Copy TV |
| `hud/tv-payload.js` | Builder compartido (browser + Node) |
| `scripts/build-tv-payload.mjs` | CLI plan → payloads |
| `fixtures/*` | Classic + v2 samples + plan snippet |

## Claves Overlay v2 (nuevas)

`VSCORE`, `FCONFLICT`, `WHIP`, `DIR` (`LONG|SHORT|INDECISO`), `HYP`, `PRED` —
todas opcionales; classic sigue funcionando.

## Qué no hace

- No clona el repo (este paquete se construyó vía `raw.githubusercontent.com`).
- No inventa análisis de mercado: el método instruye al agente.
- No sustituye el CC de producción de golpe: dual-run classic/v2.

## Apply

Ver [`APPLY.md`](./APPLY.md).
