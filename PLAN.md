# The plan

What comes next for joestanley.org and On Product Judgment, and where the work stands, kept so that no session needs Joe to brief it. Every session reads this after `CLAUDE.md` and leaves it up to date before it ends. Joe's own decisions are in `decisions.md`; this page holds the order of the work, not his rulings.

## How the work moves

| Who | Where | What |
| --- | --- | --- |
| Joe decides | [Decisions page](https://claude.ai/artifact/QGLpeYcbz14tPBAPiQSYGq) | One card per decision, options with the session's pick first. He taps an answer. `CLAUDE.md`, "Decisions", says how a card is written and read. |
| Joe reads and comments | [Working doc](https://claude.ai/artifact/66JD4LSrrxJ3W9Mnbv5UjJ) | The syllabus's words, a tab per unit, mirrored from this repository. |
| Joe publishes | A `For Joe:` pull request into `live` | Nothing else waits for him in GitHub. |
| A session works | This repository | The words, the rules, this plan, his decisions. |
| A session keeps notes | `notes/` in JoeStanley/pm-sources (private) | Research write-ups, reviews, anything that mentions Joe's own work. |

- **Starting a session.** The daily run starts one every day at 02:43 UTC. When Joe opens one himself, his first message can always be the same: "Take the next job. Apply my suggestions and resolve what's done." The second sentence is what lets a session accept his suggestions and resolve his threads in the doc. The session finds everything else here and in `CLAUDE.md`.
- **Runs and the doc.** A run cannot reach the working doc, so it takes only jobs marked *Run*, which change none of the syllabus's words. Everything else waits for a session Joe opens, which sees his newest edits (Joe, 20 November).
- **Which job.** The first job below that is ready and that no open pull request already covers: for a run, the first marked *Run*; for a session Joe opens, the first not marked *Run*, if one is ready, since a run cannot do it. A job that waits on Joe is skipped until his answer is in.
- **Ending a session.** `CLAUDE.md`, "End of every session": record his answers, put new questions on the Decisions page, update this page, sync the doc, one pull request by auto-merge.

## Where it stands, 21 November 2026

- **Built and on the site's `main`:** Start; Module 1, See the System; Module 2, Find the Constraint (the pilot); their three cards; the glossary. They print on 12 pages.
- **Drafts, winnowed:** the other ten modules, one file each in `drafts/pm/`, all now in the pilot's parts at their real size (job 5). Each module's text is about 650 to 750 words, so it fits three printed pages once a "Last time" joins it, and runs 41 to 70 minutes. Full paths are long, as Joe chose. Each card is about 360 words. `data/pm/modules.yaml` says what the cut did to each, and pm-sources `notes/2026-11-21-winnowing-done.md` says where it departed from the proposal.
- **Cards:** one a module, as Joe aimed. Four modules carry two, for him to keep one: Own Your Role (The Concept Champion or Curious and Opinionated), Design for Change (Coupling Is About a Change or Pace Layers), Weigh the Evidence (The Law of Small Numbers or The McNamara Fallacy) and Bring People With You (The Trust Equation or SCR). That's 14 cards drafted, 10 once he picks: with the built units, about 52 to 62 pages in all.
- **The deck** is cited only for Ruth Malan's own lines (Mind the Seams, p. 314; Design for Change, p. 329), and in "To check:" lines that name where an unopened quote was copied from.
- **The live site** is still the old one. The move waits until more modules are rebuilt (Joe, 18 November).
- **Waiting on Joe,** on the Decisions page: which card each of the four modules keeps; whether every title takes the "Data-Informed, Not Data-Driven" form (`title-convention`); whether Own Your Role's question changes; and whether Double-Loop Learning's source may sit behind a paywall. And his read of the winnowed syllabus in the doc.

### Joe's input not yet carried out

- His direction that the full path prints outside a module's three pages changes spec P1 and its check. That waits for the first rebuild whose full path needs the fourth page (job 7).

His suggestions of 20 November on the Start tab are in the repository and accepted in the doc.

## Jobs, in order

1. **The shape of the whole, put to Joe.** Done on 20 November: a cold read (pm-sources `notes/2026-11-20-cold-read-modules-3-to-7.md`) and six cards.
2. **Carry his answers in.** Done on 20 November: the map, who decides, the split of Modules 10 and 11, the *Mozart in the Jungle* idea and the order of the work are in the drafts and `data/pm/modules.yaml`, and Weigh the Evidence has a first draft from sources opened that day (pm-sources `notes/2026-11-20-weigh-the-evidence-sources.md`). His question on the card count went back to him as a card.
3. **The menu label.** Done on 20 November: the menu says "Product Judgment".
4. **Propose the winnowing.** Done on 20 November: pm-sources `notes/2026-11-20-winnowing-proposal.md`, every draft's cut for one card a module and for two, with the overlaps between modules settled. Joe's rulings on it are in its part 2 and in `decisions.md`.
5. **Winnow all the drafts.** Done on 21 November: all ten in the pilot's parts at their real size, one card a module and two in four modules for Joe to keep one (pm-sources `notes/2026-11-21-winnowing-done.md`).
6. *Run.* **Prepare each rebuild,** one module to a run, in reading order: 0, 3, 4, 5, 6, 7, 8, 9, 10, 11. See "Preparing a rebuild" below. Ready. Where a module carries two cards, check both, since Joe may keep either.
7. **Rebuild the modules,** two to a round, each from its prep note, in the pilot's pattern, each draft deleted as its module is built. Each round lands in the doc for Joe to read once. The first rebuild whose full path runs past the module's three pages changes spec P1 and its check, with a mutation: the module through Check yourself on three pages, and with its full path on four at most (Joe, 20 November). Waits on: each module's prep, and, in Modules 0, 5, 7 and 11, Joe's pick of a card.
8. **Go live.** A `For Joe:` pull request into `live`, and a card asking Joe what should wait for him once the site is live (`CLAUDE.md`). Waits on: Joe, since publishing is his.

When nothing above is ready, nothing else waits.

## Preparing a rebuild

Done by a run, so the session that rebuilds a module starts from checked facts. It writes `notes/YYYY-MM-DD-module-N-prep.md` in pm-sources and changes nothing in this repository but this page.

- Open and check every source the winnowed draft cites: the address works, it says what the draft says it says, it is free if it is on the short path, and its "Why trust it" holds. Name what you could not open.
- Settle each flag for the module in pm-sources `notes/2026-11-20-readers-flags.md`, and each "To check:" line in the draft, from the sources.
- For a module that leans on the deck, use `citation-map.md` and `finds.md` in pm-sources, and name the original work to cite in place of each deck page.
- Anything that needs Joe goes on the Decisions page as a card.

## For each rebuild

- Work from the module's prep note. Read the draft, its tab's comments and his edits there.
- Where a module carried two cards, keep the one Joe picked and give the other its line in the module. Then rewrite any Check question or exercise that rested on the card that went: the cold read of 21 November found some in Modules 5, 7 and 11. Read, too, the research tab in the doc's frozen Notes that goes with it, if any: the concept champion (Module 0), agency and cohesion (now in Module 8), value created, value captured (Module 9).

## To post in the doc

What a run would have said in the working doc, for the next session Joe opens to post and then delete here.

- None.

## To put to Joe

Cards a session could not put on the Decisions page itself. The next session that can moves each one there and deletes its line.

- None.
