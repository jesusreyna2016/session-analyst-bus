# Zonas de Mi Mesa · reporte del agente

Generado 2026-11-26T02:33:48Z · pesos `v1` · en prueba `s1`

18 dias · 5088 zonas · 506 armadas (394 resueltas, 112 abiertas) · 1599 trades de Mi Mesa.

`·` = muestra menor a 20: no sacar conclusiones. Acierto con intervalo 95% (Wilson). E[R] = R promedio por setup.

## Setups armados (gatillo de 5 min)

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| Todos | 394 | 68% (63%–72%) | 0.7 | 3.17 |
| Ultimos dias (desde 2026-11-12) | 307 | 70% (65%–75%) | 0.739 | 3.49 |
| Tocadas que NUNCA se armaron | 358 | 61% (56%–66%) | 0.489 | 2.26 |

### Por grado

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| A | 241 | 69% (63%–74%) | 0.684 | 3.2 |
| A+ | 42 | 62% (47%–75%) | 0.584 | 2.53 |
| B | 111 | 68% (58%–76%) | 0.778 | 3.4 |

### Por mercado

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| BTCUSDT | 83 | 65% (54%–74%) | 0.655 | 2.87 |
| ES | 87 | 64% (54%–74%) | 0.637 | 2.79 |
| ETHUSDT | 105 | 74% (65%–82%) | 0.807 | 4.14 |
| GC | 58 | 69% (56%–79%) | 0.74 | 3.38 |
| NQ | 61 | 64% (51%–75%) | 0.63 | 2.75 |

### Por lado

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| long | 111 | 59% (49%–67%) | 0.537 | 2.3 |
| short | 283 | 71% (66%–76%) | 0.764 | 3.67 |

### Por direccion

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| a favor | 255 | 71% (65%–76%) | 0.73 | 3.48 |
| contra | 25 | 76% (57%–88%) | 1.083 | 5.51 |
| neutral | 114 | 60% (50%–68%) | 0.549 | 2.36 |

### Por regimen

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| BEAR | 5 · | 80% (38%–96%) | 1.072 | 6.36 |
| CHOP | 6 · | 50% (19%–81%) | 0.215 | 1.43 |
| sin dato | 383 | 68% (63%–72%) | 0.703 | 3.19 |

### Por sesion

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| asia | 147 | 68% (60%–75%) | 0.705 | 3.2 |
| london | 116 | 69% (60%–77%) | 0.73 | 3.35 |
| ny | 112 | 69% (60%–77%) | 0.722 | 3.31 |
| off | 19 · | 53% (32%–73%) | 0.348 | 1.73 |

### Por grado x regimen

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| A · BEAR | 5 · | 80% (38%–96%) | 1.072 | 6.36 |
| A · CHOP | 4 · | 25% (5%–70%) | -0.495 | 0.34 |
| A · sin dato | 232 | 69% (63%–75%) | 0.696 | 3.27 |
| A+ · sin dato | 42 | 62% (47%–75%) | 0.584 | 2.53 |
| B · CHOP | 2 · | 100% (34%–100%) | 1.635 | 99.0 |
| B · sin dato | 109 | 67% (58%–75%) | 0.763 | 3.31 |

### Por grado x direccion

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| A · a favor | 188 | 73% (66%–79%) | 0.76 | 3.8 |
| A · neutral | 53 | 55% (42%–67%) | 0.413 | 1.91 |
| A+ · a favor | 42 | 62% (47%–75%) | 0.584 | 2.53 |
| B · a favor | 25 | 68% (48%–83%) | 0.747 | 3.33 |
| B · contra | 25 | 76% (57%–88%) | 1.083 | 5.51 |
| B · neutral | 61 | 64% (51%–75%) | 0.667 | 2.85 |

