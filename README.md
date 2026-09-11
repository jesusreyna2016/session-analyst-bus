# Session Analyst · bus

Canal de datos entre Netlify (que sí tiene red) y las rutinas cloud del Session Analyst (que no pueden salir a tradedadlog.com).

- `method/instructions.md` · método del agente (lo mantiene el equipo)
- `state/sa-state.json` · historial/aprendizaje acumulado (lo mergea la rutina)
- `live/market.json` · feed de mercado + noticias (lo refresca Netlify cada 5 min)
- `plans/latest.json` + `plans/<fecha>-<sesion>.json` · planes (los escribe la rutina)
- `reviews/<fecha>.md` · calificación del día (pre-asia)

Repo de trabajo, historial ruidoso por diseño. No tocar a mano salvo el método.

## STEROIDS v2

See [`README-STEROIDS.md`](./README-STEROIDS.md) for overlay Pine + HUD 2.0 apply notes (`overlay/`, `hud/`, `scripts/`, `APPLY.md`).
