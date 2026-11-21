# joestanley.org design spec

The rules the site must meet. Each rule has an ID. `tests/check_site.py` checks every rule marked **auto** on every build and names the rule when one fails. Rules marked **review** need a person or a review agent. Change a rule here first, then the code, then the check.

Values such as colors and sizes live in the stylesheets (`assets/css/base.css`, and `pm.css` for the syllabus). This spec states what they must achieve, so the checks read the stylesheets rather than copying numbers into a second place.

The look was locked on 18 November 2026, from round 9: one orange ink on white, Newsreader for reading, Libre Franklin for titles and headings, Public Sans for labels, Shantell Sans for the owner's notes, a blended highlighter and a felt-pen circle (H1). V1 and V2 hold it there.

## Color roles

- **C1 auto.** Orange text appears only in page titles (`h1`) and the name on the home page. No other text is orange, except a link while hovered.
- **C2 auto.** No element has an orange or near-black fill behind text, except buttons in the dice game. No filled label boxes.
- **C3 auto.** Yellow fills appear only on the highlighter (`mark`), answers, the takeaway panel, figure marks and the dice game's waiting piles. Glossary terms carry no fill: like every link, they are marked by their underline alone.
- **C4 auto.** Every text and background pair meets WCAG 2.2 AA: 4.5:1 for body text, 3:1 for large text, in light and dark. Checked from the stylesheet tokens and by an automated scan of the rendered pages.
- **C5 auto.** Links are distinguishable without color: every link in running text is underlined, on screen and in the PDF, where a link is something to tap too. The underline is a quiet cue, not an accent: a thin grey line (`--link-line`) at 3:1 or better against the page, in light and dark (WCAG 1.4.1, 1.4.11). It turns orange and thicker on hover and keyboard focus, easing in over about 180 milliseconds, in CSS alone, with no script; with reduced motion requested the change is instant (D5). Glossary terms carry a dotted underline, the web's sign for a definition. The controls that fold and unfold (Show answer, Why this source) use the same grey line, and so does the line beside a margin note folded into the text.
- **C6 auto.** Words on the highlighter sit wholly on its stroke: no part of a letter reaches past the yellow, in light or dark, in each of the highlighter's three strokes (H1), because dark ink past the stroke meets a dark page. Measured from rendered pixels on the module's one thing and a card's question to carry.
- **C7 auto.** A picture may use colors of its own, beyond the page's ink, orange and highlighter, where its subject calls for one: water is blue. The owner lifted the lock for pictures on 19 November 2026, as long as their colors stay consistent with the family: soft, and no louder than the highlighter. Every picture color is a named value in `pm.css` (`--fig-` and its job), with a second value for dark screens, and no picture file sets a color itself, so the whole family can be read in one place. Whether a new color belongs in the family is the owner's call, as with any change to a picture (V1).

## Order of weight

- **W1 review.** Each page has one focal point: its title. The yellow highlighter is second.
- **W2 auto.** Section headings (`h2`) are near-black, never orange.
- **W3 auto.** Labels, times and notes are smaller than body text.
- **W4 auto.** Headings look their level: on every page, a heading is never smaller than a heading of a lower level, so the page's outline can be seen as well as heard. (WCAG 1.3.1)

## Margin

- **M1 auto.** On wide screens the margin holds only the owner's notes, in the owner's hand (Shantell Sans), each beside the part of the page it is about. Nothing else sits in the margin: glossary definitions open from the term, and a picture's caption sits under the picture at every width. On phones and in print a note folds into the text under the heading of its part, in the typeset face, marked by a thin line at its left.
- **M2 auto.** Margin notes never overlap each other or the reading column.
- **M3 auto.** Screen readers meet each margin note once, introduced as a note: right after the heading of the part it is about, or, for a step or a source, after its description, so a title stays with its time.
- **M4 auto.** Every part of every unit has a preserved slot for a margin note: each section, each step and source, the dice game, and each glossary term. A unit's slots are listed in reading order in `data/pm/margin/<unit>.yaml`, empty until the owner writes in one; an empty slot prints nothing. The file lists every part of its unit and nothing else, so a note can never be lost to a renamed part. `tools-pm/margin-slots.py` adds the slots for a new or changed unit and keeps the notes already written.

## Type

