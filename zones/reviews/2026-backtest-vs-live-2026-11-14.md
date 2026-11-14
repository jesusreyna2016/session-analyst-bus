# Historico vs vivo · zonas de Mi Mesa · 2026-11-14

Fuentes: `zones/report.md` (corrida del 2026-11-14 03:45 UTC, pesos `v1`), `zones/backtest/summary.json`
(motor `mi_mesa_zonas.pine v3.5`, velas hasta 2026-11-13 en futuros y 2026-11-14 en crypto) y
`zones/backtest/live_vs_backtest.json` (generado por `zones/backtest/compare_live.py` con las funciones de
`analyze_zones.py`). Ningun numero de este documento sale de otro sitio.

## 1. El historico rehecho

| | corrida 2026-11-08 | corrida 2026-11-14 |
|---|---|---|
| ventana | 2026-09-10 a 2026-11-08 (59 dias) | 2026-09-10 a 2026-11-13 (64 dias) |
| armadas resueltas | 2452 | 2698 |
| acierto | 63% (61%-65%) | 63% (61%-65%) |
| E[R] teorico (entrada de la zona) | 0.585 | 0.585 |
| E[R] real (cierre de la vela del gatillo) | -0.13 | -0.131 |
| limite en la entrada, solo armadas | 0.234 (n 2116) | 0.23 (n 2333) |
| tocadas que nunca se armaron, acierto | 49% (n 1656) | 49% (n 1842) |

Con 246 setups mas el historico no se movio. Nota: los 6 dias del vivo (2026-11-08 a 11-13) estan tambien dentro
de la ventana del historico, que no es una muestra independiente al 100%.

## 2. Como se compara

El vivo (`analyze_zones.py`) mide el R **teorico**: gana `rr` si llega a TP1, pierde 1 si se invalida, con entrada
en la zona. Por eso la tabla compara contra el R teorico del historico, y anade aparte el R real (entrada al cierre
de la vela del gatillo). El acierto es el mismo en las dos definiciones.

Divergencia = el acierto del historico cae **fuera** del intervalo 95% (Wilson) del vivo. Es el criterio justo: el
vivo es la muestra chica. Se marca aparte (·) cuando solo el vivo cae fuera del intervalo, mucho mas estrecho, del
historico: eso con n 30-130 no basta para hablar de diferencia.

| segmento | vivo n | vivo acierto (IC 95%) | vivo E[R] | hist n | hist acierto (IC 95%) | hist E[R] teorico | hist E[R] real | diverge |
|---|---|---|---|---|---|---|---|---|
| todas las armadas | 133 | 67% (58%-74%) | 0.739 | 2698 | 63% (61%-65%) | 0.585 | -0.131 | · |
| A+ | 11 (poca muestra) | 73% (43%-90%) | 0.805 | 402 | 60% (55%-64%) | 0.506 | -0.17 | · |
| A | 72 | 68% (57%-78%) | 0.787 | 1389 | 64% (62%-67%) | 0.605 | -0.076 | · |
| B | 50 | 64% (50%-76%) | 0.657 | 907 | 62% (59%-66%) | 0.591 | -0.197 | no |
| VWAP < 1 ATR | 31 | 61% (44%-76%) | 0.573 | 712 | 63% (59%-66%) | 0.503 | -0.125 | no |
| VWAP 1-2 ATR | 30 | 57% (39%-73%) | 0.481 | 499 | 60% (56%-64%) | 0.468 | -0.218 | no |
| VWAP >= 2 ATR | 72 | 74% (62%-82%) | 0.918 | 1487 | 64% (61%-66%) | 0.664 | -0.105 | · |
| con FVG de 15m | 72 | 62% (51%-73%) | 0.563 | 1431 | 64% (61%-66%) | 0.554 | -0.115 | no |
| sin FVG de 15m | 61 | 72% (60%-82%) | 0.947 | 1267 | 62% (59%-65%) | 0.621 | -0.149 | · |
| tocadas que nunca se armaron | 142 | 64% (56%-72%) | 0.566 | 1842 | 49% (46%-51%) | 0.201 | (sin R real) | **SI** |
| NQ · A | 13 (poca muestra) | 62% (36%-82%) | 0.616 | 254 | 67% (61%-72%) | 0.647 | -0.016 | no |
| NQ · B | 13 (poca muestra) | 77% (50%-92%) | 0.969 | 152 | 63% (55%-70%) | 0.556 | -0.16 | · |

