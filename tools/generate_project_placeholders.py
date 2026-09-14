from pathlib import Path
import sys

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "pdf"

PROJECTS = [
    {
        "filename": "drum-shape-placeholder.pdf",
        "title": "Can One Hear the Shape of a Drum?",
        "field": "PURE MATHEMATICS / SPECTRAL GEOMETRY",
        "question": "What geometric information is encoded by a domain's spectrum?",
        "sections": ["Motivation and background", "Definitions and mathematical setup", "Central arguments and examples", "Reflection and references"],
    },
    {
        "filename": "pinn-placeholder.pdf",
        "title": "Physics-Informed Neural Networks",
        "field": "SCIENTIFIC COMPUTING / MACHINE LEARNING",
        "question": "How can physical laws guide a neural network's approximation?",
        "sections": ["Problem and governing equations", "Model and loss design", "Experiments and evaluation", "Limitations and next questions"],
    },
    {
        "filename": "flood-prevention-placeholder.pdf",
        "title": "Flood Prevention",
        "field": "APPLIED RESEARCH / MODELING AND RESILIENCE",
        "question": "How can models inform more resilient flood-prevention decisions?",
        "sections": ["Context and research question", "Data and modeling approach", "Risk analysis and interventions", "Discussion and references"],
    },
]


def build_project_pdf(project: dict[str, object]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / str(project["filename"])
    width, height = A4
    pdf = canvas.Canvas(str(output_path), pagesize=A4)
    pdf.setTitle(f'{project["title"]} - Project Placeholder')
    pdf.setAuthor("Jiankun (Kevin) Xu")

    paper = HexColor("#F3EFE4")
    ink = HexColor("#20251F")
    muted = HexColor("#696E66")
    green = HexColor("#355A4D")
    line = HexColor("#D2CCBE")
    margin = 58

    pdf.setFillColor(paper)
    pdf.rect(0, 0, width, height, fill=1, stroke=0)
    pdf.setStrokeColor(line)
    pdf.setLineWidth(0.7)
    pdf.line(margin, height - 70, width - margin, height - 70)

    pdf.setFillColor(green)
    pdf.setFont("Helvetica", 7.5)
    pdf.drawString(margin, height - 101, str(project["field"]))

    pdf.setFillColor(ink)
    pdf.setFont("Times-Roman", 27)
    title = str(project["title"])
    if len(title) > 34:
        split_at = title.rfind(" ", 0, 34)
        pdf.drawString(margin, height - 143, title[:split_at])
        pdf.drawString(margin, height - 175, title[split_at + 1 :])
        question_y = height - 222
    else:
        pdf.drawString(margin, height - 143, title)
        question_y = height - 190

    pdf.setFillColor(muted)
    pdf.setFont("Times-Italic", 13)
    pdf.drawString(margin, question_y, str(project["question"]))

    y = question_y - 82
    for number, section in enumerate(project["sections"], start=1):
        pdf.setStrokeColor(line)
        pdf.line(margin, y + 18, width - margin, y + 18)
        pdf.setFillColor(green)
        pdf.setFont("Helvetica", 7.5)
        pdf.drawString(margin, y, f"0{number}")
        pdf.setFillColor(ink)
        pdf.setFont("Times-Roman", 13)
        pdf.drawString(margin + 48, y, str(section))
        pdf.setFillColor(muted)
        pdf.setFont("Helvetica", 8)
        pdf.drawString(margin + 48, y - 21, "Content, figures, and references will be added here.")
        y -= 88

    pdf.setStrokeColor(line)
    pdf.line(margin, 72, width - margin, 72)
    pdf.setFillColor(muted)
    pdf.setFont("Helvetica", 7)
    pdf.drawString(margin, 53, "Temporary project document - replace this file when the research material is ready.")
    pdf.drawRightString(width - margin, 53, "Jiankun (Kevin) Xu")

    pdf.showPage()
    pdf.save()


if __name__ == "__main__":
    requested = set(sys.argv[1:])
    for project_data in PROJECTS:
        if requested and str(project_data["filename"]) not in requested:
            continue
        build_project_pdf(project_data)
