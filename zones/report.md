# Zonas de Mi Mesa · reporte del agente

Generado 2026-11-28T02:35:08Z · pesos `v1` · en prueba `s1`

20 dias · 5551 zonas · 567 armadas (448 resueltas, 119 abiertas) · 1599 trades de Mi Mesa.

`·` = muestra menor a 20: no sacar conclusiones. Acierto con intervalo 95% (Wilson). E[R] = R promedio por setup.

## Setups armados (gatillo de 5 min)

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| Todos | 448 | 66% (61%–70%) | 0.646 | 2.89 |
| Ultimos dias (desde 2026-11-14) | 314 | 66% (60%–71%) | 0.612 | 2.78 |
| Tocadas que NUNCA se armaron | 418 | 60% (56%–65%) | 0.465 | 2.17 |

### Por grado

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| A | 272 | 66% (60%–72%) | 0.622 | 2.84 |
| A+ | 46 | 61% (46%–74%) | 0.557 | 2.42 |
| B | 130 | 67% (58%–74%) | 0.728 | 3.2 |

### Por mercado

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| BTCUSDT | 94 | 65% (55%–74%) | 0.651 | 2.86 |
| ES | 96 | 62% (52%–72%) | 0.585 | 2.56 |
| ETHUSDT | 119 | 71% (62%–78%) | 0.706 | 3.4 |
| GC | 68 | 65% (53%–75%) | 0.623 | 2.77 |
| NQ | 71 | 65% (53%–75%) | 0.645 | 2.83 |

### Por lado

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| long | 142 | 58% (50%–66%) | 0.485 | 2.15 |
| short | 306 | 70% (64%–74%) | 0.721 | 3.37 |

### Por direccion

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| a favor | 266 | 70% (64%–75%) | 0.709 | 3.33 |
| contra | 25 | 76% (57%–88%) | 1.083 | 5.51 |
| neutral | 157 | 58% (50%–65%) | 0.471 | 2.12 |

### Por regimen

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| BEAR | 5 · | 80% (38%–96%) | 1.072 | 6.36 |
| CHOP | 6 · | 50% (19%–81%) | 0.215 | 1.43 |
| sin dato | 437 | 66% (61%–70%) | 0.647 | 2.9 |

### Por regimen grafico

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| sin dato | 448 | 66% (61%–70%) | 0.646 | 2.89 |

### Por sesion

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| asia | 167 | 65% (58%–72%) | 0.626 | 2.8 |
| london | 138 | 67% (59%–75%) | 0.685 | 3.1 |
| ny | 123 | 68% (59%–75%) | 0.69 | 3.12 |
| off | 20 | 50% (30%–70%) | 0.28 | 1.56 |

### Por grado x regimen

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| A · BEAR | 5 · | 80% (38%–96%) | 1.072 | 6.36 |
| A · CHOP | 4 · | 25% (5%–70%) | -0.495 | 0.34 |
| A · sin dato | 263 | 66% (61%–72%) | 0.631 | 2.89 |
| A+ · sin dato | 46 | 61% (46%–74%) | 0.557 | 2.42 |
| B · CHOP | 2 · | 100% (34%–100%) | 1.635 | 99.0 |
| B · sin dato | 128 | 66% (58%–74%) | 0.713 | 3.12 |

### Por grado x direccion

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| A · a favor | 194 | 72% (65%–78%) | 0.737 | 3.6 |
| A · neutral | 78 | 53% (42%–63%) | 0.337 | 1.71 |
| A+ · a favor | 46 | 61% (46%–74%) | 0.557 | 2.42 |
| B · a favor | 26 | 69% (50%–84%) | 0.765 | 3.49 |
| B · contra | 25 | 76% (57%–88%) | 1.083 | 5.51 |
| B · neutral | 79 | 63% (52%–73%) | 0.603 | 2.64 |

