#!/usr/bin/env python3
"""Check that every scheduled routine of the bus pushed its commit.

Reads `git log origin/main` and, for each expected run (slot) of each routine in
the lookback window, reports:
  present    one matching commit near the slot
  duplicated more than one matching commit for the same slot (info only)
  missing    no commit and the slot's grace time already passed
  pending    no commit yet, but still inside the grace time

Usage (from the repo root, after `git pull`):
  python3 method/check_pushes.py                 # last 26 h
  python3 method/check_pushes.py --hours 168     # last week
  python3 method/check_pushes.py --now 2026-11-13T12:00:00Z --hours 144

Output: one JSON object on stdout. Python 3.11 stdlib only.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone, tzinfo

try:
    from zoneinfo import ZoneInfo
    CT = ZoneInfo("America/Chicago")
except Exception:  # no tz database: US Central rule by hand
    class _Central(tzinfo):
        def _dst(self, dt):
            y = dt.year
            mar = datetime(y, 3, 8) + timedelta(days=(6 - datetime(y, 3, 8).weekday()) % 7)
            nov = datetime(y, 11, 1) + timedelta(days=(6 - datetime(y, 11, 1).weekday()) % 7)
            naive = dt.replace(tzinfo=None)
            return mar.replace(hour=2) <= naive < nov.replace(hour=2)
        def utcoffset(self, dt):
            return timedelta(hours=-5 if self._dst(dt) else -6)
        def dst(self, dt):
            return timedelta(hours=1 if self._dst(dt) else 0)
        def tzname(self, dt):
            return "CDT" if self._dst(dt) else "CST"
    CT = _Central()

UTC = timezone.utc
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALL = {0, 1, 2, 3, 4, 5, 6}          # Monday = 0
MON_FRI = {0, 1, 2, 3, 4}
SUN_FRI = {6, 0, 1, 2, 3, 4}         # no futures routine on Saturday
REFRESH = re.compile(r"re-check|re-disparo|catch-up", re.I)

# tz: zone of the cron time and of the slot date. grace: minutes after the slot
# before a missing commit counts as missing. before / after: minutes around the
# slot where a commit is accepted (catch-ups land up to ~2 h late).
# plan: path of the file the run must leave, from the slot date (None = no plan).
# The 16:00-17:00 CT futures break needs no rule: pre-asia (16:05) is meant to run in it,
# and nothing else is scheduled there.
ROUTINES = [
    dict(name="pre-asia", pat=r"^sa pre-asia\b", tz=CT, times=["16:05"], days=SUN_FRI,
         grace=90, before=90, after=300,
         plan=lambda d: f"plans/{d + timedelta(days=1)}-pre-asia.json"),
    dict(name="pre-london", pat=r"^sa pre-london\b", tz=CT, times=["01:25"], days=MON_FRI,
         grace=90, before=90, after=300, plan=lambda d: f"plans/{d}-pre-london.json"),
    dict(name="pre-ny", pat=r"^sa pre-ny\b", tz=CT, times=["07:55"], days=MON_FRI,
         grace=90, before=90, after=300, plan=lambda d: f"plans/{d}-pre-ny.json"),
    dict(name="crypto-close", pat=r"^sa crypto-close\b", tz=UTC, times=["00:15"], days=ALL,
         grace=150, before=60, after=360, plan=lambda d: f"plans/crypto/{d}-close.json"),
    dict(name="crypto-ny", pat=r"^sa crypto-ny\b", tz=CT, times=["08:45"], days=ALL,
         grace=90, before=60, after=300,
         plan=lambda d: f"plans/crypto/{d}-ny.json"),  # 08:45 CT is the same UTC date
    dict(name="weekly", pat=r"^sa weekly\b", tz=CT, times=["10:00"], days={5},
         grace=120, before=60, after=480, plan=None),
    dict(name="watchdog", pat=r"^watchdog\b", tz=CT,
         times=["02:30", "09:30", "17:30", "20:30"], days=ALL,
         grace=60, before=30, after=150, plan=None),
    dict(name="zones-agent", pat=r"^zones agent\b", tz=CT, times=["20:33"], days=ALL,
         grace=120, before=60, after=360, plan=None, since="2026-11-08"),
]
PLAN_ROUTINES = {"pre-asia", "pre-london", "pre-ny", "crypto-close", "crypto-ny"}


def parse_now(s):
    if not s:
        return datetime.now(UTC)
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(UTC)


def git_commits(since, until):
    out = subprocess.run(
        ["git", "-C", ROOT, "log", "origin/main",
         f"--since=@{int(since.timestamp())}", f"--until=@{int(until.timestamp())}",
         "--format=%aI%x09%s"],
        capture_output=True, text=True, check=True).stdout
    commits = []
    for line in out.splitlines():
        at, _, msg = line.partition("\t")
        if at:
            commits.append((datetime.fromisoformat(at).astimezone(UTC), msg))
    return commits


def slots(r, start, end):
    """Expected runs of routine r with time in (start, end]."""
    tz = r["tz"]
    d = start.astimezone(tz).date() - timedelta(days=1)
    last = end.astimezone(tz).date()
    active = date.fromisoformat(r["since"]) if r.get("since") else date.min
    while d <= last:
        if d.weekday() in r["days"] and d >= active:
            for hm in r["times"]:
                h, m = map(int, hm.split(":"))
                at = datetime(d.year, d.month, d.day, h, m, tzinfo=tz).astimezone(UTC)
                if start < at <= end:
                    yield d, at
        d += timedelta(days=1)


def dst_extra(at):
    """60 min more grace in the week after a US DST change (cron may lag)."""
    a, b = at.astimezone(CT).utcoffset(), (at - timedelta(days=7)).astimezone(CT).utcoffset()
    return 60 if a != b else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=float, default=26)
    ap.add_argument("--now", help="ISO time to check as of (testing)")
    a = ap.parse_args()

    now = parse_now(a.now)
    start = now - timedelta(hours=a.hours)
    try:
        commits = git_commits(start - timedelta(hours=2), now)
    except subprocess.CalledProcessError as e:
        print(json.dumps({"checkedAt": now.isoformat(), "error": e.stderr.strip()[:300]}))
        return 1

    result, issues, info, notify = [], [], [], []
    for r in ROUTINES:
        pat = re.compile(r["pat"])
        mine = [(t, m) for t, m in commits if pat.search(m)]
        rslots = list(slots(r, start, now))
        buckets = {i: [] for i in range(len(rslots))}
        for t, m in mine:  # each commit goes to the nearest slot inside its window
            best = None
            for i, (_, at) in enumerate(rslots):
                dm = (t - at).total_seconds() / 60
                if -r["before"] <= dm <= r["after"] and (best is None or abs(dm) < best[1]):
                    best = (i, abs(dm))
            if best:
                buckets[best[0]].append((t, m))
        for i, (d, at) in enumerate(rslots):
            got = sorted(buckets[i])
            grace = r["grace"] + dst_extra(at)
            label = f"{r['name']} {d}" + (at.astimezone(r["tz"]).strftime(" %H:%M") if len(r["times"]) > 1 else "")
            row = {"routine": r["name"], "date": str(d),
                   "slot": at.astimezone(r["tz"]).strftime("%Y-%m-%d %H:%M ")
                   + ("UTC" if r["tz"] is UTC else "CT")}
            if got:
                row["state"] = "duplicated" if len(got) > 1 else "present"
                row["lateMin"] = round((got[0][0] - at).total_seconds() / 60)
                row["commits"] = [{"at": t.strftime("%Y-%m-%dT%H:%M:%SZ"), "msg": m} for t, m in got]
                if len(got) > 1:
                    refresh = all(REFRESH.search(m) for _, m in got[1:])
                    row["refresh"] = refresh
                    info.append(f"push duplicated: {label} ({len(got)}x"
                                + (", re-check/catch-up" if refresh else "") + ")")
            elif now > at + timedelta(minutes=grace):
                row["state"] = "missing"
                issues.append(f"push missing: {label}")
            else:
                row["state"] = "pending"
            if r["plan"]:
                p = r["plan"](d)
                row["planFile"] = p
                row["planExists"] = os.path.exists(os.path.join(ROOT, p))
                if row["state"] == "missing" and r["name"] in PLAN_ROUTINES and not row["planExists"]:
                    notify.append(label)
            result.append(row)

    counts = {}
    for row in result:
        counts[row["state"]] = counts.get(row["state"], 0) + 1
    out = {
        "checkedAt": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "windowHours": a.hours,
        "commitsScanned": len(commits),
        "counts": counts,
        "issues": issues,          # push missing: <routine> <date>  -> warn
        "info": info,              # duplicates, never an issue
        "notify": notify,          # plan routines missing AND plan file absent
        "slots": result,
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
