from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from PIL import Image


def create_lab_report(filename="rbs.pdf", logo_path="logo.png"):
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

    center_text("PRESIDENT ROXAS PROVINCIAL COMMUNITY HOSPITAL", height - 1 * inch, font_size=13, is_bold=True)
    center_text("New Cebu . Pres. Roxas . Cotabato.", height - 1.3 * inch, font_size=13)
    center_text("LABORATORY DEPARTMENT", height - 1.6 * inch, font_size=13, is_bold=True)
    center_text("CLINICAL CHEMISTRY", height - 2.2 * inch, font_size=14, is_bold=True)
    center_text("RBS", height - 3.5 * inch, font_size=14, is_bold=True)

    box_left = 40
    box_right = width - 40
    box_top = height - 3.1 * inch
    box_bottom = height - 7.3 * inch

    c.setFont("Helvetica", 10)
    c.drawString(box_left, height - 2.8 * inch, "Name:")
    c.drawString(box_right - 80, height - 2.8 * inch, "Room:")
    c.line(box_left + 50, height - 2.85 * inch, box_left + 280, height - 2.85 * inch)
    c.line(box_right - 45, height - 2.85 * inch, box_right, height - 2.85 * inch)

    c.rect(box_left, box_bottom, box_right - box_left, box_top - box_bottom)

    table_top = box_top - 50
    table_left = box_left + 10
    table_width = box_right - box_left - 20
    row_height = 20
    col_widths = [table_width * 0.4, table_width * 0.3, table_width * 0.3]

    c.setFont("Helvetica-Bold", 10)
    headers = ["RESULTS (mmol/dl)", "DATE", "TIME"]
    for i, header in enumerate(headers):
        c.drawString(table_left + sum(col_widths[:i]) + 5, table_top - 15, header)

    num_rows = 6
    for i in range(num_rows + 1):
        y = table_top - (i * row_height)
        c.line(table_left, y, table_left + table_width, y)

    for i in range(len(col_widths) + 1):
        x = table_left + sum(col_widths[:i])
        c.line(x, table_top, x, table_top - (num_rows * row_height))

    def draw_signature_line(c, y_position, name, license, role):
        line_width = 200
        x_line_start = (width - line_width) / 2
        x_line_end = x_line_start + line_width
        c.line(x_line_start, y_position, x_line_end, y_position)

        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(width / 2, y_position - 20, name)

        c.setFont("Helvetica", 10)
        c.drawCentredString(width / 2, y_position - 35, f"Lic no. {license}")
        c.drawCentredString(width / 2, y_position - 50, role)

    y_sig = height - 8.4 * inch
    draw_signature_line(c, y_sig, "MARY JEAN L. BERNAS, MD", "113340", "Pathologist")
    draw_signature_line(c, y_sig - 80, "FLORA JEANNE A. IRLANDEZ", "85982", "Medical Technologist")

    c.save()


if __name__ == "__main__":
    create_lab_report(
        logo_path="C:/Users/Kian/Desktop/project 2024-2025/hospital_mgmt/static/assets/img/logo.jpg"
    )
