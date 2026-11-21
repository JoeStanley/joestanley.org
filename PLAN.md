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

## Where it stands, 21 November 2026, late night

- **Built and on the site's `main`:** Start; Modules 0 to 3 (Own Your Role and Mind the Seams rebuilt in round 1); their five cards; the glossary. They print on 26 pages: each module keeps itself to three, and its full path, answers and sources' reasons may run onto two more (spec P1); each card on one; Start and the glossary on two.
- **Round 1 of job 9 is done.** Joe's editing pass of 21 November is in the repository and the doc: his edits word for word in every tab, with the fixes the pass listed (Bernadette Peters, "movie", "consumers", "the tabletop role-playing community"), "cultivate it, share it" for "shape it, spread it", *Brazil*'s "A classic film", and Klein and Kahneman's lines moved to Weigh the Evidence and Decide and Set Direction. Own Your Role and Mind the Seams are rebuilt from their preps, with Joe's four margin notes placed, each draft deleted. Departures from the preps: Graen and Scandura, never opened, left the optional exercise, which now names job crafting from Wrzesniewski and Dutton (on the full path), and the role-taking glossary term went with it; Sosa, Eppinger and Rowles's free copy isn't linked, since the prep gives no full address; Maier and Rechtin are cited by chapter title, with no edition, as Joe asked of entries; *Halt and Catch Fire* points to "the ninth episode of season 1", since Joe's edit dropped the only mention of the season.
- **New rules, each with its check and a mutation:** E3's one exception, Joe's own first-person sentences, listed in `data/pm/own-words.yaml`; S13, a source entry as a recommendation over coffee (no "borrow or buy" anywhere, no page count or running time on a built full path); S14, every time rounded Joe's way, with one total in a module's header, in every unit; M1 to M4, a margin note beside the paragraph it names (`beside`, and `at: foot`); S12, a built full path's entries name their kind. `VOICE.md` has a section on source entries. The checks now visit all four built modules: before, they looked only at Modules 1 and 2's pages.
- **Simpler source entries** are on Modules 0 and 3, and Modules 1 and 2 lost their page counts, running times and "borrow or buy". Joe agreed that every later rebuild follows them (card `simpler-entries`), and job 8 brought Modules 1 and 2's in line.
- **Print layout, job 10, done.** A module prints with its text in two thirds of the page and Joe's notes in the margin column beside it, in his hand (spec M1). A note beside a full-path source runs on past its entry, on the site and in print, and where it would meet the next note, that note waits below it (CSS anchor positioning; without it, a browser falls back to notes that may meet, which M2 catches on real notes). A paragraph with a note never breaks across pages, every note prints whole on one page (a check reads the PDF), and stacked notes keep a gap. Start, the cards and the glossary keep the full width, and a note there folds in: card `print-notes-elsewhere` asks Joe whether in his hand. Along the way: the PDF had been printing at 99.2% by accident, since a highlight reached 3px past the page and Chrome shrank every page to fit; it now prints at full size (new spec P7), and a card's Go deeper sits a step closer to its question so The Concept Champion still fits its page. The sources' reasons may run on between two sources instead of leaving a page nearly empty, and the full path's heading stays with its first source.
- **Job 8, done: Modules 1 and 2 cold-read, recut and brought in line** (pm-sources `notes/2026-11-21-job-8-modules-1-and-2.md`). A reader who wrote neither read both whole; its fixes are in, with the simpler source entries, and Meadows's book now says why to trust it (Joe's question). An unnamed "2009 literature review" left the Five Focusing Steps card: nobody could identify it. Joe picked the books in the session: Dekker's *Field Guide* for See the System, Reinertsen and *Accelerate* for Find the Constraint, so S12 now holds every built module. He also made Goodhart's Law central to Find the Constraint, "the danger to keep in mind when trying to resolve constraints": both its cards stay, and Why this matters gives it a paragraph. Fitting that on three printed pages took some trimming there (the note says what).
- **Joe's two cards of that night, carried in.** The full path's Open and Close label stays inside its own heading (new spec R10): it had been reaching every "Why this source" inside the full path, drawing a rotated orange label in place of the chevron, and "Close" sat on the rule above the first source. The list was already full width in all three engines. And every note that folds into the text, on a phone or in print on Start, a card or the glossary, carries "Sidenote:" on its own line above it, Joe's word, which screen readers also hear before every note; in print those notes are in his hand (M1, M3). New V1 baselines for the four module pages, for these and the words.
- **Drafts:** Modules 4 to 11, one file each in `drafts/pm/`, with Joe's edits in and every time rounded. None has a prep yet but those already done for 0 and 3.
- **The live site** is still the old one. The move waits until more modules are rebuilt (Joe, 18 November).
- **Waiting on Joe:** nothing.

