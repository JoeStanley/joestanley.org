#!/usr/bin/env python3
"""The working doc's tabs, made from the repository (spec X1 to X3).

The owner reviews the syllabus in one working doc with a tab for each unit. The repository is the source and the
doc mirrors it. This tool writes each tab as Markdown, so a session can put it in the doc, and keeps the record
of what was last put there.

    python3 tools-pm/source-doc.py public out/         write one .md per tab into out/, with out/tabs.json
    python3 tools-pm/source-doc.py public --check      exit 1 if a tab differs from the record (spec X3)
    python3 tools-pm/source-doc.py public --record     after the doc is synced: record the tabs as they are now
        (add Start=12 "Module 2=40" to note the doc's revision of a tab after you wrote it)
    python3 tools-pm/source-doc.py public --compare exported/   compare the doc's own Markdown export, tab by tab

"public" is a built site (hugo -d public). A built unit's tab is made from the built page, so it holds the words a
reader meets, template wording included. A draft's tab is its file in drafts/pm/, under the title, state and
question the map gives it. A voice slot (spec X4) shows its interim words in place, as the page does, and then its
own block: the brief and the owner's old words. The last tab, "Your voice pass", lists every open slot and every
word of his that moved (data/pm/voice-slots.yaml). Needs PyYAML and beautifulsoup4.
"""
import copy, datetime, hashlib, json, os, re, sys

import yaml
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCK = os.path.join(ROOT, "tools-pm", "source-doc.lock.json")
DRAFTS = os.path.join(ROOT, "drafts", "pm")
QUOTES = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', " ": " ", "…": "..."})


def clean(s):
    return re.sub(r"\s+", " ", s.translate(QUOTES))


# ---------- voice slots (spec X4) ----------
VOICE_TAB = "Your voice pass"
SLOT_HEAD = "> **Voice slot, waiting for your pass:**"
PENDING = []   # slots met in the text since the last block was written, so each one's block follows its paragraph


def voice():
    v = yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "voice-slots.yaml"), encoding="utf-8")) or {}
    return {"slots": v.get("slots") or [], "moved": v.get("moved") or []}


def slot_block(sid):
    """A slot's own block in its tab: what the passage must do, his words before, what the site shows for now."""
    s = next((x for x in voice()["slots"] if x.get("id") == sid), {})
    lines = [f"{SLOT_HEAD} `{sid}`", f"**What it must do:** {clean(s.get('brief') or '').strip()}"]
    if s.get("old"):
        lines.append(f"**Your words before:** {clean(s['old']).strip()}")
    lines.append(f"**For now the site says:** {clean(s.get('interim') or '').strip() or 'nothing, inside its sentence'}")
    return "\n>\n".join(l if i == 0 else "> " + l for i, l in enumerate(lines))


def flush():
    """The blocks of the slots met since the last call, in the order they were met."""
    out = [slot_block(sid) for sid in PENDING]
    PENDING.clear()
    return out


def strip_slots(md):
    """A tab without its slots' blocks: what X2 compares with the page."""
    return re.sub(r"(?m)^" + re.escape(SLOT_HEAD) + r".*(?:\n>.*)*", "", md)


