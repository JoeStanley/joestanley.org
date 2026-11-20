# joestanley.org shared style: round 10 source

18 November 2026. The look is locked. Nothing here has been pushed to the live site.

Round 10 is the lock round. The owner approved round 9's look, and this round removes everything that only existed to compare looks, with no change a reader can see:

- **One look, two stylesheets.** `base.css` (every page) and `pm.css` (the syllabus) now hold every value directly. The reading face, the one-ink direction and the chosen hands were folded in; `look-serif.css`, `look-sans.css`, `dir-oneink.css` and `dir-twoink.css` are gone, with the values they used to override. The `look`, `direction` and `marks` settings are gone from `hugo.yaml` and the templates. The steady and sketch hands, and the marker highlighter, are gone; the step circle keeps its three felt-pen loops and the highlighter its three blended strokes.
- **Proved unchanged.** Every page at 390 and 1280 pixels, light and dark, with and without sample margin notes, and every page of the print PDF, renders pixel for pixel as round 9 did (98 images). The PDF made by `tools-pm/make-pdf.py` matches round 9's on all 7 pages.
- **Baseline recorded** (V1) from round 9, and a new rule **V2** keeps the look single: any extra stylesheet, or a look, direction or hand setting, fails the checks. V1 now says what may record a new baseline: content alone may, a look change needs the owner. All 37 mutations are caught, two of them new for V2.
- **Ready for Claude to run the repo.** `CLAUDE.md` (standing instructions), `decisions.md` (the owner's decisions), `tests/setup.sh` (installs everything the checks need), `.github/workflows/checks.yml` (every pull request and every change to `main` is checked; failing work is not merged) and `.github/workflows/publish.yml` (the live site is built from the `live` branch only, after the same checks). The workflows pass `actionlint` but have not run on GitHub yet. `tests/check_site.py --skip V1` is what GitHub runs, because screenshots depend on the machine.
- **Licensed** (rule L1). The code is MIT (`LICENSE`); the syllabus's text and figures are CC BY 4.0, and the rest is all rights reserved (`LICENSE-content.md`). Every page but the front door now ends with "© 2026 Joe Stanley, Richmond, Virginia.", and syllabus pages add the license with a link to it; the PDF prints the same on every page and records it in its metadata. This is the one change a reader can see, approved by the owner, so V1's baseline was recorded again after it.

Round 9 was the hand-drawn marks round, with three requests from the owner:

- **Your margin notes (M1 to M4).** Every part of every unit has a preserved slot for a note of yours, listed in reading order in `data/pm/margin/<unit>.yaml` (Start, the module, each card, the glossary). Write between the quotes; leave `""` for none. On a wide screen a note shows in your hand (Shantell Sans) in the margin beside its part; on a phone and in print it sits under the part's heading, in the typeset face, with an orange pen line at its left. Markdown works for **bold** and links. After a unit changes, `python3 tools-pm/margin-slots.py public` adds new slots and keeps every note you have written; the checks fail if a slot and its part ever drift apart. New partials: `layouts/partials/pm/margin.html`, `layouts/partials/pm/prose-slots.html`.
- **Only your notes in the margin.** Glossary definitions no longer sit in the margin (they open from the term), and a card's picture caption sits under the picture at every width (class `plate-caption`).
- **Terms marked by underline only (C3).** The pale yellow highlight on glossary terms is gone; a term is a link like any other.
- **A self-contained PDF (P5, P6).** Glossary terms jump to the glossary inside the PDF, not to a local web address; every link has a description for screen readers. Bookmarks follow the document: Start Here, Module 2 with its sections and its two cards beneath, Glossary with its terms. Title, author, subject, keywords and language are set in the document information and the XMP metadata, from `content/pm/all.md` and `hugo.yaml`, and the PDF opens with its bookmarks showing. The glossary is tagged as a list of terms and definitions. `tools-pm/make-pdf.py` now needs `pikepdf` and `pypdfium2`.
- **Quieter links (C5).** Every link keeps its underline, now a thin grey line at 3.4:1 against the page (3.9:1 in dark), so the page reads calmer; it eases to orange on hover and focus, in CSS alone, and is instant with reduced motion (D5). Glossary terms are dotted. Links are underlined in print too, because in the PDF they are something to tap.
- **Hand-drawn marks (H1, C6).** `params.marks` in `hugo.yaml` sets the hand: `highlighter: blend` (steady's wobbly stroke with chisel ends, your pick) and `circles: marker` (a felt-pen loop that overshoots its start, your pick). Each comes in three variants, chosen by position, so neighbouring marks differ. Every stroke now covers its letters fully; in round 8 the tops of tall letters poked above the yellow, which in dark mode put dark ink on a dark page (new rule C6). The highlighted line hangs its stroke into the gutter, so its words line up with the text edge. The steady, marker and sketch alternatives stay selectable until the look is locked.

Round 8 was the type and spacing round. What changed:

- **One type scale.** Five sizes on screen (small, body, heading, title, and the front-door name), four in print, each named for its job in `base.css` (spec T4). Was 19 sizes on screen and 18 in print. Four weights, each doing the same job in every face (T5). Three line spacings, with text at 1.5 or more (T6). Sizes are in rem, so they follow a reader's own text-size setting (T7).
- **One spacing scale** of eight steps on one unit; print uses the same steps on a 7pt unit (T8). Was 22 different gaps on screen and 21 in print.
- **Headings look their level** (W4): concept-card section headings are now the size of every other section heading.
- **Tablets read at a comfortable line length** (T2 now checks 600 to 900 pixels too): the reading column stops at the measure below 1024 pixels.
- **Bigger tap rows** for the short path's links and the header's sections; the photo's ring lines up with the text on phones.
- **Larger text and custom spacing hold up** (R7, A13): the front-door name, footer links, module list and dice game no longer run off a phone when the reader doubles their text size.
- **Why this source.** Each source's reasons fold under it behind one line and open in place. In print, a module lists them at the back after the answers; a card prints its source's reasons at its foot (S4). New partial: `layouts/partials/pm/source-reasons.html`.
- **Step circles** are now laid out in a two-column grid, not positioned, so they travel with their step across a PDF page break (R6 now also catches a piece of ring left behind). `--head-cap-k` in `dir-oneink.css` replaces `--head-cap-mid`: the circle now follows any change to the title's size or line spacing, and is still calibrated, so recheck it when the hand-drawn marks change.
- **Checks run in three engines.** The responsive and scale checks also run in WebKit (Safari's engine, as an iPhone) and Firefox (R8). Install them once with `python3 -m playwright install webkit firefox`.
- `tests/check_site.py --only T4,T8` runs just the checks behind the named rules; `tests/mutations.sh` uses it and runs two at a time (`JOBS=` to change that).

Round 7 was the accessibility round: glossary terms open a modal dialog, the dice game speaks its board, reading order matches the screen, names read aloud cleanly, the PDF is tagged and bookmarked, and numbers sit centred in their circles.

These files replace the PaperMod theme with a small theme kept in the site repo, and carry the PM Syllabus pilot into it. One set of templates and one look serve the whole site.

## What is in here

| Path | What it holds |
| --- | --- |
| `CLAUDE.md`, `decisions.md` | Standing instructions for Claude sessions, and your decisions, newest first. |
| `LICENSE`, `LICENSE-content.md` | The MIT License for the code; what CC BY 4.0 covers, and what is all rights reserved. |
| `.github/workflows/` | `checks.yml`, the gate on every pull request and on `main`; `publish.yml`, which deploys the `live` branch after the same checks. |
| `hugo.yaml` | Site settings, the four sections and their home-page lines, your links. The `theme` line is gone. |
| `layouts/` | Every template: base page, header, footer, home, ReadMe, section index, and the syllabus units. |
| `assets/css/` | `base.css` (every page: fonts, colors, the type and spacing scales, links, header and footer, the highlighter, margin notes, the front door, print) and `pm.css` (syllabus pieces, the step circles and print). |
| `assets/js/pm.js`, `assets/figures/` | The syllabus script and card pictures, as in the pilot. |
| `static/fonts/` | Newsreader, Public Sans, Libre Franklin and Shantell Sans, all SIL Open Font License, with their license files. |
| `layouts/partials/icon.html` | The email, Bluesky and LinkedIn icons on the home page, from the PaperMod theme and Feather icons (MIT License; notice in the file). |
| `content/` | New home, Writing and Games pages; the syllabus content from the pilot. |
| `data/pm/` | Modules, glossary and dice-game numbers, as in the pilot. |
| `tests/` | The design spec (`SPEC.md`), the checks that enforce it (`check_site.py`, `mutations.sh`), the approved screenshots (`baseline/`) and `setup.sh`. See `tests/README.md`. |
| `content/page/readme.md` | Your ReadMe, with its headings moved from level 3 to level 2. Words unchanged. |
| `tools-pm/make-pdf.py` | Not part of the site. Prints `/pm/all/` to PDF and finishes it: links, bookmarks, tags, metadata. |
| `tools-pm/margin-slots.py` | Not part of the site. Keeps the margin-note slots in `data/pm/margin/` in step with the units. |
| `tools-pm/source-doc.py`, `tools-pm/source-doc.lock.json` | Not part of the site. Makes the working doc's tabs from the repository, and records what was last put in the doc (spec X1 to X3). |
| `drafts/pm/` | The modules not yet rebuilt for the site, one file each with its cards. Not part of the site. |
| `VOICE.md` | How the syllabus is written: a mentor talking to a mentee (spec E1 to E4). |
| `data/pm/margin/` | Your margin notes, one file per unit, one slot per part. |

## Build and check

1. `bash tests/setup.sh` installs Hugo 0.141.0 extended and everything the checks need, and prints the `HUGO` and `CHROME` values to export.
2. Build: `$HUGO`. Check: `python3 tests/check_site.py`.
3. PDF: `python3 tools-pm/make-pdf.py public out.pdf "label"` (needs Playwright 1.42 or later with Chrome, `pikepdf` and `pypdfium2`). The PDF is tagged for screen readers, bookmarked, self-contained and carries its metadata.

## The new repository

These files start a new repository under the JoeStanley GitHub account; the old one under joestanley3 keeps serving the current site until the move. Nothing from PaperMod comes across. Still to bring over from the old repository: `static/img/` (the photo on the front door). `baseURL` is `https://joestanley.org/`; at the move, GitHub Pages for the new repository takes the custom domain.
