# Revision semanal cripto · domingo 2026-11-08 (CT)

Semana cripto lunes 2026-11-02 00:00 UTC a lunes 2026-11-09 00:00 UTC, las 14 corridas
completas (7 dias x close+ny). Primera semana con el metodo diario corriendo los 7 dias
desde el principio, asi que ya hay muestra razonable por simbolo (aunque los cortes finos
siguen cortos).

## Marcador

- **ETHUSDT**: de 24 zonas propuestas, 10 se tocaron y 7 funcionaron (70% sobre tocadas).
  Predicciones de texto 6/14 (42.9%). Sesgo de sesion 5/10 acertado (50%).
- **BTCUSDT**: de 16 zonas propuestas, 7 se tocaron y 4 funcionaron (57.1% sobre tocadas).
  Predicciones de texto 8/14 (57.1%). Sesgo de sesion 4/7 acertado (57.1%, pero el fallo del
  jueves 06-nov en el ny y los dos fallos del fin de semana 07/08-nov fueron todos "sube en
  vez de bajar", el mismo patron repitiendose).
- **Close vs ny** (sobre zonas tocadas): el close acerto 7/11 (63.6%) y el ny 4/6 (66.7%);
  n todavia chico para llamarlo patron, pero el ny no viene empeorando los planes del close
  en ninguna semana medida hasta ahora.

## Fin de semana contra entre semana

Fin de semana (sab 07 + dom 08): 5 zonas tocadas de 12 propuestas, 4 funcionaron (80%, n muy
chico). Entre semana (lun-vie): 12 tocadas de 28 propuestas, 7 funcionaron (58.3%). La
liquidez fina de fin de semana sigue leyendose mejor que entre semana en esta muestra, pero
con solo 5 toques no es para apostarle todavia.

## Donde fallo

- Los priores acumulados que ya traia bajos siguen bajos y ahora con mas muestra: miedo
  (`fg=fear` 17/52 = 32.7%), sin titular de hackeo activo (antes `headline=hack` 16/51 =
  31.4%), sin iman del CME activo (`gap=none` 15/46 = 32.6%) y fondeo neutral (`funding=
  neutral` 12/32 = 37.5%). Los cuatro casi siempre aparecen juntos el mismo dia (no hay
  todavia un dia con uno solo activo para aislar el efecto de cada uno).
- **BTC sigue siendo el lado mas debil con mucho margen**: 5 de 22 zonas tocadas desde que
  se mide (22.7%), la tercera semana seguida bajo el 25%. Con `winN` ya en 22 (acercandose
  al umbral de 30 para un ajuste de `zonePriors`), si la semana que entra lo deja en 30+
  sin mejorar, toca proponer bajarle el prior de continuacion por separado del de ETH.
- Las 2 mejores de la semana (n chico, no para generalizar todavia): la barrida del minimo
  del dia anterior (`sweep_pdl`, 2 de 2 tocadas funcionaron) y el retest del nivel roto
  (`retest_break`, 3 de 4 tocadas funcionaron, el tipo con mas muestra de la semana).

## Contexto fuera del grafico

El hackeo de Binance de finales de octubre sigue de cola (renuncia del CFO, salida del jefe
de finanzas) pero sin escalar de nuevo esta semana: no se le midio impacto directo en precio.
Las salidas de ETF de bitcoin ($1.28B en la semana, la peor desde marzo) coincidieron con una
semana mixta (rally lunes-martes, reversion fuerte jueves-viernes tras las elecciones de
medio termino en EEUU): el fondeo y el interes abierto explicaron mas del movimiento dia a
dia que los titulares de ETF o de hackeo. El trasfondo geopolitico de Iran se mantuvo de
fondo toda la semana sin escalada real, con tono de distension hacia el domingo.

## Semana que entra

Martes 10-nov: CPI y Core CPI de EEUU (impacto alto, el dato mas relevante de la semana) y
Waller de la Fed habla. Jueves 12-nov: PIB del Reino Unido, Reclamos de Desempleo e
Inventarios de Crudo en EEUU. Viernes 13-nov: PPI y Core PPI de EEUU. Sin megacaps en el
calendario de ganancias. Seguir el fondeo de ETH (cortos cargados desde hoy, primera vez en
varias semanas) y el hueco del CME de ETH (-4.33% el viernes 06-nov, todavia sin llenar):
si se llena esta semana, anotar cuanto tardo desde que se activo.

## Propuestas de metodo

Sin propuestas firmes todavia: BTC acumula `winN`=22 con 22.7% de exito, ya bajo el 40% con
muestra de sobra para la regla dura de conviccion (que ya se aplica), pero falta llegar a
`winN`=30 para tocar su `zonePriors` de continuacion por separado del de ETH (que va mejor,
56% historico). Si las 2-3 semanas que vienen lo mantienen bajo 25% con `winN` >= 30, ahi si
proponer bajar el prior de continuacion de BTC de 0.40 a algo mas bajo, sin tocar el de ETH.
