from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from PIL import Image


def create_hematology_report(filename="hematology_report.pdf", logo_path="logo.png"):
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

    center_text("PRESIDENT ROXAS PROVINCIAL COMMUNITY HOSPITAL", height - 1 * inch, font_size=13, is_bold=True)
    center_text("New Cebu . Pres. Roxas . Cotabato.", height - 1.3 * inch, font_size=13)
    center_text("LABORATORY DEPARTMENT", height - 1.6 * inch, font_size=13, is_bold=True)

    info_top = height - 2.5 * inch
    c.setFont("Helvetica", 10)
    c.drawString(55, 600, "Name:")
    c.drawString(305, 600, "Date:")
    c.drawString(455, 600, "Room:")

    c.rect(50, info_top - 20, width - 100, 25)
    c.line(300, info_top - 20, 300, info_top + 5)
    c.line(450, info_top - 20, 450, info_top + 5)
    table_top = info_top - 45
    table_height = 250
    col_width = 180

    def draw_cell(left, top, width, height):
        c.rect(left, top, width, height)

    current_y = table_top
    left_x = 50

    cell_height = 60
    draw_cell(left_x, current_y - cell_height, col_width, cell_height)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_x + 5, current_y - 15, "Hemoglobin Mass Concentration")
    c.setFont("Helvetica", 10)
    c.drawString(left_x + 30, current_y - 35, "Female (120-160)gm/L")
    c.drawString(left_x + 30, current_y - 55, "Male   (140-180)gm/L")

    draw_cell(left_x + col_width, current_y - cell_height, 70, cell_height)
    current_y -= cell_height

    cell_height = 60
    draw_cell(left_x, current_y - cell_height, col_width, cell_height)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_x + 5, current_y - 15, "Hematocrit")
    c.setFont("Helvetica", 10)
    c.drawString(left_x + 30, current_y - 35, "Female (0.37-0.45)")
    c.drawString(left_x + 30, current_y - 55, "Male   (0.40-0.48)")

    draw_cell(left_x + col_width, current_y - cell_height, 70, cell_height)
    current_y -= cell_height

    cell_height = 60
    draw_cell(left_x, current_y - cell_height, col_width, cell_height)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_x + 5, current_y - 15, "Erythrocyte No. Concentration")
    c.setFont("Helvetica", 10)
    c.drawString(left_x + 30, current_y - 35, "Female (4.0-4.5)x10 12/L")
    c.drawString(left_x + 30, current_y - 55, "Male   (4.5-5.0)x10 12/L")

    draw_cell(left_x + col_width, current_y - cell_height, 70, cell_height)
    current_y -= cell_height

    cell_height = 40
    draw_cell(left_x, current_y - cell_height, col_width, cell_height)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_x + 5, current_y - 15, "Platelet")
    c.setFont("Helvetica", 10)
    c.drawString(left_x + 30, current_y - 35, "No. Conc. (150-350)x10 9/L")

    draw_cell(left_x + col_width, current_y - cell_height, 70, cell_height)
    current_y -= cell_height

    cell_height = 30

    draw_cell(left_x, current_y - cell_height, 250, cell_height)
    draw_cell(left_x + 2 * 125, current_y - cell_height, 261, cell_height)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_x + 5, current_y - 20, "Blood Type:")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_x + 2 * 125 + 5, current_y - 20, "Rh Type:")

    right_x = left_x + col_width + 70
    current_y = table_top
    right_col_width = col_width - 32

    cell_height = 40
    draw_cell(right_x, current_y - cell_height, right_col_width, cell_height)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(right_x + 5, current_y - 15, "Leucocyte No Concentration")
    c.setFont("Helvetica", 10)
    c.drawString(right_x + 5, current_y - 35, "WBC count (5-10)x 10 9/L")

    draw_cell(right_x + right_col_width, current_y - cell_height, 113, cell_height)
    current_y -= cell_height

    sections = [
        ("Segmenters", "(0.55-0.65)", 30),
        ("Lymphocytes", "(0.25-0.40)", 30),
        ("Monocytes", "(0.01-0.06)", 30),
        ("Eosinophils", "(0.01-0.05)", 30),
        ("Basophils", "(0-0.005)", 30),
        ("Others:", "", 30),
    ]

    for title, range_text, height in sections:
        draw_cell(right_x, current_y - height, right_col_width, height)
        draw_cell(right_x + right_col_width, current_y - height, 113, height)

        if title == "Others:":
            c.setFont("Helvetica-Bold", 10)
            c.drawString(right_x + 5, current_y - 20, title)
        else:
            c.setFont("Helvetica-Bold", 10)
            c.drawString(right_x + 5, current_y - 20, title)
            c.setFont("Helvetica", 10)
            c.drawString(right_x + right_col_width - 70, current_y - 20, range_text)

        current_y -= height

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

    y_sig = table_top - table_height - 80
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
    create_hematology_report(
        logo_path="C:/Users/Kian/Desktop/project 2024-2025/hospital_mgmt/static/assets/img/logo.jpg"
    )
