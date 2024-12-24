from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from core.settings import LOGO_PATH
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from PIL import Image


def chemical_chemistry(filename="chemical_chemistry.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    try:
        img = Image.open(LOGO_PATH)
        img_width, img_height = img.size
        aspect = img_height / float(img_width)

        desired_width = 1.3 * inch
        desired_height = desired_width * aspect

        c.drawImage(
            LOGO_PATH,
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
    center_text(
        "LABORATORY DEPARTMENT", height - 1.6 * inch, font_size=12, is_bold=True
    )
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


def create_hematology_report(filename="hematology_report.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    try:
        img = Image.open(LOGO_PATH)
        img_width, img_height = img.size
        aspect = img_height / float(img_width)
        desired_width = 1.3 * inch
        desired_height = desired_width * aspect
        c.drawImage(
            LOGO_PATH,
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
        font_size=13,
        is_bold=True,
    )
    center_text("New Cebu . Pres. Roxas . Cotabato.", height - 1.3 * inch, font_size=13)
    center_text(
        "LABORATORY DEPARTMENT", height - 1.6 * inch, font_size=13, is_bold=True
    )

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


def cross_matching(filename="cross-matching.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    try:
        img = Image.open(LOGO_PATH)
        img_width, img_height = img.size
        aspect = img_height / float(img_width)
        desired_width = 1.3 * inch
        desired_height = desired_width * aspect
        c.drawImage(
            LOGO_PATH,
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
    center_text(
        "LABORATORY DEPARTMENT", height - 1.6 * inch, font_size=12, is_bold=True
    )
    center_text(
        "CROSS MATCHING RESULT", height - 2.2 * inch, font_size=14, is_bold=True
    )

    c.setFont("Helvetica", 10)
    c.drawString(40, height - 2.8 * inch, "Name:")
    c.drawString(340, height - 2.8 * inch, "Date:")

    c.line(90, height - 2.85 * inch, 320, height - 2.85 * inch)
    c.line(375, height - 2.85 * inch, 440, height - 2.85 * inch)

    data = [
        [
            "Serial No.",
            "Blood Type",
            "Amt. In cc.",
            "Blood Bank",
            "Date of Collection",
            "Expiration Date",
            "Result",
        ],
    ]

    for _ in range(6):
        data.append(["", "", "", "", "", "", ""])

    table_style = TableStyle(
        [
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]
    )

    col_widths = [60, 70, 70, 80, 90, 90, 70]
    table = Table(data, colWidths=col_widths, rowHeights=[30] * len(data))
    table.setStyle(table_style)

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

    y_sig = height - 8.4 * inch
    draw_centered_signature_line(
        c, y_sig, "MARY JEAN L. BERNAS, MD", "Lic no. 113340", "Pathologist"
    )

    y_sig_bottom = y_sig - 80
    draw_centered_signature_line(
        c,
        y_sig_bottom,
        "CRIS L. JUNTARCIEGO, RMT",
        "Lic no. 85982",
        "Medical Technologist",
    )

    c.save()


def sars_report(filename="sars_report.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    try:
        img = Image.open(LOGO_PATH)
        img_width, img_height = img.size
        aspect = img_height / float(img_width)
        desired_width = 1.3 * inch
        desired_height = desired_width * aspect

        c.drawImage(
            LOGO_PATH,
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
        font_size=13,
        is_bold=True,
    )
    center_text("New Cebu . Pres. Roxas . Cotabato.", height - 1.3 * inch, font_size=13)
    center_text(
        "LABORATORY DEPARTMENT", height - 1.6 * inch, font_size=13, is_bold=True
    )

    y_top = height - 2.3 * inch
    c.setFont("Helvetica", 12)

    c.drawString(width - 190, y_top, "Date: 2024/13/12")

    c.drawString(50, y_top - 40, "Patient Name: Kian Jearard G. Naquines")
    c.drawString(50, y_top - 60, "Age: 23      Sex: Male")
    c.drawString(50, y_top - 80, "Req. Physician: James Bond Naquines")
    c.drawString(350, y_top - 60, "Room No: #23")
    c.drawString(350, y_top - 80, "Sample Type: Testing Type")
    c.drawString(50, y_top - 100, "Time of Collection: 7:34 AM")
    c.drawString(350, y_top - 100, "Date of Collection: 2024/13/12")

    center_text("SARS COV-2 ANTIGEN DETECTION", y_top - 150, font_size=18, is_bold=True)

    table_top = y_top - 170
    table_left = 100
    table_width = width - 2 * table_left
    row_height = 30

    c.setFont("Helvetica-Bold", 12)
    c.rect(table_left, table_top - row_height, table_width, row_height)
    c.drawString(table_left + 30, table_top - row_height + 10, "TEST")
    c.drawString(
        table_left + table_width / 2 + 30, table_top - row_height + 10, "RESULT"
    )

    c.setFont("Helvetica-Oblique", 10)
    c.rect(table_left, table_top - 2 * row_height, table_width, row_height)
    c.drawString(
        table_left + 30, table_top - 2 * row_height + 10, "SARS CoV-2 Antigen Detection"
    )
    c.drawString(
        table_left + table_width / 2 + 30,
        table_top - 2 * row_height + 10,
        "(Wondfo™ COVID-19 Ag Rapid Test)",
    )

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
    draw_signature_line(
        c, y_sig - 80, "FLORA JEANNE A. IRLANDEZ", "85982", "Medical Technologist"
    )

    c.save()


def serology_report(filename="serology.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    try:
        img = Image.open(LOGO_PATH)
        img_width, img_height = img.size
        aspect = img_height / float(img_width)
        desired_width = 1.3 * inch
        desired_height = desired_width * aspect
        c.drawImage(
            LOGO_PATH,
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
    center_text(
        "LABORATORY DEPARTMENT", height - 1.6 * inch, font_size=12, is_bold=True
    )
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

    table = Table(
        data,
        colWidths=[table_width / 2, table_width / 2],
        rowHeights=[30] + [45] * (len(data) - 1),
    )

    style = TableStyle(
        [
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.white),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 11),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]
    )

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


def create_rbs_report(filename="rbs.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    try:
        img = Image.open(LOGO_PATH)
        img_width, img_height = img.size
        aspect = img_height / float(img_width)

        desired_width = 1.3 * inch
        desired_height = desired_width * aspect

        c.drawImage(
            LOGO_PATH,
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
        font_size=13,
        is_bold=True,
    )
    center_text("New Cebu . Pres. Roxas . Cotabato.", height - 1.3 * inch, font_size=13)
    center_text(
        "LABORATORY DEPARTMENT", height - 1.6 * inch, font_size=13, is_bold=True
    )
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
    draw_signature_line(
        c, y_sig - 80, "FLORA JEANNE A. IRLANDEZ", "85982", "Medical Technologist"
    )

    c.save()
