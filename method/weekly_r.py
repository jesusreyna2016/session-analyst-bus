#!/usr/bin/env python3
"""One weekly number: expectancy in R of the plan vs Jesus's execution, same week, same unit.

Usage: python3 method/weekly_r.py                 the Mon-Fri week that last closed (CT)
       python3 method/weekly_r.py 2026-10-26      the Mon-Fri week starting that Monday
       add --json for the machine-readable block (the weekly review stores it)

plan  every zone of the futures plans of the week graded with real bars in grades/<date>.json
      that actually triggered: worked = +target/stop distance (its r), failed = -1.
      E[R] = mean r. Crypto zones (grades/crypto/) go in their own line.
exec  every real position of the week in live/journal.json (byDay[].fills, points only, no
      money, no size). 1R = the stop the plan live at that minute had for that symbol:
      the stop of the zone the entry was in (in-plan), otherwise the median stop of that
      plan's zones for the symbol. R = pts / 1R. Positions with no plan stop are "unrated".
      Split by plan_vs_exec class: in-plan / off-zone / against.
gap   plan E[R] - exec E[R]: what stays in the execution.
"""
import datetime as dt
import io
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plan_vs_exec import classify, plan_at, root, ts  # noqa: E402


def load(p):
    return json.load(io.open(p, encoding="utf-8"))


def week_days(monday):
    return [(monday + dt.timedelta(days=i)).isoformat() for i in range(5)]


def last_closed_monday(today):
    # Saturday 10:00 CT weekly: the week that closed yesterday; any other day: the last full one
    back = today.weekday() + 7 if today.weekday() < 5 else today.weekday()
    return today - dt.timedelta(days=back)


def plan_r(days, folder="grades"):
    rs = []
    for d in days:
        p = os.path.join(folder, d + ".json")
        if not os.path.exists(p):
            continue
        for run in load(p).get("runs") or []:
            for inst in (run.get("instruments") or {}).values():
                for z in inst.get("zones") or []:
                    if z.get("outcome") in ("worked", "failed") and z.get("r") is not None:
                        rs.append(float(z["r"]))
    return rs


def zone_stop_pts(z, entry=None):
    risk = z.get("risk") or {}
    if risk.get("stopPts"):
        return float(risk["stopPts"])
    play = z.get("play") or {}
    rng = z.get("range") or []
    if play.get("stop") is not None and len(rng) == 2:
        stop = float(play["stop"])
        ref = float(entry) if entry is not None else (
            max(map(float, rng)) if (z.get("dir") or "").upper() == "LONG" else min(map(float, rng)))
        d = abs(ref - stop)
        return d or None
    return None


def one_r(f, key):
    t = ts(f.get("t"))
    p = plan_at(key, t) if t else None
    inst = ((p or {}).get("instruments") or {}).get(key) if p else None
    if not inst:
        return None
    side = "LONG" if f.get("side") == "long" else "SHORT"
    e = f.get("entry")
    stops = []
    for z in inst.get("zones") or []:
        rng = z.get("range") or []
        sp = zone_stop_pts(z)
        if sp:
            stops.append(sp)
        if e is not None and len(rng) == 2 and (z.get("dir") or "").upper() == side:
            lo, hi = sorted(float(x) for x in rng)
            pad = (hi - lo) * 0.1
            if lo - pad <= float(e) <= hi + pad:
                own = zone_stop_pts(z, e)
                if own:
                    return own
    return statistics.median(stops) if stops else None


def exec_r(days, journal):
    by = {}
    unrated = 0
    for day in journal.get("byDay") or []:
        if day.get("date") not in days:
            continue
        for f in day.get("fills") or []:
            key, cls = classify(f)
            if not key or f.get("pts") is None:
                continue
            r1 = one_r(f, key)
            if not r1:
                unrated += 1
                continue
            by.setdefault(cls, []).append(float(f["pts"]) / r1)
    return by, unrated


def stats(rs):
    if not rs:
        return {"n": 0, "expR": None, "winRate": None}
    return {"n": len(rs), "expR": round(sum(rs) / len(rs), 2), "winRate": round(sum(r > 0 for r in rs) / len(rs), 2)}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        monday = dt.date.fromisoformat(args[0])
    else:
        ct = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=6)
        monday = last_closed_monday(ct.date())
    days = week_days(monday)
    try:
        journal = load("live/journal.json")
    except FileNotFoundError:
        journal = {}
    plan = stats(plan_r(days))
    crypto = stats(plan_r(days, "grades/crypto"))
    by, unrated = exec_r(days, journal)
    allx = [r for rs in by.values() for r in rs]
    ex = stats(allx)
    out = {
        "week": days[0] + ".." + days[-1],
        "plan": plan, "planCrypto": crypto,
        "exec": ex, "execByClass": {k: stats(v) for k, v in sorted(by.items())}, "execUnrated": unrated,
        "gapR": round(plan["expR"] - ex["expR"], 2) if plan["expR"] is not None and ex["expR"] is not None else None,
        "note": "plan = graded zones that triggered (grades/); exec = journal fills, R = pts / the live plan's stop for that symbol (method/weekly_r.py). No money.",
    }
    if "--json" in sys.argv:
        print(json.dumps(out, ensure_ascii=False))
        return 0
    f = lambda s: "n/a" if s["expR"] is None else "%+.2fR (n=%d, %d%% ganan)" % (s["expR"], s["n"], round(100 * s["winRate"]))
    print("semana %s" % out["week"])
    print("plan      %s" % f(plan))
    print("ejecución %s" % (f(ex) if ex["n"] else "sin posiciones con precio en el journal (sincroniza desde mywhyjournal.com)"))
    for k, s in out["execByClass"].items():
        print("  %-9s %s" % (k, f(s)))
    if unrated:
        print("  sin stop del plan para medir: %d" % unrated)
    if out["gapR"] is not None:
        print("brecha    %+.2fR por trade (plan menos ejecución)" % out["gapR"])
    if crypto["n"]:
        print("plan cripto %s" % f(crypto))
    return 0


if __name__ == "__main__":
    sys.exit(main())
