#!/usr/bin/env python3
"""Gate the Session Analyst runs before commit: is the plan personalized for Jesus?

Usage: python3 method/check_plan.py [plans/latest.json]
Exit 0 = OK. Exit 1 = prints what is missing; fix the plan and run it again.
Rules come from method/instructions.md section 4.1 and state/trader-profile.json.
"""
import json
import re
import sys

PLAN = sys.argv[1] if len(sys.argv) > 1 else "plans/latest.json"


def bi_ok(x):
    return isinstance(x, dict) and bool(str(x.get("es", "")).strip()) and bool(str(x.get("en", "")).strip())


def main():
    plan = json.load(open(PLAN, encoding="utf-8"))
    try:
        prof = json.load(open("state/trader-profile.json", encoding="utf-8"))
    except FileNotFoundError:
        print("OK (no trader-profile.json, personalization skipped)")
        return 0
    if plan.get("runType") == "weekly":
        print("OK (weekly)")
        return 0

    errs = []
    rules = prof.get("dailyRules") or {}
    ids = {p.get("id") for p in prof.get("patterns", [])}

    per = plan.get("personal")
    if not isinstance(per, dict):
        errs.append('missing top-level "personal": {patternId, note:{es,en}, capLine:{es,en}}')
    else:
        if per.get("patternId") not in ids:
            errs.append(f"personal.patternId must be one of {sorted(ids)}")
        if not bi_ok(per.get("note")):
            errs.append("personal.note needs es + en (one sentence naming today's pattern)")
        cap = per.get("capLine")
        if not bi_ok(cap):
            errs.append("personal.capLine needs es + en")
        else:
            # the cap line is whatever the profile says today (account rules change):
            # dailyRules.capLineMust lists the tokens that must survive in it
            es = cap["es"].lower()
            for tok in rules.get("capLineMust") or []:
                if str(tok).lower() not in es:
                    errs.append(f'personal.capLine.es must contain "{tok}" (copy dailyRules.capLine from the profile)')

    # every GO zone: scale with 2 prices, and no BE before the partial
    for sym, ins in (plan.get("instruments") or {}).items():
        if ((ins.get("verdict") or {}).get("signal")) != "GO":
            continue
        for z in (ins.get("zones") or [])[:2]:
            scale = (z.get("play") or {}).get("scale")
            txt = scale.get("es", "") if isinstance(scale, dict) else str(scale or "")
            prices = re.findall(r"\d{2,}(?:[.,]\d+)?", txt)
            if len(prices) < 2:
                errs.append(f"{sym} GO zone {z.get('range')}: play.scale needs TP1 and TP2 prices")
            m_be, m_part = re.search(r"\bBE\b", txt), re.search(r"1/2|2/3|parcial", txt)
            if m_be and (not m_part or m_be.start() < m_part.start()):
                errs.append(f"{sym} GO zone {z.get('range')}: BE appears before the partial in play.scale")

    if errs:
        print("PERSONALIZATION CHECK FAILED:")
        for e in errs:
            print(" -", e)
        return 1
    print("OK personalization")
    return 0


if __name__ == "__main__":
    sys.exit(main())
