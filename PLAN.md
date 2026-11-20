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

- **Starting a session.** The daily run starts one every day at 02:43 UTC. When Joe opens one himself, his first message can always be the same: "Take the next job." The session finds everything else here and in `CLAUDE.md`.
- **Which job.** The first job below that is ready and that no open pull request already covers. A job that waits on Joe is skipped until his answer is in.
- **Ending a session.** `CLAUDE.md`, "End of every session": record his answers, put new questions on the Decisions page, update this page, sync the doc, one pull request by auto-merge.

## Where it stands, 20 November 2026

- **Built and on the site's `main`:** Start; Module 1, See the System; Module 2, Find the Constraint (the pilot); their three cards; the glossary. They print on 12 pages.
- **Drafts:** the other ten modules, with 32 cards between them, one file each in `drafts/pm/`. `data/pm/modules.yaml` says where each stands. Six are in the old format and still lean on Ruth Malan's deck; four are first drafts in the pilot format that run long on purpose.
- **The live site** is still the old one. The move to the new site waits until more modules are rebuilt (Joe, 18 November).
- **The way of working** moved fully into Claude Code on 20 November. The Cowork project is retired, the deck is in pm-sources, the environment has full web access, and a daily run takes the next ready job.

### Joe's input not yet carried out

From his comments of 20 November in the working doc. Each is answered in its thread and belongs to a job below.

| His comment | Where | Job |
| --- | --- | --- |
| The list of modules on the Start page, at "6 Think With Engineers", feels like a hodgepodge: review it and the related modules cold. | Start tab | 1 |
| Put the decisions about the shape of the whole to him as picks. | Notes, Recommendation | 1 |
| The idea from *Mozart in the Jungle*: the best work comes from passion and a personal voice, and technical perfection alone is soulless. It goes somewhere in the syllabus. | Module 0 tab | 1, then 3 |
| The menu label "PM Syllabus" is too clinical. | Notes, Open items | Card on the Decisions page, then 2 |

## Jobs, in order

1. **The shape of the whole, put to Joe.** Waits on: nothing.
   - First a cold read, by a reader who did not write them, of the Start page's list of modules and of Modules 3 to 7, the ones around Think With Engineers. Then answer Joe's "hodgepodge" comment in its thread with what it found.
   - Then cards on the Decisions page: the map (twelve modules, their order and titles, after the cold read); the cut between Notice When You Are Wrong and Bring People With You; where Agency and Coherence lives (a card in Mind the Seams today); where the *Mozart in the Jungle* idea goes; the order of the work (cut all the copy down first, or rebuild module by module and cut each as it is built); and which cards stay, or that this waits for the page count from job 4.
   - Done when: the cards are on the page and the comment is answered.
2. **Carry his answers in.** Waits on: his answers to job 1's cards and to the menu card, each part as it lands. `data/pm/modules.yaml`, the Start page, the drafts, and the menu label in `hugo.yaml`. Done when: every answered card is recorded and done.
3. **Rebuild Module 0, Own Your Role,** in the pilot's pattern: sources opened and checked, 90 minutes, three printed pages, its draft deleted. Waits on: job 1's answers on the map and on the *Mozart in the Jungle* idea.
4. **Rebuild Module 5, Change Safely,** then measure what the whole would print at, and put the page target to Joe as a card: raise the target, or cut. Waits on: job 1's answer on the order of the work.
5. **Cut to the target** Joe picks, across what is built and drafted. Waits on: job 4's card.
6. **Rebuild the rest** in reading order, two modules to a round: 3, 4, 6, 7, 8, 9, 10, 11. Each round lands in the working doc for Joe to read once. Waits on: job 5.
7. **Go live.** A `For Joe:` pull request into `live`, and a card asking Joe what should wait for him once the site is live (`CLAUDE.md`). Waits on: Joe, since publishing is his.

When nothing above is ready, take one of these:

- **Mesmir's voice guide.** Attach JoeStanley/mesmir, read the voice guide its Head of Brand keeps, and put to Joe as a card what, if anything, should carry over into `VOICE.md`. `VOICE.md` was written from his direction without it.

## For each rebuild

- Read the module's draft, its sources and its tab's comments. Read, too, what the readers flagged for that module in the doc's frozen Notes tab "Open items, 20 November", and the research tab that goes with it, if any: the concept champion (Module 0), agency and cohesion (Module 3), value created, value captured (Module 9).
- For a module that leans on the deck, attach pm-sources and use `citation-map.md` and `finds.md`.

## To put to Joe

Cards a session could not put on the Decisions page itself. The next session that can moves each one there and deletes its line.

- None.
