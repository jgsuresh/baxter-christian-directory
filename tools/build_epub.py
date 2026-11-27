# /// script
# requires-python = ">=3.10"
# dependencies = ["markdown>=3.5", "pillow>=10"]
# ///
"""Build an EPUB of the modernized text, formatted for Kindle and other readers.

Run from the repository root:

    uv run tools/build_epub.py

Writes dist/baxter-christian-directory-part1.epub. Each source file becomes one
XHTML file; chapters get a title page. Baxter's footnote markers become links
to his notes (and back), which Kindle shows as pop-up notes.
"""
import datetime
import glob
import html
import io
import os
import re
import uuid
import zipfile
from xml.etree import ElementTree

import markdown
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT, "modernized", "part1-ethics")
OUT = os.path.join(ROOT, "dist", "baxter-christian-directory-part1.epub")

TITLE = "A Christian Directory, Part 1: Christian Ethics"
SUBTITLE = "A Modernized Edition (Draft)"
AUTHOR = "Richard Baxter"
BOOK_ID = "urn:uuid:" + str(uuid.uuid5(uuid.NAMESPACE_URL, "https://github.com/jgsuresh/baxter-christian-directory/part1"))

CHAPTERS = {
    1: "Directions to Unconverted Sinners, and the Temptations That Hinder Conversion",
    2: "Directions to Young Christians or Beginners in Religion, for Their Establishment and Safe Proceeding",
    3: "The General Grand Directions for Walking with God, in a Life of Faith and Holiness",
    4: "Subordinate Directions Against Those Grand Heart Sins Which Are Directly Contrary to the Life of Godliness and Christianity",
    5: "Further Subordinate Directions for the Next Great Duties of Religion (Redeeming Time)",
    6: "Directions for the Government of the Thoughts",
    7: "Directions for the Government of the Passions",
    8: "Directions for the Government of the Senses",
    9: "Directions for the Government of the Tongue",
    10: "Directions for the Government of the Body",
}

CSS = """
body { margin: 0 2%; line-height: 1.4; }
p { margin: 0 0 0.6em 0; text-indent: 0; text-align: left; }
h1 { font-size: 1.6em; text-align: center; margin: 2em 0 0.8em 0; page-break-before: always; }
h2 { font-size: 1.25em; margin: 1.6em 0 0.8em 0; page-break-before: always; }
h3 { font-size: 1.05em; margin: 1.6em 0 0.6em 0; }
.chapter-page h1 { margin-top: 30%; font-size: 1.8em; }
.chapter-page p.chapter-title { text-align: center; font-style: italic; font-size: 1.15em; margin: 1em 10%; }
p.margin { font-size: 0.85em; margin: 0.8em 0 0.3em 1.5em; color: #444; }
sup.noteref { font-size: 0.7em; line-height: 0; }
sup.noteref a, a.noteback { text-decoration: none; }
.notes { font-size: 0.88em; }
.notes h3 { font-size: 1.0em; text-transform: uppercase; letter-spacing: 0.05em; }
.notes li { margin-bottom: 0.4em; }
hr { border: 0; border-top: 1px solid #999; width: 30%; margin: 1.5em auto; }
blockquote { margin: 0.6em 1.5em; }
.titlepage { text-align: center; }
.titlepage h1 { margin-top: 25%; page-break-before: avoid; }
.titlepage p { text-align: center; margin: 0.6em 0; }
.front p { margin-bottom: 0.8em; }
"""

ENT = {"&nbsp;": "&#160;", "&mdash;": "—", "&ndash;": "–", "&hellip;": "…",
       "&lsquo;": "‘", "&rsquo;": "’", "&ldquo;": "“", "&rdquo;": "”"}


def xhtml_doc(title, body, cls=""):
    attr = f' class="{cls}"' if cls else ""
    return ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">\n'
            f'<head><meta charset="utf-8"/><title>{html.escape(title)}</title>'
            '<link rel="stylesheet" type="text/css" href="style.css"/></head>\n'
            f'<body{attr}>\n{body}\n</body>\n</html>\n')


def md_to_html(text):
    out = markdown.markdown(text, extensions=["sane_lists"], output_format="xhtml")
    for k, v in ENT.items():
        out = out.replace(k, v)
    return out


ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50}


