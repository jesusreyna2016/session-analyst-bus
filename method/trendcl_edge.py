"""Trend Checklist zone-touch test, rebuilt outside TradingView, with an offset-level control.

Replicates the "ZONE TOUCHES" table of trend_checklist.pine (v2.3+ rules):
  levels  : 1H EMA20, DO (session open 18:00 ET), session VWAP (hlc3), TDO (00:00 ET), PDH, PDL,
            previous-session pVAH / pPOC / pVAL (60 rows, 70 % value area)
  touch   : high >= lvl - tol and low <= lvl + tol, tol = 0.03 % of close; 60 min cooldown per level;
            a level is skipped on the bar it is born (v2.3 fix)
  trade   : direction = close[1] > lvl ? long : short, entry at the level, symmetric race +-0.15 % of price,
            both sides in one bar = loss, first checked on the next bar, graded by close after 4 h.
            R = result / T.
  label   : confirmed verdict (D / 4H / 1H arrows: structure by 3/3 pivots with BOS + close vs EMA20),
            in favor / against / no verdict.
Control : the same rules on fake levels at each real level x (1 +- 0.35 %) and x (1 +- 0.70 %).
          If "against" also loses at random prices, the gap is a trend effect, not a level effect.

Usage: python -I trendcl_edge.py <bus_dir> <htf_dir> <out_json>
  htf_dir holds <SYM>.json = Yahoo 1h bars [[t, o, h, l, c], ...] for HTF warm-up (bus bars have no volume and
  start 2026-08-21, too short for a daily EMA50). VWAP and profile use equal weight per bar (no volume in the bus).
"""
import bisect, datetime as dt, glob, json, math, random, sys

SYMS = ["NQ", "ES", "GC", "YM", "CL"]
TOL, RACE, LOOK, COOL = 0.0003, 0.0015, 4 * 3600, 3600
OFFS = [0.0035, -0.0035, 0.007, -0.007]


def et_offset(t):
    """Seconds to add to UTC for America/New_York (US DST rules since 2007)."""
    y = dt.datetime.fromtimestamp(t, dt.timezone.utc).year
    def nth_sun(m, n):
        d = dt.datetime(y, m, 1, tzinfo=dt.timezone.utc)
        d += dt.timedelta(days=(6 - d.weekday()) % 7 + 7 * (n - 1))
        return d
    start = nth_sun(3, 2).timestamp() + 7 * 3600   # 2:00 EST
    end = nth_sun(11, 1).timestamp() + 6 * 3600    # 2:00 EDT
    return -4 * 3600 if start <= t < end else -5 * 3600


def et(t):
    return dt.datetime.fromtimestamp(t + et_offset(t), dt.timezone.utc)


def trade_day(t):
    return (et(t) + dt.timedelta(hours=6)).date()


def session(t):
    e = et(t); m = e.hour * 60 + e.minute
    return "asia" if (m >= 18 * 60 or m < 3 * 60) else "london" if m < 9 * 60 + 30 else "ny"


def ema(xs, n):
    out, a, s = [], 2 / (n + 1), None
    for i, x in enumerate(xs):
        if i < n - 1:
            out.append(None); continue
        s = sum(xs[:n]) / n if i == n - 1 else a * x + (1 - a) * s
        out.append(s)
    return out


def f_eval(bars, pv=3):
    """bars: list of (close_time, o, h, l, c). Returns arrow per bar (Pine f_eval)."""
    H = [b[2] for b in bars]; L = [b[3] for b in bars]; C = [b[4] for b in bars]
    e20 = ema(C, 20)
    h1 = h2 = l1 = l2 = None; bos = 0; arr = []
    for i in range(len(bars)):
        j = i - pv
        if j - pv >= 0:
            if all(H[j] > H[k] for k in range(j - pv, j)) and all(H[j] >= H[k] for k in range(j + 1, i + 1)):
                h2, h1 = h1, H[j]
            if all(L[j] < L[k] for k in range(j - pv, j)) and all(L[j] <= L[k] for k in range(j + 1, i + 1)):
                l2, l1 = l1, L[j]
        if h1 is not None and C[i] > h1: bos = 1
        if l1 is not None and C[i] < l1: bos = -1
        up = None not in (h1, h2, l1, l2) and h1 > h2 and l1 > l2
        dn = None not in (h1, h2, l1, l2) and h1 < h2 and l1 < l2
        seq = 1 if up else -1 if dn else 0
        st = seq if (bos == 0 or bos == seq) else bos * 2 if seq == 0 else bos * 3
        e = e20[i]
        arr.append(0 if e is None else 1 if (st > 0 and C[i] > e) else -1 if (st < 0 and C[i] < e) else 0)
    return arr, e20


def group(h1, keyf):
    out, cur, k0 = [], None, None
    for t, o, h, l, c in h1:
        k = keyf(t)
        if k != k0:
            if cur: out.append(tuple(cur))
            cur, k0 = [t + 3600, o, h, l, c], k
        else:
            cur[0] = t + 3600; cur[2] = max(cur[2], h); cur[3] = min(cur[3], l); cur[4] = c
    if cur: out.append(tuple(cur))
    return out


