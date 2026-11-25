import sys
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from analyze_results import summarize, wilson  # noqa: E402
from assign_arms import assign  # noqa: E402


def acct(aid, parent="", ownership="independent", state="GA", size="small", st="yes"):
    return {"account_id": aid, "parent_id": parent, "ownership": ownership,
            "state": state, "size_band": size, "servicetitan_verified": st}


class AssignTests(unittest.TestCase):
    def test_excludes_non_independent_and_unknown(self):
        rows = assign([acct("1"), acct("2", ownership="pe-backed"), acct("3", ownership="franchise"),
                       acct("4", ownership="")], [], "e", ["control", "A"], 1)
        self.assertEqual([r["account_id"] for r in rows], ["1"])

    def test_same_parent_same_arm(self):
        accounts = [acct(f"{p}-{i}", parent=f"P{p}") for p in range(30) for i in range(3)]
        rows = assign(accounts, [], "e", ["control", "A"], 7)
        by_parent = {}
        for r in rows:
            by_parent.setdefault(r["parent_id"], set()).add(r["arm"])
        self.assertTrue(all(len(v) == 1 for v in by_parent.values()))

    def test_duplicates_assigned_once(self):
        rows = assign([acct("1"), acct("1"), acct("2")], [], "e", ["control", "A"], 1)
        self.assertEqual(sorted(r["account_id"] for r in rows), ["1", "2"])

    def test_balanced_within_stratum(self):
        accounts = [acct(str(i), state=s) for s in ("GA", "AZ") for i in range(s == "GA" and 0 or 100, (s == "GA" and 0 or 100) + 41)]
        rows = assign(accounts, [], "e", ["control", "A"], 3)
        for s in ("ga", "az"):
            c = Counter(r["arm"] for r in rows if r["stratum"].startswith(s))
            self.assertLessEqual(abs(c["control"] - c["A"]), 1)

    def test_deterministic_with_seed(self):
        accounts = [acct(str(i)) for i in range(50)]
        a = assign(accounts, [], "e", ["control", "A"], 42, now="t")
        b = assign(accounts, [], "e", ["control", "A"], 42, now="t")
        self.assertEqual(a, b)

    def test_never_reassigns_and_new_brand_follows_parent(self):
        first = assign([acct("1", parent="P")], [], "e", ["control", "A"], 1)
        second = assign([acct("1", parent="P"), acct("2", parent="P")], first, "e", ["control", "A"], 999)
        self.assertEqual([r["account_id"] for r in second], ["2"])
        self.assertEqual(second[0]["arm"], first[0]["arm"])

    def test_incremental_batches_with_same_seed_stay_balanced(self):
        existing = []
        for i in range(10):
            existing += assign([acct(str(i))], existing, "e", ["control", "A"], 5)
        c = Counter(r["arm"] for r in existing)
        self.assertLessEqual(abs(c["control"] - c["A"]), 1)


class AnalyzeTests(unittest.TestCase):
    def test_itt_denominator_and_leakage_flagged(self):
        assignments = [{"experiment": "e", "account_id": str(i), "arm": "A" if i % 2 else "control"} for i in range(10)]
        touches = [
            {"touch_id": "t1", "account_id": "1", "arm": "A", "decision_maker_reached": "1",
             "meeting_booked": "1", "meeting_qualified": "1"},
            {"touch_id": "t2", "account_id": "1", "arm": "A", "decision_maker_reached": "1",
             "meeting_booked": "1", "meeting_qualified": "1"},
            {"touch_id": "t3", "account_id": "2", "arm": "A", "decision_maker_reached": "1",
             "meeting_booked": "1", "meeting_qualified": "1"},
            {"touch_id": "t4", "account_id": "99", "arm": "A", "meeting_booked": "1"},
        ]
        res, issues = summarize(assignments, touches)
        self.assertEqual(res["A"], {"assigned": 5, "accounts": 5, "dm": 1, "meeting": 1, "qualified": 1})
        self.assertEqual(res["control"]["assigned"], 5)
        self.assertEqual(res["control"]["qualified"], 0)
        self.assertEqual(len(issues), 2)

    def test_multi_location_parent_counts_once(self):
        assignments = [{"experiment": "e", "account_id": a, "parent_id": "P1", "arm": "A"} for a in ("a1", "a2", "a3")]
        assignments.append({"experiment": "e", "account_id": "b1", "parent_id": "P2", "arm": "control"})
        touches = [{"touch_id": f"t{a}", "account_id": a, "arm": "A", "decision_maker_reached": "1",
                    "meeting_booked": "1", "meeting_qualified": "1"} for a in ("a1", "a2", "a3")]
        res, _ = summarize(assignments, touches)
        self.assertEqual(res["A"], {"assigned": 1, "accounts": 3, "dm": 1, "meeting": 1, "qualified": 1})

    def test_wilson_bounds(self):
        lo, hi = wilson(5, 100)
        self.assertTrue(0 < lo < 0.05 < hi < 0.12)
        self.assertEqual(wilson(0, 0), (0.0, 0.0))


if __name__ == "__main__":
    unittest.main()
