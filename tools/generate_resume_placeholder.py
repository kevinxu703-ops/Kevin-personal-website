from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "resume-placeholder.pdf"


def build_pdf() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    page_width, page_height = A4
    pdf = canvas.Canvas(str(OUTPUT), pagesize=A4)
    pdf.setTitle("Caiya Luo - Resume Placeholder")
    pdf.setAuthor("Caiya Luo")

    paper = HexColor("#F3EFE4")
    ink = HexColor("#20251F")
    muted = HexColor("#696E66")
    green = HexColor("#355A4D")
    line = HexColor("#D2CCBE")

    pdf.setFillColor(paper)
    pdf.rect(0, 0, page_width, page_height, fill=1, stroke=0)

    margin = 58
    pdf.setStrokeColor(line)
    pdf.setLineWidth(0.7)
    pdf.line(margin, page_height - 75, page_width - margin, page_height - 75)

    pdf.setFillColor(ink)
    pdf.setFont("Times-Roman", 31)
    pdf.drawString(margin, page_height - 125, "Caiya Luo")

    pdf.setFillColor(green)
    pdf.setFont("Helvetica", 8)
    pdf.drawString(margin, page_height - 148, "RESUME PLACEHOLDER")

    pdf.setFillColor(muted)
    pdf.setFont("Times-Roman", 14)
    pdf.drawString(margin, page_height - 190, "This embedded page reserves space for the final resume.")

    sections = [
        ("EDUCATION", "School, expected graduation, and selected academic context"),
        ("RESEARCH", "Research projects, questions, roles, and selected outcomes"),
        ("PROJECTS", "Independent, collaborative, and interdisciplinary work"),
        ("ACTIVITIES", "Mathematics, writing, sport, community, and other commitments"),
    ]

    y = page_height - 260
    for label, description in sections:
        pdf.setStrokeColor(line)
        pdf.line(margin, y + 15, page_width - margin, y + 15)
        pdf.setFillColor(green)
        pdf.setFont("Helvetica", 8)
        pdf.drawString(margin, y, label)
        pdf.setFillColor(muted)
        pdf.setFont("Times-Roman", 12)
        pdf.drawString(margin + 110, y, description)
        y -= 84

    pdf.setStrokeColor(line)
    pdf.line(margin, 72, page_width - margin, 72)
    pdf.setFillColor(muted)
    pdf.setFont("Helvetica", 7)
    pdf.drawString(margin, 53, "Temporary content - replace output/pdf/resume-placeholder.pdf when the final resume is ready.")

    pdf.showPage()
    pdf.save()


if __name__ == "__main__":
    build_pdf()
