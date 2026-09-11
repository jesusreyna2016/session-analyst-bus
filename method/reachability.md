# Regla dura · Factibilidad / alcance de sesión

**Fuente de verdad operativa** junto a `method/instructions.md`. El agente DEBE aplicar esto en cada corrida (pre-asia, asia-2, pre-london, pre-ny).

## 6.1bis Factibilidad de zona (alcance de sesión) — REGLA DURA

Problema que esto corta: publicar una A+ "bonita" (confluencia alta) que el precio **no puede
tocar** con el presupuesto de rango que queda → el día se va sin trade y el overlay enseña
una caja inalcanzable.

### Definiciones
- `distToZone` = distancia en puntos desde `orb.price` (o last del feed) hasta el **borde
  alcanzable** de la zona a favor del sesgo:
  - SHORT: `zone.lo - price` si price < zone.lo; `0` si ya está dentro; si price > zone.hi, zona atrás.
  - LONG: `price - zone.hi` simétrico.
- `budget` = lo que queda de rango útil:
  - Preferir `command.remPts` si viene sano; si no, `expectedMove.base * (1 - dayUsedFrac)` con
    `dayUsedFrac` de `expectedMove.dayUsed` / `command.atrPctUsed` (0–1).
  - Piso: nunca uses un budget inventado; si no hay número, marca `budgetUnknown=true` y
    trata la zona como **no táctica** (solo watch).
- `reachRatio = distToZone / budget` (si budget > 0).

### Umbrales
| reachRatio | Clase | Qué hacer |
|---|---|---|
| `≤ 0.55` | **TÁCTICA** (a tiro) | Puede ser `zones[0]` y candidata a GO/WAIT con play |
| `0.55–0.90` | **ESTIRADA** | Solo `zones[0]` si no hay otra TÁCTICA; `verdict` ≤ WAIT; digiere "borde lejos" |
| `> 0.90` o `budgetUnknown` | **WATCH** (inalcanzable hoy) | **Prohibido** como única/primary play. Va a `watchLevels[]` o `zones[]` con `"role":"watch"` |

### Obligaciones por corrida (pre-asia, asia-2, pre-london, pre-ny)
1. Rankea candidatas A+/B por confluencia **y** por `reachRatio` (lexicográfico: primero
   TÁCTICA, luego confluencia).
2. `zones[0]` **debe** ser TÁCTICA si existe al menos una zona mapeada TÁCTICA a favor del
   sesgo (aunque su confluencia sea 6 y haya una WATCH con 9). La WATCH se lista después
   con `role:"watch"` y prosa "si el precio recupera…".
3. Si **no** hay ninguna TÁCTICA a favor del sesgo:
   - `verdict` = WAIT o AVOID (AVOID si además stretch ≥ 2A o chop).
   - Publica igual el mejor nivel WATCH, pero el `focus.setup` / digest deben decir
     **"sin borde a tiro; no hay trade de sesión"** — no "esperar el pullback a la A+ lejana"
     como si fuera el plan operable.
   - Ofrece **1 plan táctico alternativo** cerca de precio (`command.nearName` / `nearTk`,
     VAL/VAH/POC/VWAP/EMA50/swing) aunque sea B (confluence ≥ 4): ese es `zones[0]` con
     `role:"tactical"` y RR honesto; si el RR sale FLOJO/STOP_ANCHO, WAIT + reason claro.
4. En updates (asia-2 / pre-london / pre-ny): **recomputa alcance**. Si la A+ strategic
   sigue WATCH y el precio está en un borde táctico nuevo, **promueve** el táctico a
   `zones[0]` sin esperar a pre-asia.
5. Overlay / `tvPayload`: el payload que va a TV es el de `zones[0]` táctico (o el watch
   solo si no hay táctico — y entonces `SIG=AVOID|WAIT` obligatorio). Nunca dibujes como
   AZ una WATCH haciéndola pasar por el play del día.

### Campos JSON (aditivo, no rompe schema)
En cada zona:
```
"role": "tactical" | "watch" | "strategic",
"reach": { "distPts": <num>, "budgetPts": <num>, "ratio": <num>, "class": "TACTICAL"|"STRETCHED"|"WATCH" }
```
En el instrumento (opcional):
```
"reachability": { "hasTactical": true|false, "bestTactical": "…", "bestWatch": "…" }
```

### Calidad / checklist
Antes de escribir `plans/latest.json`, verifica:
- [ ] Si `price` y `zones[0]` implican `reachRatio > 0.90`, o bien bajaste la zona a watch y
      subiste un táctico, o el `verdict` es AVOID/WAIT con frase "sin borde a tiro".
- [ ] `digest` no invita a "esperar la A+ lejana" como único camino operable del día.
- [ ] `tvPayload` / líneas `TV` reflejan la zona táctica (o AVOID limpio).

Esta regla **no** baja el listón de confluencia: sigue exigiendo A+ (≥6) para GO. Solo
impide que una A+ inalcanzable se vista de plan del día.

## Cumplimiento
Si `instructions.md` y este archivo divergen, gana **este archivo** para alcance de zonas.
