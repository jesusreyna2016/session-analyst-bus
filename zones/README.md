# Agente de aprendizaje de zonas (Mi Mesa)

Mide las zonas de entrada de Mi Mesa (motor `tradedadlog/netlify/functions/_intraday.mjs`, indicador
`tdl-indicators/mi_mesa_zonas.pine`) y las cruza con los trades reales de Jesus, para ir ajustando los pesos
del motor con experimentos medidos. Mismo esquema que el agente de Scalp CC (`scalp-cc-bus`).

```
zones/events/<dia CT>.jsonl  eventos del indicador (Netlify cron, cada 30 min): nueva(A+) tocada armada funciono invalidada
zones/trades.json            trades de Mi Mesa SIN dinero (R, lado, hora, precio, zona del plan)
zones/weights.json           pesos vigentes (active) y en prueba (shadow) del motor
zones/experiments.json       experimentos (proposed -> shadow -> active | rejected | reverted)
zones/analyze_zones.py       analisis (python3, sin dependencias) -> report.md, report.json, state.json
zones/state.json             resumen corto que muestra Mi Mesa (pestaña Zonas)
zones/agent-instructions.md  metodo del agente (rutina diaria + revision semanal)
zones/reviews/               revisiones semanales con propuestas
```

## Campos de un evento (linea de `events/*.jsonl`)

`sym ev id side lo hi grade entry stop tp1 size conf t receivedAt` y `f` (contexto):
`score scoreS gradeS wv wsv al(1 a favor, 0 neutral, -1 contra) reg sess(asia|london|ny|off) rr dist(ATR)
chop str(estirado, ATR del VWAP) keys(niveles que coinciden, separados por +) tf risk(puntos) mfe mae(en R, al resolverse)`.

## Un trade (`trades.json`)

`id day fam side topen tclose entry exit R session hasPlan zoneId zoneLo zoneHi zoneGrade zoneManual plannedR
planStop planTarget setup againstBias followed emotion`. Nunca dinero.

## Historico (backtest)

`backtest/backtest.mjs` corre el motor del indicador (`tdl-indicators/mi_mesa_zonas.pine`) sobre las velas de 5 min
del bus (`bars/`) y escribe `backtest/events.jsonl` con el mismo formato que el webhook, mas tres R por zona:
`rx` (entrar al cierre de la vela del gatillo), `rl` (orden limite en la entrada de la zona) y `rp` (gatillo y
luego limite si el precio regresa a la entrada). `analyze_zones.py` lo reporta aparte ("Historico"). Pesos de
prueba: `BACKTEST_WEIGHTS='{"chop":1.5}' node zones/backtest/backtest.mjs`.
