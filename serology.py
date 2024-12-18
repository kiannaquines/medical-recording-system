from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from PIL import Image

def create_lab_report(filename="serology.pdf", logo_path="logo.png"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
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

    center_text(
        "PRESIDENT ROXAS PROVINCIAL COMMUNITY HOSPITAL",
        height - 1 * inch,
        font_size=12,
        is_bold=True,
    )
    center_text("New Cebu . Pres. Roxas . Cotabato.", height - 1.3 * inch, font_size=12)
    center_text("LABORATORY DEPARTMENT", height - 1.6 * inch, font_size=12, is_bold=True)
    center_text("SEROLOGY", height - 2.1 * inch, font_size=14, is_bold=True)

    box_left = 40
    box_right = width - 40
    box_top = height - 2.5 * inch
    box_bottom = height - 6.4 * inch

    c.rect(box_left, box_bottom, box_right - box_left, box_top - box_bottom)

    c.setFont("Helvetica", 11)
    c.drawString(box_left + 15, box_top - 25, "Name:")
    c.drawString(box_left + 300, box_top - 25, "Date:")
    c.drawString(box_left + 450, box_top - 25, "Room:")

    c.line(box_left + 60, box_top - 25, box_left + 290, box_top - 25)
    c.line(box_left + 335, box_top - 25, box_left + 440, box_top - 25)
    c.line(box_left + 485, box_top - 25, box_right - 15, box_top - 25)

    table_top = box_top - 70
    table_left = box_left + 15
    table_right = box_right - 15
    table_width = table_right - table_left

    data = [
        ["TEST", "RESULT"],
        ["HBsAg DETERMINATION", ""],
        ["TYPHIDOT RAPID IgM TEST", ""],
        ["DENGUE RAPID TEST NS1 Ag", ""],
    ]

    table = Table(data, colWidths=[table_width / 2, table_width / 2], rowHeights=[30] + [45] * (len(data) - 1))

    style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ])

    table.setStyle(style)

    table.wrapOn(c, table_left, table_top - 200)
    table.drawOn(c, table_left, table_top - 150)


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

    y_sig = table_top - 200 - 80
    draw_centered_signature_line(
        c, y_sig, "MARY JEAN L. BERNAS, MD", "Lic no. 113340", "Pathologist"
    )

    y_sig_bottom = y_sig - 80
    draw_centered_signature_line(
        c,
        y_sig_bottom,
        "FLORA JEANNE A. IRLANDEZ, RMT",
        "Lic no. 85982",
        "Medical Technologist",
    )
    
    c.save()

if __name__ == "__main__":
    create_lab_report(
        logo_path="C:/Users/Kian/Desktop/project 2024-2025/hospital_mgmt/static/assets/img/logo.jpg"
    )