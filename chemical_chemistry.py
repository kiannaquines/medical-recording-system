from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from PIL import Image


def create_lab_report(filename="lab_report.pdf", logo_path="logo.png"):
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

    def center_text(
        text, y_position, font_name="Helvetica", font_size=12, is_bold=False
    ):
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
    center_text("CLINICAL CHEMISTRY", height - 2.2 * inch, font_size=14, is_bold=True)

    box_left = 40
    box_right = width - 40
    box_top = height - 3.1 * inch
    box_bottom = height - 7.3 * inch

    c.setFont("Helvetica", 10)
    c.drawString(box_left, height - 2.8 * inch, "Name:")
    c.drawString(box_left + 300, height - 2.8 * inch, "Date:")
    c.drawString(box_right - 80, height - 2.8 * inch, "Room:")

    c.line(box_left + 50, height - 2.85 * inch, box_left + 280, height - 2.85 * inch)
    c.line(box_left + 335, height - 2.85 * inch, box_left + 400, height - 2.85 * inch)
    c.line(box_right - 45, height - 2.85 * inch, box_right, height - 2.85 * inch)

    c.rect(box_left, box_bottom, box_right - box_left, box_top - box_bottom)

    tests = [
        ("GLUCOSE", "mmol/l", "3.9-6.4 mmol/l"),
        ("CHOLESTEROL", "mmol/l", "4.12-5.36 mmol/l"),
        ("TRIGLYCERIDES", "mmol/l", "0.68-1.92 mmol/l"),
        ("HDL", "mmol/l", "0.90-2.10 mmol/l"),
        ("LDL", "mmol/l", "0.00-3.37 mmol/l"),
        ("CREATININE", "umol/l", "70-106 umol/l"),
        ("", "umol/l", "70-106 umol/l"),
        ("URIC ACID", "umol/l", "214-488 umol/l"),
        ("", "umol/l", "137-363 umol/l"),
        ("BUN", "mmol/L", "1.7-8.3 mmol/l"),
        ("SGPT", "u/l", ">40 u/l"),
        ("SGOT", "u/l", ">40 u/l"),
    ]

    y_start = height - 3.5 * inch
    line_height = 0.3 * inch

    for test in tests:
        c.drawString(box_left + 10, y_start, test[0])
        c.line(box_left + 160, y_start, box_left + 260, y_start)
        c.drawString(box_left + 270, y_start, test[1])
        c.drawString(box_left + 360, y_start, test[2])
        y_start -= line_height

    y_sig = height - 8.5 * inch

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

    y_sig = height - 8.4 * inch
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
