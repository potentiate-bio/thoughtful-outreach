# CSV schemas

The viewers read these exact column names (case-sensitive). Extra columns are kept and ignored.
UTF-8, comma-separated, double quotes around any field containing a comma, quote or newline.

## `scored.csv` — Stage 1 output (one row per person)

| Column | Required | Values |
|---|---|---|
| `PersonId` | yes | Unique per row, e.g. `p0001` |
| `Name`, `Title`, `Company` | yes | `Company` is the canonical company name |
| `BadgeCompany` | no | Company as it appeared on the source list, if different |
| `Tier` | yes | `A` `B` `C` `X` |
| `TierName` | no | Display name from the rubric |
| `Priority` | no | Number within A (1 = highest); blank otherwise |
| `Segment` | yes | A rubric segment label |
| `Spotlight` | no | `strong`, `partial` or blank |
| `Signals` | no | Evidence tags separated by `;` (e.g. `Ph1 active · 2 trials; US sites`). A trailing `?` marks an unconfirmed tag |
| `Why` | yes | One-line rationale for the company's tier |
| `Borderline` | no | `Y` if the tier call was close |
| `BorderlineNote` | no | What would flip the call |
| `Seniority`, `Function` | yes | Rubric buckets |
| `Recommended` | no | `Y` = in the default shortlist |
| `CRMAccount` | no | `Y` if the company is in the user's CRM |
| `CRMDeal` | no | Short deal description/state, blank if none |
| `Note` | no | Person-level note (e.g. same person under two badges) |

Company-level columns repeat on every person row of that company.

## Shortlist export — viewer output, Stage 2 input

All `scored.csv` columns for the selected people, plus:

| Column | Values |
|---|---|
| `Selected` | `Y` |
| `AITier` | The tier the skill assigned |
| `Tier` | The **effective** tier (the user's override if any) |
| `OverrideReason` | The user's reason, blank if no override |

## Overrides export — viewer output, Refine input (one row per company)

| Column | Values |
|---|---|
| `Company`, `Segment` | |
| `AITier`, `YourTier` | Original and overridden tier |
| `Reason` | The user's one-line reason |
| `Scope` | `event`, `core` or blank — the user's hint for where the change belongs |
| `Why` | The skill's original rationale, for comparison |
| `Event` | Event name if the run was in event mode |

## `research.csv` — Stage 2 output (one row per person)

| Column | Values |
|---|---|
| `Name`, `Title`, `Company`, `Tier`, `Segment`, `Seniority`, `Function` | Carried from the shortlist |
| `Confidence` | `high`, `medium`, `unsure` |
| `Focus` | One line: what this person works on |
| `Highlight1`, `Highlight2` | Decision-relevant, verifiable facts (blank rather than invented) |
| `Tenure`, `Prior` | Short text |
| `ScopeWarning` | Text if their work looks outside the rubric's scope |
| `Email` | Address, if known |
| `EmailBasis` | `crm`, `pattern` (only if the user enabled guessing) or `none` |
| `Speaker` | Event mode: `Day · time · room — session title` |
| `TitleMismatch` | Event mode: badge vs agenda difference, in words |
| `Sources` | URLs separated by ` | ` |
