# Community phase: 90-day starter plan + channels + anti-patterns + consistency log

**Area**: community / discoverability / post-launch growth

**Refs**:
- [`README.md`](../../README.md), [`docs/index.html`](../../docs/index.html) — the surfaces a visitor lands on after community work drives them there
- [`ai-engineer-summit-cfp.md`](./ai-engineer-summit-cfp.md) — one specific community-phase action already tracked separately
- [`reach-tool-maintainer.md`](./reach-tool-maintainer.md) — one specific partnership-shaped action already tracked separately
- [`agents-md-case-study-pr.md`](./agents-md-case-study-pr.md), [`demo-asset-90sec-recording.md`](./demo-asset-90sec-recording.md) — adjacent community assets

## Context

The project shipped 2026-06-11. The single biggest risk to adoption is **discoverability** — the artifact is good, the landing page is honest, the disciplines are real, but no one finds it without intentional community work. This TODO is the work plan + the consistency-tracking convention.

Framing: this is a **learning** plan, not a launch plan. The goal is to develop the content-and-community muscle, not to maximise reach in 90 days. Sustained presence over 12 months beats any 30-day burst. Cap each month around 4–6 hours total. Sustainable beats heroic.

### Three modes of community work

| Mode | What it is | Why it matters |
|---|---|---|
| **Write** | Posts, essays, case studies, tutorials. One discipline per post. | Builds citable assets that outlive social media impressions. Establishes author-of-an-idea identity, not just repo-maintainer identity. |
| **Show up** | Replies in others' threads. PRs to adjacent projects. Comments on ecosystem posts. | People discover you through your replies more than through your posts in year one. Hardest mode mentally — feels like self-promotion when you're new. Get over it. |
| **Partner** | Integrations with adjacent tools. Cross-references in others' docs. Co-authored posts. | Compounds — one good partnership > 6 months of solo posts. Realistic only after you have something to point at (which you do). |

Engineer's failure mode is 100% Write, 0% Show up, 0% Partner. Force at least 30% Show up, 10% Partner.

### 90-day starter plan

#### Month 1 — Find where the conversation is

- [ ] Identify 5–8 channels (see ranking below)
- [ ] 30 minutes/day for 2 weeks: read, don't post — learn local culture / live debates / in-jokes
- [ ] Write down 10 questions seen in the wild that the bootstrap is an honest answer to (these become future post topics)
- [ ] **Pass log:** `____-__-__ — completed:` *(fill in on completion + 1-line retrospective)*

#### Month 2 — Ship the first post + start showing up

- [ ] Pick the strongest discipline (suggested: prompt-file convention — most extractable, most novel-shaped, copyable in 5 minutes)
- [ ] Write 1500–2500 word post, bootstrap mentioned only at end as one delivery vehicle
- [ ] Publish on owned blog → cross-post (dev.to, Hashnode, Medium)
- [ ] Submit to HN once (save for strongest content)
- [ ] Reply to 10 questions seen in Month 1 with helpful answers (no link unless literally asked for a tool)
- [ ] **Pass log:** `____-__-__ — completed:` *(fill in on completion + 1-line retrospective)*

#### Month 3 — Iterate + find one partner

- [ ] Look at which Month 2 reply got engagement → that's Month 3 post topic
- [ ] Ship second post (same length, same structure — the cadence muscle matters more than the topic)
- [ ] Identify one adjacent project worth partnering with (PR to awesome-list, Discussion in adjacent repo, contribute an example)
- [ ] Open one partnership-shaped conversation (GitHub issue, DM, email — low-stakes)
- [ ] **Pass log:** `____-__-__ — completed:` *(fill in on completion + 1-line retrospective)*

### Channels ranked by signal-to-noise

| Rank | Channel | Why | What to do |
|---|---|---|---|
| 1 | **Reddit** (`r/ClaudeAI`, `r/cursor`, `r/aider`, `r/LocalLLaMA`) | Active, specific, less hype than Twitter | Reply to questions; submit posts occasionally |
| 2 | **GitHub** (Discussions on adjacent projects, awesome-lists, PRs) | Asynchronous, discoverable forever, low-stakes | PR project to awesome-lists; open Discussions in adjacent repos |
| 3 | **Hacker News** | One good post > 6 months of Twitter | Save for strongest content; don't spam |
| 4 | **Twitter/X** | Real but noisy; niche reach is real | Reply more than post; build slowly |
| 5 | **Discord** (Aider, Cursor, Continue) | Real but ephemeral — conversations evaporate | Show up occasionally; don't optimise for it |
| 6 | **LinkedIn** | Rarely converts dev audiences | Skip unless a B2B angle emerges |

### Anti-patterns to avoid

1. **Launch-and-pray.** Posting "I built this!" simultaneously to 10 places day-one. Burst → silence → nothing. Sustained > burst.
2. **"Why my tool is better than X" post.** Always reads defensive. Write FOR the audience, not AGAINST competitors.
3. **Discord before there's an audience.** 3-person Discord actively hurts — visitors see low activity and bounce.
4. **The "engagement" treadmill.** Don't tune posts for metrics. Tune for the one reader who'd benefit.
5. **The "consistency" cult.** Weekly posts because "you have to" produces low-quality work that erodes credibility. Monthly with care > weekly with filler.

### Consistency-tracking convention

Each month, edit *this file* in place:

1. Tick the checkboxes that month
2. Fill in the "Pass log" line with the date + one-line retrospective (*what worked, what didn't, what surprised*)
3. Commit with message: `community-phase: month <N> log — <one-line summary>`

The file's `git log` becomes the audit trail of consistency. Three rules:

- **No deleting the TODO until 6+ consecutive months of consistent participation** (the practice is self-sustaining at that point).
- **If 3 consecutive months show zero participation**, the plan failed. Decide whether to relaunch (edit the plan based on what you learned) or close the TODO (acknowledge community work isn't the right investment right now). Don't let it rot silently.
- **After Month 3 of the original plan**, decide: extend (Month 4 / 5 / 6 with adjusted plan) or pause.

## Deferred because

Community work doesn't fit a single commit — it's a months-long practice. Tracking the plan + the consistency check as a TODO is the correct shape; the file lives until the practice becomes self-sustaining or is explicitly retired.

## Revisit when

Monthly — first revisit: **2026-07-12** (one month from this entry's creation). Edit in place with the month's retrospective. Stop revisiting when either 6 consecutive months show consistent participation (practice established) OR 3 consecutive months show zero participation (plan failed — relaunch or close).