# ---------- a built page's HTML, as Markdown ----------
def inline(el, strip=True):
    """The words inside an element, with emphasis, links and line edits kept."""
    out = []
    for c in el.children:
        if isinstance(c, NavigableString):
            out.append(clean(str(c)))
            continue
        cls = c.get("class") or []
        if c.name in ("script", "style", "svg") or "note" in cls or "note-label" in cls:
            continue   # a note goes in its own line; its label, "Sidenote:", is the page's, not the owner's words
        if c.get("data-voice"):   # a voice slot (spec X4): its interim words here, its block after the paragraph
            PENDING.append(c["data-voice"])
        if "sr" in cls:   # screen-reader words: keep the ones that finish a label, drop the rest
            t = clean(c.get_text())
            out.append(t if t.strip() in (":", ".") else "")
            continue
        if "edit" in cls:   # a line edit in the owner's hand (spec H2): the old word, then the new
            out.append(f"~~{inline(c.find('del'))}~~ *{inline(c.find('ins'))}*")
            continue
        t = inline(c, strip=False)
        if not t.strip():
            out.append(t)
        elif c.name in ("strong", "b"):
            out.append(f"**{t.strip()}**")
        elif c.name in ("em", "i", "cite"):
            out.append(f"*{t.strip()}*")
        elif c.name in ("del", "s"):
            out.append(f"~~{t.strip()}~~")
        elif c.name == "a" and "term" not in cls and (c.get("href") or "").startswith("http"):
            out.append(f"[{t.strip()}]({c['href']})")
        elif c.name == "br":
            out.append(" ")
        else:
            out.append(t)
    s = re.sub(r" +", " ", "".join(out))
    return s.strip() if strip else s


def note_of(el):
    """The owner's margin note that sits in this element, if he has written one."""
    n = el.find("aside", class_="note", recursive=False)
    return [f"*Margin note: {inline(n)}*"] if n else []


def blocks(el):
    """Block content (a page's prose) as Markdown paragraphs."""
    out = []
    for c in el.children:
        if isinstance(c, NavigableString):
            if clean(str(c)).strip():
                out.append(clean(str(c)).strip())
            continue
        cls = c.get("class") or []
        if c.name in ("script", "style", "svg") or "print-only" in cls:
            continue
        if c.get("data-voice"):   # a voice slot as a paragraph of its own (spec X4); its block follows it
            PENDING.append(c["data-voice"])
        if c.name in ("h2", "h3", "h4"):
            out.append("#" * int(c.name[1]) + " " + inline(c))
        elif c.name == "span" and c.get("data-voice"):
            out.append(inline(c))
        elif c.name == "p":
            out.append(inline(c))
        elif c.name == "aside" and "note" in cls:   # a note beside a paragraph (spec M1), after it
            out.append(f"*Margin note: {inline(c)}*")
        elif c.name in ("ul", "ol"):
            out.append(listing(c))
        elif c.name == "blockquote":
            out.append("\n>\n".join("> " + b.replace("\n", "\n> ") for b in blocks(c)))
        elif c.name == "table":
            rows = [[inline(x) for x in tr.find_all(["th", "td"])] for tr in c.find_all("tr")]
            out.append("\n".join(["| " + " | ".join(rows[0]) + " |", "| " + " | ".join("---" for _ in rows[0]) + " |"]
                                 + ["| " + " | ".join(r) + " |" for r in rows[1:]]))
        elif c.name == "aside" and "note" in cls:
            out.append(f"*Margin note: {inline(c)}*")
        elif c.name == "details" and "recall" in cls:
            out.append(inline(c.find("summary")))
            out.append("**Answer:** " + inline(c.find(class_="answer")))
        elif c.name == "hr":
            out.append("---")
        else:
            out.extend(blocks(c))
        out += flush()
    return [b for b in out if b]


def listing(el, depth=0):
    lines = []
    for i, li in enumerate(el.find_all("li", recursive=False), 1):
        mark = f"{i}." if el.name == "ol" else "-"
        own = BeautifulSoup(str(li), "html.parser").find("li")
        subs = [x.extract() for x in own.find_all(["ul", "ol"], recursive=False)]
        lines.append("  " * depth + f"{mark} {inline(own)}")
        for s in subs:
            lines.append(listing(s, depth + 1))
    return "\n".join(lines)


def reasons(el):
    """A source's folded reasons: Why trust it, What you'll get."""
    out = []
    dl = el.find("dl", class_="notes")
    if dl:
        for d in dl.find_all("div", recursive=False):
            out.append(f"**{inline(d.find('dt'))}:** {inline(d.find('dd'))}")
    return out


