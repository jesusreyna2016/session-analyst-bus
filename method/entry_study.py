#!/usr/bin/env python3
"""Entry and exit study for the Session Analyst futures zones, on the bus's real 5m bars.

For every zone of every saved plan (plans/<fecha>-pre-*.json) it replays the session window the
grader uses (from the plan's generatedAt to the session end) four ways and reports R per trade:

  trigger_target   entry at the close of the 5m trigger bar (what grade_plans.py does), stop at
                   entry -/+ risk.stopPts, all out at risk.tgtPts. This is the number zoneEdge reads.
  trigger_plan     same entry and stop, exits as the plan says (trader-profile.exitPlan / 4.1):
                   1/2 at +1R, the rest to breakeven, runner to the same target.
  limit_target     resting limit at the near edge of the zone (SHORT: zone low, LONG: zone high),
                   filled when a bar trades through it; stop at the plan's structural stop (first
                   price in play.structStop) or, if none, the far edge -/+ risk.stopPts; all out at
                   the same target price as trigger_target.
  limit_plan       the limit entry with the plan's exit (1/2 at +1R, BE, runner).

Conservative bar rules: a bar that touches the stop and a target counts as the stop; on the fill
bar only the stop counts; after BE is armed a bar touching BE and the target counts as BE. A trade
still open at the window end is marked at the last close.

Usage: python3 method/entry_study.py [--since 2026-10-01] [--json out.json]
Prints a table by family x vs24h, by verdict (GO / rest) and overall. Read-only.
Python 3.11 stdlib only.
"""
import argparse
import glob
import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grade_plans as gp  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUM = re.compile(r"\d[\d,]*\.?\d*")


def first_price(txt, ref):
    """First number in the text that looks like a price near ref (within 20 %)."""
    for m in NUM.finditer(txt or ""):
        try:
            v = float(m.group().replace(",", ""))
        except ValueError:
            continue
        if ref and abs(v - ref) / ref < 0.2:
            return v
    return None


def simulate(bars, i0, side, entry, stop, target, plan_exit, fill_bar_stop_only=True):
    """Walk bars from index i0 (the bar after the entry, or the fill bar itself when
    fill_bar_stop_only). Returns R (float) or None when risk is not positive."""
    risk = (entry - stop) * side
    if risk <= 0:
        return None
    one_r = entry + side * risk
    tgt_r = (target - entry) * side / risk
    half_done = False
    for j in range(i0, len(bars)):
        b = bars[j]
        hi, lo = b[2], b[3]
        only_stop = fill_bar_stop_only and j == i0
        cur_stop = entry if half_done else stop
        hit_stop = lo <= cur_stop if side == 1 else hi >= cur_stop
        hit_tgt = (hi >= target if side == 1 else lo <= target) and not only_stop
        hit_1r = (hi >= one_r if side == 1 else lo <= one_r) and not only_stop
        if hit_stop:
            if half_done:
                return 0.5 * 1.0 + 0.0
            return -1.0
        if not plan_exit or tgt_r <= 1:
            if hit_tgt:
                return round(tgt_r, 3)
            continue
        if not half_done and hit_1r:
            half_done = True
            if hit_tgt:
                return round(0.5 + 0.5 * tgt_r, 3)
            continue
        if half_done and hit_tgt:
            return round(0.5 + 0.5 * tgt_r, 3)
    last = bars[-1][4]
    r_open = (last - entry) * side / risk
    if plan_exit and half_done:
        return round(0.5 + 0.5 * max(r_open, 0.0), 3)
    return round(r_open, 3)


