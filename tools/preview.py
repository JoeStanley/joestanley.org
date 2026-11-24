#!/usr/bin/env python3
"""The preview: the whole built site as one private page on claude.ai, for the owner's notes (spec X5).

The owner walks every page as joestanley.org shows it, at phone and desktop width, and comments on any part. An
artifact's comment threads attach to its one page, so this tool puts every page of the site in one file: each page
a reader can reach from the front door, one at a time, chosen by the address's #name. Nothing in it is new to the
site. Each page's own words and markup are copied byte for byte, and only what must change to live in one file
does: each id takes its page's name in front (pm-find-the-constraint--main), links between pages and to a part of
a page go to that page's #name, the site's two stylesheets are switched page by page as the site switches them,
its fonts and photo are carried inside as data, its script runs once for every page, and the glossary's pop-ups,
which every syllabus page carries, are kept once. A copy of each dark-screen block follows a theme picked in
claude.ai as well as the system's, as the page contract asks; its values are the site's own.

    python3 tools/preview.py public out/preview.html   make the preview and list the pages it holds
    python3 tools/preview.py public --check            exit 1 if it can't be made, or differs from what was published
    python3 tools/preview.py public --record           after publishing it: record what was published
                                                       (add its address the first time: --record https://claude.ai/...)
    python3 tools/preview.py public --local out.html   the same page in a stand-in for claude.ai's frame, to open
                                                       in a browser here (the checks compare it with the site)

"public" is a built site (hugo -d public). The page is published with the Artifact tool, its address in
tools/preview.lock.json; CLAUDE.md, "The preview", says how. MIT licensed, as the site's code is.
"""
import base64, datetime, hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCK = os.path.join(ROOT, "tools", "preview.lock.json")
SITE_HOSTS = ("https://joestanley.org", "http://joestanley.org", "https://www.joestanley.org")
TITLE = "joestanley.org Preview"
# claude.ai keeps these #names for itself (the page contract), so no page or part of one may take them.
RESERVED = ("settings", "sidebar", "customize", "upgrade", "downloads")
SIZE_LIMIT = 16 * 1024 * 1024
IDREF_ATTRS = ("for", "headers", "list", "form", "aria-labelledby", "aria-describedby", "aria-controls", "aria-owns",
               "aria-activedescendant", "aria-details", "aria-errormessage", "aria-flowto", "popovertarget", "commandfor")
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif", ".svg": "image/svg+xml",
        ".webp": "image/webp", ".woff2": "font/woff2", ".woff": "font/woff", ".ico": "image/x-icon"}

TAG = re.compile(r"<([a-zA-Z][a-zA-Z0-9:-]*)((?:\s+[^\s=>/]+(?:\s*=\s*\"[^\"]*\")?)*)\s*(/?)>")
ATTR = re.compile(r"(\s+)([^\s=>/]+)(?:(\s*=\s*)\"([^\"]*)\")?")
# Raw text the tag rewriter must not touch: scripts (the games' data among them), styles and comments.
RAW = re.compile(r"(<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->)", re.S | re.I)
DIALOG = re.compile(r"<dialog\b[^>]*\bclass=\"gloss\"[^>]*>.*?</dialog>\s*", re.S)
SCRIPT_SRC = re.compile(r"<script\b[^>]*\bsrc=\"([^\"]*)\"[^>]*>\s*</script>\s*", re.S)


def key_of(path):
    """A page's #name, from its address: / is home, /pm/cards/coupling/ is pm-cards-coupling."""
    p = path.strip("/")
    return p.replace("/", "-") if p else "home"


def norm_path(p):
    """A link's path as the site serves it: /pm/glossary/ for /pm/glossary, /pm/glossary/ and /pm/glossary/index.html."""
    p = re.sub(r"index\.html$", "", p)
    if not p.endswith("/") and not os.path.splitext(p)[1]:
        p += "/"
    return p


def file_of(public, path):
    return os.path.join(public, path.lstrip("/"), "index.html") if path.endswith("/") else os.path.join(public, path.lstrip("/"))


