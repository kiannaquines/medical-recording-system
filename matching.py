from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from PIL import Image

def create_lab_report(filename="cross-matching.pdf", logo_path=""):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Logo
    try:
        img = Image.open(logo_path)
        img_width, img_height = img.size
        aspect = img_height / float(img_width)
        desired_width = 1.3 * inch
        desired_height = desired_width * aspect
        c.drawImage(
            logo_path,
            45,
            height - 1.9 * inch,
            width=desired_width,
            height=desired_height,
            preserveAspectRatio=True,
        )
    except Exception as e:
        print(f"Could not load logo: {e}")

    def center_text(text, y_position, font_name="Helvetica", font_size=12, is_bold=False):
        if is_bold:
            font_name += "-Bold"
        c.setFont(font_name, font_size)
        text_width = c.stringWidth(text, font_name, font_size)
        x_position = (width - text_width) / 2
        c.drawString(x_position, y_position, text)

    # Headers
    center_text(
        "PRESIDENT ROXAS PROVINCIAL COMMUNITY HOSPITAL",
        height - 1 * inch,
        font_size=12,
        is_bold=True,
    )
    center_text("New Cebu . Pres. Roxas . Cotabato.", height - 1.3 * inch, font_size=12)
    center_text("LABORATORY DEPARTMENT", height - 1.6 * inch, font_size=12, is_bold=True)
    center_text("CROSS MATCHING RESULT", height - 2.2 * inch, font_size=14, is_bold=True)

    # Name and Date fields
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 2.8 * inch, "Name:")
    c.drawString(340, height - 2.8 * inch, "Date:")

    c.line(90, height - 2.85 * inch, 320, height - 2.85 * inch)  # Name line
    c.line(375, height - 2.85 * inch, 440, height - 2.85 * inch)  # Date line

    # Create table
    data = [
        ["Serial No.", "Blood Type", "Amt. In cc.", "Blood Bank", "Date of Collection", "Expiration Date", "Result"],
    ]
    # Add empty rows
    for _ in range(6):
        data.append(["", "", "", "", "", "", ""])

    table_style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ])

    # Calculate column widths (adjusted to match the image proportions)
    col_widths = [60, 70, 70, 80, 90, 90, 70]  # Adjusted widths
    table = Table(data, colWidths=col_widths, rowHeights=[30] * len(data))
    table.setStyle(table_style)

    # Position the table
    table_x = 40
    table_y = height - 6.0 * inch
    table.wrapOn(c, width, height)
    table.drawOn(c, table_x, table_y)

    def draw_centered_signature_line(c, y_position, text_name, text_license, text_role):
        line_width = 200
        x_line_start = (width - line_width) / 2
        x_line_end = x_line_start + line_width

        c.line(x_line_start, y_position, x_line_end, y_position)

        c.setFont("Helvetica-Bold", 10)
        text_name_width = c.stringWidth(text_name, "Helvetica-Bold", 10)
        c.drawString((width - text_name_width) / 2, y_position - 20, text_name)

        c.setFont("Helvetica", 10)
        text_license_width = c.stringWidth(text_license, "Helvetica", 10)
        c.drawString((width - text_license_width) / 2, y_position - 35, text_license)

        text_role_width = c.stringWidth(text_role, "Helvetica", 10)
        c.drawString((width - text_role_width) / 2, y_position - 50, text_role)

    # Draw signatures
    y_sig = height - 8.4 * inch
    draw_centered_signature_line(
        c, y_sig, "MARY JEAN L. BERNAS, MD", "Lic no. 113340", "Pathologist"
    )

    y_sig_bottom = y_sig - 80
    draw_centered_signature_line(
        c,
        y_sig_bottom,
        "CRIS L. JUNTARCIEGO, RMT",  # Updated name as per image
        "Lic no. 85982",
        "Medical Technologist"
    )

    c.save()

if __name__ == "__main__":
    create_lab_report(
        logo_path="C:/Users/Kian/Desktop/project 2024-2025/hospital_mgmt/static/assets/img/logo.jpg"
    )