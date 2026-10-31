#!/usr/bin/env python3
"""Hypothesis pruning for state/sa-state.json (rule 5 and the ~20 cap of the `hypotheses` section).

Deterministic so it never depends on the model remembering it. pre-asia runs it after writing
the state and before the commit:
    python3 method/prune_hypotheses.py            # prunes in place, prints what it closed
    python3 method/prune_hypotheses.py --dry-run  # only prints

1. `abierta` with evidenceN < 3 and lastChecked more than 30 days ago -> `sin_senal`.
2. If more than MAX_OPEN stay `abierta`, the oldest by lastChecked (then lowest evidenceN) go
   to `sin_senal`, never one with evidenceN >= KEEP_EVIDENCE.
Only `status` and `note` change; the rest of the file is written back untouched.
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


def main():
    dry = "--dry-run" in sys.argv
    raw = io.open(PATH, encoding="utf-8").read()
    state = json.loads(raw)
    hyps = state.get("hypotheses") or {}
    today = dt.date.today()
    stamp = today.isoformat()
    closed = []

    def close(key, h, why):
        h["status"] = "sin_senal"
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

    for key, why in closed:
        print(f"closed {key}: {why}")
    print(f"open hypotheses: {n_open} (closed {len(closed)})")
    if closed and not dry:
        indent = 2 if raw.lstrip().startswith("{\n") else None
        out = json.dumps(state, ensure_ascii=False, indent=indent)
        io.open(PATH, "w", encoding="utf-8", newline="\n").write(out + ("\n" if raw.endswith("\n") else ""))


if __name__ == "__main__":
    main()
