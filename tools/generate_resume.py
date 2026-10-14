"""Build the author-approved public resume and render it for visual review.

Requires reportlab, pypdf, pypdfium2, and the Windows Calibri font family.
Run from the repository root with the bundled Python runtime.
"""

from pathlib import Path
from html import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, HRFlowable, KeepTogether,
    PageTemplate, Paragraph, Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "jiankun-xu-resume.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)
FONTS = Path("C:/Windows/Fonts")
for font_name, font_file in [
    ("Calibri", "calibri.ttf"),
    ("Calibri-Bold", "calibrib.ttf"),
    ("Calibri-Italic", "calibrii.ttf"),
    ("Calibri-Light", "calibril.ttf"),
]:
    pdfmetrics.registerFont(TTFont(font_name, str(FONTS / font_file)))
pdfmetrics.registerFontFamily(
    "Calibri", normal="Calibri", bold="Calibri-Bold",
    italic="Calibri-Italic", boldItalic="Calibri-Bold",
)

PAGE_W, PAGE_H = A4
MARGIN = 44
WIDTH = PAGE_W - 2 * MARGIN
INK = colors.HexColor("#202927")
MUTED = colors.HexColor("#59635E")
ACCENT = colors.HexColor("#355A4D")
LINE = colors.HexColor("#CCD3CE")

styles = {
    "body": ParagraphStyle(
        "Body", fontName="Calibri", fontSize=10.2, leading=12.4,
        textColor=INK, spaceAfter=2,
    ),
    "bullet": ParagraphStyle(
        "Bullet", fontName="Calibri", fontSize=10.2, leading=12.4,
        textColor=INK, leftIndent=10, firstLineIndent=-8, spaceAfter=2,
    ),
    "title": ParagraphStyle(
        "EntryTitle", fontName="Calibri-Bold", fontSize=10.7, leading=13,
        textColor=INK,
    ),
    "date": ParagraphStyle(
        "Date", fontName="Calibri", fontSize=9.3, leading=12,
        textColor=MUTED, alignment=TA_RIGHT,
    ),
    "meta": ParagraphStyle(
        "Meta", fontName="Calibri-Italic", fontSize=9.6, leading=11.5,
        textColor=MUTED, spaceAfter=3,
    ),
    "section": ParagraphStyle(
        "Section", fontName="Calibri-Bold", fontSize=11.7, leading=15,
        textColor=ACCENT, spaceBefore=5, spaceAfter=2,
        keepWithNext=True,
    ),
    "honor": ParagraphStyle(
        "Honor", fontName="Calibri", fontSize=10.2, leading=12.4,
        textColor=INK, spaceAfter=2.5,
    ),
}


def p(text, style="body"):
    return Paragraph(text, styles[style])


def link(text, url):
    return f'<link href="{escape(url, quote=True)}" color="#202927">{text}</link>'


def section(title):
    return [
        p(title.upper(), "section"),
        HRFlowable(width="100%", thickness=0.45, color=LINE, spaceAfter=4),
    ]


def heading(title, date="", date_width=110):
    if not date:
        return p(title, "title")
    table = Table(
        [[p(title, "title"), p(date, "date")]],
        colWidths=[WIDTH - date_width, date_width], hAlign="LEFT",
    )
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return table


