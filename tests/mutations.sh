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
run_bg "a menu label too long for a phone" R9 "sed -i 's/      name: Product Judgment/      name: Product Judgment Syllabus/' hugo.yaml"
run_bg "header that cannot wrap" R7 "echo '.site-nav { flex-wrap: nowrap; white-space: nowrap; }' >> assets/css/base.css"
run_bg "a line box that clips its text" A13 "echo '.meta-line { max-height: 1.5em; overflow: hidden; }' >> assets/css/pm.css"
run_bg "a stray gap in Firefox only" T8 "echo '@supports (-moz-appearance: none) { .hint { margin-bottom: 0.7rem; } }' >> assets/css/pm.css"

run_bg "source reasons open, not folded" S4 "sed -i 's/<details class=\"why\">/<div class=\"why\">/; s/<\/details>/<\/div>/' layouts/partials/pm/source-notes.html"
run_bg "glossary links leave the PDF for the site" P5 "sed -i 's/^{{ replace (string .).*/{{ . }}/' layouts/pm/all.html"
run_bg "PDF opens without its bookmarks" P6 "sed -i '/root.PageMode = /d' tools-pm/make-pdf.py"
run_bg "glossary definition back in the margin" M1 "sed -i 's|^{{- /\*\*/ -}}|<span class=\"note\" aria-hidden=\"true\">{{ \$g.text }}</span>|' layouts/shortcodes/pm/term.html"
run_bg "notes hidden from screen readers" M3 "sed -i 's/<aside class=\"note\"/<aside aria-hidden=\"true\" class=\"note\"/' layouts/partials/pm/margin.html"
run_bg "a slot file that lost a part" M4 "sed -i '/^step-forte:/d' data/pm/margin/find-the-constraint.yaml"
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
run_bg "a retired setting back in an example" S5 "sed -i 's/a tweak to checkout/a change to a contact frequency rule/' content/pm/find-the-constraint.md"
run_bg "a source linked from Substack" S9 "printf '\n- [A newsletter post](https://example.substack.com/p/a-post), 5 minutes.\n' >> content/pm/notice-when-you-are-wrong.md"
run_bg "two stories on one full path" S10 "python3 -c \"p='content/pm/see-the-system.md'; s=open(p).read(); e='  - title: A Film About Change\n    by: Someone\n    where: A film.\n    only: The lesson again, on screen.\n'; open(p, 'w').write(s.replace('deeper:\n', 'deeper:\n' + e, 1))\""
run_bg "a full path with no story" S10 "sed -i '/^  - title: Ocean.s Eleven\$/,/^    only: /d' content/pm/decide-and-set-direction.md"
run_bg "a story asked to be trusted as evidence" S10 "sed -i 's/^    only: Goldratt first/    trust: It sold millions of copies.\n    only: Goldratt first/' content/pm/find-the-constraint.md"
run_bg "a sixth thing on a built full path" S11 "python3 -c \"p='content/pm/see-the-system.md'; s=open(p).read(); e='  - title: Another Book\n    by: Someone\n    where: A book.\n    trust: Peer-reviewed.\n    only: More of the same.\n'; open(p, 'w').write(s.replace('deeper:\n', 'deeper:\n' + e * 5, 1))\""
run_bg "a pair counted as one thing on a built full path" S11 "python3 -c \"p='content/pm/see-the-system.md'; s=open(p).read(); e='  - title: Another Book\n    by: Someone\n    where: A book.\n    trust: Peer-reviewed.\n    only: More of the same.\n'; pr='  - title: Two Shows\n    by: Someone\n    where: A pair of TV series, watched side by side.\n    only: A contrast.\n'; open(p, 'w').write(s.replace('deeper:\n', 'deeper:\n' + pr + e * 2, 1))\""
run_bg "a short article on a built full path" S12 "python3 -c \"p='content/pm/see-the-system.md'; s=open(p).read(); e='  - title: A Short Post\n    by: Someone\n    where: A blog post, about 5 minutes.\n    trust: A practitioner.\n    only: A summary.\n'; open(p, 'w').write(s.replace('deeper:\n', 'deeper:\n' + e, 1))\""
run_bg "Find the Constraint back to one book beside its story" S12 "sed -i '/^  - title: \\\"Accelerate/,/^    only: \\\"Goodhart/d' content/pm/find-the-constraint.md"
run_bg "an unchecked source on a built page" S7 "printf '\n*To check: nobody has opened this source yet.*\n' >> content/pm/see-the-system.md"
run_bg "a module that stops talking to the reader" E1 "sed -i 's/The danger while you work on it is/The danger in working on it is/; s/Before you trust a stand-in, ask/Before trusting a stand-in, ask/; s/a stock like the one you drew in See the System/a stock like the one drawn in See the System/' content/pm/find-the-constraint.md"
run_bg "a module with its contractions spelled out" E2 "sed -i 's/\([Dd]\)on\x27t/\1o not/g; s/isn\x27t/is not/g; s/\([Ii]\)t\x27s/\1t is/g; s/doesn\x27t/does not/g; s/didn\x27t/did not/g; s/won\x27t/will not/g; s/can\x27t/cannot/g; s/you\x27re/you are/g; s/there\x27s/there is/g' content/pm/find-the-constraint.md content/pm/cards/five-focusing-steps.md content/pm/cards/goodharts-law.md layouts/partials/pm/dicegame.html data/pm/dicegame.yaml"
run_bg "an experience invented for the owner" E3 "printf '\nI learned this the hard way on my second team.\n' >> content/pm/see-the-system.md"
run_bg "a module with no source" X1 "sed -i '/^  page: decide-and-set-direction$/d' data/pm/modules.yaml"
run_bg "a draft left behind after its module is built" X1 "mkdir -p drafts/pm; cp content/pm/see-the-system.md drafts/pm/see-the-system.md; sed -i 's/^  page: see-the-system$/  page: see-the-system\n  draft: see-the-system\n  state: Left behind./' data/pm/modules.yaml"
run_bg "the tab drops what to look for" X2 "sed -i 's/paras += look(b) + reasons(b) + note_of(li)/paras += reasons(b) + note_of(li)/' tools-pm/source-doc.py"
run_bg "a word changed without reaching the working doc" X3 "sed -i 's/Nothing is sent anywhere./Nothing leaves your browser./' content/pm/_index.md"
# X4: a voice slot on Start, placed as a paragraph of its own, added first in the list whatever slots are open. The
# mutations below each place it, then break one thing.
SLOT="sed -i 's/^slots:.*$/slots:\\n  - id: t\\n    unit: Start\\n    brief: Say what judgment is, in your own words.\\n    interim: Judgment is what you bring when the map runs out./' data/pm/voice-slots.yaml; printf '\\n{{< pm/voice \\\"t\\\" \\\"paragraph\\\" >}}\\n' >> content/pm/_index.md"
run_bg "a voice slot listed and placed nowhere" X4 "sed -i 's/^slots:.*$/slots:\\n  - id: t\\n    unit: Start\\n    brief: Say what judgment is.\\n    interim: For now./' data/pm/voice-slots.yaml"
run_bg "an open voice slot on its way to joestanley.org" X4 "$SLOT; sed -i 's/LIVE = \\[\\]  /LIVE = [True]/' tests/check_site.py"
run_bg "a voice slot's brief shown on the page" X4 "$SLOT; sed -i 's/{{ with \\\$s.interim }}/{{ \\\$s.brief }} {{ with \\\$s.interim }}/' layouts/shortcodes/pm/voice.html"
run_bg "the tab drops a voice slot's block" X4 "$SLOT; sed -i 's/    out = \\[slot_block(sid) for sid in PENDING\\]/    out = []/' tools-pm/source-doc.py"
run_bg "a voice slot as a paragraph, placed without saying so" X4 "$SLOT; sed -i 's/ \\\"paragraph\\\" >}}/ >}}/' content/pm/_index.md"
run_bg "a word of the owner's moved and not listed for his pass" X4 "sed -i 's/^  - what: moved$/  - what: shifted/' data/pm/voice-slots.yaml"
run_bg "link easing ignores reduced motion" D5 "sed -i '/@media (prefers-reduced-motion: reduce) { a, .recall/d' assets/css/base.css"
wait

