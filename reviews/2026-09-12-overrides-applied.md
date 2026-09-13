# Cambios aplicados · 2026-09-12 (sábado)

Aplicación manual post meta-review `2026-09-07/09-11` (Jesus autorizó corregir lo conveniente).

## Cambios aplicados

1. **`state.overrides.predictionSkip`** (seguro / weekly):
   - `NQ|direction` — n=29, rate=0.33
   - `NQ|scenario` — n=29, rate=0.38
   - `ES|direction` — n=27, rate=0.37
   - `GC|range` — n=27, rate=0.24
   - `CL|range` — n=21, rate=0.33
   Cada entrada: `{ value: true, since: "2026-09-12", evidence: "…" }`.

2. **Método — shock macro no calendarizado** en `method/instructions.md` + detalle en
   `method/reachability.md` (newsRisk ALTA, EM +escalón, digest explícito).

3. **Método — update forzado** si remPts=0 / zona primary pasa a WATCH (`reachability.md`).

4. **Watchdog** — warn por `journal.json` stale >72h hábil; nota si orb frozen se arrastra.

## Añadido más tarde (2026-09-12, Jesus lo pidió explícitamente)

5. **`state.overrides.zonePriors`** (manual, autorizado por Jesus):
   - `bounce_val` → `0.68` (winN 136, +0.13 vs prior reversión 0.55)
   - `golden_zone` → `0.32` (winN 82, -0.23 vs prior reversión 0.55)
   El weekly lo había dejado como observación; se aplica ahora porque ambos cruzan
   winN≥30 y divergen >0.10 del prior de grupo (umbral de la sección 6.1). El
   encogimiento (`k=4`) sigue frenando el efecto a nivel de zona con winN bajo.

## No aplicado (fuera de alcance aquí)

- Regenerar `live/journal.json` (pipeline externo; stale desde 2026-09-08).
- Arreglar indicadores TV que producen `orb@GC/CL frozen` (revisión manual TradingView).
