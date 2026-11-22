# joestanley.org: standing instructions

Joe Stanley's personal site: a front door, a ReadMe, the syllabus On Product Judgment (Product Judgment in the menu), Writing and Games. Built with Hugo 0.141.0 extended and a small theme kept in this repo. Joe owns it; Claude does the work in Claude Code sessions. This repository is public, and holds what the site needs: the site, its spec and checks, its tools and its workflows. The working record is private, in JoeStanley/pm-sources (Joe, 22 November 2026): his decisions, newest first (`decisions.md`), what comes next and where the work stands (`PLAN.md`), the voice guide (`VOICE.md`), the Decisions page's source, the working notes (`notes/`), and its own `CLAUDE.md`, which says how the record is kept and how to work with Joe. Wherever this page names one of those, it means pm-sources' own. A session needs nothing from Joe to start: what he has to say is already on the Decisions page, in the working doc or in his first message.

## Start of every session

1. `bash tests/setup.sh`, then export the `HUGO` and `CHROME` values it prints on its last line.
2. Attach pm-sources. A session Joe opens and the daily run both start with it cloned beside this repository, at `../pm-sources`. If it isn't there, attach it with `add_repo` (owner `JoeStanley`, repository `pm-sources`, push access), clone it beside this repository as the tool's answer says, and register it with `register_repo_root`. If it can't be attached, stop and say so: the plan and the decisions are there.
3. Read pm-sources' `CLAUDE.md`, `decisions.md` and `PLAN.md`, and `tests/SPEC.md` here. Before you touch the syllabus's words, read `VOICE.md` too.
4. Gather what Joe has left since the last session: his answers on the Decisions page (cards whose `status` is `answered`), his comments, suggestions and edits in the working doc (see "The working doc" below), and the cards listed in `PLAN.md` under "To put to Joe". A session Joe opens also posts what waits in `PLAN.md` under "To post in the doc".
5. Look at the open pull requests from earlier sessions, in both repositories. If one has a failed check, fix it on its own branch before new work, and turn auto-merge back on if it is off.
6. Take the job. If Joe's first message names one, that is the job. Otherwise take the first job in `PLAN.md` that is ready and that no open pull request already covers, preferring one not marked *Run*, since a run cannot do it. What he has left (answers, suggestions, comments, edits) is carried in first, whatever the job, in the same pull request as the job: there are no separate passes for it.
7. Work on a branch named `claude/<short-topic>`, from an up-to-date `main`, with the same name in each repository the job changes.

## End of every session

