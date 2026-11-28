#!/bin/bash
# Proves the suite has teeth: each line breaks a copy of the site one way and confirms the named rule fails.
# Run from the repo root: HUGO=/path/to/hugo bash tests/mutations.sh
set -u
SRC=$(cd "$(dirname "$0")/.." && pwd)
run() {  # description, rule, command that breaks the copy
  D=$(mktemp -d); cp -r "$SRC"/. "$D"/; (cd "$D" && eval "$3")
  # A mutation whose target has moved or gone changes nothing, and tests nothing: say so, rather than run the
  # check and read its result as a miss or, worse, as a catch for some other reason (22 November 2026, when
  # five still aimed at drafts that every module's rebuild had deleted).
  if diff -rq --exclude=.git "$SRC" "$D" >/dev/null 2>&1; then echo "STALE: $1 ($2) changed nothing"; rm -rf "$D"; return; fi
  # The voice guide lives in pm-sources, beside this repository (T3). A mutation that breaks a copy of it puts the
  # copy in .pm-sources inside the copy of the site, and the check reads that one.
  PMS="$D/.pm-sources"; [ -d "$PMS" ] || PMS="${PM_SOURCES:-$SRC/../pm-sources}"
  (cd "$D" && PM_SOURCES="$PMS" python3 tests/check_site.py --only "$2" >/dev/null 2>&1)
  if grep -q "| $2 | auto | FAIL" "$D/tests/report.md"; then echo "caught: $1 ($2)"; else echo "MISSED: $1 ($2)"; fi
  rm -rf "$D"
}
# Runs at most $JOBS mutations at once (default 2): each one starts browsers, and too many at once on a small
# machine make checks time out, which reads as a miss.
run_bg() { while [ "$(jobs -rp | wc -l)" -ge "${JOBS:-2}" ]; do sleep 2; done; run "$@" & }
run_bg "orange section heading" W2 "echo 'h2 { color: var(--orange) !important; }' >> assets/css/pm.css"
run_bg "step without a look line" S1 "sed -i '0,/    look: The line falls short/{/    look: The line falls short/d}' content/pm/find-the-constraint.md"
run_bg "photo back above the name" R4 "sed -i 's/grid-column: 2; grid-row: 1 \/ span 4;/grid-column: 1;/' assets/css/base.css"
run_bg "light grey body text" C4 "sed -i 's/--muted: #5c5955;/--muted: #a09c96;/' assets/css/base.css"
run_bg "filled label box" C2 "echo '.kicker .tag { background: var(--orange); color: #fff; }' >> assets/css/pm.css"
run_bg "wide fixed element" R1 "echo '.unit-head h1 { min-width: 30rem; }' >> assets/css/pm.css"
run_bg "Play disabled during a run" A9 "sed -i 's/busy(true);/busy(true); el.play.disabled = true;/' assets/js/pm.js"
run_bg "a step's look line moved above its title" A6 "echo '.step-body { display: flex; flex-direction: column; } .step-body > .look { order: -1; }' >> assets/css/pm.css"
run_bg "board key read aloud" A8 "sed -i 's/ class=\"board-key\" aria-hidden=\"true\"/ class=\"board-key\"/' layouts/partials/pm/dicegame.html"
run_bg "untagged PDF" P4 "sed -i 's/tagged=True, outline=True/tagged=False, outline=False/' tools-pm/make-pdf.py"
run_bg "glossary pop-up instead of dialog" A5 "sed -i 's/dlg.showModal(); });/dlg.show(); });/' assets/js/pm.js"
run_bg "a size off the scale" T4 "echo '.meta-line { font-size: 15.2px; }' >> assets/css/pm.css"
run_bg "a stray weight" T5 "echo '.kicker { font-weight: 500; }' >> assets/css/pm.css"
run_bg "a stray line spacing" T6 "echo '.hint { line-height: 1.45; }' >> assets/css/pm.css"
run_bg "type scale in pixels" T7 "sed -i 's/--fs-small: 0.9375rem;/--fs-small: 15px;/' assets/css/base.css"
run_bg "a color named to find something, though capitalized" A12 "printf '\\nTap the Green button to start the game.\\n' >> content/pm/find-the-constraint.md"
run_bg "a stray gap" T8 "echo '.hint { margin-bottom: 0.7rem; }' >> assets/css/pm.css"
run_bg "section heading smaller than a step title" W4 "echo '.card-body h2 { font-size: var(--fs-small); }' >> assets/css/pm.css"
# The label must outrun the menu's own row: when the menu sat on a row of its own under the name, "Product Judgment
# Syllabus" still fits there, and the mutation broke nothing (found 25 November 2026)
run_bg "a menu label too long for a phone" R9 "sed -i 's/      name: On Judgment/      name: On Product Judgment, the Syllabus/' hugo.yaml"
run_bg "header that cannot wrap" R7 "echo '.masthead-row, .site-nav, .nav-list { flex-wrap: nowrap; white-space: nowrap; }' >> assets/css/base.css"
run_bg "a line box that clips its text" A13 "echo '.meta-line { max-height: 1.5em; overflow: hidden; }' >> assets/css/pm.css"
run_bg "a stray gap in Firefox only" T8 "echo '@supports (-moz-appearance: none) { .hint { margin-bottom: 0.7rem; } }' >> assets/css/pm.css"

