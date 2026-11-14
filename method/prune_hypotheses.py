#!/usr/bin/env python3
"""Hypothesis pruning for state/sa-state.json (rule 5 and the ~20 cap of the `hypotheses` section).

Deterministic so it never depends on the model remembering it. pre-asia runs it after writing
the state and before the commit:
    python3 method/prune_hypotheses.py            # prunes in place, prints what it closed
    python3 method/prune_hypotheses.py --dry-run  # only prints

1. `abierta` with evidenceN < 3 and lastChecked more than 30 days ago -> `sin_senal`.
2. If more than MAX_OPEN stay `abierta`, the oldest by lastChecked (then lowest evidenceN) go
   to `sin_senal`, never one with evidenceN >= KEEP_EVIDENCE.
3. `sin_senal` for more than DELETE_AFTER_DAYS days (since `closedAt`, else `lastChecked`) ->
   deleted from the state; one JSON line per deleted hypothesis goes to ARCHIVE.
4. `state.plans` keeps only the latest KEEP_PLANS full plans (full plans live in `plans/*.json`).
`--plans-only` runs step 4 alone (pre-london / pre-ny, which must not touch `hypotheses`).
"""
import datetime as dt
import io
import json
import sys

PATH = "state/sa-state.json"
MAX_OPEN = 20
STALE_DAYS = 30
LOW_EVIDENCE = 3
KEEP_EVIDENCE = 5
DELETE_AFTER_DAYS = 7
KEEP_PLANS = 3
ARCHIVE = "state/hypotheses-archive.jsonl"


def main():
    dry = "--dry-run" in sys.argv
    raw = io.open(PATH, encoding="utf-8").read()
    state = json.loads(raw)
    changed = trim_plans(state)
    if "--plans-only" in sys.argv:
        write(state, raw, changed and not dry)
        return
    hyps = state.get("hypotheses") or {}
    today = dt.date.today()
    stamp = today.isoformat()
    closed = []

    def close(key, h, why):
        h["status"] = "sin_senal"
        h["closedAt"] = stamp
        h["note"] = (h.get("note") or "") + f" | {stamp}: cerrada por poda ({why})."
        closed.append((key, why))

    for key, h in hyps.items():
        if h.get("status") != "abierta":
            continue
        try:
            last = dt.date.fromisoformat(str(h.get("lastChecked") or h.get("formed"))[:10])
        except ValueError:
            continue
        if (today - last).days > STALE_DAYS and int(h.get("evidenceN") or 0) < LOW_EVIDENCE:
            close(key, h, f"mas de {STALE_DAYS} dias sin ocurrencia y poca evidencia")

    still = sorted(((k, h) for k, h in hyps.items() if h.get("status") == "abierta"),
                   key=lambda kv: (str(kv[1].get("lastChecked") or ""), int(kv[1].get("evidenceN") or 0)))
    n_open = len(still)
    for key, h in still:
        if n_open <= MAX_OPEN:
            break
        if int(h.get("evidenceN") or 0) >= KEEP_EVIDENCE:
            continue
        close(key, h, f"tope de {MAX_OPEN} abiertas, la mas vieja sin senal reciente")
        n_open -= 1

    deleted = []
    just_closed = {k for k, _ in closed}
    for key, h in list(hyps.items()):
        if h.get("status") != "sin_senal" or key in just_closed:
            continue
        try:
            since = dt.date.fromisoformat(str(h.get("closedAt") or h.get("lastChecked") or h.get("formed"))[:10])
        except ValueError:
            continue
        if (today - since).days > DELETE_AFTER_DAYS:
            deleted.append({"id": key, "deletedAt": stamp, "sinSenalSince": since.isoformat(),
                            "evidenceN": h.get("evidenceN"), "hits": h.get("hits"),
                            "claim": str(h.get("claim") or "")[:200]})
            del hyps[key]

    for key, why in closed:
        print(f"closed {key}: {why}")
    for d in deleted:
        print(f"deleted {d['id']} (sin_senal since {d['sinSenalSince']})")
    print(f"open hypotheses: {n_open} (closed {len(closed)}, deleted {len(deleted)})")
    if deleted and not dry:
        with io.open(ARCHIVE, "a", encoding="utf-8", newline="\n") as fh:
            for d in deleted:
                fh.write(json.dumps(d, ensure_ascii=False) + "\n")
    write(state, raw, bool(closed or deleted or changed) and not dry)


def trim_plans(state):
    plans = state.get("plans")
    if not isinstance(plans, dict) or len(plans) <= KEEP_PLANS:
        return False
    keep = sorted(plans)[-KEEP_PLANS:]
    for k in list(plans):
        if k not in keep:
            del plans[k]
    print(f"state.plans trimmed to {keep}")
    return True


def write(state, raw, do_write):
    if not do_write:
        return
    indent = 2 if raw.lstrip().startswith("{\n") else None
    out = json.dumps(state, ensure_ascii=False, indent=indent)
    io.open(PATH, "w", encoding="utf-8", newline="\n").write(out + ("\n" if raw.endswith("\n") else ""))

if __name__ == "__main__":
    main()
