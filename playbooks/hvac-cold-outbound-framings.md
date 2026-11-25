# Cold Call & Outbound Framings: Independent HVAC Owners

Status: **hypotheses, unvalidated**. Written 2026-11-25. No Arch call transcripts, win/loss data or approved product documentation were available. Nothing here is a verified finding.

Before using any framing, confirm the "Claim to verify" line against current approved Arch documentation. Do not say a capability exists until it has been confirmed.

## Who this is for

- Independent HVAC companies: not PE-backed or franchise. Unclear ownership goes to review and is not called.
- Verified ServiceTitan users first.
- The persona is the owner/president unless noted. GMs and marketing leads get different framings; they are not interchangeable.

## Shared call structure (all framings)

Keep every arm identical except the **reason for the call** and the **diagnostic question**. That keeps the A/B test clean.

1. **Opener (fixed):** "Hi {first name}, this is {rep} with Arch. This is a cold call. Can I take 30 seconds to say why I called, and you tell me if it's worth a conversation?"
2. **Reason for call (varies by framing)**
3. **Diagnostic question (varies by framing)**
4. **Ask (fixed):** "Worth 20 minutes next week to see if it applies to {company}? Tuesday or Thursday?"

Rules: one point per call. Never use invented personalization or invented numbers. Never imply an existing relationship. Don't quote customer results or prices unless they are approved.

---

## Framing A — Dormant Customers ("money already in your system")

**Hypothesis:** Owners distrust "new leads" but believe their past customers are under-worked. Revenue from people who already trust them feels low-risk.

- **Reason for call:** "Most independent HVAC shops we talk to have thousands of past customers in ServiceTitan who haven't booked in a year or more. We help turn that list back into booked jobs."
- **Diagnostic question:** "Is anyone at {company} reaching out to customers who haven't called you in a while, or do they mostly wait for the phone to ring?"
- **Likely pushback → response:**
  - "We send a newsletter." → "Do you know how many jobs it booked last quarter? That's usually the gap."
  - "We're busy enough." → "Makes sense in peak. Is it the same in April and October?" (bridges to Framing B)
- **Claim to verify:** Arch can segment and contact past customers using ServiceTitan data.

## Framing B — Shoulder-Season Schedule ("idle techs in spring and fall")

**Hypothesis:** The most concrete pain is a half-empty schedule while payroll stays fixed. It is felt by owners who carry the payroll.

- **Reason for call:** "I'm calling HVAC owners about spring and fall, when the weather's mild, the phone slows down, and you're still paying techs. We help fill those weeks."
- **Diagnostic question:** "What do you do today when the schedule's light for a week?"
- **Likely pushback → response:**
  - "We run tune-up specials." → "How do you decide who gets them, and how many book?"
  - "Call me in March." → Book the March call on the spot. Log it as `next_step=callback`, not as a loss.
- **Timing note:** Probably strongest just before or during the shoulder season. Hold call dates constant across arms (see the experiment doc).
- **Claim to verify:** Arch campaigns can be timed or targeted to fill demand gaps.

## Framing C — Proof Over Promises ("know what your marketing actually produces")

**Hypothesis:** Many owners have been burned by agencies and lead services. A measurement-first, anti-agency stance lowers their guard.

- **Reason for call:** "I'm not an agency and I'm not selling leads. I'm calling because most owners I talk to can't tell me which marketing dollars actually turned into booked jobs. We measure that against your ServiceTitan data."
- **Diagnostic question:** "If I asked what your marketing booked last month, in jobs and dollars, could you answer?"
- **Likely pushback → response:**
  - "We have an agency." → "Good. How do they prove it worked: clicks, or jobs in ServiceTitan?"
  - "Marketing doesn't work for us." → "That's usually a measurement problem first. Can I show you how we'd check?"
- **Best for:** owners who already spend on marketing, and GM/marketing-lead personas.
- **Claim to verify:** Arch reports on booked jobs and revenue, and supports a holdout/control group to measure lift rather than just attribution.

## Framing D — Maintenance Agreements ("protect the recurring revenue")

