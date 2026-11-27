# Print the whole syllabus (/pm/all/) to PDF. Usage: make-pdf.py <site_dir> <out.pdf> <footer label>
# Serves the built site locally, prints in light mode with page numbers in the footer, then finishes the file
# the way a PDF reader and a library expect (spec P4 to P6):
#   - tagged for screen readers (headings, lists, tables, figure text), with the glossary tagged as a list
#     of terms and definitions, and non-standard tags mapped to standard ones;
#   - every link inside the syllabus jumps within the PDF, and every link carries a description;
#   - bookmarks that follow the document: units, their sections, a module's cards, the glossary's terms;
#   - title, author, subject, keywords and language in the document information and in XMP metadata,
#     taken from the page (content/pm/all.md and hugo.yaml), and opening with the bookmarks showing.
# Needs Playwright 1.42 or later with Chrome, pikepdf and pypdfium2.
import os, sys, asyncio, threading, http.server, functools, socketserver, tempfile, datetime
from playwright.async_api import async_playwright
import pikepdf
import pypdfium2 as pdfium

site, out, label = sys.argv[1], sys.argv[2], sys.argv[3]


class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass


srv = socketserver.TCPServer(("127.0.0.1", 0), functools.partial(Q, directory=site)); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
def foot(left):
    return f'''<div style="width:100%;font-family:'Public Sans',Arial,sans-serif;font-size:8pt;color:#3d4350;padding:0 0.8in;display:flex;justify-content:space-between;">
<span>{left}</span><span><span class="pageNumber"></span> of <span class="totalPages"></span></span></div>'''

# What the document says about itself and how it is divided, read from the page that is printed.
JS_INFO = """() => {
  const meta = n => { const m = document.querySelector(`meta[name="${n}"]`); return m ? m.content.trim() : ''; };
  const text = el => el ? el.textContent.replace(/\\s+/g, ' ').trim() : '';
  const units = [...document.querySelectorAll('main article.unit')].map(a => ({
    id: a.id, kind: [...a.classList].find(c => c !== 'unit'), module: a.dataset.module || '',
    num: text(a.querySelector('.kicker .tag')).replace(/\\D/g, ''), title: text(a.querySelector('h1')) }));
  const terms = [...document.querySelectorAll('.gloss-list > [id]')].map(d => ({ id: d.id, label: text(d.querySelector('dt')) }));
  return { title: meta('pdf:title'), subject: meta('pdf:subject'), keywords: meta('keywords'), author: meta('author'),
           rights: meta('pdf:rights'), rightsUrl: meta('pdf:rights-url'),
           lang: document.documentElement.lang || 'en', units, terms };
}"""


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get("CHROME", "/usr/bin/google-chrome"), args=["--no-sandbox"])
        ctx = await b.new_context(color_scheme="light")
        pg = await ctx.new_page()
        await pg.goto(f"http://127.0.0.1:{port}/pm/all/"); await pg.wait_for_timeout(600)
        await pg.evaluate("document.fonts.ready")
        await pg.evaluate("document.querySelectorAll('.deeper details, details.why').forEach(d => d.open = true)")
        info = await pg.evaluate(JS_INFO)
        info["chrome"] = b.version
        await pg.pdf(path=out, format="Letter", print_background=True, prefer_css_page_size=True,
                     display_header_footer=True, header_template="<span></span>",
                     footer_template=foot(f"{label}. {info['rights']}." if info.get("rights") else label),
                     tagged=True, outline=True)
        await b.close()
    return info


info = asyncio.run(main())
srv.shutdown()


def link_texts(path):
    """The words under each link, page by page, so each link can carry a description (spec P5)."""
    doc = pdfium.PdfDocument(path)
    found = []
    for page in doc:
        tp = page.get_textpage()
        found.append(tp)
    return doc, found


