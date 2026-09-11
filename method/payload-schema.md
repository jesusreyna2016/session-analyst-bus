# Overlay v2 · payload schema

Contrato entre `plans/latest.json`, el HUD Command Center 2.0, el CLI
`scripts/build-tv-payload.mjs` y el indicador Pine `overlay/sa_plan_overlay_v2.pine`.

## Formato

```
key=value;key=value;...
```

- Separador de pares: `;`
- Rangos: `lo-hi` (punto decimal OK). Ejemplo: `AZ=7615-7632`
- Espacios: no requeridos; el parser Pine / JS tolera whitespace menor alrededor de `=` y `;`
- Orden: recomendado clásico primero, luego claves v2; el parser no exige orden
- Una línea por símbolo. El agente también puede guardar `instruments.<SYM>.tvPayload`

## Claves clásicas (backward compatible)

| Key | Tipo | Ejemplo | Origen plan |
|-----|------|---------|-------------|
| `SYM` | enum | `ES` | instrumento |
| `SESS` | string | `asia` | `plan.session` |
| `BIAS` | enum | `SHORT` | `biasSession` |
| `SIG` | enum | `AVOID` | `verdict.signal` |
| `AZ` | range | `7615-7632` | `zones[0].range` (A+) |
| `BZ` | range | `7646-7666.25` | `scenarioB.zone` (omitir si = AZ) |
| `NT` | range | `7597-7607` | `noTradeZone` (recortar si invade AZ) |
| `FVG` | range | `7609-7632` | `zones[0].fvg[0].range` |
| `FVGDIR` | string | `bear` | fvg.dir |
| `FVGTF` | string | `1h` | fvg.tf |
| `INVAL` | number | `7646` | `invalidation.level` |
| `STOP` | number | `7632` | precio de `play.structStop` |
| `T1` | number | `7585.5` | `scenarioA.target` |
| `T2` | number | `7570` | `scenarioA.target2` |
| `RR` | number | `2.6` | `zones[0].risk.rr` |
| `EM` | number | `12` | `round(expectedMove.base)` |
| `WIN` | string | `2000-2300` | ventana play HHMM-HHMM |

Un payload **solo clásico** (sin claves v2) sigue dibujando el overlay y es el que emite
hoy el Command Center de tradedadlog.com.

### Ejemplo clásico (ES)

```
SYM=ES;SESS=asia;BIAS=SHORT;SIG=AVOID;AZ=7615-7632;BZ=7646.0-7666.25;INVAL=7646.0;T1=7585.5;T2=7570.0;RR=2.6;STOP=7632.0;WIN=2000-2300;NT=7597.0-7607.0;FVG=7609.0-7632.0;FVGDIR=bear;FVGTF=1h;EM=12
```

## Claves nuevas Overlay v2

| Key | Tipo | Ejemplo | Origen |
|-----|------|---------|--------|
| `VSCORE` | 0–100 | `55` | score operativo / confluence map / conviction |
| `FCONFLICT` | 0|1 | `1` | `frameConflict.on` |
| `WHIP` | 0–1 | `0.4` | `whipsawRisk.score` |
| `DIR` | enum | `INDECISO` | `LONG` | `SHORT` | `INDECISO` |
| `HYP` | string ≤28 | `nq-pre-rth` | id hipótesis abierta (sin `;` ni espacios) |
| `PRED` | string ≤40 | `range+direction+level_fi` | digest de `predictions[].kind` |

Claves desconocidas: **ignorar** (forward compatible).

### Ejemplo v2 (ES)

```
SYM=ES;SESS=asia;BIAS=SHORT;SIG=AVOID;AZ=7615-7632;BZ=7646.0-7666.25;INVAL=7646.0;T1=7585.5;T2=7570.0;RR=2.6;STOP=7632.0;WIN=2000-2300;NT=7597.0-7607.0;FVG=7609.0-7632.0;FVGDIR=bear;FVGTF=1h;EM=12;FCONFLICT=1;WHIP=0.4;DIR=SHORT;VSCORE=55;PRED=range+direction+level_fi
```

## SYM gate (Pine)

El overlay solo dibuja si `SYM` matchea el símbolo del chart. Roots aceptados de forma práctica:

- `NQ`, `ES`, `GC`, `YM`, `CL`
- micro: `MNQ`, `MES`, `MGC`, `MYM`, `MCL`
- futuros: `NQ1!`, `ESM2026`, `NQM2026`, `/NQ`, etc. (se toma el prefijo de letras)

Si no matchea → panel “SYM gate OFF”, sin boxes.

## Semántica de dibujo

| Artefacto | Condición |
|-----------|-----------|
| AZ | box lime A+ |
| BZ | box aqua B |
| NT | box dashed / borde naranja no-trade |
| FVG | box purple/teal **oculto si solapa AZ** |
| INVAL / STOP / T1 / T2 | líneas horizontales |
| Panel derecho | SIG, DIR/BIAS, RR, EM, VSCORE, FC, WHIP, HYP, PRED |

## Alertas Pine (nombres)

- `SA - Zona A+`
- `SA - SL`
- `SA - T1`
- `SA - T2`
- `SA - inval break`
- `SA - +1R→BE`

También `alert()` dinámico con mensaje que incluye SYM y nivel.

## Compatibilidad dual-run

1. Emite `tvPayload` v2 en el plan nuevo.
2. El CC viejo sigue usando solo claves clásicas al construir desde JSON (no lee `tvPayload`).
3. Overlay v2 acepta ambos.
4. Durante la transición: pega classic en un chart, v2 en otro, o usa `--classic` en el CLI.

## Fixtures

Ver `fixtures/sample-payloads.txt` y `fixtures/plan-snippet.json`.
Round-trip:

```bash
node scripts/build-tv-payload.mjs fixtures/plan-snippet.json
node scripts/build-tv-payload.mjs fixtures/plan-snippet.json --classic
```
