# Keep the margin-note slots in step with the units (spec M4).
# Usage, from the repo root after a build: python3 tools-pm/margin-slots.py public
#
# Reads the single document (public/pm/all/index.html), lists every part of every unit that carries a slot,
# and writes data/pm/margin/<unit>.yaml with one empty slot per part, in reading order. Notes already written
# are kept. A note whose part no longer exists is kept at the foot of its file under a warning, and the check
# suite fails until it is moved or deleted, so a renamed part never loses a note silently.
# Needs PyYAML and beautifulsoup4.
import json, os, sys
import yaml
from bs4 import BeautifulSoup

site = sys.argv[1] if len(sys.argv) > 1 else "public"
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out_dir = os.path.join(root, "data", "pm", "margin")
os.makedirs(out_dir, exist_ok=True)
soup = BeautifulSoup(open(os.path.join(site, "pm", "all", "index.html"), encoding="utf-8").read(), "html.parser")

HEAD = """# Margin notes for {title}.
# One slot per part of the page, in reading order. Write a note between the quotes; leave "" for none.
# On a wide screen, and in a module's print, a note shows in your hand in the margin beside its part. On a phone it
# sits under the part's heading, typeset; in print on Start, a card or the glossary it sits there in your hand.
# Wherever it sits in the text, "Sidenote:" goes above it, and a screen reader always reads that word first.
# A note beside a source on the full path may run on past it. Markdown works for **bold** and [a link](https://example.org).
# To put a note beside one paragraph of a part, give the slot a list, and name the paragraph by a few of its words:
#   why-this-matters:
#     - beside: "Two versions of the job"
#       note: "Your note."
# It sits level with the top of that paragraph; add  at: foot  to sit it level with the paragraph's foot.
# Keep the slot names as they are. After a unit changes, run tools-pm/margin-slots.py to add new slots;
# it keeps every note already written.
"""
NAMES = {"top": "Beside the title", "intro": "The opening paragraphs", "question": "One question to carry"}


def label(el, slot):
    if slot in NAMES:
        return NAMES[slot]
    if el.name in ("h1", "h2", "h3"):
        h = el
    else:
        h = el.find(["h2", "h3", "dt"])
    text = " ".join(h.get_text().split()) if h else slot
    if slot.startswith("step-"):
        n = len(el.find_previous_siblings("li")) + 1
        return f"Short path, step {n}: {text}"
    if slot.startswith("deeper-"):
        return f"Full path: {text}"
    return text


def quote(s):
    return json.dumps(s, ensure_ascii=False)


def entry(slot, v):
    """A slot as YAML: one note in quotes, or a list of notes, each with the paragraph it sits beside."""
    if not isinstance(v, list):
        return f"{slot}: {quote(v or '')}"
    lines = [f"{slot}:"]
    for n in v:
        keys = [k for k in ("beside", "at", "note") if k in n] + [k for k in n if k not in ("beside", "at", "note")]
        for i, k in enumerate(keys):
            lines.append(f"  {'- ' if i == 0 else '  '}{k}: {quote(n[k])}")
    return "\n".join(lines)


for art in soup.select("main article.unit"):
    unit = art["data-unit"]
    title = " ".join(art.find("h1").get_text(" ", strip=True).split())
    kind = [c for c in art["class"] if c != "unit"][0]
    if kind == "module":
        title = f"{art.select_one('.kicker .tag').get_text(strip=True)}, {title}"
    elif kind == "card":
        title = f"the concept card {title}"
    elif kind == "closing":
        title = f"the closing unit, {title}"
    slots = [(el["data-slot"], label(el, el["data-slot"])) for el in art.select("[data-slot]")]
    path = os.path.join(out_dir, f"{unit}.yaml")
    old = (yaml.safe_load(open(path, encoding="utf-8")) or {}) if os.path.exists(path) else {}
    lines = [HEAD.format(title=title)]
    for slot, name in slots:
        lines.append(f"# {name}\n{entry(slot, old.get(slot))}\n")
    lost = [(k, v) for k, v in old.items() if v and k not in dict(slots)]
    if lost:
        lines.append("# These parts are no longer on the page. Move each note to its new slot above, then delete its line here.")
        for k, v in lost:
            lines.append(entry(k, v))
            print(f"{unit}: the note in slot {k} has no part to sit beside any more; it is kept at the foot of {os.path.relpath(path, root)}")
    open(path, "w", encoding="utf-8").write("\n".join(lines).rstrip("\n") + "\n")
    print(f"{os.path.relpath(path, root)}: {len(slots)} slots")
