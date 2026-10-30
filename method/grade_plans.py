#!/usr/bin/env python3
"""Grade a day's plans against real 5m bars (bars/<YYYY-MM-DD>.json, UTC days, written hourly
by the Netlify function sa-bus-bars). Deterministic: the agent no longer grades from memory.

Usage: python3 method/grade_plans.py <fecha>             futures day (pre-asia/pre-london/pre-ny)
       python3 method/grade_plans.py --crypto <fecha>    crypto-weekend plans of that CT day

Writes grades/<fecha>.json (or grades/crypto/<fecha>.json) and prints a one-line summary.
update_scorecard.py reads grades/<fecha>.json and uses it for hitLog bias / scenA / zone.

What is graded, per plan run and instrument (window = the session the plan was written for,
starting at the plan's generatedAt, never before):
  bias   biasSession LONG/SHORT vs the session's net move (last close vs first open). NEUTRAL
         and INDECISO are skipped (not a call).
  zone   each zone with range+dir: touched (a bar overlapped the range), then the trigger the
         plans use: first 5m close back out of the zone on the trade side (SHORT close < lo,
         LONG close > hi) = entry at that close; a close through the far side first = broken
         (no trade). With risk.stopPts/risk.tgtPts (futures) or play.stop/play.tp1 (crypto):
         worked = target before stop. A bar that hits both counts as failed (conservative,
         5m bars can't order them). Outcomes: untouched | broken | no-trigger | worked |
         failed | open.
  scenA  scenarioA with entryZone+target: hit = entryZone touched and target reached later in
         the window; miss = touched, target not reached; untriggered = never touched (not
         counted). Without entryZone: hit = target reached in the window.
  em     expectedMove low/high vs the session's real range (high - low) from generatedAt.
  Each graded zone also carries family (reversion | continuation | sweep | other), vs24h
  (with | against | flat: zone direction vs the net move of the 24 h before the window, rule
  8e) and r (worked = target/stop distance, failed = -1). update_scorecard.py pools these
  into scorecard.zoneEdge.
"""
import datetime as dt
import io
import json
import os
import sys
from zoneinfo import ZoneInfo

CT = ZoneInfo("America/Chicago")
FUT = ("NQ", "ES", "GC", "YM", "CL")
RUNS = (("pre-asia", "asia"), ("pre-london", "london"), ("pre-ny", "ny"))
FAMILY = {t: "reversion" for t in ("fade_vah", "fade_val", "poc_reversion", "bounce_val", "bounce_vah", "ib_fade", "golden_zone")}
FAMILY.update({t: "continuation" for t in ("pullback_cont", "retest_break", "poc_breakout", "ib_break", "asia_range_break")})


def family(t):
    t = t or ""
    return FAMILY.get(t) or ("sweep" if t.startswith("sweep_") or t == "liq_reclaim" else "other")


def dir24h(sym, t0):
    """Net direction of the 24 h before t0: LONG | SHORT | FLAT (|move| < 0.10 %), None without bars."""
    prev = bars_for(sym, t0 - 24 * 3600, t0)
    if len(prev) < 24:
        return None
    pct = (prev[-1][4] - prev[0][1]) / prev[0][1]
    return "FLAT" if abs(pct) < 0.001 else "LONG" if pct > 0 else "SHORT"


def tag_zone(res, d24):
    res["family"] = family(res.get("type"))
    res["vs24h"] = None if d24 is None else "flat" if d24 == "FLAT" else "with" if res["dir"] == d24 else "against"
    if res.get("outcome") in ("worked", "failed") and res.get("stop") is not None:
        risk = abs(res["entry"] - res["stop"])
        res["r"] = round(abs(res["target"] - res["entry"]) / risk, 2) if res["outcome"] == "worked" and risk else -1.0
    return res


def load(p):
    return json.load(io.open(p, encoding="utf-8"))


_bars_cache = {}


def bars_for(sym, t0, t1):
    """5m bars [t, o, h, l, c] with t0 <= t < t1 (epoch seconds), across the UTC day files."""
    out = []
    d = dt.datetime.fromtimestamp(t0, dt.timezone.utc).date()
    end = dt.datetime.fromtimestamp(t1, dt.timezone.utc).date()
    while d <= end:
        key = d.isoformat()
        if key not in _bars_cache:
            try:
                _bars_cache[key] = load("bars/%s.json" % key).get("symbols") or {}
            except (FileNotFoundError, ValueError):
                _bars_cache[key] = {}
        out += [b for b in _bars_cache[key].get(sym, []) if t0 <= b[0] < t1]
        d += dt.timedelta(days=1)
    return sorted(out)


