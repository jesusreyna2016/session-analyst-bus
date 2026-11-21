#!/usr/bin/env python3
"""Aggregate state.zones leaves (<sym>|<sesion>|<tipo>) into the pure-archetype level (<tipo>).

The weekly (section 6.1) needs the raw winRate per archetype to decide `overrides.zonePriors`
(+-0.05 when |winRate - prior| > 0.10 with winN >= 30). state.zones only stores the leaves, so
this script sums them: reachedEff / respectedEff = live + 0.5 * seed (same rule as section 4).

Usage: python3 method/zone_type_rates.py            # JSON on stdout
Python 3.11 stdlib only. Read-only: it never writes state.
"""
import json
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    s = json.load(open(os.path.join(ROOT, "state", "sa-state.json"), encoding="utf-8"))
    zones = s.get("zones") or {}
    priors = (s.get("overrides") or {}).get("zonePriors") or {}
    acc = defaultdict(lambda: {"reachedEff": 0.0, "respectedEff": 0.0, "reachedLive": 0, "respectedLive": 0, "leaves": 0})
    for key, v in zones.items():
        parts = key.split("|")
        if len(parts) != 3 or not isinstance(v, dict):
            continue
        seed = v.get("seed") or {}
        a = acc[parts[2]]
        a["reachedEff"] += float(v.get("reached") or 0) + 0.5 * float(seed.get("reached") or 0)
        a["respectedEff"] += float(v.get("respected") or 0) + 0.5 * float(seed.get("respected") or 0)
        a["reachedLive"] += int(v.get("reached") or 0)
        a["respectedLive"] += int(v.get("respected") or 0)
        a["leaves"] += 1
    out = {}
    for t, a in sorted(acc.items(), key=lambda kv: -kv[1]["reachedEff"]):
        rate = a["respectedEff"] / a["reachedEff"] if a["reachedEff"] else None
        p = priors.get(t) or {}
        prior = p.get("value") if isinstance(p, dict) else None
        row = {"winN": round(a["reachedEff"], 1), "winRate": round(rate, 3) if rate is not None else None,
               "liveN": a["reachedLive"], "liveRate": round(a["respectedLive"] / a["reachedLive"], 3) if a["reachedLive"] else None,
               "leaves": a["leaves"], "prior": prior}
        if prior is not None and rate is not None:
            row["diverge"] = round(rate - prior, 3)
            row["actionable"] = a["reachedEff"] >= 30 and abs(rate - prior) > 0.10
        out[t] = row
    json.dump({"note": "pure-archetype winRate from state.zones leaves (live + 0.5*seed); zonePriors rule: "
                       "+-0.05 when winN >= 30 and |diverge| > 0.10 (section 6.1)", "types": out},
              sys.stdout, ensure_ascii=False, indent=1)
    print()


if __name__ == "__main__":
    main()
