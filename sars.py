from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from PIL import Image

def create_lab_report(filename="sars_report.pdf", logo_path="image.png"):
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
            logo_path, 45, height - 1.9 * inch,
            width=desired_width, height=desired_height,
            preserveAspectRatio=True
        )
    except Exception as e:
        print(f"Could not load logo: {e}")

    # Helper to center text
    def center_text(text, y_position, font_name="Helvetica", font_size=12, is_bold=False):
        if is_bold:
            font_name += "-Bold"
        c.setFont(font_name, font_size)
        text_width = c.stringWidth(text, font_name, font_size)
        x_position = (width - text_width) / 2
        c.drawString(x_position, y_position, text)

    # Hospital Header
    center_text("PRESIDENT ROXAS PROVINCIAL COMMUNITY HOSPITAL", height - 1 * inch, font_size=13, is_bold=True)
    center_text("New Cebu . Pres. Roxas . Cotabato.", height - 1.3 * inch, font_size=13)
    center_text("LABORATORY DEPARTMENT", height - 1.6 * inch, font_size=13, is_bold=True)

    # Main Fields
    y_top = height - 2.3 * inch
    c.setFont("Helvetica", 12)

    # Add Date
    c.drawString(width - 190, y_top, "Date: 2024/13/12")

    # Name and Other Information
    c.drawString(50, y_top - 40, "Patient Name: Kian Jearard G. Naquines")
    c.drawString(50, y_top - 60, "Age: 23      Sex: Male")
    c.drawString(50, y_top - 80, "Req. Physician: James Bond Naquines")
    c.drawString(350, y_top - 60, "Room No: #23")
    c.drawString(350, y_top - 80, "Sample Type: Testing Type")
    c.drawString(50, y_top - 100, "Time of Collection: 7:34 AM")
    c.drawString(350, y_top - 100, "Date of Collection: 2024/13/12")

    # Section Title
    center_text("SARS COV-2 ANTIGEN DETECTION", y_top - 150, font_size=18, is_bold=True)

    # Test Table
    table_top = y_top - 170
    table_left = 100
    table_width = width - 2 * table_left
    row_height = 30

    # Table Headers
    c.setFont("Helvetica-Bold", 12)
    c.rect(table_left, table_top - row_height, table_width, row_height)
    c.drawString(table_left + 30, table_top - row_height + 10, "TEST")
    c.drawString(table_left + table_width / 2 + 30, table_top - row_height + 10, "RESULT")

    # Test Row
    c.setFont("Helvetica-Oblique", 10)
    c.rect(table_left, table_top - 2 * row_height, table_width, row_height)
    c.drawString(table_left + 30, table_top - 2 * row_height + 10, "SARS CoV-2 Antigen Detection")
    c.drawString(table_left + table_width / 2 + 30, table_top - 2 * row_height + 10, "(Wondfo™ COVID-19 Ag Rapid Test)")

    # Signatures
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

    y_sig = height - 6.4 * inch
    draw_signature_line(c, y_sig, "MARY JEAN L. BERNAS, MD", "113340", "Pathologist")
    draw_signature_line(c, y_sig - 80, "FLORA JEANNE A. IRLANDEZ", "85982", "Medical Technologist")

    c.save()


if __name__ == "__main__":
    create_lab_report("sars_cov2_report.pdf","C:/Users/Kian/Desktop/project 2024-2025/hospital_mgmt/static/assets/img/logo.jpg")