def data_uri(public, path):
    f = os.path.join(public, path.lstrip("/"))
    mime = MIME.get(os.path.splitext(f)[1].lower())
    if not mime or not os.path.isfile(f):
        return None
    return f"data:{mime};base64," + base64.b64encode(open(f, "rb").read()).decode("ascii")


class Page:
    def __init__(self, public, path):
        self.path, self.key = path, key_of(path)
        html = open(file_of(public, path), encoding="utf-8").read()
        m = re.search(r"<title>(.*?)</title>", html, re.S)
        self.title = m.group(1).strip() if m else self.key
        m = re.search(r"<link rel=\"stylesheet\" href=\"([^\"]+)\">", html)
        self.css = m.group(1) if m else None
        m = re.search(r"<body([^>]*)>(.*)</body>", html, re.S)
        if not m:
            raise ValueError(f"{path} has no body")
        cm = re.search(r"\bclass=\"([^\"]*)\"", m.group(1))
        self.body_class = cm.group(1) if cm else ""
        body = m.group(2)
        self.scripts = SCRIPT_SRC.findall(body)
        body = SCRIPT_SRC.sub("", body)
        self.dialogs = DIALOG.findall(body)
        self.body = DIALOG.sub("", body)
        self.ids = set()
        for seg in RAW.split(self.body):
            if not RAW.fullmatch(seg):
                self.ids.update(re.findall(r"\sid=\"([^\"]*)\"", seg))
        self.links = []
        for seg in RAW.split(self.body):
            if not RAW.fullmatch(seg):
                self.links += re.findall(r"\shref=\"([^\"]*)\"", seg)


def internal(href):
    """The path and fragment of a link inside the site, or None for a link elsewhere (another site, mail, a phone)."""
    for h in SITE_HOSTS:
        if href == h or href.startswith(h + "/"):
            href = href[len(h):] or "/"
    if href.startswith("#"):
        return "", href[1:]
    if not href.startswith("/") or href.startswith("//"):
        return None
    path, _, frag = href.partition("#")
    return norm_path(path.split("?")[0]), frag


def gather(public):
    """Every page a reader can reach from the front door by following links, in the order a reader meets them."""
    pages, queue, seen, problems = {}, ["/"], {"/"}, []
    while queue:
        path = queue.pop(0)
        if not os.path.isfile(file_of(public, path)):
            continue
        pg = Page(public, path)
        pages[path] = pg
        for href in pg.links:
            got = internal(href)
            if not got or not got[0]:
                continue
            p = got[0]
            if p not in seen and os.path.isfile(file_of(public, p)) and p.endswith("/"):
                seen.add(p); queue.append(p)
    return pages, problems


class Rewriter:
    """Rewrites one page's tags: its ids take the page's name in front, and its links and pictures point inside."""

    def __init__(self, public, pages, key, problems, where):
        self.public, self.pages, self.key, self.problems, self.where = public, pages, key, problems, where
        self.by_key = {p.key: p for p in pages.values()}

    def pid(self, i):
        return f"{self.key}--{i}" if self.key else i

    def href(self, v):
        got = internal(v)
        if got is None:
            return v
        path, frag = got
        if not path:   # a part of this same page
            if not frag:
                return v
            if self.key is None:
                self.problems.append(f"{self.where}: a link to #{frag}, which only one page could hold")
                return v
            if frag not in self.by_key[self.key].ids:
                self.problems.append(f"{self.where}: a link to #{frag}, which nothing on the page carries")
            return "#" + self.pid(frag)
        if path not in self.pages:
            if data_uri(self.public, path.rstrip("/")):
                return data_uri(self.public, path.rstrip("/"))
            self.problems.append(f"{self.where}: a link to {path}, which the preview doesn't hold")
            return v
        tgt = self.pages[path]
        if not frag:
            return "#" + tgt.key
        if frag not in tgt.ids:
            self.problems.append(f"{self.where}: a link to {path}#{frag}, which nothing on that page carries")
        return f"#{tgt.key}--{frag}"

    def src(self, v):
        got = internal(v)
        if got is None or not v.startswith("/"):
            return v
        uri = data_uri(self.public, v.split("#")[0].split("?")[0])
        if not uri:
            self.problems.append(f"{self.where}: a picture or file at {v} the preview can't carry")
            return v
        return uri

    def tag(self, m):
        name, attrs, close = m.group(1), m.group(2), m.group(3)
        if not attrs:
            return m.group(0)

        def one(a):
            space, an, eq, val = a.group(1), a.group(2), a.group(3), a.group(4)
            if val is None:
                return a.group(0)
            low = an.lower()
            new = val
            if low == "id" and self.key is not None:
                new = self.pid(val)
            elif low in ("href", "xlink:href"):
                new = self.href(val)
            elif low in ("src", "poster"):
                new = self.src(val)
            elif low == "srcset":
                new = ", ".join(" ".join([self.src(part.split()[0])] + part.split()[1:]) for part in val.split(",") if part.strip())
            elif low in IDREF_ATTRS and self.key is not None:
                new = " ".join(i if i.startswith("term-") else self.pid(i) for i in val.split())
            if "url(#" in new and self.key is not None:
                new = re.sub(r"url\(#([^)]+)\)", lambda u: f"url(#{self.pid(u.group(1))})", new)
            return f"{space}{an}{eq}\"{new}\""

        return f"<{name}{ATTR.sub(one, attrs)}{' /' if close else ''}>" if close else f"<{name}{ATTR.sub(one, attrs)}>"

    def run(self, html):
        out = []
        for seg in RAW.split(html):
            out.append(seg if RAW.fullmatch(seg) else TAG.sub(self.tag, seg))
        return "".join(out)


