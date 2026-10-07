# Catch-up · rehacer una corrida del Session Analyst que no salió

Lo usa el Watchdog (paso "Auto-reparación" de `method/watchdog.md`) cuando una corrida
programada no dejó commit. Corres la corrida COMPLETA, como si fueras la rutina original,
con `RUN_TYPE=<el que faltó>`. Mismas reglas, mismos archivos, mismo commit.

1. Ya estás en `main` al día (`git pull --rebase --autostash origin main`).
2. Día CT: `TZ=America/Chicago date +"%A %Y-%m-%d %H:%M"`. Si es Saturday, no hay corrida.
3. Lee `method/instructions.md` ENTERO y aplícalo al pie para ese `RUN_TYPE`, incluida la
   sección "Fecha del ciclo · `<hoy>`" (la fecha de ciclo NO es el reloj de pared).
4. Lee `state/sa-state.json`, `state/trader-profile.json`, `live/market.json` y, si existe,
   `live/journal.json`. Si `market.json.builtAt` tiene > 6 h en día hábil, marca el plan
   "datos rezagados" y sigue.
5. Haz el análisis de ese `RUN_TYPE` EXACTAMENTE como lo define el método (pre-asia = pesada,
   con cierre y calificación del día; pre-london / pre-ny = updates enfocados; asia-2 = update
   ligero). Todo lo obligatorio por instrumento: `verdict`, `thesisAlign`, `prevDay`, `gap`,
   `smt`, `counterCase`, `predictions`; `alarm` solo si aplica.
6. Escribe (JSON válido, sin comentarios):
   - `plans/latest.json` y `plans/<HOY>-<RUN_TYPE>.json`
   - `plans/digest.txt`
   - `live/heartbeat.json` = `{ lastRun, runType, ok, note }` con `note` empezando por
     `"catch-up: "` (para que se vea que salió tarde y por qué).
   - `state/sa-state.json` (merge, nunca reemplazo)
   - solo pre-asia: `reviews/<AYER>.md`
6b. `python3 method/check_plan.py` tiene que dar `OK personalization` antes del commit
   (campo `personal`, sección 4.1). Si falla, arregla y repite.
7. Commit con el MISMO mensaje que la rutina original, más el sufijo:
   `git add -A && git commit -m "sa <RUN_TYPE> <HOY> (catch-up)"` y el bucle de push
   habitual (6 intentos, `sleep 5`). Verifica `git log origin/main -1 --oneline`.
8. En el plan, `dataHealth` lleva la línea `"catch-up: corrida rehecha por el watchdog a las
   <HH:MM CT>, <n> min tarde"` para que Jesus sepa que el plan llegó tarde.
