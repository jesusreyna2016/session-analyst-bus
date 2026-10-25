#!/usr/bin/env python3
"""Deterministic parts of the pre-asia scorecard merge, so they cannot fall behind.

Usage: python3 method/update_scorecard.py <fecha_ayer>        (pre-asia, after the state merge)
       python3 method/update_scorecard.py <fecha_ayer> --check (only verify, exit 1 if stale)

1. scorecard.execution.ALL is rebuilt from scratch from live/journal.json byDay
   (rolling 45 calendar days ending at <fecha_ayer>), never incremented by hand.
   Before this script it was hand-merged and stayed frozen at days:14 for a week.
2. scorecard.emErrorTicks is derived from scorecard.emCalibration (n-weighted meanErrTk per
   symbol), so the two can never disagree again.
3. Check: emCalibration._lastDate must be <fecha_ayer>, or reviews/<fecha_ayer>.md must say
   "sin muestra EM" with the reason. Both were silently skipped for weeks.
4. biasHitPct / scenarioAHitPct / scenarioABHitPct / zoneHitPct are rebuilt from
   scorecard.hitLog (one structured entry per graded day) on top of scorecard.hitBaseline (the
   hand-kept totals as of 2026-10-16). They were hand-merged from review prose and froze twice
   (9 days in October, then a full week). Check: hitLog["<fecha_ayer>"] must exist, or
   reviews/<fecha_ayer>.md must say "sin calificacion de aciertos" with the reason.
"""
import datetime as dt
import io
import json
import sys

STATE = "state/sa-state.json"
WINDOW_DAYS = 45
HIT_KEYS = {"biasHitPct": "bias", "scenarioAHitPct": "scenA", "scenarioABHitPct": "scenAB", "zoneHitPct": "zone"}
HIT_WINDOW = 60      # days of hitLog kept and summed
HIT_LOG_ONLY = 20    # once the log has this many graded days, the hand-kept baseline is dropped


def load(p):
    return json.load(io.open(p, encoding="utf-8"))


def execution(by_day, end):
    start = (dt.date.fromisoformat(end) - dt.timedelta(days=WINDOW_DAYS - 1)).isoformat()
    days = [d for d in by_day if start <= d.get("date", "") <= end]
    if not days:
        return None
    s = lambda k: sum(int(d.get(k) or 0) for d in days)
    pos = s("positions")
    flags = {k: sum(1 for d in days if d.get(k)) for k in ("overtrade", "revenge", "roundTrip")}
    return {
        "days": len(days), "n": s("trades"), "graded": s("graded"),
        "withBias": s("withBias"), "againstBias": s("againstBias"),
        "validEdge": s("validEdge"), "outsideEdge": s("outsideEdge"),
        "disciplinedPct": round(100 * sum(1 for d in days if d.get("disciplined")) / len(days)),
        "positions": pos,
        "partialRate": round(s("partials") / pos, 3) if pos else None,
        "scratchRate": round(s("scratches") / pos, 3) if pos else None,
        "fullStopRate": round(s("fullStops") / pos, 3) if pos else None,
        "overtradeDays": flags["overtrade"], "revengeDays": flags["revenge"], "roundTripDays": flags["roundTrip"],
        "firstDate": days[0]["date"], "lastDate": days[-1]["date"],
        "note": "Rebuilt by method/update_scorecard.py from live/journal.json byDay (%d-day window). Account-level, the journal does not split by instrument." % WINDOW_DAYS,
    }


def em_error_ticks(cal, end):
    out = {}
    for key, c in cal.items():
        if "|" not in key or not isinstance(c, dict) or not c.get("n"):
            continue
        sym = key.split("|")[0]
        o = out.setdefault(sym, {"n": 0, "_w": 0.0})
        o["n"] += int(c["n"])
        o["_w"] += float(c.get("meanErrTk") or 0) * int(c["n"])
    for sym, o in out.items():
        o["avgTk"] = round(o.pop("_w") / o["n"], 1) if o["n"] else None
        o["window"] = "derived from emCalibration (all sessions, n-weighted), as of %s" % end
    return out


