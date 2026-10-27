---
name: target-list-research
description: Score a list of people and companies (a conference attendee list, a CRM export, a lead list) against your ideal customer profile into an interactive target map, let you override and shortlist, research the shortlist into a briefing, and turn your overrides into proposed ICP refinements. Research only, never writes outreach. Use when someone shares an attendee or prospect list, says "who should I meet at [event]", "score this list", "research these people", or "refine my ICP".
license: MIT
metadata:
  author: potentiate.bio
  version: "1.0.0"
---

# Target list research

Turn a long list of names into a short list of the right people, with enough verified signal on each
one that the user can write a thoughtful first message themselves. The workflow has three stages,
and the input file tells you which one to run:

| Input looks like | Run |
|---|---|
| Names, titles, companies and little else | **Stage 1 — score** |
| A Stage 1 export: has `Tier`, `Seniority`, `Function`, `Selected` columns | **Stage 2 — research** |
| An overrides export: has `AITier` and `YourTier` columns | **Refine — propose ICP changes** |

Never ask which stage. If two files arrive together (e.g. a shortlist and an overrides file), run
Refine first so the rubric is current, then Stage 2.

## Principles that hold in every stage

1. **The user owns the ICP.** You apply the rubric; you don't invent it. When the list raises a
   question the rubric doesn't answer (a segment it never mentions, an ambiguous company), ask —
   don't guess. If the user can't articulate their ICP yet, run the setup interview below first.
2. **Research only.** Never draft outreach: no email copy, subject lines, openers or talking
   points, even if the same message asks for them. The signal is the machine's job; what to say,
   how and when is the user's. If they want a draft, that's a separate request outside this skill.
3. **"Unsure" is an answer.** Three confidence levels — `high`, `medium`, `unsure` — and `unsure` is
   an expected end state, not a failure. Never fill a gap with a plausible-sounding guess. Never
   start a second research pass on unsure names unless the user explicitly asks in this run.
4. **Every call is auditable.** Each company gets a one-line `Why` for its tier. Each research
   highlight is a verifiable fact with a source.
5. **Use only lists the user is entitled to use.** Work from exports and files the user provides.
   Don't scrape platforms behind a login unless the user confirms the platform's terms allow it.

## Files this skill reads and writes

Keep these next to the user's lists (or, in a chat-only tool, ask the user to paste them):

- `rubric.md` — the user's ICP: tiers, segments, signals to look for, exclusions, spotlight flag,
  preselect rule, event profiles. Start from `references/rubric-template.md`; see `references/example-rubric.md` for a
  filled-in (fictional) example. **Read it before scoring anything.**
- `playbook.md` — the running log: company aliases learned, rubric changes and why, results per
  run, data quirks. Start from `references/playbook-template.md`.
- CSV files in the schemas defined in `references/csv-schemas.md`. Stick to those column names
  exactly — the viewers depend on them.

### No rubric yet? Run the setup interview

Ask, in one round if your tool allows multiple questions at once:
1. What do you sell, in one sentence? Who buys it (role, team)?
2. Which kinds of organisations are a direct fit? Which are maybe? Which are partners or referral
   sources rather than buyers? Which are never a fit (including competitors — name them)?
3. What evidence moves a company up or down for you (e.g. an active trial, a recent funding
   round, an in-house team that does what you sell)? These become the signal vocabulary.
4. Is there a "spotlight" — a niche you particularly want surfaced regardless of tier?
5. Which seniorities and functions are worth meeting at a direct-fit company — and does that
   differ by segment?

Write the answers into `rubric.md` using the template, show it to the user, and continue once they
confirm. Don't pad it with assumptions — leave a section marked `TODO` rather than inventing a rule.

## Modes

- **List mode** (default): any list of people/companies.
- **Event mode**: switch on when the user names an event, provides an agenda, or the rubric has an
  event profile for this show. Event mode adds: the event profile's rubric adjustments, agenda and
  speaker cross-checks, badge-vs-agenda title mismatches, and timing notes (e.g. request meetings in
  the event app before the show; email after). Record the event name in your outputs.

