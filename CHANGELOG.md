# Changelog

## 1.0.1

From testing the paste-in prompt in plain chat (Gemini):

- **List integrity.** The skill and the paste-in prompt now require every input row to be scored
  exactly once, with row counts checked per chunk. Chat models were adding and merging people.
- **Confidence needs a source.** `high` or `medium` research confidence now requires a source
  opened in the run; otherwise the answer is `unsure`.
- **Unreadable files.** The model says so and asks for a paste instead of working from memory.
- **Example rubric** now shows the pre-run state, so models don't apply the demo's Refine
  outcomes before the user has made them. The outcomes are in `refine-guide.md`.
- Chat chunks are 50 rows instead of 100. README notes that it works best in Claude.
- Hosted demo: the "Added to your selection" notice is now readable.

## 1.0.0 — first public release

The skill is generalised from a private version used to prepare for industry conferences.
New in the public version:

- **List mode and event mode.** Works on any list; event mode adds agenda/speaker cross-checks,
  badge-vs-agenda title mismatches, timing notes and per-event rubric profiles.
- **Overrides and Refine.** Override any company's tier with a reason in the target map; export the
  overrides; the Refine step proposes rubric changes (event profile or core ICP) for you to accept.
- **Signals.** Each company carries short evidence tags (an active trial, an in-house team, a
  filed IND…) drawn from a vocabulary in your rubric. The target map filters and searches by them,
  so a list can be sliced as finely as your ICP needs — without hardcoding an industry.
- **Borderline flags.** The skill marks the tier calls it nearly made differently, so review time
  goes where the AI is least sure.
- **Shared viewers.** One target map and one briefing page that load any CSV in the schema, instead
  of a new page generated per run — the same interface in every AI tool.
- **Rubric as a file.** Your ICP lives in `rubric.md` (template and fictional example included);
  the skill interviews you if you don't have one yet.
- **Email guessing off by default**, every address labelled with its source.
- **Paste-in prompt** for AI chats that can't install skills.

### How it evolved privately (v0.x)

- Started as a one-off scoring of an attendee list into a spreadsheet: minutes instead of several
  hours — and the tier mix showed which shows were worth attending at all, not just whom to meet.
- Spreadsheet → interactive HTML map with filters and a CSV export, then split into two stages
  (score everyone, research only the people picked).
- Rule added: research only — never draft outreach.
- Rule added: "unsure" is a valid result; an unrequested second research pass was removed.
- The tiering rubric started changing by event type, which is what became event profiles and the
  Refine step.
- Fixes along the way: a preselect count that was hardcoded and drifted from the data; downloads
  blocked by in-app preview panes (clipboard fallback added); look-alike Unicode punctuation and
  byte-order marks in exported lists; acquisitions that flipped a company's tier; stale agenda
  links; research runs that exhausted their search budget (fewer parallel batches, prefer fetching
  known pages).