run_bg "source reasons open, not folded" S4 "sed -i 's/<details class=\"why\">/<div class=\"why\">/; s/<\/details>/<\/div>/' layouts/partials/pm/source-notes.html"
run_bg "glossary links leave the PDF for the site" P5 "sed -i 's/^{{- \$html := replace (string .) .*/{{- \$html := string . }}/' layouts/pm/all.html"
run_bg "PDF opens without its bookmarks" P6 "sed -i '/root.PageMode = /d' tools-pm/make-pdf.py"
run_bg "glossary definition back in the margin" M1 "sed -i 's|^{{- /\*\*/ -}}|<span class=\"note\" aria-hidden=\"true\">{{ \$g.text }}</span>|' layouts/shortcodes/pm/term.html"
run_bg "notes hidden from screen readers" M3 "sed -i 's/<aside class=\"note\"/<aside aria-hidden=\"true\" class=\"note\"/' layouts/partials/pm/margin.html"
run_bg "a slot file that lost a part" M4 "sed -i '/^step-forte:/d' data/pm/margin/find-the-constraint.yaml"
# A card's picture carries no slot (27 November 2026): put the slot back on the picture and in every card's file,
# so the files still list every part of the page and only the rule against a picture's slot can catch it.
run_bg "a card's picture given a margin slot again" M4 "sed -i 's|<figure class=\"plate\">|<figure class=\"plate\" data-slot=\"picture\">|' layouts/partials/pm/unit-card.html; for f in \$(grep -l 'the concept card' data/pm/margin/*.yaml); do sed -i 's/^top: \"\"\$/top: \"\"\\npicture: \"\"/' \$f; done"
run_bg "notes left in the column on wide screens" R3 "sed -i 's/    float: right; clear: right;/    float: none;/' assets/css/base.css"
run_bg "pale highlight back on glossary terms" C3 "echo '.term { background: var(--mark-soft); }' >> assets/css/pm.css"
run_bg "printed links without underline" C5 "echo '@media print { a { text-decoration: none; } }' >> assets/css/pm.css"
run_bg "highlighter stroke too low for tall letters" C6 "sed -i 's/M0,0.9 C40,0.4 80,1.1 120,0.5 C150,0.1 178,0.5 200,0.8/M0,5 C40,4.6 80,5.2 120,4.6 C150,4.2 178,4.6 200,5/' assets/css/base.css"
run_bg "every step drawn with one circle" H1 "sed -i 's/{{- \$n := mod (sub (int .) 1) 3 }}/{{- \$n := 0 }}/' layouts/partials/pm/step-mark.html"
run_bg "a step's note squeezed into the circle column on a phone" M1 "sed -i '/^.step > .note { grid-column: 2; }/d' assets/css/pm.css"
run_bg "link underline too faint to see" C4 "sed -i 's/--link-line: #8f8a84;/--link-line: #d6d2cc;/' assets/css/base.css"
run_bg "glossary terms back to a solid line" C5 "sed -i 's/a.term { text-decoration-style: dotted;/a.term { text-decoration-style: solid;/' assets/css/base.css"
run_bg "a second look kept beside the locked one" V2 "printf ':root { --ink: #000; }' > assets/css/look-sans.css"
run_bg "a hand switch back in the settings" V2 "sed -i 's/^  author: Joe Stanley$/  author: Joe Stanley\n  marks: {highlighter: steady}/' hugo.yaml"
run_bg "license dropped from the syllabus footer" L1 "sed -i 's/{{ with site.Params.license }}.*{{ end }}{{ end }}<\/p>/{{ end }}<\/p>/' layouts/partials/footer.html"
run_bg "a picture that sets a color itself" C7 "sed -i 's/<path class=\"fig-water\"/<path fill=\"#3366cc\" class=\"fig-water\"/' assets/figures/stocks-flows.svg"
run_bg "a picture color with no value for dark screens" C7 "sed -i '/prefers-color-scheme: dark) { :root { --fig-water/d' assets/css/pm.css"
run_bg "station numbers pushed low in their discs" R6 "echo '.st-name { padding-top: 2px; }' >> assets/css/pm.css"
run_bg "a module that runs past three pages" P1 "for i in \$(seq 60); do printf 'A filler paragraph that says nothing and only takes up room on the printed page.\n\n' >> content/pm/see-the-system.md; done"
run_bg "the Start page runs onto a third page" P1 "for i in \$(seq 60); do printf '\nA filler paragraph that says nothing and only takes up room on the printed page.\n' >> content/pm/_index.md; done"
run_bg "a concept card that runs onto a second page, though the glossary may run long" P1 "python3 -c \"p='content/pm/cards/many-hands.md'; s=open(p).read(); open(p, 'w').write(s + '\\n' + 'A filler sentence that only takes up room on the printed card. ' * 40 + '\\n')\""
run_bg "a built module the browser checks don't visit" X1 "sed -i '/(\"\/pm\/change-safely\/\"/d' tests/check_site.py"
run_bg "the hand-written correction dropped into the line" H2 "sed -i 's/^\.edit ins { display: flex;/.edit ins { display: inline;/' assets/css/base.css"
run_bg "the scratch drawn in one ink for light and dark" H2 "sed -i '/^  :root { --scratch-1:/d' assets/css/base.css"
run_bg "the hand-written correction pushing the words beside it apart" H2 "sed -i 's/ contain: inline-size;//' assets/css/base.css"
run_bg "the hand-written correction written level" H2 "sed -i 's/transform: rotate(-4deg);/transform: none;/' assets/css/base.css"
run_bg "the hand-written correction running past the end of its line" H2 "sed -i 's/if (over > 0) ins.style.translate/if (false) ins.style.translate/' assets/js/pm.js"
run_bg "a retired setting back in an example" S5 "sed -i 's/a tweak to sign-up/a change to a contact frequency rule/' content/pm/find-the-constraint.md"
run_bg "a source linked from Substack" S9 "printf '\n- [A newsletter post](https://example.substack.com/p/a-post), 5 minutes.\n' >> content/pm/notice-when-you-are-wrong.md"
run_bg "two stories on one full path" S10 "python3 -c \"p='content/pm/see-the-system.md'; s=open(p).read(); e='  - title: A Film About Change\n    by: Someone\n    where: A film.\n    only: The lesson again, on screen.\n'; open(p, 'w').write(s.replace('deeper:\n', 'deeper:\n' + e, 1))\""
run_bg "a full path with no story" S10 "sed -i '/^  - title: Ocean.s Eleven\$/,/^    only: /d' content/pm/decide-and-set-direction.md"
run_bg "a story asked to be trusted as evidence" S10 "sed -i 's/^    only: Goldratt first/    trust: It sold millions of copies.\n    only: Goldratt first/' content/pm/find-the-constraint.md"
run_bg "a sixth thing on a built full path" S11 "python3 -c \"p='content/pm/see-the-system.md'; s=open(p).read(); e='  - title: Another Book\n    by: Someone\n    where: A book.\n    trust: Peer-reviewed.\n    only: More of the same.\n'; open(p, 'w').write(s.replace('deeper:\n', 'deeper:\n' + e * 5, 1))\""
run_bg "a pair counted as one thing on a built full path" S11 "python3 -c \"p='content/pm/see-the-system.md'; s=open(p).read(); e='  - title: Another Book\n    by: Someone\n    where: A book.\n    trust: Peer-reviewed.\n    only: More of the same.\n'; pr='  - title: Two Shows\n    by: Someone\n    where: A pair of TV series, watched side by side.\n    only: A contrast.\n'; open(p, 'w').write(s.replace('deeper:\n', 'deeper:\n' + pr + e * 2, 1))\""
run_bg "a short article on a built full path" S12 "python3 -c \"p='content/pm/see-the-system.md'; s=open(p).read(); e='  - title: A Short Post\n    by: Someone\n    where: A blog post, about 5 minutes.\n    trust: A practitioner.\n    only: A summary.\n'; open(p, 'w').write(s.replace('deeper:\n', 'deeper:\n' + e, 1))\""
run_bg "Find the Constraint back to one book beside its story" S12 "sed -i '/^  - title: \\\"Accelerate/,/^    only: \\\"Goodhart/d' content/pm/find-the-constraint.md"
run_bg "an unchecked source on a built page" S7 "printf '\n*To check: nobody has opened this source yet.*\n' >> content/pm/see-the-system.md"
run_bg "a module that stops talking to the reader" E1 "sed -i 's/The danger while you work on it is/The danger in working on it is/; s/Before you trust a stand-in, ask/Before trusting a stand-in, ask/; s/a stock like the one you drew in See the System/a stock like the one drawn in See the System/; s/, you get more drafts piled up/, more drafts pile up/' content/pm/find-the-constraint.md"
run_bg "a module with its contractions spelled out" E2 "sed -i 's/\([Dd]\)on\x27t/\1o not/g; s/isn\x27t/is not/g; s/\([Ii]\)t\x27s/\1t is/g; s/doesn\x27t/does not/g; s/didn\x27t/did not/g; s/won\x27t/will not/g; s/can\x27t/cannot/g; s/you\x27re/you are/g; s/there\x27s/there is/g' content/pm/find-the-constraint.md content/pm/cards/five-focusing-steps.md content/pm/cards/goodharts-law.md layouts/partials/pm/dicegame.html data/pm/dicegame.yaml"
run_bg "an experience invented for the owner" E3 "printf '\nI learned this the hard way on my second team.\n' >> content/pm/see-the-system.md"
run_bg "a module with no source" X1 "sed -i '/^  page: decide-and-set-direction$/d' data/pm/modules.yaml"
run_bg "a draft left behind after its module is built" X1 "mkdir -p drafts/pm; cp content/pm/see-the-system.md drafts/pm/see-the-system.md; sed -i 's/^  page: see-the-system$/  page: see-the-system\n  draft: see-the-system\n  state: Left behind./' data/pm/modules.yaml"
run_bg "the tab drops what to look for" X2 "sed -i 's/paras += look(b) + reasons(b) + note_of(li)/paras += reasons(b) + note_of(li)/' tools-pm/source-doc.py"
run_bg "a word changed without reaching the working doc" X3 "sed -i 's/Nothing is sent anywhere./Nothing leaves your browser./' content/pm/_index.md"
run_bg "an owner's page's tab drops its later sections" X2 "sed -i 's/note\] + blocks(art.select_one(\".prose\")))$/note] + blocks(art.select_one(\".prose\"))[:5])/' tools-pm/source-doc.py"
run_bg "the ReadMe's tab runs its lines together" X2 "sed -i 's/br.replace_with(BREAK)/br.replace_with(\" \")/' tools-pm/source-doc.py"
run_bg "the owner's pages' tabs before About" X2 "sed -i 's/out = \[(\"About\", about_tab(mods, synced or today())), (DOOR_TAB, door_tab(site)),/out = [(DOOR_TAB, door_tab(site)), (\"About\", about_tab(mods, synced or today())),/' tools-pm/source-doc.py"
# The front door and Games have tabs too (27 November 2026): in order after About, every word, the photo's description and each link.
run_bg "the front door's tab and the ReadMe's out of order" X2 "sed -i 's/(DOOR_TAB, door_tab(site)), (README_TAB, readme_tab(site)),/(README_TAB, readme_tab(site)), (DOOR_TAB, door_tab(site)),/' tools-pm/source-doc.py"
run_bg "Games without a tab" X2 "sed -i 's/^           (GAMES_TAB, games_tab(site)),$/          /' tools-pm/source-doc.py"
run_bg "the front door's paragraphs left off its tab" X2 "sed -i 's/^    out += blocks(door.find(class_=\"door-text\"))$/    pass/' tools-pm/source-doc.py"
run_bg "the photo's description left off the front door's tab" X2 "sed -i 's/if photo and photo.get(\"alt\"):/if False:/' tools-pm/source-doc.py"
run_bg "a link under the photo left off the front door's tab" X2 "sed -i 's/for a in door.select(\".door-links a\")\]/for a in door.select(\".door-links a\")][1:]/' tools-pm/source-doc.py"
run_bg "a word of the ReadMe changed without reaching the working doc" X3 "sed -i 's/and avoiding exercise./and avoiding the gym./' content/page/readme.md"
run_bg "a word of the Games page changed without reaching the working doc" X3 "sed -i 's/I.m aiming to release it in March 2027./I.m aiming to release it in April 2027./' content/games/_index.md"
# X4: a voice slot on Start, placed as a paragraph of its own, added first in the list whatever slots are open. The
# mutations below each place it, then break one thing.
SLOT="sed -i 's/^slots:.*$/slots:\\n  - id: t\\n    unit: Start\\n    brief: Say what judgment is, in your own words.\\n    interim: Judgment is what you bring when the map runs out./' data/pm/voice-slots.yaml; printf '\\n{{< pm/voice \\\"t\\\" \\\"paragraph\\\" >}}\\n' >> content/pm/_index.md"
run_bg "a voice slot listed and placed nowhere" X4 "sed -i 's/^slots:.*$/slots:\\n  - id: t\\n    unit: Start\\n    brief: Say what judgment is.\\n    interim: For now./' data/pm/voice-slots.yaml"
run_bg "an open voice slot on its way to joestanley.org" X4 "$SLOT; sed -i 's/LIVE = \\[\\]  /LIVE = [True]/' tests/check_site.py"
run_bg "a voice slot's brief shown on the page" X4 "$SLOT; sed -i 's/{{ with \\\$s.interim }}/{{ \\\$s.brief }} {{ with \\\$s.interim }}/' layouts/shortcodes/pm/voice.html"
run_bg "the tab drops a voice slot's block" X4 "$SLOT; sed -i 's/    out = \\[slot_block(sid) for sid in PENDING\\]/    out = []/' tools-pm/source-doc.py"
run_bg "a voice slot as a paragraph, placed without saying so" X4 "$SLOT; sed -i 's/ \\\"paragraph\\\" >}}/ >}}/' content/pm/_index.md"
run_bg "a word of the owner's moved and not listed for his pass" X4 "sed -i 's/^  - what: moved$/  - what: shifted/' data/pm/voice-slots.yaml"
# The voice pass's tab starts from what his pass settles and ends with every empty margin slot (27 November 2026).
run_bg "what the owner's pass settles left off his tab" X4 "sed -i 's/    for i, e in enumerate(v\\[\"settle\"\\], 1):/    for i, e in enumerate([], 1):/' tools-pm/source-doc.py"
run_bg "a thing for the owner's pass with nothing asked" X4 "sed -i '0,/^    ask: /{/^    ask: /d}' data/pm/voice-slots.yaml"
run_bg "Start's empty margin slots left off the voice pass" X4 "sed -i 's/for u, n in units) if l\\]/for u, n in units[1:]) if l]/' tools-pm/source-doc.py"
run_bg "a module's empty margin slot left off the voice pass" X4 "sed -i 's/    parts = \\[label for k, label in empty\\]/    parts = [label for k, label in empty][1:]/' tools-pm/source-doc.py"
run_bg "link easing ignores reduced motion" D5 "sed -i '/@media (prefers-reduced-motion: reduce) { a, .recall/d' assets/css/base.css"
wait

# Joe's editing pass of 21 November 2026: his own sentences, simpler source entries, rounded times, notes beside a paragraph
run_bg "the owner's own sentence reworded" E3 "sed -i \"s/It's the variant I use of/It's the version I use of/\" content/pm/bring-people-with-you.md"
run_bg "borrow or buy back on a built full path" S13 "sed -i 's/^    where: A book\.$/    where: A book. Borrow it or buy it./' content/pm/see-the-system.md"
run_bg "a page count on a built full path" S13 "sed -i 's/^    where: A book\.$/    where: A book of about 240 pages./' content/pm/see-the-system.md"
run_bg "a full-path entry that hides its kind" S12 "sed -i 's/^    where: A journal article\.$/    where: Free online./' content/pm/own-your-role.md"
run_bg "a step's time off the owner's marks" S14 "sed -i 's/^    minutes: 20$/    minutes: 13/' content/pm/find-the-constraint.md"
run_bg "the header split into reading and doing again" S14 "sed -i 's|Takes about {{ partial \"pm/duration.html\" (add \$readMin \$doMin) }}.|Takes about {{ add \$readMin \$doMin }} minutes: {{ \$readMin }} reading, {{ \$doMin }} doing.|' layouts/partials/pm/unit-module.html"
run_bg "a note naming words its paragraph lost" M4 "sed -i 's/beside: \"Two versions of the job look real\"/beside: \"Three versions of the job\"/' data/pm/margin/own-your-role.yaml"
run_bg "a paragraph's note put before it" M3 "sed -i 's|(printf \`<div class=\"noted\" data-beside=\"%s\">%s%s</div>\` \$id . \$aside)|(printf \`<div class=\"noted\" data-beside=\"%s\">%s%s</div>\` \$id \$aside .)|' layouts/partials/pm/prose-slots.html"
run_bg "a paragraph's note left floating below it" M1 "sed -i '/\.reading \.noted > \.note { position: absolute/d' assets/css/base.css"
wait
run_bg "a module that pushes its full path past its three pages" P1 "python3 -c \"p='content/pm/own-your-role.md'; s=open(p).read(); open(p, 'w').write(s.replace('Now with all this said', 'A sentence that runs on to fill the page. ' * 160 + '\\n\\nNow with all this said', 1))\""
run_bg "a module without a game whose own text runs a second page over, past its grace until launch" P1 "python3 -c \"p='content/pm/map-the-domain.md'; s=open(p).read(); open(p, 'w').write(s.replace('The API\\'s shape follows', 'A sentence that runs on to fill the page. ' * 90 + 'The API\\'s shape follows', 1))\""
run_bg "a module with a game that runs past even a game's allowance" P1 "python3 -c \"p='content/pm/know-who-its-for.md'; s=open(p).read(); open(p, 'w').write(s.replace('Start with what people do, not what they say', 'A sentence that runs on to fill the page. ' * 120 + 'Start with what people do, not what they say', 1))\""
wait