## Stage 1 — score the list

**1. Prepare the rows.** If you can run Python, use `scripts/prepare_list.py` (handles a UTF-8 BOM,
look-alike Unicode punctuation, exact duplicates, company keys, and an optional CRM export match).
If you can't run code, do the same by hand: trim whitespace, normalise odd punctuation, drop exact
duplicates, and strip legal suffixes (Inc, Ltd, GmbH, Corp, Therapeutics, Bio, Pharma…) to compare
company names. Check `playbook.md` for aliases learned on earlier runs (renames, parent companies).

**2. Cross-check the CRM, if the user provides one.** Prefer an export file (company name + domain,
optional deals and contacts) — it works in every tool. If a CRM connector is available, you may
query it instead. Match in two passes: exact company key first, then a looser pass (one name
contains the other, or same domain). A loose match is a *candidate*: confirm it by domain, never by
a shared word alone, or "Northwind Bio" and "Northwind Capital" collapse together.

**3. Score each company** against `rubric.md` (plus the event profile in event mode):
- `Tier`: A direct fit / B plausible / C partner or referral / X out of scope (use the rubric's own
  tier names if it renames them), and `Priority` within A if the rubric defines one.
- `Segment`: the rubric's segment label.
- `Spotlight`: `strong` when the spotlight theme *is* the company, `partial` when it's one part of a
  broader portfolio, blank otherwise.
- `Why`: one line, specific enough that the user can disagree with it.
- `Borderline`: `Y` plus a `BorderlineNote` whenever you nearly chose a different tier — what would
  flip it. These are where the user's review time is best spent; don't be stingy with them, and
  don't mark everything borderline either.
- `Signals`: short evidence tags behind the call, separated by `;` — the facts a tier is built on,
  e.g. `Ph1 active · 2 trials; US sites; No in-house lab`. Use the signal vocabulary in the
  rubric so tags are consistent and filterable. Signals are what make a list granular: two
  companies in the same segment and tier can differ on exactly the thing the user cares about
  this week. Only tag what you know or can check quickly (a trial registry, a pipeline page, a job
  posting, a press release); suffix anything unconfirmed with `?` rather than asserting it.
- Re-check acquisitions and renames before carrying a tier forward from an earlier run.

**4. Classify each person.** `Seniority` and `Function` use the buckets in the rubric. Read titles
carefully: "Director, Clinical & Commercial Supply" is an operations role, not a commercial one. If more than
~10% of titles land in `Other / unclear`, widen your patterns and look again before moving on.
The same person under two company badges (a rename, an acquisition) stays as two rows with a
`Note` pointing at each other — never merge or drop silently.

**5. Mark the default shortlist.** Set `Recommended = Y` using the rubric's preselect rule
(typically: senior, relevant-function people at tier-A companies, plus senior people at
spotlight-`strong` companies regardless of tier). The viewer's "Preselect" button uses this column.

**6. Output `scored.csv`** (schema in `references/csv-schemas.md`) and a short summary: counts by
tier, the borderline companies, CRM matches and live deals, and any rubric questions you parked.

**7. Hand over the target map.** The viewer is `assets/target-map.html`, a single self-contained
page that loads any CSV in the schema:
- If you can write files, save `scored.csv` and copy `assets/target-map.html` next to it. Tell the
  user to open the HTML in a normal browser tab (in-app preview panes often block downloads) and
  load the CSV with the file picker or by dragging it in.
- In a chat-only tool, give the CSV as a code block and point the user to the hosted viewer listed
  in the repository README, where they can paste it.

In the viewer the user filters (by tier, segment, signal, seniority, function), reads your `Why` lines, **overrides tiers with a reason**, and
ticks the people worth researching. They export two files: the shortlist (`Selected = Y`) and the
overrides. Do not build a new HTML page per run — the shared viewer is the interface.

## Stage 2 — research the shortlist

**1. Take the shortlist as given.** It's already the user's judgement; don't re-score. Respect any
overrides in it (`Tier` is the effective tier; `AITier` shows your original call).