### Joe's input not yet carried out

- **His editing pass of 21 November** (pm-sources `notes/2026-11-21-joes-editing-pass.md`): its margin notes for Modules 4 to 11, word for word but for typos and house rules, each at its module's rebuild; the simpler entries for Modules 4 to 11, at each rebuild (he agreed, card `simpler-entries`).
- His ranking for Find the Constraint (21 November, in the session): of Goodhart's Law, the five focusing steps and the dice game, the dice game adds the least, though he loves the interactive element. Nothing to do now; if that module ever needs a cut, ask him before touching the game.
- His card picks for Design for Change, Weigh the Evidence and Bring People With You, and Argyris kept as Double-Loop Learning's source behind its paywall: each at its module's rebuild ("For each rebuild").
- His cuts to the full paths (`decisions.md`, 21 November), each at its module's rebuild, where it fits S12; the module's prep says which.
- Chesterton's fence as a line in Decide and Set Direction's "Why this matters": at its rebuild.

## Jobs, in order

1. **The shape of the whole, put to Joe.** Done on 20 November: a cold read (pm-sources `notes/2026-11-20-cold-read-modules-3-to-7.md`) and six cards.
2. **Carry his answers in.** Done on 20 November: the map, who decides, the split of Modules 10 and 11, the *Mozart in the Jungle* idea and the order of the work are in the drafts and `data/pm/modules.yaml`, and Weigh the Evidence has a first draft from sources opened that day (pm-sources `notes/2026-11-20-weigh-the-evidence-sources.md`). His question on the card count went back to him as a card.
3. **The menu label.** Done on 20 November: the menu says "Product Judgment".
4. **Propose the winnowing.** Done on 20 November: pm-sources `notes/2026-11-20-winnowing-proposal.md`, every draft's cut for one card a module and for two, with the overlaps between modules settled. Joe's rulings on it are in its part 2 and in `decisions.md`.
5. **Winnow all the drafts.** Done on 21 November: all ten in the pilot's parts at their real size, one card a module and two in four modules for Joe to keep one (pm-sources `notes/2026-11-21-winnowing-done.md`).
6. **Full paths: one story each, five things at most.** Done on 21 November, from Joe's comments that night: spec S10 and S11, a story on every full path, each picked by Joe in the session, and a card for each list to cut.
7. *Run.* **Prepare each rebuild,** one module to a run, in reading order: 4, 5, 6, 7, 8, 9, 10, 11. See "Preparing a rebuild" below. Modules 0 and 3 were prepared and rebuilt on 21 November. Ready: the next run takes Module 4's prep. Where a module carried two cards, check the one Joe kept, and the line the other leaves behind. A prep run can't see the working doc, so it works from the draft and from pm-sources `notes/2026-11-21-joes-editing-pass.md`, which holds Joe's edits of 21 November.
8. **A cold read of the built modules.** Done on 21 November, by a session Joe opened, so it made the word changes itself: pm-sources `notes/2026-11-21-job-8-modules-1-and-2.md`. Modules 1 and 2 are cold-read and in the simpler style, and hold the books Joe picked (S12 now covers every built module).
9. **Rebuild the modules,** two to a round, each from its prep note, in the pilot's pattern, each draft deleted as its module is built. Each round lands in the doc for Joe to read once. Round 1, Modules 0 and 3, done on 21 November, with Joe's editing pass and its rules. Round 2, Modules 4 and 5, waits on their preps (job 7) and on his answer on each module's full-path card where it has one. A session Joe opens takes it, since it changes the syllabus's words.
10. **The print layout at two thirds.** Done on 21 November: spec M1, M2, P1 and the new P7, the layout in `pm.css` and `base.css`, checks in print and in the PDF itself, and seven mutations. V1 needed no new baseline: on screen the full path is folded, so its notes don't show in the screenshots.
11. **Go live.** A `For Joe:` pull request into `live`, and a card asking Joe what should wait for him once the site is live (`CLAUDE.md`). Waits on: Joe, since publishing is his.