def ct(day, hh, mm=0):
    return dt.datetime.combine(day, dt.time(hh, mm), CT).timestamp()


def session_window(fecha, session):
    d = dt.date.fromisoformat(fecha)
    if session == "asia":
        return ct(d - dt.timedelta(days=1), 17), ct(d, 2)
    if session == "london":
        return ct(d, 2), ct(d, 8, 30)
    return ct(d, 8, 30), ct(d, 16)


def parse_ts(s):
    try:
        return dt.datetime.fromisoformat(str(s).replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def overlaps(b, lo, hi):
    return b[3] <= hi and b[2] >= lo


def grade_zone(z, bars, crypto=False):
    rng = z.get("range") or []
    d = (z.get("dir") or "").upper()
    if len(rng) != 2 or d not in ("LONG", "SHORT") or not bars:
        return None
    lo, hi = sorted(float(x) for x in rng)
    first = next((i for i, b in enumerate(bars) if overlaps(b, lo, hi)), None)
    res = {"range": [lo, hi], "dir": d, "type": z.get("type"), "grade": z.get("grade"), "tcl": z.get("tcl"),
           "touched": first is not None}
    if first is None:
        res["outcome"] = "untouched"
        return res
    # entry like the plans' triggers ("cierre 5m bajo X tras rechazar"): after the touch, the
    # first 5m close back out of the zone on the trade side confirms it (SHORT: close < lo,
    # LONG: close > hi). A close through the far side first = the zone broke, no trade.
    trig = None
    for j in range(first, len(bars)):
        c = bars[j][4]
        if (d == "SHORT" and c > hi) or (d == "LONG" and c < lo):
            res["outcome"] = "broken"
            return res
        if (d == "SHORT" and c < lo) or (d == "LONG" and c > hi):
            trig = j
            break
    if trig is None:
        res["outcome"] = "no-trigger"
        return res
    entry = bars[trig][4]
    first = trig + 1
    play = z.get("play") or {}
    risk = z.get("risk") or {}
    stop = tgt = None
    if crypto and play.get("stop") is not None and play.get("tp1") is not None:
        stop, tgt = float(play["stop"]), float(play["tp1"])
    elif risk.get("stopPts") and risk.get("tgtPts"):
        sp, tp = float(risk["stopPts"]), float(risk["tgtPts"])
        stop, tgt = (entry - sp, entry + tp) if d == "LONG" else (entry + sp, entry - tp)
    res["entry"] = round(entry, 4)
    if stop is None:
        res["outcome"] = "touched-no-levels"
        return res
    res.update(stop=round(stop, 4), target=round(tgt, 4))
    if first >= len(bars):
        res["outcome"] = "open"
        return res
    for b in bars[first:]:
        hit_stop = b[3] <= stop if d == "LONG" else b[2] >= stop
        hit_tgt = b[2] >= tgt if d == "LONG" else b[3] <= tgt
        if hit_stop:
            res["outcome"] = "failed"
            return res
        if hit_tgt:
            res["outcome"] = "worked"
            return res
    res["outcome"] = "open"
    return res


def grade_scen(sc, bars):
    if not isinstance(sc, dict) or sc.get("target") is None or not bars:
        return None
    tgt = float(sc["target"])
    ez = sc.get("entryZone")
    if ez and len(ez) == 2:
        lo, hi = sorted(float(x) for x in ez)
        first = next((i for i, b in enumerate(bars) if overlaps(b, lo, hi)), None)
        if first is None:
            return {"outcome": "untriggered", "target": tgt}
        up = tgt > (lo + hi) / 2
        hit = any((b[2] >= tgt) if up else (b[3] <= tgt) for b in bars[first:])
        return {"outcome": "hit" if hit else "miss", "target": tgt}
    up = tgt > bars[0][1]
    hit = any((b[2] >= tgt) if up else (b[3] <= tgt) for b in bars)
    return {"outcome": "hit" if hit else "miss", "target": tgt}


def grade_bias(bias, bars):
    b = (bias or "").upper()
    if b not in ("LONG", "SHORT") or not bars:
        return None
    move = bars[-1][4] - bars[0][1]
    return {"call": b, "movePts": round(move, 4), "outcome": "hit" if (move > 0) == (b == "LONG") and move != 0 else "miss"}


def grade_em(em, bars):
    if not isinstance(em, dict) or em.get("low") is None or em.get("high") is None or not bars:
        return None
    real = max(b[2] for b in bars) - min(b[3] for b in bars)
    lo, hi = float(em["low"]), float(em["high"])
    return {"low": lo, "base": em.get("base"), "high": hi, "realPts": round(real, 4),
            "outcome": "hit" if lo <= real <= hi else ("under" if real < lo else "over")}


def summarize(runs, syms):
    """hitLog-shaped totals per symbol: [hits, n]."""
    tot = {}
    for r in runs:
        for sym, g in r["instruments"].items():
            t = tot.setdefault(sym, {"bias": [0, 0], "scenA": [0, 0], "zone": [0, 0], "em": [0, 0]})
            if g.get("bias"):
                t["bias"][1] += 1
                t["bias"][0] += g["bias"]["outcome"] == "hit"
            if g.get("scenA") and g["scenA"]["outcome"] in ("hit", "miss"):
                t["scenA"][1] += 1
                t["scenA"][0] += g["scenA"]["outcome"] == "hit"
            for z in g.get("zones") or []:
                if z.get("outcome") in ("worked", "failed"):
                    t["zone"][1] += 1
                    t["zone"][0] += z["outcome"] == "worked"
            if g.get("em"):
                t["em"][1] += 1
                t["em"][0] += g["em"]["outcome"] == "hit"
    return {s: {k: v for k, v in t.items() if v[1]} for s, t in tot.items()}


def grade_futures(fecha):
    runs = []
    for run, session in RUNS:
        try:
            p = load("plans/%s-%s.json" % (fecha, run))
        except FileNotFoundError:
            continue
        w0, w1 = session_window(fecha, p.get("session") or session)
        g0 = max(w0, parse_ts(p.get("generatedAt")) or w0)
        out = {"run": run, "session": p.get("session") or session, "from": g0, "to": w1, "instruments": {}}
        for sym in FUT:
            inst = (p.get("instruments") or {}).get(sym)
            if not inst:
                continue
            bars = bars_for(sym, g0, w1)
            if not bars:
                out["instruments"][sym] = {"error": "no bars"}
                continue
            d24 = dir24h(sym, g0)
            out["instruments"][sym] = {
                "bars": len(bars),
                "dir24h": d24,
                "bias": grade_bias(inst.get("biasSession"), bars),
                "scenA": grade_scen(inst.get("scenarioA"), bars),
                "zones": [tag_zone(x, d24) for x in (grade_zone(z, bars) for z in inst.get("zones") or []) if x],
                "em": grade_em(inst.get("expectedMove"), bars),
            }
        runs.append(out)
    return {"date": fecha, "kind": "futures", "gradedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
            "runs": runs, "hitLog": summarize(runs, FUT)}


def grade_crypto(fecha):
    runs = []
    folder = "plans/crypto"
    for name in sorted(os.listdir(folder)) if os.path.isdir(folder) else []:
        if not name.startswith(fecha):
            continue
        p = load(os.path.join(folder, name))
        g0 = parse_ts(p.get("builtAt"))
        g1 = parse_ts(p.get("validUntil")) or (g0 + 12 * 3600 if g0 else None)
        if not g0:
            continue
        g1 = min(g1, dt.datetime.now(dt.timezone.utc).timestamp())
        out = {"run": name[:-5], "from": g0, "to": g1, "instruments": {}}
        for sym, inst in (p.get("instruments") or {}).items():
            bars = bars_for(sym, g0, g1)
            if not bars:
                out["instruments"][sym] = {"error": "no bars"}
                continue
            d24 = dir24h(sym, g0)
            out["instruments"][sym] = {
                "bars": len(bars),
                "dir24h": d24,
                "bias": grade_bias(inst.get("biasSession"), bars),
                "zones": [tag_zone(x, d24) for x in (grade_zone(z, bars, crypto=True) for z in inst.get("zones") or []) if x],
            }
        runs.append(out)
    return {"date": fecha, "kind": "crypto", "gradedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
            "runs": runs, "hitLog": summarize(runs, None)}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    fecha, crypto = args[0], "--crypto" in sys.argv
    g = grade_crypto(fecha) if crypto else grade_futures(fecha)
    path = ("grades/crypto/%s.json" if crypto else "grades/%s.json") % fecha
    os.makedirs(os.path.dirname(path), exist_ok=True)
    io.open(path, "w", encoding="utf-8", newline="\n").write(json.dumps(g, ensure_ascii=False, indent=1))
    parts = []
    for sym, t in sorted(g["hitLog"].items()):
        parts.append(sym + " " + " ".join("%s %d/%d" % (k, h, n) for k, (h, n) in t.items()))
    print("%s graded %d runs: %s" % (path, len(g["runs"]), " · ".join(parts) or "nothing gradable"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
