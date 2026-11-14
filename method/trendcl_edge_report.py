"""Summaries for trendcl_edge.py output. Usage: python -I trendcl_edge_report.py <trades.json>"""
import json, math, random, sys
from collections import defaultdict

tr = json.load(open(sys.argv[1]))
random.seed(7)


def wilson(w, n, z=1.96):
    if n == 0: return (0, 0)
    p = w / n; d = 1 + z * z / n; c = p + z * z / (2 * n); m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - m) / d, (c + m) / d)


def stats(xs):
    n = len(xs)
    if n == 0: return "n=0"
    w = sum(x["win"] for x in xs); r = [x["R"] for x in xs]; m = sum(r) / n
    sd = math.sqrt(sum((v - m) ** 2 for v in r) / max(1, n - 1)); lo, hi = wilson(w, n)
    return f"{100*w/n:.1f}% [{100*lo:.0f}-{100*hi:.0f}] n={n} E[R]={m:+.3f}+-{1.96*sd/math.sqrt(n):.3f}"


def gap(xs):
    f = [x for x in xs if x["cat"] == "favor"]; a = [x for x in xs if x["cat"] == "against"]
    if not f or not a: return None, None
    return (sum(x["win"] for x in f) / len(f) - sum(x["win"] for x in a) / len(a),
            sum(x["R"] for x in f) / len(f) - sum(x["R"] for x in a) / len(a))


def boot(xs, fn, reps=2000):
    days = defaultdict(list)
    for x in xs: days[x["day"]].append(x)
    keys = list(days); vals = []
    for _ in range(reps):
        s = [x for k in random.choices(keys, k=len(keys)) for x in days[k]]
        v = fn(s)
        if v is not None: vals.append(v)
    vals.sort(); return vals[int(.025 * len(vals))], vals[int(.975 * len(vals))]


def did(xs, i):
    k = gap([x for x in xs if x["kind"] == "key"]); c = gap([x for x in xs if x["kind"] == "ctrl"])
    return None if None in (k[i], c[i]) else k[i] - c[i]


OOS = "2026-10-21"
for tf in (5, 15):
    T = [x for x in tr if x["tf"] == tf]
    print(f"\n===== {tf}m =====")
    for per, P in (("all", T), ("before " + OOS, [x for x in T if x["day"] < OOS]), ("from " + OOS, [x for x in T if x["day"] >= OOS])):
        print(f"-- {per}")
        for kind in ("key", "ctrl"):
            K = [x for x in P if x["kind"] == kind]
            for cat in ("favor", "against", "none"):
                print(f"  {kind:4} {cat:7} {stats([x for x in K if x['cat']==cat])}")
            g = gap(K)
            lo, hi = boot(K, lambda s: gap(s)[0]); rlo, rhi = boot(K, lambda s: gap(s)[1])
            print(f"  {kind:4} gap favor-against WR {100*g[0]:+.1f} pts [{100*lo:+.1f},{100*hi:+.1f}]  E[R] {g[1]:+.3f} [{rlo:+.3f},{rhi:+.3f}]")
        d = did(P, 0); lo, hi = boot(P, lambda s: did(s, 0))
        dr = did(P, 1); rlo, rhi = boot(P, lambda s: did(s, 1))
        print(f"  DiD key-ctrl WR {100*d:+.1f} pts [{100*lo:+.1f},{100*hi:+.1f}]  E[R] {dr:+.3f} [{rlo:+.3f},{rhi:+.3f}]")
    # shuffle control on key touches: verdict labels permuted within symbol
    K = [x for x in T if x["kind"] == "key" and x["cat"] != "none"]
    obs = gap(K)[0]; cnt = 0; reps = 1000
    by = defaultdict(list)
    for x in K: by[x["sym"]].append(x)
    for _ in range(reps):
        s = []
        for sym, xs in by.items():
            labs = [x["cat"] for x in xs]; random.shuffle(labs)
            s += [{"cat": c, "win": x["win"], "R": x["R"]} for c, x in zip(labs, xs)]
        if abs(gap(s)[0]) >= abs(obs): cnt += 1
    print(f"  shuffle test key gap {100*obs:+.1f} pts, p={cnt/reps:.3f}")
    print("-- per symbol (key | ctrl)")
    for sym in ("NQ", "ES", "GC", "YM", "CL"):
        for kind in ("key", "ctrl"):
            S = [x for x in T if x["sym"] == sym and x["kind"] == kind]
            print(f"  {sym} {kind:4} favor {stats([x for x in S if x['cat']=='favor'])} | against {stats([x for x in S if x['cat']=='against'])}")
    print("-- per symbol x session (key, n>=30 each side)")
    for sym in ("NQ", "ES", "GC", "YM", "CL"):
        for ss in ("asia", "london", "ny"):
            S = [x for x in T if x["sym"] == sym and x["kind"] == "key" and x["sess"] == ss]
            f = [x for x in S if x["cat"] == "favor"]; a = [x for x in S if x["cat"] == "against"]
            if len(f) >= 30 and len(a) >= 30:
                print(f"  {sym} {ss:6} favor {stats(f)} | against {stats(a)}")