def study_zone(z, bars):
    rng = z.get("range") or []
    d = (z.get("dir") or "").upper()
    if len(rng) != 2 or d not in ("LONG", "SHORT") or not bars:
        return None
    side = 1 if d == "LONG" else -1
    lo, hi = sorted(float(x) for x in rng)
    risk = z.get("risk") or {}
    try:
        sp, tp = float(risk.get("stopPts")), float(risk.get("tgtPts"))
    except (TypeError, ValueError):
        return None
    if sp <= 0 or tp <= 0:
        return None
    out = {}
    # trigger entry, exactly as grade_plans.grade_zone
    first = next((i for i, b in enumerate(bars) if gp.overlaps(b, lo, hi)), None)
    if first is not None:
        trig = None
        for j in range(first, len(bars)):
            c = bars[j][4]
            if (side == -1 and c > hi) or (side == 1 and c < lo):
                break
            if (side == -1 and c < lo) or (side == 1 and c > hi):
                trig = j
                break
        if trig is not None and trig + 1 < len(bars):
            e = bars[trig][4]
            st, tg = e - side * sp, e + side * tp
            out["trigger_target"] = simulate(bars, trig + 1, side, e, st, tg, False, False)
            out["trigger_plan"] = simulate(bars, trig + 1, side, e, st, tg, True, False)
    # limit at the near edge
    near = lo if side == -1 else hi
    far = hi if side == -1 else lo
    ss = ((z.get("play") or {}).get("structStop") or {})
    ss = ss.get("es") if isinstance(ss, dict) else ss
    st = first_price(ss, near)
    if st is None or (near - st) * side <= 0:
        st = far - side * sp
    tg = near + side * tp
    fill = next((i for i, b in enumerate(bars) if (b[2] >= near if side == -1 else b[3] <= near)), None)
    if fill is not None:
        out["limit_target"] = simulate(bars, fill, side, near, st, tg, False, True)
        out["limit_plan"] = simulate(bars, fill, side, near, st, tg, True, True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="2026-10-01")
    ap.add_argument("--json")
    a = ap.parse_args()
    os.chdir(ROOT)
    rows = []
    for path in sorted(glob.glob("plans/20*-pre-*.json")):
        fecha, run = os.path.basename(path)[:10], os.path.basename(path)[11:-5]
        if fecha < a.since:
            continue
        sess = dict(gp.RUNS).get(run)
        if not sess:
            continue
        try:
            p = gp.load(path)
        except ValueError:
            continue
        w0, w1 = gp.session_window(fecha, p.get("session") or sess)
        g0 = max(w0, gp.parse_ts(p.get("generatedAt")) or w0)
        for sym in gp.FUT:
            inst = (p.get("instruments") or {}).get(sym)
            if not inst:
                continue
            bars = gp.bars_for(sym, g0, w1)
            if len(bars) < 3:
                continue
            d24 = gp.dir24h(sym, g0)
            verdict = (inst.get("verdict") or {}).get("signal")
            for k, z in enumerate(inst.get("zones") or []):
                res = study_zone(z, bars)
                if not res:
                    continue
                fam = gp.family(z.get("type"))
                v = None if d24 is None else "flat" if d24 == "FLAT" else "with" if (z.get("dir") or "").upper() == d24 else "against"
                rows.append({"date": fecha, "run": run, "sym": sym, "type": z.get("type"), "family": fam,
                             "vs24h": v, "go": verdict == "GO" and k == 0, **res})
    keys = ["trigger_target", "trigger_plan", "limit_target", "limit_plan"]

    def agg(rs):
        o = {}
        for k in keys:
            v = [r[k] for r in rs if r.get(k) is not None]
            if v:
                wins = sum(1 for x in v if x > 0)
                o[k] = {"n": len(v), "expR": round(sum(v) / len(v), 3), "winRate": round(wins / len(v), 3)}
        return o

    groups = defaultdict(list)
    for r in rows:
        groups["ALL"].append(r)
        groups["GO (zones[0] de un GO)" if r["go"] else "resto"].append(r)
        groups["%s|%s" % (r["family"], r["vs24h"])].append(r)
        groups["session|%s" % r["run"]].append(r)
    res = {"since": a.since, "zones": len(rows), "groups": {g: agg(rs) for g, rs in sorted(groups.items(), key=lambda kv: -len(kv[1]))}}
    if a.json:
        json.dump({**res, "rows": rows}, open(a.json, "w"), ensure_ascii=False, indent=1)
    print(f"zonas estudiadas desde {a.since}: {len(rows)}")
    print(f"{'grupo':34s} " + " ".join(f"{k:>22s}" for k in keys))
    for g, o in res["groups"].items():
        cells = []
        for k in keys:
            c = o.get(k)
            cells.append(f"{c['expR']:+.2f}R {c['winRate']*100:3.0f}% n{c['n']:<4d}" if c else f"{'-':>22s}")
        print(f"{g:34s} " + " ".join(f"{x:>22s}" for x in cells))


if __name__ == "__main__":
    main()