**2. Research shallow and wide.** For each person, look for: current role and scope, how long
they've been in it, a notable prior employer or piece of work, and anything that marks them as
relevant (or not) to what the user sells. Two highlights maximum, each one a decision-relevant,
verifiable fact with a source URL. Stop when the signal is clear either way — a few targeted
searches per person, not an exhaustive profile.

**3. Batch by company, not alphabetically,** so whoever researches a company sees its whole
delegation and can spot duplicates and reporting lines. If you can run sub-agents in parallel, use
batches of ~15–20 people, cap parallelism at what your search budget can sustain (running out of
search budget mid-batch is the most common way a run degrades), and prefer fetching a known page
over another broad search. Have each batch return one JSON object per line:

```
{"name": "", "company": "", "focus": "", "highlights": ["", ""], "tenure": "", "prior": "",
 "scope_warning": "", "confidence": "high|medium|unsure", "sources": [""]}
```

Validate every line parses before merging. `scope_warning` is for a person whose work looks outside
the rubric's scope (e.g. an excluded modality) — flag, don't drop.

**4. Contact information, honestly labelled.** Default: only addresses found in the user's own CRM
export (`EmailBasis = crm`). Email-pattern guessing (inferring `first.last@` from known addresses at
the same domain) is **off unless the user turns it on**, because unsolicited email rules (GDPR,
CAN-SPAM, ePrivacy and national laws) vary and the user is responsible for compliance. If enabled,
label every guess `pattern` with its evidence ("first.last — from 6 known addresses"), and say
plainly when a company has no known addresses to infer from.

**5. Event mode: cross-check the agenda.** Match shortlist names against the agenda text. Trust the
printed session heading and its day/time/room line over links or page slugs, which are often stale.
When the agenda shows a different title or employer than the badge, record both in `TitleMismatch`
— don't silently pick one.

**6. Output `research.csv`** (schema in `references/csv-schemas.md`) and hand over
`assets/briefing.html` the same way as Stage 1. The briefing has no checkboxes; it's for reading,
with an "export visible" button for the user's own notes.

## Refine — turn overrides into ICP changes

Overrides are the most valuable output of a run: each one is the user telling you something the
rubric doesn't yet say. See `references/refine-guide.md` for a worked example.

1. Read the overrides CSV, `rubric.md`, and the event name if any.
2. Group overrides that share a cause (same segment, same direction, similar reasons). One-offs
   stay as company-specific notes (aliases, a pivot, a confirmed asset) — not rules.
3. For each group, propose **one** rubric change: the exact rule text to add or edit, the overrides
   that support it, and a confidence (how many overrides, how consistent the reasons are).
4. Ask the user, for each proposal: **apply to this event's profile only, apply to the core ICP, or
   reject?** Events legitimately shift focus — exhibitors at one show are buyers at another — so
   never promote an event-scoped pattern to the core ICP without the user saying so.
5. Apply only what's accepted. Add a dated entry to the rubric's changelog with the reason, and log
   the run in `playbook.md`. Never apply changes automatically, even "obvious" ones.
6. If an override contradicts an explicit rule in the rubric, point that out — either the rule or
   the override is wrong, and the user should decide which.

## After every run

Update `playbook.md`: aliases learned, rubric changes (with dates and reasons), the result shape
(people and companies by tier, confidence distribution, CRM coverage), data quirks in this source,
and anything that went wrong. The next run should inherit it instead of rediscovering it.

## Adapting to your tool

- **Can run code and spawn sub-agents** (e.g. Claude with code execution, Codex, Gemini CLI): follow
  everything above as written.
- **Can run code, no sub-agents:** research in sequential batches; checkpoint `research.csv` after
  each batch so a long run can resume.
- **Chat only, no files:** follow `prompts/chat-version.md` — it processes the list in chunks and
  emits CSV text the user pastes into the hosted viewer.
- **Tight output limits:** split long lists into chunks of ~100 rows and say which chunk you're on.