- **T1 auto.** Every font the stylesheets reference exists in `static/fonts/` with its license file, and every font loads on the pages that use it.
- **T2 auto.** Reading lines stay at or under 80 characters on every screen width.
- **T3 auto.** No em dashes in content, drafts, templates or styles.
- **T4 auto.** Text comes in five sizes on screen and four in print, each named for its job in `base.css`: small (labels, times, notes, controls), body (reading text, and headings below section level), heading (section headings, and the question under a title), title (page titles) and, on screen only, the name on the front door. Every piece of text a reader meets is set at one of them, on every page, at phone and desktop widths and in print. Next sizes differ by at least 1.2 times, so each reads as a different size. Stylesheets name the sizes rather than writing numbers. Text inside pictures belongs to the picture and is exempt.
- **T5 auto.** Each face has a fixed set of weights, each with a job: Libre Franklin 800 (titles and the site name) and 700 (headings); Newsreader 400, roman and italic, for reading, and 600, roman and italic, for bold words and citations; Public Sans 400 and 600 for labels and controls, and 400 italic for the title of a work cited in small type; Shantell Sans 400 and 600 for margin notes, and 400 for a line edit in the owner's hand (H2). Four weights in all, each doing the same job in every face: 800 titles, 700 headings, 600 bold, 400 text. No other pairing of face and weight appears.
- **T6 auto.** Line spacing comes from three named values: tight (titles), heading (headings and the question under a title) and text (everything else). Text spacing is at least 1.5, so running text of any size, notes included, keeps the line spacing WCAG recommends (1.4.8).
- **T7 auto.** Sizes follow the reader's text-size setting: on screen, the type and spacing scales are set in rem, so a reader who sets a larger default text size in their browser gets larger text and proportional space, not only those who zoom. (WCAG 1.4.4)

## Spacing

- **T8 auto.** Vertical space between and inside blocks (margins, padding and gaps) comes from one spacing scale of eight steps, on screen and in print. Print uses the same steps on a smaller unit, so the printed page keeps the screen's proportions. Exempt: the highlighter, a mark inside a line of text, and the step circles, whose place is computed from their title (R6).

## Hand-drawn marks

- **H1 auto.** The marks vary as a hand does. The highlighter is a felt pen's stroke with slanted ends over a slightly wobbly middle; a step circle is a felt-pen loop that overshoots its start. Each comes in three variants, picked by where the mark sits rather than at random, so the page is the same on every visit and in print. Neighbouring steps never share a circle, and the highlighted lines of a module and its cards do not all share one stroke. Every variant meets the same rules as the others: C6 for each highlighter variant, R6 for each circle.
- **H2 auto.** A line edit in the owner's hand. Where the owner corrects a word in the text, the old word stays in its line, scratched out with a pen stroke that leaves it readable, and the new words sit just above it in his hand (Shantell Sans), the way a correction is written on a printed page. They are written as a right-handed writer's quick line edit is: they start just before the old word and run to the right, rising between 3 and 6 degrees. The old word keeps no more space beside it than any other word in the line: where the new words are longer, they reach out over the next word instead of pushing the words apart. Where the old word ends a line, the new words shift left to end with the line (the owner, 20 November 2026). The scratch comes in three strokes, picked by where the edit sits, and takes the page's ink in light and dark. The new words never touch the line above or run past the screen, at phone and desktop widths. Read aloud, the new words come first and the old word follows, announced as crossed out (A10), which is also the order the eye meets them in, top to bottom (A6). Where the drawn stroke cannot show (D4), the old word carries a plain line through it. It prints as it shows on screen. It is for the owner's own corrections, used sparingly. The owner asked for it on 20 November 2026, for the quote that opens the Start page.

## Layout and responsiveness