### Por grado x mercado

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| A · BTCUSDT | 48 | 67% (52%–78%) | 0.642 | 2.93 |
| A · ES | 44 | 68% (53%–80%) | 0.725 | 3.28 |
| A · ETHUSDT | 80 | 74% (63%–82%) | 0.743 | 3.83 |
| A · GC | 36 | 69% (53%–82%) | 0.739 | 3.42 |
| A · NQ | 33 | 61% (44%–75%) | 0.487 | 2.24 |
| A+ · BTCUSDT | 9 · | 56% (27%–81%) | 0.29 | 1.65 |
| A+ · ES | 11 · | 64% (35%–85%) | 0.55 | 2.51 |
| A+ · ETHUSDT | 8 · | 88% (53%–98%) | 1.296 | 11.37 |
| A+ · GC | 9 · | 44% (19%–73%) | 0.3 | 1.54 |
| A+ · NQ | 5 · | 60% (23%–88%) | 0.56 | 2.4 |
| B · BTCUSDT | 26 | 65% (46%–81%) | 0.804 | 3.32 |
| B · ES | 32 | 59% (42%–74%) | 0.547 | 2.35 |
| B · ETHUSDT | 17 · | 71% (47%–87%) | 0.875 | 3.98 |
| B · GC | 13 · | 85% (58%–96%) | 1.045 | 7.79 |
| B · NQ | 23 | 70% (49%–84%) | 0.85 | 3.79 |

### Por chop

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| 50-61.8 | 138 | 68% (60%–75%) | 0.702 | 3.2 |
| <50 tendencia | 211 | 67% (60%–73%) | 0.681 | 3.05 |
| >=61.8 lateral | 45 | 71% (57%–82%) | 0.783 | 3.71 |

### Por estirado (ATR del VWAP)

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| 1-2 | 85 | 66% (55%–75%) | 0.59 | 2.73 |
| <1 | 99 | 67% (57%–75%) | 0.625 | 2.88 |
| >=2 | 210 | 69% (62%–75%) | 0.78 | 3.52 |

### Por R hasta TP1

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| 1.5-2.5R | 149 | 62% (54%–70%) | 0.739 | 2.96 |
| <1.5R | 213 | 72% (66%–78%) | 0.566 | 3.04 |
| >=2.5R | 32 | 62% (45%–77%) | 1.413 | 4.77 |

### Por distancia al crearse (ATR)

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| 2-6 | 6 · | 83% (44%–97%) | 0.953 | 6.72 |
| <2 | 387 | 68% (63%–72%) | 0.7 | 3.17 |
| >=6 | 1 · | 0% (0%–79%) | -1.0 | – |

## Confluencias: acierto con y sin cada nivel

| nivel | n con | acierto con | acierto sin | diferencia |
|---|---|---|---|---|
| sh5 | 138 | 76% | 63% | +13 pts |
| loH | 71 | 75% | 66% | +8 pts |
| ibh | 36 | 75% | 67% | +8 pts |
| vah | 38 | 74% | 67% | +7 pts |
| vwapUp | 95 | 73% | 66% | +6 pts |
| dvah | 91 | 72% | 66% | +6 pts |
| f15m | 214 | 71% | 64% | +6 pts |
| pdMid | 37 | 73% | 67% | +6 pts |
| onh | 62 | 73% | 67% | +6 pts |
| val | 62 | 73% | 67% | +6 pts |
| f5m | 269 | 70% | 64% | +6 pts |
| ema50h | 44 | 70% | 67% | +3 pts |
| vwap | 89 | 70% | 67% | +2 pts |
| sh1h | 31 | 68% | 68% | 0 pts |
| pdl | 40 | 68% | 68% | 0 pts |
| pml | 15 | 67% | 68% | -1 pts |
| pdc | 72 | 67% | 68% | -1 pts |
| asH | 65 | 66% | 68% | -2 pts |
| onl | 50 | 66% | 68% | -2 pts |
| f1h | 106 | 66% | 68% | -2 pts |
| tdo | 82 | 66% | 68% | -2 pts |
| do | 61 | 66% | 68% | -3 pts |
| asL | 46 | 65% | 68% | -3 pts |
| ibl | 46 | 65% | 68% | -3 pts |
| dpoc | 122 | 66% | 69% | -3 pts |
| loL | 62 | 64% | 68% | -4 pts |
| mOpen | 11 | 64% | 68% | -4 pts |
| wo | 30 | 63% | 68% | -5 pts |
| poc | 59 | 63% | 69% | -6 pts |
| sl5 | 64 | 62% | 69% | -6 pts |
| dval | 69 | 62% | 69% | -7 pts |
| vwapDn | 89 | 62% | 70% | -8 pts |
| ema200 | 68 | 60% | 69% | -9 pts |
| gz | 19 | 58% | 68% | -10 pts |
| pwl | 26 | 58% | 68% | -11 pts |
| f4h | 45 | 58% | 69% | -11 pts |
| sl4h | 23 | 56% | 68% | -12 pts |
| sl1h | 43 | 54% | 70% | -16 pts |
| pdh | 16 | 44% | 69% | -25 pts |
| sh4h | 11 | 27% | 69% | -42 pts |

