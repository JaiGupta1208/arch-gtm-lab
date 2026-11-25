# Experiment Registration: Cold Call Framing A/B v1

Status: **draft — needs operator sign-off on the fields marked TBD before launch.**
Framings: `playbooks/hvac-cold-outbound-framings.md`

| Field | Value |
| --- | --- |
| Hypothesis | Framing A (Dormant Customers) books more qualified meetings per assigned account than the current script. |
| Eligible accounts | Independent HVAC (ownership = `independent`), in assigned territory, not contacted in the last 90 days (TBD), not a customer or open opportunity. ServiceTitan-verified preferred; stratify on it. |
| Exclusions | PE-backed, franchise or unknown ownership; do-not-contact; accounts already in another active experiment. |
| Unit | **Parent company.** All brands and locations under one parent get the same arm. |
| Arms | Control = current script (paste it into `experiments/control-script.md` before launch). Treatment = Framing A. Opener and ask are identical across arms. |
| Stratification | State × size band × ServiceTitan-verified. |
| Assignment | `tools/assign_arms.py` with a recorded seed. Assignments are append-only and never reassigned. |
| Primary outcome | Qualified meetings booked per assigned account, analysed at parent-company level (the randomisation unit; a multi-location parent counts once). Qualification definition: **TBD with operator** (e.g. owner/GM attends, independent, uses ServiceTitan, 20 min held). |
| Secondary | Meetings per decision-maker conversation; attended meetings; decision-maker connect rate (sanity check: it should *not* differ by arm); time and cost per qualified meeting; first-objection mix. |
| Duration | Until each arm reaches its target number of assigned accounts, or 6 weeks max, whichever comes first. |
| Cost | Rep time only. Record dials and minutes per arm. |
| Guardrails | Do-not-contact requests honoured immediately. Rep logs `framing_delivered_as_written`. If adherence drops below 80% in an arm, pause and retrain. |
| Stopping rule | No peeking-based early stop on the primary outcome. Analyse once, at the end. Stop early only for a guardrail breach. |

## Controlling for rep and timing

- Each rep calls **both** arms, interleaved within the same days and hours. Never run Control in week 1 and Treatment in week 2: season and day-of-week would be mixed into the result.
- Work the call list in the randomised order the tool outputs.
- If there are multiple reps, include `rep` in the analysis as a check.

## Sample size (how big the test needs to be)

Two-sided α = 0.05, 80% power, per arm, counted as **decision-maker conversations**:

| Baseline meeting rate | Detectable rate | Conversations per arm |
| --- | --- | --- |
| 5% | 10% | ~435 |
| 10% | 15% | ~686 |
| 10% | 20% | ~199 |
| 15% | 25% | ~250 |

Convert to assigned parents using your own connect rate. For example, at a 25% decision-maker connect rate across a full cadence, 200 conversations ≈ 800 parent companies per arm.

**Implication:** with typical solo-rep volumes, only large differences are detectable. Expect each round to give directional evidence, not proof. Report results with intervals and don't over-claim. The baseline rates above are illustrative, not Arch data; replace them with your actual numbers.

## Analysis

`python3 tools/analyze_results.py assignments.csv call_log.csv`

Outcomes are rolled up to the parent company, the unit that was randomised, so multi-location parents don't inflate precision. Every assigned parent stays in the denominator, including ones never reached (intention-to-treat). The script reports, per arm, assigned parents and accounts, decision-maker conversations, meetings, qualified meetings, rates with 95% Wilson intervals, and a two-proportion z-test on the primary outcome.

This is a randomised comparison, so causal language is allowed for the primary outcome within this population and period only.
