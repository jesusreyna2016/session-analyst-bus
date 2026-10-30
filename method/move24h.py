#!/usr/bin/env python3
"""Net move of the last 24 h per symbol from bars/ (5m, written hourly by sa-bus-bars).
Rule 8e: zones against this move are the measured edge; in Asia the default session bias
fades it.

Usage: python3 method/move24h.py [ISO time, default now]
Prints one JSON object: { SYM: { "dir": "LONG"|"SHORT"|"FLAT", "pct": -0.84, "from": open,
"to": last close, "bars": n } }. FLAT = |move| < 0.10 % (no call). A symbol with < 24 bars in
the window is left out (say so in dataHealth.notes).
"""
import datetime as dt
import json
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
import grade_plans as G

SYMS = ("NQ", "ES", "GC", "YM", "CL", "ETHUSDT", "BTCUSDT")
FLAT = 0.0010


def move24h(t):
    out = {}
    for s in SYMS:
        bars = G.bars_for(s, t - 24 * 3600, t)
        if len(bars) < 24:
            continue
        o, c = bars[0][1], bars[-1][4]
        pct = (c - o) / o
        out[s] = {"dir": "FLAT" if abs(pct) < FLAT else "LONG" if pct > 0 else "SHORT",
                  "pct": round(100 * pct, 2), "from": o, "to": c, "bars": len(bars)}
    return out


if __name__ == "__main__":
    t = G.parse_ts(sys.argv[1]) if len(sys.argv) > 1 else dt.datetime.now(dt.timezone.utc).timestamp()
    print(json.dumps(move24h(t)))