# ---------- the stylesheets ----------
def _block_end(css, i):
    """The index just past the brace that closes the one opened at css[i]."""
    depth, q = 0, None
    while i < len(css):
        c = css[i]
        if q:
            if c == "\\":
                i += 1
            elif c == q:
                q = None
        elif c in "\"'":
            q = c
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError("a stylesheet block that never closes")


def _split_top(s, sep):
    out, depth, q, cur = [], 0, None, ""
    for c in s:
        if q:
            q = None if c == q else q
        elif c in "\"'":
            q = c
        elif c in "([":
            depth += 1
        elif c in ")]":
            depth -= 1
        elif c == sep and depth == 0:
            out.append(cur); cur = ""; continue
        cur += c
    out.append(cur)
    return out


def _guard(rules, root):
    """The same rules, each selector tied to the root's theme: :root becomes root, and .x becomes root .x."""
    out, i = "", 0
    while i < len(rules):
        j = rules.find("{", i)
        if j < 0:
            break
        end = _block_end(rules, j)
        sels = [s.strip() for s in _split_top(rules[i:j], ",")]
        guarded = [root + s[len(":root"):] if s.startswith(":root") else f"{root} {s}" for s in sels]
        out += ",".join(guarded) + rules[j:end]
        i = end
    return out


def themed(css):
    """Each dark-screen block kept for the system's setting, unless a light theme is picked in claude.ai, and copied
    for a dark theme picked there (the page contract: data-theme on the root). The values are the site's own."""
    out, i = "", 0
    pat = re.compile(r"@media([^{]*prefers-color-scheme\s*:\s*dark[^{]*)\{")
    while True:
        m = pat.search(css, i)
        if not m:
            out += css[i:]
            break
        end = _block_end(css, m.end() - 1)
        prelude, inner = m.group(1).strip(), css[m.end():end - 1]
        rest = re.sub(r"\s*and\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)|\(\s*prefers-color-scheme\s*:\s*dark\s*\)\s*(and\s*)?", "", prelude).strip()
        out += css[i:m.start()]
        implicit = _guard(inner, ':root:not([data-theme="light"])')   # outside the f-string: Python 3.11 allows no backslash there
        out += f"@media {prelude}{{{implicit}}}"
        explicit = _guard(inner, ':root[data-theme="dark"]')
        out += f"@media {rest}{{{explicit}}}" if rest else explicit
        i = end
    return out + ':root[data-theme="dark"]{color-scheme:dark}:root[data-theme="light"]{color-scheme:light}'


FONT_FACE = re.compile(r"@font-face\s*\{[^}]*\}")


