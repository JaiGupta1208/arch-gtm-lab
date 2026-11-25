"""Intention-to-treat analysis of a framing experiment.

Usage:
    python3 tools/analyze_results.py assignments.csv call_log.csv [--experiment framing-ab-v1]

Every assigned account counts in its arm's denominator. Touches from
accounts not in the assignment file, or logged under a different arm than
assigned, are reported as data-quality issues and ignored.
"""

import argparse
import csv
from collections import defaultdict
from math import erf, sqrt


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def two_prop_p(k1, n1, k2, n2):
    if min(n1, n2) == 0:
        return float("nan")
    p = (k1 + k2) / (n1 + n2)
    se = sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    if se == 0:
        return 1.0
    z = abs(k1 / n1 - k2 / n2) / se
    return 2 * (1 - 0.5 * (1 + erf(z / sqrt(2))))


def _flag(v):
    return str(v).strip().lower() in ("1", "true", "yes", "y")


def summarize(assignments, touches, experiment=None):
    arm_of = {r["account_id"]: r["arm"] for r in assignments if not experiment or r["experiment"] == experiment}
    issues = []
    per_acct = defaultdict(lambda: {"dm": False, "meeting": False, "qualified": False})
    for t in touches:
        aid = t["account_id"]
        if aid not in arm_of:
            issues.append(f"touch {t.get('touch_id')} for unassigned account {aid}")
            continue
        if t.get("arm") and t["arm"] != arm_of[aid]:
            issues.append(f"touch {t.get('touch_id')} logged as arm {t['arm']} but {aid} assigned {arm_of[aid]}")
            continue
        s = per_acct[aid]
        s["dm"] |= _flag(t.get("decision_maker_reached"))
        s["meeting"] |= _flag(t.get("meeting_booked"))
        s["qualified"] |= _flag(t.get("meeting_qualified"))

    out = {}
    for aid, arm in arm_of.items():
        o = out.setdefault(arm, {"assigned": 0, "dm": 0, "meeting": 0, "qualified": 0})
        o["assigned"] += 1
        s = per_acct.get(aid)
        if s:
            o["dm"] += s["dm"]
            o["meeting"] += s["meeting"]
            o["qualified"] += s["qualified"]
    return out, issues


def main():
    p = argparse.ArgumentParser()
    p.add_argument("assignments")
    p.add_argument("call_log")
    p.add_argument("--experiment")
    a = p.parse_args()
    with open(a.assignments, newline="") as f:
        assignments = list(csv.DictReader(f))
    with open(a.call_log, newline="") as f:
        touches = list(csv.DictReader(f))
    res, issues = summarize(assignments, touches, a.experiment)

    print(f"{'arm':<10}{'assigned':>9}{'DM conv':>9}{'mtgs':>6}{'qual':>6}  qual/assigned (95% CI)        mtg/DM conv")
    for arm in sorted(res):
        r = res[arm]
        lo, hi = wilson(r["qualified"], r["assigned"])
        rate = r["qualified"] / r["assigned"] if r["assigned"] else 0
        mdm = f"{r['meeting'] / r['dm']:.1%}" if r["dm"] else "n/a"
        print(f"{arm:<10}{r['assigned']:>9}{r['dm']:>9}{r['meeting']:>6}{r['qualified']:>6}  {rate:6.1%} ({lo:.1%}-{hi:.1%})       {mdm}")
    arms = sorted(res)
    if len(arms) == 2:
        x, y = res[arms[0]], res[arms[1]]
        print(f"\nprimary outcome two-proportion p-value ({arms[0]} vs {arms[1]}): "
              f"{two_prop_p(x['qualified'], x['assigned'], y['qualified'], y['assigned']):.3f}")
    if issues:
        print(f"\n{len(issues)} data-quality issue(s):")
        for i in issues[:20]:
            print("  - " + i)


if __name__ == "__main__":
    main()