**Hypothesis:** Owners treat membership/maintenance-agreement counts as a health metric and fear renewals slipping.

- **Reason for call:** "I'm calling HVAC owners about maintenance agreements: getting more customers on a plan and keeping the ones you have from lapsing."
- **Diagnostic question:** "Do you know roughly how many agreements you have today compared with this time last year?"
- **Likely pushback → response:**
  - "ServiceTitan handles renewals." → "Does it tell you who's likely to lapse before they do, and who should be offered a plan?" (Only ask this if Arch can do it.)
  - "We don't push memberships." → Log as a disqualifier signal for this framing. Don't argue.
- **Claim to verify:** Arch supports membership acquisition/retention campaigns.

## Framing E — Replacement Pipeline ("aging equipment = installs")

**Hypothesis:** Install/replacement jobs are the highest-ticket work. Owners respond to "find your next replacements" more than to "more service calls".

- **Reason for call:** "Your past customers with 12-to-15-year-old systems are your next replacement jobs. Most shops don't contact them until the unit dies and the customer calls three companies. We help you get there first."
- **Diagnostic question:** "How do you find replacement opportunities today: techs on service calls, or something more systematic?"
- **Likely pushback → response:**
  - "Our techs flag those." → "On the calls they're on. What about customers you haven't seen in two years?"
- **Claim to verify:** Arch can target by equipment age/install date from ServiceTitan data. The 12–15 year equipment-age figure is an assumption and needs a sourced industry reference before use.

## Framing F — Local Competitive Insight (value-first)

**Hypothesis:** Leading with a free, specific, local insight earns the meeting better than leading with a product.

- **Reason for call:** "I put together a one-page look at {company}'s Google reviews and ratings compared with the 4–5 other HVAC shops around {city}. Happy to send it whether or not we ever work together."
- **Diagnostic question:** "Who handles your reviews and local reputation today?"
- **Ask (variant):** "Can I walk you through it in 15 minutes?" This is the one allowed deviation from the fixed ask. Note it in the analysis.
- **Requirements:** The asset is built only from public data, with a source and retrieval date on each figure and caveats, and is human-reviewed before it is sent. No invented competitor spend or revenue.
- **Claim to verify:** The asset's topic connects to something Arch actually does; otherwise it's a bait-and-switch.

---

## Email/LinkedIn companions (same framing as the call arm)

Under 80 words, one point, one ask. Each follow-up adds new information. Templates:

**A:** Subject: `past customers at {company}` — "{First name}, most HVAC shops have thousands of past customers in ServiceTitan who haven't booked in a year or more. We help turn that list back into scheduled jobs and measure the result in ServiceTitan. Worth 20 minutes to see what yours looks like? — {rep}"

**B:** Subject: `slow weeks in spring` — "{First name}, when the weather goes mild, the schedule thins out but payroll doesn't. We help independent HVAC shops fill those weeks from their existing customer base. Open to a 20-minute look before March? — {rep}"

**C:** Subject: `what did marketing book last month?` — "{First name}, not an agency, not selling leads. Most owners can't say which marketing dollars turned into booked jobs. We measure that against ServiceTitan data. Worth 20 minutes? — {rep}"

D, E and F follow the same pattern: one sentence of pain, one sentence on what Arch does (verified only), one ask.

## Suggested test order

Volumes are likely small, so don't test all six at once. Suggested sequence (each a two-arm test per `experiments/framing-ab-test-v1.md`):

1. **Round 1:** current script (control) vs **A — Dormant Customers**. This is the broadest pain and needs no asset.
2. **Round 2:** winner vs **C — Proof Over Promises**. This tests the anti-agency angle.
3. **Round 3:** winner vs **B** (run it just before spring) or **F** (needs asset production capacity).

D and E are narrower. Test them once call notes show memberships or replacements coming up as stated pain.

## What to log on every call

Use `templates/call_log_template.csv`. Most important: `arm`, `decision_maker_reached`, `framing_delivered_as_written`, `first_objection` + the buyer's verbatim words (keep buyer statements separate from rep interpretation), `meeting_booked`, `meeting_qualified`.
