# Cambios aplicados · 2026-09-19 (finde)

Jesus autorizó corregir/mejorar lo necesario tras meta-review `2026-09-14/09-18`.

## Aplicado en método / watchdog

1. **EM catalizador mayor** (FOMC/NFP/CPI): +20–25% al presupuesto (no solo +10%);
   post-dato con ADR≥85% → residual/AGOTADO. `method/instructions.md` §3 calendar + §5.
2. **`whipsawRisk` categoría `extreme_range_unresolved`**: rango ≥80% ADR con poca resolución
   neta (+0.25). Calificación en §6 admite `extreme_unresolved` como hit.
3. **GO / missedOps (solo nota):** propuesta de liberar GO con A+ táctica si missedOps alto.
   **NO aplicada** como regla viva; queda como PROPUESTA #3 pendiente de Jesus.
4. **Watchdog**: `pre-asia` cron **dom-vie** + issue `SA pre-asia viernes ausente`;
   journal gaps; dead streak de fuentes (p.ej. srzones@GC) → pedir revisión TV.
5. **Reachability**: nota post-catalizador / remPts=0.

## Journal pipeline (2026-09-19 noche)

- Causa: `journal-ingest` reemplazaba `live/journal.json` entero; un digest de 1 día
  (filtro de cuenta / import parcial) borraba el histórico.
- Fix: merge por fecha + ventana rodante 45d en Netlify `journal-ingest` (deploy pendiente).
- Cliente journal: digest usa `DB.trades` completo, no el filtro de cuenta.
- Restore en bus: días reales recuperados de commits previos del digest (sin inventar días
  ausentes: faltan p.ej. 09-09..09-17 salvo lo que vuelva a sincronizar el journal).

## Routine (Grok Bot)

- SA zone reach watch: zona horaria alineada a **America/New_York**; histéresis anti re-spam
  STRETCHED↔WATCH en el mismo `generatedAt`.

## Fuera de alcance (sigue pendiente humano / pipeline)

- Arreglar export TradingView `srzones@GC` (recrear alerta; ver checklist).
- Deploy Netlify de `journal-ingest` + deploy mywhyjournal del fix de digest.
- Confirmar en el runner/cloud del Session Analyst que el cron `pre-asia` incluye **viernes**.