def arabic(heading):
    """Show heading numbers consistently: 'Grand Direction II' becomes 'Grand Direction 2'."""
    def conv(mo):
        r, total = mo.group(2), 0
        for a, b in zip(r, r[1:] + " "):
            v = ROMAN[a]
            total += -v if b != " " and ROMAN[b] > v else v
        return f"{mo.group(1)} {total}"
    return re.sub(r"\b(Direction|Title|Part|Temptation|Chapter)s? ([IVXL]+)\b", conv, heading)


def convert_file(path):
    """Return (heading, label, xhtml body) for one modernized source file."""
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    m = re.search(r"^# (.+)$", text, flags=re.M)
    heading = arabic(m.group(1).strip()) if m else os.path.basename(path)
    text = text[:m.start()] + text[m.end():] if m else text

    # Repository-relative links (e.g. to NOTICE.md) mean nothing in the book: keep the text only.
    text = re.sub(r"\[([^\]]+)\]\((?!https?:)[^)]+\)", r"\1", text)

    # Keep Baxter's numbering exactly: stop Markdown from turning "7. ..." into a renumbered list.
    text = re.sub(r"^(\d+)\. ", r"\1\\. ", text, flags=re.M)

    split = re.search(r"^## Baxter's notes\s*$", text, flags=re.M)
    body, notes = (text[:split.start()], text[split.start():]) if split else (text, "")

    note_nums = set(re.findall(r"^\[(\d+)\](?= |$)", notes, flags=re.M))
    seen = set()

    def ref(mo):
        n = mo.group(1)
        if n not in note_nums:
            return mo.group(0)
        rid = f' id="r{n}"' if n not in seen else ""
        seen.add(n)
        return (f'<sup class="noteref"><a epub:type="noteref" href="#n{n}"{rid}>[{n}]</a></sup>')

    body = re.sub(r" \[(\d+)\]", ref, body)
    notes = re.sub(r"^\[(\d+)\](?= |$)",
                   lambda mo: (f'<a class="noteback" id="n{mo.group(1)}" href="#r{mo.group(1)}">[{mo.group(1)}]</a>'
                               if mo.group(1) in seen else mo.group(0)),
                   notes, flags=re.M)

    body_html = md_to_html(body)
    body_html = body_html.replace("<h2>", "<h3>").replace("</h2>", "</h3>")
    body_html = re.sub(r"<p><em>In the margin:", r'<p class="margin"><em>In the margin:', body_html)
    notes_html = md_to_html(notes).replace("<h2>", "<h3>").replace("</h2>", "</h3>") if notes else ""
    if notes_html:
        notes_html = f'<section class="notes" epub:type="rearnotes">\n{notes_html}\n</section>'

    label = re.sub(r"^Chapter \d+[,:]?\s*", "", heading).strip() or heading
    if label[:1].islower():
        label = label[0].upper() + label[1:]
    page_heading = heading
    out = f"<h2>{html.escape(page_heading)}</h2>\n{body_html}\n{notes_html}"
    return heading, label, out


def make_cover():
    w, h = 1600, 2560
    img = Image.new("RGB", (w, h), (244, 238, 226))
    d = ImageDraw.Draw(img)

    def font(size):
        for name in ["/System/Library/Fonts/Supplemental/Georgia.ttf", "/Library/Fonts/Georgia.ttf",
                     "/System/Library/Fonts/Times.ttc", "/System/Library/Fonts/Supplemental/Times New Roman.ttf"]:
            if os.path.exists(name):
                return ImageFont.truetype(name, size)
        return ImageFont.load_default(size)

    def center(y, text, size, fill=(40, 30, 20)):
        f = font(size)
        tw = d.textlength(text, font=f)
        d.text(((w - tw) / 2, y), text, font=f, fill=fill)

    d.rectangle([80, 80, w - 80, h - 80], outline=(120, 90, 60), width=6)
    d.rectangle([110, 110, w - 110, h - 110], outline=(120, 90, 60), width=2)
    center(520, "A CHRISTIAN", 150)
    center(700, "DIRECTORY", 150)
    d.line([(500, 940), (w - 500, 940)], fill=(120, 90, 60), width=4)
    center(1020, "Part 1: Christian Ethics", 84)
    center(1180, "or, Directions for the Private", 60, (90, 70, 50))
    center(1260, "Actions of Our Hearts and Lives", 60, (90, 70, 50))
    center(1760, "RICHARD BAXTER", 96)
    center(1900, "A Modernized Edition (Draft)", 64, (90, 70, 50))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=88)
    return buf.getvalue()


