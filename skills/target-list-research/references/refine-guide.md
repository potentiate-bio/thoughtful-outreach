# Refine — worked example

Input: `examples/demo-event/overrides-example.csv` from a (fictional) run of Northwind
Bioanalysis at the Atlantic Regulated Bioanalysis Workshop, against `example-rubric.md` as it
stood before that run (without the two changelog entries dated 2027-03-14).

## 1. Group the overrides

| Group | Overrides | Shared cause |
|---|---|---|
| Central labs C → X | Northbank, Cobblestone, Tarnwell | All three: exhibiting PK/ADA testing at this workshop |
| Preclinical sponsors B → A | Cindermoss, Velloway | Each has a fresh, company-specific trigger (IND filed; first-in-human date announced) |
| Academic IIT sponsors B → X | Eastmoor | "Investigator-initiated trials almost never fund regulated bioanalysis" — user marked `core` |
| Note only | Halcyon (A → A) | Confirms a borderline call; the acquired lab doesn't compete |

## 2. Propose one change per group

**Proposal 1 — central labs at this workshop.** Add to event profile *Atlantic Regulated
Bioanalysis Workshop*: "Central labs exhibiting here are pitching specialty bioanalysis → X."
Evidence: 3 of 3 central-lab overrides, consistent reasons, all tied to what they're doing *at
this event*. Confidence: high.
→ Ask: *event profile only, core ICP, or reject?* Suggest event: at most other meetings central
labs are still referral partners.

**Proposal 2 — preclinical sponsors.** No rule change. Both promotions rest on a dated,
company-specific event, which is exactly what the `IND planned` / `IND-enabling` signals are for.
Instead: record both companies in `playbook.md` as now tier A, and propose tightening the signal
vocabulary — add `IND filed` and `FIH date announced` as signals that move a preclinical sponsor
to A. Confidence: medium (2 overrides, same direction, different evidence).

**Proposal 3 — academic medical centers.** Add to core hard exclusions: "Academic medical centers
running only investigator-initiated trials → X (rarely fund regulated bioanalysis)." Evidence:
1 override, explicitly scoped `core`. Confidence: low on count, high on intent — say so, and let
the user decide. Ask whether academic centers running *industry-sponsored* trials stay in B.

## 3. Apply only what's accepted

For each accepted proposal: edit `rubric.md`, add a dated changelog line with the evidence, and log
the run (overrides in, proposals made, decisions) in `playbook.md`. Rejected proposals are logged
too, so the same suggestion isn't made again without new evidence.

## Things to watch for

- **An override that contradicts an explicit rule.** Don't silently side with either — ask.
- **Over-generalising.** Three central-lab overrides at one workshop is an event pattern, not a
  truth about central labs. Default to the narrowest scope the evidence supports.
- **Overrides with no reason.** Ask for one first; a tier change without a reason can't become a rule.
- **Signals vs rules.** Often the right fix isn't a new tier rule but a new signal — something to
  look for next time that would have made the AI's call right in the first place.
