#!/usr/bin/env python3
"""Scoreboard "que paga": one table of E[R] per setup across the three systems of the bus.

- Session Analyst plan zones (method/entry_study.py, real 5m bars, since the 8e rule).
- Mi Mesa zones (zones/report.json, liveEntries: executable entries on real 5m bars).
- Scalp CC (../scalp-cc-bus/report.json, net of costs; skipped if that checkout is missing).

Writes zones/scoreboard.json = {generatedAt, rows:[{system, setup, entry, exit, n, expR, winRate,
costs, asOf, note}]} and prints it as a table. Every number comes from those files; nothing is typed.
Usage: python3 method/scoreboard.py   (from the repo root or anywhere)
Python 3.11 stdlib only.
"""
import datetime as dt
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SINCE_8E = "2026-10-31"
MIN_N = 20


def load(p, default=None):
    try:
        return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        return default


def row(system, setup, entry, exit_, n, expR, wr, costs, asof, note=""):
    return {"system": system, "setup": setup, "entry": entry, "exit": exit_, "n": int(n),
            "expR": None if expR is None else round(float(expR), 3),
            "winRate": None if wr is None else round(float(wr), 3),
            "costs": costs, "asOf": asof, "note": note}


def sa_rows():
    out_path = "/tmp/_entry_study.json"
    subprocess.run([sys.executable, os.path.join(ROOT, "method", "entry_study.py"), "--since", SINCE_8E,
                    "--json", out_path], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    d = load(out_path, {})
    rows = d.get("rows") or []
    asof = max((r["date"] for r in rows), default=None)
    aplus = lambda r: r["vs24h"] == "against" and r["family"] in ("reversion", "continuation")
    groups = [("A+ del metodo (en contra de 24 h)", aplus),
              ("A+ del metodo · Asia", lambda r: aplus(r) and r["run"] == "pre-asia"),
              ("A+ del metodo · Londres", lambda r: aplus(r) and r["run"] == "pre-london"),
              ("A+ del metodo · NY", lambda r: aplus(r) and r["run"] == "pre-ny"),
              ("Resto de zonas del plan", lambda r: not aplus(r))]
    modes = [("trigger_target", "gatillo 5m", "objetivo del plan"), ("trigger_plan", "gatillo 5m", "1/2 en +1R + BE"),
             ("limit_target", "limite en la zona", "objetivo del plan")]
    out = []
    for name, f in groups:
        sel = [r for r in rows if f(r)]
        for key, ent, ex in modes:
            v = [r[key] for r in sel if r.get(key) is not None]
            if v:
                out.append(row("Session Analyst", name, ent, ex, len(v), sum(v) / len(v),
                               sum(1 for x in v if x > 0) / len(v), "bruto", asof,
                               "desde %s (regla 8e)" % SINCE_8E))
    return out


def mimesa_rows():
    r = load(os.path.join(ROOT, "zones", "report.json"), {})
    le = (r.get("liveEntries") or {})
    asof = (r.get("generatedAt") or "")[:10] or None
    names = {"limite, armadas (atraviesa)": ("limite en la entrada", "TP1 o cierre que invalida"),
             "limite, armadas, bracket stop/TP1": ("limite en la entrada", "stop/TP1 en el libro"),
             "limite, armadas, bracket + BE a +1R": ("limite en la entrada", "BE a +1R"),
             "limite, armadas, parcial 1/2 en +1R + BE": ("limite en la entrada", "1/2 en +1R + BE"),
             "gatillo (cierre de la vela de 5 min)": ("gatillo 5m", "TP1 o cierre que invalida")}
    out = []
    for key, (ent, ex) in names.items():
        s = (le.get("all") or {}).get(key)
        if s and s.get("n"):
            out.append(row("Mi Mesa", "Zonas armadas (todas)", ent, ex, s["n"], s.get("eR"), s.get("wr"), "bruto", asof))
    for g, blk in (le.get("byGrade") or {}).items():
        s = blk.get("limite, armadas, bracket stop/TP1")
        if s and s.get("n"):
            out.append(row("Mi Mesa", "Zonas armadas · grado %s" % g, "limite en la entrada", "stop/TP1 en el libro",
                           s["n"], s.get("eR"), s.get("wr"), "bruto", asof))
    return out


def scalp_rows():
    for cand in (os.path.join(ROOT, "..", "scalp-cc-bus"), os.path.join(ROOT, "..", "..", "scalp-cc-bus")):
        r = load(os.path.join(cand, "report.json"))
        if r:
            break
    else:
        return []
    asof = (r.get("generatedAt") or "")[:10] or None
    out = []
    o = r.get("expR_ci_overall") or {}
    if o.get("n"):
        out.append(row("Scalp CC", "Todas las senales", "senal del indicador", "TP1/SL del indicador", o["n"],
                       o.get("expRnet"), None, "neto (%s ticks)" % ((r.get("cost_ticks") or {}).get("default")), asof,
                       "IC90 neto %s" % o.get("ci90net")))
    segs = [(k, v) for k, v in (r.get("by_tf_kind_side") or {}).items() if (v.get("n") or 0) >= 100 and v.get("expRnet") is not None]
    for k, v in sorted(segs, key=lambda kv: -kv[1]["expRnet"]):
        out.append(row("Scalp CC", k, "senal del indicador", "TP1/SL del indicador", v["n"], v["expRnet"],
                       (v.get("wrTP1") or 0) / 100, "neto", asof))
    return out


def main():
    rows = sa_rows() + mimesa_rows() + scalp_rows()
    rows = [r for r in rows if r["n"] >= 1]
    out = {"generatedAt": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
           "minN": MIN_N, "rows": rows}
    path = os.path.join(ROOT, "zones", "scoreboard.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    for r in rows:
        flag = "" if r["n"] >= MIN_N else " ·"
        print(f"{r['system']:16s} {r['setup'][:40]:40s} {r['entry'][:20]:20s} {r['exit'][:26]:26s} "
              f"n{r['n']:<6d}{flag:2s} {('%+.2fR' % r['expR']) if r['expR'] is not None else '-':>7s} {r['costs']}")
    print(f"-> {os.path.relpath(path, ROOT)} ({len(rows)} filas)")


if __name__ == "__main__":
    main()
