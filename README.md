# Thoughtful outreach — open AI skills for business development

Skills that do the research so you can do the thinking. The first one:

## Target list research

Score a conference attendee list — or any list of people and companies — against your ideal
customer profile, research only the people you pick, and turn your disagreements with the AI into
a sharper ICP. **It never writes the outreach.** Finding the signal is the machine's job; what you
say, how you say it and when stays yours.

**[Try the live demo →](https://tools.potentiate.bio/thoughtful-outreach/)** (fictional data; lists you load never leave your browser)

| Stage | What happens | You get |
|---|---|---|
| 1 · Score | Every person gets a tier, segment, seniority and function; every company a one-line reason and **signals** — the evidence behind the call. Close calls are flagged as borderline. Optional CRM cross-check. | An interactive **target map** |
| — · Review | You filter, read the reasons, **override tiers with a why**, and tick the people worth meeting. | A shortlist and an overrides file |
| 2 · Research | Two verifiable highlights per person, a confidence level (`unsure` is allowed), CRM emails, agenda and speaker cross-checks in event mode. | A **research briefing** |
| Refine | Your overrides are grouped into proposed rubric changes — for this event only, or for your core ICP. You accept or reject each. | A rubric that learns |

### Principles

- **You own the ICP.** If you can't describe it, the AI can't apply it. The skill asks rather than invents.
- **Research only.** No drafted emails, openers or talking points.
- **Unsure is an answer.** No guessed facts. Email-address guessing is off by default.
- **Everything is auditable.** Every tier has a reason; every highlight has a source.
- **Use lists you're entitled to use.** Start from exports you have the right to work with.

## Get started

You need three things: the skill, a rubric describing your ICP, and a list.

### 1. Install the skill

<details open>
<summary><b>Claude</b> (claude.ai, Claude Code, desktop)</summary>

- **Claude Code:** `/plugin marketplace add potentiate-bio/thoughtful-outreach` then `/plugin install thoughtful-outreach@potentiate`
- **claude.ai / desktop app:** download `target-list-research.zip` from the [latest release](https://github.com/potentiate-bio/thoughtful-outreach/releases/latest) and upload it in the Skills section of Settings.
</details>

<details>
<summary><b>ChatGPT / Codex</b> (OpenAI)</summary>

- **Codex CLI:** copy `skills/target-list-research` into `~/.agents/skills/` (all projects) or `.agents/skills/` in a project.
- **ChatGPT** (plans with skill upload): upload `target-list-research.zip` from the [latest release](https://github.com/potentiate-bio/thoughtful-outreach/releases/latest) in the Skills section of Settings.
- **No skill upload?** Use the [paste-in prompt](skills/target-list-research/prompts/chat-version.md).
</details>

<details>
<summary><b>Gemini</b> (Google)</summary>

- **Gemini CLI:** `gemini extensions install https://github.com/potentiate-bio/thoughtful-outreach`
- **Gemini app:** upload `target-list-research.zip` from the [latest release](https://github.com/potentiate-bio/thoughtful-outreach/releases/latest) in the Skills section of Settings.
- **No skill upload?** Use the [paste-in prompt](skills/target-list-research/prompts/chat-version.md).
</details>

<details>
<summary><b>Cursor, Copilot and other agents</b></summary>

`npx skills add potentiate-bio/thoughtful-outreach` — or copy `skills/target-list-research` into your agent's skills folder.
</details>

### 2. Write your rubric

Copy [`rubric-template.md`](skills/target-list-research/references/rubric-template.md) to
`rubric.md` and fill it in — or just start a run and the skill will interview you for it. See the
[fictional worked example](skills/target-list-research/references/example-rubric.md).

### 3. Run it

Give your AI the list (and optionally a CRM export and an event agenda) and ask:

> *Score this attendee list for the [event] using my rubric.*

Open the target map, review, override, tick, export the shortlist. Then:

> *Research this shortlist.* &nbsp;·&nbsp; *Refine my rubric from these overrides.*

The viewers live in [`skills/target-list-research/assets/`](skills/target-list-research/assets/)
and on the [demo site](https://tools.potentiate.bio/thoughtful-outreach/). Open them in a normal browser tab — in-app preview panes
often block downloads.

## What's in this repository

```
skills/target-list-research/
  SKILL.md                    the workflow (open Agent Skills format)
  references/                 rubric template, fictional example rubric, CSV schemas,
                              playbook template, refine walkthrough
  assets/                     target-map.html and briefing.html viewers
  scripts/prepare_list.py     list cleaning + CRM export matching (standard library only)
  prompts/chat-version.md     paste-in version for any AI chat
examples/demo-event/          fictional attendee list, CRM export, agenda, outputs
docs/                         demo site (GitHub Pages)
tools/                        demo-data generator and site builder
```

## Data and compliance

The skill works on personal data (names, titles, employers). You are responsible for having the
right to use the lists you load and for how you contact people afterwards — unsolicited email is
regulated differently by country (e.g. GDPR and ePrivacy rules in Europe, CAN-SPAM in the US).
That's why email-pattern guessing is off by default and every address is labelled with where it
came from. The viewers run entirely in your browser; nothing is uploaded. The hosted demo at
tools.potentiate.bio counts visits with Google Analytics; the copies in this repository contain no
analytics or tracking of any kind.

All companies, people and events in `examples/` and on the demo site are fictional. Domains use
the reserved `.example` suffix.

## Contributing

Issues and pull requests welcome — especially rubric examples for other industries, list formats
the prepare script doesn't handle yet, and reports of how the skill behaves in different AI tools.
See [CHANGELOG.md](CHANGELOG.md) for how it has evolved.

## License

[MIT](LICENSE) © 2026 [potentiate.bio](https://potentiate.bio)
