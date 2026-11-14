# Trend Checklist · ¿aguanta "no tomar toques en contra"? (2026-11-14)

Scripts: `method/trendcl_edge.py` (reconstruye la prueba y el control) y `method/trendcl_edge_report.py` (tablas).

## Qué se midió
Copia fuera de TradingView de la tabla "TOQUES DE ZONA" de `trend_checklist.pine` con las reglas v2.3+:

- Niveles: EMA20 1H, DO, VWAP de sesión, TDO, PDH, PDL, pVAH / pPOC / pVAL del día anterior.
- Toque: la vela llega al nivel ± 0.03 % del precio; 60 min de enfriamiento por nivel; no cuenta la vela en que el
  nivel nace (fix v2.3).
- Operación: entrada en el nivel en el sentido del rebote (si venía de arriba, largo), carrera simétrica ± 0.15 %
  del precio, las dos en la misma vela = pérdida, a las 4 h se califica por el cierre. E[R] = resultado / distancia.
- Etiqueta: veredicto confirmado D / 4H / 1H (estructura por pivotes 3/3 con BOS + cierre frente a EMA20):
  a favor, en contra, sin veredicto.
- Datos: velas 5m del bus (`bars/`, NQ ES GC YM CL, 2026-08-21 a 2026-11-13, unos 60 días de trading, 24 h) y
  15m agregadas de ellas. TF superiores calentados con velas 1h de Yahoo (2 años).

Diferencias con el Pine: el bus no trae volumen, así que el VWAP y el perfil pesan igual cada vela; empates en
pivotes resueltos a mano. Los totales no coinciden con los de octubre (otra ventana de datos), pero las reglas sí.

## Control
Los mismos niveles desplazados ± 0.35 % y ± 0.70 % (4 niveles falsos por cada real), con las mismas reglas de
toque, carrera y etiqueta. Si "en contra" también pierde en precios al azar, lo que se ve es la tendencia, no el
indicador. Se compara la brecha (a favor menos en contra) del indicador con la del control (diferencia de
diferencias, intervalo 95 % por bootstrap de días). Además, barajado de etiquetas dentro de cada símbolo.

## Resultado global (todos los símbolos)

| TF | | a favor | en contra | sin veredicto | brecha WR [IC 95 %] |
|---|---|---|---|---|---|
| 5m | niveles | 56.4 % [55-58] n=3731 · +0.13R | 57.1 % [55-59] n=2082 · +0.14R | 57.7 % n=5815 | -0.7 pts [-6.3, +4.9] |
| 5m | control | 57.5 % n=7107 · +0.15R | 60.1 % n=6163 · +0.20R | 58.1 % | -2.7 pts [-6.8, +2.0] |
| 15m | niveles | 56.1 % [54-58] n=3691 · +0.12R | 53.3 % [51-55] n=2176 · +0.07R | 55.7 % n=6012 | +2.8 pts [-3.6, +9.0] |
| 15m | control | 55.3 % n=7046 · +0.11R | 57.0 % n=6619 · +0.13R | 54.9 % | -1.7 pts [-5.5, +2.5] |

- Diferencia de diferencias (niveles menos control): 5m +2.0 pts [-3.5, +7.6], E[R] +0.04 [-0.07, +0.14];
  15m +4.5 pts [-1.6, +9.9], E[R] +0.07 [-0.04, +0.19]. Ninguna excluye el cero.
- Antes y después del 21 oct (fecha de la prueba original): 5m brecha -2.1 y +2.7 pts; 15m +2.4 y +3.4 pts.
  Todas dentro del ruido.
- Barajado de etiquetas: 5m p = 0.63; 15m p = 0.04 (pero el barajado no quita la tendencia; el control sí, y
  con él no pasa).
- En el control, "en contra" gana un poco MÁS que "a favor": en precios al azar, ir contra el veredicto no castiga.

## Por símbolo (15m, niveles)
NQ 55.5 % vs 51.9 % · ES 60.0 vs 57.7 · GC 60.5 vs 51.3 · YM 54.1 vs 56.1 · CL 49.3 vs 48.2. Solo GC
muestra una brecha clara (9 pts) y en su control casi no hay (58.8 vs 57.6). En 5m NQ da 55.3 vs 55.4: nada.

## Lo único que se separa: sesión de Nueva York
Juntando los 5 símbolos, toques en NY (09:30-17:00 ET):

| TF | niveles a favor | niveles en contra | control a favor | control en contra |
|---|---|---|---|---|
| 5m | 57.5 % n=954 · +0.14R | 51.4 % n=331 · +0.02R | 56.5 % · +0.13R | 61.1 % · +0.21R |
| 15m | 59.8 % n=945 · +0.19R | 43.0 % [38-48] n=379 · -0.14R | 54.6 % · +0.09R | 56.7 % · +0.13R |

En 15m sale en las dos mitades (antes del 21 oct 45 % n=267, después 37.5 % n=112) y el control no lo tiene. En Asia
y Londres "en contra" gana igual o más que "a favor". Pero es un corte buscado después de ver los datos (3 sesiones
× 2 TF, y 5m y 15m comparten casi los mismos toques): es una hipótesis, no una regla probada.

## Veredicto
- **"Evitar toques en contra" no se sostiene en general tras el fix.** La brecha de octubre (59 % vs 52 %) no se
  repite: 5m -0.7 pts, 15m +2.8 pts, y ninguna supera al control más allá del ruido. Las tres categorías rinden
  parecido (~55-58 %) y los niveles reales no rinden más que los desplazados.
- Ni el veredicto ni los niveles aportan ventaja medible por sí solos con estas reglas mecánicas. Coincide con lo
  medido en TDL Key Levels el 2026-11-11.
- Hipótesis a seguir en vivo: en la sesión de NY, un toque en contra del veredicto en un nivel real pierde
  (15m 43 %, -0.14R) y el control no. Para confirmarla: medir solo toques de NY desde hoy, sin cambiar reglas, hasta
  n ≥ 150 en contra.
- Práctica: el filtro "en contra" no hace daño, pero no es el edge. Fuera de NY no hay razón medida para saltar un
  toque solo por ir contra el veredicto.