- **R1 auto.** No sideways scrolling at 320, 390, 768, 1024, 1280 and 1920 pixels wide, or on a landscape phone (844 by 390).
- **R2 auto.** At 200% zoom (a 640-pixel-wide viewport standing in for 1280), no sideways scrolling and no text cut off.
- **R3 auto.** Below 1024 pixels the margin folds into the text; from 1024 pixels up it sits beside the reading column. Checked on a build with a sample note in every slot.
- **R4 auto.** On the home page the photo sits beside the name on wide screens and above it on narrow ones.
- **R5 auto.** Interactive targets are at least 24 by 24 CSS pixels; the home page's icon links are at least 44 by 44.
- **R6 auto.** A number set in a circle reads clearly and sits in the middle. The numeral is at least 40% of the circle's height, and its centre is within 3% of the circle's size from the circle's centre, on screen and in the PDF itself. This covers the short-path step circles, the dice game's stations and the numbered steps in concept-card pictures. A step circle also lines up with its task: its centre is within 5% of its size from the middle of the capitals on the first line of the step's title. Measured from rendered pixels, on screen and in the PDF rendered at 600 dpi, because the drawn ring, the shapes of the digits and the way each renderer rounds positions decide what the eye sees. A circle never prints in pieces: when a step moves to a new page, no part of its ring is left behind on the page before. A dice-game station's number is text set in a drawn disc, and a browser puts text on whole pixels, so how it sits depends on where the page above happens to end: it is measured with the disc on the pixel grid, and on a page where the disc lands between pixels it may sit up to a pixel off.
- **R7 auto.** With the browser's default text size doubled (32 pixels instead of 16), no page scrolls sideways at 390 or 1280 pixels, no text is cut off, and margin notes do not overlap. (WCAG 1.4.4, 1.4.10)
- **R9 auto.** The site's menu sits on one line on a phone. At 390 pixels and wider, on every page, ReadMe, Product Judgment, Writing and Games share one line, with the current section in bold, so no section drops to a second line. On narrower screens, and with enlarged text (R7), the menu wraps rather than scroll. The owner chose this on 20 November 2026, when the menu's label became Product Judgment, over hiding sections behind a menu button.
- **R8 auto.** The site works the same in Safari's engine (WebKit) and in Firefox, not only in Chrome. In both, at 390 pixels (in WebKit, as an iPhone) and 1280: no page scrolls sideways or runs text off the screen (R1), every size, weight, line spacing and gap is on the scales (T4 to T6, T8), and the enlarged-text and text-spacing checks hold (R7, A13). A failure there is reported under its own rule and names the engine; R8 itself fails only if an engine cannot run. The step circles and the PDF are checked in Chrome, which makes the PDF.

## Graceful degradation

- **D1 auto.** Without JavaScript every page reads fully: the dice game shows its rules, one recorded run and the takeaway; answers and source reasons stay folded but open by tapping; glossary terms link to the glossary.
- **D2 auto.** Without the dialog feature (`showModal`), a glossary term still takes the reader to its definition in the glossary. With it, tapping a term opens the definition in place.
- **D3 auto.** Without web fonts, nothing scrolls sideways and nothing overlaps.
- **D4 auto.** Features newer browsers add (drawn masks, `:has()`) are guarded, so an older browser shows a plain version rather than a broken one.
- **D5 auto.** With reduced motion requested, nothing animates on its own, the dice game finishes at once, and a link's change on hover or focus is instant.

## Interaction and accessibility

- **A1 auto.** The automated accessibility scan (axe-core, WCAG 2.2 A and AA rules) finds no violations on any page, including the single document `/pm/all/`, in light or dark, at 390 or 1280 pixels.
- **A2 auto.** Every element that takes keyboard focus shows a visible focus ring.
- **A3 auto.** Icon-only links have accessible names.
- **A4 review.** A screen reader pass reads each page in a sensible order with sensible names.
- **A5 auto.** A glossary term opens a modal dialog named by the term, with the definition as its description. Opening it moves focus inside. While it is open, Tab and Shift+Tab never reach the page behind it; the browser may offer its own address bar, as it does for every modal dialog. Escape and Close return focus to the term. (WCAG 2.4.3, 4.1.2)
- **A6 auto.** A screen reader meets things in the order the eye does: in the main content, nothing sits above an element that comes before it in the source. Figure captions are the one exception, because a caption names its figure. (WCAG 1.3.2)
- **A7 auto.** Names make sense read aloud. No name starts with punctuation. A disclosure's name carries no state word the stylesheet adds ("Open", "Close"). A tick box says what ticking does ("Mark done: ..."). A label that runs straight into what it introduces, the dice game's counters and each picture's title end with punctuation, so the voice pauses. (WCAG 4.1.2, 1.3.1)
- **A8 auto.** What the dice game shows on its board is also given in words. After a run, the result names how many items wait at each station, matching the board. A change of setup is announced. The key to the board is hidden from screen readers along with the board. (WCAG 1.1.1, 4.1.3)
- **A9 auto.** Focus is never dropped. Play keeps focus while the game runs, and choosing a unit in the single document moves focus to that unit's title. (WCAG 2.4.3)
- **A10 auto.** Struck-out text is announced as crossed out, because its meaning can depend on it. (WCAG 1.3.1)
- **A11 auto.** Headings never skip a level on the way down. (WCAG 1.3.1)
- **A12 auto.** Text that screen readers read never points to a color as the way to find something. Checked by looking for color names in what screen readers read. (WCAG 1.3.3)
- **A13 auto.** Readers can override text spacing (line height 1.5, paragraph spacing 2 times the text size, letter spacing 0.12 and word spacing 0.16 times the text size) without losing anything: at 320 and 1280 pixels no page scrolls sideways, no text is cut off by its box, and margin notes do not overlap. (WCAG 1.4.12)