def entry(title, date="", meta=None, bullets=(), extra=None, gap=7):
    items = [heading(title, date), Spacer(1, 2)]
    if meta:
        items.append(p(meta, "meta"))
    for text in bullets:
        items.append(p("&#8226; " + text, "bullet"))
    if extra:
        items.append(p(extra, "meta"))
    items.append(Spacer(1, gap))
    return KeepTogether(items)


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setTitle("Jiankun (Kevin) Xu | Resume")
    canvas.setAuthor("Jiankun (Kevin) Xu")
    canvas.setSubject("Education, research, engineering projects, selected honors, and skills")
    if doc.page == 1:
        canvas.setFillColor(INK)
        canvas.setFont("Calibri-Light", 30)
        name_prefix = "Jiankun (Kevin) "
        canvas.drawString(MARGIN, PAGE_H - 49, name_prefix)
        canvas.setFont("Calibri-Bold", 30)
        canvas.drawString(
            MARGIN + pdfmetrics.stringWidth(name_prefix, "Calibri-Light", 30),
            PAGE_H - 49, "Xu",
        )
        contacts = Paragraph(
            'Beijing, China &nbsp; | &nbsp; '
            '<link href="mailto:kevinxu703@gmail.com">kevinxu703@gmail.com</link>'
            ' &nbsp; | &nbsp; '
            '<link href="https://kevinjkxu.com/">kevinjkxu.com</link>',
            ParagraphStyle(
                "Contact", fontName="Calibri", fontSize=10, leading=12,
                textColor=MUTED,
            ),
        )
        _, h = contacts.wrap(WIDTH, 20)
        contacts.drawOn(canvas, MARGIN, PAGE_H - 69 - h / 2)
        canvas.setStrokeColor(ACCENT)
        canvas.setLineWidth(1)
        canvas.line(MARGIN, PAGE_H - 86, PAGE_W - MARGIN, PAGE_H - 86)
    else:
        canvas.setFont("Calibri-Bold", 11)
        canvas.setFillColor(INK)
        canvas.drawString(MARGIN, PAGE_H - 38, "Jiankun (Kevin) Xu")
        canvas.setFont("Calibri", 9)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 38, "kevinjkxu.com")
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.45)
        canvas.line(MARGIN, PAGE_H - 47, PAGE_W - MARGIN, PAGE_H - 47)
    canvas.setFont("Calibri", 8.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN, 25, "Jiankun (Kevin) Xu")
    canvas.drawRightString(PAGE_W - MARGIN, 25, str(doc.page))
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUT), pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=93, bottomMargin=43,
    pageCompression=1, allowSplitting=1,
)
doc.addPageTemplates([
    PageTemplate(
        id="First",
        frames=[Frame(
            MARGIN, 43, WIDTH, PAGE_H - 140,
            leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
        )],
        onPage=header_footer,
    ),
    PageTemplate(
        id="Later",
        frames=[Frame(
            MARGIN, 43, WIDTH, PAGE_H - 101,
            leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
        )],
        onPage=header_footer,
    ),
])

story = []
story += section("Education")
story.append(heading(
    "The Experimental High School Attached to Beijing Normal University",
    "Sep 2024 - Jul 2027", date_width=108,
))
story.append(p("International Division | Beijing, China | Class of 2027", "meta"))
story.append(p(
    "<b>GPA:</b> 100/100 &nbsp; <b>SAT:</b> 1570 (Math 800; Reading and Writing 770)"
    " &nbsp; <b>TOEFL:</b> 113"
))
story.append(Spacer(1, 4))
story.append(heading(
    "The High School Affiliated to Beijing Normal University",
    "Sep 2021 - Jul 2024", date_width=108,
))
story.append(p("Junior Secondary Education | Beijing, China", "meta"))

story += section("Selected Research and Mathematical Exposition")
story.append(entry(
    link("Inverse Spectral Geometry: Hearing the Shape of a Drum",
         "https://kevinjkxu.com/research/drum-shape.html"),
    "Grades 11-12",
    meta="Sole author | Advisors: Jian Deng and Lingyun Chang",
    bullets=[
        "Studied how the Dirichlet spectrum encodes the boundary of an analytic planar domain. "
        "Constructed boundary operators and finite-matrix approximations from Riemann-map coefficients.",
        "Derived a regularized-determinant spectral criterion and a fixed-parameter convergence result. "
        "Tested forward spectral calculations and restricted inverse fitting on the Neumann oval.",
    ],
    gap=5,
))
story.append(entry(
    link("Constraint Repair for Reaction-Diffusion PINNs",
         "https://kevinjkxu.com/research/pinn.html"),
    "Grades 10-11",
    meta="Co-author with Lingyun Chang | Manuscripts under review at Computer Physics Communications and ICMLC 2027",
    bullets=[
        "Developed training and post-processing methods for physics-informed neural networks (PINNs) "
        "in stiff heat-species systems, testing feasibility and accuracy across 10 random seeds.",
        "Separated box clipping from mean correction. In one held-out benchmark, clipping reduced "
        "upper-bound violations from 11.2% to zero, while mean correction revealed an accuracy tradeoff.",
    ],
    gap=5,
))
story.append(entry(
    link("Flood Susceptibility Assessment in Fangshan, Beijing",
         "https://kevinjkxu.com/research/flood-prevention.html"),
    "2025-2026",
    meta="Co-author with Jia Li | Researcher and conference presenter",
    bullets=[
        "Combined flood and insurance records with 11 environmental factors in a convolutional "
        "neural network. Evaluated susceptibility maps through field checks and factor-sensitivity analysis.",
    ],
    extra="Presented at the First Symposium on Geocomputation and System Simulation "
          "(conference: July 10-12, 2026).",
    gap=5,
))
story.append(entry(
    link("Integer and Plane Partitions | Pioneer Academics",
         "https://kevinjkxu.com/research/course-paper.html"),
    "May-Sep 2025",
    meta="Expository course paper | Advisor: Carl Yerger, Davidson College",
    bullets=[
        "Reconstructed Newman's proof of the Hardy-Ramanujan partition asymptotic, "
        "expanding the generating-function argument, contour estimates, and error control "
        "for readers with a high-school mathematics background.",
    ],
    gap=2,
))