When nothing above is ready, nothing else waits.

## Preparing a rebuild

Done by a run, so the session that rebuilds a module starts from checked facts. It writes `notes/YYYY-MM-DD-module-N-prep.md` in pm-sources and changes nothing in this repository but this page.

- Open and check every source the winnowed draft cites: the address works, it says what the draft says it says, it is free if it is on the short path, and its "Why trust it" holds. Name what you could not open.
- Settle each flag for the module in pm-sources `notes/2026-11-20-readers-flags.md`, and each "To check:" line in the draft, from the sources.
- For a module that leans on the deck, use `citation-map.md` and `finds.md` in pm-sources, and name the original work to cite in place of each deck page.
- Check the module's story (spec S10), already in its draft (job 6): open enough of it, or of transcripts and reviews, to be sure the draft describes it exactly. A better one may replace it.
- Recut the full path on S12: at least two books beside the story, each read whole or in long parts, nothing else under about 30 minutes, and five things at most (S11). Where Joe's answered cut already fits, note it for the rebuild and ask nothing. Otherwise bring him the whole list as a card, books first, with your recommendation: a short piece may give way to its author's book (Reilly's talk to her book, Schulz's talk to hers), and a cut book may come back. Open and check every book you'd add: its publisher's page and table of contents at least, and the parts you'd assign where a preview allows.
- Draft the module's source entries as Joe asked on 21 November (`decisions.md`): a recommendation shared in conversation, with no edition where context makes it clear, no "Borrow it or buy it", and no page count or running time on the full path. Once round 1 has been through Joe, follow how its two modules read.
- Say where each of Joe's margin notes for the module will sit once it's built (pm-sources `notes/2026-11-21-joes-editing-pass.md`).
- Anything that needs Joe goes on the Decisions page as a card.

## For each rebuild

- Work from the module's prep note. Read the draft, its tab's comments and his edits there.
- Where a module carried two cards, keep the one Joe picked (`decisions.md`, 21 November) and give the other its line in the module. Then rewrite any Check question or exercise that rested on the card that went: the cold read of 21 November found some in Modules 5, 7 and 11. Own Your Role's is done in its draft. Read, too, the research tab in the doc's frozen Notes that goes with it, if any: the concept champion (Module 0), agency and cohesion (now in Module 8), value created, value captured (Module 9).
- Place Joe's margin notes for the module, word for word but for typos and house rules (`CLAUDE.md`), beside the paragraph or source each is about (pm-sources `notes/2026-11-21-joes-editing-pass.md`), and answer each one's thread.
- Change Safely: its short path teaches DORA's four delivery measures, which *Accelerate* on Find the Constraint's full path now picks too. Point back to Module 2 rather than teach them as new (job 8's second cold read).
- Make the full path Joe picked on the module's card, so it holds five things at most, its story included (S11), and at least two books (S12). Each book's entry opens "A book" or "A textbook" and names the chapters to read, or says to read it whole. Where the cut takes the last trace of an idea, give it a line or say so.

## To post in the doc

What a run would have said in the working doc, for the next session Joe opens to post and then delete here.

- None.

## To put to Joe

Cards a session could not put on the Decisions page itself. The next session that can moves each one there and deletes its line.

- None.