## Print

- **P1 auto.** Each unit prints on its own Letter pages and keeps to its share: Start on no more than two pages, now that it lists twelve modules, a module on no more than three, a concept card on one, and the glossary on one. What is rebuilt so far (Start, Modules 1 and 2, their three cards and the glossary) prints on 12 pages. The whole syllabus aimed at about 50; the owner settles the target after a pilot (his decision of 19 November 2026).
- **P2 auto.** Each concept card starts on a new page and fits on one page.
- **P3 auto.** Print is always light, has no header or footer, and shows every answer.
- **P4 auto.** The PDF that `tools-pm/make-pdf.py` makes is tagged for screen readers: headings, lists and tables are marked, the language is declared, every figure has a text alternative, nothing that prints is hidden from assistive technology, so every printed word reaches the tags, and it is bookmarked as P6 sets out. P1, P2, P5 and P6 check this same file.
- **P5 auto.** The PDF stands on its own. Every link to something inside the syllabus (a unit, a glossary term, the dice game) jumps to that place in the PDF; only sources outside the syllabus link to the web, by their full public address. No link points to a local, relative or test address. Every link carries a description a screen reader can announce, and each page with links follows the tagged reading order when a reader tabs through it.
- **P6 auto.** The PDF carries the metadata readers and libraries expect: a title, shown in the reader's title bar in place of the file name; author; subject; keywords; language; and the tool that made it, in both the document information and the XMP metadata, and the two agree. It opens with its bookmarks showing. Bookmarks follow the document: each unit at the top level, named for what it is ("Start: On Product Judgment", "Module 2: Find the Constraint", "Glossary"); a unit's sections beneath it; a module's concept cards beneath the module, after its sections, each named "Card: " and its title, with the card's sections beneath; and each glossary term beneath Glossary. Nothing deeper is bookmarked, and every bookmark lands on the page where its heading or term prints. The title, subject and keywords come from `content/pm/all.md`, so they change with the content, not the tool.

## Content structure