## Excursion

Perdedoras: se movieron a favor 0.95R en promedio; 52 de 127 llegaron a +1R antes del stop. Ganadoras: en contra 0.26R en promedio (n 267).

## Pesos activos vs en prueba (politica: tomar desde la calificacion)

| desde | activos n | activos acierto | activos E[R] | prueba n | prueba acierto | prueba E[R] |
|---|---|---|---|---|---|---|
| A+ | 42 | 62% | 0.584 | 53 | 64% | 0.657 |
| A | 283 | 68% | 0.669 | 282 | 68% | 0.663 |
| B | 394 | 68% | 0.7 | 394 | 68% | 0.7 |

## Experimentos

- **z-2026-11-16-rrmin** (shadow): Las zonas con R a TP1 corto (<1.5R) friegan el E[R] aunque ganan casi igual de seguido que las de R medio (67% vs 68% en vivo, n 75/62): 1.5-2.5R deja +0.88R y <1.5R solo +0.45R. Subir rrMin filtra esos setups chicos antes de calificar. · veredicto: muestra corta

## Tus trades contra las zonas

| | n | acierto | E[R] | R total | PF |
|---|---|---|---|---|---|
| todos | 241 | 14% | -0.948 | -228.53 | 0.11 |
| en zona | 149 | 13% | -0.907 | -135.16 | 0.12 |
| fuera de zona | 92 | 14% | -1.015 | -93.37 | 0.1 |
| en zona con ficha | 0 | – | – | 0 | – |
| en zona sin ficha (por precio) | 118 | 12% | -0.88 | -103.86 | 0.1 |
| antes del gatillo | 2 | 0% | -1.14 | -2.28 | – |
| despues del gatillo | 11 | 0% | -0.976 | -10.74 | – |
| zona que nunca se armo | 136 | 15% | -0.898 | -122.14 | 0.13 |

| zona del trade | n | acierto | E[R] |
|---|---|---|---|
| A+ | 53 | 24% | -0.575 |
| A | 47 | 13% | -0.916 |
| B | 49 | 2% | -1.258 |

Ejecucion (67 trades con zona resuelta): la zona gano y tu perdiste 26 veces; la zona perdio y tu ganaste 2. Tu R menos el R de la zona, en promedio: -0.88.

## Vivo: entrada ejecutable (orden limite)

Las zonas del vivo repasadas sobre las velas de 5 min del bus (748 tocadas y resueltas medidas, sin medir: sin velas en el bus 4). Limite en la entrada de la zona, puesta desde la vela del toque hasta la que resuelve la zona; sale en TP1 o al cierre que invalida (regla `rl` del historico). 'atraviesa' = el precio paso mas alla de la entrada; 'toca' = llego a ella. 'bracket' = stop y TP1 como ordenes reales (mecha al stop = -1R, stop y TP1 en la misma vela = stop). '+ BE a +1R' = el mismo bracket con el stop a la entrada en cuanto el precio toca +1R (desde la vela siguiente al llenado). 'parcial 1/2 en +1R + BE' = el plan de salida de Jesus (trader-profile.exitPlan): cobra la mitad en +1R si llega antes que TP1 y el resto va a BE hasta TP1. Llenado = de las zonas elegibles, en cuantas se lleno la orden; acierto y E[R] solo de las llenadas.