def look(el):
    p = el.find("p", class_="look")
    if not p:
        return []
    label = p.find(class_="sr")
    return [f"**{clean(label.get_text()).strip().rstrip(':')}:** {inline(p)}"] if label else [inline(p)]


def indent(paras, pad="   "):
    return "\n\n".join(pad + p.replace("\n", "\n" + pad) for p in paras)


def start_tab(art):
    out = ["# " + inline(art.find("h1"))] + note_of(art.find(class_="unit-head"))
    out += blocks(art.select_one(".unit-body > .prose"))
    wrap = art.find("section", class_="modules-wrap")
    out.append("## " + inline(wrap.find("h2")))
    out += note_of(wrap) + [inline(p) for p in wrap.find_all("p", class_="hint", recursive=False)]
    items = []
    for li in wrap.select("ol.modules > li"):
        num = clean(li.find(class_="mod-num").get_text()).strip()
        h3 = li.find("h3")
        for sr in h3.find_all(class_="sr"):
            sr.extract()
        items.append(f"- **{num} {inline(h3)}.** {inline(li.find(class_='mod-question'))} *{inline(li.find(class_='mod-status'))}.*")
    out.append("\n".join(items))
    return out


def game(sec):
    """A game (spec J5): its rules, then the words of its live part, its recorded run and its takeaway."""
    out = ["## " + inline(sec.find("h2"))] + note_of(sec)
    for c in sec.find_all(["p", "table", "ul"], recursive=False):
        wrap = BeautifulSoup("<div></div>", "html.parser").div
        wrap.append(copy.copy(c))
        out += blocks(wrap)
    live = sec.find(class_="game-live")
    if live:
        out.append("*On the site the playable game sits here. Its words:*")
        choices = " / ".join(clean(l.get_text()).strip() for l in live.select("fieldset label"))
        out.append(f"{inline(live.find('legend'))} {choices}.")
        labels = live.select(".setups-label")
        tests = live.select("[data-test]")
        picks = live.select("[data-pick]")
        data = json.loads(live.find("script", attrs={"data-game-setups": True}).string)
        if tests:   # the waiting game: the reader picks an estimate to test while the team builds
            out.append(f"{inline(labels[0])} " + " / ".join(inline(b) for b in tests) + ".")
            said = []
            for j in data["jobs"]:
                for r in ([j["report"]] if j.get("report") else [o["report"] for o in j.get("outcomes", [])]):
                    said.append(clean(r).replace("{value}", "*its value*"))
            out.append(f"*A test's answer, at the end of week {data['test_weeks']}:* " + " / ".join(said))
        if picks:   # the waiting game: the reader puts the jobs in any order, picking the next when it falls due
            out.append(f"{inline(labels[1 if tests else 0])} " + " / ".join(inline(b) for b in picks) + ".")
        out.append(f"{inline(live.find('button', attrs={'data-play': True}))}. {inline(labels[-1])}")
        setups = data.get("setups") or data.get("rules") or data
        items = []
        for k in [b["data-setup"] for b in live.select("button.setup[data-setup]")]:
            note = f" {clean(setups[k]['note'])}" if setups[k].get("note") else ""
            items.append(f"- **{clean(setups[k]['label'])}.**{note} *After a run:* {clean(setups[k]['after'])}")
        out.append("\n".join(items))
    for part in sec.select(".example, .takeaway"):
        out += blocks(part)
    return out