- **S1 auto.** Every short-path step has a "look for" line.
- **S2 auto.** Every recommended source on the short or full path says why to trust it and what you'll get from it that the others do not give, except concept cards and the dice game on the short path. The two lines are labeled "Why trust it" and "What you'll get".
- **S3 auto.** Every glossary term used in the text exists in the glossary, and every glossary entry is used somewhere.
- **S4 auto.** A source's reasons (why trust it, and what you'll get) stay folded under it on screen, behind one line, "Why this source", that opens in place, so readers who take the advice on its face are not slowed by them. In print, where nothing folds, a module lists every source's reasons at the back, after the answers, and a concept card prints its one source's reasons at its foot. Each reason prints exactly once.
- **S5 auto.** No example is set in a retired setting. The owner found the examples leaning on his own work and asked on 20 November 2026 for them to be stripped; the settings retired then are listed in `tests/retired-settings.txt`, and none returns in a built unit or a draft.
- **S6 review.** Examples range across kinds of complex technical products (`VOICE.md` lists some). No unit leans on one setting, and none describes the owner's own employer, team or platform.
- **S7 auto.** Nothing unchecked reaches the site. In a draft, a source or a claim that nobody has yet opened and checked carries a line that starts "To check:" and says what is open. No built unit carries one: the checking is done before a module is rebuilt.
- **S8 review.** Cite where an idea starts. Where a deck, a talk or a collection quotes or sums up someone else's work, a unit cites that work directly, opened and checked (S7), not the collection. Ruth Malan's workshop notes, which the older drafts cite as "deck p.", are cited only for an insight that is her own and that the notes clearly attribute to her (the owner's decision of 20 November 2026). The drafts that still lean on the deck move to this as they are rebuilt.
- **S9 auto.** No source is cited from Substack, by name or by link, in a built unit, a draft or the site's data. The owner never wants to cite it, because it platforms white supremacists (his decision of 20 November 2026).
- **S10 auto.** A module's full path may carry one story: a novel or other fiction, or a series, film, documentary or play, that tells or reinforces the module's lesson, so the reader carries it across from another form, as transfer does. Never more than one a full path. Its entry opens by naming its medium ("A novel", "A TV series", "A film"), so the reader knows what kind of time it asks for. The owner asked for this on 21 November 2026, with *Mozart in the Jungle* for Own Your Role; the pilot's novel, *The Goal*, is one already.

## Voice

The syllabus sounds like a mentor talking to a mentee across a table: `VOICE.md` says how, with examples. These rules hold what a check can. They cover every unit, built or draft, as the working doc shows it (X2), outside quotations, titles and links. The Start page's opening and the margin notes are the owner's own words.

- **E1 auto.** The syllabus talks to the reader. Every module's "Why this matters" and every card's "Why a PM cares" (in an older draft, "Why a PM should care") says "you".
- **E2 auto.** Contractions, a human amount. In each unit, where one of the common contractions could go (it's, don't, you'll, isn't, can't and the like), it is used at least six times in ten. Not every time: the full form stays where a speaker would stress it.
- **E3 auto.** Only the owner says "I". Outside the Start page and the margin notes, no unit speaks in the first person singular, so no experience or opinion is invented for him.
- **E4 review.** A unit reads as one person talking, a notch below the Start page, with none of the habits `VOICE.md` lists under "What it is not". Someone who did not write it reads it whole before it merges.

## Working source

The owner reviews the syllabus in one working doc, with a tab for each unit. The repository is the source; the doc mirrors it. A session carries his comments and edits from the doc into the repository, then puts the result back in the doc.

- **X1 auto.** One source for every unit. Every module on the map (`data/pm/modules.yaml`) is either built, with a page under `content/pm/`, or a draft, with one file under `drafts/pm/` that holds the module and its cards. Never both, never neither, and every draft file belongs to a module on the map. A draft is not on the site.
- **X2 auto.** The doc holds every word. `tools-pm/source-doc.py` writes one tab for each unit: Start, each module with its cards, and the glossary. A built unit's tab is made from the built page, so it holds every word a reader meets there, outside pictures, the game's board and the one line that folds a source's reasons. A draft's tab is its file, under the title and question the map gives it. Checked by comparing the words of each built page with its tab.
- **X3 auto.** The doc is in step. `tools-pm/source-doc.lock.json` records what was last put in the doc, tab by tab. When a tab made now differs from that record, the check fails until a session puts the tab in the doc and records it, in the same change. So no change to the syllabus's words merges without reaching the doc. The other direction is the session's job: before it writes a tab, it reads what the owner changed there since the recorded revision.

## Licensing

- **L1 auto.** Every page says whose it is. Every page but the front door ends with the copyright line (`copyright` in `hugo.yaml`). Every syllabus page adds that its text and figures are free to share and adapt, with credit, under CC BY 4.0, linking to the license (`params.license`). The PDF prints the copyright line and the license on every page, and states them in its metadata (XMP `dc:rights`, marked as rights-managed, with the license's address). The repository's `LICENSE` is the MIT License, for the code; `LICENSE-content.md` says what CC BY 4.0 covers and that everything else is all rights reserved.

## Change control

- **V1 auto.** Screenshots of every page at 390 and 1280 pixels, light and dark, are compared against an approved baseline. Any change beyond a small threshold fails, for a person to look at. A change to the look (the stylesheets, templates, fonts, figures or hand-drawn marks) needs the owner's approval before a new baseline is recorded. A change to content alone (words, data, a new module, card or post) may record a new baseline in the same change, and says so. Screenshots depend on the machine that takes them, so V1 runs in working sessions against a baseline recorded there, not in GitHub's checks; if V1 fails on an unchanged look in a new environment, record the baseline again from the locked commit and say so. The first baseline was recorded from round 9 when the owner locked the look on 18 November 2026.
- **V2 auto.** One look, with no switches. The site has two stylesheets, `base.css` on every page and `pm.css` added on the syllabus, and every stylesheet in `assets/css/` is one of them. No setting in `hugo.yaml` chooses a look, a direction or a hand, and no template reads one. Changing the look means changing these files, with the owner's approval and a new V1 baseline, not keeping an alternative beside it.