| | elegibles | llenado | n | acierto | E[R] | PF |
|---|---|---|---|---|---|---|
| limite, armadas (atraviesa) | 392 | 70% | 275 | 55% (49%–61%) | 0.125 | 1.19 |
| limite, armadas (toca, regla del historico) | 392 | 71% | 277 | 56% (50%–61%) | 0.133 | 1.2 |
| limite, armadas, bracket stop/TP1 | 392 | 70% | 275 | 52% (46%–58%) | 0.279 | 1.6 |
| limite, armadas, bracket + BE a +1R | 392 | 70% | 275 | 48% (42%–54%) | 0.287 | 1.76 |
| limite, armadas, parcial 1/2 en +1R + BE | 392 | 70% | 275 | 62% (56%–67%) | 0.276 | 1.74 |
| limite, todas las tocadas (atraviesa) | 748 | 72% | 537 | 52% (48%–56%) | 0.052 | 1.08 |
| gatillo (cierre de la vela de 5 min) | 392 | 99% | 387 | 62% (57%–67%) | -0.11 | 0.75 |

| grado | elegibles | limite llenado | limite n | limite acierto (IC 95%) | limite E[R] | bracket E[R] | gatillo n | gatillo E[R] | historico limite E[R] (armadas) |
|---|---|---|---|---|---|---|---|---|---|
| A+ | 42 | 74% | 31 | 52% (35%–68%) | 0.192 | 0.207 | 42 | -0.131 | 0.169 (n 390) |
| A | 240 | 67% | 160 | 54% (47%–62%) | 0.045 | 0.258 | 235 | -0.114 | 0.289 (n 1356) |
| B | 110 | 76% | 84 | 58% (48%–68%) | 0.252 | 0.344 | 110 | -0.095 | 0.2 (n 824) |

## Historico (backtest)

El mismo motor sobre las velas de 5 min del bus, 2026-09-10 a 2026-11-22 (73 dias): 5285 zonas tocadas, 3149 armadas, 2973 resueltas. TWAP y perfil por tiempo (sin volumen), sin regimen ni VIX, grafico de 5 min con velas cerradas.
E[R] **real**: entrando al cierre de la vela del gatillo y saliendo en TP1 o al cierre que invalida. Sirve para proponer experimentos; el vivo es el que confirma.

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| Todos (R real) | 2973 | 63% (62%–65%) | -0.124 | 0.74 |
| Todos (R teorico, entrada de la zona) | 2973 | 63% (62%–65%) | 0.597 | 2.63 |
| Tocadas que NUNCA se armaron | 2040 | 50% (48%–52%) | 0.224 | 1.45 |

### Historico: como entrar (R real)

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| gatillo (cierre de la vela de 5 min) | 2973 | 61% (59%–63%) | -0.124 | 0.74 |
| limite en la entrada, todas las tocadas | 4319 | 51% (50%–52%) | 0.042 | 1.06 |
| limite en la entrada, solo las que se armaron | 2570 | 57% (56%–59%) | 0.242 | 1.4 |
| limite en la entrada, las que NUNCA se armaron | 1749 | 41% (39%–44%) | -0.252 | 0.71 |
| gatillo y luego limite si regresa a la entrada | 1933 | 44% (41%–46%) | -0.172 | 0.78 |

Gatillo + regreso a la entrada: el precio volvio a la entrada en 65% de las 2973 armadas (las demas se pierden: no hay trade).

| grado | gatillo n | gatillo E[R] | limite n | limite acierto | limite E[R] |
|---|---|---|---|---|---|
| A+ | 458 | -0.14 | 615 | 46% | -0.062 |
| A | 1542 | -0.076 | 2178 | 53% | 0.087 |
| B | 973 | -0.191 | 1526 | 50% | 0.019 |