# Joe's editing pass of 21 November 2026: his own sentences, simpler source entries, rounded times, notes beside a paragraph
run_bg "the owner's own sentence reworded" E3 "sed -i \"s/I'm not exaggerating when I tell you/I'm not joking when I say/\" content/pm/own-your-role.md"
run_bg "borrow or buy back on a built full path" S13 "sed -i 's/^    where: A book\.$/    where: A book. Borrow it or buy it./' content/pm/see-the-system.md"
run_bg "a page count on a built full path" S13 "sed -i 's/^    where: A book\.$/    where: A book of about 240 pages./' content/pm/see-the-system.md"
run_bg "a full-path entry that hides its kind" S12 "sed -i 's/^    where: A journal article\.$/    where: Free online./' content/pm/own-your-role.md"
run_bg "a step's time off the owner's marks" S14 "sed -i 's/^    minutes: 15$/    minutes: 13/' content/pm/find-the-constraint.md"
run_bg "the header split into reading and doing again" S14 "sed -i 's|About {{ partial \"pm/duration.html\" (add \$readMin \$doMin) }}.|About {{ add \$readMin \$doMin }} minutes: {{ \$readMin }} reading, {{ \$doMin }} doing.|' layouts/partials/pm/unit-module.html"
run_bg "a note naming words its paragraph lost" M4 "sed -i 's/beside: \"Two versions of the job look real\"/beside: \"Three versions of the job\"/' data/pm/margin/own-your-role.yaml"
run_bg "a paragraph's note put before it" M3 "sed -i 's|(printf \`<div class=\"noted\" data-beside=\"%s\">%s%s</div>\` \$id . \$aside)|(printf \`<div class=\"noted\" data-beside=\"%s\">%s%s</div>\` \$id \$aside .)|' layouts/partials/pm/prose-slots.html"
run_bg "a paragraph's note left floating below it" M1 "sed -i '/\.reading \.noted > \.note { position: absolute/d' assets/css/base.css"
wait
run_bg "a module that pushes its full path past its three pages" P1 "python3 -c \"p='content/pm/own-your-role.md'; s=open(p).read(); open(p, 'w').write(s.replace('And if you work together', 'A sentence that runs on to fill the page. ' * 160 + '\\n\\nAnd if you work together', 1))\""
run_bg "a module whose own text runs a second page over, past its grace until launch" P1 "python3 -c \"p='content/pm/find-the-constraint.md'; s=open(p).read(); open(p, 'w').write(s.replace('Before you trust a stand-in', 'A sentence that runs on to fill the page. ' * 90 + 'Before you trust a stand-in', 1))\""
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
run_bg "the full path's label floating over the first source" R10 "sed -i 's/display: block; margin-top: var(--sp-1); text-align: right;/float: right; margin-top: var(--sp-1);/' assets/css/pm.css"
run_bg "a note folded in on a phone without its label" M1 "echo '@media (max-width: 63.99rem) { .note-label { position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%); } }' >> assets/css/base.css"
run_bg "a card's note printed typeset, not in the owner's hand" M1 "sed -i '/^  .note { font-family: \"Shantell Sans\", var(--ui); font-variation-settings: \"INFM\" 100; }$/d' assets/css/pm.css"
run_bg "a note read aloud as a plain note again" M3 "sed -i 's/>Sidenote: </>Note: </g' layouts/partials/pm/margin.html layouts/partials/pm/prose-slots.html"
run_bg "a step's note out of line with the margin" M1 "echo '@media (min-width: 64rem) { .reading .step > .note { margin-left: var(--sp-5) !important; } }' >> assets/css/pm.css"
run_bg "a long note beside the full path's heading pushing the first source down" R10 "sed -i '/^    .deeper-list > li:has(> .note) { clear: none; }$/d' assets/css/pm.css"
run_bg "See the System back to one book beside its story" S12 "sed -i '/^  - title: The Field Guide/,/^    only: Cook.s point/d' content/pm/see-the-system.md"
wait

