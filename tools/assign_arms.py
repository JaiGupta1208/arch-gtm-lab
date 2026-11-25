"""Stratified, parent-level random assignment of accounts to experiment arms.

Usage:
    python3 tools/assign_arms.py accounts.csv assignments.csv \
        --experiment framing-ab-v1 --arms control,A --seed 20261125

accounts.csv columns: account_id, parent_id, ownership, state, size_band,
servicetitan_verified. Only ownership == "independent" is eligible.
Existing rows in assignments.csv are kept as-is; accounts already assigned
for the experiment (or whose parent is) are never reassigned.
"""

import argparse
import csv
import os
import random
from collections import Counter, defaultdict
from datetime import datetime, timezone

FIELDS = ["experiment", "account_id", "parent_id", "arm", "stratum", "seed", "assigned_at"]


def load_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def stratum_of(row):
    return "|".join(
        (row.get(k) or "unknown").strip().lower()
        for k in ("state", "size_band", "servicetitan_verified")
    )


def assign(accounts, existing, experiment, arms, seed, now=None):
    now = now or datetime.now(timezone.utc).isoformat()
    prior = [r for r in existing if r["experiment"] == experiment]
    parent_arm = {r["parent_id"]: r["arm"] for r in prior}
    assigned_ids = {r["account_id"] for r in prior}

    seen, parents = set(), defaultdict(list)
    for row in accounts:
        aid = row["account_id"].strip()
        if aid in seen or aid in assigned_ids:
            continue
        seen.add(aid)
        if (row.get("ownership") or "").strip().lower() != "independent":
            continue
        pid = (row.get("parent_id") or "").strip() or aid
        parents[pid].append(row)

    new_rows, strata = [], defaultdict(list)
    for pid, rows in parents.items():
        if pid in parent_arm:
            new_rows += [_row(experiment, r, pid, parent_arm[pid], stratum_of(rows[0]), seed, now) for r in rows]
        else:
            strata[stratum_of(rows[0])].append(pid)

    counts = defaultdict(Counter)
    for pid, (stratum, arm) in {r["parent_id"]: (r["stratum"], r["arm"]) for r in prior}.items():
        counts[stratum][arm] += 1

    for stratum in sorted(strata):
        pids = sorted(strata[stratum])
        rng = random.Random(f"{seed}|{experiment}|{stratum}|{','.join(pids)}")
        rng.shuffle(pids)
        c = counts[stratum]
        for pid in pids:
            low = min(c[a] for a in arms)
            arm = rng.choice([a for a in arms if c[a] == low])
            c[arm] += 1
            new_rows += [_row(experiment, r, pid, arm, stratum, seed, now) for r in parents[pid]]
    return new_rows


def _row(experiment, account, pid, arm, stratum, seed, now):
    return {
        "experiment": experiment,
        "account_id": account["account_id"].strip(),
        "parent_id": pid,
        "arm": arm,
        "stratum": stratum,
        "seed": seed,
        "assigned_at": now,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("accounts")
    p.add_argument("assignments")
    p.add_argument("--experiment", required=True)
    p.add_argument("--arms", required=True, help="comma-separated, e.g. control,A")
    p.add_argument("--seed", type=int, required=True)
    a = p.parse_args()

    arms = [x.strip() for x in a.arms.split(",") if x.strip()]
    if len(arms) < 2:
        p.error("need at least two arms")
    existing = load_csv(a.assignments)
    new_rows = assign(load_csv(a.accounts), existing, a.experiment, arms, a.seed)

    write_header = not os.path.exists(a.assignments) or os.path.getsize(a.assignments) == 0
    with open(a.assignments, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if write_header:
            w.writeheader()
        w.writerows(new_rows)

    counts = defaultdict(int)
    for r in new_rows:
        counts[r["arm"]] += 1
    print(f"appended {len(new_rows)} assignments: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))


if __name__ == "__main__":
    main()
