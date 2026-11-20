# joestanley.org: standing instructions

Joe Stanley's personal site: a front door, a ReadMe, the PM Syllabus (its title is On Product Judgment), Writing and Games. Built with Hugo 0.141.0 extended and a small theme kept in this repo. Joe owns it; Claude does the work in Claude Code sessions. Joe's decisions are in `decisions.md`, newest first. What comes next, and where the work stands, is in `PLAN.md`. Read both, and `tests/SPEC.md`, before changing anything. A session needs nothing from Joe to start: what he has to say is already on the Decisions page, in the working doc or in his first message.

## Start of every session

1. `bash tests/setup.sh`, then export the `HUGO` and `CHROME` values it prints on its last line.
2. Read `decisions.md`, `PLAN.md` and `tests/SPEC.md`. Before you touch the syllabus's words, read `VOICE.md` too.
3. Gather what Joe has left since the last session: his answers on the Decisions page (cards whose `status` is `answered`), his comments and edits in the working doc (see "The working doc" below), and the cards listed in `PLAN.md` under "To put to Joe".
4. Look at the open pull requests from earlier sessions. If one has a failed check, fix it on its own branch before new work, and turn auto-merge back on if it is off.
5. Take the job. If Joe's first message names one, that is the job. Otherwise take the first job in `PLAN.md` that is ready and that no open pull request already covers. Answers he has left are carried in first, whatever the job.
6. Work on a branch named `claude/<short-topic>`, from an up-to-date `main`.

## End of every session

1. Record each answer from the Decisions page in `decisions.md`, then mark its card recorded (see "Decisions" below).
2. Put every decision you need from Joe on the Decisions page as a card, not in chat and not in the doc.
3. Bring `PLAN.md` up to date: "Where it stands", what this session did to its job, new jobs where they belong, and his input not yet carried out.
4. Put changed tabs back in the working doc and answer his comments ("The working doc", steps 3 to 5).
5. One pull request, by auto-merge, then stop ("Pull requests and merging").
6. The last message: a line or two on what changed, then what waits on Joe, each with its link. Nothing else.

## How a change is made

- **Spec first.** Change `tests/SPEC.md`, then the site, then the check in `tests/check_site.py`. A change that makes a check fail is not done.
- **Check before every push:** `python3 tests/check_site.py`. When a check changes, also run `bash tests/mutations.sh` and add a mutation that proves the new check catches what it is for.
- **V1 (screenshots) runs here, not on GitHub.** A change to content alone may record a new baseline with `--update-baseline` in the same pull request, and says so. A change to the look needs Joe's word first: describe it to him before you make it. If V1 fails on an unchanged look because this environment renders differently, record the baseline again from `main` before your change, in its own commit, and say so.
- **The look is locked** (`tests/SPEC.md`, V2): two stylesheets, `base.css` and `pm.css`; no switches for alternative looks, directions or hands. To propose a change, describe it to Joe first. Pictures may use colors of their own, as long as they stay in the family (C7).
- **Words:** American English. No em dashes anywhere (T3). Plain, short sentences; Joe's own wording is a direction, not a quotation, so edit it where it reads as management-speak. The syllabus has a voice of its own, a mentor talking to a mentee: `VOICE.md` says how, and rules E1 to E4 hold it. Only Joe says "I": never write an experience or an opinion for him.
- **Examples** come from across complex technical product work, and none describes Joe's own employer, team or platform (S5, S6). This repository is public. Nothing about his work goes in it.
- **Licensing** (`LICENSE`, `LICENSE-content.md`, spec L1): new code is MIT; new syllabus text and figures are CC BY 4.0; anything else Joe writes is all rights reserved unless he says otherwise. Quote other authors briefly and credit them; their words stay theirs.
- **Margin notes are Joe's.** Never write, edit or delete what is between the quotes in `data/pm/margin/*.yaml`. After a unit changes, run `python3 tools-pm/margin-slots.py public` (after a build) to keep the slots in step; it keeps every note.
- **PDF:** `python3 tools-pm/make-pdf.py public out.pdf "On Product Judgment, pilot draft, <date>"` after `$HUGO`. Render and look at every page before handing a PDF to Joe.

