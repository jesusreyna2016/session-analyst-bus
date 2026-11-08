# Zonas de Mi Mesa · reporte del agente

Generado 2026-11-08T22:19:56Z · pesos `v1`

0 dias · 0 zonas · 0 armadas (0 resueltas, 0 abiertas) · 1159 trades de Mi Mesa.

`·` = muestra menor a 20: no sacar conclusiones. Acierto con intervalo 95% (Wilson). E[R] = R promedio por setup.

## Setups armados (gatillo de 5 min)

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| Todos | 0 | – | – | – |
| Ultimos dias (desde 2026-10-25) | 0 | – | – | – |
| Tocadas que NUNCA se armaron | 0 | – | – | – |

### Por grado

| | n | acierto | E[R] | PF |
|---|---|---|---|---|

### Por mercado

| | n | acierto | E[R] | PF |
|---|---|---|---|---|

### Por lado

| | n | acierto | E[R] | PF |
|---|---|---|---|---|

### Por direccion

| | n | acierto | E[R] | PF |
|---|---|---|---|---|

### Por regimen

| | n | acierto | E[R] | PF |
|---|---|---|---|---|

### Por sesion

| | n | acierto | E[R] | PF |
|---|---|---|---|---|

### Por grado x regimen

| | n | acierto | E[R] | PF |
|---|---|---|---|---|

### Por grado x direccion

| | n | acierto | E[R] | PF |
|---|---|---|---|---|

### Por grado x mercado

| | n | acierto | E[R] | PF |
|---|---|---|---|---|

### Por chop

| | n | acierto | E[R] | PF |
|---|---|---|---|---|

### Por estirado (ATR del VWAP)

| | n | acierto | E[R] | PF |
|---|---|---|---|---|

### Por R hasta TP1

| | n | acierto | E[R] | PF |
|---|---|---|---|---|

### Por distancia al crearse (ATR)

| | n | acierto | E[R] | PF |
|---|---|---|---|---|

## Confluencias: acierto con y sin cada nivel

| nivel | n con | acierto con | acierto sin | diferencia |
|---|---|---|---|---|

## Excursion

Perdedoras: se movieron a favor NoneR en promedio; 0 de 0 llegaron a +1R antes del stop. Ganadoras: en contra NoneR en promedio (n 0).

## Pesos activos vs en prueba (politica: tomar desde la calificacion)

| desde | activos n | activos acierto | activos E[R] | prueba n | prueba acierto | prueba E[R] |
|---|---|---|---|---|---|---|
| A+ | 0 | – | None | – | – | – |
| A | 0 | – | None | – | – | – |
| B | 0 | – | None | – | – | – |

## Experimentos

Ninguno todavia.

## Tus trades contra las zonas

| | n | acierto | E[R] | R total | PF |
|---|---|---|---|---|---|
| todos | 0 | – | – | 0 | – |
| en zona | 0 | – | – | 0 | – |
| fuera de zona | 0 | – | – | 0 | – |
| en zona con ficha | 0 | – | – | 0 | – |
| en zona sin ficha (por precio) | 0 | – | – | 0 | – |
| antes del gatillo | 0 | – | – | 0 | – |
| despues del gatillo | 0 | – | – | 0 | – |
| zona que nunca se armo | 0 | – | – | 0 | – |

| zona del trade | n | acierto | E[R] |
|---|---|---|---|
| A+ | 0 | – | – |
| A | 0 | – | – |
| B | 0 | – | – |

Ejecucion (0 trades con zona resuelta): la zona gano y tu perdiste 0 veces; la zona perdio y tu ganaste 0. Tu R menos el R de la zona, en promedio: None.

## Historico (backtest)

El mismo motor sobre las velas de 5 min del bus, 2026-09-10 a 2026-11-08 (59 dias): 4327 zonas tocadas, 2596 armadas, 2452 resueltas. TWAP y perfil por tiempo (sin volumen), sin regimen ni VIX, grafico de 5 min con velas cerradas.
E[R] **real**: entrando al cierre de la vela del gatillo y saliendo en TP1 o al cierre que invalida. Sirve para proponer experimentos; el vivo es el que confirma.

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| Todos (R real) | 2452 | 63% (61%–65%) | -0.13 | 0.73 |
| Todos (R teorico, entrada de la zona) | 2452 | 63% (61%–65%) | 0.585 | 2.58 |
| Tocadas que NUNCA se armaron | 1656 | 49% (46%–51%) | 0.199 | 1.39 |

