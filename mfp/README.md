# MFP · diferencia perp vs futuros

Las zonas de la mesa están en precio de **futuros CME** (CL, GC, ES, NQ, YM).
MFP opera **perps** que siguen otra referencia. Para poner una orden en MFP:

```
precio_MFP = precio_zona_futuro + diff
```

`diff = perp - futuro`, medido vela a vela (5m) en `basis.json`.

## Medición inicial (17-ago → 6-nov-2026)

| Futuro | Perp MFP | diff últimos 5 días (mediana · p10…p90) | Ruido intradía (sd) | Comportamiento |
|---|---|---|---|---|
| CL | `hyperliquid\|xyz:CL` | −0.02 · −0.18…+0.03 | 0.02 | Casi igual; se abre a −0.2/−0.3 cerca del roll |
| CL | `binance\|CLUSDT` | +0.08 · 0.00…+0.12 | 0.02 | Casi igual, **pero salta −1.5 a −4.6 en rolls** (sem. 37-38, 42) |
| GC | `binance\|XAUUSDT` | −1.8 · −3.5…−0.8 | 0.75 | Spot vs futuro: la prima baja de −54 a −2 conforme vence el contrato |
| ES | `ostium\|SP500` | −25.4 · −27.4…−24.1 | 0.3 | Índice cash: prima de carry, baja ~6 pts/semana y **salta a ~−66 en el roll trimestral** |
| ES | `hyperliquid\|xyz:SP500` | −31.6 · −33…−22.7 | 0.9 | Igual idea, más ruidoso |
| NQ | `ostium\|NDX` | −112 · −121…−100 | 1.4 | Baja ~25 pts/semana; roll → ~−290 |
| NQ | `hyperliquid\|xyz:XYZ100` | −120 · −129…−100 | 3.7 | Más ruidoso |
| YM | `ostium\|DJI` | −97 · −109…−78 | 2.7 | Baja ~40 pts/semana; roll → ~−410 |

Correlación de retornos de 5m perp vs futuro: 0.96–0.99 en todos los pares,
sin desfase de tiempo (lag 0).

## Conclusiones para el agente

1. **El diff no es fijo.** En índices y oro baja cada semana (carry) y salta en
   cada roll de contrato. Una constante fija se queda vieja en días.
2. **Recalibrar antes de cada orden:** mediana de `perp - futuro` de las últimas
   ~12 velas de 5m en común. Si su dispersión (p90−p10) es mayor que ~25% del
   stop, no operar ese símbolo ese día.
3. **Semana de roll = sin operar ese símbolo** (CL mensual; ES/NQ/YM trimestral,
   próximo ~11-dic-2026), hasta tener 1 día de datos con el contrato nuevo.
4. Venues preferidos por ruido: CL → `hyperliquid|xyz:CL`, ES/NQ/YM → `ostium`,
   GC → `binance|XAUUSDT`.
5. Ojo: la vela de cierre de cada día en `bars/` es el settlement de Yahoo y no
   sirve para comparar (`basis.py` la descarta).

## Regenerar

```bash
cd mfp && npm install
NODE_EXTRA_CA_CERTS=/root/.ccr/ca-bundle.crt node fetch-perp-candles.mjs /tmp/perp.json
python3 basis.py /tmp/perp.json > basis.json
```

El WebSocket `api-stream.myfundedperpetuals.com` es público (sin API key).
