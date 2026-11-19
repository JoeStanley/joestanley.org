#!/bin/bash
# Proves the suite has teeth: each line breaks a copy of the site one way and confirms the named rule fails.
# Run from the repo root: HUGO=/path/to/hugo bash tests/mutations.sh
set -u
SRC=$(cd "$(dirname "$0")/.." && pwd)
run() {  # description, rule, command that breaks the copy
  D=$(mktemp -d); cp -r "$SRC"/. "$D"/; (cd "$D" && eval "$3")
  (cd "$D" && python3 tests/check_site.py --only "$2" >/dev/null 2>&1)
  if grep -q "| $2 | auto | FAIL" "$D/tests/report.md"; then echo "caught: $1 ($2)"; else echo "MISSED: $1 ($2)"; fi
  rm -rf "$D"
}
# Runs at most $JOBS mutations at once (default 2): each one starts browsers, and too many at once on a small
# machine make checks time out, which reads as a miss.
run_bg() { while [ "$(jobs -rp | wc -l)" -ge "${JOBS:-2}" ]; do sleep 2; done; run "$@" & }
run_bg "orange section heading" W2 "echo 'h2 { color: var(--orange) !important; }' >> assets/css/pm.css"
run_bg "step without a look line" S1 "sed -i '0,/    look: The line finishes/{/    look: The line finishes/d}' content/pm/find-the-constraint.md"
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
run_bg "a stray gap" T8 "echo '.hint { margin-bottom: 0.7rem; }' >> assets/css/pm.css"
run_bg "section heading smaller than a step title" W4 "echo '.card-body h2 { font-size: var(--fs-small); }' >> assets/css/pm.css"
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
run_bg "station numbers pushed low in their discs" R6 "echo '.st-name { padding-top: 2px; }' >> assets/css/pm.css"
run_bg "a module that runs past three pages" P1 "for i in \$(seq 60); do printf 'A filler paragraph that says nothing and only takes up room on the printed page.\n\n' >> content/pm/see-the-system.md; done"
run_bg "the Start page runs onto a second page" P1 "for i in \$(seq 30); do printf '\nA filler paragraph that says nothing and only takes up room on the printed page.\n' >> content/pm/_index.md; done"
run_bg "link easing ignores reduced motion" D5 "sed -i '/@media (prefers-reduced-motion: reduce) { a, .recall/d' assets/css/base.css"
wait