### Historico: como entrar (R real)

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| gatillo (cierre de la vela de 5 min) | 2452 | 60% (58%–62%) | -0.13 | 0.73 |
| limite en la entrada, todas las tocadas | 3540 | 50% (49%–52%) | 0.031 | 1.04 |
| limite en la entrada, solo las que se armaron | 2116 | 57% (55%–59%) | 0.234 | 1.39 |
| limite en la entrada, las que NUNCA se armaron | 1424 | 40% (38%–43%) | -0.27 | 0.69 |
| gatillo y luego limite si regresa a la entrada | 1595 | 43% (40%–45%) | -0.183 | 0.77 |

Gatillo + regreso a la entrada: el precio volvio a la entrada en 65% de las 2452 armadas (las demas se pierden: no hay trade).

| grado | gatillo n | gatillo E[R] | limite n | limite acierto | limite E[R] |
|---|---|---|---|---|---|
| A+ | 363 | -0.175 | 493 | 44% | -0.111 |
| A | 1256 | -0.072 | 1756 | 52% | 0.097 |
| B | 833 | -0.198 | 1291 | 50% | -0.004 |

### Historico por grado

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| A | 1256 | 64% (62%–67%) | -0.072 | 0.84 |
| A+ | 363 | 60% (54%–64%) | -0.175 | 0.66 |
| B | 833 | 62% (59%–65%) | -0.198 | 0.61 |

### Historico por mercado

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| BTCUSDT | 508 | 58% (54%–62%) | -0.207 | 0.61 |
| ES | 478 | 66% (61%–70%) | -0.109 | 0.76 |
| ETHUSDT | 543 | 62% (57%–66%) | -0.141 | 0.72 |
| GC | 469 | 63% (58%–67%) | -0.149 | 0.68 |
| NQ | 454 | 67% (62%–71%) | -0.035 | 0.92 |

### Historico por lado

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| long | 1267 | 60% (57%–62%) | -0.169 | 0.67 |
| short | 1185 | 66% (64%–69%) | -0.089 | 0.79 |

### Historico por direccion

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| a favor | 1356 | 62% (59%–65%) | -0.122 | 0.75 |
| contra | 204 | 68% (62%–74%) | -0.133 | 0.66 |
| neutral | 892 | 63% (60%–66%) | -0.142 | 0.71 |

### Historico por regimen

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| sin dato | 2452 | 63% (61%–65%) | -0.13 | 0.73 |

### Historico por sesion

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| asia | 950 | 62% (59%–65%) | -0.16 | 0.67 |
| london | 644 | 65% (62%–69%) | -0.092 | 0.8 |
| ny | 761 | 63% (59%–66%) | -0.113 | 0.76 |
| off | 97 | 58% (48%–67%) | -0.232 | 0.61 |

### Historico por grado x regimen

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| A · sin dato | 1256 | 64% (62%–67%) | -0.072 | 0.84 |
| A+ · sin dato | 363 | 60% (54%–64%) | -0.175 | 0.66 |
| B · sin dato | 833 | 62% (59%–65%) | -0.198 | 0.61 |

### Historico por grado x direccion

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| A · a favor | 832 | 64% (60%–67%) | -0.081 | 0.82 |
| A · contra | 2 · | 100% (34%–100%) | 0.215 | 99.0 |
| A · neutral | 422 | 66% (62%–70%) | -0.056 | 0.87 |
| A+ · a favor | 362 | 60% (55%–65%) | -0.172 | 0.66 |
| A+ · neutral | 1 · | 0% (0%–79%) | -1.35 | – |
| B · a favor | 162 | 59% (52%–66%) | -0.224 | 0.6 |
| B · contra | 202 | 68% (61%–74%) | -0.136 | 0.66 |
| B · neutral | 469 | 60% (56%–65%) | -0.216 | 0.59 |

### Historico por grado x mercado

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| A · BTCUSDT | 276 | 58% (52%–64%) | -0.168 | 0.67 |
| A · ES | 227 | 65% (59%–71%) | -0.097 | 0.79 |
| A · ETHUSDT | 288 | 64% (58%–69%) | -0.049 | 0.89 |
| A · GC | 232 | 69% (63%–75%) | -0.035 | 0.91 |
| A · NQ | 233 | 68% (62%–74%) | -0.001 | 1.0 |
| A+ · BTCUSDT | 56 | 54% (41%–66%) | -0.313 | 0.49 |
| A+ · ES | 76 | 67% (56%–77%) | -0.097 | 0.76 |
| A+ · ETHUSDT | 61 | 44% (32%–57%) | -0.451 | 0.37 |
| A+ · GC | 82 | 56% (45%–66%) | -0.226 | 0.58 |
| A+ · NQ | 88 | 70% (60%–79%) | 0.086 | 1.23 |
| B · BTCUSDT | 176 | 60% (53%–67%) | -0.234 | 0.56 |
| B · ES | 175 | 66% (58%–72%) | -0.129 | 0.73 |
| B · ETHUSDT | 194 | 63% (56%–70%) | -0.181 | 0.64 |
| B · GC | 155 | 57% (50%–65%) | -0.279 | 0.48 |
| B · NQ | 133 | 62% (54%–70%) | -0.174 | 0.63 |

