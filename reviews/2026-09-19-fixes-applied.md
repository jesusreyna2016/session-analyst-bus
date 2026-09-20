# Cambios aplicados · 2026-09-19 (finde)

Jesus autorizó corregir/mejorar lo necesario tras meta-review `2026-09-14/09-18`.

## Aplicado en método / watchdog

1. **EM catalizador mayor** (FOMC/NFP/CPI): +20–25% al presupuesto (no solo +10%);
   post-dato con ADR≥85% → residual/AGOTADO. `method/instructions.md` §3 calendar + §5.
2. **`whipsawRisk` categoría `extreme_range_unresolved`**: rango ≥80% ADR con poca resolución
   neta (+0.25). Calificación en §6 admite `extreme_unresolved` como hit.
3. **GO liberado por missedOps**: si missedOps rate≥0.30 n≥12 y hay A+ táctica limpia →
   permite GO (sin bajar listón de seguridad / sin GO contra sesgo).
4. **Watchdog**: `pre-asia` cron **dom-vie** + issue `SA pre-asia viernes ausente`;
   journal gaps; dead streak de fuentes (p.ej. srzones@GC) → pedir revisión TV.
5. **Reachability**: nota post-catalizador / remPts=0.

## Routine (Grok Bot)

- SA zone reach watch: zona horaria alineada a **America/New_York**; histéresis anti re-spam
  STRETCHED↔WATCH en el mismo `generatedAt`.

## Fuera de alcance (sigue pendiente humano / pipeline)

- Arreglar export TradingView `srzones@GC` (y orb frozen si vuelve).
- Regenerar journal lun–jue faltantes (pipeline externo).
- Confirmar en el runner/cloud del Session Analyst que el cron `pre-asia` incluye **viernes**.
