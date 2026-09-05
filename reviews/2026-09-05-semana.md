# Meta-revision semanal · 2026-08-31 a 2026-09-04

Primera corrida `weekly` del bus (tracker de scorecard arranco el 2026-08-31),
asi que todas las ventanas de calibracion siguen cortas (n=3-11) y esta es la
primera semana con datos propios, sin semana anterior para comparar (▲/▼ no
aplica todavia). El viernes 09-04 solo tiene calificacion PARCIAL (Asia, via
pre-london): el cierre completo de Londres/NY de ese dia lo califica el
`pre-asia` del domingo 09-06, asi que el marcador de abajo se apoya en
lun-jue confirmados + el parcial de Asia del viernes.

## Marcador de la semana por instrumento

- **NQ**: acierto de sesgo 57% (4/7, ventana 09-01/02/03) · escenario A 22%
  (2/9) · predictionScore global 45% (21.5/48). Semana de dos giros de
  regimen (bajista -> alcista lunes, alcista -> chop miercoles, chop ->
  alcista naciente jueves), cerro el viernes con reclamo confirmado sobre
  PDH tras el susto de NFP.
- **ES**: sesgo 50% (2/4) · escenario A 11% (1/9, el mas debil del complejo)
  · predictionScore 42% (20.5/49). Rezago consistente frente a NQ toda la
  semana (rompio su marco crudo 1 sesion mas tarde cada vez que NQ giraba),
  rompio a alcista el jueves, viernes se quedo AVOID/estirado sin
  seguimiento limpio post-NFP.
- **GC**: sesgo 83% (5/6, el mejor del complejo) · escenario A 22% (2/9) ·
  predictionScore 45% (21/47). El instrumento con la tesis mas limpia:
  rechazo confirmado 3 veces seguidas en el mismo cluster VAH/EMA200 antes
  de romper a alcista el miercoles, confirmo 2a sesion el jueves, viernes
  ya agotado (116% del ATR) sin rechazo.
- **YM**: sesgo 100% (2/2) · escenario A 80% (4/5) · predictionScore 82%
  (18/22, el mejor del bus con diferencia). Lidero el alza del complejo 3
  sesiones seguidas (introducido 09-02) con divergencia SMT real vs
  NQ/ES, pero el viernes le devolvio todo el rally al NFP, primera vez que
  el liderazgo queda en duda.
- **CL**: sesgo 0% (0/2, peor del complejo aunque n muy bajo) ·
  escenario A 20% (1/5) · predictionScore 43% (9/21). Rango sigue siendo
  su punto debil sistematico (0/3 en range el jueves); termino la semana
  en tierra de nadie, a menos de 1pt de su invalidacion semanal (89.04),
  sin sesgo.
- **EM (estimado de movimiento)**: subestimado en el complejo casi toda la
  semana, marcado como causa de fallo en 4 de los 5 reviews diarios
  (08-31, 09-01, 09-02, y de nuevo en el parcial del 09-04); `emCalibration`
  trae sesgo "+" (realizado > predicho) consistente en NQ|asia, ES|asia,
  GC|asia y GC|londres (n=3 cada uno). No hay % exacto de sesiones dentro
  de banda porque el patron dominante fue "fuera por arriba", no mixto.

## Ejecucion de la semana (`live/journal.json`, byDay 08-31 a 09-04)

0 de 5 dias disciplinados. Contra-sesgo 47.5% (96/202, peor que el 39% de
la ventana rodante de 10 dias, ▼) · fuera-de-edge 46.7% (115/246, ~igual al
47% rodante). 3 de 5 dias con overtrade (09-01, 09-03, 09-04), 2 con revenge
(09-01, 09-04) y 2 con round-trip (09-01, 09-03). El viernes 09-04 (dia NFP)
fue el peor: overtrade+revenge juntos y la peor racha de perdidas de la
semana (23 seguidas), sin bias identificable en el digest pese a 27 trades
gradados. La disciplina de la semana empeora respecto a la tendencia de 10
dias; la fuga que manda es el contra-sesgo, no el churn puro.

## Que se repitio

`level_first` fue la categoria de prediccion mas debil 2-3 dias seguidos
(dias de blowoff sin pausas limpias entre niveles). GC y CL siguen siendo
los dos instrumentos peor calibrados en rango del complejo (dicho explicito
el 09-03). El patron de contra-sesgo + churn en la ejecucion real (overtrade/
revenge/round-trip) volvio a aparecer en la mayoria de los dias de mas
volumen (09-01, 09-03, 09-04), igual que en la semana de arranque del
tracker.

## Propuestas de metodo

1. **Subir el piso del multiplicador de EM en regimen de expansion.**
   Evidencia: sesgo "+" consistente (realizado > predicho) en
   `scorecard.emCalibration` para NQ|asia (n=3, +360tk), ES|asia (n=3,
   +46.8tk), GC|asia (n=3, +347tk) y GC|londres (n=3, +470tk), mas mencion
   explicita como causa de fallo en 4/5 reviews diarios de la semana. Aun
   bajo el umbral n≥5 del metodo para aplicar `mult` automatico (seccion
   6), pero la consistencia de direccion en 4 celdas distintas amerita
   vigilar 2-3 sesiones mas antes de tocar `scorecard.emCalibration` en
   `state/sa-state.json`.
2. **Revisar el criterio de seleccion del escenario A.** Evidencia:
   `scenarioAHitPct` corre muy bajo y parejo en NQ/ES/GC (22%/11%/22%,
   n=9 cada uno, justo bajo el umbral informal de n≥10 de la seccion 4).
   Tres instrumentos coincidiendo en el mismo rango bajo sugiere que el
   escenario A se esta armando como "el camino esperado" en vez del mas
   probable dado el regimen del dia. Tocaria la seccion 3 de
   `method/instructions.md` (como se elige el escenario primario). Con
   n=9 aun no cruza el umbral duro; vigilar la proxima semana antes de
   cambiar nada.

## Leccion de la semana

El proceso tecnico (contra-caso + esperar confirmacion antes de dar GO)
funciono en precio toda la semana incluso cuando el sesgo direccional
fallaba (NQ y ES giraron su tesis justo en los niveles que sus propios
contra-casos venian marcando), pero la ejecucion real de Jesus no siguio
ese mismo proceso: el contra-sesgo domino la mayoria de los dias y el
viernes post-NFP fue el peor de la semana en disciplina.

## Regimen: como entro y como sale cada instrumento

- **NQ**: entro en balance/chop de 3 dias, rompio a tendencia alcista
  naciente el jueves, sale con el reclamo confirmado del viernes ya en
  precio (2a sesion del nuevo regimen).
- **ES**: entro en CONFLICT de 4 dias contra su propio marco semanal,
  rompio a alcista el jueves (un dia despues que NQ, como ya se esperaba),
  sale con la confirmacion del viernes todavia sin calificar.
- **GC**: entro bajista, rompio a alcista el miercoles, confirmo 2a sesion
  el jueves, sale mostrando la primera senal real de agotamiento
  (estirado 3.29 ATR, dia al 116% del ATR el viernes).
- **YM**: entro y goberno 3 sesiones seguidas liderando el alza del
  complejo con la mejor precision del bus, sale con el liderazgo en duda
  por primera vez tras devolver todo el rally del viernes.
- **CL**: entra y sale la semana igual, en rango/chop con reacciones
  violentas al catalizador (EIA), terminando en tierra de nadie a menos de
  1pt de su invalidacion semanal.