def front_matter(today):
    title = (f'<div class="titlepage"><h1>{html.escape(TITLE)}</h1>'
             f'<p><em>{html.escape(SUBTITLE)}</em></p>'
             f'<p>by {AUTHOR}</p>'
             '<p>Originally published 1673. Modernized from the 1846 edition.</p></div>')
    about = """<h1>About This Edition</h1>
<div class="front">
<p>This is a word-level modernization of Part 1 (Christian Ethics) of Richard Baxter&#8217;s <em>A Christian Directory</em>, made from the Project Gutenberg transcription of the 1846 edition. Old words, spellings, and verb forms are brought up to date; Baxter&#8217;s sentences are not split, merged, or summarized, so his argument and its order are as he wrote it.</p>
<p>Quoted Scripture is given in the NET Bible. Where the NET wording changes the sense Baxter relies on, the translator&#8217;s notes say so. Baxter&#8217;s own footnotes follow each section under &#8220;Baxter&#8217;s notes&#8221;; his Latin and Greek are kept as printed, followed by draft English translations made for this project. These translations have not yet been checked by a Latinist. The translator&#8217;s notes record word choices, corrected references, and source oddities.</p>
<p>Baxter&#8217;s margin summaries appear as small italic lines beginning &#8220;In the margin.&#8221; His footnote markers are links: select one to see the note.</p>
<p><strong>Status:</strong> this is a draft. Every section has been drafted and checked against the source, but none has had a final human edit.</p>
<p><strong>Scripture:</strong> Scripture quotations are from the NET Bible&#174;, copyright &#169; 1996, 2019 by Biblical Studies Press, L.L.C., https://netbible.com. All rights reserved. Quoted under the NET Bible&#8217;s published quotation terms.</p>
<p><strong>License:</strong> Baxter&#8217;s text is in the public domain. The modernized wording and notes are dedicated to the public domain under CC0; the NET Bible quotations are not covered by that dedication.</p>
<p>Source and updates: https://github.com/jgsuresh/baxter-christian-directory</p>
<p>Built """ + today + """.</p>
</div>"""
    return title, about