def finish(path, info):
    doc, textpages = link_texts(path)
    pdf = pikepdf.open(path, allow_overwriting_input=True)
    root = pdf.Root
    units, terms = info["units"], info["terms"]
    labels = {}
    for u in units:
        if u["kind"] == "start":
            u["label"] = f"Start: {u['title']}"
        elif u["kind"] == "module":
            u["label"] = f"Module {u['num']}: {u['title']}"
        elif u["kind"] == "card":
            u["label"] = f"Card: {u['title']}"
        elif u["kind"] == "closing":   # The Compass (spec S21), named by its kicker, "In closing"
            u["label"] = f"In closing: {u['title']}"
        else:
            u["label"] = u["title"]
        labels[u["id"]] = u["label"]
    for t in terms:
        labels[t["id"]] = f"{t['label']}, in the glossary"
    labels["dice-game"] = "The dice game"

    # Links: a description on each (P5). A link that wraps onto a second line prints as two link areas,
    # so neighbouring areas with the same target share the words of both. A glossary term is described by
    # its entry's name; other links by their words.
    for i, page in enumerate(pdf.pages):
        annots = [a for a in page.get("/Annots", []) if a.get("/Subtype") == "/Link"]
        if not annots:
            continue
        page.Tabs = pikepdf.Name.S
        tp = textpages[i]
        found = []
        for a in annots:
            x0, y0, x1, y1 = [float(v) for v in a.Rect]
            words = " ".join(tp.get_text_bounded(left=x0, bottom=y0, right=x1, top=y1).split()).strip(" .,;:")
            act = a.get("/A")
            target = str(a.get("/Dest", "")).lstrip("/") if act is None else str(act.get("/URI", ""))
            found.append([a, target, words])
        for j in range(1, len(found)):
            if found[j][1] == found[j - 1][1]:
                joined = f"{found[j - 1][2]} {found[j][2]}".strip()
                found[j - 1][2] = found[j][2] = joined
        for a, target, words in found:
            if target.startswith("g-"):
                desc = labels.get(target, f"{words}, in the glossary")
            else:
                desc = words or labels.get(target, target or "Link")
            a.Contents = pikepdf.String(desc)

    # Bookmarks: Chrome writes one per heading, nested by level. Keep units and their sections, put each
    # module's cards beneath it, name units for what they are, and list the glossary's terms (P6).
    names = {str(k).lstrip("/"): v for k, v in root.Dests.items()} if "/Dests" in root else {}
    with pdf.open_outline() as ol:
        chrome = list(ol.root)
        if len(chrome) != len(units):
            raise SystemExit(f"make-pdf: {len(chrome)} top-level headings in the PDF, but {len(units)} units on the page")

        def item(title, dest, closed=True):
            it = pikepdf.OutlineItem(title, destination=dest)
            it.is_closed = closed
            return it

        def sections(top):
            return [item(c.title, c.destination) for c in top.children]

        built = {}
        for top, u in zip(chrome, units):
            it = item(u["label"], top.destination)
            it.children.extend(sections(top))
            if u["kind"] == "glossary":
                it.children.clear()
                for t in terms:
                    if t["id"] not in names:   # left for the checks (P5, P6) to report, so the PDF still prints
                        print(f"make-pdf: no place in the PDF for glossary term {t['id']}; do the terms link within the PDF?", file=sys.stderr)
                        continue
                    it.children.append(item(t["label"], names[t["id"]]))
            built[u["id"]] = it
        tree = []
        for u in units:
            if u["kind"] == "card":
                parent = built.get(u["module"])
                if parent is None:
                    raise SystemExit(f"make-pdf: card {u['id']} names module {u['module']}, which is not in the PDF")
                parent.children.append(built[u["id"]])
            else:
                tree.append(built[u["id"]])
        ol.root.clear()
        ol.root.extend(tree)

    # Tags: map the tags PDF 1.7 does not define to standard ones, and tag the glossary as a list:
    # one item per term, the term as its label and the definition as its body.
    st = root.StructTreeRoot
    used = set()

    def kids(e):
        k = e.get("/K")
        if isinstance(k, pikepdf.Array):
            return [x for x in k if isinstance(x, pikepdf.Dictionary) and "/S" in x]
        return [k] if isinstance(k, pikepdf.Dictionary) and "/S" in k else []

    def walk(e):
        used.add(str(e.S))
        for k in kids(e):
            walk(k)
    for k in kids(st):
        walk(k)
    role = {"/Strong": "/Span", "/Em": "/Span", "/Mark": "/Span", "/Aside": "/Sect", "/Title": "/H1", "/FENote": "/Note", "/Sub": "/Span"}
    rm = pikepdf.Dictionary({k: pikepdf.Name(v) for k, v in role.items() if k in used})
    if len(rm):
        st.RoleMap = rm
    arts = []

    def find_arts(e):
        if str(e.S) == "/Art":
            arts.append(e); return
        for k in kids(e):
            find_arts(k)
    for k in kids(st):
        find_arts(k)
    gi = [i for i, u in enumerate(units) if u["kind"] == "glossary"]
    if gi and len(arts) == len(units):
        art = arts[gi[0]]

        def lists(e):
            """The glossary's list: a group whose children each hold exactly a term and a definition."""
            for k in kids(e):
                entries = kids(k)
                if entries and len(entries) == len(terms) and all(len(kids(x)) == 2 for x in entries):
                    return k
                found = lists(k)
                if found is not None:
                    return found
            return None
        dl = lists(art)
        if dl is None:
            raise SystemExit("make-pdf: could not find the glossary's list in the PDF's tags")
        dl.S = pikepdf.Name.L
        for entry in kids(dl):
            entry.S = pikepdf.Name.LI
            term, body = kids(entry)
            term.S = pikepdf.Name.Lbl
            body.S = pikepdf.Name.LBody

    # What the document says about itself (P6).
    title, author, subject, keywords, lang = info["title"], info["author"], info["subject"], info["keywords"], info["lang"]
    tool = f"joestanley.org tools-pm/make-pdf.py, Chrome {info['chrome']}"
    producer = f"{pdf.docinfo.get('/Producer', 'Skia/PDF')}; pikepdf {pikepdf.__version__}"
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    root.Lang = pikepdf.String(lang)
    root.PageMode = pikepdf.Name.UseOutlines
    root.PageLayout = pikepdf.Name.OneColumn
    vp = root.get("/ViewerPreferences") or pikepdf.Dictionary(Type=pikepdf.Name.ViewerPreferences)
    vp.DisplayDocTitle = True
    root.ViewerPreferences = vp
    with pdf.open_metadata(set_pikepdf_as_editor=False) as m:
        m.load_from_docinfo(pdf.docinfo)   # keeps Chrome's creation and modification dates
        m["dc:title"] = title
        m["dc:creator"] = [author]
        m["dc:description"] = subject
        m["dc:subject"] = [k.strip() for k in keywords.split(",") if k.strip()]
        m["dc:language"] = [lang]
        m["dc:format"] = "application/pdf"
        m["pdf:Keywords"] = keywords
        if info.get("rights"):   # whose it is and the license, on every page and here (spec L1)
            m["dc:rights"] = f"{info['rights']}: {info['rightsUrl']}"
            m["xmpRights:Marked"] = "True"
            m["xmpRights:WebStatement"] = info["rightsUrl"]
        m["pdf:Producer"] = producer
        m["xmp:CreatorTool"] = tool
        m["xmp:MetadataDate"] = now.isoformat()
    pdf.docinfo["/Title"] = title
    pdf.docinfo["/Author"] = author
    pdf.docinfo["/Subject"] = subject
    pdf.docinfo["/Keywords"] = keywords
    pdf.docinfo["/Creator"] = tool
    pdf.docinfo["/Producer"] = producer
    doc.close()
    pdf.save(path)


finish(out, info)
