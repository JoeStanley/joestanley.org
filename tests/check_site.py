#!/usr/bin/env python3
"""Checks joestanley.org against tests/SPEC.md.

Run from the site repo root:
    npm install --prefix tests          # once, for axe-core
    python3 tests/check_site.py         # build, check, report
    python3 tests/check_site.py --update-baseline   # only after the owner approves the look
    python3 tests/check_site.py --live              # before publishing: also fails while a voice slot is open (X4)

Needs Hugo 0.141.0 extended (HUGO env var or on PATH), Python 3 with playwright, pyyaml and Pillow,
Chrome or Playwright's Chromium (CHROME env var to point at one), and pdftotext.
Writes tests/report.md and exits 1 if any rule fails. Each failure names its rule ID from SPEC.md.
"""
import argparse, functools, glob, http.server, io, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading
from collections import defaultdict

import yaml
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS = os.path.join(ROOT, "tests")
# The private JoeStanley/pm-sources, which holds the working record and the voice guide (T3), sits beside this
# repository in every working session. GitHub's checks can't see it, so what lives there is noted, not failed.
PM_SOURCES = os.environ.get("PM_SOURCES") or os.path.normpath(os.path.join(ROOT, "..", "pm-sources"))
# The built modules, each with its concept cards, in reading order. Add a module here when it is built.
MODULES = [("/pm/own-your-role/", ["/pm/cards/concept-champion/"]),
           ("/pm/know-who-its-for/", ["/pm/cards/the-last-time/"]),
           ("/pm/see-the-system/", ["/pm/cards/stocks-flows-feedback/"]),
           ("/pm/find-the-constraint/", ["/pm/cards/five-focusing-steps/", "/pm/cards/goodharts-law/"]),
           ("/pm/mind-the-seams/", ["/pm/cards/conways-law/"]),
           ("/pm/map-the-domain/", ["/pm/cards/access-patterns/", "/pm/cards/api-is-a-promise/"]),
           ("/pm/design-for-change/", ["/pm/cards/coupling/"]),
           ("/pm/change-safely/", ["/pm/cards/error-budgets/", "/pm/cards/read-the-errors/"]),
           ("/pm/weigh-the-evidence/", ["/pm/cards/law-of-small-numbers/", "/pm/cards/riskiest-assumption/"]),
           ("/pm/decide-and-set-direction/", ["/pm/cards/agency-and-coherence/"]),
           ("/pm/answer-for-what-you-build/", ["/pm/cards/many-hands/", "/pm/cards/mission-excuse/"]),
           ("/pm/notice-when-you-are-wrong/", ["/pm/cards/double-loop-learning/"]),
           ("/pm/bring-people-with-you/", ["/pm/cards/trust-equation/"])]
# The closing unit, The Compass (spec S21), after the last module.
CLOSING = "/pm/the-compass/"
UNIT_PAGES = [p for m, cards in MODULES for p in [m] + cards] + [CLOSING]
# What the course leaves out, which The Compass names under its last section with the best free place to start for
# each (S21, the owner, 25 November 2026), and how the check knows each area by name.
LEAVES_OUT_ID = "what-the-course-leaves-out"
LEAVES_OUT = [("discovery method", r"\bdiscovery\b"), ("pricing and go-to-market", r"\bpricing\b.*\bgo-to-market\b"),
              ("experiments", r"\bexperiment"), ("design craft", r"\bdesign\b"), ("accessibility", r"\baccessib"),
              ("regulation", r"\bregulat|\blaw\b")]
# The concept cards' page (G6) lists every card; it's an index, not a unit, so it has no tab, slots or foot.
CARDS_INDEX = "/pm/cards/"
PAGES = ["/", "/page/readme/", "/games/", "/pm/"] + UNIT_PAGES + ["/pm/glossary/", CARDS_INDEX, "/pm/all/"]
WIDTHS = [320, 390, 768, 1024, 1280, 1920]
# P1: the most pages each kind of unit may print on, and what the rebuilt units print on in all.
# PRINT_PAGES is a record kept with the spec: a change in the count is noted in the report, not failed.
UNIT_SHARE = {"start": 2, "module": 3, "card": 1, "closing": 3, "glossary": 3}
DEEPER_PAGES = 2   # the pages a module's full path, answers and sources' reasons may run onto past its three
MODULE_GRACE = 1   # until a PDF is published, a module may run one page past either limit: noted, not failed (the owner, 22 November 2026)
GAME_GRACE = 3   # until a PDF is published, a module with a game (J5) may run its own text onto a fifth page, its full path
                 # starting on the sixth, and print on eight pages in all: noted, not failed (the owner, 22 November 2026)
RUNS_LONG = {"answer-for-what-you-build"}   # runs longer on purpose and says so: six on its full path (S11), and a game's
                                            # allowance in print (P1) (the owner, 23 November 2026)
GLOSSARY_GRACE = None   # until a PDF is published, the glossary may run past its three pages: noted, not failed (the owner, 22 November 2026)
CLOSING_GRACE = 1   # until a PDF is published, The Compass may print on a fourth page: noted, not failed (the owner, 26 November 2026)
PRINT_PAGES = 109   # a record: the check notes a change in the count, and does not fail on it
FAIL = defaultdict(list)     # rule id -> list of messages
NOTE = defaultdict(list)     # rule id -> informational messages
CHECKED = set()


def fail(rule, msg):
    FAIL[rule].append(msg)


def checked(*rules):
    CHECKED.update(rules)


ONLY = set()   # with --only, run just the checks behind these rules (mutations.sh uses this to stay quick)
SKIP = set()   # with --skip, leave these rules out (GitHub's checks skip V1: screenshots depend on the machine)
LIVE = []      # with --live, as publish.yml runs it: an open voice slot fails X4, since nothing waiting reaches the site


def run_for(*rules):
    rs = set(rules) - SKIP
    return bool(rs) and (not ONLY or bool(ONLY & rs))


# ---------- colour helpers ----------
def hex_to_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(rgb):
    def f(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def parse_tokens(css_files):
    """Return {'light': {...}, 'dark': {...}} of custom properties, later files overriding earlier."""
    out = {"light": {}, "dark": {}}
    for path in css_files:
        css = re.sub(r"/\*.*?\*/", "", open(path).read(), flags=re.S)
        # dark blocks: @media ... prefers-color-scheme: dark { :root { ... } }
        for m in re.finditer(r"@media[^{]*prefers-color-scheme:\s*dark[^{]*\{\s*:root\s*\{([^}]*)\}", css):
            for k, v in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", m.group(1)):
                out["dark"][k] = v.strip()
        light_css = re.sub(r"@media[^{]*\{(?:[^{}]*\{[^}]*\})*[^}]*\}", "", css)
        for m in re.finditer(r":root\s*\{([^}]*)\}", light_css):
            for k, v in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", m.group(1)):
                out["light"][k] = v.strip()
    dark = dict(out["light"]); dark.update(out["dark"]); out["dark"] = dark

    def resolve(d, v, depth=0):
        m = re.match(r"var\((--[\w-]+)\)", v)
        return resolve(d, d.get(m.group(1), ""), depth + 1) if m and depth < 8 else v
    return {t: {k: resolve(d, v) for k, v in d.items()} for t, d in out.items()}


# ---------- build ----------
def build(out_dir):
    hugo = os.environ.get("HUGO", "hugo")
    r = subprocess.run([hugo, "--quiet", "-s", ROOT, "-d", out_dir], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout, r.stderr)
        sys.exit("Hugo build failed")


SAMPLE = ["Sample note. Ask where work waits before you read this.",
          "Sample note, longer. When I first read this I skipped the dice game, and the idea did not land until a release was stuck for a month waiting on one sign-off.",
          "Sample note with a **bold** word and [a link](https://example.org).",
          "Sample note. Two or three lines is about right for the margin."]


def build_fixture():
    """A copy of the site with a sample note in every empty margin slot, beside the owner's own notes, so the margin
    rules (M1 to M3, R3) are checked with notes present, his among them. Every full path's heading gets the longest
    sample and a short one, so R10 always meets a note there that runs past the heading and the If you read one line under it
    (S23). Returns the built output directory."""
    tmp = tempfile.mkdtemp(prefix="fixture-")
    src = os.path.join(tmp, "src"); out = os.path.join(tmp, "out")
    shutil.copytree(ROOT, src, ignore=shutil.ignore_patterns(".git", "public", "node_modules", "baseline", "resources", "report.md"))
    for f in glob.glob(os.path.join(src, "data", "pm", "margin", "*.yaml")):
        data = yaml.safe_load(open(f, encoding="utf-8")) or {}
        filled = {k: (v if v else SAMPLE[1] + " " + SAMPLE[3] if k == "go-deeper" else SAMPLE[i % len(SAMPLE)]) for i, k in enumerate(data) for v in [data[k]]}
        open(f, "w", encoding="utf-8").write(yaml.safe_dump(filled, sort_keys=False, allow_unicode=True))
    hugo = os.environ.get("HUGO", "hugo")
    r = subprocess.run([hugo, "--quiet", "-s", src, "-d", out], capture_output=True, text=True)
    if r.returncode != 0:
        fail("M1", f"the sample-note build failed: {(r.stdout + r.stderr).strip()[-200:]}")
        return None
    return out


JS_NOTES = """() => { const col = document.querySelector('.unit-body.reading, .reading'); const cr = col.getBoundingClientRect(); const cs = getComputedStyle(col);
  const right = cr.left + col.clientWidth - parseFloat(cs.paddingRight);
  return [...document.querySelectorAll('.note')].filter(n => n.getClientRects().length).map(n => {
    const r = n.getBoundingClientRect(); const s = getComputedStyle(n);
    const prev = n.previousElementSibling, next = n.nextElementSibling;
    const slot = (prev && prev.matches('[data-slot]')) ? prev : (next && next.matches('[data-slot]')) ? next : n.closest('[data-slot], [data-beside]');
    // A part ends where the next heading of its level starts, or with its container; a heading's part is the text under it.
    let sr = slot ? slot.getBoundingClientRect() : null, partBottom = sr ? sr.bottom : null;
    if (slot && /^H[1-6]$/.test(slot.tagName)) {
      let e = slot.nextElementSibling; while (e && e.tagName !== slot.tagName) e = e.nextElementSibling;
      partBottom = e ? e.getBoundingClientRect().top : slot.parentElement.getBoundingClientRect().bottom;
    }
    const colRight = (n.closest('.reading') || col);
    const cR = colRight.getBoundingClientRect(); const cS = getComputedStyle(colRight);
    return {note: n.dataset.note, slot: slot ? (slot.dataset.slot || slot.dataset.beside) : null, left: r.left, right: r.right, top: r.top, bottom: r.bottom,
            colRight: cR.left + colRight.clientWidth - parseFloat(cS.paddingRight), colLeft: cR.left + parseFloat(cS.paddingLeft),
            slotTop: sr ? sr.top : null, slotBottom: partBottom,
            face: s.fontFamily.split(',')[0].replace(/["']/g, '').trim().toLowerCase(), border: parseFloat(s.borderLeftWidth),
            hidden: !!n.closest('[aria-hidden="true"]'), lead: (n.firstElementChild && n.firstElementChild.matches('.note-label')) ? n.firstElementChild.textContent : '',
            label: (() => { const l = n.firstElementChild; if (!l || !l.matches('.note-label')) return null; const lr = l.getBoundingClientRect(); const ls = getComputedStyle(l);
              const rest = document.createRange(); rest.setStartAfter(l); rest.setEnd(n, n.childNodes.length); const rr = [...rest.getClientRects()].filter(x => x.width && x.height);
              return {shown: lr.width > 2 && lr.height > 2 && ls.clipPath === 'none' && ls.visibility !== 'hidden', own: !rr.length || lr.bottom <= Math.min(...rr.map(x => x.top)) + 1}; })(),
            para: n.parentElement.matches('.noted') && prev && prev.tagName === 'P' ? [prev.getBoundingClientRect().top, prev.getBoundingClientRect().bottom] : null,
            after: prev ? prev.tagName : (n.parentElement.matches('.noted') ? 'NOTED-FIRST' : 'FIRST'), before: (next && next.matches('[data-slot]')) ? 'SLOT' : (!next && n.parentElement.matches('li[data-slot]')) ? 'DESCRIPTION' : (!next && prev && prev.tagName === 'P' && n.parentElement.matches('.noted')) ? 'PARAGRAPH' : '',
            kind: (n.closest('.unit') || {className: ''}).className,
            brk: Math.max(0, ...[...n.querySelectorAll(':scope > p')].slice(0, -1).map(p => parseFloat(getComputedStyle(p).marginBottom)))}; }); }"""

# A source's note on the full path holds no room open (M1): its entry ends where the entry's own words end.
JS_RUNON = """() => [...document.querySelectorAll('.deeper-list > li')].filter(li => li.querySelector(':scope > .note') && li.getClientRects().length).map(li => {
  const own = [...li.children].filter(k => !k.matches('.note') && k.getClientRects().length).map(k => k.getBoundingClientRect().bottom + Math.max(0, parseFloat(getComputedStyle(k).marginBottom)));
  return {slot: li.dataset.slot, extra: li.getBoundingClientRect().bottom - parseFloat(getComputedStyle(li).paddingBottom) - Math.max(...own)}; })"""

# The size of a spacing step where the page is, in CSS pixels.
JS_SP = """(v) => { const d = document.createElement('div'); d.style.height = `var(${v})`; document.body.appendChild(d);
  const h = d.getBoundingClientRect().height; d.remove(); return h; }"""

# Each module's text column in print: where it starts and ends (M1: about two thirds of the page).
JS_COLS = """() => [...document.querySelectorAll('.unit.module .unit-body.reading')].map(b => { const r = b.getBoundingClientRect(); const s = getComputedStyle(b);
  return {id: b.closest('.unit').id, left: r.left + parseFloat(s.paddingLeft), right: r.left + b.clientWidth - parseFloat(s.paddingRight)}; })"""

NOTE_PAGES = ["/pm/"] + UNIT_PAGES + ["/pm/glossary/"]
# The margin checks open each module's full path first: folded, its notes aren't drawn, so they meet nothing, and
# opened, every note shows, so where they sit can be checked as a reader meets them (M1, M2, R7, A13).
OPEN_FULL_PATH = "document.querySelectorAll('.deeper > details').forEach(d => d.open = true)"


def margin_checks(ctx, fix_base, axe_src):
    """M1 to M3 and R3 on the sample-note build: where notes sit, in what face, and how a screen reader meets them."""
    checked("M1", "M2", "M3", "R3")
    for scheme in ("light", "dark"):
        for w in (390, 1280):
            c = ctx(viewport={"width": w, "height": 900}, color_scheme=scheme); pg = c.new_page()
            for path in NOTE_PAGES:
                pg.goto(fix_base + path); pg.evaluate(OPEN_FULL_PATH); pg.evaluate("document.fonts.ready")
                where = f"{path} {scheme} {w}px, a sample note in every slot"
                notes = pg.evaluate(JS_NOTES)
                if not notes:
                    fail("M1", f"{where}: no notes show"); continue
                for n in notes:
                    tag = f"note '{n['note']}'"
                    if n["note"] != n["slot"]:
                        fail("M3", f"{where}: {tag} is not inside or right before its part (found {n['slot']})")
                    if n["hidden"] or n["lead"] != "Sidenote: ":
                        fail("M3", f"{where}: {tag} is not introduced to screen readers as a sidenote (\"Sidenote: \")")
                    if n["after"] not in ("H1", "H2", "H3", "DT", "FIRST") and n["before"] not in ("SLOT", "DESCRIPTION", "PARAGRAPH"):
                        fail("M3", f"{where}: {tag} does not come right after its part's heading, a step's description or its paragraph")
                    if w >= 1024:
                        if n["left"] < n["colRight"] - 1:
                            fail("R3", f"{where}: {tag} sits in the reading column, not the margin")
                        if n["face"] != "shantell sans":
                            fail("M1", f"{where}: {tag} is set in {n['face']}, not the owner's hand")
                        if n["slotBottom"] is not None and n["top"] > n["slotBottom"] + 8:
                            fail("M1", f"{where}: {tag} starts below the end of its part, so it no longer sits beside it")
                        if n["para"] and abs(n["top"] - n["para"][0]) > 8 and abs(n["bottom"] - n["para"][1]) > 8:
                            fail("M1", f"{where}: {tag} names a paragraph, and sits level with neither its top nor its foot")
                        if n["label"] and n["label"]["shown"]:
                            fail("M1", f"{where}: {tag} shows its label in the margin, where its place says it's an aside")
                    else:
                        if n["right"] > n["colRight"] + 1 or n["left"] < n["colLeft"] - 1:
                            fail("R3", f"{where}: {tag} does not fold into the text")
                        if n["face"] == "shantell sans" or n["border"] < 1:
                            fail("M1", f"{where}: {tag} folds in without the typeset face and pen line")
                        if not (n["label"] and n["label"]["shown"] and n["label"]["own"]):
                            fail("M1", f"{where}: {tag} folds in without its label, \"Sidenote:\", on its own line above it")
                        if n["right"] - n["left"] < 0.6 * (n["colRight"] - n["colLeft"]):
                            fail("M1", f"{where}: {tag} folds in only {n['right'] - n['left']:.0f}px wide, in a {n['colRight'] - n['colLeft']:.0f}px column")
                if w >= 1024:
                    _one_edge(notes, where)
                    _margin_overlaps(pg, "M2", where)
                    for e in pg.evaluate(JS_RUNON):
                        if e["extra"] > 1:
                            fail("M1", f"{where}: the full path's source {e['slot']} holds {e['extra']:.0f}px open for its note, which should run on past it")
                    m = pg.evaluate(JS_MARGIN)
                    for e in (m or {}).get("inMargin", []):
                        if not e["owner"]:
                            fail("M1", f"{where}: {e['tag']}.{e['cls']} sits in the margin, and is not one of the owner's notes")
                tok = pg.evaluate(JS_TOKENS, [FS_TOKENS, LH_TOKENS, SP_TOKENS])
                _scale_scan(pg, where, tok, details=False)
                if axe_src and scheme == "light":
                    pg.add_script_tag(content=axe_src)
                    for v in pg.evaluate("""async () => { const r = await axe.run(document, {runOnly: {type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}}); return r.violations.map(v => ({id: v.id, n: v.nodes.length, target: v.nodes[0] && v.nodes[0].target.join(' ')})); }"""):
                        fail("A1", f"{where}: {v['id']} on {v['n']} node(s), e.g. {v['target']}")
            c.close()
    # Doubled text size and the reader's own text spacing, with notes present (R7, A13)
    for rule in ("R7", "A13"):
        c = ctx(viewport={"width": 1280, "height": 900}); pg = c.new_page()
        if rule == "R7":
            cdp = c.new_cdp_session(pg); cdp.send("Page.enable"); cdp.send("Page.setFontSizes", {"fontSizes": {"standard": 32}})
        for path in NOTE_PAGES:
            pg.goto(fix_base + path)
            if rule == "A13":
                pg.add_style_tag(content=TEXT_SPACING)
            pg.evaluate(OPEN_FULL_PATH); pg.evaluate("document.fonts.ready")
            where = f"{path} 1280px, {'text size doubled' if rule == 'R7' else 'text spacing overridden'}, sample notes"
            _margin_overlaps(pg, rule, where)
            for s_ in pg.evaluate(JS_SPILL):
                fail(rule, f"{where}: {s_}")
        c.close()


def _one_edge(notes, where):
    """M1: every note in the margin starts at the same left edge, so the notes read as one column."""
    if not notes:
        return
    edge = min(n["left"] for n in notes)
    for n in notes:
        if n["left"] > edge + 1.5:
            fail("M1", f"{where}: note '{n['note']}' starts {n['left'] - edge:.0f}px right of the margin's edge, out of line with the other notes")


# R10: a module's full path, opened: the column's inner width, the list's and each source's, any control inside it that
# took the full path's Open and Close label, and where its heading ends and what follows it starts: its If you read one
# line (S23), or else its first source.
JS_FULL_PATH = """() => { const sec = document.querySelector('.deeper'); if (!sec) return null;
  const d = sec.querySelector(':scope > details'); d.open = true;
  const sum = d.querySelector(':scope > summary'), ul = sec.querySelector('.deeper-list');
  const cs = getComputedStyle(sec), r = sec.getBoundingClientRect();
  const stray = [...d.querySelectorAll('summary')].filter(x => x !== sum).filter(x => /Open|Close/.test(getComputedStyle(x, '::after').content));
  sum.scrollIntoView({block: 'center'}); const s = sum.getBoundingClientRect(), one = sec.querySelector('.deeper-one'),
        first = (one || ul.firstElementChild).getBoundingClientRect(),  // If you read one (S23) is the first thing under the heading
        li = ul.firstElementChild.getBoundingClientRect(),
        // and under it, the first source starts where the line's own margin ends, pushed down by nothing beside the heading
        gap2 = one ? li.top - one.getBoundingClientRect().bottom - Math.max(parseFloat(getComputedStyle(one).marginBottom), parseFloat(getComputedStyle(ul.firstElementChild).marginTop), parseFloat(getComputedStyle(ul).marginTop)) : 0;
  return {inner: r.width - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight), ul: ul.getBoundingClientRect().width,
          lis: [...ul.children].map(li => li.getBoundingClientRect().width), stray: stray.length,
          gap: first.top - s.bottom, gap2, left: r.left, width: r.width, bottom: s.bottom, sl: s.left, st: s.top, sw: s.width, sh: s.height}; }"""


def full_path_checks(ctx, base, fix_base):
    """R10: each module's full path, opened, spans its column; its Open and Close label draws nothing outside its own
    heading and pushes no source down, with or without a note beside the first source; and no control inside it
    takes the label. Checked on the site and on the sample-note build, where every source has a note."""
    checked("R10")
    for b_, kind in ((base, "the site"), (fix_base, "sample notes")):
        if not b_:
            continue
        for w in (390, 1280):
            c = ctx(viewport={"width": w, "height": 900}); pg = c.new_page()
            for path, _ in MODULES:
                pg.goto(b_ + path); pg.evaluate("document.fonts.ready")
                where = f"{path} {w}px, {kind}, the full path open"
                f = pg.evaluate(JS_FULL_PATH)
                if not f:
                    fail("R10", f"{where}: no full path"); continue
                if abs(f["ul"] - f["inner"]) > 1 or any(abs(x - f["inner"]) > 1 for x in f["lis"]):
                    fail("R10", f"{where}: the sources take {min([f['ul']] + f['lis']):.0f}px of the column's {f['inner']:.0f}px")
                if f["stray"]:
                    fail("R10", f"{where}: {f['stray']} control(s) inside the full path show its Open or Close label")
                if abs(f["gap"]) > 1:
                    fail("R10", f"{where}: the first source starts {f['gap']:.0f}px below the full path's heading, pushed down by its label")
                if abs(f["gap2"]) > 1:
                    fail("R10", f"{where}: the first source starts {f['gap2']:.0f}px below the If you read one line, pushed down by something beside the heading")
                clip = {"x": f["left"], "y": f["bottom"], "width": f["width"], "height": 40}
                # the heading's right half, where the label must not draw: it sits at the left (the owner, 25 November 2026)
                right = {"x": f["sl"] + f["sw"] / 2, "y": f["st"], "width": f["sw"] / 2, "height": f["sh"]}
                shown, shown_r = pg.screenshot(clip=clip), pg.screenshot(clip=right)
                pg.add_style_tag(content=".deeper > details > summary::after { visibility: hidden !important; }")
                hidden, hidden_r = pg.screenshot(clip=clip), pg.screenshot(clip=right)
                if shown != hidden:
                    fail("R10", f"{where}: the Open and Close label draws below its heading, over the first source")
                if shown_r != hidden_r:
                    fail("R10", f"{where}: the Open and Close label sits at the right of the column, not at the left under its heading")
            c.close()


def page_text_width():
    """The printed page's text width in CSS pixels: Letter, less the side margins of the @page rule in pm.css."""
    css = open(os.path.join(ROOT, "assets", "css", "pm.css"), encoding="utf-8").read()
    m = re.search(r"@page\s*\{[^}]*size:\s*Letter;[^}]*margin:\s*[\d.]+in\s+([\d.]+)in", css)
    return (8.5 - 2 * float(m.group(1))) * 96


def print_margin_checks(ctx, fix_base):
    """M1 and M2 in print, on the sample-note build laid out at the page's text width: a module's text takes about two
    thirds of the page, and its notes print in the margin column in the owner's hand, beside their parts, apart from
    each other; on Start, a card or the glossary a note folds in under its part."""
    checked("M1", "M2")
    W = page_text_width()
    c = ctx(viewport={"width": int(W), "height": 1100}); pg = c.new_page()
    pg.goto(fix_base + "/pm/all/"); pg.emulate_media(media="print"); pg.evaluate("document.fonts.ready")
    where = "print /pm/all/, a sample note in every slot"
    sp3 = pg.evaluate(JS_SP, "--sp-3")
    for col in pg.evaluate(JS_COLS):
        share = (col["right"] - col["left"]) / W
        if not 0.6 <= share <= 0.72:
            fail("M1", f"{where}: {col['id']}'s text takes {share:.0%} of the page's width, not about two thirds")
    margin = []
    for n in pg.evaluate(JS_NOTES):
        tag = f"note '{n['note']}' in {n['kind'].replace('unit ', '')}"
        if "module" in n["kind"].split():
            if n["left"] < n["colRight"] + 1 or n["right"] > W + 0.5:
                fail("M1", f"{where}: {tag} does not print in the margin column beside the text")
            if n["face"] != "shantell sans":
                fail("M1", f"{where}: {tag} prints in {n['face']}, not the owner's hand")
            if n["slotBottom"] is not None and n["top"] > n["slotBottom"] + 8:
                fail("M1", f"{where}: {tag} starts below the end of its part, so it no longer sits beside it")
            if n["para"] and abs(n["top"] - n["para"][0]) > 8 and abs(n["bottom"] - n["para"][1]) > 8:
                fail("M1", f"{where}: {tag} names a paragraph, and sits level with neither its top nor its foot")
            if n["brk"] >= sp3:
                fail("M2", f"{where}: a break inside {tag} is {n['brk']:.0f}px, as wide as the gap between two notes")
            if n["label"] and n["label"]["shown"]:
                fail("M1", f"{where}: {tag} prints its label in the margin, where its place says it's an aside")
            margin.append(n)
        else:
            if n["right"] > n["colRight"] + 1 or n["left"] < n["colLeft"] - 1:
                fail("M1", f"{where}: {tag} does not fold into the text")
            if n["face"] != "shantell sans" or n["border"] < 1:
                fail("M1", f"{where}: {tag} folds in without the owner's hand and the pen line")
            if not (n["label"] and n["label"]["shown"] and n["label"]["own"]):
                fail("M1", f"{where}: {tag} folds in without its label, \"Sidenote:\", on its own line above it")
    _one_edge(margin, where)
    margin.sort(key=lambda n: n["top"])
    for a_, b_ in zip(margin, margin[1:]):
        if b_["top"] < a_["bottom"] + sp3 - 0.5:
            fail("M2", f"{where}: notes '{a_['note']}' and '{b_['note']}' print {b_['top'] - a_['bottom']:.0f}px apart, closer than --sp-3 ({sp3:.0f}px)")
    for e in pg.evaluate(JS_RUNON):
        if e["extra"] > 1:
            fail("M1", f"{where}: the full path's source {e['slot']} holds {e['extra']:.0f}px open for its note, which should run on past it")
    c.close()


def pdf_note_checks(pdf_path, out_dir):
    """M1 in the PDF itself: each of the owner's notes in a module prints whole, on one page, in the margin column, and
    a paragraph with a note prints whole on the same page."""
    import html
    from bs4 import BeautifulSoup
    checked("M1")
    css = open(os.path.join(ROOT, "assets", "css", "pm.css"), encoding="utf-8").read()
    mg = re.search(r"\.module\s*\{\s*--margin:\s*([\d.]+)in;\s*--gutter:\s*([\d.]+)in;", css)
    side = (8.5 * 96 - page_text_width()) / 2 / 96
    if not mg:
        fail("M1", "pm.css gives a module no print margin column (--margin and --gutter in inches)"); return
    edge = (8.5 - side - float(mg.group(1)) - float(mg.group(2)) / 2) * 72   # halfway across the gutter, in points
    toks = lambda t: [w for w in (re.sub(r"[^0-9a-z]", "", x.lower()) for x in t.split()) if w]
    raw = subprocess.run(["pdftotext", "-bbox", pdf_path, "-"], capture_output=True, text=True).stdout
    pages = []
    for pg_ in re.findall(r"<page[^>]*>(.*?)</page>", raw, re.S):
        ws = [(float(a), float(b), html.unescape(w)) for a, b, w in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)"[^>]*>([^<]*)<', pg_)]
        lines = lambda keep: [t for _, _, w in sorted((w for w in ws if keep(w[0])), key=lambda w: (round(w[1] / 3), w[0])) for t in toks(w)]
        pages.append((lines(lambda x: x >= edge), lines(lambda x: x < edge)))

    def found(seq, words):
        return any(words[i:i + len(seq)] == seq for i in range(len(words) - len(seq) + 1))

    soup = BeautifulSoup(open(os.path.join(out_dir, "pm", "all", "index.html"), encoding="utf-8").read(), "html.parser")
    for n in soup.select(".unit.module aside.note"):
        for sr in n.select(".sr, .note-label"):
            sr.decompose()
        t = toks(n.get_text(" "))
        head, tail = t[:4], t[-4:]
        on = [i for i, (m, _) in enumerate(pages) if found(head, m) and found(tail, m)]
        label = " ".join(n.get_text(" ").split()[:6])
        if not on:
            fail("M1", f"PDF: the note '{label} ...' does not print whole, on one page, in the margin column"); continue
        para = n.find_previous_sibling("p") if "noted" in (n.parent.get("class") or []) else None
        if para is not None:
            pt = toks(para.get_text(" "))
            if not any(found(pt[:4], pages[i][1]) and found(pt[-4:], pages[i][1]) for i in on):
                fail("M1", f"PDF: the paragraph beside the note '{label} ...' does not print whole on the note's page")


class Server:
    def __init__(self, directory):
        class Q(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *a):
                pass
        class S(socketserver.ThreadingMixIn, socketserver.TCPServer):
            # one thread per connection: a browser that holds a connection open must not stall the next page
            daemon_threads = True
            allow_reuse_address = True

            def handle_error(self, *a):  # a page left mid-load is not an error
                pass
        self.srv = S(("127.0.0.1", 0), functools.partial(Q, directory=directory))
        self.base = f"http://127.0.0.1:{self.srv.server_address[1]}"
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()

    def close(self):
        self.srv.shutdown()


# ---------- static checks ----------
def _drop_print(css):
    """The stylesheet without its @media print blocks: print sets the scales in points, which is right for paper."""
    out, i = [], 0
    for m in re.finditer(r"@media\s+print\s*\{", css):
        if m.start() < i:
            continue
        out.append(css[i:m.start()]); depth, j = 1, m.end()
        while j < len(css) and depth:
            depth += {"{": 1, "}": -1}.get(css[j], 0); j += 1
        i = j
    out.append(css[i:])
    return "".join(out)


def license_checks(out_dir):
    """L1: every page but the front door says whose it is; syllabus pages give the license; the repo carries both."""
    from bs4 import BeautifulSoup
    checked("L1")
    cfg = yaml.safe_load(open(os.path.join(ROOT, "hugo.yaml")))
    owner, lic = cfg.get("copyright", ""), (cfg.get("params") or {}).get("license") or {}
    if not owner or not lic.get("url") or not lic.get("name"):
        fail("L1", "hugo.yaml needs a copyright line and params.license with a name and url")
        return
    path = os.path.join(ROOT, "LICENSE")
    if not os.path.exists(path) or not open(path, encoding="utf-8").read().startswith("MIT License"):
        fail("L1", "LICENSE is not the MIT License")
    path = os.path.join(ROOT, "LICENSE-content.md")
    if not os.path.exists(path) or lic["url"] not in open(path, encoding="utf-8").read():
        fail("L1", "LICENSE-content.md is missing or does not link the syllabus's license")
    for f in glob.glob(os.path.join(out_dir, "**", "index.html"), recursive=True):
        rel = os.path.relpath(os.path.dirname(f), out_dir).replace(os.sep, "/")
        rel = "/" if rel == "." else f"/{rel}/"
        if rel == "/":
            continue   # the front door has no footer
        foot = BeautifulSoup(open(f, encoding="utf-8").read(), "html.parser").select_one(".site-foot")
        if not foot or owner not in foot.get_text():
            fail("L1", f"{rel}: no copyright line at the foot of the page")
            continue
        if rel.startswith("/pm/") and not foot.select_one(f'a[href="{lic["url"]}"][rel~="license"]'):
            fail("L1", f"{rel}: the syllabus page does not link its license")


# N2: the old site's addresses that must land on the 404 page, and the pages that wait (R9) and so aren't built.
NOT_BUILT = ["/tags/", "/categories/", "/page/", "/writing/"]
# N3: the pages whose link preview shows the owner's photo; every other page is text only.
PREVIEW_PHOTO = {"/", "/page/readme/"}


def arrival_checks(out_dir):
    """N1 to N3: no placeholder reaches a reader, a missing page goes to the front door, and every page has a link
    preview, with the photo on the front door and the ReadMe only. R9's part here: the menu names only built sections."""
    from bs4 import BeautifulSoup
    checked("N1", "N2", "N3")
    cfg = yaml.safe_load(open(os.path.join(ROOT, "hugo.yaml")))
    base = cfg["baseURL"].rstrip("/")
    params = cfg.get("params") or {}
    # N1: no note marked as a placeholder in the content, and no built page that says it has nothing yet
    for f in glob.glob(os.path.join(ROOT, "content", "**", "*.md"), recursive=True):
        if re.search(r"<!--[^>]*placeholder", open(f, encoding="utf-8").read(), re.I):
            fail("N1", f"{os.path.relpath(f, ROOT)} carries a placeholder note")
    pages = {}
    for f in glob.glob(os.path.join(out_dir, "**", "index.html"), recursive=True):
        rel = os.path.relpath(os.path.dirname(f), out_dir).replace(os.sep, "/")
        rel = "/" if rel == "." else f"/{rel}/"
        pages[rel] = BeautifulSoup(open(f, encoding="utf-8").read(), "html.parser")
    for rel, soup in sorted(pages.items()):
        main = soup.select_one("main")
        if main and (main.select_one(".empty") or re.search(r"nothing here yet", main.get_text(), re.I)):
            fail("N1", f"{rel} says it has nothing yet")
    # N2: the 404 page sends the browser home at once, links home, and nowhere else in its main content
    nf = os.path.join(out_dir, "404.html")
    if not os.path.exists(nf):
        fail("N2", "no 404.html is built")
    else:
        soup = BeautifulSoup(open(nf, encoding="utf-8").read(), "html.parser")
        ref = soup.select_one('meta[http-equiv="refresh"]')
        m = re.match(r"\s*0\s*;\s*url=(\S+)\s*$", ref.get("content", "")) if ref else None
        if not m or m.group(1) not in ("/", base + "/"):
            fail("N2", "404.html does not send the browser to the front door at once")
        robots = soup.select_one('meta[name="robots"]')
        if not robots or "noindex" not in robots.get("content", ""):
            fail("N2", "404.html may be indexed")
        main = soup.select_one("main")
        links = [a.get("href") for a in main.select("a[href]")] if main else []
        if "/" not in links:
            fail("N2", "404.html gives no plain link to the front door")
        if any(h != "/" for h in links):
            fail("N2", f"404.html links elsewhere than the front door: {', '.join(h for h in links if h != '/')}")
    # R9: the menu names only sections that are built, so Writing stays out of it until it has a post
    for item in (cfg.get("menu") or {}).get("main") or []:
        url = item.get("url", "")
        if url in NOT_BUILT or not os.path.exists(os.path.join(out_dir, url.strip("/"), "index.html")):
            fail("R9", f"the menu names {item.get('name')}, at {url}, which isn't built")
    for rel in NOT_BUILT:
        if os.path.exists(os.path.join(out_dir, rel.strip("/"), "index.html")):
            fail("N2", f"{rel} is built, so a visitor there doesn't land on the 404 page")
    # N3: every page's link preview, and the photo only where it belongs
    photo = params.get("photo", "")
    for rel, soup in sorted(pages.items()):
        meta = {}
        for t in soup.select("head meta[property], head meta[name]"):
            meta[t.get("property") or t.get("name")] = t.get("content", "")
        for k in ("og:title", "og:description", "og:site_name", "og:type"):
            if not meta.get(k, "").strip():
                fail("N3", f"{rel}: no {k}")
        if meta.get("og:url") != base + rel:
            fail("N3", f"{rel}: og:url is {meta.get('og:url')!r}, not its address {base + rel}")
        if meta.get("og:site_name") and meta["og:site_name"] != cfg.get("title"):
            fail("N3", f"{rel}: og:site_name is not the site's name")
        if meta.get("twitter:card") != "summary":
            fail("N3", f"{rel}: no summary card for other sites")
        img = meta.get("og:image")
        if rel in PREVIEW_PHOTO:
            if img != base + photo:
                fail("N3", f"{rel}: the preview does not show the owner's photo at its full address")
            elif not os.path.exists(os.path.join(out_dir, photo.lstrip("/"))):
                fail("N3", f"{rel}: the preview's photo is not built")
            if meta.get("og:image:alt") != params.get("photo_alt"):
                fail("N3", f"{rel}: the preview's photo lacks its alt text")
        elif img:
            fail("N3", f"{rel}: names an image for its preview, though only the front door and the ReadMe do")


def start_checks(out_dir):
    """S19: Start invites the reader to write to the owner, in a paragraph after How it works, its link's text
    the address itself, so a reader whose browser opens no mail app can still copy it."""
    from bs4 import BeautifulSoup
    checked("S19")
    links = (yaml.safe_load(open(os.path.join(ROOT, "hugo.yaml"))).get("params") or {}).get("links") or []
    mail = next((str(l["url"]) for l in links if str(l.get("url", "")).startswith("mailto:")), "")
    if not mail:
        fail("S19", "hugo.yaml's footer links no email address, so Start has none to give")
        return
    addr = mail[len("mailto:"):]
    soup = BeautifulSoup(open(os.path.join(out_dir, "pm", "index.html"), encoding="utf-8").read(), "html.parser")
    intro = soup.select_one('[data-slot="intro"]')
    how = intro.find("h2", id="how-it-works") if intro else None
    if not how:
        fail("S19", "Start has no \"How it works\" for its invitation to follow")
        return
    found = intro.find_all("a", href=mail)
    if not found:
        fail("S19", f"Start doesn't invite the reader to write: nothing in its opening links {addr}")
        return
    if not any(a.get_text(strip=True) == addr for a in found):
        fail("S19", f"Start links {addr} under other words, so a reader whose browser opens no mail app can't copy it")
        return
    a = next(a for a in found if a.get_text(strip=True) == addr)
    p = a.find_parent("p")
    if how not in a.find_all_previous("h2"):
        fail("S19", "Start's invitation to write comes before \"How it works\", not after it")
    elif not p or p.find_parent("li") or p.parent is not intro:
        fail("S19", "Start's invitation to write isn't a paragraph of its own after How it works' list")


NAME_PARTS = "li.step, .deeper-list > li, details.recall > .answer, .answers li, .walk, details.example"
NAME_SKIP = "script, style, nav, h1, .unit-head, .unit-foot, .note, .note-label, [data-voice], .sr, .step-body > h3, .step-links, .deeper-list > li > h3, summary, .walk-title, .last-time > .hint"


def _closest(el, sel):
    """The nearest element above el that matches a CSS selector, or None."""
    import soupsieve
    for p_ in el.parents:
        if getattr(p_, "name", None) and p_.name != "[document]" and soupsieve.match(sel, p_):
            return p_
    return None


def _unit_names(out_dir):
    """Every unit a name can link (G8): its address on the site, its id in the single document, and a pattern for its
    name, straight or typeset."""
    from bs4 import BeautifulSoup
    units = {}
    for path in UNIT_PAGES:
        title = (BeautifulSoup(open(os.path.join(out_dir, path.strip("/"), "index.html"), encoding="utf-8").read(), "html.parser")
                 .select_one("article.unit h1"))
        name = " ".join(title.get_text(" ", strip=True).split()).replace("’", "'")
        units[path] = {"name": name, "id": path.rstrip("/").split("/")[-1],
                       "re": re.compile(r"(?<![\w'’])" + re.escape(name).replace("'", "['’]") + r"(?![\w])")}
    return units


def _name_events(art, units, here):
    """The names and the links to units in one unit's article, in reading order, each with its part (G8): a step, a
    source, an answer, a walk, an example, or else the section of prose under the last heading."""
    from bs4 import NavigableString, Tag
    events, h2, quotes, straight = [], "top", defaultdict(int), defaultdict(int)
    by_href = {p: p for p in units}
    by_href.update({"#" + u["id"]: p for p, u in units.items()})
    for el in art.descendants:
        if isinstance(el, Tag):
            if el.name == "h2" and not _closest(el, NAME_PARTS):
                h2 = el.get_text(" ", strip=True)
            if el.name == "a" and el.get("href") in by_href:
                part = _closest(el, NAME_PARTS)
                key = id(part) if part else h2
                skip = _closest(el, NAME_SKIP)
                question = (el.find_parent("summary") and el.find_parent("details", class_="recall")) or _closest(el, ".last-time > .hint")
                if question:
                    events.append(("question", key, by_href[el["href"]], el.get_text(" ", strip=True)))
                elif not skip:
                    events.append(("link", key, by_href[el["href"]], el.get_text(" ", strip=True)))
            continue
        if not isinstance(el, NavigableString) or el.find_parent("a") or _closest(el, NAME_SKIP):
            continue
        part = _closest(el, NAME_PARTS)
        key = id(part) if part else h2
        text = str(el)
        for path, u in units.items():
            for m in u["re"].finditer(text):
                head = text[:m.start()]
                curly = quotes[key] + head.count("“") - head.count("”")
                plain = (straight[key] + head.count('"')) % 2
                if curly <= 0 and not plain:   # words in quotation marks, curly or straight, aren't the course naming a unit
                    events.append(("name", key, path, m.group(0)))
        quotes[key] += text.count("“") - text.count("”")
        straight[key] += text.count('"')
    return events


def name_link_checks(out_dir):
    """G8 in the built pages: where a unit's words name another unit, the first mention in each part links it, and no
    other does; no unit links itself; a question meant for recall links nothing; and the single document lands every
    such link on the unit in the page, and each module's Do and Check steps on its own. Then a browser follows two."""
    from bs4 import BeautifulSoup
    checked("G8")
    units = _unit_names(out_dir)
    page = lambda path: BeautifulSoup(open(os.path.join(out_dir, path.strip("/"), "index.html"), encoding="utf-8").read(), "html.parser")
    count = 0
    for path in ["/pm/"] + UNIT_PAGES:
        art = page(path).select_one("article.unit")
        if not art:
            fail("G8", f"{path} has no unit to read"); continue
        first = {}
        for kind, part, target, words in _name_events(art, units, path):
            name = units[target]["name"]
            if kind == "question":
                fail("G8", f"{path} links {name} in a question meant for recall, which hands the reader the place to look")
                continue
            if target == path:
                if kind == "link":
                    fail("G8", f"{path} links its own name, {name}")
                continue
            seen = first.get((part, target))
            if seen is None:
                first[(part, target)] = kind
                if kind == "name":
                    fail("G8", f"{path} names {name} without linking it, the first time its part does (\"{words}\", in {part if isinstance(part, str) else 'a step, source, answer or walk'})")
                else:
                    count += 1
            elif kind == "link":
                fail("G8", f"{path} links {name} twice in one part: a name met again stays words")
    if count < 60:
        fail("G8", f"only {count} names link another unit across the syllabus, fewer than the walks found unlinked")
    # G8: in the single document every link to a unit lands on the unit in the page, and each module's Do and Check
    # steps land on that module's own Do and Check
    whole = page("/pm/all/")
    ids = {e.get("id") for e in whole.select("[id]")}
    for a in whole.select("a[href]"):
        h = a["href"]
        if h.split("#")[0] in units:
            fail("G8", f"the single document links {h}, the unit's page, where it should land on the unit in the page")
        elif h.startswith("#") and h[1:] not in ids and "'" not in h:
            fail("G8", f"the single document links {h}, which nothing in it carries")
    for art in whole.select("article.unit.module"):
        key = art.get("id")
        for kind in ("do", "check"):
            a = art.select_one(f"li.step-down a[href='#{key}-{kind}']")
            if not a or not art.select_one(f"#{key}-{kind}"):
                fail("G8", f"in the single document, {key}'s {kind.capitalize()} step doesn't land on its own {kind.capitalize()} (#{key}-{kind})")
    # G8: in a browser, a name in The Compass shows its unit in the single document and focuses its title, and a
    # module's Do step stays in that module
    chrome = os.environ.get("CHROME")
    srv = Server(out_dir)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=chrome) if chrome else p.chromium.launch()
            pg = b.new_page(viewport={"width": 1280, "height": 900})
            pg.goto(srv.base + "/pm/all/#the-compass"); pg.wait_for_load_state("load")
            pg.locator("#the-compass .walk a[href='#see-the-system']").first.click(); pg.wait_for_timeout(200)
            got = pg.evaluate("() => ({cur: (document.querySelector('.unit.is-current') || {}).id, focus: document.activeElement && document.activeElement.closest('.unit') && document.activeElement.closest('.unit').id, h1: document.activeElement && document.activeElement.tagName})")
            if got != {"cur": "see-the-system", "focus": "see-the-system", "h1": "H1"}:
                fail("G8", f"in the single document, The Compass's link to See the System shows {got.get('cur')} with focus on {got.get('h1')} in {got.get('focus')}, not See the System's title")
            pg.goto(srv.base + "/pm/all/#find-the-constraint"); pg.wait_for_load_state("load")
            pg.locator("#find-the-constraint a[href='#find-the-constraint-do']").first.click(); pg.wait_for_timeout(200)
            cur = pg.evaluate("() => (document.querySelector('.unit.is-current') || {}).id")
            if cur != "find-the-constraint":
                fail("G8", f"in the single document, Find the Constraint's Do step shows {cur}, not its own Do")
            b.close()
    finally:
        srv.close()


def thread_checks(out_dir):
    """S22: the AI and data threads run as lines in the course's own frames. Each line data/pm/threads.yaml lists is
    on its unit's built page, and The Compass asks the data thread's three questions."""
    from bs4 import BeautifulSoup
    checked("S22")
    path = os.path.join(ROOT, "data", "pm", "threads.yaml")
    if not os.path.exists(path):
        fail("S22", "data/pm/threads.yaml is missing, so nothing says where the AI and data threads run")
        return
    th = yaml.safe_load(open(path, encoding="utf-8")) or {}
    norm = lambda t: " ".join(str(t).replace("\u2019", "'").replace("\u2018", "'")
                              .replace("\u201c", '"').replace("\u201d", '"').split())
    texts = {}

    def text(unit):
        if unit not in texts:
            f = os.path.join(out_dir, "pm", *unit.split("/"), "index.html")
            if not os.path.exists(f):
                texts[unit] = None
            else:
                main = BeautifulSoup(open(f, encoding="utf-8").read(), "html.parser").find("main")
                texts[unit] = norm(main.get_text(" ")) if main else ""
        return texts[unit]

    for thread in ("ai", "data"):
        lines = th.get(thread) or []
        if len(lines) < 3:
            fail("S22", f"the {thread} thread runs through {len(lines)} line(s) in data/pm/threads.yaml, too few to be a thread")
        for e in lines:
            t = text(e["unit"])
            if t is None:
                fail("S22", f"the {thread} thread names {e['unit']}, which has no built page")
            elif norm(e["words"]) not in t:
                fail("S22", f"{e['unit']}: the {thread} thread's line \"{e['words']}\" isn't on the page")
    c = th.get("compass") or {}
    t = text(c.get("unit", "the-compass"))
    if not c.get("questions"):
        fail("S22", "data/pm/threads.yaml gives The Compass no questions to carry for the data thread")
    elif t is None or norm(c["questions"]) not in t:
        fail("S22", "The Compass doesn't ask the data thread's three questions: " + c["questions"])


JS_WALKS = """() => ({ toggle: (() => { const t = document.querySelector('[data-walk-toggle]'); return !!t && t.getClientRects().length > 0; })(),
  shown: [...document.querySelectorAll('[data-walk]')].filter(w => w.getClientRects().length > 0).map(w => w.dataset.walk),
  pressed: [...document.querySelectorAll('[data-walk-show]')].filter(b => b.getAttribute('aria-pressed') === 'true').map(b => b.dataset.walkShow),
  focus: document.activeElement && document.activeElement.dataset ? document.activeElement.dataset.walkShow || '' : '' })"""


def walk_browser_checks(out_dir, path, walks):
    """S21 in a browser: the first version shows, a button swaps it and keeps focus; without the script, and in
    print, both versions show and the buttons don't."""
    if len(walks) != 2:
        return
    chrome = os.environ.get("CHROME")
    srv = Server(out_dir)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=chrome) if chrome else p.chromium.launch()
            for js in (True, False):
                ctx = b.new_context(viewport={"width": 390, "height": 900}, java_script_enabled=js)
                pg = ctx.new_page()
                pg.goto(srv.base + path)
                r = pg.evaluate(JS_WALKS) if js else None
                if js:
                    if not r["toggle"] or r["shown"] != walks[:1] or r["pressed"] != walks[:1]:
                        fail("S21", f"{path}: with the script, the buttons and the first version should show, and only it: {r}")
                    pg.click(f"button[data-walk-show={walks[1]}]")
                    r = pg.evaluate(JS_WALKS)
                    if r["shown"] != walks[1:] or r["pressed"] != walks[1:]:
                        fail("S21", f"{path}: the second button doesn't swap the versions: {r}")
                    if r["focus"] != walks[1]:
                        fail("S21", f"{path}: focus left the button that was pressed (A9)")
                    pg.emulate_media(media="print")
                    r = pg.evaluate(JS_WALKS)
                    if r["shown"] != walks or r["toggle"]:
                        fail("S21", f"{path}: in print both versions should show, and no buttons: {r}")
                else:
                    shown = pg.evaluate("() => [...document.querySelectorAll('[data-walk]')].filter(w => w.getClientRects().length > 0).map(w => w.dataset.walk)")
                    tog = pg.evaluate("() => { const t = document.querySelector('[data-walk-toggle]'); return !!t && t.getClientRects().length > 0; }")
                    if shown != walks or tog:
                        fail("S21", f"{path}: without the script both versions should show, and no buttons: {shown}")
                ctx.close()
            b.close()
    finally:
        srv.close()


# ---------- getting around: the course bar and the foot (G1 to G5) ----------
# The pages that carry the bar: every syllabus page but the single document (the owner, 25 November 2026, job 40).
# The foot is on the modules and the cards. In a browser, one page of each kind, the pilot's two among them, and the
# last module, whose place is the longest.
BAR_PAGES = ["/pm/"] + UNIT_PAGES + ["/pm/glossary/", CARDS_INDEX]
BAR_BROWSER_PAGES = ["/pm/", "/pm/find-the-constraint/", "/pm/cards/five-focusing-steps/", MODULES[-1][0], CLOSING, "/pm/glossary/"]


def _bar_kind(path, cards_of):
    """What a page is to the bar: Start, a module, a card, The Compass, the concept cards or the glossary."""
    return "start" if path == "/pm/" else "closing" if path == CLOSING else "glossary" if path == "/pm/glossary/" else "cards" if path == CARDS_INDEX else "card" if path in cards_of else "module"


def _course_order(out_dir):
    """The course's order (G1): Start, each built module on the map, then the closing unit, as (path, label)."""
    mods = yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "modules.yaml")))
    order = [("/pm/", "Start")]
    order += [(f"/pm/{m['page']}/", f"Module {m['num']}, {m['title']}") for m in mods if m.get("page")]
    order.append((CLOSING, "The Compass"))
    return mods, order


def course_bar_checks(out_dir):
    """G1 to G5 in the built pages: the bar's place, its previous and next, its list, its plain links for a reader
    without scripts, and the foot. Then course_bar_browser_checks, in a browser."""
    from bs4 import BeautifulSoup
    checked("G1", "G2", "G4", "G5")
    mods, order = _course_order(out_dir)
    paths = [p for p, _ in order]
    page = lambda path: BeautifulSoup(open(os.path.join(out_dir, path.strip("/"), "index.html"), encoding="utf-8").read(), "html.parser")
    start = page("/pm/")
    course = start.select_one("h1").get_text(" ", strip=True)
    if not start.find(id="modules") or start.find(id="modules").name != "h2":
        fail("G4", "Start's list of modules has no address (#modules) for the bar's plain link to land on")
    cards_of = {}
    for m, cards in MODULES:
        for c in cards:
            cards_of[c] = m
    for path in BAR_PAGES:
        soup = page(path)
        bars = soup.select("nav.course-bar")
        if len(bars) != 1:
            fail("G1", f"{path}: {len(bars)} course bars, not one")
            continue
        bar = bars[0]
        head = soup.select_one("header.masthead")
        if not head or bar.find_previous("header") is not head or bar.find_parent("main") or not bar.find_next("main"):
            fail("G1", f"{path}: the course bar isn't between the site header and the page's main content")
        if bar.get("aria-label") != course:
            fail("G2", f"{path}: the bar's landmark is named '{bar.get('aria-label')}', not '{course}'")
        kind = _bar_kind(path, cards_of)
        mod_path = cards_of.get(path, path)
        if kind in ("module", "card"):
            slug = mod_path.strip("/").split("/")[-1]
            m = next((x for x in mods if x.get("page") == slug), None)
            if not m:
                fail("G1", f"{path}: no module on the map for this page")
                continue
            k = mods.index(m) + 1   # its place in the map's order, from 1 (the owner, 26 November 2026)
            nth = f"{k}{'th' if 10 <= k % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(k % 10, 'th')}"
            want = f"{course}, Module {m['num']}, {nth} of {len(mods)}"
        else:
            want = f"{course}, " + {"start": "Start", "closing": "The Compass", "glossary": "Glossary", "cards": "Concept cards"}[kind]
        link, btn = bar.select_one("a.cb-place"), bar.select_one("button.cb-place")
        for el, what in ((link, "plain link"), (btn, "button")):
            if not el:
                fail("G4" if what == "plain link" else "G2", f"{path}: the bar's place has no {what}")
            elif " ".join(el.get_text().split()) != want:
                fail("G1", f"{path}: the bar's {what} reads '{' '.join(el.get_text().split())}', not '{want}'")
        if link and link.get("href") != "/pm/#modules":
            fail("G4", f"{path}: without scripts the bar's place goes to {link.get('href')}, not Start's list (/pm/#modules)")
        # G1: the course and the place are two spans, the course quiet and the place bold; one chevron, on the button
        for el, what in ((link, "plain link"), (btn, "button")):
            if el and ([x.get_text(" ", strip=True) for x in el.select(".cb-course")] != [course + ","] or [x.get_text(" ", strip=True) for x in el.select(".cb-here")] != [want[len(course) + 2:]]):
                fail("G1", f"{path}: the bar's {what} doesn't set the course and the place apart (.cb-course, .cb-here)")
        if link and link.select(".cb-chev"):
            fail("G4", f"{path}: without scripts the bar's place shows a chevron, though it opens nothing")
        if btn and len(btn.select(".cb-chev")) != 1:
            fail("G1", f"{path}: the bar's place has {len(btn.select('.cb-chev'))} chevrons, not one")
        if bar.select(".cb-steps .cb-chev"):
            fail("G1", f"{path}: the bar's previous and next carry arrows; they're words (the owner, card bar-arrows)")
        if btn:
            if btn.get("type") != "button" or btn.get("aria-expanded") != "false" or not btn.has_attr("hidden"):
                fail("G2", f"{path}: the bar's button should start hidden (the script shows it), closed, with aria-expanded")
            ctl = btn.get("aria-controls")
            menu = soup.find(id=ctl) if ctl else None
            if not menu or not menu.has_attr("hidden") or not bar.find(id=ctl):
                fail("G2", f"{path}: the bar's button controls no list inside the bar, or the list doesn't start hidden")
        # a concept card keeps its module's place and list, with no previous or next (the owner, 26 November 2026)
        i = paths.index(mod_path) if mod_path in paths and kind != "card" else None
        for rel, j in (("prev", -1 if i is None else i - 1), ("next", -1 if i is None else i + 1)):
            a = bar.select_one(f"a.cb-step[rel={rel}]")
            exp = paths[j] if 0 <= j < len(paths) else None
            got = a.get("href") if a else None
            if got != exp:
                fail("G1", f"{path}: the bar's {rel} goes to {got}, not {exp}")
            elif a and order[j][1] not in a.get_text(" ", strip=True):
                fail("G2", f"{path}: the bar's {rel} doesn't name '{order[j][1]}' for a screen reader")
        items = bar.select(".cb-list > li")
        got = [re.sub(r"\s+", " ", li.get_text(" ", strip=True)) for li in items]
        if len(items) != len(mods):
            fail("G1", f"{path}: the bar's list has {len(items)} modules, not the map's {len(mods)}")
        for li, x in zip(items, mods):
            a = li.find("a")
            if x.get("page"):
                if not a or a.get("href") != f"/pm/{x['page']}/" or x["title"] not in a.get_text(" ", strip=True) or not li.find(attrs={"data-map-status": True}) or li.get("data-map-unit") != x["page"]:
                    fail("G1", f"{path}: the bar's list doesn't link Module {x['num']}, {x['title']}, with its progress")
            if str(x["num"]) not in li.get_text(" ", strip=True):
                fail("G1", f"{path}: the bar's list doesn't number {x['title']}")
        cur = bar.select(".cb-list a[aria-current]")
        if kind in ("module", "card"):
            if [a.get("href") for a in cur] != [mod_path]:
                fail("G2", f"{path}: the place in the bar's list is marked on {[a.get('href') for a in cur]}, not {mod_path}")
            elif cur[0].get("aria-current") != ("page" if path == mod_path else "true"):
                fail("G2", f"{path}: the place is marked aria-current='{cur[0].get('aria-current')}'")
        elif cur:
            fail("G2", f"{path}: the bar's list marks a module, {[a.get('href') for a in cur]}, as the place")
        more = [a.get("href") for a in bar.select(".cb-more a")]
        if more != [CLOSING, CARDS_INDEX, "/pm/glossary/"]:
            fail("G1", f"{path}: after the modules the bar's list goes to {more}, not The Compass, the concept cards and the glossary")
        marked = [a.get("href") for a in bar.select(".cb-more a[aria-current=page]")]
        if marked != ([path] if kind in ("closing", "glossary", "cards") else []):
            fail("G2", f"{path}: after the modules the bar's list marks {marked} as the place")
        # G1: what Start's Continue names for a screen reader, each place it can go
        labels = [(a.get("href"), a.get("data-label")) for a in bar.select(".cb-list a, .cb-more a") if a.get("href") not in ("/pm/glossary/", CARDS_INDEX)]
        if labels != [(p_, l_) for p_, l_ in order[1:]]:
            fail("G1", f"{path}: the bar's list doesn't label each module and The Compass for Continue to name: {labels[:3]}")
        # G1, G4: Continue, on Start only, hidden until the script fills it from saved progress
        cont = bar.select("a[data-continue]")
        if kind == "start":
            if len(cont) != 1 or not cont[0].has_attr("hidden") or "cb-step" not in (cont[0].get("class") or []) or not cont[0].find_parent(class_="cb-steps") or not cont[0].select_one("[data-continue-to]"):
                fail("G1", f"{path}: the bar has no Continue, hidden among its steps until the script fills it")
        elif cont:
            fail("G1", f"{path}: the bar offers Continue, which is Start's alone")
        # G5: the foot, one step onward: on a module its next unit, on a card its stop; none on Start, The Compass or the glossary
        foot = soup.select("main nav.unit-foot")
        if kind not in ("module", "card"):
            if foot:
                fail("G5", f"{path}: carries a foot; Start, The Compass, the concept cards and the glossary have none")
            continue
        if len(foot) != 1:
            fail("G5", f"{path}: {len(foot)} feet, not one")
            continue
        foot = foot[0]
        if "screen-only" not in (foot.get("class") or []):
            fail("G4", f"{path}: the foot isn't kept out of print")
        links = foot.find_all("a")
        if kind == "module":
            exp = (paths[i + 1], order[i + 1][1], "next")
            got = [(a.get("href"), a.get_text(" ", strip=True), " ".join(a.get("rel") or [])) for a in links]
            if got != [exp]:
                fail("G5", f"{path}: the foot holds {got}, not its next step alone, {exp}")
        else:
            mod = page(mod_path)
            stops = mod.select("li.step")
            card_step = next((n for n, li in enumerate(stops, 1) if li.select_one(f'h3 a[href="{path}"]')), None)
            back = foot.find("a", href=f"{mod_path}#step-{card_step}")
            if not card_step or not back:
                fail("G5", f"{path}: the foot doesn't go back to its step on {mod_path}'s short path")
            elif back.get_text(" ", strip=True).replace("\u2019", "'") != mod.select_one("h1").get_text(" ", strip=True).replace("\u2019", "'"):
                fail("G5", f"{path}: the foot's way back reads '{back.get_text(' ', strip=True)}', not its module's name alone")
            elif len(links) != 1:
                fail("G5", f"{path}: the foot holds {[a.get('href') for a in links]}, not the way back to its step alone")
        if not links or links[0].find_parent("p", class_="uf-step") is None:
            fail("G5", f"{path}: the foot's step isn't set as its one named step (.uf-step)")
    # G5: every stop has an address of its own, on every module
    for m, _ in MODULES:
        stops = page(m).select("li.step")
        if [li.get("id") for li in stops] != [f"step-{n}" for n in range(1, len(stops) + 1)]:
            fail("G5", f"{m}: its steps have no addresses of their own (#step-1 and on)")
    # Outside the syllabus, and in the single document, neither the bar nor the foot (G1)
    for path in [p for p in PAGES if p not in BAR_PAGES]:
        f_ = os.path.join(out_dir, path.strip("/"), "index.html")
        if os.path.exists(f_) and re.search(r'<nav class="(course-bar|unit-foot)', open(f_, encoding="utf-8").read()):
            fail("G1", f"{path} carries the bar or the foot, which are the syllabus's pages' alone, and not the single document's")
    course_bar_browser_checks(out_dir)


JS_BAR = """() => { const bar = document.querySelector('.course-bar'); if (!bar) return null;
  const r = bar.getBoundingClientRect(); const vis = e => e && e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden';
  const row = [...bar.querySelectorAll('.cb-row > *, .cb-steps > *')].filter(e => vis(e) && !e.matches('.cb-steps'));
  const menu = bar.querySelector('.cb-menu'); const mr = menu.getBoundingClientRect(); const btn = bar.querySelector('button.cb-place');
  const ms = getComputedStyle(menu);
  return {top: r.top, bottom: r.bottom, height: r.height, scrollW: bar.scrollWidth, clientW: bar.clientWidth, docW: document.documentElement.scrollWidth, winW: innerWidth, winH: innerHeight,
    tops: row.map(e => Math.round(e.getBoundingClientRect().top)), sizes: row.map(e => [e.className, e.getBoundingClientRect().width, e.getBoundingClientRect().height]),
    link: vis(bar.querySelector('a.cb-place')), btn: vis(btn), expanded: btn && btn.getAttribute('aria-expanded'), menu: vis(menu),
    menuBottom: mr.bottom, menuOverflow: ms.overflowY, menuScroll: menu.scrollHeight > menu.clientHeight + 1,
    rows: [...menu.querySelectorAll('a')].filter(vis).map(a => [a.textContent.trim().slice(0, 20), a.getBoundingClientRect().height]),
    focus: document.activeElement === btn,
    moves: [bar, menu, btn, ...bar.querySelectorAll('.cb-chev, .cb-list, .cb-item')].filter(Boolean).filter(e => { const s = getComputedStyle(e);
      const props = s.transitionProperty.split(',').map(x => x.trim()), durs = s.transitionDuration.split(',').map(parseFloat);
      // a color easing on hover, as on every link, is not motion (G2); anything else that eases or animates is
      return s.animationName !== 'none' || props.some((x, i) => durs[i % durs.length] > 0 && !/^(color|text-decoration-color|text-decoration-thickness)$/.test(x)); }).map(e => e.className) }; }"""


JS_BAND = """() => { const bar = document.querySelector('.course-bar'), head = document.querySelector('header.masthead');
  const probe = v => { const d = document.createElement('div'); d.style.color = 'var(' + v + ')'; document.body.appendChild(d); const c = getComputedStyle(d).color; d.remove(); return c; };
  const vis = e => !!e && e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden';
  const r = bar.getBoundingClientRect(), s = getComputedStyle(bar), a = getComputedStyle(bar, '::after');
  const cur = [...document.querySelectorAll('.site-nav[aria-label=Sections] a[aria-current]')].find(vis);
  const place = [...bar.querySelectorAll('.cb-place')].find(vis), word = e => e ? getComputedStyle(e) : null;
  const c = place && word(place.querySelector('.cb-course')), h = place && word(place.querySelector('.cb-here'));
  const tint = probe('--tint');
  return {bg: s.backgroundColor, tint: tint, paper: probe('--paper'), muted: probe('--muted'), ink: probe('--ink'), orange: probe('--orange'),
    left: r.left, width: r.width, top: r.top, winW: innerWidth, head: head.getBoundingClientRect().bottom,
    line: cur ? cur.getBoundingClientRect().bottom : null, rule: parseFloat(s.borderBottomWidth) ? s.borderBottomColor : '',
    course: c ? [c.color, c.fontWeight] : null, here: h ? [h.color, h.fontWeight] : null, place: place ? place.innerText : '',
    chevs: [...bar.querySelectorAll('.cb-chev')].filter(vis).length, steps: [...bar.querySelectorAll('.cb-step')].filter(vis).map(e => [...e.childNodes].filter(n => !(n.classList && n.classList.contains('sr'))).map(n => n.textContent).join('').trim()),
    fade: a.content && a.content !== 'none' && a.display !== 'none' ? {grad: a.backgroundImage.replace(/^linear-gradient\\((?:[^,]*deg, )?/, ''), h: parseFloat(a.height),
      moves: a.animationName !== 'none' || a.transitionDuration.split(',').some(x => parseFloat(x) > 0)} : null}; }"""


ON_PAGE = [("Why", "why-this-matters"), ("Short path", "short-path"), ("Do", "do"), ("Check", "check"), ("Go deeper", "go-deeper")]
DO_LINE = "The Do, on this page, below."
CHECK_STEP = ("Check yourself", "The Check, on this page, below.")
DONE_LINE = ["Its last two are the Do and the Check", "a module reads Done once you've done everything in it but the full path", "How well you did them is yours to judge"]


def doors_checks(out_dir):
    """G6 and G7 in the built pages: the concept cards' page, the pop-up's way to the glossary, where each term is
    used, a module's line of links and its headings' addresses, a game's way back to its step, and what Done means
    on Start. Then doors_browser_checks, in a browser."""
    from bs4 import BeautifulSoup
    checked("G6", "G7")
    page = lambda path: BeautifulSoup(open(os.path.join(out_dir, path.strip("/"), "index.html"), encoding="utf-8").read(), "html.parser")
    flat = lambda el: " ".join(el.get_text(" ", strip=True).replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"').split()) if el else ""
    mods = yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "modules.yaml")))
    num = {f"/pm/{m['page']}/": m["num"] for m in mods if m.get("page")}
    whole = page("/pm/all/")
    # G7: the Do and the Check are the short path's last two steps, links down the page with no minutes of their own;
    # the Do's line says what can come later where the Do asks a colleague outside its timed exercise
    for m in mods:
        if not m.get("page"):
            continue
        where = f"Module {m['num']}, {m['title']}"
        _, fm, body = open(os.path.join(ROOT, "content", "pm", m["page"] + ".md"), encoding="utf-8").read().split("---", 2)
        steps = (yaml.safe_load(fm) or {}).get("steps") or []
        kinds = [s_.get("kind") for s_ in steps]
        if kinds[-2:] != ["do", "check"] or kinds.count("do") != 1 or kinds.count("check") != 1:
            fail("G7", f"{where}: the short path's last two steps aren't the Do and then the Check, one each: {kinds}")
            continue
        soup = page(f"/pm/{m['page']}/")
        # G6: a card's step on the short path says it's a concept card
        for s_ in steps:
            li = soup.select_one(f'li.step[data-step="{m["page"]}:{s_.get("id")}"]')
            if s_.get("kind") == "card" and (not li or not flat(li.select_one(".meta-line")).endswith("A concept card, one page.")):
                fail("G6", f"{where}: the card's step '{s_.get('id')}' doesn't say \"A concept card, one page.\"")
        do_text = body.split("[//]: # (short-path)")[-1].split("\n## ")[1] if "\n## " in body.split("[//]: # (short-path)")[-1] else ""
        for s_, sec in ((steps[-2], "do"), (steps[-1], "check")):
            li = soup.select_one(f'li.step[data-step="{m["page"]}:{s_.get("id")}"]')
            line = flat(li.select_one(".meta-line")) if li else ""
            if s_.get("minutes") or "minutes" in line:
                fail("G7", f"{where}: the {sec.title()}'s step shows minutes of its own")
            if not li or not li.select_one(f'h3 a[href="#{sec}"]') or not soup.find(id=sec):
                fail("G7", f"{where}: the {sec.title()}'s step doesn't lead down the page to the {sec.title()} (#{sec})")
        if (steps[-1].get("title"), steps[-1].get("where")) != CHECK_STEP:
            fail("G7", f"{where}: the Check's step reads {(steps[-1].get('title'), steps[-1].get('where'))}, not {CHECK_STEP}")
        w_ = steps[-2].get("where") or ""
        if not w_.startswith(DO_LINE):
            fail("G7", f"{where}: the Do's step line doesn't open \"{DO_LINE}\": {w_!r}")
        asks = re.search(r"\b(outside|after) the \d+ minutes\b", do_text.split("**Optional")[0], re.I) is not None
        if asks != ("can come later" in w_):
            fail("G7", f"{where}: the Do {'asks a colleague outside its timed exercise' if asks else 'asks nobody outside its time'}, and its step's line {'does' if not asks else 'does not'} say what can come later: {w_!r}")
    # G6: the concept cards' page lists every card by module, in the map's order, with its question to carry
    idx = page(CARDS_INDEX)
    secs = idx.select("main section.ci-module")
    want = [(m, cards) for m, cards in MODULES if cards]
    if [s_.select_one("h2 a").get("href") if s_.select_one("h2 a") else None for s_ in secs] != [m for m, _ in want]:
        fail("G6", f"{CARDS_INDEX}: its modules are {[s_.select_one('h2 a').get('href') if s_.select_one('h2 a') else None for s_ in secs]}, not every module with a card, in the map's order")
    for sec, (m, cards) in zip(secs, want):
        mod = page(m)
        head = f"Module {num.get(m)}, {flat(mod.select_one('h1'))}"
        if flat(sec.select_one("h2")) != head:
            fail("G6", f"{CARDS_INDEX}: a module reads '{flat(sec.select_one('h2'))}', not '{head}'")
        items = sec.select("ul.ci-list > li")
        if [li.select_one("h3 a").get("href") if li.select_one("h3 a") else None for li in items] != cards:
            fail("G6", f"{CARDS_INDEX}: under {m} it lists {[li.select_one('h3 a').get('href') if li.select_one('h3 a') else None for li in items]}, not {cards}")
            continue
        for li, c in zip(items, cards):
            card = page(c)
            if flat(li.select_one("h3")) != flat(card.select_one("h1")):
                fail("G6", f"{CARDS_INDEX}: {c} is listed as '{flat(li.select_one('h3'))}', not its title")
            carry = card.select_one(".carry mark")
            if not carry or flat(li.select_one(".ci-question")) != flat(carry):
                fail("G6", f"{CARDS_INDEX}: {c}'s question to carry isn't beneath its title, word for word")
    if idx.select("main nav.unit-foot") or idx.select("main [data-slot]"):
        fail("G6", f"{CARDS_INDEX}: carries a foot or margin slots, which are a unit's")
    if whole.select(".cards-index"):
        fail("G6", "the single document carries the concept cards' page, which is the site's alone")
    # G6: from Start and from each card, plain links to the lists a reader without scripts can't reach by the bar
    start = page("/pm/")
    more = start.select("main section.modules-wrap nav.start-more")
    if len(more) != 1 or [a.get("href") for a in more[0].select("a")] != [CARDS_INDEX, "/pm/glossary/"] or more[0].get("aria-label") != "Look up" or "screen-only" not in (more[0].get("class") or []):
        fail("G6", "Start's list of modules doesn't end with 'Look up', plain links to the concept cards and the glossary")
    elif more[0].find_previous_sibling() is None or more[0].find_next_sibling() is not None:
        fail("G6", "Start's 'Look up' line isn't the last thing under its list of modules")
    for c in [c for _, cards in MODULES for c in cards]:
        tag = page(c).select_one("main .kicker .tag")
        if not tag or tag.name != "a" or tag.get("href") != CARDS_INDEX or flat(tag) != "Concept card":
            fail("G6", f"{c}: its label 'Concept card' doesn't link to the concept cards' page")
            break
    if whole.select(f'a[href="{CARDS_INDEX}"], nav.start-more'):
        fail("G6", "the single document links the concept cards' page, which isn't in it (P5)")
    # G6: each term's pop-up ends with its way to the glossary; in the single document, to the entry in it (P5)
    gl = yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "glossary.yaml")))
    for path, soup in (("/pm/find-the-constraint/", page("/pm/find-the-constraint/")), ("/pm/glossary/", page("/pm/glossary/")), ("/pm/all/", whole)):
        dlgs = soup.select("dialog.gloss")
        for d in dlgs:
            key = d.get("id", "")[len("term-"):]
            a = d.select("a.gloss-more")
            exp = f"#g-{key}" if path == "/pm/all/" else f"/pm/glossary/#g-{key}"
            if len(a) != 1 or a[0].get("href") != exp or flat(a[0]) != "In the glossary":
                fail("G6", f"{path}: the pop-up for '{key}' has no 'In the glossary' link to {exp}")
                break
        if len(dlgs) != len(gl):
            fail("G6", f"{path}: {len(dlgs)} pop-ups for {len(gl)} terms")
    # G6: where each term is used, in the map's order, a module before its cards, on the glossary page alone
    order = ["/pm/"] + UNIT_PAGES
    used = {}
    for path in order:
        for a in page(path).select("main a.term[data-term]"):
            used.setdefault(a["data-term"], [])
            if path not in used[a["data-term"]]:
                used[a["data-term"]].append(path)
    gloss = page("/pm/glossary/")
    for d in gloss.select("dl.gloss-list > div"):
        key = d.get("id", "")[2:]
        u = d.select("dd.gloss-used")
        got = [a.get("href") for a in u[0].select("a")] if u else []
        want = [f"{p_}#use-{key}" for p_ in used.get(key, [])]
        if got != want:
            fail("G6", f"/pm/glossary/: '{key}' says it's used in {got}, not {want}")
        elif u and (not flat(u[0]).startswith("Used in ") or "screen-only" not in (u[0].get("class") or [])):
            fail("G6", f"/pm/glossary/: '{key}''s line of where it's used doesn't open 'Used in', or prints")
    # G6: each "Used in" lands on the term where its unit first marks it, an address on the unit's page alone
    for path in order:
        terms = page(path).select("main a.term[data-term]")
        first = {}
        for a in terms:
            first.setdefault(a["data-term"], a)
        for key, a in first.items():
            if a.get("id") != f"use-{key}":
                fail("G6", f"{path}: the first marked use of '{key}' has no address #use-{key}, so \"Used in\" can't land on it"); break
        if any(a.get("id") for a in terms if first.get(a["data-term"]) is not a):
            fail("G6", f"{path}: a later use of a term carries the address of its first")
    if whole.select('a.term[id^="use-"]'):
        fail("G6", "the single document gives its terms the addresses of a unit's page, which repeat in it")
    # G6: finding a term by name: an A to Z rail of all 26 letters, a heading over each letter's terms
    az = gloss.select("main nav.az")
    letters = sorted({str(v["term"])[0].upper() for v in gl.values()})
    if len(az) != 1 or az[0].get("aria-label") != "A to Z":
        fail("G6", "/pm/glossary/: no A to Z rail, a nav named \"A to Z\"")
    else:
        items = az[0].select("li")
        links = {flat(a): a.get("href") for a in az[0].select("li > a")}
        plain = [flat(sp) for sp in az[0].select("li > span")]
        if [flat(li) for li in items] != list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            fail("G6", f"/pm/glossary/: the A to Z rail doesn't hold the 26 letters in order: {[flat(li) for li in items]}")
        if sorted(links) != letters or sorted(plain) != sorted(set("ABCDEFGHIJKLMNOPQRSTUVWXYZ") - set(letters)):
            fail("G6", f"/pm/glossary/: the A to Z rail links {sorted(links)}, and only letters with terms should link: {letters}")
        for l_, href in links.items():
            grp = gloss.select_one(f"section.gloss-group{href}")
            h = grp.select_one("h2") if grp else None
            if not grp or not h or flat(h) != l_ or any(flat(dt)[0].upper() != l_ for dt in grp.select("dt")):
                fail("G6", f"/pm/glossary/: the letter {l_} doesn't lead to its heading over its own terms"); break
    if whole.select("nav.az, .gloss-group"):
        fail("G6", "the single document carries the glossary's A to Z rail or its letters, which are the site's alone")
    if whole.select(".gloss-used"):
        fail("G6", "the single document says where each term is used, which is the site's alone")
    # G7: a module's line of links, under its header, to parts that each have an address
    for m, _ in MODULES:
        soup = page(m)
        body = soup.select_one("main .unit-body")
        nav = soup.select("main nav.on-page")
        first = next((c for c in body.children if getattr(c, "name", None)), None) if body else None
        if len(nav) != 1 or nav[0] is not first:
            fail("G7", f"{m}: no line of links ('On this page') first in the module's body")
            continue
        nav = nav[0]
        if nav.get("aria-label") != "On this page" or "screen-only" not in (nav.get("class") or []) or flat(nav.select_one(".op-label")) != "On this page":
            fail("G7", f"{m}: the line of links isn't a landmark named 'On this page', labeled and kept out of print")
        got = [(flat(a), a.get("href", "")) for a in nav.select("a")]
        exp = [(w, "#" + t) for w, t in ON_PAGE]
        if got != exp:
            fail("G7", f"{m}: the line of links reads {got}, not {exp}")
        for _, h in got:
            el = soup.find(id=h[1:])
            if not el or el.name != "h2":
                fail("G7", f"{m}: the line's link {h} lands on no section heading")
        # G7: every heading has an address: its own, or for a game's, its section's
        for h in soup.select("main h2, main .prose h3"):
            if h.find_parent(class_="print-only"):
                continue
            sec = h.find_parent("section")
            if not h.get("id") and not (h.name == "h2" and sec and sec.get("id") and sec.find("h2") is h):
                fail("G7", f"{m}: the heading '{flat(h)[:40]}' has no address")
        # G7: a game ends with its way back to its own step
        game = soup.select_one("main section.game[id]")
        back = soup.select("main p.game-back a")
        if game:
            step = next((n for n, li in enumerate(soup.select("li.step"), 1) if li.select_one(f'h3 a[href="#{game["id"]}"]')), None)
            if not step or len(back) != 1 or back[0].get("href") != f"#step-{step}" or flat(back[0]) != "Back to the short path":
                fail("G7", f"{m}: the game doesn't end with 'Back to the short path' to its own step (#step-{step})")
            elif "screen-only" not in (back[0].find_parent("p").get("class") or []) or back[0].find_previous("section", class_="game") is not game:
                fail("G7", f"{m}: the game's way back prints, or doesn't follow the game")
        elif back:
            fail("G7", f"{m}: a way back from a game it doesn't have")
        if not soup.select_one("main section.path p.progress[data-progress]"):
            fail("G7", f"{m}: the short path has no place for its count")
    if whole.select("nav.on-page, .game-back"):
        fail("G7", "the single document carries a module's line of links or a game's way back, which are the site's alone")
    # G7: Start says what Done means
    said = flat(page("/pm/").select_one("main .prose"))
    for w in DONE_LINE:
        if w not in said:
            fail("G7", f"Start's How it works doesn't say what Done means ('{w}')")
    doors_browser_checks(out_dir)


def doors_browser_checks(out_dir):
    """G6 and G7 in a browser: the entry a link lands on is marked, the pop-up keeps focus as it gains a link, a
    finished round ticks its step and counts it, "Go deeper" opens the full path, the line's addresses land below
    the bar, and a phone's targets are 44 pixels tall."""
    chrome = os.environ.get("CHROME")
    srv = Server(out_dir)
    mod = "/pm/find-the-constraint/"
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=chrome) if chrome else p.chromium.launch()
            # G7: on hover and keyboard focus a step's number gives way to a faint check, easing as a link's color does,
            # and at once for a reader who asks for less motion (D5)
            probe = """() => { const m = document.querySelector('.step .tick-mark'), st = e => getComputedStyle(e);
              return {num: +st(m.querySelector('.tick-num')).opacity, check: +st(m.querySelector('.tick-check')).opacity,
                      ease: st(m.querySelector('.tick-check')).transitionDuration, ticked: m.previousElementSibling.checked}; }"""
            for motion in ("no-preference", "reduce"):
                ctx = b.new_context(viewport={"width": 1280, "height": 900}, reduced_motion=motion); pg = ctx.new_page()
                pg.goto(srv.base + mod); pg.wait_for_load_state("load"); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_load_state("load")
                rest = pg.evaluate(probe)
                pg.hover(".step .tick"); pg.wait_for_timeout(400)
                hover = pg.evaluate(probe)
                pg.mouse.move(0, 0); pg.locator(".step .tick input").first.focus(); pg.keyboard.press("Shift+Tab"); pg.keyboard.press("Tab"); pg.wait_for_timeout(400)
                focus = pg.evaluate(probe)
                ease = "0s" if motion == "reduce" else "0.18s"
                if not (rest["num"] == 1 and rest["check"] == 0 and hover["num"] == 0 and 0 < hover["check"] and focus["num"] == 0 and focus["check"] > 0 and not hover["ticked"] and rest["ease"] == ease):
                    fail("G7" if motion != "reduce" else "D5", f"{mod}, {motion} motion: a step's number should give way to a faint check on hover and focus, easing over {ease}: rest {rest}, hover {hover}, focus {focus}")
                ctx.close()
            ctx = b.new_context(viewport={"width": 390, "height": 844}, reduced_motion="reduce"); pg = ctx.new_page()
            # G6: the entry a link lands on carries the orange line under its term; the others don't
            pg.goto(srv.base + "/pm/glossary/#g-constraint"); pg.wait_for_load_state("load")
            r = pg.evaluate("""() => { const st = e => getComputedStyle(e); const t = document.querySelector('#g-constraint dt'), o = document.querySelector('#g-wip dt');
              const orange = getComputedStyle(document.documentElement).getPropertyValue('--orange').trim();
              const probe = document.createElement('i'); probe.style.color = orange; document.body.append(probe); const want = st(probe).color; probe.remove();
              return {on: st(t).textDecorationLine.includes('underline') && st(t).textDecorationColor === want, off: st(o).textDecorationLine.includes('underline')}; }""")
            if not r["on"] or r["off"]:
                fail("G6", f"/pm/glossary/#g-constraint: the entry landed on isn't marked with the orange line under its term, or another is: {r}")
            # G6: the pop-up's way to the glossary, reached by Tab, and focus stays inside
            pg.goto(srv.base + mod); pg.wait_for_load_state("load")
            pg.locator("a.term").first.click()
            seen = []
            for _ in range(4):
                pg.keyboard.press("Tab")
                seen.append(pg.evaluate("() => { const a = document.activeElement; return a === document.body ? 'browser' : (a.closest('dialog[open]') ? 'in:' : 'out:') + (a.className || a.tagName); }"))  # the browser's own step, as for every modal (A5)
            if not any("gloss-more" in x for x in seen) or any(x.startswith("out:") for x in seen):
                fail("G6", f"{mod}: Tab in a term's pop-up doesn't reach 'In the glossary', or leaves the pop-up: {seen}")
            pg.keyboard.press("Escape")
            # G7: a finished round ticks the game's step and counts it; its way back lands on that step
            pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_load_state("load")
            n = pg.locator(".step").count()
            pg.click("#dice-game [data-play]"); pg.wait_for_timeout(200)
            r = pg.evaluate("() => ({tick: document.querySelector('#step-1 input').checked, said: document.querySelector('[data-progress]').textContent.trim(), kept: Object.keys(localStorage).filter(k => k.startsWith('pm:find-the-constraint:')).length, told: (document.querySelector('.game-back [role=status][data-ticked]') || {}).textContent})")
            if not r["tick"] or r["kept"] != 1 or r["said"] != f"1 of {n} steps done.":
                fail("G7", f"{mod}: a finished round of the dice game doesn't tick and count its step: {r}")
            if r["told"] != "Its step on the short path is ticked.":
                fail("G7", f"{mod}: a finished round doesn't say, beside the way back, that its step is ticked: {r['told']!r}")
            # G7: the way back goes on to the first step still waiting after the game's: the next step, then the Do,
            # then the Check, and with every step ticked the game's own step
            back = "() => { const a = document.querySelector('.game-back a'); return [a.textContent.trim(), a.getAttribute('href')]; }"
            seen = [pg.evaluate(back)]
            for k in range(1, n - 2):
                pg.locator(".step .tick").nth(k).click()
            seen.append(pg.evaluate(back))
            pg.locator(".step .tick").nth(n - 2).click(); seen.append(pg.evaluate(back))
            pg.locator(".step .tick").nth(n - 1).click(); seen.append(pg.evaluate(back))
            want = [["Back to the short path", "#step-2"], ["Next: Do", "#do"], ["Next: Check", "#check"], ["Back to the short path", "#step-1"]]
            if seen != want:
                fail("G7", f"{mod}: after a round, the game's way back reads {seen}, not {want}")
            pg.evaluate("localStorage.clear()")
            # G7: a step's tick is 44 pixels to tap on a phone
            sz = pg.evaluate("() => { const r = document.querySelector('.step .tick input').getBoundingClientRect(); return [r.width, r.height]; }")
            if min(sz) < 43.5:
                fail("G7", f"{mod} at 390px: a step's tick is {sz[0]:.0f} by {sz[1]:.0f} to tap, not 44 by 44")
            # G7: in print, where the Do and the Check follow, their steps are left out
            pg.emulate_media(media="print")
            shown = pg.evaluate("() => [...document.querySelectorAll('li.step')].filter(e => e.getClientRects().length).map(e => e.querySelector('h3 a') ? e.querySelector('h3 a').getAttribute('href') : '')")
            pg.emulate_media(media="screen")
            if len(shown) != n - 2 or any(h in ("#do", "#check") for h in shown):
                fail("G7", f"{mod}: in print the short path shows {shown}, and should leave out the Do's and the Check's steps")
            # G7: the line's addresses land below the bar, and "Go deeper" opens the full path
            for w, t in ON_PAGE:
                pg.goto(srv.base + mod); pg.wait_for_load_state("load")
                pg.locator("nav.on-page a", has_text=w).first.click(); pg.wait_for_timeout(100)
                gap = pg.evaluate("(t) => { const e = document.getElementById(t); const b = document.querySelector('.course-bar'); return e && b ? e.getBoundingClientRect().top - b.getBoundingClientRect().bottom : null; }", t)
                if gap is None or gap < 0:
                    fail("G7", f"{mod}: '{w}' lands its heading under the bar ({gap})")
            if not pg.evaluate("() => document.querySelector('.deeper details').open"):
                fail("G7", f"{mod}: 'Go deeper' doesn't open the full path it lands on")
            # G7: a phone's targets: the line's links, a card's way to its module and each "Why this source"
            pg.goto(srv.base + mod); pg.wait_for_load_state("load")
            hs = pg.evaluate("() => [...document.querySelectorAll('nav.on-page a, .game-back a, details.why > summary')].filter(e => e.getClientRects().length).map(e => [e.textContent.trim().slice(0, 20), e.getBoundingClientRect().height])")
            pg.goto(srv.base + MODULES[3][1][0]); pg.wait_for_load_state("load")
            hs += pg.evaluate("() => [...document.querySelectorAll('.kicker a, .unit-foot a')].map(e => [e.textContent.trim().slice(0, 20), e.getBoundingClientRect().height])")
            # each "What a good one looks like" (J7), on every module that has one
            for m_, _ in MODULES:
                built = os.path.join(out_dir, m_.strip("/"), "index.html")
                if os.path.exists(built) and 'class="example' in open(built, encoding="utf-8").read():
                    pg.goto(srv.base + m_); pg.wait_for_load_state("load")
                    # where it waits for the Do's tick, tick it first, as a reader would
                    if pg.evaluate("() => { const d = document.querySelector('details.example[data-gate]'); if (d) localStorage.setItem('pm:' + d.dataset.gate, '1'); return !!d; }"):
                        pg.reload(); pg.wait_for_load_state("load")
                    hs += pg.evaluate("() => [...document.querySelectorAll('details.example > summary')].map(e => [e.textContent.trim().slice(0, 20), e.getBoundingClientRect().height])")
            short = [x for x in hs if x[1] < 43.5]
            if short or len(hs) < 8:
                fail("G7", f"at 390px, targets under 44 pixels tall: {short[:4]}")
            ctx.close()
            # G7, G4: without scripts the line and the way back are plain links that land
            ctx = b.new_context(viewport={"width": 390, "height": 844}, java_script_enabled=False); pg = ctx.new_page()
            pg.goto(srv.base + mod + "#check"); pg.wait_for_load_state("load")
            vis = pg.evaluate("() => [...document.querySelectorAll('nav.on-page a, .game-back a')].filter(e => e.getClientRects().length).length")
            if vis != len(ON_PAGE) + 1:
                fail("G7", f"{mod}: without scripts the line of links and the game's way back don't all show ({vis})")
            ctx.close()
            b.close()
    finally:
        srv.close()


def course_bar_browser_checks(out_dir):
    """G1 to G4 in a browser: the bar stays in view, keeps to one line and to the page, opens and closes as a
    disclosure should, shows saved progress, never covers what an address lands on, and without scripts is plain
    links; neither it nor the foot prints. On Start, Continue goes where saved progress says."""
    checked("G3")
    chrome = os.environ.get("CHROME")
    mods, order = _course_order(out_dir)
    paths = [p_ for p_, _ in order]
    cards_of = {c: m for m, cards in MODULES for c in cards}
    srv = Server(out_dir)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=chrome) if chrome else p.chromium.launch()
            for path in BAR_BROWSER_PAGES:
                kind = _bar_kind(path, cards_of)
                at = cards_of.get(path, path)
                i = paths.index(at) if at in paths and kind != "card" else None
                words = (["Previous"] if i else []) + (["Next"] if i is not None and i + 1 < len(paths) else [])
                for w, h in ((390, 844), (1280, 900)):
                    ctx = b.new_context(viewport={"width": w, "height": h})
                    pg = ctx.new_page()
                    pg.goto(srv.base + path); pg.wait_for_load_state("load"); pg.evaluate("document.fonts.ready")
                    where = f"{path} at {w}px"
                    r = pg.evaluate(JS_BAR)
                    if not r:
                        fail("G1", f"{where}: no course bar"); ctx.close(); continue
                    if not r["btn"] or r["link"]:
                        fail("G2", f"{where}: with the script the place should be its button, and the plain link gone")
                    if max(r["tops"]) - min(r["tops"]) > 2 or r["height"] > 44.5:
                        fail("G3", f"{where}: the bar takes more than one line ({r['height']:.0f}px tall)")
                    if r["scrollW"] > r["clientW"] + 1:
                        fail("G3", f"{where}: something in the bar runs past the page's edge")
                    if w == 390:
                        for cls, tw, th in r["sizes"]:
                            if tw < 43.5 or th < 43.5:
                                fail("G2", f"{where}: the bar's {cls} is {tw:.0f} by {th:.0f}, under 44 by 44")
                    # G1: it stays in view as the page scrolls
                    for y in ("document.body.scrollHeight / 2", "document.body.scrollHeight"):
                        pg.evaluate(f"window.scrollTo(0, {y})")
                        r = pg.evaluate(JS_BAR)
                        if abs(r["top"]) > 1:
                            fail("G1", f"{where}: scrolled down, the bar is at {r['top']:.0f}px, not in view at the top")
                    # G1: the band, its words, its steps and its fade (the owner's cards bar-tie, bar-arrows, band-edge)
                    pg.evaluate("window.scrollTo(0, 0)"); pg.wait_for_timeout(100)
                    k = pg.evaluate(JS_BAND)
                    if k["bg"] != k["tint"] or abs(k["left"]) > 0.5 or abs(k["width"] - k["winW"]) > 0.5:
                        fail("G1", f"{where}: the bar isn't a band on the page's tint across the window ({k['bg']}, {k['left']:.0f} to {k['left'] + k['width']:.0f})")
                    if k["line"] is None or abs(k["line"] - k["top"]) > 1 or abs(k["head"] - k["top"]) > 1:
                        fail("G1", f"{where}: the menu's orange line doesn't rest on the band's top edge (line {k['line']}, header {k['head']}, band {k['top']})")
                    if k["course"] != [k["muted"], "400"] or k["here"] != [k["ink"], "600"]:
                        fail("G1", f"{where}: the bar's words aren't the course in the menu's grey and the place in bold ink: {k['course']}, {k['here']}")
                    if k["rule"]:
                        fail("G1", f"{where}: the band draws a rule under it ({k['rule']}); the band is the surface")
                    if k["chevs"] != 1:
                        fail("G1", f"{where}: the bar shows {k['chevs']} chevrons, not one")
                    if w < 736 and (k["steps"] or (kind in ("module", "card") and "Module" not in k["place"])):
                        fail("G1", f"{where}: on a phone the bar should be its place alone, \"Module\" spelled out: {k['steps']}, '{k['place']}'")
                    if w >= 736 and k["steps"] != words:
                        fail("G1", f"{where}: from 46rem up the bar's steps should read {words}: {k['steps']}")
                    if k["fade"]:
                        fail("G1", f"{where}: at rest, before it sticks, the bar shows its fade")
                    pg.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)"); pg.wait_for_timeout(150)
                    k = pg.evaluate(JS_BAND)
                    if not k["fade"] or not k["fade"]["grad"].startswith(k["paper"]) or not 14 <= k["fade"]["h"] <= 28:
                        fail("G1", f"{where}: stuck at the top, the bar should fade the text under it into the page's paper over about 20px: {k['fade']}")
                    elif k["fade"]["moves"]:
                        fail("G2", f"{where}: the fade under the stuck bar eases in or out; it appears and goes at once")
                    pg.evaluate("window.scrollTo(0, 0)"); pg.wait_for_timeout(150)
                    # G1: the place turns orange on hover, as previous and next do (the owner, 25 November 2026)
                    color = "(s) => getComputedStyle(document.querySelector(s)).color"
                    rest = [pg.evaluate(color, "button.cb-place"), pg.evaluate(color, "button.cb-place .cb-course")]
                    pg.hover("button.cb-place"); pg.wait_for_timeout(300)
                    over = [pg.evaluate(color, "button.cb-place"), pg.evaluate(color, "button.cb-place .cb-course")]
                    pg.mouse.move(w // 2, h - 20)
                    if over != [k["orange"], k["orange"]] or rest[0] == over[0]:
                        fail("G1", f"{where}: the bar's place is {over} on hover, not orange as previous and next are ({k['orange']})")
                    # G2: Enter opens, Escape closes and gives focus back; a click outside closes
                    pg.focus("button.cb-place"); pg.keyboard.press("Enter")
                    r = pg.evaluate(JS_BAR)
                    if r["expanded"] != "true" or not r["menu"]:
                        fail("G2", f"{where}: Enter on the bar's button doesn't open its list")
                    if r["moves"]:
                        fail("G2", f"{where}: parts of the bar move on their own: {r['moves']}")
                    if r["menuBottom"] > r["winH"] + 1:
                        fail("G3", f"{where}: the open list runs past the window's foot")
                    if w == 390:
                        for name, th in r["rows"]:
                            if th < 43.5:
                                fail("G2", f"{where}: '{name}' in the bar's list is {th:.0f}px tall, under 44")
                    pg.keyboard.press("Tab"); pg.keyboard.press("Escape")
                    r = pg.evaluate(JS_BAR)
                    if r["expanded"] != "false" or r["menu"] or not r["focus"]:
                        fail("G2", f"{where}: Escape doesn't close the bar's list and give focus back to its button")
                    pg.keyboard.press(" ")
                    if pg.evaluate(JS_BAR)["expanded"] != "true":
                        fail("G2", f"{where}: Space on the bar's button doesn't open its list")
                    # a click outside: outside the bar and its open list, on a spot with nothing to tap under it, so the
                    # click can't follow a link (thirteen modules make the list reach the window's foot on a phone)
                    cx, cy = pg.evaluate("""([w, h]) => { for (let y = h - 20; y > 0; y -= 10) for (const x of [w / 2, 8, w - 8, w / 4, 3 * w / 4]) {
                        const e = document.elementFromPoint(x, y); if (e && !e.closest('a, button, summary, label, input, nav, .course-bar, .cb-menu')) return [x, y]; }
                        return [w / 2, h - 20]; }""", [w, h])
                    pg.mouse.click(cx, cy)
                    if pg.evaluate(JS_BAR)["menu"]:
                        fail("G2", f"{where}: a click outside the bar leaves its list open")
                    ctx.close()
                # G3: a short window, a narrow one and enlarged text
                for kw, what in (({"viewport": {"width": 390, "height": 420}}, "a short window"), ({"viewport": {"width": 320, "height": 700}}, "320px")):
                    ctx = b.new_context(**kw); pg = ctx.new_page(); pg.goto(srv.base + path); pg.wait_for_load_state("load")
                    pg.click("button.cb-place")
                    r = pg.evaluate(JS_BAR)
                    if r["scrollW"] > r["clientW"] + 1 or r["docW"] > r["winW"]:
                        fail("G3", f"{path} in {what}: the bar runs past the page's edge")
                    if r["menuBottom"] > r["winH"] + 1 or (r["menuScroll"] and r["menuOverflow"] not in ("auto", "scroll")):
                        fail("G3", f"{path} in {what}: the open list doesn't fit the window or scroll inside itself")
                    ctx.close()
                big = b.new_context(viewport={"width": 390, "height": 844}); pg = big.new_page()
                pg.goto(srv.base + path); pg.wait_for_load_state("load")
                pg.add_style_tag(content="html { font-size: 32px !important; }")
                r = pg.evaluate(JS_BAR)
                if r["scrollW"] > r["clientW"] + 1 or r["docW"] > r["winW"]:
                    fail("G3", f"{path} with enlarged text: the bar runs past the page's edge rather than wrap")
                big.close()
                # G2: what an address lands on sits below the bar
                ctx = b.new_context(viewport={"width": 390, "height": 844}); pg = ctx.new_page()
                targets = ["#step-3", "#do"] if path in dict(MODULES) else []
                for t in targets:
                    pg.goto(srv.base + path + t); pg.wait_for_load_state("load"); pg.wait_for_timeout(100)
                    gap = pg.evaluate("(t) => { const e = document.querySelector(t); const b = document.querySelector('.course-bar'); return e && b ? e.getBoundingClientRect().top - b.getBoundingClientRect().bottom : null; }", t)
                    if gap is None or gap < 0:
                        fail("G2", f"{path}{t}: what the address lands on sits under the bar ({gap})")
                # G1: saved progress shows in the list
                if path in dict(MODULES):
                    pg.goto(srv.base + path); pg.wait_for_load_state("load")
                    pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_load_state("load")
                    n = pg.locator(".step").count()
                    said = pg.evaluate("() => document.querySelector('[data-progress]').textContent.trim()")
                    if said != f"{n} steps. Tap a step's number to tick it off.":
                        fail("G5", f"{path}: above the short path, '{said}', not '{n} steps. Tap a step's number to tick it off.'")
                    pg.locator(".step .tick").first.click()
                    status = pg.evaluate(f"() => document.querySelector('.cb-list [data-map-unit=\"{path.strip('/').split('/')[-1]}\"] [data-map-status]').textContent.trim()")
                    said = pg.evaluate("() => document.querySelector('[data-progress]').textContent.trim()")
                    if status != f"1 of {n} steps":
                        fail("G1", f"{path}: one step ticked, the bar's list says '{status}', not '1 of {n} steps'")
                    if said != f"1 of {n} steps done.":
                        fail("G5", f"{path}: one step ticked, above the short path, '{said}', not '1 of {n} steps done.'")
                    for k in range(1, n):
                        pg.locator(".step .tick").nth(k).click()
                    status = pg.evaluate(f"() => document.querySelector('.cb-list [data-map-unit=\"{path.strip('/').split('/')[-1]}\"] [data-map-status]').textContent.trim()")
                    if status != "Done":
                        fail("G1", f"{path}: every step ticked, the bar's list says '{status}', not 'Done'")
                    pg.evaluate("localStorage.clear()")
                # G4: in print neither the bar nor the foot shows
                pg.emulate_media(media="print")
                shown = pg.evaluate("() => [...document.querySelectorAll('.course-bar, .unit-foot')].filter(e => e.getClientRects().length).map(e => e.className)")
                if shown:
                    fail("G4", f"{path}: {shown} shows in print")
                ctx.close()
                # G4: without scripts, plain links: the place, and from 46rem up previous and next
                for w in (390, 1280):
                    ctx = b.new_context(viewport={"width": w, "height": 844}, java_script_enabled=False); pg = ctx.new_page()
                    pg.goto(srv.base + path); pg.wait_for_load_state("load")
                    r = pg.evaluate("""() => { const vis = e => !!e && e.getClientRects().length > 0; const bar = document.querySelector('.course-bar');
                      return {links: [...bar.querySelectorAll('a')].filter(vis).map(a => a.getAttribute('href')), btn: vis(bar.querySelector('button')), menu: vis(bar.querySelector('.cb-menu')), chevs: [...bar.querySelectorAll('.cb-chev')].filter(vis).length}; }""")
                    if r["btn"] or r["menu"] or r["chevs"] or not r["links"] or r["links"][0] != "/pm/#modules" or len(r["links"]) != (1 if w < 736 else 1 + len(words)):
                        fail("G4", f"{path} at {w}px: without scripts the bar should be plain links, its place to Start's list, with previous and next from 46rem up: {r}")
                    ctx.close()
            # G1: Start's Continue goes where the reader left off, at every width, in place of Next
            built = [m["page"] for m in mods if m.get("page")]
            label = dict(order)
            # in a module started, Continue lands on its next unticked step; one not yet started opens at its top
            cases = [({built[2]: "part", built[5]: "part", built[0]: "done"}, f"/pm/{built[2]}/#step-2", "the first module started and not done"),
                     ({built[0]: "done", built[1]: "gap"}, f"/pm/{built[1]}/#step-3", "a module with its third step unticked and the rest ticked"),
                     ({built[0]: "done", built[1]: "done"}, f"/pm/{built[2]}/", "the module after the last one done"),
                     ({built[3]: "done"}, f"/pm/{built[4]}/", "the first not done after the furthest one done"),
                     ({built[-1]: "done"}, f"/pm/{built[0]}/", "the first not done, when none follows the one done"),
                     ({m_: "done" for m_ in built}, CLOSING, "The Compass, every module done")]
            for w, h in ((390, 844), (1280, 900)):
                ctx = b.new_context(viewport={"width": w, "height": h}); pg = ctx.new_page()
                pg.goto(srv.base + "/pm/"); pg.wait_for_load_state("load")
                for plan, exp, what in (cases if w == 390 else cases[:1]):
                    pg.evaluate(JS_SAVE, plan); pg.reload(); pg.wait_for_load_state("load"); pg.evaluate("document.fonts.ready")
                    c = pg.evaluate(JS_CONTINUE)
                    if c["steps"] != ["Continue"] or c["href"] != exp or c["sr"] != f"Continue: {label[exp.split('#')[0]]}":
                        fail("G1", f"/pm/ at {w}px, with {what} saved: the bar's steps are {c['steps']}, Continue to {c['href']} ('{c['sr']}'), not Continue alone to {exp} ('Continue: {label[exp.split('#')[0]]}')")
                    if w == 390 and plan.get(built[2]) == "part":
                        said = pg.evaluate("(u) => { const li = document.querySelector('main [data-map-unit=\"' + u + '\"]'); return [li.querySelector('[data-map-status]').textContent.trim(), +li.getAttribute('data-map-steps')]; }", built[2])
                        if said[0] != f"Started: 1 of {said[1]} steps done.":
                            fail("G5", f"/pm/ with one step of {built[2]} ticked: Start's list says '{said[0]}', not 'Started: 1 of {said[1]} steps done.'")
                    if w == 390 and (c["height"] > 44.5 or c["size"][0] < 43.5 or c["size"][1] < 43.5):
                        fail("G3", f"/pm/ at {w}px with Continue: the bar is {c['height']:.0f}px tall, Continue {c['size'][0]:.0f} by {c['size'][1]:.0f}; one line, and 44 by 44")
                pg.evaluate("localStorage.clear()")
                ctx.close()
            b.close()
    finally:
        srv.close()


JS_SAVE = """(plan) => { localStorage.clear(); for (const [unit, how] of Object.entries(plan)) {
  const li = document.querySelector('.cb-list [data-map-unit="' + unit + '"]'); const ids = li.getAttribute('data-map-ids').split(' ').filter(Boolean);
  (how === 'done' ? ids : how === 'gap' ? ids.slice(0, 2).concat(ids.slice(3)) : ids.slice(0, 1)).forEach(id => localStorage.setItem('pm:' + unit + ':' + id, '1')); } }"""
JS_CONTINUE = """() => { const vis = e => !!e && e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden';
  const bar = document.querySelector('.course-bar'), c = bar.querySelector('[data-continue]'), r = c.getBoundingClientRect();
  return {steps: [...bar.querySelectorAll('.cb-step')].filter(vis).map(e => [...e.childNodes].filter(n => !(n.classList && n.classList.contains('sr'))).map(n => n.textContent).join('').trim()),
    href: vis(c) ? c.getAttribute('href') : null, sr: c.textContent.trim(), height: bar.getBoundingClientRect().height, size: [r.width, r.height]}; }"""


# ---------- the site's menu (R9) ----------
MENU_WIDE = 736   # 46rem: from here up the name and every section share one line; below it, a Menu button (R9)
JS_MENU = """() => { const nav = document.querySelector('nav.site-nav[aria-label=Sections]'); if (!nav) return null;
  const vis = e => !!e && e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden';
  const box = e => { const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom]; };
  const name = document.querySelector('.site-name'), here = nav.querySelector('.nav-here'), btn = nav.querySelector('.nav-open'), list = nav.querySelector('.nav-list');
  const links = [...list.querySelectorAll('a')];
  return {name: box(name), here: vis(here) ? box(here) : null, hereLine: vis(here) ? getComputedStyle(here).borderBottomColor : null,
    btn: vis(btn) ? box(btn) : null, expanded: btn && btn.getAttribute('aria-expanded'), list: vis(list) ? box(list) : null,
    links: links.filter(vis).map(a => { const g = document.createRange(); g.selectNodeContents(a); return [a.textContent.trim(), ...box(a), g.getBoundingClientRect().left]; }), focus: document.activeElement === btn,
    winH: innerHeight, docW: document.documentElement.scrollWidth, winW: innerWidth}; }"""


def site_menu_checks(out_dir):
    """R9: the menu's label, its markup on every page, and in a browser its one line from 46rem up, and below it the
    current section beside a Menu button whose list opens, stays open and closes as the spec says."""
    from bs4 import BeautifulSoup
    checked("R9")
    cfg = yaml.safe_load(open(os.path.join(ROOT, "hugo.yaml"), encoding="utf-8"))
    items = (cfg.get("menu") or {}).get("main") or []
    pm_item = next((i for i in items if i.get("url") == "/pm/"), None)
    if not pm_item or pm_item.get("name") != "On Judgment":
        fail("R9", f"the menu calls the syllabus {pm_item and pm_item.get('name')!r}, not 'On Judgment'")
    names = [i.get("name") for i in sorted(items, key=lambda i: i.get("weight", 0))]
    for path in PAGES:
        if path == "/pm/all/":
            continue
        f_ = os.path.join(out_dir, path.strip("/"), "index.html")
        soup = BeautifulSoup(open(f_, encoding="utf-8").read(), "html.parser")
        nav = soup.select_one("header nav.site-nav[aria-label=Sections]")
        if not nav:
            fail("R9", f"{path}: no menu in the header"); continue
        listed = nav.select(".nav-list a")
        if [a.get_text(strip=True) for a in listed] != names:
            fail("R9", f"{path}: the menu lists {[a.get_text(strip=True) for a in listed]}, not {names}")
        cur = [a for a in listed if a.has_attr("aria-current")]
        here = nav.select(".nav-here")
        want = "/" if path == "/" else next((i.get("url") for i in items if path.startswith(i.get("url", "-"))), None)
        if path == "/":
            if cur or here:
                fail("R9", "/: the front door marks a section as current, though it is none")
        elif len(cur) != 1 or cur[0].get("href") != want or len(here) != 1 or here[0].get("href") != want or here[0].get("aria-current") != cur[0].get("aria-current"):
            fail("R9", f"{path}: the menu doesn't mark its section ({want}) both in its list and beside the Menu button")
        btn = nav.select_one("button.nav-open")
        lst = nav.select_one(".nav-list")
        if not btn or btn.get("type") != "button" or btn.get("aria-expanded") != "false" or not btn.has_attr("hidden") or "Menu" not in btn.get_text() or not lst or btn.get("aria-controls") != lst.get("id"):
            fail("R9", f"{path}: the Menu button should be a real button, start hidden (the script shows it) and closed, and control the menu's list")
    srv = Server(out_dir)
    chrome = os.environ.get("CHROME")
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=chrome) if chrome else p.chromium.launch()
            # From 46rem up: the name and every section on one line, with room for a fourth, Writing
            ctx = b.new_context(viewport={"width": MENU_WIDE, "height": 700}); pg = ctx.new_page()
            pg.goto(srv.base + "/pm/find-the-constraint/"); pg.wait_for_load_state("load"); pg.evaluate("document.fonts.ready")
            pg.evaluate("() => { const l = document.querySelector('.nav-list'); const a = l.lastElementChild.cloneNode(true); a.textContent = 'Writing'; a.removeAttribute('aria-current'); l.insertBefore(a, l.lastElementChild); }")
            r = pg.evaluate(JS_MENU)
            n = r["name"]
            if r["btn"] or r["here"] or len(r["links"]) != len(names) + 1 or any(t[4] <= n[1] or t[2] >= n[3] for t in r["links"]) or max(t[2] for t in r["links"]) - min(t[2] for t in r["links"]) > 2:
                fail("R9", f"at {MENU_WIDE}px, with a fourth section, the name and the sections don't share one line: {r['links']}")
            ctx.close()
            # Below 46rem: the current section and the button share the name's line; the list opens and closes
            for w in (320, 390):
                ctx = b.new_context(viewport={"width": w, "height": 844}); pg = ctx.new_page()
                for path in ("/", "/page/readme/", "/pm/find-the-constraint/"):
                    pg.goto(srv.base + path); pg.wait_for_load_state("load"); pg.evaluate("document.fonts.ready")
                    where = f"{path} at {w}px"
                    r = pg.evaluate(JS_MENU)
                    n = r["name"]
                    if not r["btn"] or r["list"]:
                        fail("R9", f"{where}: with the script, the sections should wait behind a Menu button"); continue
                    if (path == "/") != (r["here"] is None):
                        fail("R9", f"{where}: the current section {'shows on the front door' if path == '/' else 'is missing beside the Menu button'}")
                    row = [r["btn"]] + ([r["here"]] if r["here"] else [])
                    if any(x[3] <= n[1] or x[1] >= n[3] for x in row):
                        fail("R9", f"{where}: the current section and the Menu button don't share the name's line")
                    if r["here"] and r["hereLine"] != pg.evaluate("() => { const d = document.createElement('div'); d.style.color = 'var(--orange)'; document.body.appendChild(d); const c = getComputedStyle(d).color; d.remove(); return c; }"):
                        fail("R9", f"{where}: the current section has no orange line beside the Menu button")
                    if w == 390:
                        for x, what in [(r["btn"], "Menu button")] + ([(r["here"], "current section")] if r["here"] else []):
                            if x[3] - x[1] < 43.5:
                                fail("R9", f"{where}: the {what} is {x[3] - x[1]:.0f}px tall, under 44")
                    # It opens on a tap and stays open; the list sits over the page and holds every section but the
                    # current one, which is beside the button already
                    cur_name = pg.evaluate("() => { const h = document.querySelector('.nav-here'); return h ? h.textContent.trim() : null; }")
                    pg.click("button.nav-open"); pg.wait_for_timeout(50)
                    r = pg.evaluate(JS_MENU)
                    others = [x for x in names if x != cur_name]
                    if r["expanded"] != "true" or not r["list"] or [t[0] for t in r["links"]] != others:
                        fail("R9", f"{where}: the Menu button doesn't open a list of {others}: {[t[0] for t in r['links']]}"); continue
                    # It hangs from the header's right edge and reaches left a step past where the menu starts, its
                    # sections lined up under the current one (the owner, 25 November 2026)
                    lst, nav_left = r["list"], pg.evaluate("document.querySelector('nav.site-nav[aria-label=Sections]').getBoundingClientRect().left")
                    if abs(lst[2] - w) > 1:
                        fail("R9", f"{where}: the menu's list doesn't hang from the header's right edge (it ends at {lst[2]:.0f})")
                    if r["here"] and not (nav_left - 24.5 <= lst[0] <= nav_left - 7.5):
                        fail("R9", f"{where}: the menu's list reaches left to {lst[0]:.0f}, not a step past where the menu starts ({nav_left:.0f})")
                    if r["here"] and any(abs(t[5] - r["here"][0]) > 1 for t in r["links"]):
                        fail("R9", f"{where}: the menu's sections don't line up under the current one")
                    if any(t[1] > lst[0] + 1.5 or t[3] < lst[2] - 0.5 for t in r["links"]):
                        fail("R9", f"{where}: a row of the menu's list is a link only across its words, not the list's full width")
                    if w == 390 and any(t[4] - t[2] < 43.5 for t in r["links"]):
                        fail("R9", f"{where}: a section in the menu's list is under 44px tall")
                    top = pg.evaluate("() => [...document.querySelectorAll('.nav-list a')].filter(a => a.getClientRects().length).every(a => { const l = a.getBoundingClientRect(); const e = document.elementFromPoint(l.left + 2, l.top + l.height / 2); return !!e && !!e.closest('.nav-list'); })")
                    if not top:
                        fail("R9", f"{where}: the menu's list sits under the page or the course bar, not over it")
                    pg.wait_for_timeout(400)
                    if pg.evaluate(JS_MENU)["expanded"] != "true":
                        fail("R9", f"{where}: the menu's list closes on its own")
                    pg.click("button.nav-open")
                    if pg.evaluate(JS_MENU)["list"]:
                        fail("R9", f"{where}: pressing the Menu button again doesn't close its list")
                    pg.focus("button.nav-open"); pg.keyboard.press("Enter"); pg.keyboard.press("Tab"); pg.keyboard.press("Escape")
                    r = pg.evaluate(JS_MENU)
                    if r["list"] or not r["focus"]:
                        fail("R9", f"{where}: Escape doesn't close the menu's list and give focus back to its button")
                    pg.click("button.nav-open"); pg.mouse.click(w // 2, 800)
                    if pg.evaluate(JS_MENU)["list"]:
                        fail("R9", f"{where}: a tap outside the menu leaves its list open")
                    if pg.evaluate("document.documentElement.scrollHeight - innerHeight") > 300:
                        pg.click("button.nav-open"); pg.evaluate("window.scrollBy(0, 200)"); pg.wait_for_timeout(100)
                        if pg.evaluate(JS_MENU)["list"]:
                            fail("R9", f"{where}: scrolling the page leaves the menu's list open")
                        pg.evaluate("window.scrollTo(0, 0)"); pg.wait_for_timeout(50)
                        pg.click("button.nav-open"); pg.keyboard.press("Tab"); pg.evaluate("window.scrollBy(0, 200)"); pg.wait_for_timeout(100)
                        if not pg.evaluate(JS_MENU)["list"]:
                            fail("R9", f"{where}: a scroll closes the menu's list while focus is inside it")
                        pg.keyboard.press("Escape")
                    if path == "/pm/find-the-constraint/":
                        # The menu and the course bar's list never show together (R9, G2)
                        pg.evaluate("window.scrollTo(0, 0)"); pg.wait_for_timeout(50)
                        # on a phone a tap leaves no focus on a button (Safari), so the tap itself must close the other list
                        pg.click("button.cb-place"); pg.evaluate("document.activeElement.blur()"); pg.click("button.nav-open")
                        if pg.evaluate("() => !document.querySelector('.cb-menu').hidden") or not pg.evaluate(JS_MENU)["list"]:
                            fail("R9", f"{where}: opening the menu leaves the course bar's list open")
                        # the open menu covers the bar, so a reader reaches the bar's button by moving focus to it
                        pg.focus("button.cb-place"); pg.keyboard.press("Enter")
                        if pg.evaluate(JS_MENU)["list"] or pg.evaluate("() => document.querySelector('.cb-menu').hidden"):
                            fail("R9", f"{where}: opening the course bar's list leaves the menu's open")
                        pg.keyboard.press("Escape")
                ctx.close()
            # A window too short for the list: a scroll leaves it open, so a reader can reach every section
            ctx = b.new_context(viewport={"width": 390, "height": 160}); pg = ctx.new_page()
            pg.goto(srv.base + "/page/readme/"); pg.wait_for_load_state("load")
            pg.click("button.nav-open"); pg.evaluate("window.scrollBy(0, 60)"); pg.wait_for_timeout(100)
            if not pg.evaluate(JS_MENU)["list"]:
                fail("R9", "in a window shorter than the menu's list, a scroll closes the list before the reader can reach it")
            ctx.close()
            # Without scripts: every section shows, wrapping where it must, and no button
            ctx = b.new_context(viewport={"width": 390, "height": 844}, java_script_enabled=False); pg = ctx.new_page()
            pg.goto(srv.base + "/pm/find-the-constraint/"); pg.wait_for_load_state("load")
            r = pg.evaluate(JS_MENU)
            if r["btn"] or r["here"] or [t[0] for t in r["links"]] != names or r["docW"] > r["winW"]:
                fail("R9", f"without scripts, every section should show in the header, and no Menu button: {r}")
            ctx.close()
            b.close()
    finally:
        srv.close()

def arc_checks(out_dir):
    """S20: the arc's four parts on Start, each name and line above its modules, every module in one part in reading
    order, The Compass last under "To close". S21: The Compass, made from a module's parts, closes the course."""
    from bs4 import BeautifulSoup
    checked("S20", "S21")
    mods = yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "modules.yaml"), encoding="utf-8"))
    arc = yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "arc.yaml"), encoding="utf-8")) or {}
    parts, closing = arc.get("parts") or [], arc.get("closing") or {}
    order = [m["id"] for m in mods]
    placed = [i for p_ in parts for i in (p_.get("modules") or [])]
    if len(parts) != 4:
        fail("S20", f"data/pm/arc.yaml has {len(parts)} parts, and the arc has four")
    if placed != order:
        missing = [i for i in order if placed.count(i) != 1]
        fail("S20", "data/pm/arc.yaml doesn't hold every module on the map once, in reading order"
             + (f": {', '.join(missing)}" if missing else ""))
    for p_ in parts:
        if not str(p_.get("title", "")).strip() or not str(p_.get("line", "")).strip():
            fail("S20", f"an arc part has no name or no line: {p_.get('title') or p_.get('modules')}")
    title = {m["id"]: m["title"] for m in mods}
    question = {m["id"]: m["question"] for m in mods}
    norm = lambda t: " ".join(str(t).replace("\u2019", "'").split())

    def groups(wrap, where, start):
        """The labels and lists in a wrap, as (label, [(num, title, question, href)]), in the page's order."""
        out = []
        for el in wrap.find_all(["p", "ol"], recursive=False):
            cls = el.get("class") or []
            if "arc-part" in cls:
                out.append((norm(el.get_text(" ")), []))
            elif "modules" in cls:
                if not out:
                    fail("S20", f"{where}: a list of modules comes before any part's name")
                    out.append(("", []))
                for li in el.find_all("li", recursive=False):
                    h3 = li.find("h3")
                    for sr in h3.find_all(class_="sr"):
                        sr.extract()
                    a = h3.find("a")
                    out[-1][1].append((norm(li.find(class_="mod-num").get_text()), norm(h3.get_text(" ")),
                                       norm(li.find(class_="mod-question").get_text(" ")), a.get("href") if a else None))
        return out

    want = [(f"{p_['title']}. {p_['line']}", [title[i] for i in p_.get("modules") or [] if i in title]) for p_ in parts]
    start = BeautifulSoup(open(os.path.join(out_dir, "pm", "index.html"), encoding="utf-8").read(), "html.parser")
    wrap = start.find("section", class_="modules-wrap")
    if not wrap:
        fail("S20", "Start has no list of modules"); return
    got = groups(wrap, "Start", True)
    for k, (label, items) in enumerate(want):
        if k >= len(got):
            fail("S20", f"Start doesn't show the part \"{label}\""); continue
        if got[k][0] != norm(label):
            fail("S20", f"Start's part {k + 1} reads \"{got[k][0]}\", not \"{norm(label)}\"")
        if [t for _, t, _, _ in got[k][1]] != items:
            fail("S20", f"Start's part {k + 1}, {label.split('.')[0]}, lists {[t for _, t, _, _ in got[k][1]]}, not {items}")
    page = closing.get("page")
    label = f"{closing.get('label')}. {closing.get('line')}"
    if len(got) != len(want) + 1 or got[-1][0] != norm(label):
        fail("S20", f"Start's list doesn't end with the closing unit under \"{closing.get('label')}.\"")
    else:
        items = got[-1][1]
        if len(items) != 1 or items[0][0] or not (items[0][3] or "").rstrip("/").endswith(f"/pm/{page}"):
            fail("S20", "Start's last entry should be The Compass alone, unnumbered and linked")
    if wrap.find("span", class_="mod-num", string=re.compile(r"\d")) is None:
        fail("S20", "Start's modules lost their numbers")
    for el in wrap.find_all("p", class_="arc-part"):
        if el.find_parent("li"):
            fail("S20", "a part's name sits inside a module's entry, not above its modules")
    # S21: The Compass itself
    path = os.path.join(out_dir, "pm", str(page), "index.html")
    if not page or not os.path.exists(path):
        fail("S21", f"The Compass isn't built: no page at /pm/{page}/"); return
    if os.path.exists(os.path.join(ROOT, "drafts", "pm", f"{page}.md")):
        fail("S21", f"The Compass has a draft, drafts/pm/{page}.md, and it's built: one source only (X1)")
    art = BeautifulSoup(open(path, encoding="utf-8").read(), "html.parser").select_one("main article.unit")
    where = "The Compass"
    if not art or "closing" not in (art.get("class") or []):
        fail("S21", f"{where}'s page isn't a closing unit (article class \"unit closing\")"); return
    head = art.find(class_="unit-head")
    tag = head.select_one(".kicker .tag") if head else None
    if not tag or norm(tag.get_text()) != closing.get("label"):
        fail("S21", f"{where} should say \"{closing.get('label')}\" where a module names its number")
    if not head or not head.find(class_="question") or not head.find(class_="meta"):
        fail("S21", f"{where} has no question or no time under its title")
    else:
        fm = open(os.path.join(ROOT, "content", "pm", f"{page}.md"), encoding="utf-8").read().split("---", 2)[1]
        mins = int((yaml.safe_load(fm) or {}).get("do_minutes") or 0)
        t = norm(head.find(class_="meta").get_text())
        if not re.fullmatch(r"About (\d+ minutes|an hour.*|\d.*hours?)\.", t):
            fail("S21", f"{where}'s time reads \"{t}\"")
        if mins and str(mins) not in t and "hour" not in t:
            fail("S21", f"{where}'s time, \"{t}\", isn't its Do's {mins} minutes")
    body = art.find(class_="unit-body")
    if body.select(".steps, .check, .deeper, .path, .last-time"):
        fail("S21", f"{where} carries a short path, a Check or a full path, and it has none")
    intro = body.find("section", attrs={"data-slot": "intro"})
    if not intro or not intro.find(attrs={"data-voice": True}):
        fail("S21", f"{where} doesn't open with the owner's framing in a voice slot")
    h2s = [norm(h.get_text(" ")) for h in body.find_all("h2")]
    for h in ("The compass", "One call, walked through", "Do", "Where to go from here"):
        if h not in h2s:
            fail("S21", f"{where} has no section \"{h}\"")
    if h2s[:1] != ["The compass"]:
        fail("S21", f"{where}'s first section should be \"The compass\", the questions, and it's \"{h2s[:1]}\"")
    cw = body.find("section", class_="compass")
    if cw:
        cg = groups(cw, where, False)
        if [(l, [t for _, t, _, _ in it]) for l, it in cg] != [(norm(l), it) for l, it in want]:
            fail("S21", f"{where}'s questions aren't grouped by the arc as Start shows it (S20)")
        for l, it in cg:
            for num_, t, q, href in it:
                mid = next((m["id"] for m in mods if m["title"] == t), None)
                if mid and norm(question[mid]) != q:
                    fail("S21", f"{where}: {t}'s question reads \"{q}\", not the map's")
                if mid and not href:
                    fail("S21", f"{where}: {t} isn't linked")
    else:
        fail("S21", f"{where} doesn't list the modules' questions")

    def section(name):
        h = next((h for h in body.find_all("h2") if norm(h.get_text(" ")) == name), None)
        out = []
        for sib in (h.find_all_next() if h else []):
            if sib.name == "h2":
                break
            if sib.name == "p":
                out.append(norm(sib.get_text(" ")))
        return out
    # the call, walked twice: a customer-facing product and an internal platform, picked with two buttons
    fm_ = yaml.safe_load(open(os.path.join(ROOT, "content", "pm", f"{page}.md"), encoding="utf-8").read().split("---", 2)[1]) or {}
    want_walks = [w_.get("id") for w_ in fm_.get("walks") or []]
    walks = body.select("div.walk[data-walk]")
    if [w_["data-walk"] for w_ in walks] != want_walks or len(walks) != 2:
        fail("S21", f"{where}'s call should be walked twice, a customer-facing product and an internal platform: it has {[w_.get('data-walk') for w_ in walks]}")
    for w_ in walks:
        t_ = w_.find(class_="walk-title")
        text_ = norm(w_.get_text(" "))
        named = [t for t in title.values() if t in text_]
        label_ = norm(t_.get_text()) if t_ else w_["data-walk"]
        if not t_:
            fail("S21", f"{where}: the walk {w_['data-walk']} has no title, so without the script or in print nothing names it")
        if len(named) < 6:
            fail("S21", f"{where}: the walk \"{label_}\" names {len(named)} modules by title, and each names at least six")
        if not re.search(r"\bcollide", text_):
            fail("S21", f"{where}: the walk \"{label_}\" doesn't say where two questions collide, and how to weigh them")
        if w_.has_attr("hidden"):
            fail("S21", f"{where}: the walk \"{label_}\" is hidden in the page itself, so without the script nobody reads it")
    tog = body.select_one("[data-walk-toggle]")
    btns = tog.select("button[data-walk-show]") if tog else []
    if not tog or [b_["data-walk-show"] for b_ in btns] != want_walks:
        fail("S21", f"{where} has no buttons to pick a version of its call, one for each")
    elif not tog.has_attr("hidden"):
        fail("S21", f"{where}'s buttons show without the script, where they'd do nothing")
    elif [b_.get("aria-pressed") for b_ in btns] != ["true"] + ["false"] * (len(btns) - 1):
        fail("S21", f"{where}'s first button should start pressed, and only it")
    elif any("setup" not in (b_.get("class") or []) for b_ in btns):
        fail("S21", f"{where}'s buttons should take the games' setup style, so they bring no new look")
    do = section("Do")
    if not do or not do[0].startswith("Review your decision log"):
        fail("J3", f"{where}'s Do should open \"Review your decision log.\" in bold, and review the log whole")
    elif not body.find("strong", string=re.compile(r"^Review your decision log")):
        fail("J3", f"{where}'s Do should open \"Review your decision log.\" in bold")
    if not re.search(r"where to draw (the|a) line", " ".join(section("Where to go from here")), re.I):
        fail("S21", f"{where}'s last section doesn't name the judgment that recurs, where to draw the line")
    # ... and then what the course leaves out, each with the best free place to start, linked (the owner, 25 November 2026)
    out_h = body.find("h3", id=LEAVES_OUT_ID)
    last_h2 = next((h for h in body.find_all("h2") if norm(h.get_text(" ")) == "Where to go from here"), None)
    if not out_h or not last_h2 or out_h.find_previous("h2") is not last_h2:
        fail("S21", f"{where}'s last section has no heading for what the course leaves out (#{LEAVES_OUT_ID})")
    else:
        items = out_h.find_next("ul").find_all("li") if out_h.find_next("ul") else []
        for area, pat in LEAVES_OUT:
            hit = [li for li in items if re.search(pat, norm(li.get_text(" ")), re.I)]
            if not hit:
                fail("S21", f"{where} doesn't say the course leaves out {area}")
            elif not any(a.get("href", "").startswith("https://") for li in hit for a in li.find_all("a")):
                fail("S21", f"{where} names {area} as left out, with no free place to start, linked")
    walk_browser_checks(out_dir, f"/pm/{page}/", want_walks)
    how = start.find("h2", id="how-it-works")
    ul = how.find_next("ul") if how else None
    if not ul or "closing page" not in norm(ul.get_text(" ")) or "The Compass" not in norm(ul.get_text(" ")):
        fail("S21", "Start's \"How it works\" doesn't name the closing page, The Compass")
    elif not ul.find("a", href=re.compile(rf"/pm/{page}/#{LEAVES_OUT_ID}$")):
        fail("S21", f"Start's \"How it works\" doesn't point to what The Compass says the course leaves out (#{LEAVES_OUT_ID})")


def check_static():
    checked("T1", "T3", "S1", "S2", "S3", "C4", "D4")
    css_dir = os.path.join(ROOT, "assets", "css")
    cfg = yaml.safe_load(open(os.path.join(ROOT, "hugo.yaml")))
    params = cfg.get("params", {})
    css_files = [os.path.join(css_dir, "base.css"), os.path.join(css_dir, "pm.css")]

    # V2: one look, no switches
    checked("V2")
    extra = sorted(set(os.listdir(css_dir)) - {"base.css", "pm.css"})
    if extra:
        fail("V2", f"stylesheets beside base.css and pm.css: {', '.join(extra)}")
    for key in ("look", "direction", "marks"):
        if key in params:
            fail("V2", f"hugo.yaml still has a {key} setting")
    for path in glob.glob(os.path.join(ROOT, "layouts", "**", "*.html"), recursive=True):
        if re.search(r"site\.Params\.(look|direction|marks)\b", open(path, encoding="utf-8").read()):
            fail("V2", f"{os.path.relpath(path, ROOT)} reads a look, direction or hand setting")

    # C7: picture colors are named in pm.css, each with a value for dark screens, and no picture file sets a color itself
    checked("C7")
    pm_css = re.sub(r"/\*.*?\*/", "", open(os.path.join(css_dir, "pm.css"), encoding="utf-8").read(), flags=re.S)
    fig_dark = set()
    for m in re.finditer(r"@media[^{]*prefers-color-scheme:\s*dark[^{]*\{\s*:root\s*\{([^}]*)\}", pm_css):
        fig_dark.update(re.findall(r"(--fig-[\w-]+)\s*:", m.group(1)))
    fig_light = set()
    for m in re.finditer(r":root\s*\{([^}]*)\}", re.sub(r"@media[^{]*\{(?:[^{}]*\{[^}]*\})*[^}]*\}", "", pm_css)):
        fig_light.update(re.findall(r"(--fig-[\w-]+)\s*:", m.group(1)))
    for tok in sorted(set(re.findall(r"var\((--fig-[\w-]+)\)", pm_css)) | fig_light | fig_dark):
        if tok not in fig_light:
            fail("C7", f"pm.css uses {tok} but does not name its value")
        if tok not in fig_dark:
            fail("C7", f"pm.css gives {tok} no value for dark screens")
    for path in sorted(glob.glob(os.path.join(ROOT, "assets", "figures", "*.svg"))):
        svg = open(path, encoding="utf-8").read()
        own = re.findall(r"\s(?:fill|stroke|style|color|stop-color)\s*=", svg) + re.findall(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(", re.sub(r"<(title|desc)\b.*?</\1>", "", svg, flags=re.S))
        if own:
            fail("C7", f"{os.path.relpath(path, ROOT)} sets a color itself ({own[0].strip()}); name it in pm.css and use a class")

    # T3: no em dashes, here and in the voice guide, which lives in pm-sources (22 November 2026)
    t3_paths = [p for pattern in ["content/**/*", "drafts/**/*", "layouts/**/*", "assets/**/*.css", "assets/**/*.js", "data/**/*", "hugo.yaml", "tests/SPEC.md", "README*.md"]
                for p in glob.glob(os.path.join(ROOT, pattern), recursive=True)]
    voice = os.path.join(PM_SOURCES, "VOICE.md")
    if os.path.isfile(voice):
        t3_paths.append(voice)
    else:
        NOTE["T3"].append(f"VOICE.md not scanned: pm-sources isn't at {PM_SOURCES}, as on GitHub; a working session scans it")
    for path in t3_paths:
        if os.path.isfile(path):
            try:
                text = open(path, encoding="utf-8").read()
            except UnicodeDecodeError:
                continue
            if "\u2014" in text:
                where = "pm-sources/" + os.path.relpath(path, PM_SOURCES) if path == voice else os.path.relpath(path, ROOT)
                fail("T3", f"em dash in {where}")

    # T1: fonts referenced exist, with a licence file per family
    fonts_dir = os.path.join(ROOT, "static", "fonts")
    for path in css_files:
        for url in re.findall(r'url\("(/fonts/[^"]+)"\)', open(path).read()):
            f = os.path.join(ROOT, "static", url.lstrip("/"))
            if not os.path.exists(f):
                fail("T1", f"{os.path.basename(path)} references missing font {url}")
            family = os.path.basename(url).split("-")[0]
            if not glob.glob(os.path.join(fonts_dir, f"LICENSE-{family}*")):
                fail("T1", f"no license file for {os.path.basename(url)}")

    # C4: token contrast pairs, light and dark
    tokens = parse_tokens(css_files)
    pairs = [("--ink", "--paper", 4.5), ("--muted", "--paper", 4.5), ("--muted", "--tint", 4.5), ("--ink", "--tint", 4.5),
             ("--muted", "--panel", 4.5), ("--orange", "--paper", 4.5), ("--mark-ink", "--mark", 4.5),
             ("--ink", "--mark-soft", 4.5), ("--muted", "--mark-soft", 4.5), ("--link-line", "--paper", 3.0)]
    for theme, t in tokens.items():
        for fg, bg, need in pairs:
            if fg not in t or bg not in t:
                fail("C4", f"{theme}: token {fg} or {bg} not defined")
                continue
            try:
                c = contrast(hex_to_rgb(t[fg]), hex_to_rgb(t[bg]))
            except ValueError:
                fail("C4", f"{theme}: cannot read {fg}={t[fg]} or {bg}={t[bg]}")
                continue
            if c < need:
                fail("C4", f"{theme}: {fg} on {bg} is {c:.2f}:1, needs {need}:1")
            NOTE["C4"].append(f"{theme}: {fg} on {bg} {c:.2f}:1")

    # D4: newer features guarded by @supports
    for path in css_files:
        css = re.sub(r"/\*.*?\*/", "", open(path).read(), flags=re.S)
        unguarded = re.sub(r"@supports[^{]*\{(?:[^{}]*\{[^}]*\})*[^}]*\}", "", css)
        if re.search(r"(?<![\w-])(-webkit-)?mask(-image)?\s*:", unguarded):
            fail("D4", f"{os.path.basename(path)} uses mask outside @supports")
        if ":has(" in unguarded:
            fail("D4", f"{os.path.basename(path)} uses :has() outside @supports")

    # T4, T6, T7: stylesheets name sizes and line spacing rather than writing numbers, and the screen scales are in rem.
    # This catches states the rendered check may not open (hover, a dialog, a narrow breakpoint).
    checked("T4", "T6", "T7")
    for path in css_files:
        css = re.sub(r"/\*.*?\*/", "", open(path).read(), flags=re.S)
        fname = os.path.basename(path)
        for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
            sel = " ".join(sel.split())
            if re.search(r"\.fig\b|\.fig-|\.tick-num|@font-face", sel):  # text inside pictures belongs to the picture
                continue
            decls = re.findall(r"(?<![\w-])(font-size|line-height|font)\s*:\s*([^;]+)", body)
            for prop, val in decls:
                val = val.strip()
                if val in ("inherit", "unset"):
                    continue
                if prop in ("font-size", "font") and "var(--fs-" not in val:
                    fail("T4", f"{fname}: {sel} sets {prop}: {val} without a size from the scale")
                if prop == "line-height" and "var(--lh-" not in val:
                    fail("T6", f"{fname}: {sel} sets line-height: {val} without a value from the scale")
                if prop == "font" and "/" in val and "var(--lh-" not in val.split("/", 1)[1]:
                    fail("T6", f"{fname}: {sel} sets font: {val} with line spacing not from the scale")
        if fname == "base.css":
            screen_css = _drop_print(css)
            for body in re.findall(r":root\s*\{([^{}]*)\}", screen_css):
                for k, v in re.findall(r"(--(?:fs|sp)-[\w-]+)\s*:\s*([^;]+);", body):
                    if re.search(r"\d(px|pt)\b", v):
                        fail("T7", f"base.css: {k} is {v.strip()}; on screen the scale is set in rem so it follows the reader's text size")

    # S1, S2, S3: content structure
    glossary = yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "glossary.yaml")))
    used = set()
    for path in glob.glob(os.path.join(ROOT, "content", "pm", "**", "*.md"), recursive=True):
        text = open(path, encoding="utf-8").read()
        used.update(re.findall(r'pm/term "([\w-]+)"', text))
        m = re.match(r"---\n(.*?)\n---", text, re.S)
        fm = yaml.safe_load(m.group(1)) if m else {}
        rel = os.path.relpath(path, ROOT)
        earlier = {}
        for step in fm.get("steps", []) or []:
            if not step.get("look"):
                fail("S1", f"{rel}: step {step.get('id')} has no look line")
            # a step that reads on in the step before it shares that step's trust (spec S2)
            before = earlier.get(step.get("continues")) if step.get("continues") else None
            if step.get("continues") and not (before and before.get("trust") and list(earlier)[-1] == step.get("continues")):
                fail("S2", f"{rel}: step {step.get('id')} continues {step.get('continues')}, which isn't the step just before it with a trust line")
            if step.get("kind") not in ("card", "play", "do", "check") and not ((step.get("trust") or before) and step.get("only")):
                fail("S2", f"{rel}: step {step.get('id')} lacks trust or only")
            earlier[step.get("id")] = step
        deeper = fm.get("deeper")
        for d in (deeper if isinstance(deeper, list) else [deeper] if deeper else []):
            story = STORY.match(d.get("where") or "") and not re.match(r"(?:An? )?documentary", d.get("where") or "", re.I)
            if not (d.get("only") and (story or d.get("trust"))):
                fail("S2", f"{rel}: further reading {d.get('title')} lacks " + ("what you'll get" if story else "trust or only"))
    for key in used - set(glossary):
        fail("S3", f"term {key} is used but not in the glossary")
    for key in set(glossary) - used:
        fail("S3", f"glossary entry {key} is never used")
    return tokens


# S15: what each kind of full-path entry shows as, read from its kind's words, apart from the template's own reading
KIND_SCREEN = re.compile(r"(?:An? |A pair of |Two )?(?:classic )?(?:film|(?:TV |television |streaming )?series|documentary)\b", re.I)
KIND_BOOK = re.compile(r"An? (?:book|textbook|novel|novella)\b", re.I)
KIND_ARTICLE = re.compile(r"An? (?:(?:journal |law review |magazine |long )?article|(?:conference |research |working |long )?paper|(?:staff )?report|essay)\b", re.I)


def kind_checks(out_dir):
    """S15: a full-path entry's kind as an icon before its title, its words kept for screen readers and the doc.
    S16: a card opens with a picture, or a quoted sentence in its place, credited under it."""
    from bs4 import BeautifulSoup
    checked("S15", "S16")
    for m in yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "modules.yaml"))):
        if not m.get("page"):
            continue
        path = os.path.join(out_dir, "pm", m["page"], "index.html")
        soup = BeautifulSoup(open(path, encoding="utf-8").read(), "html.parser")
        for li in soup.select(".deeper-list > li"):
            h3 = li.find("h3")
            title = clean_text(h3.get_text()) if h3 else "?"
            icons = h3.select("svg.kind-icon") if h3 else []
            line = li.find("p", class_="meta-line")
            words = clean_text(line.get_text()) if line else ""
            if len(icons) != 1 or h3.find(True) is not icons[0]:
                fail("S15", f"{m['page']}: {title}: no single kind icon before the title"); continue
            icon = icons[0]
            if icon.get("aria-hidden") != "true":
                fail("S15", f"{m['page']}: {title}: the kind icon is read aloud, so the kind would be heard twice")
            if not line or "sr" not in (line.get("class") or []):
                fail("S15", f"{m['page']}: {title}: the kind's words show to the eye, or are gone; keep them for screen readers only")
            want = "screen" if KIND_SCREEN.match(words) else "book" if KIND_BOOK.match(words) else "article" if KIND_ARTICLE.match(words) else None
            if want is None:
                fail("S15", f"{m['page']}: {title}: \"{words}\" names no kind the icons show (a book, an article or a screen)")
            elif icon.get("data-kind") != want:
                fail("S15", f"{m['page']}: {title}: \"{words}\" shows the {icon.get('data-kind')} icon, not the {want}")
            if re.search(r"\bFree at\b", words):
                fail("S15", f"{m['page']}: {title}: \"Free at\" sits in the hidden kind line; it opens the note")
        for st in soup.select("li.step .meta-line"):
            if "sr" in (st.get("class") or []):
                fail("S15", f"{m['page']}: a short-path step's line is hidden, and it carries the minutes")
    for path in sorted(glob.glob(os.path.join(ROOT, "content", "pm", "cards", "*.md"))):
        text = open(path, encoding="utf-8").read()
        fm = yaml.safe_load(re.match(r"---\n(.*?)\n---", text, re.S).group(1))
        name = os.path.splitext(os.path.basename(path))[0]
        html = os.path.join(out_dir, "pm", "cards", name, "index.html")
        soup = BeautifulSoup(open(html, encoding="utf-8").read(), "html.parser")
        plate = soup.select_one("article.card figure.plate[data-slot=picture]")
        q = fm.get("figure_quote")
        if bool(fm.get("figure")) == bool(q):
            fail("S16", f"card {name}: opens with {'both a picture and a quote' if q else 'neither a picture nor a quote'}")
        if not plate:
            fail("S16", f"card {name}: no picture in the picture's place"); continue
        if q:
            missing = [k for k in ("text", "by", "work", "url", "year") if not q.get(k)]
            if missing:
                fail("S16", f"card {name}: the quote lacks its {', '.join(missing)}")
            bq = plate.select_one("blockquote.plate-quote-text")
            cap = plate.find("figcaption")
            if not bq or clean_text(bq.get_text()) != clean_text(q.get("text") or ""):
                fail("S16", f"card {name}: the quoted sentence isn't set word for word in the picture's place")
            if not cap or not cap.find("cite") or (q.get("by") or "") not in clean_text(cap.get_text()):
                fail("S16", f"card {name}: the quote isn't credited under it, with its author and work")
        elif not plate.select_one("svg[role=img]"):
            fail("S16", f"card {name}: its picture is missing")
        # a card that quotes its idea's first sentence does so first under "The idea", word for word and credited
        quoted = QUOTED_FIRST.get(name)
        idea = soup.find("h2", string=re.compile(r"^\s*The idea\s*$"))
        first = idea.find_next_sibling() if idea else None
        if quoted:
            if not first or first.name != "blockquote" or clean_text(quoted["text"]) not in clean_text(first.get_text()):
                fail("S16", f"card {name}: {quoted['by']}'s sentence isn't quoted word for word as the first thing under \"The idea\"")
            elif quoted["by"] not in first.get_text() or quoted["year"] not in first.get_text() or not first.find("a", href=quoted["url"]):
                fail("S16", f"card {name}: the quoted sentence isn't credited with its author, its work linked, and its year")
        elif soup.select_one("article.card .card-body blockquote"):
            fail("S16", f"card {name}: quotes a sentence in a block that S16 doesn't know of; name it in QUOTED_FIRST")


QUOTED_FIRST = {"conways-law": {"by": "Melvin Conway", "year": "1968", "url": "https://www.melconway.com/Home/Committees_Paper.html",
                                 "text": "The basic thesis of this article is that organizations which design systems (in the broad sense used here) are constrained to produce designs which are copies of the communication structures of these organizations."}}


def clean_text(s):
    return re.sub(r"\s+", " ", s.translate(QUOTE_FOLD)).strip()


QUOTE_FOLD = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "\u00a0": " "})


def slot_checks(out_dir):
    """M4: every part of every unit has a slot in data/pm/margin/<unit>.yaml, in reading order, and nothing else."""
    from bs4 import BeautifulSoup
    checked("M4")
    soup = BeautifulSoup(open(os.path.join(out_dir, "pm", "all", "index.html"), encoding="utf-8").read(), "html.parser")
    units = soup.select("main article.unit")
    seen = set()
    for art in units:
        unit = art.get("data-unit")
        slots = [el["data-slot"] for el in art.select("[data-slot]")]
        if len(set(slots)) != len(slots):
            fail("M4", f"{unit}: two parts share a slot name: {sorted(x for x in slots if slots.count(x) > 1)}")
        path = os.path.join(ROOT, "data", "pm", "margin", f"{unit}.yaml")
        rel = os.path.relpath(path, ROOT)
        seen.add(os.path.abspath(path))
        if not os.path.exists(path):
            fail("M4", f"{unit}: no slot file {rel}; run tools-pm/margin-slots.py"); continue
        data = yaml.safe_load(open(path, encoding="utf-8")) or {}
        keys = list(data)
        for k in keys:
            if k not in slots:
                fail("M4", f"{rel}: slot {k} is not a part of the page{' and holds a note' if data[k] else ''}")
        for k in slots:
            if k not in keys:
                fail("M4", f"{rel}: no slot for {k}; run tools-pm/margin-slots.py")
        if [k for k in keys if k in slots] != [k for k in slots if k in keys]:
            fail("M4", f"{rel}: slots are not in reading order")
        for k, v in data.items():
            if isinstance(v, list):
                for n in v:
                    if not isinstance(n, dict) or not isinstance(n.get("note"), str) or set(n) - {"note", "beside", "at"} \
                            or not isinstance(n.get("beside", ""), str) or n.get("at", "foot") != "foot":
                        fail("M4", f"{rel}: slot {k} holds a list, and each item is a note in quotes, with beside: and at: foot if wanted")
                        continue
                    if n.get("beside"):
                        want = " ".join(n["beside"].translate(QUOTE_FOLD).split())
                        hits = [d for d in art.select(f'div.noted[data-beside="{k}"]')
                                if d.find("p") and want in " ".join(d.find("p").get_text().translate(QUOTE_FOLD).split())]
                        if not hits:
                            fail("M4", f"{rel}: a note in slot {k} sits beside the paragraph that holds \"{n['beside']}\", and no paragraph of that part holds it now")
            elif v is not None and not isinstance(v, str):
                fail("M4", f"{rel}: slot {k} holds {type(v).__name__}, not text; put the note in quotes")
        # Each unit's parts each carry a slot: sections, steps, sources, the game, the picture, the question, terms.
        for el in art.select("section:not(.print-only), li.step, .deeper-list > li, figure, p.carry, .gloss-list > div"):
            if not el.has_attr("data-slot") and not el.find("h2", attrs={"data-slot": True}) and el.name == "section" and el.find("h2"):
                fail("M4", f"{unit}: the part '{' '.join(el.find('h2').get_text().split())}' has no slot")
            elif el.name != "section" and not el.has_attr("data-slot"):
                fail("M4", f"{unit}: a {el.name}.{'.'.join(el.get('class', []))} has no slot")
    for f in glob.glob(os.path.join(ROOT, "data", "pm", "margin", "*.yaml")):
        if os.path.abspath(f) not in seen:
            fail("M4", f"{os.path.relpath(f, ROOT)} belongs to no unit")


# ---------- page checks ----------
JS_ORANGE = """() => { const p = document.createElement('span'); p.style.color = getComputedStyle(document.documentElement).getPropertyValue('--orange'); document.body.appendChild(p); const c = getComputedStyle(p).color; p.remove(); return c; }"""
JS_VAR = """(name) => { const p = document.createElement('span'); p.style.color = getComputedStyle(document.documentElement).getPropertyValue(name); document.body.appendChild(p); const c = getComputedStyle(p).color; p.remove(); return c; }"""

JS_TEXT_COLORS = """(orange) => {
  const out = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const t = walker.currentNode; if (!t.textContent.trim()) continue;
    const el = t.parentElement; if (!el || el.closest('script,style,svg,[hidden],.sr')) continue;
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
    const s = getComputedStyle(el); if (s.visibility === 'hidden' || s.display === 'none') continue;
    if (s.color === orange) out.push({tag: el.tagName, cls: el.className && el.className.baseVal === undefined ? el.className : '', inH1: !!el.closest('h1'), text: t.textContent.trim().slice(0, 40)});
  }
  // words the stylesheet draws, as a control's label ("Open", "Show answer") is: text too, held to the same rule
  for (const el of document.body.querySelectorAll('*')) {
    if (el.closest('script,style,svg,[hidden],.sr')) continue;
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
    for (const pe of ['::before', '::after']) {
      const s = getComputedStyle(el, pe), m = /"([^"]*[A-Za-z][^"]*)"/.exec(s.content || '');
      if (m && s.display !== 'none' && s.visibility !== 'hidden' && s.color === orange)
        out.push({tag: el.tagName + pe, cls: el.className && el.className.baseVal === undefined ? el.className : '', inH1: !!el.closest('h1'), text: m[1].slice(0, 40)});
    }
  }
  return out;
}"""

# C5: the underline is a quiet grey line at 3:1 or better against the page, glossary terms dotted, at rest.
JS_LINK_LINES = """() => {
  const rgb = c => { const m = c.match(/[\d.]+/g).map(Number); return m; };
  const lum = c => { const [r, g, b] = rgb(c).slice(0, 3).map(v => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const page = getComputedStyle(document.body).backgroundColor.includes('0, 0, 0, 0') ? 'rgb(255, 255, 255)' : getComputedStyle(document.body).backgroundColor;
  const orange = (() => { const p = document.createElement('span'); p.style.color = getComputedStyle(document.documentElement).getPropertyValue('--orange'); document.body.appendChild(p); const c = getComputedStyle(p).color; p.remove(); return c; })();
  const out = [];
  for (const a of document.querySelectorAll('main a')) {
    if (!a.getClientRects().length || a.matches('.site-nav a, .door-links a, .unit-nav a, .skip')) continue;
    const s = getComputedStyle(a); if (!s.textDecorationLine.includes('underline')) continue;
    const c = s.textDecorationColor, name = a.textContent.trim().slice(0, 30);
    if (c === orange) out.push(`the underline of '${name}' is orange at rest, not the quiet grey line`);
    else if (ratio(c, page) < 3 - 1e-3) out.push(`the underline of '${name}' is ${ratio(c, page).toFixed(2)}:1 against the page, needs 3:1`);
    if (a.matches('.term') && s.textDecorationStyle !== 'dotted') out.push(`glossary term '${name}' is not dotted`);
    if (!a.matches('.term') && s.textDecorationStyle !== 'solid') out.push(`link '${name}' has a ${s.textDecorationStyle} underline; only glossary terms are dotted`);
  }
  return [...new Set(out)];
}"""

JS_FILLS = """(cols) => {
  const out = [];
  for (const el of document.querySelectorAll('body *')) {
    const s = getComputedStyle(el); if (s.display === 'none' || s.visibility === 'hidden') continue;
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
    const bg = s.backgroundColor;
    if (!cols.includes(bg)) continue;
    if (!el.textContent.trim()) continue;
    out.push({bg, tag: el.tagName, cls: typeof el.className === 'string' ? el.className : '', game: !!el.closest('.game'), skip: el.matches('.skip'), text: el.textContent.trim().slice(0, 30)});
  }
  return out;
}"""

JS_MARGIN = """() => {
  const col = document.querySelector('.unit-body.reading, .page .reading, .reading');
  if (!col) return null;
  const cr = col.getBoundingClientRect(); const cs = getComputedStyle(col);
  const right = cr.left + col.clientWidth - parseFloat(cs.paddingRight);
  const inMargin = [];
  for (const el of document.querySelectorAll('.reading *')) {
    const s = getComputedStyle(el); if (s.display === 'none' || s.visibility === 'hidden') continue;
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
    if (r.left >= right - 1 && !el.parentElement.closest('.note')) inMargin.push({cls: typeof el.className === 'string' ? el.className : '', tag: el.tagName, left: r.left, top: r.top, bottom: r.bottom, right: r.right, hidden: el.getAttribute('aria-hidden'), owner: el.matches('aside.note[data-note]')});
  }
  return {right, inMargin};
}"""


# ---------- what a screen reader and a keyboard user meet (A5 to A12) ----------
COLOR_WORDS = r"\b(yellow|orange|red|green|blue|purple|pink|grey|gray)\b"
PUNCT_START = ".,;:!?)–-"

JS_ORDER = """() => { const out = [];
  for (const el of document.querySelectorAll('main *')) {
    const s = getComputedStyle(el); if (!/flex|grid/.test(s.display)) continue;
    const kids = [...el.children].filter(k => { const r = k.getBoundingClientRect(); const ks = getComputedStyle(k);
      return r.width && r.height && ks.display !== 'none' && ks.position !== 'absolute' && ks.position !== 'fixed' && !k.matches('.sr'); });
    for (let i = 1; i < kids.length; i++) {
      if (kids[i - 1].tagName === 'FIGCAPTION' || kids[i].tagName === 'FIGCAPTION') continue;
      const a = kids[i - 1].getBoundingClientRect(), b = kids[i].getBoundingClientRect();
      if (b.bottom <= a.top + 1 && b.right > a.left && b.left < a.right)
        out.push(kids[i].tagName + '.' + (typeof kids[i].className === 'string' ? kids[i].className : '') + ' shows above the ' + kids[i - 1].tagName + '.' + (typeof kids[i - 1].className === 'string' ? kids[i - 1].className : '') + ' it follows');
    }
  }
  return [...new Set(out)]; }"""

JS_HEADINGS = """() => { const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(h => h.getClientRects().length && !h.closest('[aria-hidden=true], dialog:not([open])'));
  const out = []; let prev = 0;
  for (const h of hs) { const l = +h.tagName[1]; if (prev && l > prev + 1) out.push('h' + prev + ' to h' + l + ' at "' + h.textContent.trim().slice(0, 40) + '"'); prev = l; }
  return out; }"""

JS_PAUSES = """() => [...document.querySelectorAll('.one-thing-label, .carry-label, .tally > span, svg[role=img] > title')]
  .filter(e => !/[.:,;?!]$/.test(e.textContent.trim())).map(e => (e.tagName === 'title' ? 'picture title' : e.className || e.tagName) + ': "' + e.textContent.trim().slice(0, 40) + '"')"""

JS_STRIKE = """() => [...document.querySelectorAll('del, s, strike')].filter(el => { const before = getComputedStyle(el, '::before').content || '';
  const sr = el.querySelector('.sr'); return !/crossed out/i.test(before + ' ' + (sr ? sr.textContent : '')); }).map(el => el.textContent.trim().slice(0, 30))"""


def ax_tree(c, pg):
    cdp = c.new_cdp_session(pg)
    return cdp, cdp.send("Accessibility.getFullAXTree")["nodes"]


def ax_node(cdp, selector):
    root = cdp.send("DOM.getDocument", {"depth": 0})["root"]["nodeId"]
    nid = cdp.send("DOM.querySelector", {"nodeId": root, "selector": selector}).get("nodeId")
    if not nid:
        return None
    nodes = cdp.send("Accessibility.getPartialAXTree", {"nodeId": nid, "fetchRelatives": False})["nodes"]
    return nodes[0] if nodes else None


def axv(n, key):
    return ((n or {}).get(key) or {}).get("value", "")


def a11y_checks(browser, ctx, base, out_dir):
    checked("A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12")
    glossary = yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "glossary.yaml")))

    # A6 at phone and desktop widths; A7, A10, A11, A12 once per page
    try:
        for w in (390, 1280):
            c = ctx(viewport={"width": w, "height": 900}); pg = c.new_page(); pg.set_default_timeout(8000)
            for path in PAGES:
                pg.goto(base + path); pg.wait_for_load_state("load"); pg.evaluate("document.fonts.ready")
                for msg in pg.evaluate(JS_ORDER):
                    fail("A6", f"{path} {w}px: {msg}")
                if w != 1280:
                    continue
                cdp, nodes = ax_tree(c, pg)
                spoken = []
                for n in nodes:
                    if n.get("ignored"):
                        continue
                    role, name = axv(n, "role"), str(axv(n, "name")).strip()
                    if role == "StaticText":
                        spoken.append(name)
                    if role in ("button", "link", "checkbox", "radio", "DisclosureTriangle", "heading", "image", "dialog") and name:
                        if name[0] in PUNCT_START:
                            fail("A7", f"{path}: {role} name starts with punctuation: '{name[:40]}'")
                        if role == "DisclosureTriangle" and re.search(r"\b(Open|Close)$", name):
                            fail("A7", f"{path}: disclosure name ends with a state word: '...{name[-40:]}'")
                        if role == "checkbox" and not name.startswith("Mark done:"):
                            fail("A7", f"{path}: tick box name does not say what ticking does: '{name[:40]}'")
                for msg in pg.evaluate(JS_PAUSES):
                    fail("A7", f"{path}: no pause after {msg}")
                text = " ".join(spoken)
                for m in re.finditer(COLOR_WORDS, text, re.I):
                    i = m.start()
                    # A capitalized color word after another capitalized word is a name, such as Charles Green
                    if m.group(0)[0].isupper() and re.search(r"\b[A-Z][\w'.-]*\s+$", text[:i]):
                        continue
                    fail("A12", f"{path}: screen readers read a color: '...{text[max(0, i - 40):i + 30]}...'")
                    break
                for msg in pg.evaluate(JS_HEADINGS):
                    fail("A11", f"{path}: heading skips a level, {msg}")
                for t in pg.evaluate(JS_STRIKE):
                    fail("A10", f"{path}: struck-out '{t}' is not announced as crossed out")
            c.close()
    except Exception as e:  # a broken page must fail its rule, not stop the suite
        fail("A6", f"check could not finish: {str(e).splitlines()[0][:160]}")

    # A5: the glossary dialog, by keyboard
    try:
        c = ctx(viewport={"width": 1280, "height": 900}); pg = c.new_page(); pg.set_default_timeout(8000); pg.goto(base + "/pm/find-the-constraint/")
        key = pg.evaluate("document.querySelector('a.term').dataset.term"); g = glossary.get(key, {})
        want = g.get("term", "") + (f" ({g['also']})" if g.get("also") else "")
        state = """() => { const d = document.querySelector('dialog.gloss[open]'); const a = document.activeElement;
          return {open: !!d, modal: !!d && d.matches(':modal'), inside: !!d && d.contains(a), onTerm: a && a.matches('a.term'), page: document.hasFocus()}; }"""
        pg.focus("a.term"); pg.keyboard.press("Enter"); pg.wait_for_timeout(150)
        s = pg.evaluate(state)
        if not (s["open"] and s["modal"]):
            fail("A5", "Enter on a glossary term does not open a modal dialog")
        else:
            cdp = c.new_cdp_session(pg)
            n = ax_node(cdp, "dialog.gloss[open]")
            if axv(n, "role") != "dialog":
                fail("A5", f"the definition is exposed as {axv(n, 'role')!r}, not a dialog")
            if str(axv(n, "name")).strip() != want:
                fail("A5", f"the dialog is named {axv(n, 'name')!r}, expected {want!r}")
            if g.get("text", "")[:30] not in str(axv(n, "description")):
                fail("A5", "the dialog's description is not the definition")
            if not s["inside"]:
                fail("A5", "opening the dialog does not move focus inside it")
            for keys in ("Tab", "Shift+Tab", "Tab"):
                pg.keyboard.press(keys); pg.wait_for_timeout(80)
                s2 = pg.evaluate(state)
                if not s2["open"] or (s2["page"] and not s2["inside"]):
                    fail("A5", f"{keys} moves focus to the page behind the open dialog"); break
            pg.keyboard.press("Escape"); pg.wait_for_timeout(150)
            s3 = pg.evaluate(state)
            if s3["open"] or not s3["onTerm"]:
                fail("A5", "Escape does not close the dialog and return focus to the term")
            pg.keyboard.press("Enter"); pg.wait_for_timeout(150)
            pg.focus("dialog.gloss[open] button"); pg.keyboard.press("Enter"); pg.wait_for_timeout(150)
            s4 = pg.evaluate(state)
            if s4["open"] or not s4["onTerm"]:
                fail("A5", "Close does not close the dialog and return focus to the term")
        c.close()
    except Exception as e:  # a broken page must fail its rule, not stop the suite
        fail("A5", f"check could not finish: {str(e).splitlines()[0][:160]}")

    # A8: each game in words (reduced motion, so a run finishes at once)
    for g, mid in GAMES.items():
        try:
            c = ctx(viewport={"width": 1280, "height": 900}, reduced_motion="reduce"); pg = c.new_page(); pg.set_default_timeout(8000); pg.goto(base + f"/pm/{mid}/")
            attrs = pg.evaluate("""() => ({key: document.querySelector('.board-key') ? document.querySelector('.board-key').closest('[aria-hidden=true]') !== null : true,
                note: (() => { const n = document.querySelector('[data-setup-note]'); return !!n && (n.getAttribute('aria-live') === 'polite' || n.getAttribute('role') === 'status' || !!n.closest('[aria-live=polite], [role=status]')); })()})""")
            if not attrs["key"]:
                fail("A8", f"the {g} game: the key to the board is read by screen readers, but the board is hidden from them")
            if not attrs["note"]:
                fail("A8", f"the {g} game: a change of setup is not announced")
            if g == "dice":
                for setup in ("equal", "slow3"):
                    pg.click(f"[data-setup={setup}]"); pg.click("[data-play]"); pg.wait_for_timeout(100)
                    res = pg.evaluate("""() => ({text: document.querySelector('[data-result]').textContent,
                        board: [...document.querySelectorAll('.st')].slice(1).map(st => +(st.querySelector('.pile-n').textContent || 0))})""")
                    said = {int(st): int(n) for n, st in re.findall(r"(\d+) at station (\d)", res["text"])}
                    for i, n in enumerate(res["board"], start=2):
                        if said.get(i) != n:
                            fail("A8", f"the dice game, setup {setup}: the result says {said.get(i)} waiting at station {i}; the board shows {n}")
            elif g == "waiting":
                # the reader's own call first: the plans show after it (J8)
                pg.click("[data-pick=fix]"); pg.click("[data-pick=reorder]"); pg.click("[data-play]"); pg.wait_for_timeout(100)
                for setup in ("biggest", "stop", "test"):
                    pg.click(f"[data-setup={setup}]"); pg.click("[data-play]"); pg.wait_for_timeout(100)
                    res = pg.evaluate("""() => ({text: document.querySelector('[data-result]').textContent, cost: document.querySelector('[data-cost]').textContent,
                        rows: Object.fromEntries([...document.querySelectorAll('[data-row]')].map(r => [r.getAttribute('data-row'), r.querySelectorAll('.wk.is-wait, .wk.is-build').length]))})""")
                    jobs = yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "waitgame.yaml"), encoding="utf-8"))["jobs"]
                    for j in jobs:
                        m_ = re.search(re.escape(j["short"]) + r"(?: went live)? (?:in|after) week (\d+)", res["text"])
                        if not m_ or int(m_.group(1)) != res["rows"].get(j["id"]):
                            fail("A8", f"the waiting game, {setup}: the result says {j['short']} went live in week {m_.group(1) if m_ else 'none'}; the board shows {res['rows'].get(j['id'])} weeks before it was live")
                    if res["cost"] not in res["text"]:
                        fail("A8", f"the waiting game, {setup}: the result doesn't say what the board's tally does, {res['cost']}")
                    for j in jobs:
                        if not re.search(re.escape(j["short"]) + r"(?: \w+)? (?:was worth|\$[\d,]+)|" + re.escape(j["tag"]) + r" \w+: it was worth", res["text"], re.I):
                            fail("A8", f"the waiting game, {setup}: the result doesn't say what {j['short']} turned out to be worth")
                # a pick left for later: the run waits when it falls due, and says so
                pg.goto(base + f"/pm/{mid}/")
                pg.check("input[name=waiting-guess][value=swaps]"); pg.click("[data-pick=fix]"); pg.click("[data-play]"); pg.wait_for_timeout(100)
                st = pg.evaluate("""() => ({week: document.querySelector('[data-week]').textContent, report: document.querySelector('[data-report]').textContent, result: document.querySelector('[data-result]').textContent})""")
                if st["week"] != "2" or "answer is in" not in st["report"] or st["result"]:
                    fail("A8", f"the waiting game: with the next pick left open, the run doesn't wait at week 2 and give the test's answer in words ({st})")
            else:
                pg.click("[data-setup=trial]"); pg.click("[data-play]"); pg.wait_for_timeout(100)
                res = pg.evaluate("""() => ({text: document.querySelector('[data-result]').textContent, n: document.querySelectorAll('.rk-dot.is-trial.is-worst').length, ringed: document.querySelectorAll('.rk-dot.is-trial').length})""")
                m_ = re.search(r"Of the five worst stores, (none|one|two|three|four|five|\d+) ha", res["text"])
                said = ["none", "one", "two", "three", "four", "five"].index(m_.group(1)) if m_ and not m_.group(1).isdigit() else int(m_.group(1)) if m_ else -1
                if said != res["n"] or not res["ringed"]:
                    fail("A8", f"the ranking game, trial: the result says {said} of the five worst have the fix; the board shows {res['n']}")
                for setup in ("equal", "funnel"):
                    pg.click(f"[data-setup={setup}]"); pg.click("[data-play]"); pg.wait_for_timeout(100)
                    res = pg.evaluate("""() => ({text: document.querySelector('[data-result]').textContent,
                        small: document.querySelectorAll('.rk-col[data-col="0"] .rk-dot.is-worst').length, out: document.querySelectorAll('.rk-dot.is-out').length})""")
                    m_ = re.search(r"five worst stores were (all small|(\d+) small)", res["text"])
                    said = 5 if m_ and m_.group(1) == "all small" else int(m_.group(2)) if m_ and m_.group(2) else 0
                    if said != res["small"]:
                        fail("A8", f"the ranking game, {setup}: the result says {said} small stores in the five worst; the board shows {res['small']}")
                    if setup == "funnel":
                        o = re.search(r"(\d+) other stores?", res["text"])
                        n_out = (0 if "stayed inside" in res["text"] else 1) + (int(o.group(1)) if o else 0)
                        if n_out != res["out"]:
                            fail("A8", f"the ranking game, funnel: the result puts {n_out} stores outside the funnel; the board shows {res['out']}")
            c.close()
        except Exception as e:  # a broken page must fail its rule, not stop the suite
            fail("A8", f"the {g} game: check could not finish: {str(e).splitlines()[0][:160]}")

    # A9: focus is never dropped
    try:
        c = ctx(viewport={"width": 1280, "height": 900}); pg = c.new_page(); pg.set_default_timeout(8000)
        for g, mid in GAMES.items():
            pg.goto(base + f"/pm/{mid}/")
            if g == "waiting":
                pg.click("[data-pick=fix]"); pg.click("[data-pick=reorder]")
            pg.focus("[data-play]"); pg.keyboard.press("Enter"); pg.wait_for_timeout(500)
            if not pg.evaluate("document.activeElement.matches('[data-play]')"):
                fail("A9", f"the {g} game: pressing Play drops focus while the game runs")
            pg.wait_for_timeout(4500)
            if not pg.evaluate("document.activeElement.matches('[data-play]')"):
                fail("A9", f"the {g} game: focus is not on Play when the game finishes")
        pg.goto(base + "/pm/all/")
        target = pg.evaluate("[...document.querySelectorAll('.unit-nav a')].map(a => a.getAttribute('href')).pop()")
        pg.focus(f".unit-nav a[href='{target}']"); pg.keyboard.press("Enter"); pg.wait_for_timeout(200)
        if not pg.evaluate("(t) => document.activeElement === document.querySelector(t + ' h1')", target):
            fail("A9", f"choosing {target} in the single document does not move focus to its title")
        c.close()
    except Exception as e:  # a broken page must fail its rule, not stop the suite
        fail("A9", f"check could not finish: {str(e).splitlines()[0][:160]}")


# ---------- R6: numbers in circles, measured from rendered pixels ----------
JS_STEP_BOXES = """() => [...document.querySelectorAll('.step')].filter(s => s.getClientRects().length).map(s => {
    const m = s.querySelector('.tick-mark').getBoundingClientRect(); const h = s.querySelector('h3');
    const r = document.createRange(); r.selectNodeContents(h); const l = r.getClientRects()[0];
    const cs = getComputedStyle(h), cv = document.createElement('canvas').getContext('2d'); cv.font = cs.fontWeight + ' 100px ' + cs.fontFamily;
    const cap = cv.measureText('H').actualBoundingBoxAscent / 100 * parseFloat(cs.fontSize);
    return {m: [m.left + scrollX, m.top + scrollY, m.width, m.height], t: [l.left + scrollX, l.top + scrollY, l.width, l.height], cap, name: h.textContent.trim().slice(0, 30)}; })"""


def _lum(p):
    return 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]


def _is_orange(p):
    return p[0] > 140 and p[0] - p[2] > 90 and p[1] < 160


def _shot(pg, x, y, w, h, scale):
    import io
    return Image.open(io.BytesIO(pg.screenshot(full_page=True, clip={"x": x, "y": y, "width": w, "height": h}))).convert("RGB")


def _numeral(im, cx, cy, rad, ground):
    """Bounding box of the numeral: pixels inside the circle that stand out from its ground."""
    px = im.load(); pts = []
    for y in range(max(0, int(cy - rad)), min(im.height, int(cy + rad) + 1)):
        for x in range(max(0, int(cx - rad)), min(im.width, int(cx + rad) + 1)):
            p = px[x, y]
            if ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 < 0.72 * rad and abs(_lum(p) - ground) > 90 and not _is_orange(p):
                pts.append((x, y))
    if not pts:
        return None
    return min(a for a, _ in pts), max(a for a, _ in pts), min(b for _, b in pts), max(b for _, b in pts)


def _judge(where, size, cx, cy, box, rule_size=0.40, rule_off=0.03):
    l, r, t, b = box
    if (b - t + 1) / size < rule_size:
        fail("R6", f"{where}: the numeral is {(b - t + 1) / size:.0%} of the circle's height, needs {rule_size:.0%}")
    dx, dy = ((l + r) / 2 - cx) / size, ((t + b) / 2 - cy) / size
    if abs(dx) > rule_off or abs(dy) > rule_off:
        fail("R6", f"{where}: the numeral sits off centre by {dx:+.1%} across and {dy:+.1%} down")


PRINT_TITLE_CAP = {}  # the step title's capital height in print, in CSS pixels, for the PDF check


def circle_checks(ctx, base):
    checked("R6")
    S = 4
    pad_print = "@media print { body { padding-left: 24px !important; } }"  # the page margin, so the ring is not cut off
    # Short-path step circles: numeral, centring, and line-up with the step's title
    for module, (media, w, scheme) in [(m, v) for m, _ in MODULES for v in (("screen", 390, "light"), ("screen", 1280, "light"), ("screen", 1280, "dark"), ("print", 662, "light"))]:
        c = ctx(viewport={"width": w, "height": 900}, device_scale_factor=S, color_scheme=scheme); pg = c.new_page()
        pg.goto(base + module)
        if media == "print":
            pg.emulate_media(media="print", color_scheme=scheme); pg.add_style_tag(content=pad_print)
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(200)
        paper = _lum(tuple(int(v) for v in re.findall(r"\d+", pg.evaluate("getComputedStyle(document.body).backgroundColor"))[:3])) if media == "screen" else 255
        for bx in pg.evaluate(JS_STEP_BOXES):
            where = f"{module} {media} {w}px {scheme}, step '{bx['name']}'"
            mx, my, mw, mh = bx["m"]; tx, ty, tw, th = bx["t"]; pad = 6
            x0, y0 = mx - pad, min(my, ty) - pad
            im = _shot(pg, x0, y0, (tx + tw) - x0 + 2, max(my + mh, ty + th) - y0 + pad, S); px = im.load()
            ring = [(x, y) for y in range(im.height) for x in range(int((mw + 2 * pad) * S)) if _is_orange(px[x, y])]
            if not ring:
                fail("R6", f"{where}: no drawn ring found"); continue
            rl, rr, rt, rb = min(a for a, _ in ring), max(a for a, _ in ring), min(b for _, b in ring), max(b for _, b in ring)
            size, cx, cy = rb - rt + 1, (rl + rr) / 2, (rt + rb) / 2
            box = _numeral(im, cx, cy, size / 2, paper)
            if not box:
                fail("R6", f"{where}: no numeral found in the ring"); continue
            _judge(where, size, cx, cy, box)
            # the title's first line: the baseline ends the dense band of letters; the capitals rise from it by the font's cap height
            # (quotation marks and tall letters such as l and h reach above the capitals, so the top of the ink is not used)
            if media == "print":
                PRINT_TITLE_CAP["px"] = bx["cap"]
            ox, oy = int((tx - x0) * S), int((ty - y0) * S)
            counts = [sum(1 for x in range(ox, min(im.width, ox + int(tw * S))) if abs(_lum(px[x, y]) - paper) > 90 and not _is_orange(px[x, y])) for y in range(oy, min(im.height, oy + int(th * S)))]
            inked = [i for i, n in enumerate(counts) if n]
            if not inked:
                continue
            dense = [i for i, n in enumerate(counts) if n >= 0.3 * max(counts)]
            title_mid = oy + dense[-1] - bx["cap"] * S / 2
            if abs(cy - title_mid) / size > 0.05:
                fail("R6", f"{where}: the circle sits {(cy - title_mid) / size:+.1%} of its size {'below' if cy > title_mid else 'above'} the middle of the title's capitals")
        c.close()
    # Filled discs: the dice game's stations (screen) and the numbered steps in a card's picture (screen and print)
    for media, path, sel in (("screen", "/pm/find-the-constraint/", ".st-name"), ("screen", "/pm/cards/five-focusing-steps/", ".fig-stops circle"),
                             ("print", "/pm/cards/five-focusing-steps/", ".fig-stops circle")):
        for scheme in (("light", "dark") if media == "screen" else ("light",)):
            c = ctx(viewport={"width": 1280, "height": 900}, device_scale_factor=S, color_scheme=scheme); pg = c.new_page()
            pg.goto(base + path)
            if media == "print":
                pg.emulate_media(media="print", color_scheme=scheme); pg.add_style_tag(content=pad_print)
            pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(200)
            if sel == ".st-name":
                # A station's number is text in a drawn disc. A browser puts text on whole pixels, so how the number sits
                # depends on where the page above happens to end: one more line of small text moves the disc half a pixel.
                # Measure with the discs on the pixel grid, so the rule judges the design and not the page's length (spec R6).
                pg.evaluate("""(s) => { const f = (document.querySelector(s).getBoundingClientRect().top + scrollY) % 1;
                    if (f) document.querySelector('main').style.paddingTop = (1 - f) + 'px'; }""", sel)
            rects = pg.evaluate("(s) => [...document.querySelectorAll(s)].map(e => { const r = e.getBoundingClientRect(); return [r.left + scrollX, r.top + scrollY, r.width, r.height]; })", sel)
            for i, (x, y, w, h) in enumerate(rects, start=1):
                where = f"{media} {scheme} {path} {sel} {i}"
                pad = 2; im = _shot(pg, x - pad, y - pad, w + 2 * pad, h + 2 * pad, S); px = im.load()
                cx, cy, rad = im.width / 2, im.height / 2, min(w, h) * S / 2
                band = sorted(_lum(px[int(cx + rad * 0.88 * a), int(cy + rad * 0.88 * b)]) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1), (0.7, 0.7), (-0.7, 0.7), (0.7, -0.7), (-0.7, -0.7)))
                box = _numeral(im, cx, cy, rad, band[len(band) // 2])
                if not box:
                    fail("R6", f"{where}: no numeral found"); continue
                _judge(where, 2 * rad, cx, cy, box)
            c.close()


# ---------- T4 to T8, W4: the type and spacing scales, as the reader meets them ----------
FS_TOKENS = ["small", "body", "head", "title", "door"]      # screen; print drops "door"
LH_TOKENS = ["tight", "head", "text"]
SP_TOKENS = [str(i) for i in range(1, 9)]
FACES = {("libre franklin", "800", "normal"), ("libre franklin", "700", "normal"),
         ("newsreader", "400", "normal"), ("newsreader", "400", "italic"), ("newsreader", "600", "normal"), ("newsreader", "600", "italic"),
         ("public sans", "400", "normal"), ("public sans", "600", "normal"), ("public sans", "400", "italic"),
         ("shantell sans", "400", "normal"), ("shantell sans", "600", "normal")}
# Not judged against the scales: text inside pictures (the figures and the drawn step marks), hidden text,
# the highlighter, and the step circle's box, which R6 places from its title.
SCALE_EXEMPT = "svg, .sr, .skip, script, style, mark, .tick, .tick-mark"

JS_TOKENS = """([fs, lh, sp]) => {
  const probe = css => { const d = document.createElement('div'); d.style.cssText = 'position:absolute;visibility:hidden;' + css; document.body.appendChild(d); const s = getComputedStyle(d); const v = {fs: parseFloat(s.fontSize), lh: parseFloat(s.lineHeight), mt: parseFloat(s.marginTop), set: s.fontSize}; d.remove(); return v; };
  const has = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim() !== '';
  return {fs: Object.fromEntries(fs.filter(t => has('--fs-' + t)).map(t => [t, probe('font-size: var(--fs-' + t + ')').fs])),
          lh: Object.fromEntries(lh.filter(t => has('--lh-' + t)).map(t => [t, probe('font-size: 100px; line-height: var(--lh-' + t + ')').lh / 100])),
          sp: Object.fromEntries(sp.filter(t => has('--sp-' + t)).map(t => [t, probe('margin-top: var(--sp-' + t + ')').mt]))}; }"""

JS_SCALE_SCAN = """([exempt]) => {
  const type = [], space = [], heads = [];
  const shown = (el, cs) => el.getClientRects().length && cs.display !== 'none' && cs.visibility !== 'hidden' && !el.closest('dialog:not([open]), [hidden]');
  const name = el => el.tagName.toLowerCase() + (el.classList.length ? '.' + [...el.classList].join('.') : '');
  const face = cs => [cs.fontFamily.split(',')[0].replace(/["']/g, '').trim().toLowerCase(), String(cs.fontWeight), cs.fontStyle === 'normal' ? 'normal' : 'italic'];
  const text = (where, cs, sample) => type.push({where, size: parseFloat(cs.fontSize), face: face(cs), lh: cs.lineHeight === 'normal' ? null : parseFloat(cs.lineHeight) / parseFloat(cs.fontSize), sample});
  for (const el of document.body.querySelectorAll('*')) {
    if (el.closest(exempt)) continue;
    const cs = getComputedStyle(el); if (!shown(el, cs)) continue;
    const own = [...el.childNodes].filter(n => n.nodeType === 3 && n.textContent.trim()).map(n => n.textContent.trim()).join(' ');
    if (own) text(name(el), cs, own.slice(0, 30));
    for (const pseudo of ['::before', '::after']) {
      const ps = getComputedStyle(el, pseudo); const c = ps.content || 'none';
      if (c === 'none' || c === 'normal' || /^"\\s*"/.test(c) || ps.display === 'none' || ps.clipPath.startsWith('inset(50%')) continue;
      text(name(el) + pseudo, ps, c.slice(0, 30));
    }
    if (/^H[1-6]$/.test(el.tagName)) heads.push({level: +el.tagName[1], size: parseFloat(cs.fontSize), where: name(el), sample: el.textContent.trim().slice(0, 30)});
    if (cs.display === 'inline' || cs.display === 'contents') continue;
    const props = ['marginTop', 'marginBottom', 'paddingTop', 'paddingBottom'];
    if (/flex|grid/.test(cs.display)) props.push('rowGap');
    for (const k of props) { const v = parseFloat(cs[k]); if (v) space.push({where: name(el), k, v}); }
  }
  return {type, space, heads}; }"""


def _near(v, values, tol):
    return any(abs(v - x) <= tol for x in values)


def _scale_scan(pg, where, tok, print_media=False, details=True):
    """Judge one rendered page against the scales. Returns nothing; records failures by rule."""
    if details:
        pg.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
    scan = pg.evaluate(JS_SCALE_SCAN, [SCALE_EXEMPT])
    sizes, lhs, sps = list(tok["fs"].values()), list(tok["lh"].values()), [0] + list(tok["sp"].values())
    seen = set()
    for t in scan["type"]:
        if not _near(t["size"], sizes, 0.3) and ("T4", t["where"], round(t["size"], 1)) not in seen:
            seen.add(("T4", t["where"], round(t["size"], 1)))
            fail("T4", f"{where}: {t['where']} is {t['size']:.2f}px, not a size on the scale ('{t['sample']}')")
        if tuple(t["face"]) not in FACES and ("T5", t["where"], tuple(t["face"])) not in seen:
            seen.add(("T5", t["where"], tuple(t["face"])))
            fail("T5", f"{where}: {t['where']} is set in {t['face'][0]} {t['face'][1]} {t['face'][2]} ('{t['sample']}')")
        if (t["lh"] is None or not _near(t["lh"], lhs, 0.02)) and ("T6", t["where"]) not in seen:
            seen.add(("T6", t["where"]))
            fail("T6", f"{where}: {t['where']} has line spacing {'normal' if t['lh'] is None else round(t['lh'], 3)} ('{t['sample']}')")
    for s in scan["space"]:
        if not _near(s["v"], sps, 0.5) and ("T8", s["where"], s["k"], round(s["v"], 1)) not in seen:
            seen.add(("T8", s["where"], s["k"], round(s["v"], 1)))
            fail("T8", f"{where}: {s['where']} {s['k']} is {s['v']:.2f}px, not a step on the spacing scale")
    for a in scan["heads"]:
        for b in scan["heads"]:
            if a["level"] < b["level"] and a["size"] < b["size"] - 0.3 and ("W4", a["where"], b["where"]) not in seen:
                seen.add(("W4", a["where"], b["where"]))
                fail("W4", f"{where}: h{a['level']} '{a['sample']}' ({a['size']:.1f}px) is smaller than h{b['level']} '{b['sample']}' ({b['size']:.1f}px)")


def _judge_tokens(where, tok, print_media):
    want = FS_TOKENS[:-1] if print_media else FS_TOKENS
    for t in want:
        if t not in tok["fs"]:
            fail("T4", f"{where}: size --fs-{t} is not defined")
    for t in LH_TOKENS:
        if t not in tok["lh"]:
            fail("T6", f"{where}: line spacing --lh-{t} is not defined")
    for t in SP_TOKENS:
        if t not in tok["sp"]:
            fail("T8", f"{where}: space --sp-{t} is not defined")
    vals = sorted(tok["fs"][t] for t in want if t in tok["fs"])
    for a, b in zip(vals, vals[1:]):
        if b / a < 1.2 - 1e-3:
            fail("T4", f"{where}: next sizes {a:.1f}px and {b:.1f}px differ by {b / a:.2f} times, needs 1.2")
    if "text" in tok["lh"] and tok["lh"]["text"] < 1.5 - 1e-3:
        fail("T6", f"{where}: text line spacing is {tok['lh']['text']:.2f}, needs at least 1.5")
    sp = [tok["sp"][t] for t in SP_TOKENS if t in tok["sp"]]
    if sp != sorted(sp) or len(set(sp)) != len(sp):
        fail("T8", f"{where}: the spacing steps do not rise: {sp}")


JS_SPILL = """() => { const out = []; const W = document.documentElement.clientWidth;
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
  while ((n = w.nextNode())) {
    if (!n.textContent.trim()) continue; const el = n.parentElement;
    if (!el || el.closest('svg, .sr, .skip, script, style, [hidden], dialog:not([open])')) continue;
    if (getComputedStyle(el).visibility === 'hidden') continue;
    if (getComputedStyle(el).clipPath !== 'none' && el.getBoundingClientRect().width <= 1) continue;   // for screen readers only, as .sr is
    const r = document.createRange(); r.selectNodeContents(n); const rects = [...r.getClientRects()].filter(x => x.width > 0.5); if (!rects.length) continue;
    const fs = parseFloat(getComputedStyle(el).fontSize), vt = Math.max(1.5, 0.3 * fs);
    let box = el; while (box.parentElement && getComputedStyle(box).display === 'inline') box = box.parentElement;
    const b = box.getBoundingClientRect(); const label = box.tagName.toLowerCase() + (box.classList.length ? '.' + [...box.classList].join('.') : '');
    const sample = n.textContent.trim().slice(0, 30);
    // a line edit's new words reach out over the next word by design (H2 holds them to the screen and clear of other text)
    if (!box.matches('.edit ins') && rects.some(t => t.right > b.right + 1.5 || t.left < b.left - 1.5 || t.bottom > b.bottom + vt || t.top < b.top - vt)) { out.push(label + ' spills out of its box: ' + sample); continue; }
    if (rects.some(t => t.right > W + 1 || t.left < -1)) { out.push(label + ' runs past the edge of the screen: ' + sample); continue; }
    for (let a = el.parentElement; a && a !== document.body; a = a.parentElement) {
      const s = getComputedStyle(a); if (s.overflowX === 'visible' && s.overflowY === 'visible') continue;
      const ab = a.getBoundingClientRect();
      if (rects.some(t => t.right > ab.right + 1.5 || t.left < ab.left - 1.5 || t.bottom > ab.bottom + vt || t.top < ab.top - vt)) { out.push(label + ' is cut off by ' + a.tagName.toLowerCase() + '.' + [...a.classList].join('.') + ': ' + sample); break; }
    }
  }
  return [...new Set(out)]; }"""

JS_LINE_LENGTH = """() => { const c = document.createElement('canvas').getContext('2d'); const sample = 'the quick brown fox jumps over a lazy dog and then sits in the sun'; const out = [];
  for (const p of document.querySelectorAll('.prose p, .prose li, .door-text p, .unit-head .question, .look, .deeper-note, .recall summary')) { const r = p.getBoundingClientRect(); if (!r.width) continue; const s = getComputedStyle(p);
    c.font = s.fontStyle + ' ' + s.fontWeight + ' ' + s.fontSize + ' ' + s.fontFamily; const avg = c.measureText(sample).width / sample.length; const chars = p.clientWidth / avg; if (chars > 85) out.push(Math.round(chars)); }
  return [...new Set(out)]; }"""

TEXT_SPACING = "* { line-height: 1.5 !important; letter-spacing: 0.12em !important; word-spacing: 0.16em !important; } p { margin-bottom: 2em !important; }"


def _margin_overlaps(pg, rule, where):
    m = pg.evaluate(JS_MARGIN)
    if not m:
        return
    boxes = sorted((e for e in m["inMargin"] if re.search(r"\bnote\b", e["cls"])), key=lambda b: b["top"])
    for a_, b_ in zip(boxes, boxes[1:]):
        if b_["top"] < a_["bottom"] - 1:
            fail(rule, f"{where}: margin notes overlap at y={b_['top']:.0f}")


def play_checks(ctx, base):
    """J8: playing a game. One layout in the order of play; the next move beside the result; the board brought into
    view when a run starts; the guess answered; a row for each run; the takeaway held until the setups are played; and
    each game's own changes from the designer's review, all at 390 by 844 with reduced motion, as a phone plays it."""
    checked("J8")
    order_js = """(sels) => { const els = sels.map(s => document.querySelector('.game ' + s));
        if (els.some(e => !e)) return 'missing ' + sels[els.findIndex(e => !e)];
        for (let i = 1; i < els.length; i++) if (!(els[i - 1].compareDocumentPosition(els[i]) & Node.DOCUMENT_POSITION_FOLLOWING)) return sels[i - 1] + ' comes after ' + sels[i];
        return ''; }"""
    in_view = """() => { const b = document.querySelector('.game .board').getBoundingClientRect(), bar = document.querySelector('[data-course-bar]');
        const top = bar ? bar.getBoundingClientRect().bottom : 0; return b.top >= top - 2 && b.top < innerHeight / 2; }"""
    shown = "(s) => { const e = document.querySelector(s); return !!e && !e.closest('[hidden]') && e.getClientRects().length > 0; }"
    c = ctx(viewport={"width": 390, "height": 844}, reduced_motion="reduce"); pg = c.new_page(); pg.set_default_timeout(8000)
    for g, mid in GAMES.items():
        where = f"the {g} game"
        try:
            pg.goto(base + f"/pm/{mid}/")
            after = "[data-plans]" if g == "waiting" else "[data-next-move]"
            bad = pg.evaluate(order_js, [".guess", ".board", "[data-play]", "[data-result]", after, "[data-setup]"])
            if bad:
                fail("J8", f"{where}: its parts aren't in the order of play ({bad})")
            short = pg.evaluate("[...document.querySelectorAll('.guess label')].filter(l => l.getBoundingClientRect().height < 43.5).length")
            if short:
                fail("J8", f"{where}: on a phone {short} of the guess's options are shorter than 44 pixels")
            if pg.evaluate(shown, "[data-takeaway]") or not pg.evaluate(shown, "[data-takeaway-hold]"):
                fail("J8", f"{where}: the takeaway shows before any run, or nothing holds its place")
            if g == "dice":
                pg.check("input[name=dice-guess] >> nth=1"); pg.click("[data-play]"); pg.wait_for_timeout(150)
                res = pg.text_content("[data-result]")
                if not pg.evaluate(in_view):
                    fail("J8", f"{where}: a run doesn't bring the board into view under the bar")
                if not res.startswith("Finished ") or not re.search(r"You guessed [^;.]+; over 400,000 runs", res) or not re.search(r"Left waiting: [^.]+\.$", res):
                    fail("J8", f"{where}: the result doesn't lead with what finished, answer the guess with the long run, and end with where work waits: {res[:160]}")
                if pg.text_content("[data-next]") != "Next: 2. Station 3 is slower" or not pg.evaluate(shown, "[data-next]"):
                    fail("J8", f"{where}: after the first run there's no \"Next: 2. Station 3 is slower\" under the result")
                if pg.evaluate(shown, "[data-takeaway]"):
                    fail("J8", f"{where}: the takeaway shows after the first run")
                pg.click("[data-next]"); pg.wait_for_timeout(150)
                st = pg.evaluate("""() => ({pressed: document.querySelector('[data-setup][aria-pressed=true]').getAttribute('data-setup'), round: document.querySelector('[data-round]').textContent,
                    focus: document.activeElement.matches('[data-play]'), rows: document.querySelectorAll('[data-runs] tbody tr').length})""")
                if st != {"pressed": "slow3", "round": "20", "focus": True, "rows": 2}:
                    fail("J8", f"{where}: Next doesn't pick the next line and play it, keeping focus on Play, with a row for each run ({st})")
                pg.click("[data-next]"); pg.click("[data-next]"); pg.wait_for_timeout(150)
                if not pg.evaluate(shown, "[data-next-done]") or not pg.evaluate(shown, "[data-takeaway]"):
                    fail("J8", f"{where}: after the fourth line it doesn't say that's all four, or the takeaway stays hidden")
            elif g == "waiting":
                st = pg.evaluate("""() => ({pressed: document.querySelectorAll('.game [aria-pressed=true]').length, checked: document.querySelectorAll('.game input:checked').length,
                    plans: !!document.querySelector('[data-plans]').closest('[hidden]'), tally: document.querySelector('.tally').textContent})""")
                if st["pressed"] or st["checked"]:
                    fail("J8", f"{where}: something is chosen before the reader chooses it ({st['pressed']} pressed, {st['checked']} checked)")
                if not st["plans"]:
                    fail("J8", f"{where}: the plans show before the reader's own call")
                if "Cost of delay so far" not in st["tally"]:
                    fail("J8", f"{where}: the tally doesn't read \"Cost of delay so far\"")
                pg.click("[data-play]"); pg.wait_for_timeout(100)
                if "Pick the job to build first" not in (pg.text_content("[data-play-status]") or "") or pg.text_content("[data-week]") != "0":
                    fail("J8", f"{where}: Play with no first job doesn't say so beside Play")
                pg.check("input[name=waiting-guess][value=swaps]"); pg.click("[data-pick=fix]"); pg.click("[data-play]"); pg.wait_for_timeout(150)
                st = pg.evaluate("""() => ({buttons: document.querySelectorAll('[data-pause]:not([hidden]) [data-pause-list] button').length, focus: !!document.activeElement.closest('[data-pause]'),
                    play: !!document.querySelector('.game [data-play]').closest('[hidden]') || document.querySelector('.game [data-play]').hidden,
                    ask: document.querySelector('[data-pause]').textContent.includes('Which job next?'), report: document.querySelector('[data-report]').textContent})""")
                if st["buttons"] != 2 or not st["focus"] or not st["play"] or not st["ask"] or "is live" not in st["report"]:
                    fail("J8", f"{where}: where the run stops it doesn't ask \"Which job next?\" under the week's report, one button for each job left, focus on the first, in Play's place ({st})")
                pg.click("[data-pause-list] button"); pg.wait_for_timeout(150)
                res = pg.text_content("[data-result]")
                if not re.match(r"(No order could have done better|Your order cost \$[\d,]+ more than the cheapest)", res) or "You guessed swap approvals" not in res:
                    fail("J8", f"{where}: the first result doesn't lead with the cost above the cheapest and answer the guess: {res[:160]}")
                if not pg.evaluate(shown, "[data-plans]") or pg.evaluate(shown, "[data-takeaway]"):
                    fail("J8", f"{where}: after the reader's own call the plans don't show, or the takeaway already does")
                pg.click("[data-setup=est]"); pg.wait_for_timeout(150)
                if pg.text_content("[data-week]") == "0" or not pg.evaluate(shown, "[data-takeaway]") or pg.evaluate("document.querySelectorAll('[data-runs] tbody tr').length") != 2:
                    fail("J8", f"{where}: a plan doesn't play at once, keep a row for its run, and show the takeaway after the reader's own call")
                if pg.evaluate("document.querySelectorAll('.wk-ruler .wk-n').length") < 1 or "live after week" not in pg.evaluate("[...document.querySelectorAll('.wk-name')].map(n => n.textContent).join(' ')"):
                    fail("J8", f"{where}: no ruler counts the weeks, or a row doesn't say when its job went live")
            else:
                labels = pg.evaluate("[...document.querySelectorAll('[data-setup]')].map(b => b.textContent)")
                if len(labels) != 4 or labels[0] != "Every store the same":
                    fail("J8", f"{where}: its setups should be four, the first \"Every store the same\": {labels}")
                pg.check("input[name=ranking-guess] >> nth=0"); pg.click("[data-play]"); pg.wait_for_timeout(150)
                res = pg.text_content("[data-result]")
                if not pg.evaluate(in_view):
                    fail("J8", f"{where}: a week doesn't bring the board into view under the bar")
                if not re.search(r"You guessed [^.]+\. Over many weeks about \d of the five worst are small", res) or pg.evaluate(shown, "[data-next]"):
                    fail("J8", f"{where}: the first week doesn't answer the guess with the long run, or offers the next setup before a second week")
                if not re.match(r"Week 1\. Five worst: \d small\. Five best: \d small\.$", pg.text_content("[data-tally]")):
                    fail("J8", f"{where}: the tally isn't a line of short sentences: {pg.text_content('[data-tally]')}")
                pg.click("[data-play]"); pg.wait_for_timeout(150)
                st = pg.evaluate("""() => ({rings: document.querySelectorAll('.rk-dot.was-worst').length, key: document.querySelector('.board-key').textContent, next: document.querySelector('[data-next]').textContent})""")
                if st["rings"] != 5 or "Ringed: last week's five worst" not in st["key"] or not pg.evaluate(shown, "[data-next]"):
                    fail("J8", f"{where}: from the second week the first setup doesn't ring last week's five worst, name the ring in its key, and offer the next setup ({st})")
                if "Ringed" in pg.evaluate("(() => { document.querySelector('[data-setup=worse]').click(); return document.querySelector('.board-key').textContent; })()"):
                    fail("J8", f"{where}: the key names a ring the board doesn't show")
                pg.click("[data-setup=trial]")
                if pg.text_content("[data-play]") != "Play week 1 of 8":
                    fail("J8", f"{where}: the trial's Play doesn't read \"Play week 1 of 8\"")
                for _ in range(8):
                    pg.click("[data-play]")
                pg.wait_for_timeout(150)
                if "After eight weeks" not in pg.text_content("[data-result]") or not pg.text_content("[data-tally]").startswith("Week 8 of 8.") or not pg.evaluate(shown, "[data-takeaway]"):
                    fail("J8", f"{where}: the trial doesn't end at week 8 with what eight weeks show, or the takeaway stays hidden")
        except Exception as e:  # a broken page must fail its rule, not stop the suite
            fail("J8", f"{where}: check could not finish: {str(e).splitlines()[0][:160]}")
    c.close()


def rail_checks(ctx, base):
    """G6: the glossary's A to Z rail, as a phone's contacts have: on the screen's right edge, below the bar, while the
    page scrolls; each letter a target of 24 pixels or more; the text clear of it; a tap or a drag landing on the
    letter's heading below the bar; and, on a screen too short for it, a row above the list."""
    checked("G6")
    for w, h in ((390, 844), (1280, 900)):
        where = f"/pm/glossary/ {w}px"
        c = ctx(viewport={"width": w, "height": h}, reduced_motion="reduce"); pg = c.new_page(); pg.set_default_timeout(8000)
        try:
            pg.goto(base + "/pm/glossary/")
            pg.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)"); pg.wait_for_timeout(100)
            st = pg.evaluate("""() => { const n = document.querySelector('nav.az'), r = n.getBoundingClientRect(), bar = document.querySelector('[data-course-bar]').getBoundingClientRect();
                const lis = [...n.querySelectorAll('li')].map(l => l.getBoundingClientRect().height);
                const text = Math.max(...[...document.querySelectorAll('.gloss-list dd, .gloss-list dt')].map(e => e.getBoundingClientRect().right));
                const col = document.querySelector('main .unit-body').getBoundingClientRect().right;
                return {fixed: getComputedStyle(n).position === 'fixed', pos: getComputedStyle(n).position, column: col, top: r.top, bottom: r.bottom, right: r.right, left: r.left, bar: bar.bottom, min: Math.min(...lis), text}; }""")
            if w < 700 and (not st["fixed"] or st["top"] < st["bar"] or st["bottom"] > h or st["right"] < w - 24):
                fail("G6", f"{where}: on a phone the A to Z rail doesn't stand on the screen's right edge, below the bar, as the page scrolls ({st})")
            if w >= 700 and (st["pos"] != "sticky" or st["top"] < st["bar"] or st["bottom"] > h or st["right"] > st["column"] + 1):
                fail("G6", f"{where}: on a wide screen the A to Z rail doesn't stick in view inside the column, just right of the list ({st})")
            if st["min"] < 24:
                fail("G6", f"{where}: a letter on the rail is {st['min']:.0f} pixels tall, under the 24 a target needs (R5)")
            if st["text"] > st["left"] + 1:
                fail("G6", f"{where}: the glossary's text runs under the rail")
            pg.click('nav.az a[href="#l-o"]'); pg.wait_for_timeout(150)
            t = pg.evaluate("() => { const r = document.querySelector('#l-o .gloss-letter').getBoundingClientRect(), bar = document.querySelector('[data-course-bar]').getBoundingClientRect(); return [r.top, bar.bottom]; }")
            if t[0] < t[1] - 1 or t[0] > h / 3:
                fail("G6", f"{where}: tapping O on the rail doesn't bring its heading to the top, below the bar ({t})")
            a, s_ = pg.locator("nav.az li").nth(0).bounding_box(), pg.locator("nav.az li").nth(18).bounding_box()
            pg.mouse.move(a["x"] + a["width"] / 2, a["y"] + 4); pg.mouse.down()
            pg.mouse.move(s_["x"] + s_["width"] / 2, s_["y"] + s_["height"] / 2, steps=8); pg.mouse.up(); pg.wait_for_timeout(150)
            top = pg.evaluate("() => { const bar = document.querySelector('[data-course-bar]').getBoundingClientRect().bottom; const h = [...document.querySelectorAll('.gloss-letter')].find(e => { const r = e.getBoundingClientRect(); return r.top >= bar - 1 && r.bottom > bar; }); return h ? h.textContent.trim() : ''; }")
            if top != "S":
                fail("G6", f"{where}: dragging along the rail from A to S doesn't bring S's heading to the top (it shows {top or 'none'})")
            pg.wait_for_timeout(300)
            mark = pg.evaluate("() => { const a = document.querySelector('nav.az a.is-here'), o = document.querySelector('nav.az a[href=\"#l-a\"]'); return [a ? a.textContent.trim() : '', a ? getComputedStyle(a).color : '', getComputedStyle(o).color]; }")
            if mark[0] != "S" or mark[1] == mark[2]:
                fail("G6", f"{where}: with S's terms under the bar, S isn't the letter marked on the rail in its own color ({mark})")
            # scrolling alone, no letter tapped: the letter whose terms are under the bar is the one marked
            pg.evaluate("window.scrollTo(0, 0)"); pg.wait_for_timeout(200)
            pg.evaluate("() => { const h = document.querySelector('#l-p'); window.scrollTo(0, h.getBoundingClientRect().top + window.scrollY - document.querySelector('[data-course-bar]').offsetHeight - 4); }")
            pg.wait_for_timeout(300)
            here = pg.evaluate("() => [...document.querySelectorAll('nav.az a.is-here')].map(a => a.textContent.trim())")
            if here != ["P"]:
                fail("G6", f"{where}: scrolled to P's terms, the rail marks {here}, not P alone")
            pg.click('nav.az a[href="#l-w"]'); pg.wait_for_timeout(300)
            lit = pg.evaluate("() => { const ink = getComputedStyle(document.querySelector('nav.az span')).color; const a0 = getComputedStyle(document.querySelector('nav.az a[href=\"#l-b\"]')).color; return [...document.querySelectorAll('nav.az a')].filter(a => getComputedStyle(a).color !== a0 || a.classList.contains('is-here')).map(a => a.textContent.trim()); }")
            if lit != ["W"]:
                fail("G6", f"{where}: after tapping W at the page's end, the rail lights {lit}, not W alone")
            if w >= 700:
                pg.evaluate("window.scrollTo(0, document.body.scrollHeight)"); pg.wait_for_timeout(100)
                e = pg.evaluate("() => [document.querySelector('nav.az').getBoundingClientRect().bottom, document.querySelector('footer').getBoundingClientRect().top]")
                if e[0] > e[1]:
                    fail("G6", f"{where}: at the page's end the rail runs into the foot ({e})")
            pg.goto(base + "/pm/glossary/#g-constraint"); pg.wait_for_timeout(150)
            t = pg.evaluate("() => { const e = document.querySelector('#g-constraint dt').getBoundingClientRect(), hd = document.querySelector('#l-c .gloss-letter').getBoundingClientRect(); return [e.top, hd.bottom]; }")
            if t[0] < t[1] - 1:
                fail("G6", f"{where}: an entry reached by its address lands under its letter's heading ({t})")
            c.close()
        except Exception as e:  # a broken page must fail its rule, not stop the suite
            fail("G6", f"{where}: rail check could not finish: {str(e).splitlines()[0][:160]}"); c.close()
    c = ctx(viewport={"width": 844, "height": 390}); pg = c.new_page()
    try:
        pg.goto(base + "/pm/glossary/")
        if pg.evaluate("getComputedStyle(document.querySelector('nav.az')).position") == "fixed":
            fail("G6", "/pm/glossary/ 844 by 390: on a screen too short for the rail, it doesn't lie flat above the list")
    finally:
        c.close()


def scale_checks(ctx, base):
    checked("T2", "T4", "T5", "T6", "T7", "T8", "W4", "R7", "A13")
    normal = {}
    for w in (390, 1280):
        c = ctx(viewport={"width": w, "height": 900}, color_scheme="light", reduced_motion="reduce"); pg = c.new_page()
        for path in PAGES:
            pg.goto(base + path); pg.evaluate("document.fonts.ready")
            where = f"{path} {w}px"
            tok = pg.evaluate(JS_TOKENS, [FS_TOKENS, LH_TOKENS, SP_TOKENS])
            if path == "/pm/find-the-constraint/":
                normal[w] = tok
                _judge_tokens(f"screen {w}px", tok, False)
                pg.click("[data-setup=fast3]"); pg.click("[data-play]"); pg.wait_for_timeout(100)   # the result and takeaway show once the last line is played (J8)
                pg.evaluate("document.querySelector('dialog.gloss').show()")   # a glossary definition, as it opens in place
            _scale_scan(pg, where, tok)
        c.close()
    # Print: the single document as it prints, on the Letter page's text width
    c = ctx(viewport={"width": 662, "height": 900}, color_scheme="light"); pg = c.new_page()
    pg.goto(base + "/pm/all/"); pg.emulate_media(media="print"); pg.evaluate("document.fonts.ready")
    tok = pg.evaluate(JS_TOKENS, [FS_TOKENS, LH_TOKENS, SP_TOKENS])
    _judge_tokens("print", tok, True)
    _scale_scan(pg, "print /pm/all/", tok)
    c.close()

    # T2 between phone and desktop, where the reading column is widest before the margin appears
    for w in (600, 768, 900):
        c = ctx(viewport={"width": w, "height": 900}); pg = c.new_page()
        for path in PAGES:
            pg.goto(base + path); pg.evaluate("document.fonts.ready")
            for n in pg.evaluate(JS_LINE_LENGTH):
                fail("T2", f"{path} {w}px: reading lines run to about {n} characters")
        c.close()

    # T7 and R7: the browser's default text size doubled, as a reader with low vision might set it
    for w in (390, 1280):
        c = ctx(viewport={"width": w, "height": 900}); pg = c.new_page()
        cdp = c.new_cdp_session(pg); cdp.send("Page.enable"); cdp.send("Page.setFontSizes", {"fontSizes": {"standard": 32}})
        for path in PAGES:
            pg.goto(base + path); pg.evaluate("document.fonts.ready")
            where = f"{path} {w}px, text size doubled"
            if pg.evaluate("getComputedStyle(document.documentElement).fontSize") != "32px":
                fail("R7", f"{where}: the browser setting did not take effect"); break
            if path == "/pm/find-the-constraint/" and w in normal:
                big = pg.evaluate(JS_TOKENS, [FS_TOKENS, LH_TOKENS, SP_TOKENS])
                for kind, names in (("fs", ("small", "body", "head")), ("sp", ("2", "4", "7"))):
                    for t in names:
                        a, b = normal[w][kind].get(t), big[kind].get(t)
                        if a and b and b / a < 1.9:
                            fail("T7", f"{w}px: --{kind}-{t} grows {b / a:.2f} times when the reader doubles their text size, expected 2")
            if pg.evaluate("document.documentElement.scrollWidth") > w:
                fail("R7", f"{where}: scrolls sideways")
            for s in pg.evaluate(JS_SPILL):
                fail("R7", f"{where}: {s}")
            if w == 1280:
                _margin_overlaps(pg, "R7", where)
        c.close()

    # A13: the reader's own text spacing (WCAG 1.4.12)
    for w in (320, 1280):
        c = ctx(viewport={"width": w, "height": 900}); pg = c.new_page()
        for path in PAGES:
            pg.goto(base + path); pg.add_style_tag(content=TEXT_SPACING); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(50)
            where = f"{path} {w}px, text spacing overridden"
            if pg.evaluate("document.documentElement.scrollWidth") > w:
                fail("A13", f"{where}: scrolls sideways")
            for s in pg.evaluate(JS_SPILL):
                fail("A13", f"{where}: {s}")
            if w == 1280:
                _margin_overlaps(pg, "A13", where)
        c.close()


def engine_checks(p, base):
    """R8: the responsive and scale checks again, in WebKit (Safari's engine) and Firefox."""
    checked("R8")
    for eng in ("webkit", "firefox"):
        try:
            b = getattr(p, eng).launch()
        except Exception as e:
            fail("R8", f"{eng} could not start ({str(e).splitlines()[0][:80]}); install it with: python3 -m playwright install webkit firefox")
            continue
        label = "WebKit" if eng == "webkit" else "Firefox"
        for w in (390, 1280):
            kw = {"viewport": {"width": w, "height": 900}}
            if eng == "webkit" and w == 390:
                d = dict(p.devices["iPhone 13"]); d.pop("default_browser_type", None); kw = d
            for cond in ("normal", "text doubled", "text spacing"):
                c = b.new_context(**kw); pg = c.new_page()
                for path in PAGES:
                    # the single document is long; a page that stalls once is loaded again in a fresh tab before
                    # the run gives up, so one slow load can't hide every check after it
                    for attempt in (1, 2):
                        try:
                            pg.goto(base + path, timeout=60000); pg.wait_for_load_state("load", timeout=60000)
                            break
                        except Exception:
                            if attempt == 2:
                                raise
                            pg.close(); pg = c.new_page()
                    if cond == "text doubled":   # WebKit and Firefox take no default-size setting here; doubling the root size is the same for rem
                        pg.add_style_tag(content="html { font-size: 200% !important; }")
                    elif cond == "text spacing":
                        pg.add_style_tag(content=TEXT_SPACING)
                    pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(30)
                    where = f"{label} {path} {pg.viewport_size['width']}px" + ("" if cond == "normal" else f", {cond}")
                    rule = {"normal": "R1", "text doubled": "R7", "text spacing": "A13"}[cond]
                    if pg.evaluate("document.documentElement.scrollWidth") > pg.viewport_size["width"]:
                        fail(rule, f"{where}: scrolls sideways")
                    for s in pg.evaluate(JS_SPILL):
                        fail(rule, f"{where}: {s}")
                    if cond == "normal":
                        tok = pg.evaluate(JS_TOKENS, [FS_TOKENS, LH_TOKENS, SP_TOKENS])
                        _scale_scan(pg, where, tok)
                c.close()
        b.close()


JS_SOURCES = """() => ({
  loose: [...document.querySelectorAll('dl.notes')].filter(d => !d.closest('details.why, .sources-back')).length,
  folds: [...document.querySelectorAll('details.why')].map(d => ({open: d.open, label: (d.querySelector(':scope > summary') || {}).textContent || ''})) })"""

JS_SOURCES_PRINT = """() => [...document.querySelectorAll('.unit')].map(u => {
  const shown = el => el.getClientRects().length > 0 && getComputedStyle(el).visibility !== 'hidden';
  const notes = [...u.querySelectorAll('dl.notes')];
  return {id: u.id, card: u.classList.contains('card'), notes: notes.length,
          inPlaceShown: notes.filter(n => !n.closest('.sources-back') && shown(n)).length,
          backShown: [...u.querySelectorAll('.sources-back dl.notes')].filter(shown).length,
          sourcesInBody: notes.filter(n => !n.closest('.sources-back')).length}; })"""


def sources_checks(ctx, base):
    """S4: reasons fold under each source on screen; print lists them at the back of a module and at the foot of a card."""
    checked("S4")
    for w in (390, 1280):
        c = ctx(viewport={"width": w, "height": 900}); pg = c.new_page()
        for path in UNIT_PAGES:
            pg.goto(base + path)
            r = pg.evaluate(JS_SOURCES)
            if r["loose"]:
                fail("S4", f"{path} {w}px: {r['loose']} source reason list(s) sit open, not folded under 'Why this source'")
            for f_ in r["folds"]:
                if f_["open"]:
                    fail("S4", f"{path} {w}px: a 'Why this source' fold starts open")
                if f_["label"].strip() != "Why this source":
                    fail("S4", f"{path} {w}px: a fold is labelled '{f_['label'].strip()}', not 'Why this source'")
        c.close()
    c = ctx(viewport={"width": 662, "height": 900}); pg = c.new_page()
    pg.goto(base + "/pm/all/"); pg.emulate_media(media="print")
    for u in pg.evaluate(JS_SOURCES_PRINT):
        if not u["notes"]:
            continue
        if u["card"]:
            if u["inPlaceShown"] != u["sourcesInBody"]:
                fail("S4", f"print, card {u['id']}: its source's reasons do not print at its foot")
        else:
            if u["inPlaceShown"]:
                fail("S4", f"print, module {u['id']}: {u['inPlaceShown']} source reason list(s) print in place instead of at the back")
            if u["backShown"] != u["sourcesInBody"]:
                fail("S4", f"print, module {u['id']}: {u['backShown']} reasons at the back for {u['sourcesInBody']} sources")
    c.close()


def _plain(md):
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", str(md))
    return " ".join(re.sub(r"[*_`]", "", t).split())


def sources_pdf_check(pdf):
    """S4 in the PDF itself: each source's reasons print exactly once."""
    text = " ".join(subprocess.run(["pdftotext", pdf, "-"], capture_output=True, text=True).stdout.split())
    text = text.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    # A voice slot in a source's lines (X4) prints its interim words, so the probe reads those.
    slots = {x.get("id"): x.get("interim") or "" for x in (yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "voice-slots.yaml"), encoding="utf-8")) or {}).get("slots") or []}
    for path in glob.glob(os.path.join(ROOT, "content", "pm", "**", "*.md"), recursive=True):
        m = re.match(r"---\n(.*?)\n---", open(path, encoding="utf-8").read(), re.S)
        fm = yaml.safe_load(m.group(1)) if m else {}
        deeper = fm.get("deeper")
        for s_ in (fm.get("steps") or []) + (deeper if isinstance(deeper, list) else [deeper] if deeper else []):
            for key in ("trust", "only"):
                if s_.get(key):
                    said = re.sub(r'\{\{<\s*pm/voice\s+"([^"]+)"[^>]*>\}\}', lambda v: slots.get(v.group(1), ""), str(s_[key]))
                    # Eight words, since every "Why trust it" now opens with one of four tags (S17).
                    probe = " ".join(_plain(said).replace("\u2019", "'").split()[:8])
                    n = text.count(probe)
                    if n != 1:
                        fail("S4", f"PDF: '{probe}' prints {n} times, expected once")


def pdf_ring_checks(pdf):
    """R6 in the PDF itself: Chrome rounds boxes to whole pixels when it prints, so screen checks alone can miss print drift."""
    import numpy as np
    Image.MAX_IMAGE_PIXELS = None
    tmp = tempfile.mkdtemp()
    dpi = 600
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-x", "0", "-y", "0", "-W", str(int(3.4 * dpi)), "-H", str(int(11 * dpi)), pdf, os.path.join(tmp, "p")], capture_output=True)
    found = 0
    for f in sorted(glob.glob(os.path.join(tmp, "p-*.png"))):
        a = np.asarray(Image.open(f).convert("RGB")).astype(int); r, g, b = a[..., 0], a[..., 1], a[..., 2]
        orange = (r > 140) & (r - b > 90) & (g < 160)
        dark = a.max(axis=2) < 75
        page = os.path.basename(f)
        strip = orange[:, int(0.7 * dpi):int(1.25 * dpi)]
        rows = np.where(strip.any(axis=1))[0]
        groups = np.split(rows, np.where(np.diff(rows) > 4)[0] + 1) if len(rows) else []
        for grp in groups:
            t, bt = int(grp[0]), int(grp[-1]); size = bt - t + 1
            cols = np.where(strip[t:bt + 1].any(axis=0))[0]
            if size < 40 and len(cols):  # far smaller than any circle or title letter: a piece of ring left behind by a page break?
                if cols[-1] >= strip.shape[1] - 3 and size <= 16:
                    continue  # a link's underline: a thin line that runs on past the strip into the text, which no ring does
                x0 = int(0.7 * dpi); reg = a[t:bt + 1, x0:x0 + strip.shape[1]]
                # true orange only: dark text on the yellow highlighter blends to orange-ish pixels, but keeps green high
                pen = (reg[..., 0] > 140) & (reg[..., 0] - reg[..., 2] > 90) & (reg[..., 1] < 0.6 * reg[..., 0])
                if pen.sum() >= 15:
                    fail("R6", f"PDF {os.path.basename(f)}: a piece of a step circle prints on its own at {t / dpi:.2f}in")
                continue
            if size < 80 or not len(cols):
                continue
            left, right = int(cols[0]) + int(0.7 * dpi), int(cols[-1]) + int(0.7 * dpi)
            if not 0.85 < (right - left + 1) / size < 1.15:
                continue
            found += 1
            cx, cy = (left + right) / 2, (t + bt) / 2
            yy, xx = np.mgrid[t:bt + 1, left:right + 1]
            inside = ((xx - cx) ** 2 + (yy - cy) ** 2) ** 0.5 < 0.36 * size
            ny, nx = np.where(dark[t:bt + 1, left:right + 1] & inside)
            where = f"PDF {page} step circle at {t / dpi:.2f}in"
            if not len(ny):
                fail("R6", f"{where}: no numeral found"); continue
            _judge(where, size, cx, cy, (left + nx.min(), left + nx.max(), t + ny.min(), t + ny.max()))
            band0, band1 = t - size // 8, bt + size // 8
            counts = dark[band0:band1, right + int(0.05 * dpi):right + int(1.6 * dpi)].sum(axis=1)
            inked = np.where(counts > 0)[0]
            if not len(inked):
                continue
            dense = np.where(counts >= 0.3 * counts.max())[0]
            if "px" not in PRINT_TITLE_CAP:
                fail("R6", "the title's capital height in print was not measured"); continue
            # the title's first line: a title that wraps brings a second line's capitals into the band, after a gap
            first = np.split(dense, np.where(np.diff(dense) > 0.04 * dpi)[0] + 1)[0]
            title_mid = band0 + first[-1] - PRINT_TITLE_CAP["px"] / 96 * dpi / 2
            if abs(cy - title_mid) / size > 0.05:
                fail("R6", f"{where}: the circle sits {(cy - title_mid) / size:+.1%} of its size {'below' if cy > title_mid else 'above'} the middle of the title's capitals")
    if not found:
        fail("R6", "no step circles found in the PDF")
    shutil.rmtree(tmp, ignore_errors=True)


def _norm(t):
    t = str(t).replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("­", "")
    return " ".join(t.split())


def _expected_outline(out_dir):
    """The bookmark tree P6 asks for, read from the single document's HTML."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(open(os.path.join(out_dir, "pm", "all", "index.html"), encoding="utf-8").read(), "html.parser")
    units = []
    for art in soup.select("main article.unit"):
        kind = [c for c in art["class"] if c != "unit"][0]
        h1 = _norm(art.find("h1").get_text(" ", strip=True))
        h2s = [(_norm(h.get_text(" ", strip=True)), _norm(h.get_text(" ", strip=True))) for h in art.find_all("h2")]
        u = {"id": art.get("id"), "kind": kind, "module": art.get("data-module"), "probe": h1}
        if kind == "start":
            u["label"] = f"Start: {h1}"
        elif kind == "module":
            num = re.sub(r"\D", "", art.select_one(".kicker .tag").get_text())
            u["label"] = f"Module {num}: {h1}"
        elif kind == "card":
            u["label"] = f"Card: {h1}"
        elif kind == "closing":
            u["label"] = f"To close: {h1}"
        else:
            u["label"] = h1
        if kind == "glossary":
            u["kids"] = [(_norm(dt.get_text(" ", strip=True)),) * 2 for dt in art.select("dl.gloss-list dt")]
        else:
            u["kids"] = h2s
        units.append(u)
    tree = []
    for u in units:
        if u["kind"] == "card":
            continue
        kids = [(t, p, []) for t, p in u["kids"]]
        if u["kind"] == "module":
            kids += [(c["label"], c["probe"], [(t, p, []) for t, p in c["kids"]]) for c in units if c["kind"] == "card" and c["module"] == u["id"]]
        tree.append((u["label"], u["probe"], kids))
    orphans = [c["label"] for c in units if c["kind"] == "card" and not any(m["id"] == c["module"] and m["kind"] == "module" for m in units)]
    return tree, orphans


def unit_page_checks(pdf_path, n_pages):
    """P1: each unit starts on a page of its own and prints on no more pages than its share.
    Where each unit starts is read from the PDF's bookmarks, which P6 checks against the document."""
    import pikepdf
    with pikepdf.open(pdf_path) as pdf:
        page_index = {p.objgen: i for i, p in enumerate(pdf.pages)}
        names = {str(k).lstrip("/"): v for k, v in pdf.Root.Dests.items()} if "/Dests" in pdf.Root else {}

        def first_page(item):
            d = item.destination if item.destination is not None else (item.action.get("/D") if item.action is not None else None)
            if isinstance(d, (pikepdf.Name, pikepdf.String)):
                d = names.get(str(d).lstrip("/"))
            if isinstance(d, pikepdf.Dictionary) and "/D" in d:
                d = d.D
            try:
                return page_index.get(d[0].objgen)
            except Exception:
                return None

        units = []
        with pdf.open_outline() as ol:
            for top in ol.root:
                kind = ("start" if top.title.startswith("Start:") else "module" if top.title.startswith("Module ")
                        else "closing" if top.title.startswith("To close:") else "glossary")
                deeper = next((first_page(k) for k in top.children if k.title.startswith("Go deeper: the full path")), None)
                units.append((first_page(top), kind, top.title, deeper))
                units += [(first_page(k), "card", k.title, None) for k in top.children if k.title.startswith("Card: ")]
    if any(u[0] is None for u in units):
        fail("P1", "a unit's bookmark does not land on a page, so its pages cannot be counted"); return
    units.sort(key=lambda u: u[0])
    mods_ = yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "modules.yaml"), encoding="utf-8"))
    with_game = {f"Module {m['num']}: {m['title']}" for m in mods_ if m["id"] in GAMES.values()}
    long_ = {f"Module {m['num']}: {m['title']}" for m in mods_ if m["id"] in RUNS_LONG}
    for (pg, kind, title, deeper), nxt in zip(units, units[1:] + [(n_pages, "", "", None)]):
        n = nxt[0] - pg
        # a module's full path prints outside its three pages: it starts within them, and may take two more
        share = UNIT_SHARE[kind] + (DEEPER_PAGES if kind == "module" and deeper is not None else 0)
        # the website first: a module's extra page is noted, not failed, and a module with a game may run further
        grace = (GAME_GRACE if _plain_title(title) in with_game | long_ else MODULE_GRACE) if kind == "module" else CLOSING_GRACE if kind == "closing" else 0
        why_ = "since it runs long on purpose" if _plain_title(title) in long_ else "since it carries a game"
        said = f"'{title}' prints on {n} pages; a {kind} gets {UNIT_SHARE[kind]}{f', and {DEEPER_PAGES} more for its full path' if share > UNIT_SHARE[kind] else ''}"
        if n < 1:
            fail("P1", f"'{title}' starts on PDF page {pg + 1}, which it shares with another unit")
        elif kind == "glossary" and GLOSSARY_GRACE is None and n > share:
            NOTE["P1"].append(said + ", and may run past them until a PDF is published, so every term goes in")
        elif n > share + grace:
            fail("P1", said)
        elif n > share:
            NOTE["P1"].append(said + (f", and may run further, {why_}, until a PDF is published" if grace == GAME_GRACE else ", and may run one page over until a PDF is published"))
        if kind == "module" and deeper is not None and deeper - pg >= UNIT_SHARE["module"]:
            said = f"'{title}' starts its full path on its page {deeper - pg + 1}, so the module itself runs past its {UNIT_SHARE['module']} pages"
            if deeper - pg >= UNIT_SHARE["module"] + grace:
                fail("P1", said)
            else:
                NOTE["P1"].append(said + (f", which it may do, {why_}, until a PDF is published" if grace == GAME_GRACE else ", which it may do by one page until a PDF is published"))


def _plain_title(t):
    """A bookmark's title with the typographer's apostrophe made plain, to match the map's."""
    return t.replace("\u2019", "'")


def pdf_link_meta_checks(pdf_path, out_dir):
    """P5 and P6, read from the PDF file itself."""
    import pikepdf
    from urllib.parse import urlparse
    checked("P5", "P6")
    pdf = pikepdf.open(pdf_path)
    root = pdf.Root
    page_index = {p.objgen: i for i, p in enumerate(pdf.pages)}
    names = {}
    if "/Dests" in root:
        for k, v in root.Dests.items():
            names[str(k).lstrip("/")] = v
    page_text = [_norm(t) for t in subprocess.run(["pdftotext", pdf_path, "-"], capture_output=True, text=True).stdout.split("\f")]
    site_host = urlparse(yaml.safe_load(open(os.path.join(ROOT, "hugo.yaml")))["baseURL"]).hostname

    def dest_page(d):
        if isinstance(d, (pikepdf.Name, pikepdf.String)):
            d = names.get(str(d).lstrip("/"))
            if d is None:
                return None
        if isinstance(d, pikepdf.Dictionary) and "/D" in d:
            d = d.D
        try:
            return page_index.get(d[0].objgen)
        except Exception:
            return None

    # P5: links
    term_links = 0
    for i, page in enumerate(pdf.pages):
        annots = [a for a in page.get("/Annots", []) if a.get("/Subtype") == "/Link"]
        if annots and page.get("/Tabs") != "/S":
            fail("P5", f"PDF page {i + 1} has links but does not follow the tagged order when tabbing (/Tabs /S)")
        for a in annots:
            act = a.get("/A")
            target = None
            if act is not None and act.get("/S") == "/URI":
                uri = str(act.URI); u = urlparse(uri); target = uri
                if u.scheme not in ("https", "http", "mailto") or (u.scheme != "mailto" and not u.hostname):
                    fail("P5", f"PDF page {i + 1}: link to '{uri}' is not a full public address")
                elif u.hostname in ("127.0.0.1", "localhost") or (u.hostname or "").endswith(".local"):
                    fail("P5", f"PDF page {i + 1}: link points to a local address, {uri}")
                elif u.hostname == site_host and u.path.startswith("/pm/"):
                    fail("P5", f"PDF page {i + 1}: link leaves the PDF for {uri}, which the PDF contains")
            else:
                d = a.get("/Dest") if act is None else (act.get("/D") if act.get("/S") == "/GoTo" else None)
                if d is None:
                    fail("P5", f"PDF page {i + 1}: a link has neither a web address nor a place in the PDF"); continue
                target = str(d).lstrip("/") if isinstance(d, (pikepdf.Name, pikepdf.String)) else "page"
                if dest_page(d) is None:
                    fail("P5", f"PDF page {i + 1}: a link goes to '{target}', which is not in the PDF")
                if target.startswith("g-"):
                    term_links += 1
            if not _norm(a.get("/Contents", "")):
                fail("P5", f"PDF page {i + 1}: the link to {target} has no description for screen readers")
    html = open(os.path.join(out_dir, "pm", "all", "index.html"), encoding="utf-8").read()
    want_terms = len(re.findall(r'<a class="term"', html))
    if term_links < want_terms:
        fail("P5", f"{term_links} glossary links jump within the PDF, expected {want_terms}, one per marked term")

    # P6: metadata
    m = re.match(r"---\n(.*?)\n---", open(os.path.join(ROOT, "content", "pm", "all.md"), encoding="utf-8").read(), re.S)
    fm = (yaml.safe_load(m.group(1)) if m else {}) or {}
    want = fm.get("pdf") or {}
    if not (want.get("title") and want.get("subject") and want.get("keywords")):
        fail("P6", "content/pm/all.md has no pdf title, subject and keywords")
    info = {str(k): _norm(v) for k, v in pdf.docinfo.items()}
    author = (yaml.safe_load(open(os.path.join(ROOT, "hugo.yaml"))).get("params") or {}).get("author")
    expect = {"/Title": want.get("title"), "/Subject": want.get("subject"), "/Keywords": ", ".join(want.get("keywords") or []), "/Author": author}
    for k, v in expect.items():
        if not v or info.get(k) != _norm(v):
            fail("P6", f"document information {k[1:]} is '{info.get(k)}', expected '{v}'")
    if not info.get("/Creator") or "Mozilla/" in info.get("/Creator", ""):
        fail("P6", f"document information Creator names a browser, not the tool that made the PDF: '{info.get('/Creator')}'")
    with pdf.open_metadata() as x:
        xmp = {"title": _norm(x.get("dc:title", "")), "creator": _norm(" ".join(x.get("dc:creator", []) or [])),
               "description": _norm(x.get("dc:description", "")), "keywords": _norm(x.get("pdf:Keywords", "")),
               "language": _norm(" ".join(x.get("dc:language", []) or [])), "tool": _norm(x.get("xmp:CreatorTool", ""))}
    for k, d in (("title", "/Title"), ("creator", "/Author"), ("description", "/Subject"), ("keywords", "/Keywords"), ("tool", "/Creator")):
        if not xmp[k] or xmp[k] != info.get(d):
            fail("P6", f"XMP {k} is '{xmp[k]}', which does not match the document information ('{info.get(d)}')")
    if not xmp["language"] or not _norm(root.get("/Lang", "")) or xmp["language"].lower() != _norm(root.get("/Lang", "")).lower():
        fail("P6", f"XMP language '{xmp['language']}' and document language '{root.get('/Lang')}' are missing or disagree")
    if root.get("/PageMode") != "/UseOutlines":
        fail("P6", "the PDF does not open with its bookmarks showing (/PageMode /UseOutlines)")
    vp = root.get("/ViewerPreferences") or {}
    if not bool(vp.get("/DisplayDocTitle", False)):
        fail("P6", "the reader's title bar shows the file name, not the title (/DisplayDocTitle)")

    # P6: bookmarks
    want_tree, orphans = _expected_outline(out_dir)
    for o in orphans:
        fail("P6", f"{o} has no module to sit under")
    with pdf.open_outline() as ol:
        def walk(items, wants, depth):
            got = [it.title for it in items]
            if [_norm(g) for g in got] != [w[0] for w in wants]:
                fail("P6", f"bookmarks at level {depth} read {got}, expected {[w[0] for w in wants]}")
                return
            for it, (label, probe, kids) in zip(items, wants):
                d = it.destination if it.destination is not None else (it.action.get("/D") if it.action is not None else None)
                pg = dest_page(d) if d is not None else None
                if pg is None:
                    fail("P6", f"bookmark '{label}' does not land on a page")
                elif probe and probe not in page_text[pg]:
                    fail("P6", f"bookmark '{label}' lands on page {pg + 1}, where '{probe}' does not print")
                walk(it.children, kids, depth + 1)
        walk(ol.root, want_tree, 1)


def highlighter_checks(ctx, base):
    """C6: every letter on the highlighter sits on the yellow. The words are drawn in pure red, once with the stroke and
    once without; red that lands outside the stroke (with a pixel of slack for antialiasing) is a letter past the yellow."""
    import numpy as np
    checked("C6")
    for scheme in ("light", "dark"):
        c = ctx(viewport={"width": 1280, "height": 900}, color_scheme=scheme, device_scale_factor=2); pg = c.new_page()
        cases = [("/pm/find-the-constraint/", ".one-thing mark", f"hl-v{v}") for v in (1, 2, 3)] + [("/pm/cards/goodharts-law/", ".carry mark", None)]
        for path, sel, variant in cases:   # every variant of the stroke, on the module's line; and a card's question as it is
            pg.goto(base + path); pg.evaluate("document.fonts.ready")
            el = pg.locator(sel)
            if variant:
                el.evaluate("(m, v) => { m.className = v; }", variant)
            el.evaluate("m => { m.style.color = '#ff0000'; m.style.setProperty('-webkit-text-fill-color', '#ff0000'); }")
            box = el.bounding_box(); pad = 8
            clip = {"x": box["x"] - pad, "y": box["y"] - pad, "width": box["width"] + 2 * pad, "height": box["height"] + 2 * pad}
            f1 = tempfile.mktemp(suffix=".png"); pg.screenshot(path=f1, clip=clip, full_page=True)
            el.evaluate("m => { m.style.color = 'transparent'; m.style.setProperty('-webkit-text-fill-color', 'transparent'); }")
            f2 = tempfile.mktemp(suffix=".png"); pg.screenshot(path=f2, clip=clip, full_page=True)
            a = np.asarray(Image.open(f1).convert("RGB")).astype(int); y = np.asarray(Image.open(f2).convert("RGB")).astype(int)
            red = (a[..., 0] > 120) & (a[..., 1] < 0.55 * a[..., 0]) & (a[..., 2] < 0.55 * a[..., 0])
            yellow = (y[..., 0] > 180) & (y[..., 1] > 150) & (y[..., 2] < 140)
            grown = yellow.copy()
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                grown |= np.roll(np.roll(yellow, dy, 0), dx, 1)
            out = red & ~grown
            if out.sum() > 6:
                ys, xs = np.where(out)
                fail("C6", f"{path} {scheme}{' ' + variant if variant else ''}: {int(out.sum())} pixels of the words on the highlighter fall outside the stroke, {'above' if ys.mean() < a.shape[0] / 2 else 'below'} it")
            if os.environ.get("KEEP_C6"): shutil.copy(f1, f"/tmp/c6-{scheme}-{sel[1:4]}-text.png"); shutil.copy(f2, f"/tmp/c6-{scheme}-{sel[1:4]}-band.png")
            os.remove(f1); os.remove(f2)
        c.close()


def variant_checks(ctx, base):
    """H1: the marks come in variants, and neighbours differ."""
    checked("H1")
    c = ctx(viewport={"width": 1280, "height": 900}); pg = c.new_page()
    for module, cards in MODULES:
        pg.goto(base + module)
        rings = pg.evaluate("() => [...document.querySelectorAll('.steps .tick-ring')].map(r => r.getAttribute('d'))")
        if len(set(rings)) < min(3, len(rings)):
            fail("H1", f"{module}: the short path's {len(rings)} circles use {len(set(rings))} drawings, expected {min(3, len(rings))}")
        for i, (a, b) in enumerate(zip(rings, rings[1:])):
            if a == b:
                fail("H1", f"{module}: steps {i + 1} and {i + 2} share one circle")
        strokes = []
        for path, sel in [(module, ".one-thing mark")] + [(c_, ".carry mark") for c_ in cards]:
            pg.goto(base + path)
            strokes.append(pg.evaluate("s => getComputedStyle(document.querySelector(s)).backgroundImage", sel))
        if len(set(strokes)) < 2:
            fail("H1", f"{module}: every highlighted line in the module and its cards uses one stroke")
    variants = pg.evaluate("""() => { const m = document.querySelector('.carry mark'); const out = new Set();
      for (const v of ['hl-v1', 'hl-v2', 'hl-v3']) { m.className = v; out.add(getComputedStyle(m).backgroundImage); } return out.size; }""")
    if variants < 3:
        fail("H1", f"the highlighter has {variants} variants in the chosen hand, expected 3")
    c.close()


# ---------- the working source: one source per unit, mirrored in the doc (X1 to X3), its voice (E1 to E3, S5) and punctuation (T9) ----------
def _source_doc():
    import importlib.util
    spec = importlib.util.spec_from_file_location("source_doc", os.path.join(ROOT, "tools-pm", "source-doc.py"))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


CONTRACTIONS = [  # (the full form, where a speaker could contract it; the contraction)
    (r"\bdo not\b", r"\bdon't\b"), (r"\bdoes not\b", r"\bdoesn't\b"), (r"\bdid not\b", r"\bdidn't\b"),
    (r"\bis not\b", r"\bisn't\b"), (r"\bare not\b", r"\baren't\b"), (r"\bwas not\b", r"\bwasn't\b"), (r"\bwere not\b", r"\bweren't\b"),
    (r"\bcannot\b|\bcan not\b", r"\bcan't\b"), (r"\bwill not\b", r"\bwon't\b"), (r"\bwould not\b", r"\bwouldn't\b"),
    (r"\bshould not\b", r"\bshouldn't\b"), (r"\bcould not\b", r"\bcouldn't\b"), (r"\bhave not\b", r"\bhaven't\b"), (r"\bhas not\b", r"\bhasn't\b"),
    (r"\bit is\b(?! (?:not|n't))(?=\s+[a-z])", r"\bit's\b"), (r"\bthat is\b(?=\s+[a-z])", r"\bthat's\b"), (r"\bthere is\b(?=\s+[a-z])", r"\bthere's\b"),
    (r"\bwhat is\b(?=\s+[a-z])", r"\bwhat's\b"), (r"\bhere is\b(?=\s+[a-z])", r"\bhere's\b"),
    (r"\byou are\b(?=\s+[a-z])", r"\byou're\b"), (r"\byou will\b(?=\s+[a-z])", r"\byou'll\b"), (r"\bthey are\b(?=\s+[a-z])", r"\bthey're\b"),
    (r"\bwe are\b(?=\s+[a-z])", r"\bwe're\b"), (r"\bit will\b(?=\s+[a-z])", r"\bit'll\b")]


# S10: an entry that opens with one of these media is a story (fiction, or a story told on screen or stage)
STORY = re.compile(r"(?:An? |A pair of |Two )?(?:classic )?(?:novel|novella|short story|graphic novel|comic|(?:TV |television |streaming )?series(?! of)|film|documentary|play)\b", re.I)
# S12: a book's entry opens "A book" or "A textbook"; a time under about 30 minutes marks something short.
BOOK = re.compile(r"An? (?:book|textbook)\b", re.I)
SHORT = re.compile(r"\b(?:a few|a couple of|(?:about |some |under )?(\d+)) minutes?\b", re.I)
# S12: a built module that may hold fewer than two books for now. Empty since Modules 1 and 2 took theirs (job 8).
S12_PENDING = set()
# S12: on a built full path every entry opens with what it is; these kinds ask for 30 minutes or more
LONG_KIND = re.compile(r"An? (?:book|textbook|(?:journal |law review |long )?article|(?:conference |research |long )?paper|(?:staff )?report)\b", re.I)
# S13: no unit tells the reader to borrow or buy; no built full path gives a page count or a running time
BORROW = re.compile(r"\b(?:borrow|buy) it\b", re.I)
LENGTH = re.compile(r"\b(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|a few|a couple of)[ -](?:pages?|minutes?|hours?|episodes?)\b|\babout an? hour\b|\bhalf an hour\b|\bhalf-hour\b|\bof about\b", re.I)
# T9: a comma or a period after a closing double quotation mark (straight or curly), past any bold, italic or
# link markup that closes with it. A quote that follows a space or an opening bracket opens; it doesn't close.
OUTSIDE = re.compile(r"(?<=[^\s(\[{])[\"\u201d](?:\*{1,3}|_)?(?:\]\([^)\s]*\))?(?:\*{1,3}|_)?[,.]")
# S14: a time estimate, and the rounded marks it may take
DURATION = re.compile(r"(?:(\d+) hours?(?: (\d+) minutes?)?|(\d+) minutes?)")


def s14_round(m):
    """The owner's rounding (spec S14): up to 5 minutes under 30; nearest quarter hour to 2 hours; nearest half
    hour to 5; nearest hour beyond."""
    if m < 30:
        return -(-m // 5) * 5
    step = 15 if m <= 120 else 30 if m <= 300 else 60
    return int(m / step + 0.5) * step


def s14_minutes(d):
    """Minutes in "1 hour 15 minutes", "2 hours", "45 minutes"; None if it doesn't read as one."""
    m_ = DURATION.fullmatch(d.strip())
    if not m_:
        return None
    return int(m_.group(3)) if m_.group(3) else int(m_.group(1)) * 60 + int(m_.group(2) or 0)


# S14: a module's header puts the hour in words: "an hour", "an hour and 15 minutes", "an hour and a half",
# "2 hours", "2 and a half hours", "2 hours and 15 minutes", "45 minutes"
HEADER_TIME = re.compile(r"(?:(an|\d+) hours?(?: and (?:a half|(\d+) minutes))?|(\d+) and a half hours|(\d+) minutes)")


def s14_header_minutes(d):
    """Minutes in a header's total, written as the owner wrote it (spec S14); None if it doesn't read so."""
    m_ = HEADER_TIME.fullmatch(d.strip())
    if not m_:
        return None
    if m_.group(4):
        return int(m_.group(4))
    if m_.group(3):
        return int(m_.group(3)) * 60 + 30
    h = 1 if m_.group(1) == "an" else int(m_.group(1))
    if (h == 1) != (m_.group(1) == "an") or (h == 1 and "hours" in d):
        return None
    half = d.strip().endswith("a half")
    return h * 60 + (30 if half else int(m_.group(2) or 0))


def s14_on_mark(m):
    return m == s14_round(m) and (m >= 30 or m % 5 == 0)


def _own_words(md):
    """A tab's own running text: no headings, no quotations, no titles of works, no links, no table rows."""
    lines = [l for l in md.split("\n") if not re.match(r"\s*(#|>|\|)", l)]
    s = "\n".join(lines)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", " ", s)          # links: the words are a title
    s = re.sub(r'"[^"\n]*"', " ", s)                       # quotations, and titles in quotation marks
    s = re.sub(r"(?<!\*)\*(?!\*)[^*\n]+\*(?!\*)", " ", s)  # italics: titles of works, status lines
    return s.replace("**", "")


def _sections(md, names):
    """The text under each heading whose name is in names, up to the next heading."""
    out, cur = [], None
    for l in md.split("\n"):
        h = re.match(r"#{1,4} (.*)", l)
        if h:
            cur = [] if h.group(1).strip() in names else None
            if cur is not None:
                out.append(cur)
        elif cur is not None:
            cur.append(l)
    return ["\n".join(x) for x in out]


def s14_checks(name, text):
    """S14: the header's one total, the steps' and exercises' times, and the times sources ask, all on the
    owner's marks, and the total the rounded sum of the parts."""
    where = name
    lines = text.split("\n")
    times = []
    if re.match(r"\d+ ", name):
        head = next((l for l in lines if l.startswith("About ")), None)
        total = None
        if head is None:
            fail("S14", f"{where}: the header gives no total")
        else:
            h_ = re.fullmatch(r"About (.+?)\.", head.strip())
            total = s14_header_minutes(h_.group(1)) if h_ else None
            if total is None:
                fail("S14", f"{where}: the header reads \"{head.strip()[:60]}\", and gives one total with the hour in words, such as \"About an hour and 15 minutes.\", with no reading and doing split")
            elif not s14_on_mark(total):
                fail("S14", f"{where}: the header's total, {head.strip()}, isn't rounded the owner's way")
        for sec in _sections(text, {"The short path"}):
            for l in sec.split("\n"):
                s_ = re.match(r"\s+(?:Concept card\. )?(\d+) minutes\.", l)
                if s_:
                    times.append(("a step", int(s_.group(1))))
        optional = []
        for e_ in re.finditer(r"^\*\*([^*\n]*?)\((\d+) minutes\)\.\*\*", text, re.M):
            # an optional exercise shows its time and stays outside the module's total (S14, 26 November 2026)
            (optional if e_.group(1).startswith("Optional") else times).append(("an exercise", int(e_.group(2))))
        for what, m in times + optional:
            if not s14_on_mark(m):
                fail("S14", f"{where}: {what} takes {m} minutes, and rounds to {s14_round(m)}")
        if total is not None and times and s14_round(sum(m for _, m in times)) != total:
            fail("S14", f"{where}: the header says {total} minutes, and the steps and required exercises add up to {sum(m for _, m in times)}, which rounds to {s14_round(sum(m for _, m in times))}")
    # the time a source asks, on a full path or a card: not a story's running time
    for sec in _sections(text, {"Go deeper: the full path", "Go deeper"}):
        for entry in re.split(r"\n(?=- \*\*|\*\*)", sec):
            body = re.sub(r"^- \*\*.+?\*\*(?!\*)\s*", "", entry, flags=re.S)
            if STORY.match(body):
                continue
            if re.match(r"\*\*(?:Why trust it|What you'll get):", entry):
                continue
            # what the entry says before its reasons; a "To check:" note quotes facts to check, not estimates
            lead = body.split("**Why trust it:**")[0].split("**What you'll get:**")[0]
            lead = "\n".join(l for l in lead.split("\n") if not l.strip().startswith("*To check"))
            for d_ in re.finditer(r"\b(?:[Aa]bout )?(\d+) minutes\b", lead):
                if not s14_on_mark(int(d_.group(1))):
                    fail("S14", f"{where}: a source asks \"{d_.group(0)}\", which rounds to {s14_round(int(d_.group(1)))} minutes")


def voice_checks(sd, soup, mods, tab_of, by_name):
    """X4: every voice slot in data/pm/voice-slots.yaml is placed in its unit and shows its block in its tab, every
    placed slot is in the file, no brief or old words reach a page, no wordless slot stands as a paragraph, the moved
    list says what, from, to, why and when, and with --live no slot is open."""
    v = sd.voice()
    slots = {s_.get("id"): s_ for s_ in v["slots"]}
    norm = lambda t: " ".join(re.findall(r"[a-z0-9']+", (t or "").translate(sd.QUOTES).lower()))
    for i, s_ in enumerate(v["slots"]):
        for k in ("id", "unit", "brief"):
            if not s_.get(k):
                fail("X4", f"data/pm/voice-slots.yaml: slot {s_.get('id') or i + 1} has no {k}")
        if s_.get("unit") and s_["unit"] not in by_name:
            fail("X4", f"the voice slot {s_.get('id')} names the unit {s_['unit']}, which has no tab")
    # where each slot is placed: a built page, as the single document shows it, or a draft's file
    placed = {}
    for art in soup.select("main article.unit"):
        unit = art["data-unit"]
        name = tab_of.get(unit) or next((tab_of[m["page"]] for m in mods if m.get("page") and m["id"] == art.get("data-module")), None)
        for el in art.select("[data-voice]"):
            placed.setdefault(el["data-voice"], []).append(name)
            if el.name == "p" and not norm(el.get_text()):
                fail("X4", f"{name}: the voice slot {el['data-voice']} shows no words and stands as a paragraph of its own, which leaves an empty one")
            if el.name == "span" and el.parent.name in ("div", "section", "article", "blockquote", "main"):
                fail("X4", f"{name}: the voice slot {el['data-voice']} stands on its own line outside any paragraph: place it as {{{{< pm/voice \"{el['data-voice']}\" \"paragraph\" >}}}}")
        text = norm(art.get_text(" "))
        for sid, s_ in slots.items():
            b = norm(s_.get("brief"))
            if b and len(b.split()) >= 3 and b in text:
                fail("X4", f"{name}: the brief of the voice slot {sid} reached the page")
            o = norm(s_.get("old"))
            if o and len(o.split()) >= 3 and o != norm(s_.get("interim")) and o in text:
                fail("X4", f"{name}: the owner's old words for the voice slot {sid} reached the page, and only its interim words should")
    for m in mods:
        if m.get("draft") and os.path.exists(os.path.join(ROOT, "drafts", "pm", m["draft"] + ".md")):
            for sid in sd.VOICE_CODE.findall(open(os.path.join(ROOT, "drafts", "pm", m["draft"] + ".md"), encoding="utf-8").read()):
                placed.setdefault(sid, []).append(f"{m['num']} {m['title']}")
    for sid, units in placed.items():
        if sid not in slots:
            fail("X4", f"{units[0]} places the voice slot {sid}, and data/pm/voice-slots.yaml has no such slot")
    for sid, s_ in slots.items():
        if sid not in placed:
            fail("X4", f"the voice slot {sid} is in data/pm/voice-slots.yaml and placed in no unit: place it with {{{{< pm/voice \"{sid}\" >}}}}, or delete it once it's filled")
        elif s_.get("unit") not in placed[sid]:
            fail("X4", f"the voice slot {sid} belongs to {s_.get('unit')} and is placed in {', '.join(placed[sid])}")
        elif f"{sd.SLOT_HEAD} `{sid}`" not in by_name.get(s_.get("unit"), ""):
            fail("X4", f"{s_.get('unit')}: the tab doesn't show the block of the voice slot {sid}, so the owner can't fill it where he reads")
        if sid not in by_name.get(sd.VOICE_TAB, ""):
            fail("X4", f"the tab {sd.VOICE_TAB} doesn't list the voice slot {sid}")
    for i, e in enumerate(v["moved"]):
        missing = [k for k in ("what", "words", "from", "to", "why", "when") if not e.get(k)]
        if missing:
            fail("X4", f"data/pm/voice-slots.yaml: moved entry {i + 1} has no {', '.join(missing)}")
        if e.get("what") not in ("cut", "moved", "changed"):
            fail("X4", f"data/pm/voice-slots.yaml: moved entry {i + 1} says what happened as \"{e.get('what')}\", and it's cut, moved or changed")
        if e.get("words") and " ".join(sd.clean(e["words"]).split()) not in " ".join(by_name.get(sd.VOICE_TAB, "").split()):
            fail("X4", f"the tab {sd.VOICE_TAB} doesn't list moved entry {i + 1}: \"{e['words'][:50]}...\"")
    if LIVE:
        for sid, s_ in slots.items():
            fail("X4", f"the voice slot {sid} in {s_.get('unit')} is still open, and nothing that waits for the owner's voice is published")
    elif slots:
        NOTE["X4"].append(f"{len(slots)} voice slot{'' if len(slots) == 1 else 's'} open, which publishing (--live) would fail on")


# The games (spec J5): each one's name, as a module's front matter gives it, and the module that carries it.
GAMES = {"dice": "find-the-constraint", "waiting": "know-who-its-for", "ranking": "weigh-the-evidence"}
BEYOND = "**Beyond this module.**"
LOG_LABEL = {"know-who-its-for": "Start a decision log", "notice-when-you-are-wrong": "Review your decision log"}
LOG_TIMED = {"notice-when-you-are-wrong"}  # the one log line with its minutes (J3)
LOG_RE = r"\*\*(Start a decision log|For your decision log|Review your decision log)( \(\d+ minutes\))?\.\*\*"


# ---------- F1, F2: the pictures' one grammar, and reading them on a phone ----------
FIG_CLASSES = {"fig", "fig-pipe", "fig-mark", "fig-on-mark", "fig-ink", "fig-water", "fig-loss", "fig-cell", "fig-label", "fig-item",
               "fig-note", "fig-axis", "fig-line", "fig-return", "fig-guide", "fig-ramp-1", "fig-ramp-2", "fig-ramp-3",
               "fig-ramp-4", "fig-ramp-5", "fig-arrow", "fig-arrow-ink", "fig-stops", "fig-num"}
FIG_ONLY_IN = {"fig-ramp-1": "access-patterns.svg", "fig-ramp-2": "access-patterns.svg",
               "fig-ramp-3": "access-patterns.svg", "fig-ramp-4": "access-patterns.svg", "fig-ramp-5": "access-patterns.svg"}


def picture_checks(out_dir):
    """F1 in each picture's source: only the grammar's marks, one key moment in yellow, one arrowhead, the dot and
    corner scales. F2 in a browser, on every card: the picture fills its panel and its caption shares its left edge, at 390 and
    1280 pixels; at 390, no word under 12 pixels, no text overlapping or running out, and words on the yellow in the highlighter's ink, readable in dark."""
    from bs4 import BeautifulSoup
    checked("F1", "F2")
    pm_css = re.sub(r"/\*.*?\*/", "", open(os.path.join(ROOT, "assets", "css", "pm.css"), encoding="utf-8").read(), flags=re.S)
    for c in sorted(FIG_CLASSES):
        if not re.search(r"\." + re.escape(c) + r"(?![\w-])", pm_css):
            fail("F1", f"pm.css names no mark .{c}")
    files = sorted(glob.glob(os.path.join(ROOT, "assets", "figures", "*.svg")))
    if not files:
        fail("F1", "no picture files found")
    for path in files:
        name = os.path.basename(path)
        soup = BeautifulSoup(open(path, encoding="utf-8").read(), "html.parser")
        svg = soup.find("svg")
        vb = (svg.get("viewbox") or svg.get("viewBox") or "").split()
        if len(vb) != 4 or vb[:3] != ["0", "0", "360"] or not 120 <= float(vb[3]) <= 244:
            fail("F1", f"{name}: drawn in viewBox \"{' '.join(vb)}\", not 360 units wide from 0 0 and 120 to 244 tall"); continue
        frame = 360 * float(vb[3])
        used = set()
        for el in svg.find_all(True):
            used.update(el.get("class") or [])
            own = [a for a in ("font-size", "font-weight", "font-family", "stroke-width", "stroke-dasharray", "opacity") if el.get(a) is not None]
            if own:
                fail("F1", f"{name}: a <{el.name}> sets its own {own[0]}; pictures use the marks pm.css names")
        for c in sorted(used - FIG_CLASSES):
            fail("F1", f"{name}: uses .{c}, which is not one of the pictures' marks")
        for c in sorted(used & set(FIG_ONLY_IN)):
            if FIG_ONLY_IN[c] != name:
                fail("F1", f"{name}: uses .{c}, which belongs to {FIG_ONLY_IN[c]} alone")

        def cls(el):   # an element's marks, its own and its group's
            out = set(el.get("class") or [])
            for par in el.parents:
                if par.name == "g":
                    out.update(par.get("class") or [])
            return out
        for t in svg.find_all("text"):
            if not cls(t) & {"fig-label", "fig-item", "fig-note", "fig-num"}:
                fail("F1", f"{name}: \"{t.get_text()[:30]}\" has no rank (label, item or note)")
        for r in svg.find_all("rect"):
            if r.get("rx") not in (None, "6"):
                fail("F1", f"{name}: a box's corners are rounded by {r.get('rx')}, not 6")
        for c in svg.find_all("circle"):
            k, rad = cls(c), float(c.get("r"))
            if "fig-stops" in k:
                ok = rad == 14
            elif "fig-ink" in k:
                ok = rad in (4, 5.5)
            else:
                ok = "fig-return" in k   # an outline, not a dot
            if not ok:
                fail("F1", f"{name}: a circle of radius {c.get('r')} is not on the dot scale (4 counted, 5.5 named, 14 numbered)")
        marks = [m for m in svg.find_all(True) if "fig-mark" in (m.get("class") or [])]
        if not 1 <= len(marks) <= 3:
            fail("F1", f"{name}: {len(marks)} yellow marks; a picture has one key moment, of up to three like marks")
        if any(m.name != "rect" for m in marks):
            fail("F1", f"{name}: the yellow is a <{[m.name for m in marks if m.name != 'rect'][0]}>, not a rectangle behind the thing")
        else:
            area = sum(float(m["width"]) * float(m["height"]) for m in marks)
            if area > 0.08 * frame:
                fail("F1", f"{name}: the yellow covers {area / frame:.1%} of the picture, more than 8%")
            if len(marks) > 1 and any(m["height"] != "18" for m in marks):
                fail("F1", f"{name}: more than one yellow mark, and they aren't all highlighters behind words, 18 units high")
            if len({m["height"] for m in marks}) > 1:
                fail("F1", f"{name}: its yellow marks differ in height, so they aren't like marks of one moment")
        for a in svg.find_all("path"):
            k = set(a.get("class") or [])
            if not k & {"fig-arrow", "fig-arrow-ink"}:
                continue
            pts = [tuple(map(float, q)) for q in re.findall(r"(-?[\d.]+),(-?[\d.]+)", a.get("d") or "")]
            sides = sorted(((pts[i][0] - pts[j][0]) ** 2 + (pts[i][1] - pts[j][1]) ** 2) ** 0.5 for i, j in ((0, 1), (1, 2), (0, 2))) if len(pts) == 3 else []
            if not sides or abs(sides[0] - 10) > 0.35 or abs(sides[1] - 10.296) > 0.35 or abs(sides[2] - 10.296) > 0.35:
                fail("F1", f"{name}: an arrowhead ({a.get('d')}) is not the one triangle, 10 across and 9 long")
            shaft = {"fig-arrow": {"fig-return"}, "fig-arrow-ink": {"fig-axis", "fig-line"}}[(k & {"fig-arrow", "fig-arrow-ink"}).pop()]
            if not used & shaft:
                fail("F1", f"{name}: an arrowhead has no shaft of its color (grey on a dotted line, ink on a solid one)")

    # F2, in a browser
    cards = sorted(glob.glob(os.path.join(out_dir, "pm", "cards", "*", "index.html")))
    probe = """() => { const svg = document.querySelector('figure.plate svg.fig'); if (!svg) return null;
      const plate = svg.closest('figure').getBoundingClientRect(), sb = svg.getBoundingClientRect(), fill = e => getComputedStyle(e).fill;
      const has = (t, c) => t.classList.contains(c) || t.parentNode.classList.contains(c);
      const marks = [...svg.querySelectorAll('.fig-mark')].map(m => { const b = m.getBoundingClientRect(); return {x: b.left, y: b.top, w: b.width, h: b.height, fill: fill(m)}; });
      const texts = [...svg.querySelectorAll('text')].map(t => { const b = t.getBoundingClientRect();
        return {s: t.textContent.trim(), x: b.left, y: b.top, w: b.width, h: b.height, px: parseFloat(getComputedStyle(t).fontSize) * sb.width / svg.viewBox.baseVal.width,
                fill: fill(t), on: has(t, 'fig-on-mark'), num: has(t, 'fig-num')}; });
      const cap = svg.closest('figure').querySelector('.plate-caption'), cb = cap ? cap.getBoundingClientRect() : null;
      return {plate: plate.width, left: sb.left, top: sb.top, w: sb.width, h: sb.height, marks, texts,
              cap: cb ? cb.left + parseFloat(getComputedStyle(cap).paddingLeft) : null}; }"""
    chrome = os.environ.get("CHROME")
    srv = Server(out_dir)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=chrome) if chrome else p.chromium.launch()
            # at a wide screen too, the picture fills its panel and the caption starts where its words do
            ctx = b.new_context(viewport={"width": 1280, "height": 900}); pg = ctx.new_page()
            for html in cards:
                card = os.path.basename(os.path.dirname(html))
                pg.goto(f"{srv.base}/pm/cards/{card}/"); pg.wait_for_load_state("load")
                d = pg.evaluate(probe)
                if d and d["w"] < d["plate"] - 1:
                    fail("F2", f"card {card}: at 1280 pixels the picture is {d['w']:.0f} pixels wide in a panel of {d['plate']:.0f}")
                if d and d["cap"] is not None and abs(d["cap"] - (d["left"] + d["w"] / 30)) > 1.5:
                    fail("F2", f"card {card}: at 1280 pixels the caption starts {d['cap'] - (d['left'] + d['w'] / 30):+.0f} pixels from where the picture's words start")
            ctx.close()
            for scheme in ("light", "dark"):
                ctx = b.new_context(viewport={"width": 390, "height": 900}, color_scheme=scheme); pg = ctx.new_page()
                for html in cards:
                    card = os.path.basename(os.path.dirname(html))
                    pg.goto(f"{srv.base}/pm/cards/{card}/"); pg.wait_for_load_state("load")
                    pg.evaluate("document.fonts.ready")
                    d = pg.evaluate(probe)
                    if not d:
                        continue   # a card that opens with a quotation (S16)
                    on_mark = lambda t: any(m["x"] <= t["x"] + t["w"] / 2 <= m["x"] + m["w"] and m["y"] <= t["y"] + t["h"] / 2 <= m["y"] + m["h"] for m in d["marks"])
                    if scheme == "dark":
                        for t in d["texts"]:
                            if t["on"] and d["marks"]:
                                fg, bg = [tuple(int(float(v)) for v in re.findall(r"[\d.]+", c)[:3]) for c in (t["fill"], d["marks"][0]["fill"])]
                                ratio = contrast(fg, bg)
                                if ratio < 4.5:
                                    fail("F2", f"card {card}: \"{t['s']}\" on the yellow reads at {ratio:.1f} to 1 on a dark screen, under 4.5")
                        continue
                    if d["w"] < d["plate"] - 1:
                        fail("F2", f"card {card}: at 390 pixels the picture is {d['w']:.0f} pixels wide in a panel of {d['plate']:.0f}")
                    if d["cap"] is not None and abs(d["cap"] - (d["left"] + d["w"] / 30)) > 1.5:
                        fail("F2", f"card {card}: at 390 pixels the caption starts {d['cap'] - (d['left'] + d['w'] / 30):+.0f} pixels from where the picture's words start")
                    small = [t for t in d["texts"] if t["px"] < 12]
                    if small:
                        fail("F2", f"card {card}: \"{small[0]['s']}\" is set at {small[0]['px']:.1f} pixels on a phone, under 12")
                    for i, a in enumerate(d["texts"]):
                        if a["x"] < d["left"] - 0.5 or a["x"] + a["w"] > d["left"] + d["w"] + 0.5 or a["y"] < d["top"] - 0.5 or a["y"] + a["h"] > d["top"] + d["h"] + 0.5:
                            fail("F2", f"card {card}: \"{a['s']}\" runs out of the picture")
                        if on_mark(a) != a["on"] and not a["num"]:
                            fail("F2", f"card {card}: \"{a['s']}\" {'sits on the yellow without' if not a['on'] else 'takes the highlighter ink off'} the yellow")
                        for o in d["texts"][i + 1:]:
                            # the middle of each line box, where the letters are: a line box is taller than its letters
                            if (a["x"] < o["x"] + o["w"] + 2 and o["x"] < a["x"] + a["w"] + 2
                                    and a["y"] + a["h"] * 0.22 < o["y"] + o["h"] * 0.80 and o["y"] + o["h"] * 0.22 < a["y"] + a["h"] * 0.80):
                                fail("F2", f"card {card}: \"{a['s']}\" and \"{o['s']}\" overlap in the picture")
                ctx.close()
            b.close()
    finally:
        srv.close()


def practice_checks(out_dir):
    """J1 to J5: every Check ends with one question beyond the module; from Module 1 one question collides with an
    earlier module, names it and carries against:; each Do from Module 1 has its line for the decision log, after the
    timed exercises and before any optional one; each module from 1 names an earlier one in its Why this matters or
    Do; and each game is a step on its module's short path, with a guess, a result, a takeaway that says what it leaves
    out, and numbers that match what tools-pm/game-numbers.py works out."""
    from bs4 import BeautifulSoup
    checked("J1", "J2", "J3", "J4", "J5")
    mods = yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "modules.yaml"), encoding="utf-8"))
    num = {m["id"]: int(m["num"]) for m in mods}
    title = {m["id"]: m["title"] for m in mods}
    carried = {}
    wins_count = 0
    for m in mods:
        if not m.get("page"):
            continue
        where = f"Module {m['num']}, {m['title']}"
        n = int(m["num"])
        _, fm, body = open(os.path.join(ROOT, "content", "pm", m["page"] + ".md"), encoding="utf-8").read().split("---", 2)
        d = yaml.safe_load(fm) or {}
        checks = d.get("check") or []
        # J1: the last Check question, and only that one, reaches past the module
        beyond = [c for c in checks if str(c.get("q", "")).lstrip().startswith(BEYOND)]
        if not checks or not str(checks[-1].get("q", "")).lstrip().startswith(BEYOND):
            fail("J1", f"{where}: its Check doesn't end with a question that opens \"Beyond this module.\" in bold")
        if len(beyond) > 1:
            fail("J1", f"{where}: {len(beyond)} Check questions are marked \"Beyond this module\", and only the last one should be")
        # J2: from Module 1, one question collides with an earlier module and names it by its title
        coll = [c for c in checks if c.get("against")]
        if n >= 1 and len(coll) != 1:
            fail("J2", f"{where}: {len(coll)} Check questions carry against:, and one should set this module against an earlier one")
        for c in coll:
            a = c["against"]
            if a not in num:
                fail("J2", f"{where}: a Check question is set against {a}, which isn't on the map")
            elif num[a] >= n:
                fail("J2", f"{where}: a Check question is set against {title[a]}, which doesn't come earlier on the map")
            elif title[a] not in str(c.get("q", "")):
                fail("J2", f"{where}: the question set against {title[a]} doesn't name it by its title")
            if c.get("wins") is not None:
                wins_count += 1
                if c["wins"] not in (a, m["id"]):
                    fail("J2", f"{where}: the collision says {c['wins']} wins, and should name {title.get(a, a)} or this module")
        parts = body.split("[//]: # (short-path)")
        why = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        do = re.split(r"\n## ", rest.split("## Do", 1)[1])[0] if "## Do" in rest else ""
        if n < 1:
            continue
        # J3: the decision log's line, after the timed exercises and before any optional one
        want = LOG_LABEL.get(m["id"], "For your decision log")
        paras = [p_.strip() for p_ in do.split("\n\n") if p_.strip()]
        labels = [p_ for p_ in paras if re.match(LOG_RE, p_)]
        timed_log = bool(labels) and bool(re.match(r"\*\*[^*]*\(\d+ minutes\)\.\*\*", labels[0]))
        if len(labels) != 1 or not re.match(re.escape(f"**{want}") + r"( \(\d+ minutes\))?\.\*\*", labels[0]):
            fail("J3", f"{where}: its Do should hold one line for the decision log, opening \"{want}.\" in bold")
        elif timed_log != (m["id"] in LOG_TIMED):
            fail("J3", f"{where}: " + (f"its log review should show its minutes, as \"{want} (15 minutes).\" does, since reading back a module's worth of calls takes real time" if m["id"] in LOG_TIMED else "its decision log line is a sentence or two and shows no time; only Notice When You Are Wrong's review does"))
        elif m["id"] in LOG_TIMED and not re.search(r"Outside the \d+ minutes, show it to your manager or a mentor", labels[0]):
            fail("J3", f"{where}: its log review should end, outside its minutes, by showing the log to a manager or a mentor")
        else:
            i_log = paras.index(labels[0])
            i_opt = next((i for i, p_ in enumerate(paras) if p_.startswith("**Optional")), len(paras))
            timed = [i for i, p_ in enumerate(paras) if re.match(r"\*\*.*?\(\d+ minutes\)\.\*\*", p_) and not p_.startswith("**Optional")]
            if i_log > i_opt or not timed or i_log < max(timed):
                fail("J3", f"{where}: the decision log's line should follow the Do's timed exercises and come before any optional one")
        # J4: an earlier module named by its title in Why this matters or the Do
        if not any(title[o] in why + do for o in num if num[o] < n):
            fail("J4", f"{where}: neither its Why this matters nor its Do names an earlier module by its title")
        # J5: the module's game
        if d.get("game"):
            carried[d["game"]] = m["id"]
    if wins_count < 3:
        fail("J2", f"{wins_count} collisions carry wins:, and at least three should give one case and say which side wins in it")
    for g, mid in GAMES.items():
        where = f"the {g} game"
        if carried.get(g) != mid:
            fail("J5", f"{where} belongs in {title.get(mid, mid)}, and isn't there")
            continue
        m = next(m_ for m_ in mods if m_["id"] == mid)
        d = yaml.safe_load(open(os.path.join(ROOT, "content", "pm", m["page"] + ".md"), encoding="utf-8").read().split("---", 2)[1])
        if not any(s_.get("kind") == "play" for s_ in d.get("steps") or []):
            fail("J5", f"{where} isn't a step on {title[mid]}'s short path")
        soup = BeautifulSoup(open(os.path.join(out_dir, "pm", m["page"], "index.html"), encoding="utf-8").read(), "html.parser")
        sec = soup.select_one(f"section[data-game={g}]")
        if not sec:
            fail("J5", f"{where} isn't on {title[mid]}'s page"); continue
        if not soup.select_one(f'.steps a[href="#{sec.get("id")}"]'):
            fail("J5", f"{title[mid]}: the step that plays {where} doesn't lead to it")
        for sel, what in ((".guess legend", "a guess before the first play"), ("[data-play]", "a Play button"), ("[data-result]", "a result in words"), (".takeaway", "a takeaway")):
            if not sec.select_one(sel):
                fail("J5", f"{where} has no {what}")
        lim = sec.select_one(".takeaway .limits")
        if not lim or not clean_text(lim.get_text()).startswith("What the game leaves out."):
            fail("J5", f"{where}: its takeaway doesn't say what the game leaves out")
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools-pm", "game-numbers.py"), "check"], capture_output=True, text=True)
    for line in (r.stdout + r.stderr).strip().splitlines() if r.returncode else []:
        fail("J5", line[:200])


# Both ways with engineering (spec J9). In each Do that hands its work to engineers, the first phrase sits after
# "Outside the N minutes" in its own paragraph, so the colleague's time stays outside the reader's (S18).
ENG_HEAD = "## To bring to "
ENG_LISTS = {"know-who-its-for", "mind-the-seams", "map-the-domain", "design-for-change", "change-safely"}
GIVE = {"own-your-role": ("an engineer on the work", "measure today"),
        "know-who-its-for": ("engineers who'd build the fix", "price on a week of waiting"),
        "notice-when-you-are-wrong": ("an engineer on the work", "measured today"),
        "change-safely": ("leads on call", "proposal")}
TAKE_PART = {"map-the-domain": ("design doc", "design review"),
             "change-safely": ("incident write-up", "incident review"),
             "decide-and-set-direction": ("advice process", "still making")}


def both_ways_checks():
    """J9: three Dos hand their work to engineers outside their minutes, Change Safely's reader proposes a rollout
    for on call's feedback, the reader reads, reviews and advises on engineering's work, and every list for
    engineers is headed "To bring to engineers" with one paragraph opening "Bring" above its questions."""
    checked("J9")
    mods = yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "modules.yaml"), encoding="utf-8"))
    headed = set()
    for m in mods:
        if not m.get("page"):
            continue
        where = f"Module {m['num']}, {m['title']}"
        body = open(os.path.join(ROOT, "content", "pm", m["page"] + ".md"), encoding="utf-8").read().split("---", 2)[2]
        do = re.split(r"\n## ", body.split("\n## Do\n", 1)[1])[0] if "\n## Do\n" in body else ""
        if "## Questions to bring to" in body:
            fail("J9", f"{where}: a list is still headed \"Questions to bring to ...\", not \"To bring to ...\"")
        if "\n" + ENG_HEAD in body:
            headed.add(m["id"])
            sec = re.split(r"\n## ", body.split("\n" + ENG_HEAD, 1)[1].split("\n", 1)[1])[0]
            paras = [p_.strip() for p_ in sec.split("\n\n") if p_.strip()]
            if len(paras) != 2 or not paras[0].startswith("Bring ") or "\n" in paras[0] or not paras[1].startswith("- "):
                fail("J9", f"{where}: \"To bring to ...\" should open with one paragraph, starting \"Bring\", above its list of questions")
        give = GIVE.get(m["id"])
        if give:
            para = next((p_ for p_ in do.split("\n\n") if give[0] in p_), "")
            out = re.search(r"Outside the \d+ minutes", para)
            if not para or not out or para.index(give[0]) < out.start():
                fail("J9", f"{where}: its Do should hand its work to engineers outside its minutes, with \"{give[0]}\" after \"Outside the ... minutes\"")
            if give[1] not in do:
                fail("J9", f"{where}: its Do should say \"{give[1]}\"")
        for w in TAKE_PART.get(m["id"], ()):
            if w not in do:
                fail("J9", f"{where}: its Do should take part in engineering's work, and doesn't say \"{w}\"")
    for mid in sorted(ENG_LISTS - headed):
        fail("J9", f"{mid}: its list should be headed \"To bring to ...\", with one line of what to bring")


EXAMPLE_LINE = "What a good one looks like"
EXAMPLE_GOOD = "What makes it good:"
EXAMPLE_WORDS = 120   # "under about 120 words" (the owner, 25 November 2026)
EXAMPLE_GATE = "Try yours first: an example is easier to copy than to judge."
EXAMPLE_UNGATE = "I've done mine"


def example_checks(out_dir):
    """J7: a module's Do shows one finished example of its main exercise, folded shut under "What a good one looks
    like", after the main exercise and its decision log line and before any optional exercise; under about 120
    words, then "What makes it good:" and three lines of one sentence each; left out of print, and in the single
    document as in the module. Where the Do is a step of the short path, a link down the page with no minutes of its
    own, the example opens to a gate until that step is ticked. Every built module has one; Own Your Role's, whose Do
    comes before the log starts, sits right after its main exercise."""
    from bs4 import BeautifulSoup
    checked("J7")
    mods = yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "modules.yaml"), encoding="utf-8"))
    count = lambda t: len(re.findall(r"[A-Za-z0-9$][A-Za-z0-9$,'’-]*", t))
    whole = BeautifulSoup(open(os.path.join(out_dir, "pm", "all", "index.html"), encoding="utf-8").read(), "html.parser")
    gated = []
    first_log = next(x["num"] for x in mods if x["id"] == "know-who-its-for")
    for m in mods:
        if not m.get("page"):
            continue
        where = f"Module {m['num']}, {m['title']}"
        _, fm, body = open(os.path.join(ROOT, "content", "pm", m["page"] + ".md"), encoding="utf-8").read().split("---", 2)
        d_fm = yaml.safe_load(fm) or {}
        ex = d_fm.get("example")
        dos = [s_ for s_ in d_fm.get("steps") or [] if s_.get("kind") == "do"]
        placed = len(re.findall(r"\{\{<\s*pm/example\s*>\}\}", body))
        if not ex and not placed:
            fail("J7", f"{where}: a built module shows one example of its Do's main exercise, and it has none")
            continue
        if not ex or placed != 1:
            fail("J7", f"{where}: an example: in the front matter and one {{{{< pm/example >}}}} in the Do go together, and it has {'no example:' if not ex else f'{placed} placed'}")
            continue
        text = str(ex.get("body") or "") if isinstance(ex, dict) else ""
        good = ex.get("good") if isinstance(ex, dict) else None
        if not text.strip():
            fail("J7", f"{where}: its example has no body"); continue
        n = count(re.sub(r"[*_#>`]", " ", re.sub(r"(?m)^\s*[-*] ", " ", text)))
        if n > EXAMPLE_WORDS:
            fail("J7", f"{where}: its example runs {n} words, and keeps under about {EXAMPLE_WORDS}")
        if not isinstance(good, list) or len(good) != 3 or not all(isinstance(g, str) and g.strip() for g in good):
            fail("J7", f"{where}: what makes its example good is three lines, and it has {len(good) if isinstance(good, list) else 'none'}")
        else:
            for g in good:
                if len(re.findall(r"[.!?](?=\s+[A-Z\u201c\"])", g.strip())) or not g.strip().endswith("."):
                    fail("J7", f"{where}: each line on what makes its example good is one sentence: \"{g.strip()[:50]}\"")
        # where it sits in the Do: after the main exercise and its decision log line, before any optional exercise
        rest = body.split("[//]: # (short-path)")[-1]
        do = re.split(r"\n## ", rest.split("## Do", 1)[1])[0] if "## Do" in rest else ""
        paras = [p_.strip() for p_ in do.split("\n\n") if p_.strip()]
        i_ex = next((i for i, p_ in enumerate(paras) if re.fullmatch(r"\{\{<\s*pm/example\s*>\}\}", p_)), None)
        i_log = next((i for i, p_ in enumerate(paras) if re.match(LOG_RE, p_)), None)
        i_opt = next((i for i, p_ in enumerate(paras) if p_.startswith("**Optional")), len(paras))
        if i_log is None and m["num"] < first_log:
            i_log = 0  # Own Your Role's Do comes before the log starts (J3): the example follows its main exercise
        if i_ex is None or i_log is None or not i_log < i_ex < i_opt or i_ex != i_log + 1:
            fail("J7", f"{where}: its example sits right after the Do's decision log line (in Own Your Role, its main exercise), on a line of its own, and before any optional exercise")
        # on the built page and in the single document
        page = BeautifulSoup(open(os.path.join(out_dir, "pm", m["page"], "index.html"), encoding="utf-8").read(), "html.parser")
        art = whole.select_one(f'article[data-unit="{m["page"]}"]')
        for doc_, what in ((page, "its page"), (art, "the single document")):
            dets = doc_.select("details.example") if doc_ else []
            if len(dets) != 1:
                fail("J7", f"{where}: {what} shows {len(dets)} examples, and should show one"); continue
            d_ = dets[0]
            summ = d_.find("summary", recursive=False)
            if not d_.find_parent("section", class_="do"):
                fail("J7", f"{where}: on {what}, its example isn't in the Do")
            if not summ or clean_text(summ.get_text()) != EXAMPLE_LINE:
                fail("J7", f"{where}: on {what}, its example opens under \"{clean_text(summ.get_text()) if summ else ''}\", not \"{EXAMPLE_LINE}\"")
            if d_.has_attr("open"):
                fail("J7", f"{where}: on {what}, its example isn't folded shut")
            if "screen-only" not in (d_.get("class") or []):
                fail("J7", f"{where}: on {what}, its example prints, and is for the screen alone")
            lab = d_.select_one(".example-body > .example-good-label")
            items = d_.select(".example-body > ul.example-good > li")
            if not lab or clean_text(lab.get_text()) != EXAMPLE_GOOD or len(items) != 3 or lab.find_next_sibling() is not items[0].parent:
                fail("J7", f"{where}: on {what}, its example doesn't end \"{EXAMPLE_GOOD}\" in bold and three lines")
            # the example waits for the Do's tick, where the Do is a step of the short path (the pilot); in the markup it
            # shows, so a reader without scripts has it
            want = f"{m['page']}:{dos[0].get('id')}" if dos else None
            if d_.get("data-gate") != want:
                fail("J7", f"{where}: on {what}, its example waits on {d_.get('data-gate')!r}, and should wait on {want!r}, the Do's step")
            gate = d_.select_one("[data-example-gate]")
            body_ = d_.select_one(".example-body")
            if d_.has_attr("hidden") or (body_ and body_.has_attr("hidden")):
                fail("J7", f"{where}: on {what}, its example is hidden in the markup, so a reader without scripts never has it")
            if want and (not gate or not gate.has_attr("hidden") or clean_text(gate.find("p").get_text() if gate.find("p") else "") != EXAMPLE_GATE
                         or not gate.select_one("button[data-example-ungate]") or clean_text(gate.select_one("button").get_text()) != EXAMPLE_UNGATE):
                fail("J7", f"{where}: on {what}, its example's gate isn't \"{EXAMPLE_GATE}\" and a button, \"{EXAMPLE_UNGATE}\", hidden until the script shows it")
            if not want and gate:
                fail("J7", f"{where}: on {what}, its example has a gate, and its Do isn't a step to tick")
        # the example's gate waits on the Do's step, which G7 holds to its form
        if ex and dos:
            gated.append(f"/pm/{m['page']}/")
    if not gated:
        return
    # in a browser: before the Do is ticked, the line opens to its gate; the button ticks the step and shows the example;
    # once ticked, the line opens the example; unticked, the gate is back; without scripts, the example opens as it is
    from playwright.sync_api import sync_playwright
    chrome = os.environ.get("CHROME")
    srv = Server(out_dir)
    state = """() => { const d = document.querySelector('details.example'), g = d.querySelector('[data-example-gate]'), b = d.querySelector('.example-body');
      const box = document.querySelector('[data-step="' + d.dataset.gate + '"] input');
      return {line: d.getClientRects().length > 0, open: d.open, gate: g.getClientRects().length > 0, body: b.getClientRects().length > 0, ticked: box.checked, focus: b.contains(document.activeElement)}; }"""
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(executable_path=chrome) if chrome else p.chromium.launch()
            for url in gated:
                ctx = b.new_context(viewport={"width": 390, "height": 844}); pg = ctx.new_page()
                pg.goto(srv.base + url); pg.wait_for_load_state("load")
                if not pg.evaluate(state)["line"]:
                    fail("J7", f"{url}: the example's line should show before the Do is ticked")
                pg.locator("details.example > summary").click()
                r = pg.evaluate(state)
                if not (r["open"] and r["gate"] and not r["body"] and not r["ticked"]):
                    fail("J7", f"{url}: before the Do is ticked, opening the example should show only its gate: {r}")
                else:
                    pg.locator("[data-example-ungate]").click()
                    r = pg.evaluate(state)
                    if not (r["ticked"] and r["body"] and not r["gate"] and r["focus"]):
                        fail("J7", f"{url}: \"{EXAMPLE_UNGATE}\" should tick the Do's step, show the example and move focus to it: {r}")
                    pg.reload(); pg.wait_for_load_state("load")
                    pg.locator("details.example > summary").click()
                    r = pg.evaluate(state)
                    if not (r["body"] and not r["gate"]):
                        fail("J7", f"{url}: once the Do is ticked, the example should open at once: {r}")
                    key = pg.evaluate("() => document.querySelector('details.example').dataset.gate")
                    pg.locator(f'[data-step="{key}"] .tick').click()
                    r = pg.evaluate(state)
                    if not (r["gate"] and not r["body"] and not r["ticked"]):
                        fail("J7", f"{url}: unticking the Do should bring the gate back: {r}")
                ctx.close()
                ctx = b.new_context(viewport={"width": 390, "height": 844}, java_script_enabled=False); pg = ctx.new_page()
                pg.goto(srv.base + url); pg.wait_for_load_state("load")
                pg.locator("details.example > summary").click()
                r = pg.evaluate("() => { const d = document.querySelector('details.example'); return {gate: d.querySelector('[data-example-gate]').getClientRects().length > 0, body: d.querySelector('.example-body').getClientRects().length > 0}; }")
                if r["gate"] or not r["body"]:
                    fail("J7", f"{url}: without scripts the example should open as it is, with no gate: {r}")
                ctx.close()
            b.close()
    finally:
        srv.close()


EVIDENCE_TAGS = ("A study.", "A review of studies.", "Experience.", "An argument.")


def setting_evidence_checks():
    """S6: every built module names its main setting, and no setting leads more than two modules.
    S17: every "Why trust it" in a module or a card opens with one of the four evidence tags, and none says
    "not a study"."""
    checked("S6", "S17")
    mods = yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "modules.yaml"), encoding="utf-8"))
    units = []
    for m in mods:
        if m.get("page"):
            units.append((f"Module {m['num']}, {m['title']}", os.path.join(ROOT, "content", "pm", m["page"] + ".md"), True))
    card_dir = os.path.join(ROOT, "content", "pm", "cards")
    for f in sorted(os.listdir(card_dir)) if os.path.isdir(card_dir) else []:
        if f.endswith(".md"):
            units.append((f"the card {f[:-3]}", os.path.join(card_dir, f), False))
    leads = defaultdict(list)
    for where, path, is_module in units:
        m = re.match(r"---\n(.*?)\n---", open(path, encoding="utf-8").read(), re.S)
        fm = (yaml.safe_load(m.group(1)) if m else {}) or {}
        if is_module:
            setting = " ".join(str(fm.get("setting") or "").split())
            if not setting:
                fail("S6", f"{where} names no main setting: add setting: to its front matter, the product its own examples follow")
            else:
                leads[setting.lower()].append(where)
        trusts = []
        def walk(x):
            if isinstance(x, dict):
                if "trust" in x:
                    trusts.append((x.get("title") or x.get("card") or "its source", str(x["trust"])))
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
        walk(fm)
        for title, t in trusts:
            if not t.strip().startswith(EVIDENCE_TAGS):
                fail("S17", f"{where}: the \"Why trust it\" for {title} doesn't open with its kind of evidence, one of {', '.join(EVIDENCE_TAGS)}: \"{t[:50]}...\"")
            if re.search(r"\bnot a study\b", t, re.I):
                fail("S17", f"{where}: the \"Why trust it\" for {title} says \"not a study,\" which its tag now says plainly")
    for setting, where in sorted(leads.items()):
        if len(where) > 2:
            fail("S6", f"the setting \"{setting}\" leads {len(where)} modules ({', '.join(where)}), and two is the most")


def source_checks(out_dir):
    from bs4 import BeautifulSoup
    checked("X1", "X2", "X3", "X4", "E1", "E2", "E3", "S5", "S7", "S9", "S10", "S11", "S12", "S13", "S14", "S23", "T9")
    # S9: no source from Substack, by name or by link, in a unit, a draft or the site's data
    for base in ("content", "drafts", "data"):
        for dirpath, _, files in os.walk(os.path.join(ROOT, base)):
            for f in sorted(files):
                if f.endswith((".md", ".yaml", ".yml", ".json")):
                    path = os.path.join(dirpath, f)
                    if "substack" in open(path, encoding="utf-8").read().lower():
                        fail("S9", f"{os.path.relpath(path, ROOT)} cites Substack, which the owner never cites")
    mods = yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "modules.yaml"), encoding="utf-8"))
    # X1: one source for every unit
    drafts = {os.path.splitext(f)[0] for f in os.listdir(os.path.join(ROOT, "drafts", "pm")) if f.endswith(".md")} if os.path.isdir(os.path.join(ROOT, "drafts", "pm")) else set()
    used = set()
    for m in mods:
        where = f"Module {m['num']}, {m['title']}"
        page = m.get("page") and os.path.exists(os.path.join(ROOT, "content", "pm", m["page"] + ".md"))
        draft = m.get("draft") and m["draft"] in drafts
        if m.get("page") and not page:
            fail("X1", f"{where}: the map names the page {m['page']}, and content/pm/{m['page']}.md is not there")
        if m.get("draft") and not draft:
            fail("X1", f"{where}: the map names the draft {m['draft']}, and drafts/pm/{m['draft']}.md is not there")
        if page and draft:
            fail("X1", f"{where} is both built and a draft: delete drafts/pm/{m['draft']}.md once the module is rebuilt")
        if not m.get("page") and not m.get("draft"):
            fail("X1", f"{where} has neither a page nor a draft")
        if m.get("draft") and not m.get("state"):
            fail("X1", f"{where}: a draft says where it stands, in its state line on the map")
        used.add(m.get("draft"))
    for d in sorted(drafts - used):
        fail("X1", f"drafts/pm/{d}.md belongs to no module on the map")
    # X1: the checks visit every built module and its cards, so none is built without being checked in a browser
    listed = {m_: set(c_) for m_, c_ in MODULES}
    card_dir = os.path.join(ROOT, "content", "pm", "cards")
    card_of = {}
    for f in sorted(os.listdir(card_dir)) if os.path.isdir(card_dir) else []:
        if f.endswith(".md"):
            mm = re.search(r"^module:\s*(\S+)", open(os.path.join(card_dir, f), encoding="utf-8").read(), re.M)
            if mm:
                card_of.setdefault(mm.group(1), []).append(f"/pm/cards/{f[:-3]}/")
    for m in mods:
        if not m.get("page"):
            continue
        url = f"/pm/{m['page']}/"
        if url not in listed:
            fail("X1", f"Module {m['num']}, {m['title']}, is built, and the checks don't visit it: add it to MODULES in tests/check_site.py")
            continue
        for c in card_of.get(m["id"], []):
            if c not in listed[url]:
                fail("X1", f"the card {c} is built, and the checks don't visit it: add it to its module in MODULES")
    closing_page = ((yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "arc.yaml"), encoding="utf-8")) or {}).get("closing") or {}).get("page")
    if closing_page and os.path.exists(os.path.join(ROOT, "content", "pm", f"{closing_page}.md")) and f"/pm/{closing_page}/" not in UNIT_PAGES:
        fail("X1", f"the closing unit /pm/{closing_page}/ is built, and the checks don't visit it: set CLOSING in tests/check_site.py")
    if FAIL.get("X1"):
        return
    sd = _source_doc()
    lock_path = os.path.join(ROOT, "tools-pm", "source-doc.lock.json")
    lock_all = json.load(open(lock_path, encoding="utf-8")) if os.path.exists(lock_path) else {}
    try:
        tabs = sd.tabs(out_dir, lock_all.get("synced") or None)
    except Exception as e:
        for r in ("X2", "X3", "X4"):
            fail(r, f"tools-pm/source-doc.py could not make the tabs: {str(e).splitlines()[0][:160]}")
        return
    by_name = dict(tabs)
    # X2: a built unit's tab holds every word a reader meets on its page
    soup = BeautifulSoup(open(os.path.join(out_dir, "pm", "all", "index.html"), encoding="utf-8").read(), "html.parser")
    norm = lambda s: " ".join(re.findall(r"[a-z0-9']+", s.translate(sd.QUOTES).lower()))
    tab_of = {"start": "Start", "glossary": "Glossary", CLOSING.strip("/").split("/")[-1]: getattr(sd, "CLOSING_TAB", "The Compass")}
    for m in mods:
        if m.get("page"):
            tab_of[m["page"]] = f"{m['num']} {m['title']}"
    for art in soup.select("main article.unit"):
        unit = art["data-unit"]
        name = tab_of.get(unit) or next((tab_of[m["page"]] for m in mods if m.get("page") and m["id"] == art.get("data-module")), None)
        if not name or name not in by_name:
            fail("X2", f"the unit {unit} has no tab"); continue
        have = norm(sd.strip_slots(by_name[name]))
        for junk in art.select("svg, script, style, .sr, .note-label, .print-only, .board, .board-key, .tally, .progress, .result, .setup-note, details.why > summary, [hidden]"):
            junk.extract()
        missing = []
        for node in art.find_all(string=True):
            want = norm(str(node))
            if len(want.split()) >= 2 and want not in have:
                missing.append(str(node).strip()[:60])
        for w in missing[:4]:
            fail("X2", f"{name}: the page says \"{w}\" and the tab does not")
        if len(missing) > 4:
            fail("X2", f"{name}: and {len(missing) - 4} more passages are on the page and not in the tab")
    # X2: the ReadMe's tab, after About, holds every word of its page, so the owner can revise it there
    readme = os.path.join(out_dir, "page", "readme", "index.html")
    names = [n_ for n_, _ in tabs]
    if sd.README_TAB not in by_name:
        fail("X2", "the ReadMe has no tab")
    elif names.index(sd.README_TAB) != 1 or names[0] != "About":
        fail("X2", f"the ReadMe's tab is number {names.index(sd.README_TAB) + 1} of the doc's, and it's the second, right after About")
    if sd.README_TAB in by_name and os.path.exists(readme):
        art = BeautifulSoup(open(readme, encoding="utf-8").read(), "html.parser").select_one("main article")
        have = norm(by_name[sd.README_TAB])
        missing = [str(n_).strip()[:60] for n_ in art.find_all(string=True) if len(norm(str(n_)).split()) >= 2 and norm(str(n_)) not in have]
        for w in missing[:4]:
            fail("X2", f"{sd.README_TAB}: the page says \"{w}\" and the tab does not")
        if len(missing) > 4:
            fail("X2", f"{sd.README_TAB}: and {len(missing) - 4} more passages are on the page and not in the tab")
        if len(art.find_all("br")) != by_name[sd.README_TAB].count("\\\n"):
            fail("X2", f"{sd.README_TAB}: the page breaks {len(art.find_all('br'))} lines inside its paragraphs and the tab {by_name[sd.README_TAB].count(chr(92) + chr(10))}, so the owner wouldn't see its lines as they stand")
    # X3: the doc is in step with the repository
    lock = {t_["name"]: t_ for t_ in lock_all.get("tabs", [])}
    if not lock:
        fail("X3", "tools-pm/source-doc.lock.json is missing or empty: sync the working doc, then run source-doc.py --record")
    for name, text in tabs:
        if name not in lock:
            fail("X3", f"the tab {name} has never been put in the working doc")
        elif lock[name].get("sha256") != sd.sha(text):
            fail("X3", f"the tab {name} has changed since it was last put in the working doc: sync the doc, then run source-doc.py --record")
    for name in lock:
        if name not in by_name:
            fail("X3", f"the record lists a tab the repository no longer makes: {name}")
    voice_checks(sd, soup, mods, tab_of, by_name)
    # S5, E1 to E3: every unit, built or draft, as its tab shows it
    built_tabs = {f"{m['num']} {m['title']}" for m in mods if m.get("page")}
    long_tabs = {f"{m['num']} {m['title']}" for m in mods if m["id"] in RUNS_LONG}
    own_words = yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "own-words.yaml"), encoding="utf-8")) or []
    for o in own_words:
        if o.get("unit") not in by_name:
            fail("E3", f"data/pm/own-words.yaml lists a sentence for {o.get('unit')}, which has no tab")
    retired = [l.strip().lower() for l in open(os.path.join(TESTS, "retired-settings.txt"), encoding="utf-8") if l.strip() and not l.startswith("#")]
    for name, text in tabs:
        if name in ("About", sd.README_TAB, sd.VOICE_TAB):   # the ReadMe is the owner's own words, not the syllabus's (X2)
            continue
        low = text.lower()
        for phrase in retired:
            if phrase in low:
                fail("S5", f"{name}: an example is set in a retired setting (\"{phrase}\")")
        if (name in ("Start", "Glossary") or name in built_tabs) and "to check:" in low:
            fail("S7", f"{name} is built and still carries a \"To check:\" line")
        if BORROW.search(text):
            fail("S13", f"{name}: \"{BORROW.search(text).group(0)}\": a source entry never tells the reader to borrow or buy")
        # T9: American punctuation, a comma or a period inside the closing quotation mark
        outside = list(OUTSIDE.finditer(text))
        for o_ in outside[:3]:
            ctx_ = text[max(0, o_.start() - 40):o_.end() + 10].replace("\n", " ")
            fail("T9", f"{name}: a comma or a period after a closing quotation mark, where American punctuation puts it inside: \"...{ctx_}...\"")
        if len(outside) > 3:
            fail("T9", f"{name}: and {len(outside) - 3} more commas or periods after a closing quotation mark")
        s14_checks(name, text)
        if name in ("Start", "Glossary"):
            continue
        if name == getattr(sd, "CLOSING_TAB", None):   # The Compass: every section speaks to the reader (S21)
            heads = set(re.findall(r"(?m)^## (.+)$", text)) - {"The compass"}
            for sec in _sections(text, heads):
                if not re.search(r"\byou(r|'re|'ll|'ve|'d)?\b", sec, re.I):
                    fail("E1", f"{name}: a section that should speak to the reader never says \"you\": {sec.strip()[:50]}")
        for sec in _sections(text, {"Why this matters", "Why a PM cares", "Why a PM should care"}):
            if not re.search(r"\byou(r|'re|'ll|'ve|'d)?\b", sec, re.I):
                fail("E1", f"{name}: a section that should speak to the reader never says \"you\": {sec.strip()[:50]}")
        # S10: every full path carries one story, its entry opening with its medium; a story says what
        # you'll get and carries no "Why trust it" (a documentary may). S11: a built module's full path
        # recommends five things at most, the story included.
        paths = _sections(text, {"Go deeper: the full path"})
        if name in long_tabs and name in built_tabs:
            # S11: a module that runs long on purpose says so, and why, at the start of its Why this matters
            wtm_ = _sections(text, {"Why this matters"})
            first_ = wtm_[0].strip().split("\n\n")[0] if wtm_ else ""
            if not re.search(r"\blonger\b", first_):
                fail("S11", f"{name} runs longer than the other modules, and the first paragraph of its Why this matters doesn't say so")
        if name not in ("About",) and re.match(r"\d+ ", name) and not paths:
            fail("S10", f"{name} has no full path, so it carries no story")
        for sec in paths:
            stories, count, books = [], 0, 0
            # S23: a built module's full path opens with one line, "If you read one:", naming one of its own
            # entries that isn't its story.
            ones = re.findall(r"(?m)^\*\*If you read one:\*\* \*(.+?)\*\. \S", sec)
            entries_ = {}
            for entry in re.split(r"\n(?=- \*\*)", sec):
                m_ = re.match(r"- \*\*(.+?)\*\*(?!\*)\s*(.*)", entry, re.S)
                t_ = re.match(r"\[?\*(.+?)\*", m_.group(1)) if m_ else None   # the entry's title, in italics
                if t_:
                    entries_[t_.group(1).strip()] = bool(STORY.match(m_.group(2)))
            if name in built_tabs:
                if len(ones) != 1:
                    fail("S23", f"{name}: the full path has {len(ones)} \"If you read one\" lines, and it opens with one")
                elif ones[0] not in entries_:
                    fail("S23", f"{name}: \"If you read one\" names {ones[0]}, which isn't on its full path")
                elif entries_[ones[0]]:
                    fail("S23", f"{name}: \"If you read one\" names its story, {ones[0]}, and the line is for a book or an article")
            for entry in re.split(r"\n(?=- \*\*)", sec):
                m_ = re.match(r"- \*\*(.+?)\*\*(?!\*)\s*(.*)", entry, re.S)
                if not m_:
                    continue
                count += 2 if re.match(r"(?:A pair of|Two) ", m_.group(2)) else 1
                title = re.sub(r"[*\[\]]|\(http[^)]*\)", "", m_.group(1))[:50]
                # what the entry says of itself: a story's first line (its plot may mention hours), else all before its reasons
                lead_ = m_.group(2).strip().split("\n")[0] if STORY.match(m_.group(2)) else m_.group(2).split("**Why trust it:**")[0].split("**What you'll get:**")[0]
                if name in built_tabs and LENGTH.search(lead_):
                    fail("S13", f"{name}: {title} gives \"{LENGTH.search(lead_).group(0)}\", and a full path gives no page count or running time")
                if name in built_tabs and not STORY.match(m_.group(2)) and not LONG_KIND.match(m_.group(2)):
                    fail("S12", f"{name}: {title} doesn't open by naming a long kind (a book, a journal article, a paper, a report): \"{m_.group(2)[:40]}\"")
                if not STORY.match(m_.group(2)):
                    books += 1 if BOOK.match(m_.group(2)) else 0
                    short = [t for t in SHORT.finditer(m_.group(2)) if not t.group(1) or int(t.group(1)) < 30]
                    if name in built_tabs and short:
                        fail("S12", f"{name}: {title} takes {short[0].group(0)}, and nothing on a full path but its story takes under about 30 minutes")
                if STORY.match(m_.group(2)):
                    title = re.sub(r"[*\[\]]|\(http[^)]*\)", "", m_.group(1))[:50]
                    stories.append(title)
                    if "Why trust it:" in entry and not re.match(r"(?:An? )?documentary", m_.group(2), re.I):
                        fail("S10", f"{name}: the story {title} carries a \"Why trust it\", and a story is there to make the lesson stick, not as evidence")
                    if "What you'll get:" not in entry:
                        fail("S10", f"{name}: the story {title} doesn't say what you'll get")
                    # S10: its credit ends with who made it and when, a year or a first and last: "(HBO, 2014 to 2019)";
                    # a pair gives each of its two the same way
                    years_ = re.findall(r"\([^()]*, (?:from )?(\d{4})(?: to (\d{4}))?\)", m_.group(1))
                    want_ = 2 if re.match(r"(?:A pair of|Two) ", m_.group(2)) else 1
                    screen_ = not re.match(r"(?:An? )?(?:novel|play)\b", m_.group(2), re.I)
                    if screen_ and (len(years_) < want_ or not re.search(r"\([^()]*, (?:from )?\d{4}(?: to \d{4})?\)$", m_.group(1).strip())):
                        fail("S10", f"{name}: the story {title}'s credit doesn't end with who made it and when, as \"(HBO, 2014 to 2019)\" or \"(Paramount, 2016)\": \"{m_.group(1)[-60:]}\"")
            if len(stories) > 1:
                fail("S10", f"{name}: the full path carries {len(stories)} stories, and one is the most: {'; '.join(stories)}")
            if not stories:
                fail("S10", f"{name}: the full path carries no story, and every full path carries one")
            most = 6 if name in long_tabs else 5
            if name in built_tabs and count > most:
                fail("S11", f"{name}: the full path recommends {count} things, and {'six' if most == 6 else 'five'} is the most")
            if name in built_tabs and name not in S12_PENDING and books < 2:
                fail("S12", f"{name}: the full path holds {books} book{'' if books == 1 else 's'} beside its story, and two is the least")
        own = _own_words(text)
        flat = " ".join(own.split())
        for o in own_words:
            if o["unit"] == name:
                said = " ".join(o["text"].translate(sd.QUOTES).split())
                if said not in flat:
                    fail("E3", f"{name}: the owner's own sentence is no longer there word for word: \"{said[:60]}...\"")
                flat = flat.replace(said, " ")
        own = flat
        full = sum(len(re.findall(a, own, re.I)) for a, b in CONTRACTIONS)
        short = sum(len(re.findall(b, own, re.I)) for a, b in CONTRACTIONS)
        if full + short >= 8 and short / (full + short) < 0.6:
            fail("E2", f"{name}: {short} of {full + short} places a contraction could go use one ({short / (full + short):.0%}, needs 60%)")
        # "I" the pronoun is followed by a verb; "Part I", "section I," and RACI's "I" are not
        m_ = re.search(r"(?<![\w'])(?:(?<!Part )(?<!Section )(?<!section )(?<!Chapter )(?<!chapter )(?<!Phase )I(?= [a-z])|I'm|I've|I'd|I'll|my|me|mine|myself)(?![\w'])", own)
        if m_:
            ctx_ = own[max(0, m_.start() - 30):m_.end() + 30].replace("\n", " ")
            fail("E3", f"{name}: first person outside a quotation: \"...{ctx_}...\"")


JS_EDIT = """() => [...document.querySelectorAll('.edit')].map(e => { const ins = e.querySelector('ins'), del = e.querySelector('del');
  const rg = document.createRange(); rg.selectNodeContents(ins);
  const a = rg.getBoundingClientRect(), b = del.getBoundingClientRect(), cs = getComputedStyle(ins), ds = getComputedStyle(del);
  const block = e.closest('p, li, dd, td, blockquote'), bs = getComputedStyle(block), br = block.getBoundingClientRect();
  const range = document.createRange(), others = [];
  const w = document.createTreeWalker(e.closest('p, li, blockquote, div'), NodeFilter.SHOW_TEXT); let n;
  while ((n = w.nextNode())) { if (e.contains(n) || !n.textContent.trim()) continue; range.selectNodeContents(n); for (const r of range.getClientRects()) others.push([r.left, r.top, r.right, r.bottom]); }
  const m = new DOMMatrixReadOnly(cs.transform === 'none' ? undefined : cs.transform);
  const glyph = (node, last) => { if (!node || node.nodeType !== 3) return null; const t = node.textContent, i = last ? t.trimEnd().length - 1 : t.length - t.trimStart().length;
    if (i < 0 || i >= t.length) return null; const r = document.createRange(); r.setStart(node, i); r.setEnd(node, i + 1); const g = r.getBoundingClientRect();
    return Math.abs(g.bottom - b.bottom) < b.height / 2 ? g : null; };
  const pv = glyph(e.previousSibling, true), nx = glyph(e.nextSibling, false);
  return {ins: [a.left, a.top, a.right, a.bottom], del: [b.left, b.top, b.right, b.bottom], face: cs.fontFamily.split(',')[0].replace(/["']/g, '').trim().toLowerCase(),
    stroke: ds.backgroundImage, line: ds.textDecorationLine, order: !!(ins.compareDocumentPosition(del) & Node.DOCUMENT_POSITION_FOLLOWING), old: del.textContent.trim(), others,
    W: document.documentElement.clientWidth, end: br.right - parseFloat(bs.paddingRight) - parseFloat(bs.borderRightWidth),
    em: parseFloat(cs.fontSize), wordEm: parseFloat(ds.fontSize), angle: Math.atan2(m.b, m.a) * 180 / Math.PI,
    gaps: [pv ? b.left - pv.right : null, nx ? nx.left - b.right : null]}; })"""


def edit_checks(ctx, base):
    """H2: a line edit in the owner's hand. The new words sit above the old word, in his hand, clear of the lines
    around it and of the screen's edge; the old word carries a drawn stroke; the new words come first in the source."""
    checked("H2")
    seen = 0
    strokes = set()
    for w, scheme in ((320, "light"), (340, "light"), (390, "light"), (390, "dark"), (1280, "light"), (1280, "dark")):
        c = ctx(viewport={"width": w, "height": 900}, color_scheme=scheme); pg = c.new_page()
        for path in ["/pm/", "/pm/all/"]:
            pg.goto(base + path); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(100)
            for e in pg.evaluate(JS_EDIT):
                seen += 1; where = f"{path} at {w} {scheme}, \"{e['old']}\""
                il, it, ir, ib = e["ins"]; dl, dt, dr, db = e["del"]
                if ib > dt + 2:
                    fail("H2", f"{where}: the new words do not sit above the old word")
                if min(ir, dr) - max(il, dl) < min(ir - il, dr - dl) / 2:
                    fail("H2", f"{where}: the new words are not written over the old word")
                if ir < e["end"] - 1 and not (dl - 0.6 * e["em"] <= il <= dl + 1):
                    fail("H2", f"{where}: the new words do not start just before the old word ({il - dl:+.0f}px)")
                if ir > e["end"] + 1:
                    fail("H2", f"{where}: the new words run past the end of the line ({ir - e['end']:.0f}px)")
                if not -6.5 <= e["angle"] <= -2.5:
                    fail("H2", f"{where}: the new words rise {-e['angle']:.1f} degrees to the right, not 3 to 6")
                if e["face"] != "shantell sans":
                    fail("H2", f"{where}: the new words are set in {e['face']}, not in the owner's hand")
                if "url(" not in e["stroke"] and "line-through" not in e["line"]:
                    fail("H2", f"{where}: the old word is not scratched out")
                if not e["order"]:
                    fail("H2", f"{where}: the old word comes before the new words in the source")
                if il < -1 or ir > e["W"] + 1:
                    fail("H2", f"{where}: the new words run past the edge of the screen")
                if any(l < ir - 1 and r > il + 1 and t_ < ib - 2 and b > it + 2 for l, t_, r, b in e["others"]):
                    fail("H2", f"{where}: the new words touch the text around them")
                # the old word keeps an ordinary space beside it: from its scratch to the next letter on its line, either side
                for g in (g for g in e["gaps"] if g is not None):
                    if g > 0.5 * e["wordEm"]:
                        fail("H2", f"{where}: the old word has {g:.0f}px beside it, more than an ordinary space")
                strokes.add((scheme, e["stroke"]))
        if w == 1280:   # three strokes, and each takes the page's ink
            pg.goto(base + "/pm/")
            got = pg.evaluate("""() => { const d = document.querySelector('.edit del'); if (!d) return []; const out = [];
              for (const v of ['scratch-v1', 'scratch-v2', 'scratch-v3']) { d.className = v; out.push(getComputedStyle(d).backgroundImage); } return out; }""")
            if len(set(got)) < 3:
                fail("H2", f"{scheme}: the scratch has {len(set(got))} strokes, expected 3")
            strokes.update((scheme, g) for g in got)
        c.close()
    if not seen:
        fail("H2", "no line edit was found on the Start page")
    light = {s for sc, s in strokes if sc == "light"}; dark = {s for sc, s in strokes if sc == "dark"}
    if light & dark:
        fail("H2", "the scratch is drawn in one ink for light and dark screens")


# ---------- X5: the preview, the whole site in one page on claude.ai ----------
PREVIEW = {}   # what preview_checks made: the tool, the page in its stand-in frame, and the pages it holds


def _preview_tool():
    import importlib.util
    spec = importlib.util.spec_from_file_location("preview", os.path.join(ROOT, "tools", "preview.py"))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def preview_checks(out_dir):
    """X5: the preview can be made from the build, holds every page a reader can reach, and points nowhere outside."""
    checked("X5")
    pv = _preview_tool()
    try:
        page, pages, problems = pv.build(out_dir)
    except Exception as e:
        fail("X5", f"tools/preview.py could not make the preview: {str(e).splitlines()[0][:160]}"); return
    for p in problems:
        fail("X5", f"the preview: {p}")
    held = {p.path for p in pages}
    for path in PAGES:
        if path != "/pm/all/" and path not in held:
            fail("X5", f"the preview doesn't hold {path}, which a reader can reach on the site")
    lock = json.load(open(pv.LOCK, encoding="utf-8")) if os.path.exists(pv.LOCK) else {}
    if not lock.get("url"):
        fail("X5", "tools/preview.lock.json names no preview: publish it, then record it (CLAUDE.md, 'The preview')")
    elif lock.get("sha256") != pv.sha(page):
        NOTE["X5"].append(f"the preview differs from what was last published ({lock.get('published', 'never')}): "
                          "republish it, then record it (CLAUDE.md, 'The preview')")
    d = tempfile.mkdtemp(prefix="preview-")
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(pv.STAND_IN + page + "</body></html>\n")
    PREVIEW.update(tool=pv, dir=d, pages=[p.path for p in pages])


def preview_render_checks(ctx, base):
    """X5: each page in the preview, in a stand-in for claude.ai's frame, renders as the site renders it."""
    pv, srv = PREVIEW["tool"], Server(PREVIEW["dir"])

    def shot(pg):
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(100)
        return Image.open(io.BytesIO(pg.screenshot(full_page=True))).convert("RGB")

    def same(a, b, where):
        if a.size != b.size:
            fail("X5", f"{where}: the preview's page is {b.size[0]}x{b.size[1]}, the site's {a.size[0]}x{a.size[1]}"); return
        diff = ImageChops.difference(a, b).convert("L").point(lambda v: 255 if v > 24 else 0)
        share = sum(diff.histogram()[255:]) / (a.width * a.height)
        if share > 0.005:
            fail("X5", f"{where}: the preview's page differs from the site's in {share:.1%} of pixels")

    sample = ["/", "/pm/find-the-constraint/", "/pm/cards/stocks-flows-feedback/", "/pm/glossary/"]
    runs = [("light", w, PREVIEW["pages"], None) for w in (390, 1280)]
    runs += [("dark", w, sample, None) for w in (390, 1280)]
    # A theme picked in claude.ai sets data-theme on the root, whatever the system's setting is.
    runs += [("light", 1280, sample[:2], "dark"), ("dark", 1280, sample[:2], "light")]
    try:
        for scheme, w, paths, picked in runs:
            c_site = ctx(viewport={"width": w, "height": 900}, color_scheme=picked or scheme, device_scale_factor=1)
            c_prev = ctx(viewport={"width": w, "height": 900}, color_scheme=scheme, device_scale_factor=1)
            site, prev = c_site.new_page(), c_prev.new_page()
            prev.goto(srv.base + "/"); prev.wait_for_load_state("load")
            if picked:
                prev.evaluate(f"document.documentElement.setAttribute('data-theme', '{picked}')")
            for path in paths:
                site.goto(base + path); site.wait_for_load_state("load")
                prev.evaluate(f"location.hash = '{pv.key_of(path)}'")
                where = f"{path} {scheme}{' with ' + picked + ' picked in claude.ai' if picked else ''} {w}px"
                same(shot(site), shot(prev), where)
            c_site.close(); c_prev.close()
    finally:
        srv.close()


def page_checks(base, out_dir, tokens, update_baseline, fix_base=None):
    axe_path = os.path.join(TESTS, "node_modules", "axe-core", "axe.min.js")
    axe_src = open(axe_path).read() if os.path.exists(axe_path) else None
    if not axe_src:
        fail("A1", "axe-core not installed: run npm install --prefix tests")
    chrome = os.environ.get("CHROME") or (shutil.which("google-chrome") or None)
    shots_dir = tempfile.mkdtemp(prefix="shots-")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome) if chrome else p.chromium.launch()

        def ctx(**kw):
            return browser.new_context(**kw)

        if run_for("R1", "R2"):
            # R1, R2: no sideways scrolling
            checked("R1", "R2")
            for w, h in [(w, 900) for w in WIDTHS] + [(844, 390), (640, 800)]:
                c = ctx(viewport={"width": w, "height": h}); pg = c.new_page()
                for path in PAGES:
                    pg.goto(base + path); pg.wait_for_load_state("load")
                    sw = pg.evaluate("document.documentElement.scrollWidth")
                    if sw > w:
                        rule = "R2" if w == 640 else "R1"
                        fail(rule, f"{path} scrolls sideways at {w}x{h} ({sw}px)")
                c.close()

        if run_for("C1", "C2", "C3", "C5", "W2", "W3", "M1", "M2", "M3", "R3", "R4", "R5", "R9", "A1", "A3", "T1", "T2", "V1"):
            # Colour roles, weight, margin, targets, focus, axe: light and dark, phone and desktop
            checked("C1", "C2", "C3", "C5", "W2", "W3", "M1", "M2", "M3", "R3", "R4", "R5", "R9", "A1", "A2", "A3", "T1", "T2")
            for scheme in ("light", "dark"):
                for w in (390, 1280):
                    c = ctx(viewport={"width": w, "height": 900}, color_scheme=scheme, device_scale_factor=1); pg = c.new_page()
                    for path in PAGES:
                        pg.goto(base + path); pg.wait_for_load_state("load"); pg.evaluate("document.fonts.ready")
                        where = f"{path} {scheme} {w}px"
                        orange = pg.evaluate(JS_ORANGE)
                        # C1
                        for t in pg.evaluate(JS_TEXT_COLORS, orange):
                            if not t["inH1"]:
                                fail("C1", f"{where}: orange text in {t['tag']}.{t['cls']}: '{t['text']}'")
                        # C2
                        ink = pg.evaluate(JS_VAR, "--ink")
                        for f_ in pg.evaluate(JS_FILLS, [orange, ink]):
                            if not (f_["game"] or f_["skip"]):
                                fail("C2", f"{where}: filled {f_['tag']}.{f_['cls']} behind '{f_['text']}'")
                        # C3
                        yellows = [pg.evaluate(JS_VAR, "--mark"), pg.evaluate(JS_VAR, "--mark-soft")]
                        allowed = "mark, .answer, .takeaway, .pile, .st-range, .recall .answer"
                        bad = pg.evaluate("""([cols, allowed]) => [...document.querySelectorAll('body *')].filter(el => cols.includes(getComputedStyle(el).backgroundColor) && el.getBoundingClientRect().width && !el.matches(allowed)).map(el => el.tagName + '.' + el.className)""", [yellows, allowed])
                        for b in bad:
                            fail("C3", f"{where}: yellow fill on {b}")
                        # C5
                        bad = pg.evaluate("""() => [...document.querySelectorAll('a')].filter(a => !a.matches('.site-name, .site-nav a, .door-links a, .skip, .unit-nav a, .course-bar a, nav.az a') && a.getBoundingClientRect().width && !getComputedStyle(a).textDecorationLine.includes('underline')).map(a => a.textContent.trim().slice(0, 30))""")
                        for b in bad:
                            fail("C5", f"{where}: link without underline: '{b}'")
                        for b in pg.evaluate(JS_LINK_LINES):
                            fail("C5", f"{where}: {b}")
                        # W2
                        if pg.evaluate("(o) => [...document.querySelectorAll('h2')].some(h => getComputedStyle(h).color === o)", orange):
                            fail("W2", f"{where}: an h2 is orange")
                        # W3
                        small = pg.evaluate("""() => { const p = document.querySelector('.prose p, .door-text p'); if (!p) return []; const body = parseFloat(getComputedStyle(p).fontSize);
                          return [...document.querySelectorAll('.kicker, .meta, .hint, .meta-line, .source-note, .one-thing-label, .carry-label')].filter(e => e.getBoundingClientRect().width && parseFloat(getComputedStyle(e).fontSize) >= body).map(e => e.className); }""")
                        for s in small:
                            fail("W3", f"{where}: label {s} is not smaller than body text")
                        # M1, M2, M3, R3 (desktop only)
                        if w == 1280:
                            m = pg.evaluate(JS_MARGIN)
                            if m:
                                boxes = []
                                for e in m["inMargin"]:
                                    if not e["owner"]:
                                        fail("M1", f"{where}: {e['tag']}.{e['cls']} sits in the margin, and is not one of the owner's notes")
                                    else:
                                        boxes.append(e)
                                boxes.sort(key=lambda b: b["top"])
                                for a_, b_ in zip(boxes, boxes[1:]):
                                    if b_["top"] < a_["bottom"] - 1:
                                        fail("M2", f"{where}: margin notes overlap at y={b_['top']:.0f}")
                        # R4
                        if path == "/":
                            r = pg.evaluate("() => { const i = document.querySelector('.door-photo').getBoundingClientRect(); const h = document.querySelector('.door h1').getBoundingClientRect(); return {i: [i.left, i.top, i.right, i.bottom], h: [h.left, h.top, h.right, h.bottom]}; }")
                            i, h_ = r["i"], r["h"]
                            if w >= 1024 and not (i[0] >= h_[2] - 1):
                                fail("R4", f"{where}: photo is not beside the name")
                            if w < 1024 and not (i[3] <= h_[1] + 1):
                                fail("R4", f"{where}: photo is not above the name")
                        # R9: on every page, the name and the menu on one line: the sections from 46rem up, and below it the
                        # current section and the Menu button (site_menu_checks has the rest)
                        r = pg.evaluate(JS_MENU)
                        if r:
                            n = r["name"]
                            row = [t[1:] for t in r["links"]] if w >= MENU_WIDE else [x for x in (r["here"], r["btn"]) if x]
                            if not row or any(x[3] <= n[1] or x[1] >= n[3] for x in row) or max(x[1] for x in row) - min(x[1] for x in row) > 2:
                                fail("R9", f"{where}: the menu doesn't share the name's line")
                        # R5
                        small_targets = pg.evaluate("""() => [...document.querySelectorAll('button, input, summary, .door-links a, .site-nav a, .tick')].filter(e => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e); if (!r.width || s.display === 'none') return false; if (e.matches('input') && e.closest('.tick')) return false; if (e.matches('button.term, a.term')) return false; const t = (e.matches('input') && e.closest('label')) ? e.closest('label').getBoundingClientRect() : r; const min = e.matches('.door-links a') ? 44 : 24; return t.width < min - 0.5 || t.height < min - 0.5; }).map(e => e.tagName + '.' + e.className + ' ' + Math.round(e.getBoundingClientRect().width) + 'x' + Math.round(e.getBoundingClientRect().height))""")
                        for s in small_targets:
                            fail("R5", f"{where}: small target {s}")
                        # A3
                        for n in pg.evaluate("() => [...document.querySelectorAll('.door-links a')].filter(a => !a.textContent.trim() && !a.getAttribute('aria-label')).length"),:
                            if n:
                                fail("A3", f"{where}: {n} icon links without a name")
                        # T1: fonts in use have loaded
                        bad = pg.evaluate("""() => { const fams = new Set(); for (const el of document.querySelectorAll('body *')) { const r = el.getBoundingClientRect(); if (!r.width || !el.childNodes.length) continue; const f = getComputedStyle(el).fontFamily.split(',')[0].replace(/["']/g, '').trim(); fams.add(f); }
                          return [...fams].filter(f => ['newsreader','public sans','libre franklin','shantell sans'].includes(f.toLowerCase()) && ![...document.fonts].some(ff => ff.family.replace(/["']/g,'').toLowerCase() === f.toLowerCase() && ff.status === 'loaded')); }""")
                        for f_ in bad:
                            fail("T1", f"{where}: font {f_} is used but did not load")
                        # T2: line length
                        if w in (1280,):
                            long = pg.evaluate("""() => { const c = document.createElement('canvas').getContext('2d'); const sample = 'the quick brown fox jumps over a lazy dog and then sits in the sun'; const out = [];
                              for (const p of document.querySelectorAll('.prose p, .door-text p, .unit-head .question')) { const r = p.getBoundingClientRect(); if (!r.width) continue; const s = getComputedStyle(p); c.font = s.fontStyle + ' ' + s.fontWeight + ' ' + s.fontSize + ' ' + s.fontFamily; const avg = c.measureText(sample).width / sample.length; const chars = p.clientWidth / avg; if (chars > 85) out.push(Math.round(chars)); } return out; }""")
                            for n in long:
                                fail("T2", f"{where}: reading lines run to about {n} characters")
                        # A1: axe
                        if axe_src:
                            pg.add_script_tag(content=axe_src)
                            res = pg.evaluate("""async () => { const r = await axe.run(document, {runOnly: {type: 'tag', values: ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}}); return r.violations.map(v => ({id: v.id, impact: v.impact, n: v.nodes.length, target: v.nodes[0] && v.nodes[0].target.join(' ')})); }""")
                            for v in res:
                                fail("A1", f"{where}: {v['id']} ({v['impact']}) on {v['n']} node(s), e.g. {v['target']}")
                            if path == "/pm/find-the-constraint/" and w == 1280 and scheme == "light":
                                NOTE["A1"].append("axe ran on every page; it leaves color contrast over drawn highlights as 'incomplete', which C4 covers from the tokens")
                        # V1 screenshot for baseline comparison
                        name = (path.strip("/").replace("/", "_") or "home") + f"-{w}-{scheme}.png"
                        pg.screenshot(path=os.path.join(shots_dir, name), full_page=True)
                    c.close()

        if run_for("A2"):
            # A2: focus ring on everything reachable by keyboard (module and home pages)
            for path in ["/", "/pm/find-the-constraint/", "/pm/cards/goodharts-law/"]:
                c = ctx(viewport={"width": 1280, "height": 900}); pg = c.new_page(); pg.goto(base + path)
                seen = 0
                for _ in range(80):
                    pg.keyboard.press("Tab")
                    info = pg.evaluate("""() => { const e = document.activeElement; if (!e || e === document.body) return null;
                      const t = e.matches('.tick input') ? e.nextElementSibling : e; const s = getComputedStyle(t);
                      const ring = (s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) >= 2) || s.outlineStyle === 'auto' || (s.boxShadow && s.boxShadow !== 'none');
                      return {ring, name: e.tagName + '.' + e.className + ' ' + (e.textContent || '').trim().slice(0, 20)}; }""")
                    if not info:
                        break
                    seen += 1
                    if not info["ring"]:
                        fail("A2", f"{path}: no visible focus on {info['name']}")
                c.close()

        if run_for("D1"):
            # D1: without JavaScript
            checked("D1", "D2", "D3", "D5")
            c = ctx(viewport={"width": 390, "height": 900}, java_script_enabled=False); pg = c.new_page()
            for g, mid in GAMES.items():
                pg.goto(base + f"/pm/{mid}/")
                v = pg.evaluate("""() => ({example: getComputedStyle(document.querySelector('.game .example')).display, takeaway: getComputedStyle(document.querySelector('.game .takeaway')).display,
                     live: getComputedStyle(document.querySelector('.game-live')).display, folded: [...document.querySelectorAll('.recall')].every(d => !d.open),
                     terms: [...document.querySelectorAll('.term')].map(t => t.tagName === 'A' ? t.getAttribute('href') : null)})""")
                if v["example"] == "none" or v["takeaway"] == "none":
                    fail("D1", f"the {g} game: without JavaScript the recorded run or takeaway is hidden")
                if v["live"] != "none":
                    fail("D1", f"the {g} game: without JavaScript the live game controls show")
                if not v["folded"]:
                    fail("D1", f"{mid}: answers are not folded")
            glossary_html = open(os.path.join(out_dir, "pm", "glossary", "index.html"), encoding="utf-8").read()
            for href in v["terms"]:
                if not href:
                    fail("D1", "a glossary term is not a link, so it does nothing without JavaScript")
                    continue
                anchor = href.split("#")[-1]
                if f'id="{anchor}"' not in glossary_html:
                    fail("D1", f"glossary term links to #{anchor}, which the glossary page lacks")
            c.close()

        if run_for("D2"):
            # D2: with JavaScript but no dialog support, a term still reaches its definition
            c = ctx(viewport={"width": 390, "height": 900}); pg = c.new_page()
            pg.add_init_script("if (window.HTMLDialogElement) { delete HTMLDialogElement.prototype.showModal; }")
            pg.goto(base + "/pm/find-the-constraint/")
            pg.click(".term")
            pg.wait_for_timeout(300)
            if "/pm/glossary/" not in pg.url:
                fail("D2", f"without dialog support, tapping a term stays on {pg.url}")
            c.close()
            # and with dialog support, tapping opens the definition in place
            c = ctx(viewport={"width": 390, "height": 900}); pg = c.new_page(); pg.goto(base + "/pm/find-the-constraint/")
            pg.click(".term"); pg.wait_for_timeout(200)
            if "/pm/glossary/" in pg.url or not pg.evaluate("!!document.querySelector('dialog.gloss[open]')"):
                fail("D2", "with dialog support, tapping a term does not open its definition in place")
            c.close()

        if run_for("A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12"):
            a11y_checks(browser, ctx, base, out_dir)
        if run_for("J8"):
            play_checks(ctx, base)
        if run_for("G6"):
            rail_checks(ctx, base)
        if fix_base and run_for("M1", "M2", "M3", "R3", "R7", "A13", "A1"):
            try:
                margin_checks(ctx, fix_base, axe_src)
            except Exception as e:  # a broken page must fail its rule, not stop the suite
                fail("M1", f"sample-note check could not finish: {str(e).splitlines()[0][:160]}")
        if run_for("R10"):
            try:
                full_path_checks(ctx, base, fix_base)
            except Exception as e:  # a broken page must fail its rule, not stop the suite
                fail("R10", f"check could not finish: {str(e).splitlines()[0][:160]}")
        if fix_base and run_for("M1", "M2"):
            try:
                print_margin_checks(ctx, fix_base)
            except Exception as e:  # a broken page must fail its rule, not stop the suite
                fail("M1", f"sample-note print check could not finish: {str(e).splitlines()[0][:160]}")
        if run_for("H1"):
            try:
                variant_checks(ctx, base)
            except Exception as e:  # a broken page must fail its rule, not stop the suite
                fail("H1", f"check could not finish: {str(e).splitlines()[0][:160]}")
        if run_for("H2"):
            try:
                edit_checks(ctx, base)
            except Exception as e:  # a broken page must fail its rule, not stop the suite
                fail("H2", f"check could not finish: {str(e).splitlines()[0][:160]}")
        if run_for("C6"):
            try:
                highlighter_checks(ctx, base)
            except Exception as e:  # a broken page must fail its rule, not stop the suite
                fail("C6", f"check could not finish: {str(e).splitlines()[0][:160]}")
        if run_for("R6"):
            try:
                circle_checks(ctx, base)
            except Exception as e:  # a broken page must fail its rule, not stop the suite
                fail("R6", f"check could not finish: {str(e).splitlines()[0][:160]}")
        if run_for("T2", "T4", "T5", "T6", "T7", "T8", "W4", "R7", "A13"):
            try:
                scale_checks(ctx, base)
            except Exception as e:  # a broken page must fail its rule, not stop the suite
                fail("T4", f"check could not finish: {str(e).splitlines()[0][:160]}")

        if run_for("D3"):
            # D3: without web fonts
            c = ctx(viewport={"width": 390, "height": 900}); pg = c.new_page()
            pg.route("**/*.woff2", lambda r: r.abort())
            for path in PAGES:
                pg.goto(base + path)
                if pg.evaluate("document.documentElement.scrollWidth") > 390:
                    fail("D3", f"{path} scrolls sideways without web fonts")
            c.close()

        if run_for("D5"):
            # D5: reduced motion
            c = ctx(viewport={"width": 1280, "height": 900}, reduced_motion="reduce"); pg = c.new_page()
            pg.goto(base + "/pm/find-the-constraint/"); pg.click("[data-play]")
            if pg.evaluate("document.querySelector('[data-round]').textContent") != "20":
                fail("D5", "with reduced motion the dice game does not finish at once")
            if pg.evaluate("getComputedStyle(document.querySelector('.pile')).transitionDuration") not in ("0s", ""):
                fail("D5", "with reduced motion the piles still animate")
            weeks = yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "waitgame.yaml"), encoding="utf-8"))["weeks"]
            pg.goto(base + f"/pm/{GAMES['waiting']}/"); pg.click("[data-pick=fix]"); pg.click("[data-pick=reorder]"); pg.click("[data-play]")
            if pg.evaluate("document.querySelector('[data-week]').textContent") != str(weeks):
                fail("D5", "with reduced motion the waiting game does not finish at once")
            pg.goto(base + f"/pm/{GAMES['ranking']}/"); pg.click("[data-play]")
            if pg.evaluate("getComputedStyle(document.querySelector('.rk-dot')).transitionDuration") not in ("0s", ""):
                fail("D5", "with reduced motion the ranking game's stores still glide")
            pg.goto(base + f"/pm/{GAMES['dice']}/")
            if any(d not in ("0s", "") for d in pg.evaluate("[...document.querySelectorAll('main a')].slice(0, 20).map(a => getComputedStyle(a).transitionDuration.split(',')[0].trim())")):
                fail("D5", "with reduced motion a link still eases on hover")
            c.close()
            c = ctx(viewport={"width": 1280, "height": 900}); pg = c.new_page(); pg.goto(base + "/pm/find-the-constraint/")
            checked("C5")
            dur = pg.evaluate("getComputedStyle(document.querySelector('main a')).transitionDuration.split(',')[0].trim()")
            if dur in ("0s", ""):
                fail("C5", "a link's change on hover does not ease in")
            c.close()

        if run_for("P3", "P4", "C5"):
            # P3: print is light, has no header or footer, shows answers
            checked("P1", "P2", "P3")
            c = ctx(viewport={"width": 1280, "height": 900}, color_scheme="dark"); pg = c.new_page()
            pg.goto(base + "/pm/all/"); pg.emulate_media(media="print", color_scheme="dark")
            pr = pg.evaluate("""() => ({bg: getComputedStyle(document.body).backgroundColor, ink: getComputedStyle(document.querySelector('.prose p')).color,
                 head: getComputedStyle(document.querySelector('.masthead')).display, answers: getComputedStyle(document.querySelector('.answers')).display})""")
            if pr["bg"] not in ("rgb(255, 255, 255)", "rgba(0, 0, 0, 0)"):
                fail("P3", f"print background is {pr['bg']} with a dark preference")
            if lum(tuple(int(x) for x in re.findall(r"\d+", pr["ink"])[:3])) > 0.2:
                fail("P3", f"print text is light ({pr['ink']}) with a dark preference")
            if pr["head"] != "none":
                fail("P3", "print shows the site header")
            if pr["answers"] == "none":
                fail("P3", "print hides the answers")
            checked("C5")
            for b in pg.evaluate("""() => [...document.querySelectorAll('main a')].filter(a => a.getClientRects().length && !getComputedStyle(a).textDecorationLine.includes('underline')).map(a => a.textContent.trim().slice(0, 30))"""):
                fail("C5", f"print: link without underline, so the PDF does not show it can be tapped: '{b}'")
            for b in pg.evaluate(JS_LINK_LINES):
                fail("C5", f"print: {b}")
            # P4: what prints must not be hidden from assistive technology, or the tagged PDF leaves it out
            checked("P4")
            for t in pg.evaluate("""() => [...document.querySelectorAll('[aria-hidden="true"]')].filter(el => !el.closest('svg') && el.getClientRects().length
                  && el.textContent.replace(/[\\d\\s.,:;]/g, '').length).map(el => el.tagName + '.' + el.className + ' "' + el.textContent.trim().slice(0, 40) + '"')"""):
                fail("P4", f"prints but is hidden from assistive technology, so the PDF leaves it untagged: {t}")
            c.close()
        if run_for("P7"):
            # P7: nothing that prints reaches past the page's text width, or Chrome shrinks the whole PDF to fit it
            checked("P7")
            W = page_text_width()
            c = ctx(viewport={"width": int(W), "height": 1100}); pg = c.new_page()
            pg.goto(base + "/pm/all/"); pg.emulate_media(media="print"); pg.evaluate("document.fonts.ready")
            for e in pg.evaluate("""() => { const W = document.documentElement.clientWidth; const out = [];
                  for (const el of document.querySelectorAll('body *')) { const r = el.getBoundingClientRect();
                    if (r.width && r.right > W + 0.5 && !el.parentElement.closest('svg')) out.push(el.tagName + '.' + (typeof el.className === 'string' ? el.className : '') + ' "' + (el.textContent || '').trim().slice(0, 40) + '" to ' + Math.round(r.right) + 'px'); }
                  if (!out.length && document.documentElement.scrollWidth > W) out.push('the page is ' + document.documentElement.scrollWidth + 'px wide');
                  return out.slice(0, 5); }"""):
                fail("P7", f"print: {e} reaches past the page's {int(W)}px, so the PDF prints shrunk")
            c.close()
        if run_for("S4"):
            try:
                sources_checks(ctx, base)
            except Exception as e:  # a broken page must fail its rule, not stop the suite
                fail("S4", f"check could not finish: {str(e).splitlines()[0][:160]}")
        if run_for("X5") and PREVIEW:
            try:
                preview_render_checks(ctx, base)
            except Exception as e:  # a broken preview must fail its rule, not stop the suite
                fail("X5", f"check could not finish: {str(e).splitlines()[0][:160]}")
        browser.close()
        if run_for("R8", "R1", "R7", "A13", "T4", "T5", "T6", "T8"):
            try:
                engine_checks(p, base)
            except Exception as e:  # a broken engine run must fail its rule, not stop the suite
                fail("R8", f"check could not finish: {str(e).splitlines()[0][:160]}")

    if run_for("P1", "P2", "P4", "P5", "P6", "R6", "S4", "L1", "M1"):
        # P1, P2, P4: the PDF, made by the same tool that makes the delivered file
        pdf = os.path.join(tempfile.mkdtemp(), "pilot.pdf")
        r = subprocess.run([sys.executable, os.path.join(ROOT, "tools-pm", "make-pdf.py"), out_dir, pdf, "check"], capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(pdf):
            for rule in ("P1", "P4", "P5", "P6"):
                fail(rule, f"tools-pm/make-pdf.py failed, so there is no PDF to check: {r.stderr.strip()[-300:]}")
            return
        checked("P4")
        info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
        raw = open(pdf, "rb").read()
        if not re.search(r"^Tagged:\s+yes", info, re.M) or b"/StructTreeRoot" not in raw:
            fail("P4", "the PDF is not tagged")
        if b"/Lang" not in raw:
            fail("P4", "the PDF does not declare its language")
        if b"/Outlines" not in raw:
            fail("P4", "the PDF has no bookmarks")
        figures = open(os.path.join(out_dir, "pm", "all", "index.html"), encoding="utf-8").read().count('role="img"')
        if raw.count(b"/Alt") < figures:
            fail("P4", f"{raw.count(b'/Alt')} figure text alternatives in the PDF, expected {figures}")
        struct = subprocess.run(["pdfinfo", "-struct", pdf], capture_output=True, text=True).stdout
        for tag in ("H1", "H2", "L", "Table"):
            if not re.search(rf"^\s*{tag}\b", struct, re.M):
                fail("P4", f"no {tag} elements in the PDF structure")

        if run_for("P5", "P6"):
            try:
                pdf_link_meta_checks(pdf, out_dir)
            except Exception as e:  # a broken PDF must fail its rule, not stop the suite
                fail("P5", f"PDF check could not finish: {str(e).splitlines()[0][:160]}")
        if run_for("M1"):
            try:
                pdf_note_checks(pdf, out_dir)
            except Exception as e:  # a broken PDF must fail its rule, not stop the suite
                fail("M1", f"PDF note check could not finish: {str(e).splitlines()[0][:160]}")
        if run_for("S4"):
            try:
                sources_pdf_check(pdf)
            except Exception as e:
                fail("S4", f"PDF check could not finish: {str(e).splitlines()[0][:160]}")
        if run_for("R6"):
            try:
                pdf_ring_checks(pdf)
            except Exception as e:  # a broken render must fail its rule, not stop the suite
                fail("R6", f"PDF check could not finish: {str(e).splitlines()[0][:160]}")

        pages = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout.split("\f")
        pages = [p for p in pages if p.strip()]
        if len(pages) != PRINT_PAGES:
            NOTE["P1"].append(f"the syllabus prints on {len(pages)} pages; the spec records {PRINT_PAGES}")
        try:
            unit_page_checks(pdf, len(pages))
        except Exception as e:  # a broken PDF must fail its rule, not stop the suite
            fail("P1", f"PDF check could not finish: {str(e).splitlines()[0][:160]}")
        for i, text in enumerate(pages):
            if "Concept card for" in text and "Go deeper" not in text:
                fail("P2", f"the concept card on PDF page {i + 1} runs onto the next page")
        if run_for("L1"):
            owner = (yaml.safe_load(open(os.path.join(ROOT, "hugo.yaml"))) or {}).get("copyright", "")
            for i, text in enumerate(pages):
                if not owner or owner not in text or "CC BY 4.0" not in text:
                    fail("L1", f"PDF page {i + 1} does not print the copyright line and the license")
            import pikepdf
            with pikepdf.open(pdf) as doc:
                x = doc.open_metadata()
                if "CC BY 4.0" not in str(x.get("dc:rights", "")) or not str(x.get("xmpRights:WebStatement", "")).startswith("https://creativecommons.org/"):
                    fail("L1", "the PDF's metadata does not state its rights and license")
        cards = sum("Concept card for" in t for t in pages)
        if cards != len(glob.glob(os.path.join(ROOT, "content", "pm", "cards", "*.md"))):
            fail("P2", f"{cards} card pages in the PDF, expected one per card")

    if run_for("V1"):
        # V1: compare to the approved baseline
        checked("V1")
        base_dir = os.path.join(TESTS, "baseline")
        if update_baseline:
            shutil.rmtree(base_dir, ignore_errors=True); os.makedirs(base_dir)
            for f in glob.glob(os.path.join(shots_dir, "*.png")):
                im = Image.open(f).convert("RGB"); im = im.resize((im.width // 2, im.height // 2))
                im.save(os.path.join(base_dir, os.path.basename(f)), optimize=True)
            NOTE["V1"].append("baseline recorded")
        elif not os.path.isdir(base_dir):
            NOTE["V1"].append("no approved baseline yet; record one with --update-baseline once the owner approves the look")
        else:
            for f in glob.glob(os.path.join(shots_dir, "*.png")):
                ref = os.path.join(base_dir, os.path.basename(f))
                im = Image.open(f).convert("RGB"); im = im.resize((im.width // 2, im.height // 2))
                if not os.path.exists(ref):
                    fail("V1", f"{os.path.basename(f)} has no baseline"); continue
                old = Image.open(ref).convert("RGB")
                if old.size != im.size:
                    fail("V1", f"{os.path.basename(f)} changed size {old.size} to {im.size}"); continue
                diff = ImageChops.difference(old, im).convert("L").point(lambda v: 255 if v > 24 else 0)
                share = sum(diff.histogram()[255:]) / (im.width * im.height)
                if share > 0.005:
                    fail("V1", f"{os.path.basename(f)} differs from the baseline in {share:.1%} of pixels")


def report():
    spec = open(os.path.join(TESTS, "SPEC.md")).read()
    rules = re.findall(r"\*\*([A-Z]\d+) (auto|review)\.\*\*", spec)
    lines = ["# Check report", "", "| Rule | Kind | Result |", "| --- | --- | --- |"]
    failed = 0
    for rid, kind in rules:
        if kind == "review":
            res = "needs review"
        elif (ONLY and rid not in ONLY or rid in SKIP) and rid not in FAIL:
            res = "skipped"
        elif rid in FAIL:
            res = f"FAIL ({len(FAIL[rid])})"; failed += 1
        elif rid in CHECKED:
            res = "pass"
        else:
            res = "NOT CHECKED"; failed += 1
        lines.append(f"| {rid} | {kind} | {res} |")
    lines += ["", "## Failures", ""]
    for rid, msgs in sorted(FAIL.items()):
        for m in msgs[:15]:
            lines.append(f"- **{rid}** {m}")
        if len(msgs) > 15:
            lines.append(f"- **{rid}** and {len(msgs) - 15} more")
    if not FAIL:
        lines.append("None.")
    lines += ["", "## Notes", ""] + [f"- **{k}** {m}" for k, ms in NOTE.items() for m in ms]
    open(os.path.join(TESTS, "report.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines[:len(rules) + 4]))
    # The failures go to the log as well as the report, so a failed run on GitHub can be read without its artifact.
    if FAIL:
        print("\n".join(lines[len(rules) + 4:lines.index("## Notes")]))
    print(f"\n{failed} rule(s) failing. Details in tests/report.md")
    return failed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--update-baseline", action="store_true")
    ap.add_argument("--only", default="", help="comma-separated rule IDs: run just the checks behind them")
    ap.add_argument("--skip", default="", help="comma-separated rule IDs: leave them out")
    ap.add_argument("--live", action="store_true", help="as publishing runs it: X4 fails while any voice slot is open")
    args = ap.parse_args()
    if args.live:
        LIVE.append(True)
    ONLY.update(r.strip() for r in args.only.split(",") if r.strip())
    SKIP.update(r.strip() for r in args.skip.split(",") if r.strip())
    out_dir = tempfile.mkdtemp(prefix="site-")
    build(out_dir)
    tokens = check_static()
    if run_for("L1"):
        license_checks(out_dir)
    if run_for("N1", "N2", "N3", "R9"):
        try:
            arrival_checks(out_dir)
        except Exception as e:  # a broken page must fail its rules, not stop the suite
            for r in ("N1", "N2", "N3"):
                fail(r, f"check could not finish: {str(e).splitlines()[0][:160]}")
    if run_for("S19"):
        try:
            start_checks(out_dir)
        except Exception as e:  # a broken page must fail its rule, not stop the suite
            fail("S19", f"check could not finish: {str(e).splitlines()[0][:160]}")
    if run_for("S20", "S21", "J3"):
        try:
            arc_checks(out_dir)
        except Exception as e:  # a broken page must fail its rules, not stop the suite
            for r in ("S20", "S21"):
                fail(r, f"check could not finish: {str(e).splitlines()[0][:160]}")
    if run_for("R9"):
        try:
            site_menu_checks(out_dir)
        except Exception as e:  # a broken page must fail its rule, not stop the suite
            fail("R9", f"check could not finish: {str(e).splitlines()[0][:160]}")
    if run_for("G1", "G2", "G3", "G4", "G5"):
        try:
            course_bar_checks(out_dir)
        except Exception as e:  # a broken page must fail its rules, not stop the suite
            for r in ("G1", "G2", "G3", "G4", "G5"):
                fail(r, f"check could not finish: {str(e).splitlines()[0][:160]}")
    if run_for("G6", "G7", "D5"):
        try:
            doors_checks(out_dir)
        except Exception as e:  # a broken page must fail its rules, not stop the suite
            for r in ("G6", "G7"):
                fail(r, f"check could not finish: {str(e).splitlines()[0][:160]}")
    if run_for("G8"):
        try:
            name_link_checks(out_dir)
        except Exception as e:  # a broken page must fail its rule, not stop the suite
            fail("G8", f"check could not finish: {str(e).splitlines()[0][:160]}")
    if run_for("S22"):
        try:
            thread_checks(out_dir)
        except Exception as e:  # a broken page must fail its rule, not stop the suite
            fail("S22", f"check could not finish: {str(e).splitlines()[0][:160]}")
    if run_for("S15", "S16"):
        try:
            kind_checks(out_dir)
        except Exception as e:  # a broken page must fail its rules, not stop the suite
            for r in ("S15", "S16"):
                fail(r, f"check could not finish: {str(e).splitlines()[0][:160]}")
    if run_for("M4"):
        try:
            slot_checks(out_dir)
        except Exception as e:  # a broken page must fail its rule, not stop the suite
            fail("M4", f"check could not finish: {str(e).splitlines()[0][:160]}")
    if run_for("X1", "X2", "X3", "X4", "E1", "E2", "E3", "S5", "S7", "S9", "S10", "S11", "S12", "S13", "S14", "S23", "T9"):
        try:
            source_checks(out_dir)
        except Exception as e:  # a broken tool must fail its rules, not stop the suite
            for r in ("X1", "X2", "X3", "X4", "E1", "E2", "E3", "S5", "S7", "S9", "S10", "S11", "S12", "S13", "S14", "S23", "T9"):
                fail(r, f"check could not finish: {str(e).splitlines()[0][:160]}")
    if run_for("S6", "S17"):
        try:
            setting_evidence_checks()
        except Exception as e:  # a broken file must fail its rules, not stop the suite
            for r in ("S6", "S17"):
                fail(r, f"check could not finish: {str(e).splitlines()[0][:160]}")
    if run_for("J1", "J2", "J3", "J4", "J5"):
        try:
            practice_checks(out_dir)
        except Exception as e:  # a broken page must fail its rules, not stop the suite
            for r in ("J1", "J2", "J3", "J4", "J5"):
                fail(r, f"check could not finish: {str(e).splitlines()[0][:160]}")
    if run_for("J9"):
        try:
            both_ways_checks()
        except Exception as e:  # a broken page must fail its rule, not stop the suite
            fail("J9", f"check could not finish: {str(e).splitlines()[0][:160]}")
    if run_for("F1", "F2"):
        try:
            picture_checks(out_dir)
        except Exception as e:  # a broken picture must fail its rules, not stop the suite
            for r in ("F1", "F2"):
                fail(r, f"check could not finish: {str(e).splitlines()[0][:160]}")
    if run_for("J7"):
        try:
            example_checks(out_dir)
        except Exception as e:  # a broken page must fail its rule, not stop the suite
            fail("J7", f"check could not finish: {str(e).splitlines()[0][:160]}")
    if run_for("X5"):
        try:
            preview_checks(out_dir)
        except Exception as e:  # a broken tool must fail its rule, not stop the suite
            fail("X5", f"check could not finish: {str(e).splitlines()[0][:160]}")
    fix_out = build_fixture() if run_for("M1", "M2", "M3", "R3", "R7", "A13", "A1", "R10") else None
    srv = Server(out_dir)
    fix = Server(fix_out) if fix_out else None
    try:
        page_checks(srv.base, out_dir, tokens, args.update_baseline, fix.base if fix else None)
    finally:
        srv.close()
        if fix:
            fix.close()
    sys.exit(1 if report() else 0)


if __name__ == "__main__":
    main()