def main():
    files = sorted(glob.glob(os.path.join(SRC_DIR, "*.md")))
    today = datetime.date.today().isoformat()
    docs = []   # (filename, title, xhtml)
    toc = []    # [(label, href, [(label, href), ...])]

    title_x, about_x = front_matter(today)
    docs.append(("title.xhtml", TITLE, xhtml_doc(TITLE, title_x)))
    docs.append(("about.xhtml", "About This Edition", xhtml_doc("About This Edition", about_x)))
    toc.append(("About This Edition", "about.xhtml", []))

    current = None
    for i, path in enumerate(files):
        name = os.path.basename(path)
        heading, label, body = convert_file(path)
        fn = f"s{i:03d}.xhtml"
        if name.startswith("00-advertisement"):
            group = "adv"
        elif name.startswith("00-introduction"):
            group = "intro"
        else:
            group = int(re.match(r"ch(\d+)", name).group(1))
        if group != current:
            current = group
            if group == "adv":
                toc.append(("Advertisement to the Readers", fn, []))
            elif group == "intro":
                toc.append(("Part 1: Christian Ethics (Introduction)", fn, []))
            else:
                cfn = f"c{group:02d}.xhtml"
                page = (f'<h1>Chapter {group}</h1>\n<p class="chapter-title">{html.escape(CHAPTERS[group])}</p>')
                docs.append((cfn, f"Chapter {group}", xhtml_doc(f"Chapter {group}", page, "chapter-page")))
                toc.append((f"Chapter {group}: {CHAPTERS[group]}", cfn, []))
        if group == "adv":
            label = re.sub(r"^Advertisement to the Readers\s*", "", label).strip(" ()").capitalize() or label
        if group != "intro":
            toc[-1][2].append((label, fn))
        docs.append((fn, heading, xhtml_doc(heading, body)))

    # Check every document is well-formed XML before packaging.
    for fn, _, x in docs:
        try:
            ElementTree.fromstring(x.encode("utf-8"))
        except ElementTree.ParseError as e:
            raise SystemExit(f"Malformed XHTML in {fn}: {e}")

    # Navigation document (EPUB 3) and NCX (for older readers and Kindle conversion).
    def nav_items(items):
        out = []
        for label, href, kids in items:
            li = f'<li><a href="{href}">{html.escape(label)}</a>'
            if kids:
                li += "<ol>" + "".join(f'<li><a href="{h}">{html.escape(l)}</a></li>' for l, h in kids) + "</ol>"
            out.append(li + "</li>")
        return "\n".join(out)

    nav = xhtml_doc("Contents", '<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>\n' + nav_items(toc) + "\n</ol></nav>"
                    '\n<nav epub:type="landmarks" hidden=""><ol>'
                    '<li><a epub:type="cover" href="cover.xhtml">Cover</a></li>'
                    '<li><a epub:type="toc" href="nav.xhtml">Contents</a></li>'
                    f'<li><a epub:type="bodymatter" href="{toc[1][1]}">Beginning</a></li></ol></nav>')
    ElementTree.fromstring(nav.encode("utf-8"))

    ncx_pts, order = "", 0
    for label, href, kids in toc:
        order += 1
        pid = order
        inner = ""
        for l, h in kids:
            order += 1
            inner += f'<navPoint id="p{order}" playOrder="{order}"><navLabel><text>{html.escape(l)}</text></navLabel><content src="{h}"/></navPoint>'
        ncx_pts += f'<navPoint id="p{pid}" playOrder="{pid}"><navLabel><text>{html.escape(label)}</text></navLabel><content src="{href}"/>{inner}</navPoint>\n'
    ncx = ('<?xml version="1.0" encoding="utf-8"?>\n<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">'
           f'<head><meta name="dtb:uid" content="{BOOK_ID}"/><meta name="dtb:depth" content="2"/></head>'
           f'<docTitle><text>{html.escape(TITLE)}</text></docTitle><navMap>\n{ncx_pts}</navMap></ncx>')
    ElementTree.fromstring(ncx.encode("utf-8"))

    cover_x = xhtml_doc("Cover", '<div style="text-align:center"><img src="cover.jpg" alt="Cover" style="height:100%; max-width:100%"/></div>')

    modified = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest = ['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
                '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
                '<item id="css" href="style.css" media-type="text/css"/>',
                '<item id="cover-image" href="cover.jpg" media-type="image/jpeg" properties="cover-image"/>',
                '<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>']
    spine = ['<itemref idref="cover" linear="yes"/>']
    for fn, _, _ in docs:
        iid = fn.replace(".xhtml", "")
        manifest.append(f'<item id="{iid}" href="{fn}" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="{iid}"/>')
        if fn == "about.xhtml":
            spine.append('<itemref idref="nav"/>')
    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="en">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">{BOOK_ID}</dc:identifier>
<dc:title id="t1">{html.escape(TITLE)}</dc:title>
<meta refines="#t1" property="title-type">main</meta>
<dc:title id="t2">{html.escape(SUBTITLE)}</dc:title>
<meta refines="#t2" property="title-type">subtitle</meta>
<dc:creator id="a1">{AUTHOR}</dc:creator>
<meta refines="#a1" property="role" scheme="marc:relators">aut</meta>
<meta refines="#a1" property="file-as">Baxter, Richard</meta>
<dc:language>en</dc:language>
<dc:date>{today}</dc:date>
<dc:subject>Christian ethics</dc:subject>
<dc:subject>Puritans</dc:subject>
<dc:rights>Modernized text and notes: CC0. NET Bible quotations: copyright 1996, 2019 Biblical Studies Press, L.L.C.</dc:rights>
<meta property="dcterms:modified">{modified}</meta>
<meta name="cover" content="cover-image"/>
</metadata>
<manifest>
{chr(10).join(manifest)}
</manifest>
<spine toc="ncx">
{chr(10).join(spine)}
</spine>
</package>
"""
    ElementTree.fromstring(opf.encode("utf-8"))

    container = ('<?xml version="1.0" encoding="utf-8"?>\n<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                 '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with zipfile.ZipFile(OUT, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", container, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/toc.ncx", ncx, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", CSS, compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/cover.jpg", make_cover(), compress_type=zipfile.ZIP_STORED)
        z.writestr("OEBPS/cover.xhtml", cover_x, compress_type=zipfile.ZIP_DEFLATED)
        for fn, _, x in docs:
            z.writestr("OEBPS/" + fn, x, compress_type=zipfile.ZIP_DEFLATED)
    print(f"Wrote {OUT}: {len(docs)} documents, {os.path.getsize(OUT) // 1024} KB")


if __name__ == "__main__":
    main()