1. Record each answer from the Decisions page in `decisions.md`, then mark its card recorded (pm-sources' `CLAUDE.md`, "Decisions").
2. Put every decision you need from Joe on the Decisions page as a card, not in chat and not in the doc.
3. Bring `PLAN.md` up to date: "Where it stands", what this session did to its job, new jobs where they belong, and his input not yet carried out.
4. Put changed tabs back in the working doc and answer his comments ("The working doc", steps 3 to 6).
5. One pull request in each repository the session changed, then stop: pm-sources' first, merged at once, then this one's, by auto-merge ("Pull requests and merging").
6. The last message: a line or two on what changed, then what waits on Joe, each with its link. Nothing else.

## Until Joe's final voice pass

Joe's picks of 22 November 2026, after the cold read of the whole. They hold until his final voice pass (job 23 in `PLAN.md`). After that, this section comes out and the rules below hold as written.

- **More agency.** Sessions do the structure, sourcing and practice first, and Joe makes one voice pass last. Where any part can be refined, even at the highest levels of intent (the map, a module's question, the thesis on Start, how a unit is built), bring the change to him as a decision, with your pick first.
- **His words are open.** A session may cut, move or reword his words in the syllabus: his sentences in a module, the source entries he wrote, his margin notes and Start's words. This lifts "Margin notes are Joe's" below, and the minor-revision limit on his own sentences (E3). Two things still hold. Never write a new "I" sentence, an experience or an opinion for him. Never write a new margin note in his name. Where a passage needs his voice, keep his line as raw material and leave a brief of what it now has to do, in a voice slot: an entry in `data/pm/voice-slots.yaml`, placed with `{{< pm/voice "id" >}}` (spec X4). The site shows its interim words, the doc shows its brief, and publishing fails while any slot is open. The front door, the ReadMe and Writing stay his.
- **Tell him what moved.** Each pull request, and each changed tab's thread in the doc, says which of his words were cut, moved or changed, and each goes under `moved:` in `data/pm/voice-slots.yaml`, which the doc's "Your voice pass" tab lists. That way his final pass starts from one list.

## How a change is made

- **Spec first.** Change `tests/SPEC.md`, then the site, then the check in `tests/check_site.py`. A change that makes a check fail is not done.
- **Check before every push:** `python3 tests/check_site.py`. When a check changes, also run `bash tests/mutations.sh` and add a mutation that proves the new check catches what it is for.
- **V1 (screenshots) runs here, not on GitHub.** A change to content alone may record a new baseline with `--update-baseline` in the same pull request, and says so. A change to the look needs Joe's word first: describe it to him before you make it. If V1 fails on an unchanged look because this environment renders differently, record the baseline again from `main` before your change, in its own commit, and say so.
- **The look is locked** (`tests/SPEC.md`, V2): two stylesheets, `base.css` and `pm.css`; no switches for alternative looks, directions or hands. To propose a change, describe it to Joe first. Pictures may use colors of their own, as long as they stay in the family (C7).
- **Words:** American English. No em dashes anywhere (T3). Plain, short sentences. Joe's own wording is a direction, not a quotation: his sentences in a unit and his suggestions in the doc may be revised in minor ways wherever that serves a larger goal, such as cohesion or clarity, or where it reads as management-speak. Preserving his words at the cost of the whole is the mistake to avoid. Where you hesitate, put it to him as a decision (Joe, 21 November 2026). The syllabus has a voice of its own, a mentor talking to a mentee: `VOICE.md` says how, and rules E1 to E4 hold it. Only Joe says "I": never write an experience or an opinion for him.
- **Examples** come from across complex technical product work, and none describes Joe's own employer, team or platform (S5, S6). This repository is public. Nothing about his work goes in it beyond what his ReadMe or LinkedIn already shows, and then only in his own words, such as a margin note. Never name his employer, or imply they support anything here (Joe, 21 November 2026).
- **Licensing** (`LICENSE`, `LICENSE-content.md`, spec L1): new code is MIT; new syllabus text and figures are CC BY 4.0; anything else Joe writes is all rights reserved unless he says otherwise. Quote other authors briefly and credit them; their words stay theirs.
- **Margin notes are Joe's** (until his final voice pass, see above). Never write or delete what is between the quotes in `data/pm/margin/*.yaml`, beyond placing a note he wrote in its slot, word for word. You may fix a typo or a house rule in one (no em dashes, American spelling) and tell him; anything more goes to him as a card with your proposed wording. His notes are meant to be looser, more casual and tangential than the syllabus, so never smooth them toward its voice (Joe, 21 November 2026). A note beside one paragraph names that paragraph by a few of its words (`beside`); when a paragraph is reworded, keep those words or move the note with it. After a unit changes, run `python3 tools-pm/margin-slots.py public` (after a build) to keep the slots in step; it keeps every note. His own first-person sentences in a module are listed in `data/pm/own-words.yaml` (E3). Revise one only in a minor way that serves the unit, change the list in the same change, and tell him what changed and why, in the pull request and in the doc.
- **PDF:** `python3 tools-pm/make-pdf.py public out.pdf "On Product Judgment, pilot draft, <date>"` after `$HUGO`. Render and look at every page before handing a PDF to Joe.

## Pull requests and merging

- One pull request per piece of work, into `main`. The title says what changes for a reader.
- **pm-sources merges at once.** It has no checks, so a session merges its own pull request there with a merge commit as soon as it's open, before it opens this repository's, so the record already says what this one holds when it merges. If this one's checks then fail, the next session fixes it ("Start of every session", step 5).
- **Merge your own pull request into `main` by auto-merge, then stop** (Joe's decision, 20 November 2026). Open the pull request, turn on auto-merge with a merge commit, and end the turn without watching it. GitHub merges it once the `checks` workflow passes, so nothing wakes the session again. A session left waiting is woken by every CI event and re-reads its whole context each time. If a check fails, the next session fixes it ("Start of every session", step 5).
- **If GitHub refuses auto-merge** (the setting is off, or `checks` is not a required check), watch the pull request instead and merge it once every check has passed. Ask GitHub twice for the merge state: it reads `unknown` for a few seconds after a push. Stop watching the moment it merges.
- **Before the site goes live, only a merge that is costly to undo or irreversible waits for Joe** (his decision, 19 November 2026). A change to the look or to his own words that he asked for, or has seen in the session, merges like any other: lead the description with what he would want to know, show him the result, and merge.
- **Leave for Joe**, with a title starting `For Joe:` and a description that leads with the decision he is asked to make:
  1. Publishing: any pull request into `live`. Nothing reaches joestanley.org except through `live`, and only `publish.yml` deploys it, after the same checks pass.
  2. Any other merge that is costly to undo or irreversible.
- **Once the site is live, ask Joe what should wait for him again.** Until he says, hold what waited before 19 November: any change to the look (stylesheets, templates, fonts, figures, the hand-drawn marks, or a new V1 baseline that is not for content alone), and anything in his own voice (the ReadMe's words, the front door's lines, a Writing post's text).
- Never force-push to `main` or `live`. Never change repository settings; GitHub refuses them from a session. Write them up for Joe as numbered clicks.

## The syllabus

- Twelve modules, listed in `data/pm/modules.yaml`. Each is either built (a page under `content/pm/`) or a draft (one file under `drafts/pm/`, the module with its cards), never both (X1). A draft is not on the site. When you rebuild a module, delete its draft in the same change.
- Module 3, Find the Constraint, is the pilot: rebuild the other modules in its pattern (`content/pm/find-the-constraint.md`, its cards in `content/pm/cards/`, `data/pm/`).
- Open and check every source before a module is rebuilt. In a draft, mark what nobody has opened yet with a line that starts "To check:". No built unit may carry one (S7).
- **Ruth Malan's deck**, her February 2025 workshop notes, which the older drafts cite as "deck p.", is in pm-sources too: the PDF, its text one file per page, a map of every deck reference in the drafts, and what a full read found for each module. Search it rather than reading it whole. Cite the works it points to, and the deck only for Malan's own insight (S8). Nothing from the deck comes here beyond a brief, credited quote.
- The short path uses only freely available sources; books go on the full path. Every recommended source says why to trust it and what only it gives the reader (S2).
- The whole syllabus should read as manageable, not overwhelming. It aimed at about 50 printed pages; after the pilot Joe set the target at about 75, as it runs: each module's own text keeps to three pages, and its optional full path and back matter add about two more (21 November 2026).
- Pilot first: build one piece, get Joe's reaction, then replicate. Ask Joe before a format becomes fixed.

## The working doc

Joe reviews the syllabus in one Claude Docs document, "On Product Judgment: Working Source": https://claude.ai/artifact/66JD4LSrrxJ3W9Mnbv5UjJ. It has a tab for each unit. The repository is the source and the doc mirrors it (X1 to X3). Keep it that way:

1. **Read the doc first.** `tools-pm/source-doc.lock.json` holds each tab's ids and the revision it had when it was last written. On each tab, list the comments and the open suggestions (a `read` with `{"kind": "suggestions"}`), and read the tab with `sinceRev` set to that revision: what comes back is what Joe changed, his suggestions shown as `<ins>` and `<del>`. His comments, suggestions and edits are the brief.
2. **Carry them into the repository**, spec first, like any change. Never edit the doc in place of the repository. Apply each of his suggestions, within the rules here (T3, the voice), revising its words in minor ways where that serves cohesion or clarity, and say so in its thread. Where his intent is unclear, ask: with picks when he is in the session, otherwise as a reply on the suggestion's card or in the comment's thread, and leave it open.
3. **Close what's done, before writing tabs back.** Once the repository holds a suggestion's change, accept the suggestion: one `decide` call each, since the connector refuses them in a batch. Where the repository's words differ from the suggestion's, accept it all the same and correct the words in step 4. Once the repository holds what a comment asked for, answer it and resolve its thread with `"resolveAskedIn": "chat"`. The connector allows both only when Joe has asked for it in the session's own chat, as his usual first message does: "Take the next job. Apply my suggestions and resolve what's done." Without that, answer in the thread and leave the card and the thread open for him. On each tab the session writes back, older open threads are closed the same way when the repository already holds what they asked.
4. **Put the result back.** After `$HUGO`, run `python3 tools-pm/source-doc.py public out/`. It writes each tab as Markdown and says which have changed. Bring each changed tab in the doc into line with its file: replace its contents, or, where a few words changed, replace just those words. Rename a tab when its module is renamed.
5. **Record it.** `python3 tools-pm/source-doc.py public --record "Start=12" "2 Find the Constraint=40"`, with each written tab's new revision. Commit the lock with the change. X3 fails until you do, so no change to the syllabus's words merges without reaching the doc.
6. **Answer every comment** in its own thread, in a line or two: what changed, or why nothing did.

The Notes tabs at the end of the doc are history, frozen on 20 November 2026: read them, but add nothing there. New working notes (research write-ups, reviews, anything that mentions Joe's own work) go in `notes/` in pm-sources, never in this one.

Research needs the web. The Joestanley.org environment has full web access (Joe, 20 November 2026). When a site still refuses, say so plainly, mark what you could not open with "To check:", and name the site in `PLAN.md`. Do not pass off a search result or a memory as a source you opened.

## Decisions

Joe decides on one private page, the Decisions page: https://claude.ai/artifact/QGLpeYcbz14tPBAPiQSYGq. pm-sources' `CLAUDE.md` says how a card is written, how his answer is read and recorded, and how to work with him.

## The daily run

A scheduled task, "joestanley.org daily run", starts a fresh session every day at 02:43 UTC. Its first message begins "Daily run", and a session whose first message begins so is a run. A run works like any session, with three differences: it asks Joe nothing, and puts what it needs from him on the Decisions page; it takes only a job that waits on nothing; and if no job is ready and no answer waits to be recorded, it stops with no branch and no pull request. It starts with pm-sources beside it and merges like any session, one pull request in each repository it changed. Joe pauses or changes it in his list of scheduled tasks on claude.ai.

- **Its branch.** A run works on the branch its session names, in place of `claude/<short-topic>`, and restarts it from `main` once its last pull request has merged.
- **Another session first.** Before it takes a job, a run checks that nobody else is at work: if any branch but `main` was pushed to either repository in the last hour, it stops, and the next run tries again.
- **No working doc.** A scheduled task cannot carry the Claude Docs connector, so a run never sees the working doc. It takes only jobs marked *Run* in `PLAN.md`, which change none of the syllabus's words, and X3 must pass on its pull request, which proves no tab changed. It skips the doc in step 4 of the start and step 4 of the end: what it would say in a thread goes in `PLAN.md` under "To post in the doc". Joe chose this on 20 November 2026, so that no run works against an edit he made in the doc.