### Historico por grado

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| A | 1542 | 64% (62%–67%) | -0.076 | 0.83 |
| A+ | 458 | 61% (57%–66%) | -0.14 | 0.71 |
| B | 973 | 62% (59%–66%) | -0.191 | 0.62 |

### Historico por mercado

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| BTCUSDT | 614 | 60% (56%–64%) | -0.158 | 0.69 |
| ES | 580 | 64% (60%–68%) | -0.137 | 0.71 |
| ETHUSDT | 660 | 62% (58%–65%) | -0.138 | 0.72 |
| GC | 573 | 64% (60%–68%) | -0.122 | 0.74 |
| NQ | 546 | 66% (62%–70%) | -0.058 | 0.87 |

### Historico por lado

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| long | 1393 | 60% (57%–62%) | -0.17 | 0.67 |
| short | 1580 | 66% (64%–69%) | -0.083 | 0.81 |

### Historico por direccion

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| a favor | 1739 | 63% (60%–65%) | -0.111 | 0.77 |
| contra | 251 | 67% (61%–73%) | -0.146 | 0.64 |
| neutral | 983 | 63% (60%–66%) | -0.14 | 0.71 |

### Historico por regimen

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| sin dato | 2973 | 63% (62%–65%) | -0.124 | 0.74 |

### Historico por sesion

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| asia | 1147 | 63% (60%–65%) | -0.139 | 0.71 |
| london | 790 | 66% (62%–69%) | -0.095 | 0.79 |
| ny | 916 | 62% (59%–66%) | -0.12 | 0.74 |
| off | 120 | 61% (52%–69%) | -0.194 | 0.67 |

### Historico por grado x regimen

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| A · sin dato | 1542 | 64% (62%–67%) | -0.076 | 0.83 |
| A+ · sin dato | 458 | 61% (57%–66%) | -0.14 | 0.71 |
| B · sin dato | 973 | 62% (59%–66%) | -0.191 | 0.62 |

### Historico por grado x direccion

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| A · a favor | 1073 | 64% (61%–67%) | -0.082 | 0.82 |
| A · contra | 2 · | 100% (34%–100%) | 0.215 | 99.0 |
| A · neutral | 467 | 66% (61%–70%) | -0.065 | 0.85 |
| A+ · a favor | 457 | 61% (57%–66%) | -0.137 | 0.72 |
| A+ · neutral | 1 · | 0% (0%–79%) | -1.35 | – |
| B · a favor | 209 | 60% (54%–67%) | -0.204 | 0.63 |
| B · contra | 249 | 67% (61%–73%) | -0.149 | 0.63 |
| B · neutral | 515 | 61% (57%–65%) | -0.207 | 0.61 |

### Historico por grado x mercado

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| A · BTCUSDT | 343 | 60% (55%–65%) | -0.124 | 0.75 |
| A · ES | 275 | 64% (58%–69%) | -0.133 | 0.72 |
| A · ETHUSDT | 360 | 64% (59%–69%) | -0.055 | 0.88 |
| A · GC | 287 | 68% (63%–73%) | -0.03 | 0.93 |
| A · NQ | 277 | 66% (61%–72%) | -0.038 | 0.91 |
| A+ · BTCUSDT | 76 | 62% (51%–72%) | -0.098 | 0.8 |
| A+ · ES | 93 | 62% (52%–72%) | -0.169 | 0.63 |
| A+ · ETHUSDT | 78 | 46% (36%–57%) | -0.413 | 0.39 |
| A+ · GC | 105 | 62% (52%–71%) | -0.111 | 0.76 |
| A+ · NQ | 106 | 70% (60%–78%) | 0.027 | 1.07 |
| B · BTCUSDT | 195 | 60% (53%–67%) | -0.239 | 0.57 |
| B · ES | 212 | 66% (59%–72%) | -0.127 | 0.73 |
| B · ETHUSDT | 222 | 63% (56%–69%) | -0.176 | 0.65 |
| B · GC | 181 | 59% (52%–66%) | -0.273 | 0.48 |
| B · NQ | 163 | 64% (56%–71%) | -0.147 | 0.67 |

