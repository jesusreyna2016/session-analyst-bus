# RESULT · STEROIDS v2 package

## Qué cambió

- Método (`method/instructions.md`) partido del fetch ~115KB y **reforzado** (no stub):
  secciones nuevas **§6.2 Overlay v2**, **§6.3 checklist mandatorio**, notas en digest +
  reglas de calidad. Voz/estructura española del original conservada.
- Contrato payload documentado en `method/payload-schema.md` (classic + v2).
- Pine v6 overlay nuevo con SYM gate, dibujo AZ/BZ/NT/FVG/INVAL/STOP/T1/T2, panel, alertas
  nombradas + `alert()` dinámico; claves v2 opcionales.
- HUD 2.0 estático (dark, Orbitron/JetBrains) con health strip, timeline, cards heat,
  drill-down, Copy TV / classic; fetch relativo + file inputs offline.
- Builder JS compartido + CLI Node; fixtures classic/v2 desde `plans/latest.json` real
  (asia-2 2026-09-11).
- Watchdog: nota STEROIDS + warn opcional `tvPayload missing` (no breaking).

## Fuentes fetch

| Fuente | Estado |
|--------|--------|
| raw bus README, instructions, watchdog, plans, live, reviews | OK |
| state/sa-state.json (~1.2MB) | OK — solo resumen keys/settings/scorecard/hypotheses |
| https://tradedadlog.com/command-center.html | OK (~196KB) — patrón `buildPayload` + paleta reutilizados |

## Residual risks

1. **Pine string parsing** en TV puede ser frágil con unicode dash / payloads enormes; fixtures
   cubren el happy path — validar en chart real NQ1! / ESM.
2. **VSCORE** hoy se deriva (confluence/conviction) si el plan no trae score explícito; el
   agente debe documentar la derivación o emitir número calibrado.
3. **HUD fetch CORS**: sin mismo-origen o Netlify path correcto, hay que usar file inputs.
4. **Dual-run**: el CC viejo no lee `tvPayload`; hasta que el agente emita el campo, el HUD 2.0
   construye desde JSON (OK) pero el digest puede no tener líneas `TV` aún.
5. **FVG hide-if-overlap-AZ**: heurística de overlap inclusivo; FVGs casi coincidentes con AZ
   pueden ocultarse a propósito (deseado).
6. Instructions creció ~6.7KB; weekly/overrides ya existían — STEROIDS los endurece como
   checklist, no reescribe la política weekly.

## Round-trip verificado

```
node scripts/build-tv-payload.mjs fixtures/plan-snippet.json
node scripts/build-tv-payload.mjs _fetch/plans/latest.json
```

Ambos OK en el box de build.
