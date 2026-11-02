# Revision semanal cripto · domingo 2026-11-01 (CT)

Semana cripto lunes 00:00 UTC a lunes 00:00 UTC. El metodo diario (crypto-close +
crypto-ny) arranco apenas el 30-31 de octubre: esta es la PRIMERA revision semanal real,
con solo 2 dias de datos completos (sabado 31-oct y domingo 1-nov, 4 corridas en total).
Todos los numeros de abajo son de muestra chica; se leen como arranque, no como veredicto.

## Marcador

- **ETHUSDT**: zonas 5/8 funcionaron (62.5%), sesgo 2/2 acertado. Predicciones de texto
  (solo se generan en el close) 5/8 aciertos (62.5%).
- **BTCUSDT**: zonas 1/6 funcionaron (16.7%), sesgo 1/3 acertado (el fallo grande: 1-nov
  close predijo corto y BTC subio 453.7 pts con el interes abierto cayendo).
- **Close vs ny**: en las zonas TOCADAS, el close acerto 2/3 (66.7%) y el ny 4/4 (100%);
  el update de ny no empeoro ningun plan esta semana, en todo caso lo confirmo. n muy
  chico (3-4 por lado), no es un patron todavia.

## Fin de semana contra entre semana

No hay comparacion posible: las dos corridas con dato real caen en fin de semana (sabado
y domingo). El metodo diario entre semana (lunes a viernes) todavia no acumula un dia
completo calificado.

## Donde fallo

- **BTC fallo el sesgo 1 de 3 veces**, y la vez que fallo fue la mas cara (453.7 pts en
  contra, interes abierto cayendo mientras el precio subia: cerro de cortos, no dinero
  nuevo, la pista que el plan si nombro pero que no evito la perdida en el papel).
- **`funding=shorts-crowded` (fondeo de ETH con los cortos pagando) rinde 3/10 (30%,
  n ≥ 8)**: ya toca la regla dura de la seccion 4 (baja la conviccion un escalon). El
  contraste con `funding=neutral` (3/4, 75%, n chico) sugiere que el viento de cola de
  fin de semana medido en semanas pasadas (5/5) no se esta repitiendo en estos 2 dias; se
  aplico ya en el plan del lunes y se sigue vigilando.
- Las 2 mejores: continuacion con la tendencia (`liq_reclaim`/`sweep_pdl` LONG, 3/3
  tocadas funcionaron) y reversion en el maximo (`sweep_pdh`/`fade_pdh` SHORT, 3/4
  resueltas funcionaron); ninguna con n ≥ 8 todavia.

## Contexto fuera del grafico

El hackeo de Binance (6.3B) dominó toda la semana: paso de riesgo ALTO a recuperacion
(90% repuesto, reapertura de retiros) y volvio a escalar el domingo/lunes (retiros
3.64B a 5.8B, atribucion del FBI a Corea del Norte). No se le midio impacto directo en
precio en ninguna de las 2 jornadas calificadas; el funding y el interes abierto
(dinero nuevo en ETH, cierres en BTC) explicaron mas del movimiento que los titulares.

## Semana que entra

Lunes 2-nov: ISM Manufacturing PMI (impacto medio, EEUU). Martes 3-nov: elecciones
legislativas de EEUU (impacto alto, puede mover el sentimiento de riesgo general) y
RBA (AUD, no cripto). Miercoles: ISM Services + inventarios de crudo. Seguir el
hackeo de Binance: si los retiros netos se estabilizan o si aparece un nuevo titular de
"hack"/"liquidation", actualizar `cryptoContext.risk` en la corrida que corresponda.

## Propuestas de metodo

Sin propuestas, muestra corta (n < 8 en casi todos los cortes; el metodo diario lleva
solo 2 dias calificados). Unico punto a vigilar sin tocar nada todavia: `funding=
shorts-crowded` ya tiene n ≥ 8 y rinde 30%, justo bajo el umbral de 0.4 de la regla
dura; si en 1-2 semanas mas se mantiene bajo con n mayor, ahi si proponer bajar o
quitar la excepcion de +1 por apalancamiento de la seccion 1b.