# The print layout at two thirds (job 10, 21 November 2026): notes in a module's print margin, notes that run on
# past a full-path source and stack, and print at full size
run_bg "a module's text back to nearly the page's width in print" M1 "sed -i 's/  .module { --margin: 2in; --gutter: 0.3in; }/  .module { --margin: 0.5in; --gutter: 0.3in; }/' assets/css/pm.css"
run_bg "a paragraph's note printed over the text" M1 "sed -i 's/  .module .reading .noted > .note { position: absolute; top: 0; right: calc(-1 \* (var(--margin) + var(--gutter)));/  .module .reading .noted > .note { position: absolute; top: 0; right: 0;/' assets/css/pm.css"
run_bg "a paragraph's foot note pushed onto the next page" M1 "echo '@media print { .module .reading .noted { break-inside: auto; padding-bottom: 9in; } }' >> assets/css/pm.css"
run_bg "a full-path note holding room open again" M1 "echo '.reading .deeper-list > li > .note { position: static !important; }' >> assets/css/pm.css"
run_bg "stacked notes nearly touching in print" M2 "sed -i '/  .module .reading .note p { margin-bottom: var(--sp-2); }/d; /  .module .reading .note > :last-child { margin-bottom: 0; }/d' assets/css/pm.css"
run_bg "a full-path note running into the next one" M2 "sed -i 's/@supports (anchor-scope: --a)/@supports (anchor-scope: --a) and (not (display: block))/' assets/css/pm.css"
run_bg "a highlight reaching past the printed page" P7 "sed -i '/  .hl-line { margin-right: 0; }/d' assets/css/base.css"
wait

# Joe's answers of 21 November 2026: the full path's label kept to its own heading (R10), and his notes labeled
# "Sidenote:" wherever they fold in, in his hand in print on Start, the cards and the glossary (M1, M3)
run_bg "the full path's label reaching every Why this source" R10 "sed -i 's/^\.deeper > details > summary::after {/.deeper summary::after {/; s/^\.deeper > details\[open\] > summary::after {/.deeper details[open] summary::after {/' assets/css/pm.css"
run_bg "the full path's label floating over the first source" R10 "sed -i 's/display: block; margin-top: var(--sp-1); text-align: left;/float: right; margin-top: var(--sp-1);/' assets/css/pm.css"
# Joe's notes of 25 November 2026 on the course bar's card: the full path's label at the left (R10), and the bar's
# place orange on hover, as previous and next are (G1)
run_bg "the full path's label back at the right of the column" R10 "sed -i 's/display: block; margin-top: var(--sp-1); text-align: left;/display: block; margin-top: var(--sp-1); text-align: right;/' assets/css/pm.css"
run_bg "the full path's label orange at rest" C1 "sed -i 's/text-align: left; font: var(--w-strong) var(--fs-small)\/var(--lh-text) var(--ui); color: var(--ink);/text-align: left; font: var(--w-strong) var(--fs-small)\/var(--lh-text) var(--ui); color: var(--orange);/' assets/css/pm.css"
run_bg "the bar's place staying ink on hover" G1 "sed -i '/^.cb-open:hover, .cb-place:hover .cb-course { color: var(--orange); }$/d' assets/css/pm.css"
run_bg "a note folded in on a phone without its label" M1 "echo '@media (max-width: 63.99rem) { .note-label { position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%); } }' >> assets/css/base.css"
run_bg "a card's note printed typeset, not in the owner's hand" M1 "echo '@media print { .note { font-family: var(--ui) !important; } }' >> assets/css/pm.css"
# A card prints in two columns; a note there that breaks between them leaves its label at the foot of the first
# (27 November 2026, when the sample notes moved up a slot with the picture's gone and one landed on the break).
run_bg "a card's note split between its two printed columns" M1 "echo '@media print { .card-body .note::after { content: \"\"; display: block; break-before: column; height: 1px; } }' >> assets/css/pm.css"
run_bg "a note read aloud as a plain note again" M3 "sed -i 's/>Sidenote: </>Note: </g' layouts/partials/pm/margin.html layouts/partials/pm/prose-slots.html"
run_bg "a step's note out of line with the margin" M1 "echo '@media (min-width: 64rem) { .reading .step > .note { margin-left: var(--sp-5) !important; } }' >> assets/css/pm.css"
run_bg "a long note beside the full path's heading pushing the first source down" R10 "sed -i '/^    .deeper-list > li:has(> .note) { clear: none; }$/d' assets/css/pm.css"
run_bg "See the System back to one book beside its story" S12 "sed -i '/^  - title: The Field Guide/,/^    only: Cook.s point/d' content/pm/see-the-system.md"
wait

# Joe's picks of 22 November 2026: the kind as an icon on the full path (S15), Conway's sentence in his card's
# picture slot (S16), the hour in words in a module's header (S14), and a step that reads on in the one before (S2)
run_bg "a film shown with the article icon" S15 "sed -i 's/(?:classic )?(?:film|/(?:classic )?(?:flim|/' layouts/partials/pm/kind-icon.html"
run_bg "the kind's words shown to the eye beside the icon" S15 "sed -i 's/<p class=\"meta-line kind-line sr\">/<p class=\"meta-line kind-line\">/' layouts/partials/pm/unit-module.html"
run_bg "the header's hour back in digits" S14 "sed -i 's/{{- else if eq \$h 1 }}an hour/{{- else if eq \$h 1 }}1 hour/' layouts/partials/pm/duration.html"
run_bg "a step that reads on in a step that isn't the one before it" S2 "sed -i 's/    continues: meadows-1/    continues: card-stocks/' content/pm/see-the-system.md"
run_bg "a comma back outside a closing quotation mark" T9 "sed -i 's/\"Leverage Points,\" first half/\"Leverage Points\", first half/' content/pm/see-the-system.md"
run_bg "a period back outside a quoted title in a source's note" T9 "sed -i 's/Aspiring Superforecasters.\\\\\"/Aspiring Superforecasters\\\\\"./' content/pm/weigh-the-evidence.md"
run_bg "an em dash in the voice guide, which lives in pm-sources" T3 "mkdir .pm-sources && cp \"\${PM_SOURCES:-\$SRC/../pm-sources}/VOICE.md\" .pm-sources/ && printf '\\nA line \\xe2\\x80\\x94 with an em dash.\\n' >> .pm-sources/VOICE.md"
run_bg "a Check that doesn't end beyond its module" J1 "sed -i 's/\*\*Beyond this module\.\*\* You.ve said no/You have said no/' content/pm/decide-and-set-direction.md"
run_bg "a collision with no against" J2 "sed -i '/^    against: see-the-system$/d' content/pm/find-the-constraint.md"
run_bg "a collision set against a later module" J2 "sed -i 's/^    against: own-your-role$/    against: weigh-the-evidence/' content/pm/mind-the-seams.md"
run_bg "the log's review under the wrong label" J3 "sed -i 's/^\*\*Review your decision log (15 minutes)\.\*\*/**For your decision log.**/' content/pm/notice-when-you-are-wrong.md"
run_bg "the log's review without its minutes" J3 "sed -i 's/^\*\*Review your decision log (15 minutes)\.\*\*/**Review your decision log.**/' content/pm/notice-when-you-are-wrong.md"
run_bg "a log line that shows a time" J3 "sed -i 's/^\*\*For your decision log\.\*\*/**For your decision log (5 minutes).**/' content/pm/see-the-system.md"
run_bg "the log's review shown to nobody" J3 "sed -i 's/ Outside the 15 minutes, show it to your manager or a mentor: which call would they have made differently?//' content/pm/notice-when-you-are-wrong.md"
run_bg "only two collisions pick a winner" J2 "sed -i '/^    wins: find-the-constraint$/d' content/pm/find-the-constraint.md"
run_bg "a collision's winner from neither side" J2 "sed -i 's/^    wins: weigh-the-evidence$/    wins: see-the-system/' content/pm/weigh-the-evidence.md"
run_bg "the decision log's line after the optional exercise" J3 "python3 -c 'p=\"content/pm/find-the-constraint.md\"; s=open(p).read(); l=[x for x in s.split(chr(10)) if x.startswith(\"**For your decision log.**\")][0]; s=s.replace(l+chr(10)+chr(10), \"\", 1).rstrip()+chr(10)+chr(10)+l+chr(10); open(p, \"w\").write(s)'"
run_bg "a module that names no earlier one" J4 "sed -i 's| The longest wait you mapped in {{< pm/mod find-the-constraint >}} may well sit at one of them\\.||' content/pm/mind-the-seams.md"
run_bg "a game that doesn't say what it leaves out" J5 "sed -i '/<p class=\"limits\">/d' layouts/partials/pm/rankinggame.html"
run_bg "an average the waiting game's jobs don't give" J5 "sed -i 's/^    average: 570000$/    average: 507000/' data/pm/waitgame.yaml"
run_bg "a narrow estimate said to move the waiting game's order" J5 "sed -i 's/^moves: \\[swaps\\]$/moves: [fix, swaps]/' data/pm/waitgame.yaml"
run_bg "the ranking game's trial odds off the exact numbers" J5 "sed -i 's/trial_better_one: 80,/trial_better_one: 90,/' data/pm/rankgame.yaml"
run_bg "the waiting game off the short path" J5 "sed -i '/^  - id: waiting$/,/^    look: Which estimate is worth testing/d' content/pm/know-who-its-for.md"
run_bg "the waiting game's result a week off its board" A8 "sed -i 's/ + \" after week \" + p\[id\]\.live; });/ + \" after week \" + (p[id].live + 1); });/' assets/js/pm.js"
run_bg "the ranking game's board hiding the small stores among the worst" A8 "sed -i 's/dot.classList.toggle(\"is-worst\", has \&\& worst.indexOf(i) >= 0);/dot.classList.toggle(\"is-worst\", has \&\& worst.indexOf(i) >= 0 \&\& group[i] > 0);/' assets/js/pm.js"
run_bg "the waiting game's Play disabled during a run" A9 "sed -i 's/running = true; busyOn(el.play, true);/running = true; el.play.disabled = true;/' assets/js/pm.js"
run_bg "the waiting game's recorded orders hidden without JavaScript" D1 "echo '.game[data-game=waiting] .example { display: none; }' >> assets/css/pm.css"
run_bg "the waiting game animated with reduced motion" D5 "sed -i 's/if (still()) { while (step()) {} return; }//' assets/js/pm.js"
run_bg "the waiting game playing past a pick left open" A8 "sed -i 's/if (rule === \"stop\" || rule === \"test\") {/if (true) {/' assets/js/pm.js"
run_bg "the ranking game's trial miscounting the fixed stores among the worst" A8 "sed -i 's/var n_ = worst.filter(function (i) { return i < F; }).length;/var n_ = worst.filter(function (i) { return i < F; }).length + 1;/' assets/js/pm.js"
wait