story += section("Additional Engineering Projects")
story.append(entry(
    "Real World Design Challenge (RWDC) | (Vice) President",
    "Sep 2024 - May 2025",
    bullets=[
        "Worked on a biplane cargo-drone concept for wildfire relief, including avionics selection, "
        "power and payload checks, and route planning. Team placed 2nd in China and 3rd globally.",
    ],
    gap=5,
))
story.append(entry(
    "ISSSP | Team Leader",
    "Jun-Nov 2025",
    bullets=[
        "Developed the proposal <i>Ilmenite Reduction and Magnetic Separation in Space</i>, "
        "combining carbon reduction and magnetic separation to recover iron and titanium dioxide "
        "under microgravity. Received Global Gold.",
    ],
    gap=2,
))

story += section("Selected Honors")
honors = [
    "<b>AIME:</b> 14/15 (2026). <b>AMC 12:</b> 132 (2025); AMC 10/12 Distinction.",
    "<b>PUMaC, B Division:</b> Team Overall 2nd; Individual Overall 10th; "
    "Number Theory 9th; Algebra Gold Medal.",
    "<b>ARML Local:</b> Team 23rd globally, National Gold; Individual Round National Gold.",
    "<b>John Locke Essay Competition:</b> Commendations in History and Philosophy.",
    "<b>PhysicsBowl, Division 1:</b> National Top Gold. <b>HiMCM:</b> Honorable Mention.",
    "<b>SDSZ:</b> Full Academic Scholarship (Grades 10-12); Academic Contribution Award.",
]
story.extend(p(text, "honor") for text in honors)

story += section("Technical Skills and Languages")
story.append(p(
    "<b>Programming and typesetting:</b> Python, R, LaTeX."
    " &nbsp; <b>Languages:</b> Chinese (native), English (fluent)."
))

doc.build(story)
print(f"Created: {OUT}")

# PDFium is used for visual QA because Poppler is not installed in this environment.
import pypdfium2 as pdfium
from pypdf import PdfReader

reader = PdfReader(str(OUT))
print(f"Page count: {len(reader.pages)}")
assert len(reader.pages) == 1, "Resume should fit one readable page after the requested cuts."
text = "\n".join(page.extract_text() for page in reader.pages)
for expected in [
    "Jiankun (Kevin)", "Sep 2024 - Jul 2027", "100/100", "1570",
    "113", "14/15 (2026)", "23rd globally", "Computer Physics Communications",
    "ICMLC 2027", "Python, R, LaTeX", "under review",
    "The High School Affiliated to Beijing Normal University", "Sep 2021 - Jul 2024",
]:
    assert expected in text, f"Missing required content: {expected}"
assert "potential qualifier" not in text
for removed in [
    "AP scores", "WRITING IN MATHEMATICS AND PHILOSOPHY",
    "TEACHING, LEADERSHIP", "SDSZ Incubator", "Integration Bee",
    "Table Tennis", "Nursing Home",
]:
    assert removed not in text, f"Unwanted content remains: {removed}"
assert "11.2%" in text
link_count = sum(
    1 for page in reader.pages for item in page.get("/Annots", [])
    if item.get_object().get("/Subtype") == "/Link"
)
print(f"Clickable links: {link_count}")
qa_dir = ROOT / "tmp" / "pdfs"
qa_dir.mkdir(parents=True, exist_ok=True)
pdf = pdfium.PdfDocument(str(OUT))
for page_index in range(len(pdf)):
    page = pdf[page_index]
    bitmap = page.render(scale=1.75)
    image = bitmap.to_pil()
    png_path = qa_dir / f"resume-public-page-{page_index + 1}.png"
    image.save(png_path)
    image.convert("RGB").save(
        qa_dir / f"resume-public-page-{page_index + 1}.jpg", quality=85,
    )
    print(f"Rendered: {png_path}")
    page.close()
pdf.close()