def stylesheets(public, hrefs, problems):
    """The site's stylesheets as the preview carries them: font faces once, with their files inside, then each sheet."""
    faces, sheets = [], {}
    for href in hrefs:
        f = os.path.join(public, href.lstrip("/"))
        if not os.path.isfile(f):
            problems.append(f"the stylesheet {href} isn't in the build"); continue
        css = open(f, encoding="utf-8").read()
        for face in FONT_FACE.findall(css):
            if face not in faces:
                faces.append(face)
        css = FONT_FACE.sub("", css)
        if re.search(r"url\(\s*[\"']?/", css):
            problems.append(f"{href} points to a file by its address on the site, which the preview can't follow")
        sheets[href] = themed(css)

    def inline(m):
        uri = data_uri(public, m.group(1))
        if not uri:
            problems.append(f"the font {m.group(1)} isn't in the build")
            return m.group(0)
        return f'url("{uri}")'

    fonts = "".join(re.sub(r"url\(\s*[\"']?(/[^\"')]+)[\"']?\s*\)", inline, f) for f in faces)
    return fonts, sheets


ROUTER = """(function () {
  "use strict";
  /* The preview's own script (spec X5): it shows one page at a time, the one the address's #name chooses, with the
     stylesheet and the body's classes that page has on the site. A #name with "--" in it is a part of a page. */
  var doc = document, body = doc.body, pages = {}, current = null;
  doc.documentElement.lang = "en";
  Array.prototype.forEach.call(doc.querySelectorAll("[data-preview-page]"), function (p) { pages[p.id] = p; });
  var sheets = Array.prototype.slice.call(doc.querySelectorAll("style[data-sheet]"));
  var classes = {};
  Object.keys(pages).forEach(function (k) { (pages[k].getAttribute("data-body-class") || "").split(" ").forEach(function (c) { if (c) classes[c] = 1; }); });
  function show(picked) {
    var name = decodeURIComponent((location.hash || "").slice(1)), key = name.split("--")[0];
    var page = pages[key] || pages.home, target = name && name !== page.id ? doc.getElementById(name) : null;
    if (page !== current) {
      Object.keys(pages).forEach(function (k) { pages[k].hidden = pages[k] !== page; });
      sheets.forEach(function (s) { s.media = s.getAttribute("data-sheet") === page.getAttribute("data-sheet") ? "all" : "not all"; });
      Object.keys(classes).forEach(function (c) { body.classList.remove(c); });
      (page.getAttribute("data-body-class") || "").split(" ").forEach(function (c) { if (c) body.classList.add(c); });
      current = page;
    }
    if (target) { target.scrollIntoView(); }
    else { window.scrollTo(0, 0); }
    /* Focus is never dropped: a reader who follows a link lands on the page's title, as the site's own single document does. */
    var title = page.querySelector("h1");
    if (picked === true && title && !target) { title.setAttribute("tabindex", "-1"); title.focus({ preventScroll: true }); }
  }
  window.addEventListener("hashchange", function () { show(true); });
  show(false);
})();"""

STAND_IN = """<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
</head><body>
"""