### Historico por chop

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| 50-61.8 | 1005 | 61% (58%–64%) | -0.174 | 0.65 |
| <50 tendencia | 1729 | 64% (62%–66%) | -0.112 | 0.76 |
| >=61.8 lateral | 239 | 70% (64%–75%) | -0.003 | 0.99 |

### Historico por estirado (ATR del VWAP)

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| 1-2 | 553 | 62% (57%–66%) | -0.194 | 0.61 |
| <1 | 774 | 63% (60%–66%) | -0.122 | 0.74 |
| >=2 | 1646 | 64% (62%–66%) | -0.101 | 0.78 |

### Historico por R hasta TP1

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| 1.5-2.5R | 1101 | 62% (59%–64%) | -0.116 | 0.77 |
| <1.5R | 1641 | 65% (63%–67%) | -0.129 | 0.71 |
| >=2.5R | 231 | 59% (52%–65%) | -0.123 | 0.78 |

### Historico por distancia al crearse (ATR)

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| 2-6 | 47 | 62% (47%–74%) | -0.243 | 0.51 |
| <2 | 2913 | 63% (62%–65%) | -0.123 | 0.74 |
| >=6 | 13 · | 77% (50%–92%) | 0.049 | 1.15 |

### Historico: confluencias

| nivel | n con | acierto con | acierto sin | diferencia |
|---|---|---|---|---|
| loH | 442 | 70% | 62% | +8 pts |
| pwh | 44 | 70% | 63% | +7 pts |
| pwl | 162 | 70% | 63% | +7 pts |
| ibh | 354 | 68% | 63% | +6 pts |
| vah | 263 | 68% | 63% | +5 pts |
| dvah | 664 | 66% | 62% | +4 pts |
| ibl | 407 | 66% | 63% | +4 pts |
| ema200 | 564 | 66% | 63% | +3 pts |
| pdMid | 297 | 66% | 63% | +3 pts |
| f15m | 1572 | 64% | 62% | +2 pts |
| onh | 480 | 65% | 63% | +2 pts |
| pmh | 32 | 66% | 63% | +2 pts |
| sl1h | 279 | 65% | 63% | +2 pts |
| pml | 94 | 65% | 63% | +2 pts |
| mOpen | 113 | 65% | 63% | +1 pts |
| poc | 328 | 64% | 63% | +1 pts |
| vwapUp | 700 | 64% | 63% | +1 pts |
| onl | 488 | 64% | 63% | +1 pts |
| val | 340 | 64% | 63% | +1 pts |
| f1h | 856 | 64% | 63% | +1 pts |
| pdh | 261 | 64% | 63% | +1 pts |
| asH | 503 | 63% | 63% | +0 pts |
| loL | 429 | 63% | 63% | +0 pts |
| f4h | 448 | 63% | 63% | 0 pts |
| sh4h | 155 | 63% | 63% | 0 pts |
| vwap | 727 | 63% | 63% | 0 pts |
| dval | 700 | 63% | 63% | 0 pts |
| pdc | 599 | 63% | 63% | 0 pts |
| sh1h | 293 | 63% | 63% | -1 pts |
| asL | 491 | 63% | 63% | -1 pts |
| do | 589 | 63% | 64% | -1 pts |
| wo | 184 | 62% | 63% | -1 pts |
| sh5 | 813 | 62% | 64% | -2 pts |
| f5m | 2048 | 63% | 65% | -2 pts |
| ema50h | 390 | 62% | 64% | -2 pts |
| sl4h | 208 | 61% | 64% | -3 pts |
| pdl | 278 | 60% | 64% | -3 pts |
| vwapDn | 715 | 61% | 64% | -3 pts |
| sl5 | 777 | 60% | 65% | -5 pts |
| dpoc | 765 | 59% | 65% | -6 pts |
| gz | 200 | 57% | 64% | -7 pts |
| tdo | 488 | 63% | 63% | 0 pts |

Excursion historica: perdedoras a favor 1.0R en promedio, 487 de 1091 llegaron a +1R antes del stop; ganadoras en contra 0.26R (n 1882).
