#!/usr/bin/env python3
"""Lint a Session Analyst plan against the hard rules of the method before pushing it.

Usage: python3 method/lint_plan.py plans/latest.json [more plans...]
       python3 method/lint_plan.py plans/crypto-latest.json
Exit 0 = no ERROR (WARN lines may remain: copy them to the plan's notes).
Exit 1 = one line per violation: "ERROR <instrument>/<zone>: <rule>". Fix the plan
(downgrade GO to WAIT, conviction to "baja", fill the field) and run it again.

Only rules the method states without ambiguity are ERROR:
- instructions.md 8e / 8f (A+ del metodo, caps per zone type, conviction "alta" / "baja"),
  section 9 (GO conditions), section 2 (tcl "contra" = cap B only for plans before 2026-11-14), section 4
  (zone fields, risk flags, rr >= 1.5 for GO), reachability.md (no GO on a WATCH / STRETCHED zone).
- crypto.md sections 1, 3, 5, 6 (same 8e hierarchy, grade field, stop / tp1 / tp2 on GO zones).
Soft issues (numbers that look off, text the script can only parse loosely) are WARN.
Python 3.11 standard library only.
"""
import json
import re
import sys

REVERSION = {"fade_vah", "fade_val", "poc_reversion", "bounce_val", "bounce_vah", "ib_fade"}
CONTINUATION = {"pullback_cont", "retest_break", "poc_breakout", "ib_break", "asia_range_break"}
SWEEP_PREFIX = "sweep_"
ZONE_TYPES = REVERSION | CONTINUATION | {
    "sweep_pdh", "sweep_pdl", "sweep_pwh", "sweep_pwl", "sweep_asiaH", "sweep_asiaL",
    "sweep_onh", "sweep_onl", "liq_reclaim", "golden_zone", "supply", "demand", "ext_target", "otro"}
BIAS = {"LONG", "SHORT", "NEUTRAL"}
DIRS = {"LONG", "SHORT"}
SIGNALS = {"GO", "WAIT", "AVOID"}
CONVICTION = {"alta", "baja"}
VS24H = {"with", "against", "flat"}
TCL = {"favor", "contra", None}
WIN_SOURCE = {"leaf", "symType", "type"}
ROLES = {"tactical", "watch", "strategic", None}
FLAGS = {"OK", "AJUSTADO", "FLOJO", "STOP_ANCHO", "OBJETIVO_BLOQUEADO", "RR_SOSPECHOSO"}
BAD_FLAGS = {"FLOJO", "STOP_ANCHO", "OBJETIVO_BLOQUEADO", "RR_SOSPECHOSO"}
GRADES = {"A+", "B"}

FUT_INSTR_FIELDS = ["biasDay", "biasSession", "conviction", "verdict", "frameConflict",
                    "whipsawRisk", "counterCase", "predictions", "zones", "invalidation", "move24h"]
FUT_ZONE_FIELDS = ["range", "dir", "type", "vs24h", "confluence", "winRate", "winSource",
                   "winN", "tcl", "fvg", "risk", "play"]
CRY_INSTR_FIELDS = ["biasDay", "biasSession", "conviction", "verdict", "counterCase",
                    "predictions", "zones", "move24h"]
CRY_ZONE_FIELDS = ["range", "dir", "type", "confluence", "grade", "tcl", "vs24h", "play"]

out = []
# 8e change of 2026-11-14 (commit a59b68d0): continuation against = A+, golden_zone capped at B.
# Plans dated before it are linted with the old hierarchy so old plans can be re-checked.
RULE_CHANGE = "2026-11-14"
ctx = {"old": False}


def err(sym, zone, msg):
    out.append(("ERROR", f"ERROR {sym}/{zone}: {msg}"))


def warn(sym, zone, msg):
    out.append(("WARN", f"WARN {sym}/{zone}: {msg}"))