def hit_counters(sc, end):
    """Rebuild the four hit counters from hitLog (+ baseline while the log is short). Prunes the log."""
    log = sc.setdefault("hitLog", {})
    start = (dt.date.fromisoformat(end) - dt.timedelta(days=HIT_WINDOW - 1)).isoformat()
    for d in [d for d in log if d < start]:
        del log[d]
    days = sorted(d for d in log if d <= end)
    base = sc.get("hitBaseline") or {}
    use_base = len(days) < HIT_LOG_ONLY and base
    for counter, k in HIT_KEYS.items():
        tot = {}
        if use_base:
            for sym, c in (base.get(counter) or {}).items():
                tot[sym] = [float(c.get("hits") or 0), int(c.get("n") or 0)]
        for d in days:
            for sym, g in log[d].items():
                if not isinstance(g, dict) or not g.get(k):
                    continue
                h, n = g[k]
                t = tot.setdefault(sym, [0.0, 0])
                t[0] += float(h)
                t[1] += int(n)
        win = ("baseline %s + hitLog %d days to %s" % (base.get("asOf"), len(days), end)) if use_base \
            else "hitLog %d graded days to %s" % (len(days), end)
        sc[counter] = {sym: {"n": n, "hits": round(h, 2), "pct": round(100 * h / n) if n else None, "window": win}
                       for sym, (h, n) in sorted(tot.items())}


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    end, check_only = sys.argv[1], "--check" in sys.argv
    state = load(STATE)
    sc = state.setdefault("scorecard", {})
    errs = []

    try:
        by_day = sorted(load("live/journal.json").get("byDay") or [], key=lambda d: d.get("date", ""))
    except FileNotFoundError:
        by_day = []
    ex = execution(by_day, end)
    cur = (sc.get("execution") or {}).get("ALL") or {}
    if check_only:
        if ex and cur.get("lastDate") != ex["lastDate"]:
            errs.append("scorecard.execution.ALL.lastDate=%s but journal has %s: run python3 method/update_scorecard.py %s" % (cur.get("lastDate"), ex["lastDate"], end))
    elif ex:
        sc.setdefault("execution", {})["ALL"] = ex

    cal = sc.get("emCalibration") or {}
    if not check_only:
        sc["emErrorTicks"] = em_error_ticks(cal, end)
    if cal.get("_lastDate") != end:
        try:
            rv = io.open("reviews/%s.md" % end, encoding="utf-8").read().lower()
        except FileNotFoundError:
            rv = ""
        if "sin muestra em" not in rv:
            errs.append('emCalibration._lastDate=%s, expected %s: add the EM samples of %s to emCalibration (section "Calibracion") and set _lastDate, or write "sin muestra EM: <motivo>" in reviews/%s.md' % (cal.get("_lastDate"), end, end, end))

    if not check_only:
        hit_counters(sc, end)
    if end not in (sc.get("hitLog") or {}):
        try:
            rv = io.open("reviews/%s.md" % end, encoding="utf-8").read().lower()
        except FileNotFoundError:
            rv = ""
        if "sin calificacion de aciertos" not in rv and "sin calificación de aciertos" not in rv:
            errs.append('scorecard.hitLog["%s"] missing: add the day\'s bias/scenario/zone grades per symbol (section "Calibracion", hitLog), or write "sin calificacion de aciertos: <motivo>" in reviews/%s.md' % (end, end))

    if not check_only:
        io.open(STATE, "w", encoding="utf-8", newline="\n").write(json.dumps(state, ensure_ascii=False, indent=1))
        if ex:
            print("execution.ALL: %d days to %s, disciplined %d%%" % (ex["days"], ex["lastDate"], ex["disciplinedPct"]))
    if errs:
        print("FAIL\n- " + "\n- ".join(errs))
        return 1
    print("OK scorecard")
    return 0


if __name__ == "__main__":
    sys.exit(main())