### Por grado x mercado

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| A · BTCUSDT | 55 | 66% (52%–77%) | 0.636 | 2.84 |
| A · ES | 47 | 66% (52%–78%) | 0.677 | 2.99 |
| A · ETHUSDT | 91 | 70% (60%–79%) | 0.654 | 3.2 |
| A · GC | 43 | 65% (50%–78%) | 0.63 | 2.81 |
| A · NQ | 36 | 58% (42%–73%) | 0.442 | 2.06 |
| A+ · BTCUSDT | 9 · | 56% (27%–81%) | 0.29 | 1.65 |
| A+ · ES | 11 · | 64% (35%–85%) | 0.55 | 2.51 |
| A+ · ETHUSDT | 9 · | 78% (45%–94%) | 1.041 | 5.69 |
| A+ · GC | 9 · | 44% (19%–73%) | 0.3 | 1.54 |
| A+ · NQ | 8 · | 62% (31%–86%) | 0.612 | 2.63 |
| B · BTCUSDT | 30 | 67% (49%–81%) | 0.787 | 3.36 |
| B · ES | 38 | 58% (42%–72%) | 0.482 | 2.14 |
| B · ETHUSDT | 19 · | 68% (46%–85%) | 0.795 | 3.52 |
| B · GC | 16 · | 75% (50%–90%) | 0.788 | 4.15 |
| B · NQ | 27 | 74% (55%–87%) | 0.924 | 4.56 |

### Por chop

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| 50-61.8 | 151 | 66% (58%–73%) | 0.63 | 2.83 |
| <50 tendencia | 245 | 66% (60%–72%) | 0.661 | 2.95 |
| >=61.8 lateral | 52 | 65% (52%–77%) | 0.623 | 2.8 |

### Por estirado (ATR del VWAP)

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| 1-2 | 102 | 64% (54%–72%) | 0.524 | 2.44 |
| <1 | 109 | 65% (56%–73%) | 0.593 | 2.7 |
| >=2 | 237 | 67% (61%–73%) | 0.723 | 3.2 |

### Por R hasta TP1

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| 1.5-2.5R | 171 | 60% (53%–67%) | 0.686 | 2.72 |
| <1.5R | 244 | 70% (64%–76%) | 0.525 | 2.78 |
| >=2.5R | 33 | 61% (44%–75%) | 1.34 | 4.4 |

### Por distancia al crearse (ATR)

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| 2-6 | 6 · | 83% (44%–97%) | 0.953 | 6.72 |
| <2 | 441 | 66% (61%–70%) | 0.646 | 2.89 |
| >=6 | 1 · | 0% (0%–79%) | -1.0 | – |

## Confluencias: acierto con y sin cada nivel

| nivel | n con | acierto con | acierto sin | diferencia |
|---|---|---|---|---|
| loH | 76 | 75% | 64% | +11 pts |
| sh5 | 150 | 73% | 62% | +10 pts |
| ibh | 38 | 74% | 65% | +9 pts |
| pdMid | 37 | 73% | 65% | +8 pts |
| val | 62 | 73% | 65% | +8 pts |
| f15m | 250 | 69% | 62% | +7 pts |
| vah | 39 | 72% | 65% | +6 pts |
| ema50h | 45 | 71% | 65% | +6 pts |
| dvah | 102 | 70% | 65% | +5 pts |
| vwapUp | 105 | 70% | 65% | +5 pts |
| vwap | 105 | 69% | 65% | +4 pts |
| f5m | 305 | 67% | 64% | +3 pts |
| onh | 69 | 68% | 65% | +3 pts |
| pdl | 41 | 68% | 66% | +3 pts |
| pdc | 74 | 68% | 66% | +2 pts |
| do | 63 | 67% | 66% | +1 pts |
| onl | 51 | 67% | 66% | +1 pts |
| pml | 15 | 67% | 66% | +1 pts |
| sh1h | 39 | 67% | 66% | +1 pts |
| asL | 47 | 66% | 66% | +0 pts |
| ibl | 49 | 65% | 66% | -1 pts |
| mOpen | 11 | 64% | 66% | -2 pts |
| dpoc | 139 | 64% | 67% | -3 pts |
| f1h | 128 | 63% | 67% | -4 pts |
| wo | 32 | 62% | 66% | -4 pts |
| tdo | 93 | 62% | 67% | -4 pts |
| poc | 60 | 62% | 66% | -5 pts |
| asH | 73 | 62% | 67% | -5 pts |
| dval | 74 | 61% | 67% | -6 pts |
| gz | 20 | 60% | 66% | -6 pts |
| loL | 71 | 61% | 67% | -6 pts |
| vwapDn | 94 | 61% | 67% | -7 pts |
| sl4h | 24 | 58% | 66% | -8 pts |
| sl5 | 75 | 59% | 67% | -9 pts |
| pwl | 26 | 58% | 66% | -9 pts |
| f4h | 57 | 58% | 67% | -9 pts |
| ema200 | 76 | 57% | 68% | -11 pts |
| sl1h | 43 | 54% | 67% | -14 pts |
| pdh | 39 | 46% | 68% | -22 pts |
| sh4h | 21 | 33% | 67% | -34 pts |

