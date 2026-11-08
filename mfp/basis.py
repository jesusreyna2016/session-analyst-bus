"""Diferencia de precio perp MFP - futuro (CME) por simbolo de la mesa.

Uso:
  node mfp/fetch-perp-candles.mjs /tmp/perp.json      # baja velas 5m de MFP
  python3 mfp/basis.py /tmp/perp.json > mfp/basis.json

Futuros: bars/*.json (5m, Yahoo). Perps: candles.history del WebSocket de MFP.
diff = perp - futuro, al cierre de la misma vela de 5m.
Precio en MFP ~= precio de la zona (futuro) + diff.
"""
import json, glob, statistics as st, datetime as dt, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
perp = json.load(open(sys.argv[1]))

fut = {}
for f in sorted(glob.glob(os.path.join(ROOT, 'bars', '*.json'))):
    d = json.load(open(f))
    for s, rows in d['symbols'].items():
        for r in rows:
            fut.setdefault(s, {})[int(r[0]) * 1000] = r[4]

# Ultima vela antes de un hueco >30 min = vela de cierre de Yahoo (precio de
# settlement, no de mercado). Se descarta.
for s, F in fut.items():
    ts = sorted(F)
    for a, b in zip(ts, ts[1:]):
        if b - a > 30 * 60000:
            F.pop(a, None)
    if ts:
        F.pop(ts[-1], None)

MAP = {
    'CL': ['hyperliquid|xyz:CL', 'binance|CLUSDT'],
    'GC': ['binance|XAUUSDT'],
    'ES': ['ostium|SP500', 'hyperliquid|xyz:SP500'],
    'NQ': ['ostium|NDX', 'hyperliquid|xyz:XYZ100'],
    'YM': ['ostium|DJI'],
}


def q(a, p):
    a = sorted(a)
    return a[int(p * (len(a) - 1))]


def utc(t):
    return dt.datetime.fromtimestamp(t / 1000, dt.UTC)


out = {'builtAt': dt.datetime.now(dt.UTC).isoformat(timespec='seconds'), 'pairs': {}}
for fs, pl in MAP.items():
    F = fut.get(fs, {})
    for pk in pl:
        if pk not in perp:
            continue
        P = dict(perp[pk])
        D = [(t, P[t] - F[t]) for t in sorted(F) if t in P]
        if len(D) < 200:
            continue
        xs, ys = [], []
        for t, _ in D:
            if t - 300000 in F and t - 300000 in P:
                xs.append(F[t] / F[t - 300000] - 1)
                ys.append(P[t] / P[t - 300000] - 1)
        diffs = [d for _, d in D]
        end = D[-1][0]
        last5 = [d for t, d in D if t >= end - 5 * 86400000]
        last1 = [d for t, d in D if t >= end - 86400000]
        day, wk = {}, {}
        for t, d in D:
            day.setdefault(t // 86400000, []).append(d)
            wk.setdefault(utc(t).strftime('%G-W%V'), []).append(d)
        out['pairs'][f'{fs}->{pk}'] = {
            'fut': fs, 'market_id': pk, 'n': len(D),
            'from': utc(D[0][0]).isoformat(), 'to': utc(end).isoformat(),
            'ret_corr_5m': round(st.correlation(xs, ys), 3),
            'all': {'med': round(st.median(diffs), 3), 'p10': round(q(diffs, .1), 3), 'p90': round(q(diffs, .9), 3)},
            'last5d': {'med': round(st.median(last5), 3), 'p10': round(q(last5, .1), 3), 'p90': round(q(last5, .9), 3)},
            'last1d_med': round(st.median(last1), 3),
            'intraday_sd': round(st.median([st.pstdev(v) for v in day.values() if len(v) > 20]), 3),
            'weekly_med': {k: round(st.median(v), 2) for k, v in sorted(wk.items())},
        }

json.dump(out, sys.stdout, indent=1)
