from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO
from typing import List, Dict


def generate_breeds_pdf(breeds: List[Dict]) -> BytesIO:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=LETTER)
    width, height = LETTER

    title = "Dog Breeds - Alphabetical List with Details"
    margin_left = 50
    y = height - inch

    def add_footer(page_number: int):
        pdf.setFont("Helvetica-Oblique", 8)
        pdf.drawCentredString(width / 2, 20, f"Page {page_number}")

    page_number = 1
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(margin_left, y, title)
    y -= 30

    pdf.setFont("Helvetica", 11)

    for breed in breeds:
        fields = [
            ("Name", breed.get("name", "")),
            ("Life Span", breed.get("life_span", "")),
            ("Bred For", breed.get("bred_for", "")),
            ("Breed Group", breed.get("breed_group", "")),
            ("Temperament", breed.get("temperament", "")),
        ]

        for label, value in fields:
            pdf.setFont("Helvetica-Bold", 11)
            pdf.drawString(margin_left, y, f"{label}:")
            pdf.setFont("Helvetica", 11)
            pdf.drawString(margin_left + 100, y, value)
            y -= 18

        # Add spacing between breeds
        y -= 12

        # Handle page overflow
        if y < 60:
            add_footer(page_number)
            pdf.showPage()
            page_number += 1
            y = height - inch
            pdf.setFont("Helvetica", 11)

    add_footer(page_number)
    pdf.save()
    buffer.seek(0)
    return buffer
