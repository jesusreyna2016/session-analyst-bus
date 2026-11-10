# mfp-zone-bot

Bot que opera las **zonas de Mi Mesa** en **MyFundedPerps** y mide dos cosas por separado:

1. **Las zonas**: ¿la zona funcionó en futuros? (registro de Mi Mesa, `?log=`)
2. **La ejecución en MFP**: ¿se llenó?, ¿a qué precio?, ¿la diferencia perp−futuro estuvo bien?, comisiones y swap.

Por defecto apunta al **sandbox** ($100K simulados). Para una cuenta real hay que cambiar `MFP_API_BASE` y poner `ALLOW_LIVE=1` a propósito.

## Qué hace

Cada 15 s:

1. Lee el plan intradía cada minuto con `?fresh=1` (`tradedadlog.com/api/intraday-plan?fresh=1`): recalculado al momento
   con la última vela de 5m y el estado en vivo del indicador de TradingView, en vez de esperar la corrida de 15 min.
   NQ, ES, GC, ETH, BTC. `ZONES_FRESH=0` vuelve al plan guardado.
2. Con cada vela nueva de 5m toma una muestra de la **diferencia perp − futuro**: el cierre de 5m del futuro
   contra el minuto de MFP que cierra en el mismo instante. Usa la mediana de las últimas 8 muestras; la estabilidad se mide con la desviación robusta (MAD), así una muestra suelta mal alineada no frena las órdenes.
3. Lee la cuenta y aplica el **riesgo**:
   - $300 por trade (tamaño = 300 / (distancia al stop + comisión de ida y vuelta)).
   - Freno diario al 90% del DLL de $3,000 = **$2,700**. Al tocarlo cancela todo, cierra posiciones y no opera hasta el reinicio diario de MFP.
   - Freno de drawdown al 90% de $3,000 (piso propio en inicial − $2,700).
   - Nunca pone una orden si la pérdida del día + el riesgo de lo abierto + $300 pasa de ese freno.
   - Máximo 5 a la vez (posiciones + órdenes en espera) y 1 por mercado. Sin límite de entradas por día
     (`MAX_ENTRIES_PER_DAY=0`); se puede poner un tope después de la fase de pruebas.
4. Elige zonas **A+ y A**, en estado `nueva`, `activa`, `tocada` o `armada` (re-test: el precio tocó la zona, salió y
   la orden espera que vuelva), sin el precio adentro, que no hayan funcionado ni se hayan invalidado antes en el día, con TP1 ≥ 1R, a ≤ 6 ATR de 5m, con el feed fresco y el veredicto `OPERABLE`.
   **Racha de stops**: si un mercado toca stop loss **2 veces seguidas en la misma dirección en menos de 1 hora**, deja de
   tomar zonas en esa dirección en ese mercado durante **2 horas** (la otra dirección sigue). Las órdenes en espera de esa
   dirección se cancelan. Un TP en medio corta la racha. Se ajusta con `SL_STREAK`, `SL_STREAK_WINDOW_MIN`, `SL_BLOCK_MIN`
   y `SL_BLOCK_SCOPE` (`market` por mercado, `all` para todos los mercados juntos). En los trades del 9-nov habría evitado
   el tercer stop seguido en NQ short (−3.17R → −2.17R); con `all` habría bloqueado además un TP de BTC.

   **Filtros de dirección** (opcionales, `TREND_FILTERS`, por defecto vacío = se operan las zonas tal cual):
   - `cisd`: dirección del último CISD en 1m, 3m y 5m (`CISD_TFS`, `CISD_MODE=last|all`). Una orden puesta solo se cancela
     por un CISD contrario de 5m (`CISD_HOLD_TF`) posterior a ponerla.
   - `ema20_50`, `ema200`, `ema9_21`, `struct5`, `struct15` (último CHoCH/MSS, BOS, CISD o IFVG, `src/structure.mjs`) y
     `vwap` (TWAP de la sesión). Todos los de la lista tienen que estar a favor.

   Medido en el histórico de zonas (`node tools/trend-backtest.mjs`, A+/A, 21-ago a 6-nov, R en futuros sin comisiones;
   el histórico solo tiene velas de 5m):

   | | trades | R promedio |
   |---|---|---|
   | sin filtro | 1396 | −0.04 |
   | último CISD de 5m o 15m a favor | 592 | −0.04 (sep −0.22, oct–nov +0.03) |
   | solo EMA20/50 | 744 | +0.05 |
   | EMA20/50 + EMA200 + estructura 5m | 360 | +0.12 (sep +0.07, oct–nov +0.14) |
5. Pone una **orden limit en la entrada de la zona** trasladada a precio MFP, con **SL y TP1 incluidos** y expiración (GTD) de 30 min.
   La renueva antes de vencer y la cancela si la zona deja de ser elegible o sus precios cambian.
   Si el bot se cae, las órdenes vencen solas y las posiciones quedan con su SL y TP en MFP.
6. Registra todo en `DATA_DIR/<día UTC>.jsonl` y al cambiar de día escribe `report-<día>.md`.

Entrar con límite en la entrada es la variante que mejor salió en el histórico de las zonas
(`zones/report.md`: +0.03R todas las tocadas, +0.10R en grado A). El vivo es el que confirma.

## Correr

```bash
cp .env.example .env    # poner MFP_API_KEY (fp_test_...)
npm install
node --env-file=.env index.mjs check    # verifica cuenta, mercados, zonas y precios; no opera
node --env-file=.env index.mjs          # corre el bot
node --env-file=.env index.mjs report 2026-11-09            # reporte de un día
node --env-file=.env index.mjs report 2026-11-09 2026-11-15 # de un rango
```

`GET /health` y `GET /status` (puerto `PORT`) muestran el estado: riesgo, diferencia por símbolo, órdenes y posiciones.

### Docker

```bash
docker build -t mfp-zone-bot .
docker run -d --restart unless-stopped --env-file .env -v $PWD/data:/data -p 8080:8080 mfp-zone-bot
```

Necesita disco persistente para `DATA_DIR` (ahí vive `state.json`). Con `GH_TOKEN` además copia la bitácora y los reportes a
`session-analyst-bus/mfp/bot-data/` cada 10 min.

## Bitácora (eventos)

| evento | qué es |
|---|---|
| `basis_sample` | muestra de diferencia perp − futuro |
| `skip` | zona candidata que no se operó y por qué (solo cuando cambia el motivo) |
| `place` / `place_error` | orden puesta (zona en futuros, diferencia usada, precios MFP, tamaño, riesgo) o rechazo |
| `cancel` | orden cancelada y motivo |
| `entry_filled` | se llenó la entrada |
| `order_end` | la orden venció o fue rechazada al llenarse (p. ej. tope de exposición) |
| `sl_block` | racha de stops: dirección bloqueada (mercado, lado, hasta cuándo) |
| `cisd` | cambió la dirección del CISD de un mercado (con el último CISD de cada temporalidad) |
| `trade_closed` | resultado: PnL, comisiones, swap, R, deslizamiento en entrada y salida, minutos en posición |
| `halt` / `new_day` | freno de riesgo / reinicio diario |