### Historico por chop

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| 50-61.8 | 824 | 60% (57%–63%) | -0.187 | 0.63 |
| <50 tendencia | 1444 | 64% (61%–66%) | -0.115 | 0.76 |
| >=61.8 lateral | 184 | 70% (63%–76%) | 0.001 | 1.0 |

### Historico por estirado (ATR del VWAP)

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| 1-2 | 443 | 60% (56%–65%) | -0.21 | 0.59 |
| <1 | 655 | 63% (59%–66%) | -0.125 | 0.73 |
| >=2 | 1354 | 64% (61%–66%) | -0.107 | 0.77 |

### Historico por R hasta TP1

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| 1.5-2.5R | 910 | 61% (58%–64%) | -0.133 | 0.74 |
| <1.5R | 1354 | 65% (62%–68%) | -0.13 | 0.7 |
| >=2.5R | 188 | 58% (51%–65%) | -0.119 | 0.78 |

### Historico por distancia al crearse (ATR)

| | n | acierto | E[R] | PF |
|---|---|---|---|---|
| 2-6 | 39 | 56% (41%–71%) | -0.361 | 0.36 |
| <2 | 2402 | 63% (61%–65%) | -0.127 | 0.73 |
| >=6 | 11 · | 73% (43%–90%) | -0.05 | 0.87 |

### Historico: confluencias

| nivel | n con | acierto con | acierto sin | diferencia |
|---|---|---|---|---|
| loH | 346 | 69% | 62% | +8 pts |
| pwh | 43 | 70% | 63% | +7 pts |
| ibh | 296 | 67% | 62% | +5 pts |
| ibl | 335 | 67% | 62% | +4 pts |
| pwl | 118 | 67% | 63% | +4 pts |
| vah | 212 | 66% | 63% | +3 pts |
| ema200 | 476 | 66% | 62% | +3 pts |
| dvah | 535 | 65% | 62% | +3 pts |
| sl1h | 227 | 66% | 63% | +3 pts |
| pmh | 32 | 66% | 63% | +3 pts |
| tdo | 396 | 65% | 62% | +3 pts |
| onl | 417 | 65% | 62% | +2 pts |
| val | 262 | 64% | 63% | +2 pts |
| f1h | 718 | 64% | 62% | +2 pts |
| pdMid | 235 | 64% | 63% | +2 pts |
| f15m | 1289 | 64% | 62% | +1 pts |
| loL | 353 | 64% | 63% | +1 pts |
| onh | 389 | 64% | 63% | +1 pts |
| mOpen | 104 | 64% | 63% | +1 pts |
| asL | 412 | 63% | 63% | +0 pts |
| sl4h | 163 | 63% | 63% | +0 pts |
| f4h | 376 | 63% | 63% | +0 pts |
| dval | 581 | 63% | 63% | 0 pts |
| sh4h | 135 | 62% | 63% | -1 pts |
| pdl | 222 | 62% | 63% | -1 pts |
| ema50h | 343 | 62% | 63% | -1 pts |
| poc | 277 | 62% | 63% | -1 pts |
| asH | 414 | 62% | 63% | -1 pts |
| vwapUp | 572 | 62% | 63% | -1 pts |
| pdc | 498 | 62% | 63% | -1 pts |
| sh1h | 255 | 62% | 63% | -1 pts |
| sh5 | 637 | 62% | 63% | -1 pts |
| f5m | 1685 | 62% | 64% | -2 pts |
| wo | 157 | 61% | 63% | -2 pts |
| vwap | 591 | 61% | 63% | -2 pts |
| do | 495 | 61% | 63% | -3 pts |
| vwapDn | 581 | 61% | 64% | -3 pts |
| pml | 64 | 59% | 63% | -4 pts |
| sl5 | 658 | 59% | 64% | -5 pts |
| dpoc | 621 | 59% | 64% | -6 pts |
| gz | 162 | 57% | 63% | -6 pts |
| pdh | 237 | 63% | 63% | 0 pts |

Excursion historica: perdedoras a favor 1.0R en promedio, 402 de 910 llegaron a +1R antes del stop; ganadoras en contra 0.26R (n 1542).