# Joe's picks of 22 November 2026: the kind as an icon on the full path (S15), Conway's sentence in his card's
# picture slot (S16), the hour in words in a module's header (S14), and a step that reads on in the one before (S2)
run_bg "a film shown with the article icon" S15 "sed -i 's/(?:classic )?(?:film|/(?:classic )?(?:flim|/' layouts/partials/pm/kind-icon.html"
run_bg "the kind's words shown to the eye beside the icon" S15 "sed -i 's/<p class=\"meta-line kind-line sr\">/<p class=\"meta-line kind-line\">/' layouts/partials/pm/unit-module.html"
run_bg "a card's quoted sentence left uncredited" S16 "sed -i '/<figcaption class=\"plate-caption\">{{ .by }}/d' layouts/partials/pm/unit-card.html"
run_bg "the header's hour back in digits" S14 "sed -i 's/{{- else if eq \$h 1 }}an hour/{{- else if eq \$h 1 }}1 hour/' layouts/partials/pm/duration.html"
run_bg "a step that reads on in a step that isn't the one before it" S2 "sed -i 's/    continues: meadows-1/    continues: card-stocks/' content/pm/see-the-system.md"
run_bg "a comma back outside a closing quotation mark" T9 "sed -i 's/\"Leverage Points,\" first half/\"Leverage Points\", first half/' content/pm/see-the-system.md"
run_bg "a period back outside a quoted title in a source's note" T9 "sed -i 's/Backward Design.\\\\\"/Backward Design\\\\\"./' content/pm/own-your-role.md"
run_bg "an em dash in the voice guide, which lives in pm-sources" T3 "mkdir .pm-sources && cp \"\${PM_SOURCES:-\$SRC/../pm-sources}/VOICE.md\" .pm-sources/ && printf '\\nA line \\xe2\\x80\\x94 with an em dash.\\n' >> .pm-sources/VOICE.md"
run_bg "a Check that doesn't end beyond its module" J1 "sed -i 's/\*\*Beyond this module\.\*\* This module helps you choose/This module helps you choose/' content/pm/decide-and-set-direction.md"
run_bg "a collision with no against" J2 "sed -i '/^    against: see-the-system$/d' content/pm/find-the-constraint.md"
run_bg "a collision set against a later module" J2 "sed -i 's/^    against: own-your-role$/    against: weigh-the-evidence/' content/pm/mind-the-seams.md"
run_bg "the log's review under the wrong label" J3 "sed -i 's/^\*\*Review your decision log\.\*\*/**For your decision log.**/' content/pm/notice-when-you-are-wrong.md"
run_bg "the decision log's line after the optional exercise" J3 "python3 -c 'p=\"content/pm/find-the-constraint.md\"; s=open(p).read(); l=[x for x in s.split(chr(10)) if x.startswith(\"**For your decision log.**\")][0]; s=s.replace(l+chr(10)+chr(10), \"\", 1).rstrip()+chr(10)+chr(10)+l+chr(10); open(p, \"w\").write(s)'"
run_bg "a module that names no earlier one" J4 "sed -i 's/ The longest wait you mapped in Find the Constraint may well sit at one of them\.//' content/pm/mind-the-seams.md"
run_bg "a game that doesn't say what it leaves out" J5 "sed -i '/<p class=\"limits\">/d' layouts/partials/pm/rankinggame.html"
run_bg "a total the waiting game's jobs don't give" J5 "sed -i 's/^    total: 493000$/    total: 439000/' data/pm/waitgame.yaml"
run_bg "the waiting game off the short path" J5 "sed -i '/^  - id: waiting$/,/^    look: What each week of waiting costs/d' content/pm/know-who-its-for.md"
run_bg "the waiting game's result a week off its board" A8 "sed -i 's/ in week \") + p\[id\]\.live; });/ in week \") + (p[id].live + 1); });/' assets/js/pm.js"
run_bg "the ranking game's board hiding the small stores among the worst" A8 "sed -i 's/dot.classList.toggle(\"is-worst\", has \&\& worst.indexOf(i) >= 0);/dot.classList.toggle(\"is-worst\", has \&\& worst.indexOf(i) >= 0 \&\& group[i] > 0);/' assets/js/pm.js"
run_bg "the waiting game's Play disabled during a run" A9 "sed -i 's/running = true; busyOn(el.play, true);/running = true; el.play.disabled = true;/' assets/js/pm.js"
run_bg "the waiting game's recorded orders hidden without JavaScript" D1 "echo '.game[data-game=waiting] .example { display: none; }' >> assets/css/pm.css"
run_bg "the waiting game animated with reduced motion" D5 "sed -i 's/if (still()) { wk = W; draw(); finish(); return; }//' assets/js/pm.js"
wait