def build(public):
    """The preview's page, the pages it holds, and what stands in the way of a faithful copy."""
    pages, problems = gather(public)
    if "/" not in pages:
        raise ValueError(f"{public} has no front door: build the site first")
    for p in pages.values():
        if not re.fullmatch(r"[A-Za-z0-9-]+", p.key) or p.key in RESERVED or p.key.startswith("comment-") or "--" in p.key:
            problems.append(f"{p.path}: its #name {p.key} can't be used on claude.ai")
        for i in p.ids:
            if not re.fullmatch(r"[A-Za-z0-9-]+", i) or "--" in i:
                problems.append(f"{p.path}: the id {i} can't become a plain #name")
        if p.css is None:
            problems.append(f"{p.path} links no stylesheet")
    hrefs = sorted({p.css for p in pages.values() if p.css})
    fonts, sheets = stylesheets(public, hrefs, problems)
    first = pages["/"].css
    parts = [f"<title>{TITLE}</title>",
             "<meta name=\"description\" content=\"Every page of joestanley.org as the site shows it, for the owner's notes.\">",
             # A title the preview focuses when a reader follows a link shows no ring, as the site's single document
             # does for its units (pm.css): on the site, a page that opens has nothing focused.
             f"<style data-fonts>{fonts}[data-preview-page] h1[tabindex=\"-1\"]:focus{{outline:none}}</style>"]
    for h in hrefs:
        parts.append(f"<style data-sheet=\"{hrefs.index(h)}\" media=\"{'all' if h == first else 'not all'}\">{sheets.get(h, '')}</style>")
    dialogs, scripts = {}, []
    for p in pages.values():
        body = Rewriter(public, pages, p.key, problems, p.path).run(p.body)
        attrs = (f" id=\"{p.key}\" data-preview-page data-path=\"{p.path}\" data-sheet=\"{hrefs.index(p.css) if p.css else ''}\""
                 f" data-body-class=\"{p.body_class}\" aria-label=\"{p.title}\" style=\"display: contents\""
                 + ("" if p.path == "/" else " hidden"))
        parts.append(f"<div{attrs}>{body}</div>")
        for d in p.dialogs:
            did = re.search(r"\bid=\"([^\"]*)\"", d).group(1)
            if did in dialogs and dialogs[did] != d.strip():
                problems.append(f"{p.path}: the glossary pop-up {did} differs from another page's")
            dialogs.setdefault(did, d.strip())
        for s in p.scripts:
            if s not in scripts:
                scripts.append(s)
    shared = Rewriter(public, pages, None, problems, "a glossary pop-up").run("\n".join(dialogs.values()))
    parts.append(shared)
    parts.append(f"<script>{ROUTER}</script>")
    for s in scripts:
        f = os.path.join(public, s.lstrip("/"))
        js = open(f, encoding="utf-8").read() if os.path.isfile(f) else ""
        if not js:
            problems.append(f"the script {s} isn't in the build")
        parts.append("<script>" + js.replace("</script", "<\\/script") + "</script>")
    page = "\n".join(parts) + "\n"
    ids = re.findall(r"\sid=\"([^\"]*)\"", "".join(RAW.sub("", x) for x in parts))
    seen = set()
    for i in ids:
        if i in seen:
            problems.append(f"the id {i} appears twice in the preview")
        seen.add(i)
    if re.search(r"\s(?:href|src)=\"/(?!/)", RAW.sub("", page)):
        problems.append("something in the preview still points to an address on the site")
    if len(page.encode("utf-8")) > SIZE_LIMIT:
        problems.append(f"the preview is {len(page.encode('utf-8')) / 1e6:.1f} MB, over claude.ai's 16 MB")
    return page, list(pages.values()), sorted(set(problems))


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(2)
    public = a[0]
    page, pages, problems = build(public)
    lock = json.load(open(LOCK, encoding="utf-8")) if os.path.exists(LOCK) else {}
    for p in problems:
        print("problem:", p)
    if "--check" in a:
        if problems:
            sys.exit(1)
        if lock.get("sha256") != sha(page):
            print(f"The preview differs from what was last published ({lock.get('published', 'never')}): republish it.")
            sys.exit(1)
        print("The preview matches what was last published."); return
    if "--record" in a:
        if problems:
            sys.exit(1)
        nxt = a[a.index("--record") + 1:a.index("--record") + 2]
        if nxt and nxt[0].startswith("https://claude.ai/"):
            lock["url"] = nxt[0]   # the first publish, or a new artifact
        lock.update({"sha256": sha(page), "published": datetime.date.today().isoformat(), "pages": len(pages)})
        lock = {"url": lock.get("url", ""), **{k: v for k, v in lock.items() if k != "url"}}
        json.dump(lock, open(LOCK, "w", encoding="utf-8"), indent=2); open(LOCK, "a").write("\n")
        print(f"Recorded the preview as published: {len(pages)} pages, {lock['sha256'][:12]}."); return
    out = a[a.index("--local") + 1] if "--local" in a else a[1]
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    open(out, "w", encoding="utf-8").write(STAND_IN + page + "</body></html>\n" if "--local" in a else page)
    print(f"{out}: {len(page.encode('utf-8')) / 1e6:.1f} MB, {len(pages)} pages")
    for p in pages:
        print(f"  #{p.key:<38} {p.path}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