## Pull requests and merging

- One pull request per piece of work, into `main`. The title says what changes for a reader.
- **Merge your own pull request into `main` by auto-merge, then stop** (Joe's decision, 20 November 2026). Open the pull request, turn on auto-merge with a merge commit, and end the turn without watching it. GitHub merges it once the `checks` workflow passes, so nothing wakes the session again. A session left waiting is woken by every CI event and re-reads its whole context each time. If a check fails, the next session fixes it ("Start of every session", step 4).
- **If GitHub refuses auto-merge** (the setting is off, or `checks` is not a required check), watch the pull request instead and merge it once every check has passed. Ask GitHub twice for the merge state: it reads `unknown` for a few seconds after a push. Stop watching the moment it merges.
- **Before the site goes live, only a merge that is costly to undo or irreversible waits for Joe** (his decision, 19 November 2026). A change to the look or to his own words that he asked for, or has seen in the session, merges like any other: lead the description with what he would want to know, show him the result, and merge.
- **Leave for Joe**, with a title starting `For Joe:` and a description that leads with the decision he is asked to make:
  1. Publishing: any pull request into `live`. Nothing reaches joestanley.org except through `live`, and only `publish.yml` deploys it, after the same checks pass.
  2. Any other merge that is costly to undo or irreversible.
- **Once the site is live, ask Joe what should wait for him again.** Until he says, hold what waited before 19 November: any change to the look (stylesheets, templates, fonts, figures, the hand-drawn marks, or a new V1 baseline that is not for content alone), and anything in his own voice (the ReadMe's words, the front door's lines, a Writing post's text).
- Never force-push to `main` or `live`. Never change repository settings; GitHub refuses them from a session. Write them up for Joe as numbered clicks.

## The syllabus

- Twelve modules, listed in `data/pm/modules.yaml`. Each is either built (a page under `content/pm/`) or a draft (one file under `drafts/pm/`, the module with its cards), never both (X1). A draft is not on the site. When you rebuild a module, delete its draft in the same change.
- Module 2, Find the Constraint, is the pilot: rebuild the other modules in its pattern (`content/pm/find-the-constraint.md`, its cards in `content/pm/cards/`, `data/pm/`).
- Open and check every source before a module is rebuilt. In a draft, mark what nobody has opened yet with a line that starts "To check:". No built unit may carry one (S7).
- **Ruth Malan's deck**, her February 2025 workshop notes, which the older drafts cite as "deck p.", is in the private repository `JoeStanley/pm-sources`: the PDF, its text one file per page, a map of every deck reference in the drafts, and what a full read found for each module. Attach it with `add_repo` when you rebuild a module that leans on the deck, and search it rather than reading it whole. Cite the works it points to, and the deck only for Malan's own insight (S8). Nothing from that repository comes here beyond a brief, credited quote.
- The short path uses only freely available sources; books go on the full path. Every recommended source says why to trust it and what only it gives the reader (S2).
- The whole syllabus aimed at about 50 printed pages and should read as manageable, not overwhelming. With twelve modules the drafts run past that; Joe settles the page target after a pilot (19 November 2026).
- Pilot first: build one piece, get Joe's reaction, then replicate. Ask Joe before a format becomes fixed.

## The working doc

Joe reviews the syllabus in one Claude Docs document, "On Product Judgment: Working Source": https://claude.ai/artifact/66JD4LSrrxJ3W9Mnbv5UjJ. It has a tab for each unit. The repository is the source and the doc mirrors it (X1 to X3). Keep it that way:

1. **Read the doc first.** `tools-pm/source-doc.lock.json` holds each tab's ids and the revision it had when it was last written. List the comments on each tab, and read each tab with `sinceRev` set to that revision: what comes back is what Joe changed. His comments and edits are the brief.
2. **Carry them into the repository**, spec first, like any change. Never edit the doc in place of the repository.
3. **Put the result back.** After `$HUGO`, run `python3 tools-pm/source-doc.py public out/`. It writes each tab as Markdown and says which have changed. Replace the contents of each changed tab in the doc with its file. Rename a tab when its module is renamed.
4. **Record it.** `python3 tools-pm/source-doc.py public --record "Start=12" "2 Find the Constraint=40"`, with each written tab's new revision. Commit the lock with the change. X3 fails until you do, so no change to the syllabus's words merges without reaching the doc.
5. **Answer every comment** in its own thread, in a line or two: what changed, or why nothing did. Leave his threads for him to resolve.

The Notes tabs at the end of the doc are history, frozen on 20 November 2026: read them, but add nothing there. New working notes (research write-ups, reviews, anything that mentions Joe's own work) go in `notes/` in the private repository `JoeStanley/pm-sources`, never in this one. Attach it with `add_repo`.

Research needs the web. The Joestanley.org environment has full web access (Joe, 20 November 2026). When a site still refuses, say so plainly, mark what you could not open with "To check:", and name the site in `PLAN.md`. Do not pass off a search result or a memory as a source you opened.

## Decisions

Joe decides on one private page, the Decisions page: https://claude.ai/artifact/QGLpeYcbz14tPBAPiQSYGq. Its source is `tools/decisions-page.html`; to change the page, publish that file with the Artifact tool and the page's address as `url`. The cards are documents in its database, collection `decisions`, read and written with the `ArtifactData` tool.

- **A card** is one question he can answer in a minute. Its id is `YYYY-MM-DD-short-name`, and its fields are `question`; `context`, a few plain sentences; `options`, three or four `{label, detail}` with your pick first; `why`, the reason for your pick; `blocks`, what waits on it, if anything; `links`, `{label, url}` to the tab, pull request or file he may want to read; `asked`, the date as `YYYY-MM-DD`; `order`, a number for cards asked the same day; and `status`, `open`.
- **His answer** arrives as `status: answered` with `answer: {choice, label, strength, note, at}`. `choice` is the option's index, or -1 for something else, which his note explains. `strength` is `agree` or `accept`, as below. Record it in `decisions.md`, then update the card with `status: recorded` and `recorded`, the date and where it went. A card he answered with something else may need a new card; never guess.
- **When he is in the session,** ask with picks there instead, and record his answers the same way.
- **If a session cannot write to the page,** it lists the card in `PLAN.md` under "To put to Joe", and the next session that can moves it to the page.

## The daily run

A scheduled task, "joestanley.org daily run", starts a fresh session every day at 02:43 UTC. Its first message begins "Daily run", and a session whose first message begins so is a run. A run works like any session, with three differences: it asks Joe nothing, and puts what it needs from him on the Decisions page; it takes only a job that waits on nothing; and if no job is ready and no answer waits to be recorded, it stops with no branch and no pull request. It merges by auto-merge like any session. Joe pauses or changes it in his list of scheduled tasks on claude.ai.

- **Another session first.** Before it takes a job, a run checks that nobody else is at work: if any branch but `main` was pushed in the last hour, it stops, and the next run tries again.
- **Without the working doc.** A run that cannot reach the working doc (the scheduled task needs the Claude Docs connector) takes only a job that changes none of the syllabus's words, and says so in `PLAN.md`.

## Working with Joe

- Put each decision to him as a card on the Decisions page, or with picks when he is in the session: your recommendation first, with its reason. He would rather answer questions than review long drafts.
- Lead with the decision, keep the rest brief. When you call something better, say why.
- He reviews in Markdown or in an editable doc where he can comment; he does not need Word.
- When he says "agree" he supports it; "accept" means he has no strong view. Record his decisions in `decisions.md`, one dated line each, in his terms, and nothing he did not decide.
