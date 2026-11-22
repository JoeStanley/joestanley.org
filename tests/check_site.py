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
import argparse, functools, glob, http.server, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading
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
           ("/pm/design-for-change/", ["/pm/cards/coupling/", "/pm/cards/access-patterns/"]),
           ("/pm/change-safely/", ["/pm/cards/error-budgets/"]),
           ("/pm/weigh-the-evidence/", ["/pm/cards/law-of-small-numbers/"]),
           ("/pm/decide-and-set-direction/", ["/pm/cards/agency-and-coherence/"]),
           ("/pm/answer-for-what-you-build/", ["/pm/cards/many-hands/"]),
           ("/pm/notice-when-you-are-wrong/", ["/pm/cards/double-loop-learning/"]),
           ("/pm/bring-people-with-you/", ["/pm/cards/trust-equation/"])]
UNIT_PAGES = [p for m, cards in MODULES for p in [m] + cards]
PAGES = ["/", "/page/readme/", "/writing/", "/games/", "/pm/"] + UNIT_PAGES + ["/pm/glossary/", "/pm/all/"]
WIDTHS = [320, 390, 768, 1024, 1280, 1920]
# P1: the most pages each kind of unit may print on, and what the rebuilt units print on in all.
# PRINT_PAGES is a record kept with the spec: a change in the count is noted in the report, not failed.
UNIT_SHARE = {"start": 2, "module": 3, "card": 1, "glossary": 3}
DEEPER_PAGES = 2   # the pages a module's full path, answers and sources' reasons may run onto past its three
MODULE_GRACE = 1   # until launch, a module may run one page past either limit: noted, not failed (the owner, 22 November 2026)
GLOSSARY_GRACE = None   # until launch, the glossary may run past its three pages: noted, not failed (the owner, 22 November 2026)
PRINT_PAGES = 73   # a record: the check notes a change in the count, and does not fail on it
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
    sample, so R10 always meets a note there that runs past the heading. Returns the built output directory."""
    tmp = tempfile.mkdtemp(prefix="fixture-")
    src = os.path.join(tmp, "src"); out = os.path.join(tmp, "out")
    shutil.copytree(ROOT, src, ignore=shutil.ignore_patterns(".git", "public", "node_modules", "baseline", "resources", "report.md"))
    for f in glob.glob(os.path.join(src, "data", "pm", "margin", "*.yaml")):
        data = yaml.safe_load(open(f, encoding="utf-8")) or {}
        filled = {k: (v if v else SAMPLE[1] if k == "go-deeper" else SAMPLE[i % len(SAMPLE)]) for i, k in enumerate(data) for v in [data[k]]}
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
# took the full path's Open and Close label, and where its heading ends and its first source starts.
JS_FULL_PATH = """() => { const sec = document.querySelector('.deeper'); if (!sec) return null;
  const d = sec.querySelector(':scope > details'); d.open = true;
  const sum = d.querySelector(':scope > summary'), ul = sec.querySelector('.deeper-list');
  const cs = getComputedStyle(sec), r = sec.getBoundingClientRect();
  const stray = [...d.querySelectorAll('summary')].filter(x => x !== sum).filter(x => /Open|Close/.test(getComputedStyle(x, '::after').content));
  sum.scrollIntoView({block: 'center'}); const s = sum.getBoundingClientRect(), first = ul.firstElementChild.getBoundingClientRect();
  return {inner: r.width - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight), ul: ul.getBoundingClientRect().width,
          lis: [...ul.children].map(li => li.getBoundingClientRect().width), stray: stray.length,
          gap: first.top - s.bottom, left: r.left, width: r.width, bottom: s.bottom}; }"""


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
                clip = {"x": f["left"], "y": f["bottom"], "width": f["width"], "height": 40}
                shown = pg.screenshot(clip=clip)
                pg.add_style_tag(content=".deeper > details > summary::after { visibility: hidden !important; }")
                hidden = pg.screenshot(clip=clip)
                if shown != hidden:
                    fail("R10", f"{where}: the Open and Close label draws below its heading, over the first source")
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
            if step.get("kind") not in ("card", "play") and not ((step.get("trust") or before) and step.get("only")):
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

    # A8: the dice game in words (reduced motion, so a run finishes at once)
    try:
        c = ctx(viewport={"width": 1280, "height": 900}, reduced_motion="reduce"); pg = c.new_page(); pg.set_default_timeout(8000); pg.goto(base + "/pm/find-the-constraint/")
        attrs = pg.evaluate("""() => ({key: document.querySelector('.board-key') ? document.querySelector('.board-key').closest('[aria-hidden=true]') !== null : true,
            note: (() => { const n = document.querySelector('[data-setup-note]'); return !!n && (n.getAttribute('aria-live') === 'polite' || n.getAttribute('role') === 'status' || !!n.closest('[aria-live=polite], [role=status]')); })()})""")
        if not attrs["key"]:
            fail("A8", "the key to the board is read by screen readers, but the board is hidden from them")
        if not attrs["note"]:
            fail("A8", "a change of setup is not announced")
        for setup in ("equal", "slow3"):
            pg.click(f"[data-setup={setup}]"); pg.click("[data-play]"); pg.wait_for_timeout(100)
            res = pg.evaluate("""() => ({text: document.querySelector('[data-result]').textContent,
                board: [...document.querySelectorAll('.st')].slice(1).map(st => +(st.querySelector('.pile-n').textContent || 0))})""")
            said = {int(st): int(n) for n, st in re.findall(r"(\d+) at station (\d)", res["text"])}
            for i, n in enumerate(res["board"], start=2):
                if said.get(i) != n:
                    fail("A8", f"setup {setup}: the result says {said.get(i)} waiting at station {i}; the board shows {n}")
        c.close()
    except Exception as e:  # a broken page must fail its rule, not stop the suite
        fail("A8", f"check could not finish: {str(e).splitlines()[0][:160]}")

    # A9: focus is never dropped
    try:
        c = ctx(viewport={"width": 1280, "height": 900}); pg = c.new_page(); pg.set_default_timeout(8000); pg.goto(base + "/pm/find-the-constraint/")
        pg.focus("[data-play]"); pg.keyboard.press("Enter"); pg.wait_for_timeout(500)
        if not pg.evaluate("document.activeElement.matches('[data-play]')"):
            fail("A9", "pressing Play drops focus while the game runs")
        pg.wait_for_timeout(4500)
        if not pg.evaluate("document.activeElement.matches('[data-play]')"):
            fail("A9", "focus is not on Play when the game finishes")
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
                pg.click("[data-play]"); pg.wait_for_timeout(100)               # the result and takeaway show after a run
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
    for path in glob.glob(os.path.join(ROOT, "content", "pm", "**", "*.md"), recursive=True):
        m = re.match(r"---\n(.*?)\n---", open(path, encoding="utf-8").read(), re.S)
        fm = yaml.safe_load(m.group(1)) if m else {}
        deeper = fm.get("deeper")
        for s_ in (fm.get("steps") or []) + (deeper if isinstance(deeper, list) else [deeper] if deeper else []):
            for key in ("trust", "only"):
                if s_.get(key):
                    probe = " ".join(_plain(s_[key]).replace("\u2019", "'").split()[:6])
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
                kind = "start" if top.title.startswith("Start:") else "module" if top.title.startswith("Module ") else "glossary"
                deeper = next((first_page(k) for k in top.children if k.title.startswith("Go deeper: the full path")), None)
                units.append((first_page(top), kind, top.title, deeper))
                units += [(first_page(k), "card", k.title, None) for k in top.children if k.title.startswith("Card: ")]
    if any(u[0] is None for u in units):
        fail("P1", "a unit's bookmark does not land on a page, so its pages cannot be counted"); return
    units.sort(key=lambda u: u[0])
    for (pg, kind, title, deeper), nxt in zip(units, units[1:] + [(n_pages, "", "", None)]):
        n = nxt[0] - pg
        # a module's full path prints outside its three pages: it starts within them, and may take two more
        share = UNIT_SHARE[kind] + (DEEPER_PAGES if kind == "module" and deeper is not None else 0)
        grace = MODULE_GRACE if kind == "module" else 0   # the website first: a module's extra page is noted, not failed
        said = f"'{title}' prints on {n} pages; a {kind} gets {UNIT_SHARE[kind]}{f', and {DEEPER_PAGES} more for its full path' if share > UNIT_SHARE[kind] else ''}"
        if n < 1:
            fail("P1", f"'{title}' starts on PDF page {pg + 1}, which it shares with another unit")
        elif kind == "glossary" and GLOSSARY_GRACE is None and n > share:
            NOTE["P1"].append(said + ", and may run past them until the site goes live, so every term goes in")
        elif n > share + grace:
            fail("P1", said)
        elif n > share:
            NOTE["P1"].append(said + ", and may run one page over until the site goes live")
        if kind == "module" and deeper is not None and deeper - pg >= UNIT_SHARE["module"]:
            said = f"'{title}' starts its full path on its page {deeper - pg + 1}, so the module itself runs past its {UNIT_SHARE['module']} pages"
            if deeper - pg >= UNIT_SHARE["module"] + MODULE_GRACE:
                fail("P1", said)
            else:
                NOTE["P1"].append(said + ", which it may do by one page until the site goes live")


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
        for e_ in re.finditer(r"^\*\*[^*\n]*?\((\d+) minutes\)\.\*\*", text, re.M):
            times.append(("an exercise", int(e_.group(1))))
        for what, m in times:
            if not s14_on_mark(m):
                fail("S14", f"{where}: {what} takes {m} minutes, and rounds to {s14_round(m)}")
        if total is not None and times and s14_round(sum(m for _, m in times)) != total:
            fail("S14", f"{where}: the header says {total} minutes, and the steps and exercises add up to {sum(m for _, m in times)}, which rounds to {s14_round(sum(m for _, m in times))}")
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


def source_checks(out_dir):
    from bs4 import BeautifulSoup
    checked("X1", "X2", "X3", "X4", "E1", "E2", "E3", "S5", "S7", "S9", "S10", "S11", "S12", "S13", "S14", "T9")
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
    tab_of = {"start": "Start", "glossary": "Glossary"}
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
    own_words = yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "own-words.yaml"), encoding="utf-8")) or []
    for o in own_words:
        if o.get("unit") not in by_name:
            fail("E3", f"data/pm/own-words.yaml lists a sentence for {o.get('unit')}, which has no tab")
    retired = [l.strip().lower() for l in open(os.path.join(TESTS, "retired-settings.txt"), encoding="utf-8") if l.strip() and not l.startswith("#")]
    for name, text in tabs:
        if name in ("About", sd.VOICE_TAB):
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
        for sec in _sections(text, {"Why this matters", "Why a PM cares", "Why a PM should care"}):
            if not re.search(r"\byou(r|'re|'ll|'ve|'d)?\b", sec, re.I):
                fail("E1", f"{name}: a section that should speak to the reader never says \"you\": {sec.strip()[:50]}")
        # S10: every full path carries one story, its entry opening with its medium; a story says what
        # you'll get and carries no "Why trust it" (a documentary may). S11: a built module's full path
        # recommends five things at most, the story included.
        paths = _sections(text, {"Go deeper: the full path"})
        if name not in ("About",) and re.match(r"\d+ ", name) and not paths:
            fail("S10", f"{name} has no full path, so it carries no story")
        for sec in paths:
            stories, count, books = [], 0, 0
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
            if len(stories) > 1:
                fail("S10", f"{name}: the full path carries {len(stories)} stories, and one is the most: {'; '.join(stories)}")
            if not stories:
                fail("S10", f"{name}: the full path carries no story, and every full path carries one")
            if name in built_tabs and count > 5:
                fail("S11", f"{name}: the full path recommends {count} things, and five is the most")
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
                        bad = pg.evaluate("""() => [...document.querySelectorAll('a')].filter(a => !a.matches('.site-name, .site-nav a, .door-links a, .skip, .unit-nav a') && a.getBoundingClientRect().width && !getComputedStyle(a).textDecorationLine.includes('underline')).map(a => a.textContent.trim().slice(0, 30))""")
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
                        # R9: the menu on one line at phone width
                        tops = pg.evaluate("() => [...document.querySelectorAll('.site-nav[aria-label=Sections] a')].map(a => Math.round(a.getBoundingClientRect().top))")
                        if tops and max(tops) - min(tops) > 2:
                            fail("R9", f"{where}: the menu takes more than one line")
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
            pg.goto(base + "/pm/find-the-constraint/")
            v = pg.evaluate("""() => ({example: getComputedStyle(document.querySelector('.example')).display, takeaway: getComputedStyle(document.querySelector('.takeaway')).display,
                 live: getComputedStyle(document.querySelector('.game-live')).display, folded: [...document.querySelectorAll('.recall')].every(d => !d.open),
                 terms: [...document.querySelectorAll('.term')].map(t => t.tagName === 'A' ? t.getAttribute('href') : null)})""")
            if v["example"] == "none" or v["takeaway"] == "none":
                fail("D1", "without JavaScript the recorded run or takeaway is hidden")
            if v["live"] != "none":
                fail("D1", "without JavaScript the live game controls show")
            if not v["folded"]:
                fail("D1", "answers are not folded")
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
    if run_for("X1", "X2", "X3", "X4", "E1", "E2", "E3", "S5", "S7", "S9", "S10", "S11", "S12", "S13", "S14", "T9"):
        try:
            source_checks(out_dir)
        except Exception as e:  # a broken tool must fail its rules, not stop the suite
            for r in ("X1", "X2", "X3", "X4", "E1", "E2", "E3", "S5", "S7", "S9", "S10", "S11", "S12", "S13", "S14", "T9"):
                fail(r, f"check could not finish: {str(e).splitlines()[0][:160]}")
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