# Job 34, the mechanics pass (23 November 2026): one main setting a module (S6), and every source's kind of evidence
# named first in its "Why trust it" (S17)
run_bg "a module that names no main setting" S6 "sed -i '/^setting: a fitness app$/d' content/pm/find-the-constraint.md"
run_bg "one setting leading three modules" S6 "sed -i 's/^setting: a ride-hailing app$/setting: a grocery delivery app/' content/pm/see-the-system.md"
run_bg "a Why trust it that hides its kind of evidence" S17 "sed -i 's/^    trust: \"Experience. Forte runs/    trust: \"Forte runs/' content/pm/find-the-constraint.md"
run_bg "the reflexive not a study back in a card" S17 "sed -i 's/on the limits of her own field\./on the limits of her own field, not a study./' content/pm/cards/stocks-flows-feedback.md"
run_bg "every source's reasons printed twice at the back of the PDF" S4 "sed -i 's/^{{ \$list }}\$/{{ \$list }}{{ \$list }}/' layouts/partials/pm/source-notes.html"
# Job 18, the preview (23 November 2026): the whole site in one page on claude.ai, as joestanley.org shows it (X5)
run_bg "the preview leaves ids as they were, so two pages' ids meet" X5 "sed -i 's/^                new = self.pid(val)$/                new = val/' tools/preview.py"
run_bg "the preview ignores a dark theme picked in claude.ai" X5 "sed -i 's/{{{explicit}}}/{{}}/' tools/preview.py"
run_bg "the preview shows each page with the other page's stylesheet" X5 "sed -i 's/? \"all\" : \"not all\"; });/? \"not all\" : \"all\"; });/' tools/preview.py"
run_bg "a link to a page the preview doesn't hold" X5 "printf '\nThe [archive](/pm/archive/) holds the rest.\n' >> content/pm/find-the-constraint.md"
# The pull from inside (23 November 2026): Answer for What You Build runs longer on purpose, says so first, and may
# recommend six on its full path (S11), with a game's allowance in print (P1)
run_bg "the long module no longer says it runs longer" S11 "sed -i '/^This module runs longer than the others, on purpose/d' content/pm/answer-for-what-you-build.md"
run_bg "a seventh thing on the long module's full path" S11 "python3 -c \"p='content/pm/answer-for-what-you-build.md'; s=open(p).read(); e='  - title: Another Book\n    by: Someone\n    where: A book.\n    trust: An argument. Someone.\n    only: More of the same.\n'; open(p, 'w').write(s.replace('deeper:\n', 'deeper:\n' + e, 1))\""
run_bg "the long module running past even its longer allowance" P1 "for i in \$(seq 60); do printf 'A filler paragraph that says nothing and only takes up room on the printed page.\n\n' >> content/pm/answer-for-what-you-build.md; done"
# Job 22, Joe's line on Start (23 November 2026): an invitation to write, with his address shown as text (S19)
run_bg "Start's invitation to write gone" S19 "sed -i '/^This is largely a synthesis of the work of others/d' content/pm/_index.md"
run_bg "Start's address hidden under other words" S19 "sed -i 's|Tell me why at {{< pm/email >}}|[Tell me why](mailto:mail@joestanley.org)|' content/pm/_index.md"
run_bg "Start's invitation folded into How it works' list" S19 "sed -i 's/^This is largely a synthesis/- This is largely a synthesis/' content/pm/_index.md"
# Job 29, the two ends (23 November 2026): the arc on Start (S20) and The Compass, the closing unit (S21)
run_bg "a module left out of the arc" S20 "sed -i 's/modules: \\[own-your-role, know-who-its-for\\]/modules: [own-your-role]/' data/pm/arc.yaml"
run_bg "the arc's part names gone from Start" S20 "sed -i '/^<p class=\"arc-part\"><strong id=\"arc-{{ \$where }}-{{ \$i }}\">/d' layouts/partials/pm/arc-list.html"
run_bg "The Compass gone from Start's list" S20 "sed -i 's/{{- if \\\$start }}{{ with site.Data.pm.arc.closing }}/{{- if false }}{{ with site.Data.pm.arc.closing }}/' layouts/partials/pm/arc-list.html"
run_bg "The Compass's framing not in a voice slot" S21 "sed -i '/pm\\/voice \"compass-framing\"/d' content/pm/the-compass.md"
run_bg "The Compass's walk-through with no collision" S21 "sed -i '/^Here two questions collide/d' content/pm/the-compass.md"
run_bg "Start's How it works without the closing page" S21 "sed -i 's/, then a closing page\\./\\./; s| The closing page, \\[The Compass\\](/pm/the-compass/), has you look back over it, and names \\[what the course leaves out\\](/pm/the-compass/#what-the-course-leaves-out)\\.||' content/pm/_index.md"
run_bg "The Compass's Do not reviewing the log" J3 "sed -i 's/^\\*\\*Review your decision log (20 minutes)\\.\\*\\*/**Look back (20 minutes).**/' content/pm/the-compass.md"
run_bg "The Compass a page too long" P1 "python3 -c \"p='content/pm/the-compass.md'; s=open(p).read(); a=s.index('Real calls'); b=s.index('## Do'); open(p, 'w').write(s[:b] + s[a:b] + s[b:])\""
run_bg "The Compass bookmarked without its kind" P6 "sed -i 's/u\\[\"label\"\\] = f\"In closing: {u\\[.title.\\]}\"/u[\"label\"] = u[\"title\"]/' tools-pm/make-pdf.py"
run_bg "The Compass without a tab" X2 "sed -i 's/    if closing and closing in arts:/    if False:/' tools-pm/source-doc.py"
run_bg "The Compass not on the checks' list" X1 "sed -i 's/ + \\[CLOSING\\]$//' tests/check_site.py"
run_bg "The Compass's call walked once, the platform gone" S21 "python3 -c \"p='content/pm/the-compass.md'; s=open(p).read(); a=s.index('{{< pm/walk \\\"platform\\\" >}}'); b=s.index('{{< /pm/walk >}}', a) + 16; open(p, 'w').write(s[:a] + s[b:])\""
run_bg "The Compass's buttons pick nothing" S21 "sed -i 's/w.hidden = w.getAttribute(\"data-walk\") !== id;/w.hidden = false;/' assets/js/pm.js"
# Job 32, AI and the new readings (23 November 2026): the AI and data threads, in the course's own frames (S22)
run_bg "Change Safely's model-and-rule line cut" S22 "sed -i '/^That.s harder to say when the output varies/d' content/pm/change-safely.md"
run_bg "the Many Hands card's model bullet cut" S22 "sed -i '/A model passes through many hands, too/d' content/pm/cards/many-hands.md"
run_bg "The Compass without the data thread's questions" S22 "sed -i '/^Data ran through the course/d' content/pm/the-compass.md"
run_bg "the threads' list gone" S22 "rm data/pm/threads.yaml"
# Job 16, launch plumbing (24 November 2026): no placeholder (N1), the 404 page (N2), link previews (N3), Writing out of the
# menu (R9), and P1's allowances, which hold until a PDF is published
run_bg "the front door's placeholder note back" N1 "sed -i 's/^I.m based in Richmond/<!-- Placeholder: rewrite these in your own voice. -->\\nI.m based in Richmond/' content/_index.md"
run_bg "Writing built again, empty" N2 "sed -i '/^build:/,/^  list: never/d' content/writing/_index.md"
run_bg "Writing built again, saying it has nothing yet" N1 "sed -i '/^build:/,/^  list: never/d' content/writing/_index.md"
run_bg "the old site's /page/ built again" N2 "rm content/page/_index.md"
run_bg "a missing page that stays put" N2 "sed -i '/http-equiv=\"refresh\"/d' layouts/_default/baseof.html"
run_bg "a missing page that points to the ReadMe" N2 "sed -i 's|<a href=\"{{ \"/\" \| relURL }}\">Go to the front door.</a>|<a href=\"/page/readme/\">Read the ReadMe.</a>|' layouts/404.html"
run_bg "the photo in every page's preview" N3 "sed -i 's/{{- if or .IsHome (eq .RelPermalink \"\/page\/readme\/\") }}/{{- if true }}/' layouts/_default/baseof.html"
run_bg "no summary card for other sites" N3 "sed -i '/twitter:card/d' layouts/_default/baseof.html"
run_bg "a preview's address off the site" N3 "sed -i 's/<meta property=\"og:url\" content=\"{{ .Permalink }}\">/<meta property=\"og:url\" content=\"{{ .RelPermalink }}\">/' layouts/_default/baseof.html"
# Job 21, the site's icon (27 November 2026): the drawing, the links in every head, and the files made from it (N4).
run_bg "a page that links no home-screen icon" N4 "sed -i '/rel=\"apple-touch-icon\"/d' layouts/_default/baseof.html"
run_bg "the icon's drawing left out of the head" N4 "sed -i '/favicon.svg/d' layouts/_default/baseof.html"
run_bg "the icon's disc in another orange" N4 "sed -i 's/fill=\"#c84b00\"/fill=\"#e2571a\"/' static/favicon.svg"
run_bg "a third shape in the icon's drawing" N4 "sed -i 's|</svg>|<rect x=\"2\" y=\"2\" width=\"4\" height=\"4\" fill=\"#ffffff\"/></svg>|' static/favicon.svg"
run_bg "the site's orange changed and the made icons left as they were" N4 "sed -i '0,/--orange: #c84b00;/s//--orange: #b34300;/' assets/css/base.css; sed -i 's/fill=\"#c84b00\"/fill=\"#b34300\"/' static/favicon.svg"
run_bg "the home-screen icon missing" N4 "rm static/apple-touch-icon.png"
run_bg "the home-screen icon with nothing behind the disc" N4 "python3 -c \"from PIL import Image; i = Image.open('static/apple-touch-icon.png').convert('RGBA'); i.putpixel((0, 0), (0, 0, 0, 0)); i.save('static/apple-touch-icon.png')\""
run_bg "a manifest that names a file that isn't there" N4 "sed -i 's|/icon-512.png|/icon-1024.png|' static/site.webmanifest"
run_bg "Writing back in the menu" R9 "sed -i 's/^    - identifier: games$/    - identifier: writing\\n      name: Writing\\n      url: \\/writing\\/\\n      weight: 30\\n    - identifier: games/' hugo.yaml"
run_bg "a module's allowance in print gone before a PDF is published" P1 "sed -i 's/^MODULE_GRACE = 1 /MODULE_GRACE = 0 /' tests/check_site.py"
# Job 40, the course bar and the foot (25 November 2026): first on Find the Constraint and its card The Five Focusing
# Steps, then on every syllabus page once the owner spread them (G1 to G5); the bar's links are controls, not running
# text (C5)
run_bg "the bar scrolls away with the page" G1 "sed -i 's/^.course-bar { position: sticky;/.course-bar { position: relative;/' assets/css/pm.css"
# The count comes from the map, so it followed Map the Domain's return from twelve to thirteen (26 November 2026).
run_bg "the bar counts twelve modules, not the map's" G1 "sed -i 's/\$suf (len site.Data.pm.modules) }}/\$suf 12 }}/' layouts/partials/pm/course-bar.html"
run_bg "the bar's list without its progress" G1 "sed -i 's/ data-map-short{{ end }}>/{{ end }}>/; s/<span class=\"cb-status\" data-map-status><\/span>//' layouts/partials/pm/course-bar.html"
run_bg "a syllabus page without the bar" G1 "sed -i 's/{{- \$bar := and \$pm (not \$all) }}/{{- \$bar := and \$pm (not \$all) (ne .Layout \"glossary\") }}/' layouts/_default/baseof.html"
run_bg "the bar on the single document" G1 "sed -i 's/{{- \$bar := and \$pm (not \$all) }}/{{- \$bar := \$pm }}/' layouts/_default/baseof.html"
run_bg "Escape closes the list and drops focus" G2 "sed -i 's/if (!on \&\& refocus) btn.focus();//' assets/js/pm.js"
# A phone's bar is its place alone since card bar-arrows (25 November 2026), so the small target is the place
run_bg "the bar's place too small to tap on a phone" G2 "echo '.course-bar .cb-place { min-height: 2rem; }' >> assets/css/pm.css"
run_bg "the bar's list fades in" G2 "echo '.cb-menu { transition: opacity 200ms ease-out; }' >> assets/css/pm.css"
run_bg "an address lands under the bar" G2 "sed -i '/^.has-course-bar main \[id\] { scroll-margin-top/d' assets/css/pm.css"
# The check clicks outside the bar on a spot with nothing to tap, outside the open list, which thirteen modules
# stretch to a phone's foot (26 November 2026): a click there must still close the list.
run_bg "a click outside the bar leaves its list open" G2 "sed -i 's/doc.addEventListener(\"click\", function (e) { if (!menu.hidden \&\& !bar.contains(e.target)) open(false); });//' assets/js/pm.js"
run_bg "the bar on two lines on a phone" G3 "echo '.cb-here::after { content: \" and a longer place\"; }' >> assets/css/pm.css"
run_bg "the bar's list runs past a short window" G3 "sed -i 's/if (on) fit();//' assets/js/pm.js; sed -i 's/ max-height: calc(100svh - 4rem); overflow-y: auto;//' assets/css/pm.css"
run_bg "without scripts the bar's place goes nowhere useful" G4 "sed -i 's|#modules\"><span class=\"cb-label\">|\"><span class=\"cb-label\">|' layouts/partials/pm/course-bar.html"
run_bg "the bar prints" G4 "sed -i 's/, .tick input, .course-bar { display: none !important; }/, .tick input { display: none !important; }/' assets/css/pm.css"
run_bg "a module's foot with All modules back" G5 "sed -i 's|<nav class=\"unit-foot screen-only\" aria-label=\"Next\">|<nav class=\"unit-foot screen-only\" aria-label=\"Next\"><p><a href=\"/pm/#modules\">All modules</a></p>|' layouts/partials/pm/unit-foot.html"
run_bg "a card's foot back to the module's top, not its step" G5 "sed -i 's/{{ if \$step }}#step-{{ \$step }}{{ end }}//' layouts/partials/pm/unit-foot.html"
run_bg "steps without addresses" G5 "sed -i 's/{{ if not \$all }} id=\"step-{{ add \$i 1 }}\"{{ end }}//' layouts/partials/pm/unit-module.html"
run_bg "the foot's links without their underline" C5 "echo '.unit-foot a { text-decoration: none; }' >> assets/css/pm.css"
# Job 48, Joe's four cards of 25 November 2026: the menu's label and its Menu button on a phone (R9), and the bar as a
# band hung from the menu's line, its words quieter, one chevron on a phone and a fade once stuck (G1 to G4)
run_bg "the menu calls the syllabus Product Judgment again" R9 "sed -i 's/      name: On Judgment/      name: Product Judgment/' hugo.yaml"
run_bg "no current section beside the Menu button" R9 "sed -i '/class=\"nav-here\"/d' layouts/partials/header.html"
run_bg "the menu's list closes on its own" R9 "sed -i 's/btn.addEventListener(\"click\", function () { open(!isOpen()); });/btn.addEventListener(\"click\", function () { open(!isOpen()); setTimeout(function () { open(false); }, 200); });/' assets/js/site.js"
run_bg "a scroll leaves the menu's list open" R9 "sed -i '/if (Math.abs(window.scrollY - from) > 8) open(false);/d' assets/js/site.js"
run_bg "a scroll closes the menu's list while a reader tabs through it" R9 "sed -i 's/if (!isOpen() || (nav.contains(doc.activeElement) \&\& doc.activeElement !== btn)) return;/if (!isOpen()) return;/' assets/js/site.js"
run_bg "a scroll closes a menu's list too tall for the window" R9 "sed -i '/      if (tall) return;/d' assets/js/site.js"
run_bg "the menu's list under the course bar" R9 "sed -i 's/^.masthead { position: relative; z-index: 6; }/.masthead { position: static; }/' assets/css/base.css"
run_bg "the Menu button too small to tap" R9 "echo '.site-nav .nav-open { min-height: 1rem !important; }' >> assets/css/base.css"
run_bg "Escape closes the menu and drops focus" R9 "sed -i 's/if (!on \&\& refocus) btn.focus();//' assets/js/site.js"
run_bg "no room for Writing on a wide screen" R9 "echo '@media (min-width: 46rem) { .nav-list a { padding-left: 6rem; } }' >> assets/css/base.css"
run_bg "without scripts, no sections on a phone" R9 "echo '@media (max-width: 45.99rem) { .nav-list { display: none; } }' >> assets/css/base.css"
run_bg "the menu's list from edge to edge" R9 "sed -i 's/  .has-menu .nav-list.is-open { position: absolute; top: 100%; right: calc(-1 \* var(--pad)); width: max-content; min-width: calc(100% + var(--pad) + var(--sp-4));/  .has-menu .nav-list.is-open { position: absolute; top: 100%; right: calc(-1 * var(--pad)); width: 100vw;/' assets/css/base.css"
run_bg "the menu's list keeps the current section" R9 "sed -i '/^  .has-menu .nav-list.is-open a\[aria-current\] { display: none; }$/d' assets/css/base.css"
run_bg "the menu's rows a link only across their words" R9 "echo '.has-menu .nav-list.is-open a { align-self: flex-start; }' >> assets/css/base.css"
run_bg "the menu and the bar's list open together" R9 "sed -i 's/btn.addEventListener(\"click\", function () { open(!isOpen()); });/btn.addEventListener(\"click\", function (e) { e.stopPropagation(); open(!isOpen()); });/' assets/js/site.js"
run_bg "the bar back on the page's paper" G1 "sed -i 's/^.course-bar { position: sticky; top: 0; z-index: 5; background: var(--tint);/.course-bar { position: sticky; top: 0; z-index: 5; background: var(--paper);/' assets/css/pm.css"
run_bg "a gap between the menu's line and the band" G1 "echo '.course-bar { margin-top: var(--sp-3); }' >> assets/css/pm.css"
run_bg "the course as dark as the place" G1 "sed -i '/^.cb-course { color: var(--muted); }$/d' assets/css/pm.css"
run_bg "a rule under the band" G1 "echo '.course-bar { border-bottom: 1px solid var(--rule); }' >> assets/css/pm.css"
run_bg "arrows back on previous and next" G1 "sed -i 's|rel=\"prev\">Previous|rel=\"prev\"><span class=\"cb-chev cb-left\" aria-hidden=\"true\"></span>Previous|' layouts/partials/pm/course-bar.html"
run_bg "previous and next back in the bar on a phone" G1 "sed -i '/^@media (max-width: 45.99rem) { .cb-steps > :not(.cb-continue) { display: none; } }$/d' assets/css/pm.css"
run_bg "no fade once the bar sticks" G1 "sed -i 's/^.course-bar.is-stuck::after/.course-bar.never-stuck::after/' assets/css/pm.css"
run_bg "the fade in the band's tint, not the page's paper" G1 "sed -i 's/background: linear-gradient(var(--paper), transparent)/background: linear-gradient(var(--tint), transparent)/' assets/css/pm.css"
run_bg "the fade showing at rest" G1 "sed -i 's/bar.classList.toggle(\"is-stuck\", window.scrollY > 0 \&\& bar.getBoundingClientRect().top <= 0.5);/bar.classList.add(\"is-stuck\");/' assets/js/pm.js"
run_bg "the fade eases in" G2 "echo '.course-bar::after { transition: opacity 300ms ease-out; }' >> assets/css/pm.css"
run_bg "without scripts the bar's place shows a chevron" G4 "sed -i 's|<span class=\"cb-here\">{{ \$place }}</span></span></a>|<span class=\"cb-here\">{{ \$place }}</span></span><span class=\"cb-chev cb-down\" aria-hidden=\"true\"></span></a>|' layouts/partials/pm/course-bar.html"
wait
# Job 40's spread (25 November 2026): the foot trimmed to one step onward, the owner's pick in the session (G5), and
# Start's Continue, from saved progress, in place of Next (G1); The Compass and the glossary mark their place (G2)
run_bg "a card's foot with its other card back" G5 "sed -i 's|{{ \$mod.Title }}</a></p>|{{ \$mod.Title }}</a></p><p><a href=\"/pm/glossary/\">Its other card</a></p>|' layouts/partials/pm/unit-foot.html"
run_bg "a module's foot steps back, not on" G5 "sed -i 's/{{ with index \$order (add \$i 1) }}/{{ with index \$order (sub \$i 1) }}/' layouts/partials/pm/unit-foot.html"
run_bg "Start's bar without Continue" G1 "sed -i '/data-continue hidden>/d' layouts/partials/pm/course-bar.html"
run_bg "Continue only for a module half done" G1 "sed -i 's/if (!to \&\& last >= 0) {/if (false) {/' assets/js/pm.js"
run_bg "Continue beside Next, not in its place" G1 "sed -i 's/if (next) next.hidden = true;//' assets/js/pm.js"
run_bg "Continue hidden on a phone" G1 "sed -i 's/^@media (max-width: 45.99rem) { .cb-steps > :not(.cb-continue) { display: none; } }$/@media (max-width: 45.99rem) { .cb-steps { display: none; } }/' assets/css/pm.css"
run_bg "The Compass not marked as the place in the bar's list" G2 "sed -i 's/ data-label=\"{{ .Title }}\"{{ if eq \$p . }} aria-current=\"page\"{{ end }}/ data-label=\"{{ .Title }}\"/' layouts/partials/pm/course-bar.html"
# The short path's items are its steps wherever a reader sees them, and a card's foot names its module alone (the owner,
# 25 November 2026, on seeing "stop 3" in a card's foot, a word the site had never taught) (G5)
run_bg "a card's foot names the stop's number again" G5 "sed -i 's|{{ \$mod.Title }}</a></p>|{{ \$mod.Title }}, stop {{ \$step }}</a></p>|' layouts/partials/pm/unit-foot.html"
run_bg "the line above the short path says stops" G5 "sed -i 's/ steps. Tap a step/ stops. Tap a step/' assets/js/pm.js"
run_bg "Start's list says stops" G5 "sed -i 's/n + \" of \" + total + \" steps done\";/n + \" of \" + total + \" stops done\";/' assets/js/pm.js"
# Job 40's doors and the ways around inside a module (the owner's picks of 25 November 2026, from job 36's review):
# the concept cards' page, the pop-up's way to the glossary, where a term is used and the entry landed on (G6); a
# module's line of links, its headings' addresses, a game's way back and its tick, and a phone's targets (G7)
run_bg "the concept cards' page drops a module's second card" G6 "sed -i 's/      {{- range . }}/      {{- range first 1 . }}/' layouts/partials/pm/unit-cards.html"
run_bg "the concept cards' page without each card's question" G6 "sed -i 's|{{ with .Params.question }}<p class=\"ci-question\">{{ . }}</p>{{ end }}||' layouts/partials/pm/unit-cards.html"
run_bg "the concept cards' page left out of the bar's list" G1 "sed -i '/site.GetPage \"\/pm\/concept-cards\"/,+2d' layouts/partials/pm/course-bar.html"
run_bg "Start without its Look up line" G6 "sed -i '/<nav class=\"on-page start-more screen-only\"/,/<\/nav>/d' layouts/partials/pm/unit-start.html"
run_bg "a card's label no longer a way to the concept cards" G6 "sed -i 's|<a class=\"tag\" href=\"{{ .RelPermalink }}\">Concept card</a>|<span class=\"tag\">Concept card</span>|' layouts/partials/pm/unit-card.html"
run_bg "a term's pop-up with no way to the glossary" G6 "sed -i '/<a class=\"gloss-more\"/d' layouts/partials/pm/glossary-dialogs.html"
run_bg "the pop-up's way to the glossary leaves the single document" G6 "sed -i 's/{{ if \$all }}{{ else }}/{{ if false }}{{ else }}/' layouts/partials/pm/glossary-dialogs.html"
run_bg "where a term is used leaves out the cards" G6 "sed -i '/RegularPagesRecursive/s/{{ \$units = \$units | append (dict \"p\" . \"label\" .Title) }}//' layouts/partials/pm/unit-glossary.html"
run_bg "the entry a link lands on is unmarked" G6 "sed -i '/^.gloss-list > div:target > dt/d' assets/css/pm.css"
run_bg "the line of links names a part wrongly" G7 "sed -i 's|<a href=\"#short-path\">Short path</a>|<a href=\"#short-path\">The path</a>|' layouts/partials/pm/unit-module.html"
run_bg "a section heading without an address" G7 "sed -i 's/{{ if not \$all }} id=\"check\"{{ end }}//' layouts/partials/pm/unit-module.html"
run_bg "a game without its way back" G7 "sed -i '/<p class=\"game-back screen-only\">/d' layouts/partials/pm/unit-module.html"
run_bg "a finished round ticks nothing" G7 "sed -i '/^      played(game);$/d' assets/js/pm.js"
# "Go deeper" opens the full path two ways, by its click and by arriving at its address: take both away
run_bg "a finished round ticks its step without saying so" G7 "sed -i '/if (said) said.textContent = /d' assets/js/pm.js"
run_bg "a card's foot too small to tap on a phone" G7 "sed -i 's/  .card .kicker a, .unit-foot .uf-step a { display: inline-flex;/  .card .kicker a { display: inline-flex;/' assets/css/pm.css"
run_bg "Go deeper lands on the full path shut" G7 "sed -i '/all(\"\[data-open-deeper\]\")/d; s/if (location.hash === \"#go-deeper\") openDeeper();//' assets/js/pm.js"
run_bg "a phone's Why this source under 44 pixels" G7 "sed -i '/^  .why > summary { display: flex; align-items: center; min-height: 2.75rem; padding: 0; }$/d' assets/css/pm.css"
run_bg "a card's way to its module under 44 pixels on a phone" G7 "sed -i '/^  .card .kicker a { display: inline-flex;/d' assets/css/pm.css"
run_bg "Start silent on what Done means" G7 "sed -i 's/ Its last two are the Do and the Check, so a module reads Done once you.ve done everything in it but the full path. How well you did them is yours to judge.//' content/pm/_index.md"
# What a good one looks like (J7): its form, its place, its length and the screen alone; its phone target (G7) and its tab (X2)
run_bg "an example with four lines on what makes it good" J7 "sed -i 's/^    - The call expects one thing you can count, by a date, and says why you.re only that sure\.$/&\n    - One more line./' content/pm/know-who-its-for.md"
run_bg "an example that prints" J7 "sed -i 's/<details class=\"example screen-only\"/<details class=\"example\"/' layouts/shortcodes/pm/example.html"
run_bg "an example above the decision log line" J7 "sed -i '/^{{< pm\/example >}}$/d; s/^\*\*Start a decision log\.\*\*/{{< pm\/example >}}\n\n&/' content/pm/know-who-its-for.md"
run_bg "an example run long" J7 "sed -i 's/Know by April 30\.$/Know by April 30, and look again then at what the tickets and the shoppers say, so the next call starts from what happened rather than from what was hoped./' content/pm/know-who-its-for.md"
# Every built module has one, since the eleven were written on 26 November 2026, and Own Your Role's, whose Do comes
# before the log starts, follows its main exercise
run_bg "a built module without its example" J7 "sed -i '/^{{< pm\/example >}}$/d; s/^example:$/unused_example:/' content/pm/see-the-system.md"
run_bg "Own Your Role's example below its optional exercise" J7 "sed -i '/^{{< pm\/example >}}$/d; s/^\*\*Optional: map your scope.*/&\n\n{{< pm\/example >}}/' content/pm/own-your-role.md"
run_bg "a phone's What a good one looks like under 44 pixels" G7 "sed -i 's/^  .why > summary, .example > summary { display: flex;/  .why > summary { display: flex;/' assets/css/pm.css"
run_bg "an example left out of its module's tab" X2 "sed -i 's/or \"walk-toggle\" in cls:/or \"walk-toggle\" in cls or \"example\" in cls:/' tools-pm/source-doc.py"
# The pilot of the Do's step (J7): the example's gate until the Do is ticked, the example there without scripts
run_bg "an example that opens before the Do is ticked" J7 "sed -i 's/function show() { gate.hidden = box.checked; body.hidden = !box.checked; }/function show() { gate.hidden = true; body.hidden = false; }/' assets/js/pm.js"
run_bg "a gate whose button ticks nothing" J7 "sed -i '/^      if (!box.checked) { box.checked = true; box.dispatchEvent(new Event(\"change\")); }$/d' assets/js/pm.js"
run_bg "an example hidden from a reader without scripts" J7 "sed -i 's/<div class=\"example-body\" tabindex=\"-1\">/<div class=\"example-body\" tabindex=\"-1\" hidden>/' layouts/shortcodes/pm/example.html"
run_bg "the Do's and the Check's steps leading nowhere" G7 "sed -i 's|<h3><a href=\"#{{ .kind }}\">{{ .title }}</a></h3>|<h3>{{ .title }}</h3>|' layouts/partials/pm/unit-module.html"
run_bg "the Do's minutes shown on its step too" G7 "sed -i 's/^    kind: do$/&\n    minutes: 30/' content/pm/know-who-its-for.md"
wait
# Job 50 (the owner's answers of 26 November 2026): the Do and the Check as the short path's last two steps, Continue
# to the next unticked step, a card's bar without Previous and Next, the bar's count, a game's way back past its own
# step, the tick's faint check and its phone target, and a card's step named a concept card (G1, G6, G7, D5)
run_bg "a module without its Check step" G7 "sed -i '/^  - id: check$/,/^    look: The answers you missed/d' content/pm/see-the-system.md"
run_bg "the Do's step silent on what can come later" G7 "sed -i 's/ Asking whoever tracks delivery can come later\.//' content/pm/find-the-constraint.md"
run_bg "the Do's step promising later asks the Do never makes" G7 "sed -i 's/^    where: The Do, on this page, below\.$/    where: The Do, on this page, below. The conversations can come later./' content/pm/see-the-system.md"
run_bg "the bar's count with a wrong ordinal" G1 "sed -i 's/\"3\" \"rd\"/\"3\" \"th\"/' layouts/partials/pm/course-bar.html"
run_bg "a card's bar with Previous and Next again" G1 "sed -i '/^{{- if not \$isPage }}{{ \$i = -1 }}{{ end -}}$/d' layouts/partials/pm/course-bar.html"
run_bg "Continue lands on the module's top" G1 "sed -i 's/ + (step ? \"#step-\" + step : \"\")//' assets/js/pm.js"
run_bg "a game's way back stays on its own step" G7 "sed -i 's/^  function onward() {$/  function onward() { return;/' assets/js/pm.js"
run_bg "a step's number stays on hover" G7 "sed -i '/^.tick:hover input:not(:checked) + .tick-mark .tick-num/d' assets/css/pm.css"
run_bg "the hover check snaps in" G7 "sed -i 's/tick-num { transition: opacity 180ms ease-out; }/tick-num { transition: none; }/' assets/css/pm.css"
run_bg "the hover check eases for a reader who asks for less motion" D5 "sed -i 's/, .tick-check, .tick-num { transition: none !important; }/ { transition: none; }/' assets/css/pm.css"
run_bg "a step's tick under 44 pixels on a phone" G7 "sed -i '/^@media (max-width: 45.99rem) { .tick input { inset:/d' assets/css/pm.css"
run_bg "the Do's and the Check's steps print" G7 "sed -i '/^  .step-down { display: none !important; }$/d' assets/css/pm.css"
run_bg "a card's step says only One page" G6 "sed -i 's/A concept card, one page\./One page./' layouts/partials/pm/unit-module.html"
# J8, playing a game (26 November 2026)
run_bg "the dice game's takeaway after its first run" J8 "sed -i 's/holdTakeaway(game, seen\[keys\[keys.length - 1\]\] || runs >= 3);/holdTakeaway(game, true);/' assets/js/pm.js"
run_bg "the dice game with no Next under its result" J8 "sed -i '/if (nk) el.next.textContent = \"Next: \" + (i + 2) + \". \" + setups\[nk\].label;/d' assets/js/pm.js"
run_bg "a dice run that leaves the board off the screen" J8 "sed -i 's/el.move.hidden = true; busy(true); toBoard(game);/el.move.hidden = true; busy(true);/' assets/js/pm.js"
run_bg "the waiting game's plans before the reader's own call" J8 "sed -i 's/<div class=\"setups plans\" data-plans hidden>/<div class=\"setups plans\" data-plans>/' layouts/partials/pm/waitinggame.html"
run_bg "the waiting game's pause without its question" J8 "sed -i 's/ showState(); askNext(); return false; }/ showState(); return false; }/' assets/js/pm.js"
run_bg "the ranking game's trial with no end" J8 "sed -i 's/if (current === \"trial\") return week >= W ? \"Play the trial again\" : \"Play week \" + (week + 1) + \" of \" + W;/if (current === \"trial\") return \"Play a week\";/' assets/js/pm.js"
run_bg "a guess's options under 44 pixels on a phone" J8 "sed -i '/^  .guess label { display: flex; align-items: center; min-height: 2.75rem; padding: 0; }$/d' assets/css/pm.css"
# G6, the glossary found by name, and Used in landing on the term (26 November 2026)
run_bg "Used in lands on the unit's top" G6 "sed -i 's/{{ \$u.p.RelPermalink }}#use-{{ \$key }}/{{ \$u.p.RelPermalink }}/' layouts/partials/pm/gloss-entry.html"
run_bg "no address on a term's first use" G6 "sed -i '/if in \$h \$at/d' layouts/partials/pm/mark-uses.html"
run_bg "an empty letter linked on the A to Z rail" G6 "sed -i 's/{{ if .keys }}<a href=\"#l-/{{ if true }}<a href=\"#l-/' layouts/partials/pm/unit-glossary.html"
run_bg "the rail marking no letter as the list scrolls" G6 "sed -i 's/m\[0\].classList.toggle(\"is-here\", m\[0\] === cur);/m[0].classList.toggle(\"is-here\", false);/' assets/js/pm.js"
# G8, names that link (26 November 2026): the first mention in each part links its unit, once; questions for recall
# link nothing; no unit links itself; the single document lands every link, and each module's Do and Check, in the page
run_bg "a name in Where to go from here left unlinked" G8 "sed -i 's|{{< pm/mod see-the-system >}} drew it|{{< pm/mod see-the-system words >}} drew it|' content/pm/the-compass.md"
run_bg "a name linked again in the same part" G8 "sed -i 's|Here two questions collide\\. {{< pm/mod know-who-its-for words >}} says|Here two questions collide. {{< pm/mod know-who-its-for >}} says|' content/pm/the-compass.md"
run_bg "a Check question that links where to look" G8 "sed -i 's|^  - q: \\\"{{< pm/mod decide-and-set-direction words >}} asks you to decide on purpose|  - q: \\\"Remember how {{< pm/mod decide-and-set-direction >}} asks you to decide on purpose|' content/pm/notice-when-you-are-wrong.md"
run_bg "Last time's line links the module before" G8 "sed -i 's|Two questions on {{ with \$prev }}<span class=\"mod-name\">|Two questions on {{ with \$prev }}<a href=\"/pm/{{ .page }}/\">link</a> <span class=\"mod-name\">|' layouts/partials/pm/unit-module.html"
run_bg "a module that links its own name" G8 "printf '\\nThat is the question [Find the Constraint](/pm/find-the-constraint/) asks.\\n' >> content/pm/find-the-constraint.md"
run_bg "the single document links a unit's page" G8 "sed -i '/^{{- range \$to }}/d' layouts/pm/all.html"
run_bg "the single document's Do step lands on the first module's Do" G8 "sed -i 's/#{{ if \$all }}{{ \$key }}-{{ end }}{{ .kind }}/#{{ .kind }}/' layouts/partials/pm/unit-module.html"
# Job 44, two cards and what the course leaves out (26 November 2026): The Compass names what the course leaves out,
# each with a free place to start, linked, and Start's line for it says where to go from here (S21); the model card is on the AI thread (S22)
run_bg "The Compass without what the course leaves out" S21 "sed -i '/^### What the course leaves out/d' content/pm/the-compass.md"
run_bg "a left-out area with no free place linked" S21 "sed -i 's|\[the W3C.s introduction to web accessibility\](https://www.w3.org/WAI/fundamentals/accessibility-intro/)|the W3C introduction|' content/pm/the-compass.md"
run_bg "The Compass leaving regulation unnamed" S21 "sed -i 's|^- \*\*Regulation:\*\* for privacy|- **Rules:** for privacy|; s|UK law, though|UK rules, though|; s|the UK regulator.s guide|the UK watchdog guide|; s|ask your own lawyers early|ask early|' content/pm/the-compass.md"
run_bg "Start's line for The Compass not saying where to go from here" S21 "sed -i 's/, and where to go from here\\./\\./' data/pm/arc.yaml"
# Start's pointer to what the course leaves out, cut in the owner's pass and back the same day, after all four blind
# readers asked for it (27 November 2026)
run_bg "Start not pointing to what the course leaves out" S21 "sed -i 's|(/pm/the-compass/#what-the-course-leaves-out)|(/pm/the-compass/)|' content/pm/_index.md"
run_bg "the single document leaving Start's pointer on The Compass's page" G8 "sed -i '/(printf \"href=\\\\\"%s#\" .RelPermalink)/d' layouts/pm/all.html"
run_bg "the model card off the AI thread" S22 "sed -i 's|So before you trust one, read its mistakes|So read its mistakes before you rely on it|' content/pm/cards/read-the-errors.md"
run_bg "The Compass two pages over its three" P1 "python3 -c \"p='content/pm/the-compass.md'; open(p, 'a').write(('\\n\\n' + 'A sentence that runs the page long. ' * 40) * 12)\""
run_bg "a full path without If you read one" S23 "sed -i '/^deeper_one:/,/^  why:/d' content/pm/mind-the-seams.md"
run_bg "If you read one naming the story" S23 "sed -i '/^deeper_one:/{n;s/title: .*/title: \"The Goal\"/}' content/pm/find-the-constraint.md"
run_bg "a story's credit without its years" S10 "sed -i 's/(NBC, 2016 to 2020)/(NBC)/' content/pm/answer-for-what-you-build.md"
# Both ways with engineering (J9): the old heading, a list with nothing to bring, an engineer's ask inside the minutes,
# a rollout prescribed rather than proposed, and a Do that no longer takes part
run_bg "a list for engineers under its old heading" J9 "sed -i 's/^## To bring to engineers$/## Questions to bring to engineers/' content/pm/design-for-change.md"
run_bg "a list for engineers with nothing to bring" J9 "sed -i '/^Bring your access patterns:/,+1d' content/pm/map-the-domain.md"
run_bg "the engineer's ask moved inside the minutes" J9 "python3 -c \"p='content/pm/know-who-its-for.md'; s=open(p).read(); s=s.replace(' Then give the engineers who', ' Give the engineers who', 1); s=s.replace('Outside the 30 minutes, talk to two people', 'Talk to two people', 1); open(p, 'w').write(s)\""
run_bg "a rollout prescribed, not proposed" J9 "sed -i 's/show it to your tech lead and whoever leads on call, and ask/ask whoever.s on call/' content/pm/change-safely.md"
run_bg "the advice exercise gone back to a look back" J9 "sed -i 's/Find a decision your engineers are still making/Pick a decision from last quarter that stalled/' content/pm/decide-and-set-direction.md"
wait