def num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def text_es(x):
    if isinstance(x, dict):
        return str(x.get("es") or x.get("en") or "")
    return str(x or "")


def prices_in(txt):
    return [float(p.replace(",", "")) for p in re.findall(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d{3,}(?:\.\d+)?", txt)]


def zlabel(z, i):
    r = z.get("range")
    if isinstance(r, list) and len(r) == 2 and all(num(v) for v in r):
        return f"{z.get('type', '?')}@{r[0]:g}-{r[1]:g}"
    return f"{z.get('type', '?')}#{i}"


def expected_vs24h(zdir, m24):
    d = (m24 or {}).get("dir") if isinstance(m24, dict) else None
    if d not in DIRS:
        return "flat"
    return "with" if zdir == d else "against"


def method_aplus(z):
    """A+ del metodo (8e, cambio 2026-11-14): reversion or continuation against the 24h move,
    never golden_zone / sweeps / liq_reclaim. Against the Trend Checklist capped it only before
    2026-11-14 (rule retired after the controlled re-test)."""
    t = z.get("type")
    if z.get("vs24h") != "against":
        return False, f"vs24h={z.get('vs24h')}"
    if ctx["old"]:
        if t in CONTINUATION:
            return False, "continuation capped at B before 2026-11-14"
        if t == "golden_zone":
            return (z.get("tcl") != "contra"), ""
    if t not in REVERSION | CONTINUATION:
        return False, f"type {t} is capped at B"
    if z.get("tcl") == "contra" and ctx["old"]:
        return False, "tcl contra (cap B)"
    return True, ""


def cap_reason(z):
    t = z.get("type") or ""
    if t.startswith(SWEEP_PREFIX) or t == "liq_reclaim":
        return "sweeps / liq_reclaim are capped at B and never GO (8e)"
    if t == "golden_zone" and not ctx["old"]:
        return "golden_zone is capped at B (8e, 2026-11-14)"
    if t in CONTINUATION and ctx["old"]:
        return "continuation is capped at B (8e before 2026-11-14)"
    if t in CONTINUATION and z.get("vs24h") in ("with", "flat"):
        return f"continuation {z.get('vs24h')} the 24h move is capped at B, never GO (8e)"
    if t in REVERSION and z.get("vs24h") in ("with", "flat"):
        return f"reversion {z.get('vs24h')} the 24h move is capped at B (8e)"
    if z.get("tcl") == "contra" and ctx["old"]:
        return "zone against the Trend Checklist is capped at B, never GO (section 2, before 2026-11-14)"
    if z.get("vs24h") != "against":
        return f"A+ needs vs24h against (has {z.get('vs24h')})"
    return f"type {t} is not A+ of the method (8e)"


def check_enums_zone(sym, zl, z, crypto):
    if z.get("dir") not in DIRS:
        err(sym, zl, f"dir must be LONG|SHORT (has {z.get('dir')!r})")
    if z.get("type") not in ZONE_TYPES:
        err(sym, zl, f"type {z.get('type')!r} is not a section 4 zone type")
    if "vs24h" in z and z.get("vs24h") not in VS24H:
        err(sym, zl, f"vs24h must be with|against|flat (has {z.get('vs24h')!r})")
    if "tcl" in z and z.get("tcl") not in TCL:
        err(sym, zl, f"tcl must be favor|contra|null (has {z.get('tcl')!r})")
    r = z.get("range")
    if not (isinstance(r, list) and len(r) == 2 and all(num(v) for v in r)):
        err(sym, zl, "range must be [lo, hi] numbers")
    elif r[0] > r[1]:
        err(sym, zl, f"range lo > hi ({r[0]} > {r[1]})")
    if crypto:
        if "grade" in z and z.get("grade") not in GRADES:
            err(sym, zl, f"grade must be A+|B (has {z.get('grade')!r})")
    else:
        if "winRate" in z and not (num(z["winRate"]) and 0 <= z["winRate"] <= 1):
            err(sym, zl, f"winRate must be a number in [0,1], never null (has {z.get('winRate')!r})")
        if "winSource" in z and z.get("winSource") not in WIN_SOURCE:
            err(sym, zl, f"winSource must be leaf|symType|type (has {z.get('winSource')!r})")
        if z.get("role") not in ROLES:
            err(sym, zl, f"role must be tactical|watch|strategic (has {z.get('role')!r})")
        if "fvg" in z and not isinstance(z.get("fvg"), list):
            err(sym, zl, "fvg must be a list ([] if none)")


def check_vs24h(sym, zl, z, m24, soft=False):
    if z.get("dir") in DIRS and z.get("vs24h") in VS24H:
        exp = expected_vs24h(z["dir"], m24)
        if z["vs24h"] != exp:
            # crypto-ny re-runs move24h but leaves the zones of the close intact (crypto.md 7)
            (warn if soft else err)(sym, zl, f"vs24h={z['vs24h']} but zone {z['dir']} vs move24h {((m24 or {}).get('dir') if isinstance(m24, dict) else None)} is {exp} (8e)")


def check_risk(sym, zl, z, aplus):
    risk = z.get("risk")
    if not isinstance(risk, dict):
        return
    sp, tp, rr = risk.get("stopPts"), risk.get("tgtPts"), risk.get("rr")
    if not (num(sp) and sp > 0):
        err(sym, zl, f"risk.stopPts must be > 0 (has {sp!r})")
    if not (num(tp) and tp > 0):
        err(sym, zl, f"risk.tgtPts must be > 0 (has {tp!r})")
    if not num(rr):
        err(sym, zl, f"risk.rr must be a number (has {rr!r})")
    elif num(sp) and num(tp) and sp > 0 and abs(rr - tp / sp) > max(0.15, 0.06 * rr):
        warn(sym, zl, f"risk.rr {rr} does not match tgtPts/stopPts = {tp / sp:.2f}")
    flag = risk.get("flag")
    if flag not in FLAGS:
        err(sym, zl, f"risk.flag must be one of {sorted(FLAGS)} (has {flag!r})")
    elif num(rr) and rr >= 3.5 and not aplus and flag != "RR_SOSPECHOSO":
        err(sym, zl, f"rr {rr} >= 3.5 on a zone that is not A+ of the method needs flag RR_SOSPECHOSO (8f)")
    elif flag == "RR_SOSPECHOSO" and aplus:
        warn(sym, zl, "RR_SOSPECHOSO on an A+ of the method (8f: high rr on an A+ is fine)")
    elif num(rr) and rr < 1.3 and flag == "OK":
        warn(sym, zl, f"rr {rr} < 1.3 should be FLOJO, flag says OK")


def check_play_numbers(sym, zl, z):
    """Loose text checks on futures play: structStop beyond the zone, first target beyond entry."""
    r, d, play = z.get("range"), z.get("dir"), z.get("play")
    if not (isinstance(play, dict) and isinstance(r, list) and len(r) == 2 and all(num(v) for v in r) and d in DIRS):
        return
    lo, hi = r
    width = max(hi - lo, 1e-9)
    stop = prices_in(text_es(play.get("structStop")))
    if stop:
        s = stop[0]
        if (d == "LONG" and s > hi) or (d == "SHORT" and s < lo):
            warn(sym, zl, f"play.structStop {s:g} is on the wrong side of a {d} zone {lo:g}-{hi:g}")
    tps = [p for p in prices_in(text_es(play.get("scale"))) if abs(p - (lo + hi) / 2) < 50 * width + 0.2 * hi]
    if tps:
        t = tps[0]
        if (d == "LONG" and t <= lo) or (d == "SHORT" and t >= hi):
            warn(sym, zl, f"first play.scale target {t:g} is not beyond the entry of a {d} zone {lo:g}-{hi:g}")


def lint_futures(plan):
    if plan.get("runType") == "weekly":
        return
    for f in ["date", "runType", "schema", "focus", "instruments"]:
        if f not in plan:
            err("plan", "-", f"missing top-level field {f}")
    zoneA = {}
    for a in plan.get("alertLevels") or []:
        if isinstance(a, dict) and a.get("kind") == "zoneA" and isinstance(a.get("band"), list):
            zoneA.setdefault(a.get("sym"), []).append(a["band"])
    for sym, ins in (plan.get("instruments") or {}).items():
        if not isinstance(ins, dict):
            err(sym, "-", "instrument is not an object")
            continue
        for f in FUT_INSTR_FIELDS:
            if f not in ins:
                err(sym, "-", f"missing field {f}")
        verdict = ins.get("verdict") or {}
        sig = verdict.get("signal")
        conv = ins.get("conviction")
        if sig not in SIGNALS:
            err(sym, "-", f"verdict.signal must be GO|WAIT|AVOID (has {sig!r})")
        if conv not in CONVICTION:
            err(sym, "-", f"conviction must be alta|baja (has {conv!r}; 'media' is retired, 8e)")
        for f in ("biasDay", "biasSession"):
            if f in ins and ins[f] not in BIAS:
                err(sym, "-", f"{f} must be LONG|SHORT|NEUTRAL (has {ins[f]!r})")
        fc = ins.get("frameConflict") if isinstance(ins.get("frameConflict"), dict) else {}
        ws = ins.get("whipsawRisk") if isinstance(ins.get("whipsawRisk"), dict) else {}
        if "frameConflict" in ins and not isinstance(fc.get("on"), bool):
            err(sym, "-", "frameConflict.on must be true|false")
        wscore = ws.get("score")
        if "whipsawRisk" in ins and not num(wscore):
            err(sym, "-", "whipsawRisk.score must be a number")
        if not ins.get("counterCase"):
            err(sym, "-", "counterCase is empty (section 3)")
        if "predictions" in ins and not ins.get("predictions"):
            err(sym, "-", "predictions is empty (section 3)")
        m24 = ins.get("move24h")
        zones = ins.get("zones") if isinstance(ins.get("zones"), list) else []
        verdicts = []
        for i, z in enumerate(zones):
            zl = zlabel(z, i)
            for f in FUT_ZONE_FIELDS:
                if f not in z:
                    err(sym, zl, f"missing zone field {f}")
            check_enums_zone(sym, zl, z, crypto=False)
            check_vs24h(sym, zl, z, m24)
            ok, _ = method_aplus(z)
            verdicts.append(ok)
            check_risk(sym, zl, z, ok)
            check_play_numbers(sym, zl, z)
        # section 7 (2026-11-14): kind zoneA is the alert of any zone of the table, A+ or B,
        # but it must point at a zone of this plan (never tierra de nadie or a stale zone)
        ranges = [z.get("range") for z in zones]
        for band in zoneA.get(sym, []):
            if band not in ranges:
                warn(sym, "-", f"alertLevels zoneA band {band} matches no zone of the plan (section 7)")
        # conviction "alta" (8e): the focus zone (zones[0]) is A+ of the method, no frame conflict,
        # whipsaw < 0.6
        z0 = zones[0] if zones else None
        z0l = zlabel(z0, 0) if z0 else "-"
        if conv == "alta":
            if not z0:
                err(sym, "-", 'conviction "alta" without zones (8e)')
            elif not verdicts[0]:
                err(sym, z0l, f'conviction "alta" needs zones[0] A+ of the method, but {cap_reason(z0)}')
            if fc.get("on") is True:
                err(sym, "-", 'conviction "alta" with frameConflict.on (8e)')
            if num(wscore) and wscore >= 0.6:
                err(sym, "-", f'conviction "alta" with whipsawRisk {wscore} >= 0.6 (8e)')
        if sig == "GO":
            if conv != "alta":
                err(sym, "-", f'GO needs conviction "alta" (has {conv!r}) (8e, section 9)')
            if fc.get("on") is True:
                err(sym, "-", "GO with frameConflict.on: verdict must be WAIT or AVOID (section 9)")
            if num(wscore) and wscore >= 0.6:
                err(sym, "-", f"GO with whipsawRisk {wscore} >= 0.6 (section 9)")
            if not z0:
                err(sym, "-", "GO without zones")
            else:
                if not verdicts[0]:
                    err(sym, z0l, f"GO on a zone that is not A+ of the method: {cap_reason(z0)}")
                risk = z0.get("risk") or {}
                if num(risk.get("rr")) and risk["rr"] < 1.5:
                    err(sym, z0l, f"GO with risk.rr {risk['rr']} < 1.5 (section 4)")
                if risk.get("flag") in BAD_FLAGS:
                    err(sym, z0l, f"GO with risk.flag {risk.get('flag')} (section 4, 9)")
                rc = (z0.get("reach") or {}).get("class") if isinstance(z0.get("reach"), dict) else None
                if z0.get("role") == "watch" or rc in ("WATCH", "STRETCHED"):
                    err(sym, z0l, f"GO on a zone out of reach (role {z0.get('role')}, reach {rc}) (reachability.md)")
                if ins.get("biasSession") in DIRS and z0.get("dir") in DIRS and z0["dir"] != ins["biasSession"]:
                    warn(sym, z0l, f"GO zone {z0['dir']} against biasSession {ins['biasSession']}")
    focus = plan.get("focus") or {}
    fsym, fsig = focus.get("sym"), focus.get("verdict")
    if fsig is not None and fsig not in SIGNALS:
        err("focus", "-", f"focus.verdict must be GO|WAIT|AVOID (has {fsig!r})")
    ins = (plan.get("instruments") or {}).get(fsym) if fsym else None
    if fsig == "GO" and isinstance(ins, dict) and (ins.get("verdict") or {}).get("signal") != "GO":
        err("focus", "-", f"focus.verdict GO but {fsym} verdict is {(ins.get('verdict') or {}).get('signal')}")
    if isinstance(ins, dict) and text_es(focus.get("setup")).lstrip().startswith("A+"):
        zones = ins.get("zones") or []
        if zones and not method_aplus(zones[0])[0]:
            err("focus", zlabel(zones[0], 0), f"focus.setup says A+ but {cap_reason(zones[0])}")


def lint_crypto(plan):
    for f in ["date", "runType", "schema", "focus", "instruments", "personal"]:
        if f not in plan:
            err("plan", "-", f"missing top-level field {f}")
    for sym, ins in (plan.get("instruments") or {}).items():
        if not isinstance(ins, dict):
            err(sym, "-", "instrument is not an object")
            continue
        for f in CRY_INSTR_FIELDS:
            if f not in ins:
                err(sym, "-", f"missing field {f}")
        sig = (ins.get("verdict") or {}).get("signal")
        conv = ins.get("conviction")
        if sig not in SIGNALS:
            err(sym, "-", f"verdict.signal must be GO|WAIT|AVOID (has {sig!r})")
        if conv not in CONVICTION:
            err(sym, "-", f"conviction must be alta|baja (has {conv!r})")
        for f in ("biasDay", "biasSession"):
            if f in ins and ins[f] not in BIAS:
                err(sym, "-", f"{f} must be LONG|SHORT|NEUTRAL (has {ins[f]!r})")
        m24 = ins.get("move24h")
        zones = ins.get("zones") if isinstance(ins.get("zones"), list) else []
        aplus_live = []
        for i, z in enumerate(zones):
            zl = zlabel(z, i)
            for f in CRY_ZONE_FIELDS:
                if f not in z:
                    err(sym, zl, f"missing zone field {f}")
            check_enums_zone(sym, zl, z, crypto=True)
            check_vs24h(sym, zl, z, m24, soft=plan.get("runType") == "crypto-ny")
            ok, _ = method_aplus(z)
            if z.get("grade") == "A+" and not ok:
                err(sym, zl, f"grade A+ but {cap_reason(z)}")
            if z.get("grade") == "A+" and ok and not z.get("broken"):
                aplus_live.append(z)
        if conv == "alta" and not aplus_live:
            err(sym, "-", 'conviction "alta" needs a live zone A+ of the method (8e)')
        if sig == "GO":
            if conv != "alta":
                err(sym, "-", f'GO needs conviction "alta" (has {conv!r}) (8e)')
            if not aplus_live:
                err(sym, "-", "GO without a live zone A+ of the method (8e, crypto.md 5)")
            if plan.get("riskWindow"):
                warn(sym, "-", "GO while riskWindow is set: check it is not in progress (crypto.md 5)")
            for z in aplus_live:
                zl = zlabel(z, zones.index(z))
                play = z.get("play") or {}
                st, t1, t2 = play.get("stop"), play.get("tp1"), play.get("tp2")
                if not all(num(v) for v in (st, t1, t2)):
                    err(sym, zl, "GO zone needs play.stop, play.tp1 and play.tp2 as prices (crypto.md 3)")
                    continue
                lo, hi = z["range"]
                if z["dir"] == "LONG" and not (st < lo and t1 > hi and t2 >= t1):
                    err(sym, zl, f"LONG numbers off: stop {st} < {lo} < {hi} < tp1 {t1} <= tp2 {t2} expected")
                if z["dir"] == "SHORT" and not (st > hi and t1 < lo and t2 <= t1):
                    err(sym, zl, f"SHORT numbers off: stop {st} > {hi} > {lo} > tp1 {t1} >= tp2 {t2} expected")
                if not num(play.get("maxNotionalUsd")):
                    err(sym, zl, "GO zone needs play.maxNotionalUsd (crypto.md 3)")
                if ins.get("biasSession") in DIRS and z["dir"] != ins["biasSession"]:
                    warn(sym, zl, f"GO zone {z['dir']} against biasSession {ins['biasSession']} (crypto.md 5)")
        # numbers on every zone with a stop / targets
        for i, z in enumerate(zones):
            play = z.get("play") or {}
            st, t1 = play.get("stop"), play.get("tp1")
            r = z.get("range")
            if num(st) and num(t1) and isinstance(r, list) and len(r) == 2 and all(num(v) for v in r):
                lo, hi = r
                if (z.get("dir") == "LONG" and (st >= hi or t1 <= lo)) or (z.get("dir") == "SHORT" and (st <= lo or t1 >= hi)):
                    warn(sym, zlabel(z, i), f"{z.get('dir')} stop {st} / tp1 {t1} on the wrong side of {lo}-{hi}")


def lint(path):
    out.clear()
    try:
        plan = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError) as e:
        err("plan", "-", f"cannot read JSON: {e}")
        return list(out)
    ctx["old"] = str(plan.get("date", "9999")) < RULE_CHANGE
    crypto = str(plan.get("schema", "")).startswith("crypto") or str(plan.get("runType", "")).startswith("crypto")
    (lint_crypto if crypto else lint_futures)(plan)
    return list(out)


def main():
    paths = sys.argv[1:] or ["plans/latest.json"]
    bad = False
    for p in paths:
        res = lint(p)
        if len(paths) > 1:
            print(f"== {p}")
        for _, line in res:
            print(line)
        n_err = sum(1 for k, _ in res if k == "ERROR")
        n_warn = len(res) - n_err
        bad = bad or n_err > 0
        if len(paths) == 1 or res:
            print(f"{'FAIL' if n_err else 'OK'} lint: {n_err} error(s), {n_warn} warning(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