def module_tab(art, state):
    head = art.find(class_="unit-head")
    out = [f"# {inline(head.select_one('.kicker .tag'))}: {inline(head.find('h1'))}", f"*{state}*"] + note_of(head)
    out.append("**The question:** " + inline(head.find(class_="question")))
    out.append(inline(head.find(class_="meta")))
    one = head.find(class_="one-thing")
    if one:
        out.append(f"**{inline(one.find(class_='one-thing-label'))}** {inline(one.find('mark'))}")
    body = art.find(class_="unit-body")
    for sec in body.find_all("section", recursive=False):
        cls = sec.get("class") or []
        if "print-only" in cls:
            continue
        if "path" in cls:
            out.append("## " + inline(sec.find("h2")))
            out += note_of(sec)
            steps = []
            for i, li in enumerate(sec.select("ol.steps > li"), 1):
                b = li.find(class_="step-body")
                paras = [inline(b.find(class_="meta-line"))]
                links = b.find("ul", class_="step-links")
                if links:
                    paras[0] += "\n" + listing(links)
                paras += look(b) + reasons(b) + note_of(li) + flush()
                steps.append(f"{i}. **{inline(b.find('h3'))}**\n\n" + indent(paras))
            out.append("\n".join(steps))
        elif "game" in cls:
            out += game(sec)
        elif "deeper" in cls:
            out.append("## " + inline(sec.find("h2")))
            out += note_of(sec) + [inline(sec.find(class_="deeper-hint"))]
            items = []
            for li in sec.select("ul.deeper-list > li"):
                paras = [inline(li.find(class_="meta-line"))]
                paras += [inline(p) for p in li.find_all("p", class_="deeper-note")] + look(li) + reasons(li) + note_of(li) + flush()
                items.append(f"- **{inline(li.find('h3'))}**\n\n" + indent(paras, "  "))
            out.append("\n\n".join(items))
        else:
            out += blocks(sec)
    return out


def card_tab(art):
    head = art.find(class_="unit-head")
    out = ["---", "# " + inline(head.find("h1")), f"*{inline(head.find(class_='kicker'))}.*"] + note_of(head)
    body = art.find(class_="unit-body")
    fig = body.find("figure")
    if fig:
        cap = fig.find("figcaption")
        quote = fig.find("blockquote")
        if quote:   # a sentence in its author's words in the picture's place (spec S16), then its credit
            out += note_of(fig) + [f"> {inline(quote.find('p'))}"] + ([f"*{inline(cap)}*"] if cap else [])
        else:
            out += note_of(fig) + ([f"*Picture: {inline(cap)}*"] if cap else [])
    out += blocks(body.find(class_="card-body"))
    for n in body.find_all("aside", class_="note", recursive=False):
        out.append(f"*Margin note: {inline(n)}*")
    carry = body.find(class_="carry")
    if carry:
        out.append(f"**{inline(carry.find(class_='carry-label'))}** {inline(carry.find('mark'))}")
    deep = body.find("section", class_="card-deeper")
    if deep:
        out.append("## " + inline(deep.find("h2")))
        out += note_of(deep) + [f"**{inline(deep.find('h3'))}**", inline(deep.find(class_="meta-line"))] + look(deep) + reasons(deep)
    return out


def glossary_tab(art):
    out = ["# " + inline(art.find("h1"))] + note_of(art.find(class_="unit-head")) + blocks(art.select_one(".unit-body > .prose"))
    items = []
    for d in art.select("dl.gloss-list > div"):
        dd = d.find("dd")
        note = dd.find("aside", class_="note")
        text = inline(dd)
        items.append(f"- **{inline(d.find('dt'))}:** {text}" + (f" *Margin note: {inline(note)}*" if note else ""))
    out.append("\n".join(items))
    return out


# ---------- a draft file, as its tab ----------
VOICE_CODE = re.compile(r'\{\{<\s*pm/voice\s+"([^"]+)"(?:\s+"paragraph")?\s*>\}\}')


def draft_slots(md):
    """A draft's voice slots, as a built page's: the interim words in place, then each slot's block."""
    slots = {x.get("id"): x for x in voice()["slots"]}
    out = []
    for para in md.split("\n\n"):
        ids = VOICE_CODE.findall(para)
        out.append(VOICE_CODE.sub(lambda m_: clean(slots.get(m_.group(1), {}).get("interim") or "").strip(), para))
        out += [slot_block(i) for i in ids]
    return "\n\n".join(out)