# F1, F2: the pictures' one grammar (27 November 2026)
run_bg "a picture's yellow as a disc, not a rectangle behind the thing" F1 "sed -i 's|<rect class=\"fig-mark\"[^/]*/>|<circle class=\"fig-mark\" cx=\"178\" cy=\"18\" r=\"12\"/>|' assets/figures/mission-excuse.svg"
run_bg "a picture with two unlike yellow moments" F1 "sed -i 's|<rect class=\"fig-pipe\" x=\"12\" y=\"42\" width=\"154\" height=\"46\" rx=\"6\"/>|<rect class=\"fig-mark\" x=\"12\" y=\"42\" width=\"154\" height=\"46\"/>|' assets/figures/coupling.svg"
run_bg "a picture flooded with yellow" F1 "sed -i 's|<rect class=\"fig-mark\"[^/]*/>|<rect class=\"fig-mark\" x=\"180\" y=\"30\" width=\"166\" height=\"74\"/>|' assets/figures/riskiest-assumption.svg"
run_bg "a picture with no key moment" F1 "sed -i '/class=\"fig-mark\"/d' assets/figures/stocks-flows.svg"
run_bg "an arrowhead of its own size" F1 "sed -i 's|M293,101 L302,106 L293,111 Z|M291,99 L303,106 L291,113 Z|' assets/figures/many-hands.svg"
run_bg "a dot off the dot scale" F1 "sed -i 's|<circle cx=\"312\" cy=\"106\" r=\"5.5\"/>|<circle cx=\"312\" cy=\"106\" r=\"9\"/>|' assets/figures/many-hands.svg"
run_bg "a box with corners of its own" F1 "sed -i '0,/rx=\"6\"/s//rx=\"10\"/' assets/figures/api-promise.svg"
run_bg "a picture that sets its own line weight" F1 "sed -i 's|<path class=\"fig-line\" d=\"M28,75 L150,75\"/>|<path class=\"fig-line\" stroke-width=\"7\" d=\"M28,75 L150,75\"/>|' assets/figures/coupling.svg"
run_bg "a mark the grammar doesn't name" F1 "sed -i 's|<text class=\"fig-note\" x=\"12\" y=\"214\">|<text class=\"fig-shout\" x=\"12\" y=\"214\">|' assets/figures/many-hands.svg"
run_bg "the weight ramp borrowed by another picture" F1 "sed -i 's|<path class=\"fig-line\" d=\"M178,36 L178,144\"/>|<path class=\"fig-line fig-ramp-5\" d=\"M178,36 L178,144\"/>|' assets/figures/mission-excuse.svg"
run_bg "three highlights that aren't all behind words" F1 "sed -i '0,/<rect class=\"fig-mark\" x=\"\([0-9.]*\)\" y=\"80\" width=\"\([0-9.]*\)\" height=\"18\"\/>/s//<rect class=\"fig-mark\" x=\"\\1\" y=\"74\" width=\"\\2\" height=\"30\"\/>/' assets/figures/last-time.svg"
run_bg "picture labels back under 12 pixels on a phone" F2 "sed -i 's/.fig-note { font-weight: 400; font-size: 12.5px;/.fig-note { font-weight: 400; font-size: 11px;/' assets/css/pm.css"
run_bg "a picture held inside the panel's padding, short of its sides" F2 "sed -i 's/^.fig { display: block; width: 100%; max-width: none;/.fig { display: block; width: 88%; max-width: 30rem;/' assets/css/pm.css"
run_bg "a caption that starts off the picture's left edge" F2 "sed -i 's|padding: 0 calc(100% / 30); font:|padding: 0 var(--sp-5); font:|' assets/css/pm.css"
run_bg "two labels on top of each other in a picture" F2 "sed -i 's|<text class=\"fig-note\" x=\"12\" y=\"33\">only the catalog changes</text>|<text class=\"fig-note\" x=\"12\" y=\"22\">only the catalog changes</text>|' assets/figures/coupling.svg"
run_bg "a label running out of its picture" F2 "sed -i 's|<text class=\"fig-label\" x=\"312\" y=\"132\" text-anchor=\"middle\">A customer</text>|<text class=\"fig-label\" x=\"340\" y=\"132\" text-anchor=\"middle\">A customer</text>|' assets/figures/many-hands.svg"
run_bg "words on a picture's yellow in the page's ink" F2 "sed -i 's|<text class=\"fig-label fig-on-mark\" x=\"178\" y=\"22\" text-anchor=\"middle\">Your line</text>|<text class=\"fig-label\" x=\"178\" y=\"22\" text-anchor=\"middle\">Your line</text>|' assets/figures/mission-excuse.svg"
run_bg "words on a picture's yellow unreadable on a dark screen" F2 "sed -i 's/^.fig .fig-on-mark { fill: var(--mark-ink); }/.fig .fig-on-mark { fill: var(--ink); }/' assets/css/pm.css"
run_bg "a picture color with no job named for dark screens" C7 "sed -i 's/ --fig-loss: #8a5340; }/ }/' assets/css/pm.css"
run_bg "Conway's sentence dropped from his card" S16 "sed -i '/^> /d; /^>\$/d' content/pm/cards/conways-law.md"
run_bg "a card's quoted sentence left uncredited" S16 "sed -i '/^> Melvin Conway, /d' content/pm/cards/conways-law.md"
run_bg "a card's quoted sentence reworded" S16 "sed -i 's/are constrained to produce designs which are copies/tend to produce designs which are copies/' content/pm/cards/conways-law.md"
wait
# Joe's pass on Start, the pilot of his holistic pass (27 November 2026): the address kept from harvesters (S19); the
# list's codes and its progress right after a title (S20); a module's code before its name in running text (G8);
# and his notes beside one bullet and one opening paragraph (M4)
run_bg "the footer's address back as plain text" S19 "sed -i 's|{{ if hasPrefix .url \"mailto:\" }}{{ partial \"email.html\" \"href\" }}{{ else }}href=\"{{ .url }}\"{{ end }}|href=\"{{ .url }}\"|' layouts/partials/footer.html"
run_bg "Start's address without its hidden decoy" S19 "sed -i 's|<span hidden>not.</span>||' layouts/partials/email.html"
run_bg "Start's address written out as a plain link" S19 "sed -i 's|{{< pm/email >}}|[mail@joestanley.org](mailto:mail@joestanley.org)|' content/pm/_index.md"
run_bg "Ready back on every module" S20 "sed -i 's|{{ if not \$page }}Not built yet{{ end }}</p>|{{ if not \$page }}Not built yet{{ else }}Ready{{ end }}</p>|' layouts/partials/pm/arc-list.html"
run_bg "Start's markers back to bare numbers" S20 "sed -i 's|aria-hidden=\"true\">M{{ \$m.num }}</span>|aria-hidden=\"true\">{{ \$m.num }}</span>|' layouts/partials/pm/arc-list.html"
run_bg "progress pushed to the far end of the title's line" S20 "echo '.mod-body { justify-content: space-between; }' >> assets/css/pm.css"
run_bg "progress shown under the question" S20 "echo '.mod-status { order: 3; }' >> assets/css/pm.css"
run_bg "an unstarted module says Not started" S20 "sed -i 's|else out.textContent = n === 0 ? \"\" :|else out.textContent = n === 0 ? \"Not started\" :|' assets/js/pm.js"
run_bg "a module's code at the reading size" S20 "echo '.mod-num { font-size: 1.5rem; white-space: normal; }' >> assets/css/pm.css"
run_bg "the question narrowed beside its progress" S20 "echo '.mod-question { flex-basis: 70%; }' >> assets/css/pm.css"
run_bg "Start's progress printing" S20 "echo '@media print { .mod-status { display: block !important; } }' >> assets/css/pm.css"
run_bg "a list of modules with no name" S20 "sed -i 's| aria-labelledby=\"arc-{{ \$where }}-{{ \$i }}\"||' layouts/partials/pm/arc-list.html"
run_bg "a module named on Start without its code" G8 "sed -i 's|{{< pm/mod \"know-who-its-for\" >}}|[Know Who It\x27s For](/pm/know-who-its-for/)|' content/pm/_index.md"
run_bg "a module's code not read out as Module" G8 "sed -i 's|<span class=\"sr\">Module %v</span>||; s|\$m.num \$m.num (\$m.title|\$m.num (\$m.title|' layouts/shortcodes/pm/mod.html"
run_bg "a note beside a bullet Start no longer has" M4 "sed -i 's|beside: \"Thirteen modules, each built on one question\"|beside: \"Fourteen modules, each built on one question\"|' data/pm/margin/start.yaml"
run_bg "a note beside an opening paragraph Start no longer has" M4 "sed -i 's|beside: \"Instead, it.s a set of lessons\"|beside: \"Instead, it is a set of lectures\"|' data/pm/margin/start.yaml"
# Notes where there's no margin (27 November 2026): the owner's hand, his word run in and muted, tied to their paragraph (M1)
run_bg "a note folded in on a phone in the interface's face" M1 "echo '@media screen and (max-width: 63.99rem) { .note { font-family: var(--ui) !important; } }' >> assets/css/base.css"
run_bg "a folded note's word back on its own line" M1 "echo '.note-label { display: block; float: none; }' >> assets/css/base.css"
run_bg "a folded note's word in the label type, bold" M1 "sed -i 's/^.note-label { float: left; margin-right: 0.3em; font: inherit; color: var(--muted); }/.note-label { float: left; margin-right: 0.3em; font: var(--w-strong) var(--fs-small)\\/var(--lh-text) var(--ui); color: var(--ink); }/' assets/css/base.css"
run_bg "a folded note nearer the next paragraph than its own" M1 "sed -i 's/^  .note { margin: var(--sp-2) 0 var(--sp-5); }/  .note { margin: var(--sp-5) 0 var(--sp-1); }/; s/^  .noted > p:not(:last-child) { margin-bottom: var(--sp-2); }//' assets/css/base.css"
# Job 52, a module's code before its name everywhere (27 November 2026): linked or not, in every unit (G8)
run_bg "a module named in a module's text without its code" G8 "sed -i 's|{{< pm/mod see-the-system >}}|[See the System](/pm/see-the-system/)|' content/pm/find-the-constraint.md"
run_bg "a recall question naming a module without its code" G8 "sed -i 's|{{< pm/mod see-the-system words >}}|See the System|' content/pm/find-the-constraint.md"
run_bg "Last time's line naming the module before without its code" G8 "sed -i 's|<span class=\"mod-name\"><span aria-hidden=\"true\">M{{ .num }}</span><span class=\"sr\">Module {{ .num }}</span>: {{ .title }}</span>|{{ .title }}|' layouts/partials/pm/unit-module.html"
run_bg "a walk's module names lost when its words are rendered" G8 "sed -i '/MODNAMEHELD%dX\" \$i) \$h 1 }}{{ end }}/d' layouts/shortcodes/pm/walk.html"
run_bg "a voice slot's interim words naming a module without its code" G8 "sed -i 's|in M10: Answer for What You Build\\.|in Answer for What You Build.|' data/pm/voice-slots.yaml"
run_bg "a module's code that isn't its own" G8 "sed -i 's|<span aria-hidden=\"true\">M%v</span>|<span aria-hidden=\"true\">M1%v</span>|' layouts/shortcodes/pm/mod.html"
# The front door's icons turn into the companies' own marks on hover and focus (N5, the owner, 27 November 2026)
run_bg "LinkedIn's mark in a lookalike blue" N5 "sed -i 's/#0a66c2/#0077b5/' layouts/partials/icon.html"
run_bg "the companies' marks never shown on hover" N5 "sed -i '/^.door-links a:hover .icon-mark/d' assets/css/base.css"
run_bg "Bluesky's mark read aloud" N5 "sed -i 's/<svg class=\"icon-mark\" aria-hidden=\"true\" focusable=\"false\" xmlns=\"http:\/\/www.w3.org\/2000\/svg\" viewBox=\"0 0 320 286\">/<svg class=\"icon-mark\" focusable=\"false\" xmlns=\"http:\/\/www.w3.org\/2000\/svg\" viewBox=\"0 0 320 286\">/' layouts/partials/icon.html"
# The ReadMe's record: each place a heading, its time in a rail at the left, level with it (R11, the owner, 27 November 2026)
run_bg "the ReadMe without its rail" R11 "sed -i '/^class: cv$/d' content/page/readme.md"
run_bg "a ReadMe time run into its text" R11 "python3 -c \"p='content/page/readme.md'; s=open(p).read(); open(p, 'w').write(s.replace('2023+\\n\\nConfidential', '2023+\\nConfidential'))\""
run_bg "the ReadMe's times off their places' baselines" R11 "echo '.cv .prose h3 + p { padding-top: 0.6rem !important; }' >> assets/css/base.css"
wait
# The owner's pass on Own Your Role (28 November 2026): the em dashes he typed are kept and listed, and no other (T3);
# a note for one answer of the Check shows only with its answer (M4); a header's time is a sentence (S14); the front
# door's marks fade in and out (N5); "On this page" sits in the header, and in the margin level with the module's number (G7)
run_bg "an em dash nobody listed" T3 "printf '\\nA plain \\xe2\\x80\\x94 dash.\\n' >> content/pm/see-the-system.md"
run_bg "a kept em dash whose sentence has gone" T3 "sed -i 's/One heads up \\xe2\\x80\\x94 \\[/One heads up: [/' data/pm/margin/start.yaml"
run_bg "an answer's note shown before its answer" M4 "sed -i 's/<div class=\"answer noted\" data-beside=\"{{ .slot }}\"><p>{{ .a | .p.RenderString }}<\\/p>\\(<aside.*<\\/aside>\\)<\\/div>/\\1<div class=\"answer\">{{ .a | .p.RenderString }}<\\/div>/' layouts/partials/pm/recall.html"
run_bg "a header's time as a fragment again" S14 "sed -i 's/Takes about {{ partial \"pm\\/duration.html\" (add/About {{ partial \"pm\\/duration.html\" (add/' layouts/partials/pm/unit-module.html"
run_bg "the companies' marks swapped at once, with no fade" N5 "sed -i '/^.door-links .icon-line, .door-links .icon-mark { transition/d' assets/css/base.css"
run_bg "On this page back under the header" G7 "sed -i 's/<nav class=\"on-page screen-only\" aria-label=\"On this page\">/<\\/div><\\/div><div><div><nav class=\"on-page screen-only\" aria-label=\"On this page\">/' layouts/partials/pm/unit-module.html"
run_bg "On this page lower than the module's number" G7 "sed -i 's/  .unit-head .on-page { position: absolute; top: 0; right: 0;/  .unit-head .on-page { position: absolute; top: 3rem; right: 0;/' assets/css/pm.css"
wait
