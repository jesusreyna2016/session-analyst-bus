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

## No aplicado (fuera de alcance aquí)

- Regenerar `live/journal.json` (pipeline externo; stale desde 2026-09-08).
- Arreglar indicadores TV que producen `orb@GC/CL frozen` (revisión manual TradingView).
- `zonePriors` (weekly lo dejó como observación).