def draft_tab(m):
    body = draft_slots(open(os.path.join(DRAFTS, m["draft"] + ".md"), encoding="utf-8").read().strip())
    head = [f"# Module {m['num']}: {m['title']}", f"*{m['state']}*", f"**The question:** {m['question']}"]
    parts = re.split(r"(?m)^(?=# )", body)
    out = ["\n\n".join(head) + "\n\n" + parts[0].strip()]
    for card in parts[1:]:
        title, _, rest = card.partition("\n")
        out.append(f"---\n\n{title.strip()}\n\n*Concept card for Module {m['num']}, {m['title']}.*\n\n{rest.strip()}")
    return "\n\n".join(out)


def about_tab(mods, synced):
    rows = []
    for m in mods:
        src = f"`content/pm/{m['page']}.md`, its cards in `content/pm/cards/`" if m.get("page") else f"`drafts/pm/{m['draft']}.md`"
        state = "Built, and on the site." if m.get("page") else m["state"]
        rows.append(f"| {m['num']} {m['title']} | {state} | {src} |")
    return "\n\n".join([
        "# On Product Judgment: Working Source",
        f"Last put here from the repository on {synced}.",
        "This doc mirrors the syllabus as it stands in the joestanley.org repository. Each tab is one unit: the Start page, each module with its concept cards, and the glossary. What you read here is what the repository holds, word for word.",
        "Comment on any line, or edit it. A Claude Code session carries your comments and edits into the repository, then puts the result back here, so the two stay the same. The checks in the repository fail if a tab falls out of step.",
        "| Tab | Where it stands | Its source in the repository |\n| --- | --- | --- |\n| Start | Built, and on the site. | `content/pm/_index.md`, with the list of modules from `data/pm/modules.yaml` |\n"
        + "\n".join(rows) + "\n| Glossary | Built, and on the site. | `data/pm/glossary.yaml` |",
        f"The last tab, {VOICE_TAB}, lists every passage that waits for your voice and every word of yours a session cut, moved or changed, so your final pass starts from one list. A passage that waits shows a block in its own tab too, where you read it.",
        "The pictures on the cards are not shown here, only their captions. The Notes tabs at the end are working notes from before 20 November 2026, kept as history. Decisions for you now wait on the [Decisions page](https://claude.ai/artifact/QGLpeYcbz14tPBAPiQSYGq), and what comes next is in `PLAN.md` in the private pm-sources repository.",
    ])


def voice_tab():
    """The owner's voice pass in one list (spec X4): every open slot, then every word of his that moved."""
    v = voice()
    out = [f"# {VOICE_TAB}",
           "Everything that waits for you in your final voice pass, in one place. A voice slot is a passage that needs your voice: the site shows its interim words for now, and its tab shows a block with what the passage must do. Below them, every passage of your words a session cut, moved or changed since you opened your words to agents on 22 November 2026, with where it went and why. Nothing here is written as you.",
           "## Open voice slots"]
    for s_ in v["slots"]:
        out += [f"**In {s_.get('unit')}.**", slot_block(s_.get("id"))]
    if not v["slots"]:
        out.append("None yet.")
    out.append("## Your words that moved")
    if not v["moved"]:
        out.append("None yet.")
    for e in v["moved"]:
        out.append(f"**{str(e.get('what', '')).capitalize()}, {e.get('when')}.** From {e.get('from')}. To {e.get('to')}. {e.get('why')}")
        out.append("> " + clean(e.get("words") or "").strip())
    return "\n\n".join(out)