## Excursion

Perdedoras: se movieron a favor 0.95R en promedio; 62 de 153 llegaron a +1R antes del stop. Ganadoras: en contra 0.27R en promedio (n 295).

## Pesos activos vs en prueba (politica: tomar desde la calificacion)

| desde | activos n | activos acierto | activos E[R] | prueba n | prueba acierto | prueba E[R] |
|---|---|---|---|---|---|---|
| A+ | 46 | 61% | 0.557 | 56 | 62% | 0.621 |
| A | 318 | 65% | 0.613 | 317 | 65% | 0.607 |
| B | 448 | 66% | 0.646 | 448 | 66% | 0.646 |

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

Las zonas del vivo repasadas sobre las velas de 5 min del bus (814 tocadas y resueltas medidas, sin medir: sin velas en el bus 52). Limite en la entrada de la zona, puesta desde la vela del toque hasta la que resuelve la zona; sale en TP1 o al cierre que invalida (regla `rl` del historico). 'atraviesa' = el precio paso mas alla de la entrada; 'toca' = llego a ella. 'bracket' = stop y TP1 como ordenes reales (mecha al stop = -1R, stop y TP1 en la misma vela = stop). '+ BE a +1R' = el mismo bracket con el stop a la entrada en cuanto el precio toca +1R (desde la vela siguiente al llenado). 'parcial 1/2 en +1R + BE' = el plan de salida de Jesus (trader-profile.exitPlan): cobra la mitad en +1R si llega antes que TP1 y el resto va a BE hasta TP1. Llenado = de las zonas elegibles, en cuantas se lleno la orden; acierto y E[R] solo de las llenadas.

| | elegibles | llenado | n | acierto | E[R] | PF |
|---|---|---|---|---|---|---|
| limite, armadas (atraviesa) | 423 | 71% | 302 | 54% (48%–59%) | 0.051 | 1.07 |
| limite, armadas (toca, regla del historico) | 423 | 72% | 304 | 54% (48%–60%) | 0.059 | 1.08 |
| limite, armadas, bracket stop/TP1 | 423 | 71% | 302 | 50% (44%–56%) | 0.225 | 1.46 |
| limite, armadas, bracket + BE a +1R | 423 | 71% | 302 | 46% (40%–52%) | 0.237 | 1.6 |
| limite, armadas, parcial 1/2 en +1R + BE | 423 | 71% | 302 | 59% (54%–65%) | 0.231 | 1.59 |
| limite, todas las tocadas (atraviesa) | 814 | 73% | 593 | 51% (47%–55%) | 0.012 | 1.02 |
| gatillo (cierre de la vela de 5 min) | 423 | 99% | 418 | 60% (56%–65%) | -0.155 | 0.68 |

| grado | elegibles | limite llenado | limite n | limite acierto (IC 95%) | limite E[R] | bracket E[R] | gatillo n | gatillo E[R] | historico limite E[R] (armadas) |
|---|---|---|---|---|---|---|---|---|---|
| A+ | 44 | 75% | 33 | 48% (32%–65%) | 0.001 | 0.134 | 44 | -0.207 | 0.169 (n 390) |
| A | 262 | 68% | 179 | 52% (45%–60%) | -0.012 | 0.2 | 257 | -0.146 | 0.289 (n 1356) |
| B | 117 | 77% | 90 | 58% (48%–68%) | 0.194 | 0.307 | 117 | -0.153 | 0.2 (n 824) |

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

### Historico por regimen grafico

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