## 3. Lo que dice

1. **Una sola divergencia real: el gatillo.** En el historico, armarse separa mucho (63% armadas frente a 49% de
   tocadas sin gatillo; E[R] teorico 0.585 frente a 0.201). En el vivo casi no separa: 67% frente a 64%, E[R]
   0.739 frente a 0.566. El 49% del historico queda fuera del intervalo del vivo (56%-72%). O el vivo ha tenido
   6 dias faciles para las zonas sin gatillo, o el gatillo en vivo (ticks dentro de la vela) se comporta distinto
   del historico (velas de 5 min cerradas). Hay que seguirlo; con 142 casos todavia no se puede decir cual.
2. **El vivo va por encima del historico en todo, pero dentro del ruido.** Acierto 67% frente a 63%, E[R] teorico
   0.739 frente a 0.585. Lo mismo en A, A+, VWAP >= 2 ATR y sin FVG de 15m: el vivo queda por encima, pero el
   historico cae siempre dentro del intervalo del vivo. Lo esperable es que el vivo baje hacia el historico.
3. **La ventaja del vivo es teorica, no de ejecucion.** Todo el E[R] positivo supone entrar en la zona. En el
   historico, entrar al cierre de la vela del gatillo pierde en todos los grados y segmentos (de -0.016 en NQ · A a
   -0.218 en VWAP 1-2 ATR); la unica forma de entrar con E[R] positivo es la orden limite en la entrada de las que
   se arman (0.23, n 2333). El vivo no mide todavia la entrada real.
4. **VWAP >= 2 ATR**: el historico confirma la direccion (64% y 0.664 frente a 60% y 0.468 en 1-2 ATR), pero con
   una diferencia mucho menor que el vivo (74% frente a 57%). Hipotesis razonable, sin cambio de pesos aun.
5. **FVG de 15m**: en el vivo baja el acierto (62% frente a 72%); en el historico no (64% frente a 62%, al reves).
   El vivo con FVG de 15m (62%) cae dentro del historico; la diferencia viene del grupo sin FVG, que va alto.

## 4. Prueba de pesos en el historico

`BACKTEST_WEIGHTS='{"f15m":1}'` (1.5 a 1), comparado con los pesos activos, E[R] real:

| | activos | f15m 1 |
|---|---|---|
| todas | -0.131 (n 2698) | -0.133 (n 2627) |
| A | -0.076 (n 1389) | -0.08 (n 1330) |
| A+ | -0.17 (n 402) | -0.163 (n 374) |
| B | -0.197 (n 907) | -0.199 (n 923) |
| limite, solo armadas | 0.23 | 0.228 |

No mejora. Segun el metodo ("si en el historico empeora, no lo propongas") **no se propone**. El historico quedo
rehecho con los pesos activos.

## 5. Propuesta

Ningun cambio de pesos para sombra esta semana: ninguna diferencia del vivo sale del ruido salvo la del gatillo, y
esa no se traduce en un peso. Lo que si vale la pena seguir (sin tocar `weights.json`):

- Tocadas sin gatillo frente a armadas en el vivo: si con ~300 casos sigue la brecha de 3 puntos, el gatillo no
  aporta en vivo lo que aporta en el historico.
- VWAP >= 2 ATR: candidato a experimento cuando el vivo tenga 30+ casos en 1-2 ATR y la diferencia siga clara.
- Medir en el vivo el R de entrada real (gatillo y limite), igual que el historico, antes de fiarse del E[R]
  teorico.