# ---------- all tabs ----------
def tabs(site, synced=None):
    soup = BeautifulSoup(open(os.path.join(site, "pm", "all", "index.html"), encoding="utf-8").read(), "html.parser")
    arts = {a["data-unit"]: a for a in soup.select("main article.unit")}
    mods = yaml.safe_load(open(os.path.join(ROOT, "data", "pm", "modules.yaml"), encoding="utf-8"))
    PENDING.clear()
    out = [("About", about_tab(mods, synced or today())), ("Start", "\n\n".join(start_tab(arts["start"]) + flush()))]
    for m in mods:
        name = f"{m['num']} {m['title']}"
        if m.get("page"):
            parts = module_tab(arts[m["page"]], "Built, and on the site.") + flush()
            for a in arts.values():
                if "card" in a["class"] and a.get("data-module") == m["id"]:
                    parts += card_tab(a) + flush()
            out.append((name, "\n\n".join(parts)))
        else:
            out.append((name, draft_tab(m)))
    out.append(("Glossary", "\n\n".join(glossary_tab(arts["glossary"]) + flush())))
    out.append((VOICE_TAB, voice_tab()))
    return [(n, re.sub(r"\n{3,}", "\n\n", t.translate(QUOTES)).strip() + "\n") for n, t in out]


def today():
    d = datetime.date.today()
    return f"{d.day} {d.strftime('%B %Y')}"


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") + ".md"


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def words(md):
    """A tab's words alone, for comparing with the doc's own export: markup, link addresses and case set aside."""
    md = re.sub(r"\]\([^)]*\)", "]", md.translate(QUOTES))
    return re.findall(r"[a-z0-9']+", md.lower())


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    lock = json.load(open(LOCK, encoding="utf-8")) if os.path.exists(LOCK) else {"doc": "", "synced": "", "tabs": []}
    # The About tab says when the doc was last synced: today when a sync is being made, the recorded day when checking.
    made = tabs(args[0], lock["synced"] if "--check" in args else None)
    old = {t["name"]: t for t in lock["tabs"]}
    if "--check" in args:
        bad = [n for n, t in made if old.get(n, {}).get("sha256") != sha(t)] + [n for n in old if n not in dict(made)]
        for n in bad:
            print(f"out of step with the working doc: {n}")
        sys.exit(1 if bad else 0)
    if "--record" in args:
        revs = dict(a.split("=", 1) for a in args[args.index("--record") + 1:] if "=" in a)
        lock["synced"] = today()
        lock["tabs"] = []
        for n, t in made:
            e = {"name": n, "file": slug(n), "sha256": sha(t)}
            for k in ("doc_tab", "doc_node", "rev"):
                if k in old.get(n, {}):
                    e[k] = old[n][k]
            if n in revs:
                e["rev"] = int(revs[n])
            lock["tabs"].append(e)
        json.dump(lock, open(LOCK, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        open(LOCK, "a", encoding="utf-8").write("\n")
        print(f"recorded {len(made)} tabs in {os.path.relpath(LOCK, ROOT)}")
        return
    if "--compare" in args:
        d = args[args.index("--compare") + 1]
        diff = 0
        for n, t in made:
            f = os.path.join(d, n + ".md")
            if not os.path.exists(f):
                print(f"{n}: no export found at {f}"); diff += 1; continue
            a, b = words(t), words(open(f, encoding="utf-8").read())
            if a == b:
                print(f"{n}: same words ({len(a)})")
            else:
                i = next((k for k, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
                print(f"{n}: DIFFERS at word {i}: repository \"{' '.join(a[max(0, i - 6):i + 8])}\" / doc \"{' '.join(b[max(0, i - 6):i + 8])}\""); diff += 1
        sys.exit(1 if diff else 0)
    out = args[1]
    os.makedirs(out, exist_ok=True)
    index = []
    for n, t in made:
        open(os.path.join(out, slug(n)), "w", encoding="utf-8").write(t)
        index.append({"name": n, "file": slug(n), "sha256": sha(t), "in_step": old.get(n, {}).get("sha256") == sha(t)})
    json.dump(index, open(os.path.join(out, "tabs.json"), "w", encoding="utf-8"), indent=1)
    for e in index:
        print(f"{'  same' if e['in_step'] else 'CHANGED'}  {e['file']}")


if __name__ == "__main__":
    main()
