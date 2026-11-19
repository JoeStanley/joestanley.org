# joestanley.org: standing instructions

Joe Stanley's personal site: a front door, a ReadMe, the PM Syllabus, Writing and Games. Built with Hugo 0.141.0 extended and a small theme kept in this repo. Joe owns it; Claude does the work in Claude Code sessions. Joe's decisions are in `decisions.md`, newest first. Read it, and `tests/SPEC.md`, before changing anything.

## Start of every session

1. `bash tests/setup.sh`, then export the `HUGO` and `CHROME` values it prints on its last line.
2. Read `decisions.md` and `tests/SPEC.md`.
3. Work on a branch named `claude/<short-topic>`, from an up-to-date `main`.

## How a change is made

- **Spec first.** Change `tests/SPEC.md`, then the site, then the check in `tests/check_site.py`. A change that makes a check fail is not done.
- **Check before every push:** `python3 tests/check_site.py`. When a check changes, also run `bash tests/mutations.sh` and add a mutation that proves the new check catches what it is for.
- **V1 (screenshots) runs here, not on GitHub.** A change to content alone may record a new baseline with `--update-baseline` in the same pull request, and says so. A change to the look needs Joe's word first: describe it to him before you make it. If V1 fails on an unchanged look because this environment renders differently, record the baseline again from `main` before your change, in its own commit, and say so.
- **The look is locked** (`tests/SPEC.md`, V2): two stylesheets, `base.css` and `pm.css`; no switches for alternative looks, directions or hands. To propose a change, describe it to Joe first. Pictures may use colors of their own, as long as they stay in the family (C7).
- **Words:** American English. No em dashes anywhere (T3). Plain, short sentences; Joe's own wording is a direction, not a quotation, so edit it where it reads as management-speak.
- **Licensing** (`LICENSE`, `LICENSE-content.md`, spec L1): new code is MIT; new syllabus text and figures are CC BY 4.0; anything else Joe writes is all rights reserved unless he says otherwise. Quote other authors briefly and credit them; their words stay theirs.
- **Margin notes are Joe's.** Never write, edit or delete what is between the quotes in `data/pm/margin/*.yaml`. After a unit changes, run `python3 tools-pm/margin-slots.py public` (after a build) to keep the slots in step; it keeps every note.
- **PDF:** `python3 tools-pm/make-pdf.py public out.pdf "PM Syllabus, pilot draft, <date>"` after `$HUGO`. Render and look at every page before handing a PDF to Joe.

## Pull requests and merging

- One pull request per piece of work, into `main`. The title says what changes for a reader.
- **Merge your own pull request into `main`** once every check on GitHub has passed (the `checks` workflow). Ask GitHub twice for the merge state: it reads `unknown` for a few seconds after a push.
- **Before the site goes live, only a merge that is costly to undo or irreversible waits for Joe** (his decision, 19 November 2026). A change to the look or to his own words that he asked for, or has seen in the session, merges like any other: lead the description with what he would want to know, show him the result, and merge.
- **Leave for Joe**, with a title starting `For Joe:` and a description that leads with the decision he is asked to make:
  1. Publishing: any pull request into `live`. Nothing reaches joestanley.org except through `live`, and only `publish.yml` deploys it, after the same checks pass.
  2. Any other merge that is costly to undo or irreversible.
- **Once the site is live, ask Joe what should wait for him again.** Until he says, hold what waited before 19 November: any change to the look (stylesheets, templates, fonts, figures, the hand-drawn marks, or a new V1 baseline that is not for content alone), and anything in his own voice (the ReadMe's words, the front door's lines, a Writing post's text).
- Never force-push to `main` or `live`. Never change repository settings; GitHub refuses them from a session. Write them up for Joe as numbered clicks.

## The syllabus

- Module 2, Find the Constraint, is the pilot: rebuild the other modules in its pattern (`content/pm/find-the-constraint.md`, its cards in `content/pm/cards/`, `data/pm/`).
- The short path uses only freely available sources; books go on the full path. Every recommended source says why to trust it and what only it gives the reader (S2).
- The whole syllabus aims at about 50 printed pages and should read as manageable, not overwhelming.
- Pilot first: build one piece, get Joe's reaction, then replicate. Ask Joe before a format becomes fixed.

## Working with Joe

- Ask him structured questions with picks as you go, with your recommendation first and its reason; he would rather answer questions than review long drafts.
- Lead with the decision, keep the rest brief. When you call something better, say why.
- He reviews in Markdown or in an editable doc where he can comment; he does not need Word.
- When he says "agree" he supports it; "accept" means he has no strong view. Record his decisions in `decisions.md`, one dated line each, in his terms, and nothing he did not decide.
