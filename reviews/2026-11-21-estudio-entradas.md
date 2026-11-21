# Estudio de entradas y salidas · zonas del Session Analyst · 2026-11-21

Fuente: `python3 method/entry_study.py --since 2026-10-01` (planes pre-asia/london/ny, velas reales de 5 min del bus,
misma ventana que `grade_plans.py`). Reglas conservadoras: vela que toca stop y objetivo = stop; en la vela del llenado
solo cuenta el stop; abierto al final = marcado al ultimo cierre.

Cuatro formas de operar cada zona:
- **gatillo + objetivo**: entrada al cierre de la vela de 5 min que confirma (lo que mide hoy `zoneEdge`), stop a
  `risk.stopPts`, todo fuera en `risk.tgtPts`.
- **gatillo + plan**: misma entrada; 1/2 en +1R, resto a BE, runner al mismo objetivo (`trader-profile.exitPlan`).
- **limite + objetivo / limite + plan**: orden limite en el borde cercano de la zona, stop en `play.structStop`.

## Resultado (desde la regla 8e, 2026-10-31)

| | gatillo + objetivo | gatillo + plan | limite + objetivo | limite + plan |
|---|---|---|---|---|
| Zonas A+ del metodo (reversion/continuacion EN CONTRA de 24 h) | +0.50R, 37%, n35 | +0.27R, 54%, n35 | -0.16R, 29%, n66 | -0.30R, 33%, n66 |
| Resto de zonas | -0.22R, 26%, n80 | -0.23R, 41%, n80 | -0.45R, 24%, n120 | -0.34R, 35%, n120 |
| Todas | -0.00R, 30%, n115 | -0.08R, 45%, n115 | -0.35R, 26%, n186 | -0.32R, 34%, n186 |

Zonas A+ por sesion (gatillo + objetivo / gatillo + plan): Asia +2.14R / +1.17R (n5), Londres -0.23R / -0.03R (n18),
NY +0.92R / +0.34R (n12).

## Lectura

1. **En estas zonas el gatillo SI paga y la limite no.** Al reves que en Mi Mesa: aqui el gatillo filtra las zonas
   que se rompen; con limite se llena tambien en las que se van de largo. No cambiar la regla de entrada del plan.
2. **El edge esta en las A+ del metodo (+0.50R, n35), y casi nunca son GO.** Desde el 31 oct solo hubo 2 GO, porque
   GO exige conviccion "alta" y la 8e deja casi todo en "baja". La alarma de "2 de 40 GO ganaron" venia de GO de antes
   de la 8e (continuacion a favor de 24 h, la combinacion que mas pierde).
3. **Londres no paga ni en las A+** (-0.23R, n18). Asia y NY si, con muestra chica.
4. **El plan de salida (1/2 en +1R + BE) baja el E[R] (+0.50 -> +0.27) y sube el acierto (37% -> 54%).** Cambia
   R por constancia; es decision de Jesus, no del metodo.

## Propuesta (para Jesus, sin aplicar)

Que una zona A+ del metodo en Asia o NY, con gatillo confirmado, cuente como operable aunque la conviccion del dia
sea "baja" (hoy queda en WAIT). Londres se queda en WAIT. Revisar con n >= 60 en A+ y cortar si el E[R] con gatillo
cae bajo +0.15R.
