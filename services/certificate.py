from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from datetime import date
import io

def generate_certificate(name: str, course: str = "Retail Analytics") -> bytes:
    buffer = io.BytesIO()
    w, h = landscape(A4)
    c = canvas.Canvas(buffer, pagesize=landscape(A4))

    # Background
    c.setFillColor(colors.HexColor("#F7FBFC"))
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # Border
    c.setStrokeColor(colors.HexColor("#769FCD"))
    c.setLineWidth(8)
    c.rect(20, 20, w - 40, h - 40, fill=0, stroke=1)

    c.setStrokeColor(colors.HexColor("#B9D7EA"))
    c.setLineWidth(2)
    c.rect(30, 30, w - 60, h - 60, fill=0, stroke=1)

    # Title
    c.setFillColor(colors.HexColor("#769FCD"))
    c.setFont("Helvetica-Bold", 42)
    c.drawCentredString(w / 2, h - 130, "Certificate of Completion")

    # Subtitle line
    c.setStrokeColor(colors.HexColor("#769FCD"))
    c.setLineWidth(1.5)
    c.line(100, h - 150, w - 100, h - 150)

    # Body text
    c.setFillColor(colors.HexColor("#444444"))
    c.setFont("Helvetica", 18)
    c.drawCentredString(w / 2, h - 200, "This is to certify that")

    # Name
    c.setFillColor(colors.HexColor("#2C3E50"))
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(w / 2, h - 255, name)

    # Underline name
    name_width = c.stringWidth(name, "Helvetica-Bold", 36)
    c.setStrokeColor(colors.HexColor("#769FCD"))
    c.setLineWidth(1.5)
    c.line(w / 2 - name_width / 2, h - 265, w / 2 + name_width / 2, h - 265)

    # Course text
    c.setFillColor(colors.HexColor("#444444"))
    c.setFont("Helvetica", 18)
    c.drawCentredString(w / 2, h - 310, "has successfully completed the course")

    c.setFillColor(colors.HexColor("#769FCD"))
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(w / 2, h - 355, course)

    # Date
    c.setFillColor(colors.HexColor("#777777"))
    c.setFont("Helvetica", 14)
    c.drawCentredString(w / 2, h - 410, f"Date of Completion: {date.today().strftime('%B %d, %Y')}")

    # Footer
    c.setFillColor(colors.HexColor("#769FCD"))
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(w / 2, 60, "AI Training Platform — Powered by GANIT Business Solutions")

    c.save()
    buffer.seek(0)
    return buffer.read()