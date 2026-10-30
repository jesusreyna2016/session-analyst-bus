#!/usr/bin/env python3
"""Plan vs execution: each real position from live/journal.json (byDay[].fills, points only,
no money) checked against the plan that was live at that minute.

Usage: python3 method/plan_vs_exec.py           prints the summary
       (update_scorecard.py imports plan_fit() and stores it in scorecard.execution.planFit)

Per position:
  plan     the latest futures plan (plans/<date>-pre-*.json) with generatedAt <= entry time
           and < 12 h old, or the crypto plan (plans/crypto/*.json) whose builtAt..validUntil
           covers it. Symbol roots: NQ/MNQ -> NQ, ES/MES -> ES, GC/MGC -> GC, YM/MYM -> YM,
           CL/MCL -> CL, ETH* -> ETHUSDT, BTC* -> BTCUSDT; NDX/US100/NAS100 -> NQ by bias and
           verdict only (index vs futures basis, prices are not comparable to the zones).
  class    in-plan     entry inside a plan zone (10 % width tolerance) in the zone's direction,
                       or, without comparable prices, verdict GO and side = biasSession
           against     side against the plan's biasSession, or verdict AVOID
           off-zone    everything else (no zone at the entry price, WAIT without a zone)
           no-plan     no plan covered that minute
Totals per class: n, wins (pts > 0), winRate, avgPts by symbol root (points are per root,
never summed across roots).
"""
import datetime as dt
import glob
import io
import json
import os
import re
import sys

ROOTS = [(r"^M?NQ", "NQ"), (r"^M?ES", "ES"), (r"^M?GC", "GC"), (r"^M?YM", "YM"), (r"^M?CL", "CL"),
         (r"^ETH", "ETHUSDT"), (r"^BTC", "BTCUSDT"), (r"^(NDX|US100|NAS100|USTEC)", "NQ*")]


def load(p):
    return json.load(io.open(p, encoding="utf-8"))


def root(sym):
    s = str(sym or "").upper()
    for rx, r in ROOTS:
        if re.match(rx, s):
            return r
    return None


def ts(s):
    try:
        return dt.datetime.fromisoformat(str(s).replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


_fut, _cry = None, None


def plans():
    global _fut, _cry
    if _fut is None:
        _fut, _cry = [], []
        for f in glob.glob("plans/20??-??-??-pre-*.json"):
            try:
                p = load(f)
            except ValueError:
                continue
            t = ts(p.get("generatedAt"))
            if t:
                _fut.append((t, p))
        for f in glob.glob("plans/crypto/*.json"):
            try:
                p = load(f)
            except ValueError:
                continue
            t0, t1 = ts(p.get("builtAt")), ts(p.get("validUntil"))
            if t0:
                _cry.append((t0, t1 or t0 + 12 * 3600, p))
        _fut.sort(key=lambda x: x[0])
    return _fut, _cry


def plan_at(r, t):
    fut, cry = plans()
    if r in ("ETHUSDT", "BTCUSDT"):
        hit = [p for t0, t1, p in cry if t0 <= t <= t1]
        return hit[-1] if hit else None
    cand = [p for t0, p in fut if t0 <= t and t - t0 < 12 * 3600]
    return cand[-1] if cand else None


def classify(f):
    r = root(f.get("sym"))
    t = ts(f.get("t"))
    if not r or not t:
        return None, None
    comparable = not r.endswith("*")
    key = r.rstrip("*")
    p = plan_at(key, t)
    inst = ((p or {}).get("instruments") or {}).get(key) if p else None
    if not inst:
        return key, "no-plan"
    side = "LONG" if f.get("side") == "long" else "SHORT"
    bias = (inst.get("biasSession") or "").upper()
    verdict = (((inst.get("verdict") or {}).get("signal")) or "").upper()
    if bias in ("LONG", "SHORT") and side != bias or verdict == "AVOID":
        return key, "against"
    if comparable and f.get("entry") is not None:
        e = float(f["entry"])
        for z in inst.get("zones") or []:
            rng = z.get("range") or []
            if len(rng) != 2:
                continue
            lo, hi = sorted(float(x) for x in rng)
            pad = (hi - lo) * 0.1
            if lo - pad <= e <= hi + pad and (z.get("dir") or "").upper() == side:
                return key, "in-plan"
        return key, "off-zone"
    return key, "in-plan" if verdict == "GO" and side == bias else "off-zone"


def plan_fit(journal):
    out = {}
    n_all = 0
    for day in journal.get("byDay") or []:
        for f in day.get("fills") or []:
            key, cls = classify(f)
            if not key:
                continue
            n_all += 1
            o = out.setdefault(cls, {}).setdefault(key, {"n": 0, "wins": 0, "pts": 0.0})
            o["n"] += 1
            pts = float(f.get("pts") or 0)
            o["wins"] += pts > 0
            o["pts"] += pts
    for cls, by in out.items():
        for key, o in by.items():
            o["winRate"] = round(o["wins"] / o["n"], 3) if o["n"] else None
            o["avgPts"] = round(o.pop("pts") / o["n"], 2) if o["n"] else None
    return {"positions": n_all, "byClass": out,
            "note": "Real positions vs the plan live at that minute (method/plan_vs_exec.py). Points per symbol root, no money."}


def main():
    try:
        j = load("live/journal.json")
    except FileNotFoundError:
        print("no live/journal.json")
        return 1
    fit = plan_fit(j)
    if not fit["positions"]:
        print("no fills yet in live/journal.json (journal digest without per-position prices)")
        return 0
    for cls in ("in-plan", "off-zone", "against", "no-plan"):
        for key, o in sorted((fit["byClass"].get(cls) or {}).items()):
            print("%-9s %-8s n=%3d  win %3.0f%%  avg %+.2f pts" % (cls, key, o["n"], 100 * (o["winRate"] or 0), o["avgPts"] or 0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