def htf_series(h1):
    s1 = [(t + 3600, o, h, l, c) for t, o, h, l, c in h1]
    s4 = group(h1, lambda t: (trade_day(t), ((et(t).hour + 6) % 24) // 4))
    sD = group(h1, trade_day)
    res = {}
    for name, s in (("1", s1), ("4", s4), ("D", sD)):
        a, e = f_eval(s)
        res[name] = ([b[0] for b in s], a, e)
    return res


def lookup(ser, ct):
    ts, a, e = ser
    i = bisect.bisect_right(ts, ct) - 1
    return (a[i], e[i]) if i >= 0 else (0, None)


def verdict(a, b, c):
    u = (a == 1) + (b == 1) + (c == 1); d = (a == -1) + (b == -1) + (c == -1)
    return 2 if u == 3 else -2 if d == 3 else 1 if (u == 2 and c == 1) else -1 if (d == 2 and c == -1) else 0


def profile(bars, rows=60, pct=70):
    hi = max(b[2] for b in bars); lo = min(b[3] for b in bars)
    if not hi > lo: return (None, None, None)
    step = (hi - lo) / rows; bins = [0.0] * rows
    for b in bars:
        i0 = max(0, min(rows - 1, int(math.floor((b[3] - lo) / step))))
        i1 = max(0, min(rows - 1, int(math.floor((b[2] - lo) / step))))
        for k in range(i0, i1 + 1): bins[k] += 1.0 / (i1 - i0 + 1)
    pi = bins.index(max(bins)); tot = sum(bins); acc = bins[pi]; up = dn = pi
    while acc < tot * pct / 100 and (up < rows - 1 or dn > 0):
        vu = bins[up + 1] if up < rows - 1 else -1.0
        vd = bins[dn - 1] if dn > 0 else -1.0
        if vu >= vd: up += 1; acc += vu
        else: dn -= 1; acc += vd
    return (lo + (up + 1) * step, lo + (pi + 0.5) * step, lo + dn * step)  # vah, poc, val


def run(sym, bars, sec, htf, out):
    names = ["EMA20_1H", "DO", "VWAP", "TDO", "PDH", "PDL", "pVAH", "pPOC", "pVAL"]
    lv_last = {}; open_tr = []
    day = None; do = vws = vwn = tdo = pdh = pdl = vah = poc = val = None
    sess_bars = []; prev_sess = None; ny_day = None
    for i, (t, o, h, l, c) in enumerate(bars):
        ct = t + sec
        td = trade_day(t)
        born = {"DO": False, "VWAP": False, "TDO": False, "PD": False, "VP": False}
        if td != day:
            if sess_bars:
                prev_sess = sess_bars
                pdh = max(b[2] for b in prev_sess); pdl = min(b[3] for b in prev_sess)
                vah, poc, val = profile(prev_sess)
                born["PD"] = born["VP"] = True
            day, do, vws, vwn, sess_bars = td, o, 0.0, 0, []
            born["DO"] = born["VWAP"] = True
        sess_bars.append((t, o, h, l, c))
        vws += (h + l + c) / 3; vwn += 1
        vw = vws / vwn
        nd = et(t).date()
        if nd != ny_day:
            if ny_day is not None: born["TDO"] = True
            ny_day, tdo = nd, o
        aD, _ = lookup(htf["D"], ct); a4, _ = lookup(htf["4"], ct); a1, e201 = lookup(htf["1"], ct)
        sV = (verdict(aD, a4, a1) > 0) - (verdict(aD, a4, a1) < 0)
        # resolve open trades on this bar
        T = c * RACE
        keep = []
        for tr in open_tr:
            en, dd = tr["en"], tr["dir"]
            hw = h >= en + T if dd > 0 else l <= en - T
            hl = l <= en - T if dd > 0 else h >= en + T
            if hw or hl or t >= tr["due"]:
                r = -1.0 if hl else 1.0 if hw else dd * (c - en) / T
                tr["R"] = r; tr["win"] = r > 0
                del tr["en"], tr["due"]
                out.append(tr)
            else:
                keep.append(tr)
        open_tr = keep
        if i == 0: continue
        pc = bars[i - 1][4]
        lv = [e201, do, vw, tdo, pdh, pdl, vah, poc, val]
        bn = [False, born["DO"], born["VWAP"], born["TDO"], born["PD"], born["PD"], born["VP"], born["VP"], born["VP"]]
        tol = c * TOL
        for k in range(9):
            base = lv[k]
            if base is None or bn[k]: continue
            for kind, off in [("key", 0.0)] + [("ctrl", x) for x in OFFS]:
                x = base * (1 + off); key = (k, off)
                if h >= x - tol and l <= x + tol and t - lv_last.get(key, -10**12) >= COOL:
                    lv_last[key] = t
                    dz = 1 if pc > x else -1
                    open_tr.append({"sym": sym, "tf": sec // 60, "kind": kind, "lvl": names[k], "t": t,
                                    "day": str(trade_day(t)), "sess": session(t), "dir": dz,
                                    "cat": "none" if sV == 0 else "favor" if dz == sV else "against",
                                    "en": x, "due": t + LOOK})


def main():
    bus, htfdir, outp = sys.argv[1:4]
    raw = {}
    for f in sorted(glob.glob(bus + "/bars/*.json")):
        for s, b in json.load(open(f))["symbols"].items():
            if s in SYMS:
                m = raw.setdefault(s, {})
                for r in b:
                    if r[0] % 300 == 0: m[r[0]] = tuple(r[:5])
    out = []
    for s in SYMS:
        b5 = [raw[s][t] for t in sorted(raw[s])]
        htf = htf_series(json.load(open(htfdir + "/" + s + ".json")))
        b15, cur = [], None
        for t, o, h, l, c in b5:
            k = t // 900 * 900
            if cur is None or cur[0] != k:
                if cur: b15.append(tuple(cur))
                cur = [k, o, h, l, c]
            else:
                cur[2] = max(cur[2], h); cur[3] = min(cur[3], l); cur[4] = c
        if cur: b15.append(tuple(cur))
        run(s, b5, 300, htf, out)
        run(s, b15, 900, htf, out)
        print(s, len(b5), "bars 5m", len(out), "trades so far", file=sys.stderr)
    json.dump(out, open(outp, "w"))


if __name__ == "__main__":
    main()
