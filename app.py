# ------------------------------------------------------------
# FINAL WORKING APP.PY – PAYMENT + QR + EMAIL + RECEIPT
# ------------------------------------------------------------

from flask import Flask, request, redirect, render_template, send_from_directory
import os
import datetime
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import traceback

# FIX reportlab md5 error for Python 3.8
import hashlib
hashlib.md5 = lambda *args, **kwargs: hashlib._hashlib.openssl_md5()

# UTIL MODULES
from utils.detection_utils import run_detection
from utils.ocr_utils import extract_plate, extract_text_violations
from utils.csv_utils import append_violation_row, load_csv
from utils.overlay_utils import create_proof_image

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

import base64
from io import BytesIO

def render_fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

# EMAIL

from reportlab.pdfgen import canvas



import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

EMAIL_SENDER = "iampallavivasanth77@gmail.com"
EMAIL_PASSWORD = "prcw mmvb nauj kzfi"  # GOOGLE APP PASSWORD

# PDF + QR
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import qrcode

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_receipt_email(to_email, row, pdf_path, index):
    try:
        sender = "iampallavivasanth77@gmail.com"
        password = "prcw mmvb nauj kzfi"

        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = to_email
        msg["Subject"] = "Traffic Violation Receipt"

        html = """
        <h3>Your Payment Receipt</h3>
        <p>Please find the attached PDF receipt.</p>
        """
        msg.attach(MIMEText(html, "html"))

        # Attach PDF
        with open(pdf_path, "rb") as f:
            attach = MIMEApplication(f.read(), _subtype="pdf")
        attach.add_header(
            "Content-Disposition",
            "attachment",
            filename=f"receipt.pdf"
        )
        msg.attach(attach)

        # Send email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, to_email, msg.as_string())
        server.quit()

        print("Email sent successfully with PDF!")

    except Exception as e:
        print("EMAIL ERROR:", e)



from flask import send_from_directory

VIOLATION_IMAGE_MAP = {
    "DrivingUsingMobile": "DrivingUsingMobile.png",
    "Overspeeding": "Overspeeding.png",
    "Overloading": "Overloading.png",
    "SignalJump": "SignalJump.png",
    "TripleRide": "TripleRide.png",
    "WrongLane": "WrongLane.png",
    "BikeWrongLane": "BikeWrongLane.png",
    "SingleJumpandRidingWithoutHelmet": "SingleJumpandRidingWithoutHelmet.png",
    "NoParking": "NoParking.png"
}


# ------------------------------------------------------------
# FLASK CONFIG
# ------------------------------------------------------------
app = Flask(__name__)

from flask import send_from_directory

@app.route('/data/images_data/<path:filename>')
def images_data_route(filename):
    return send_from_directory('data/images_data', filename)

@app.route('/data/proof_images/<path:filename>')
def proof_images_route(filename):
    return send_from_directory('data/proof_images', filename)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response

# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_PATH, "data")
CSV_PATH = os.path.join(DATASET_PATH, "main_dataset.csv")
IMG_PATH = os.path.join(DATASET_PATH, "images")
IMG_DATA_PATH = os.path.join(DATASET_PATH, "images_data")
PROOF_PATH = os.path.join(DATASET_PATH, "proof_images")
QR_PATH = os.path.join(DATASET_PATH, "payment_qr")

# Ensure folders exist
os.makedirs(DATASET_PATH, exist_ok=True)
os.makedirs(IMG_PATH, exist_ok=True)
os.makedirs(IMG_DATA_PATH, exist_ok=True)
os.makedirs(PROOF_PATH, exist_ok=True)
os.makedirs(QR_PATH, exist_ok=True)

# ------------------------------------------------------------
# PDF RECEIPT GENERATOR
# ------------------------------------------------------------
# ------------------------------------------------------------
# PDF RECEIPT GENERATOR (VioTrack Official - Dark Blue + Logo + Seal)
# ------------------------------------------------------------
def generate_receipt_pdf(row, pdf_path, index):
    import random
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm

    # Basic values from row (safe fallbacks)
    name = row.get("name") or random.choice([
        "Gowrav Shetty",
        "Gagan Gowda",
        "Nuthan Sharma",
        "Rahul Verma",
        "John Doe"
    ])

    email = row.get("email", "")
    address = row.get("address", row.get("location", row.get("area", "")))
    phone = row.get("phone", "9123456780")  # default phone as requested

    violation = row.get("violation", "")
    fine_amount = row.get("fine_amount", row.get("amount", ""))
    date_of_violation = row.get("date_of_violation", row.get("date", ""))
    time_of_violation = row.get("time_of_violation", row.get("time", ""))
    status = row.get("status", "Paid")

    # Fix rupee symbol problems: ensure string shows Rs.
    def format_amount(a):
        if a is None:
            return ""
        s = str(a)
        s = s.replace("₹", "Rs. ").replace("INR", "Rs.")
        if "Rs." not in s and any(ch.isdigit() for ch in s):
            s = "Rs. " + s
        return s

    amount_text = format_amount(fine_amount)

    # Create canvas
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # ----------------------------------------------------------------
    # Header bar
    # ----------------------------------------------------------------
    header_height = 60
    dark_blue = colors.Color(0/255, 32/255, 96/255)
    c.setFillColor(dark_blue)
    c.rect(0, height - header_height, width, header_height, stroke=0, fill=1)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 38, "VioTrack – Payment Receipt")

    # ----------------------------------------------------------------
    # Top-right vector logo (fixed, no polyline)
    # ----------------------------------------------------------------
    logo_size = 60
    logo_x = width - 60 - 20
    logo_y = height - header_height + (header_height - logo_size) / 2

    # Outer dark-blue circle
    c.setFillColor(dark_blue)
    c.circle(logo_x + logo_size/2, logo_y + logo_size/2, logo_size/2, stroke=0, fill=1)

    # Inner white circle
    c.setFillColor(colors.white)
    c.circle(logo_x + logo_size/2, logo_y + logo_size/2, logo_size/2 - 6, stroke=0, fill=1)

    # Draw shield using a path (SUPPORTED)
    cx = logo_x + logo_size/2
    cy = logo_y + logo_size/2
    shield_w = 22
    shield_h = 26

    shield_path = c.beginPath()
    shield_path.moveTo(cx - shield_w/2, cy + shield_h/4)
    shield_path.lineTo(cx + shield_w/2, cy + shield_h/4)
    shield_path.lineTo(cx, cy - shield_h/2)
    shield_path.close()

    c.setFillColor(dark_blue)
    c.drawPath(shield_path, fill=1, stroke=0)

    # Traffic lights (3 vertical bars)
    c.setFillColor(dark_blue)
    c.setLineWidth(2)
    c.line(cx - 6, cy + 6, cx - 6, cy - 6)
    c.line(cx,     cy + 6, cx,     cy - 6)
    c.line(cx + 6, cy + 6, cx + 6, cy - 6)

    

    # ----------------------------------------------------------------
    # Main rounded box
    # ----------------------------------------------------------------
    left = 50
    right = width - 50
    top = height - 110
    bottom = 110
    c.setLineWidth(1)
    c.roundRect(left, bottom, right - left, top - bottom, 8, stroke=1, fill=0)

    # Vertical position cursor
    cursor_y = top - 20
    line_gap = 18

    # ----------------------------------------------------------------
    # CLIENT INFORMATION blue bar
    # ----------------------------------------------------------------
    client_bar_h = 24
    c.setFillColor(dark_blue)
    c.roundRect(left + 6, cursor_y - client_bar_h + 6, (right - left) - 12, client_bar_h, 4, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(left + 14, cursor_y - client_bar_h + 12, "CLIENT INFORMATION")
    cursor_y -= (client_bar_h + 10)

    # Client fields
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(left + 12, cursor_y, "Name:")
    c.setFont("Helvetica", 11)
    c.drawString(left + 100, cursor_y, name)
    cursor_y -= line_gap

    c.setFont("Helvetica-Bold", 11)
    c.drawString(left + 12, cursor_y, "Phone:")
    c.setFont("Helvetica", 11)
    c.drawString(left + 100, cursor_y, str(phone))
    cursor_y -= line_gap

    # Address (wrap if long)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(left + 12, cursor_y, "Address:")
    c.setFont("Helvetica", 11)
    addr_text = address or ""
    # simple wrap: break into ~70-char chunks
    def simple_wrap(text, max_chars=70):
        words = text.split()
        lines = []
        cur = ""
        for w in words:
            if len(cur) + len(w) + 1 <= max_chars:
                cur = (cur + " " + w).strip()
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    addr_lines = simple_wrap(addr_text, max_chars=60)
    for ln in addr_lines:
        c.drawString(left + 100, cursor_y, ln)
        cursor_y -= line_gap
    if not addr_lines:
        cursor_y -= line_gap / 2

    cursor_y -= 6  # spacing before next bar

    # ----------------------------------------------------------------
    # VIOLATION DETAILS blue bar
    # ----------------------------------------------------------------
    vio_bar_h = 24
    c.setFillColor(dark_blue)
    c.roundRect(left + 6, cursor_y - vio_bar_h + 6, (right - left) - 12, vio_bar_h, 4, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(left + 14, cursor_y - vio_bar_h + 12, "VIOLATION DETAILS")
    cursor_y -= (vio_bar_h + 10)

    # Violation rows (labels on left, values on right)
    label_x = left + 12
    value_x = left + 160

    def draw_label_value(lbl, val):
        nonlocal cursor_y
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(colors.black)
        c.drawString(label_x, cursor_y, lbl)
        c.setFont("Helvetica", 11)
        c.drawString(value_x, cursor_y, str(val))
        # grey divider under each
        c.setStrokeColor(colors.lightgrey)
        c.setLineWidth(0.5)
        c.line(left + 10, cursor_y - 6, right - 10, cursor_y - 6)
        c.setStrokeColor(colors.black)
        cursor_y -= 22

    draw_label_value("Receipt ID:", index)
    draw_label_value("Violation:", violation)
    draw_label_value("Fine Amount:", amount_text)
    draw_label_value("Date:", date_of_violation)
    draw_label_value("Time:", time_of_violation)
    draw_label_value("Status:", status)

    # ----------------------------------------------------------------
    # PAYMENT METHOD & TOTAL footer bar
    # ----------------------------------------------------------------
    cursor_y -= 6
    # Payment method stub (left)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(left + 12, cursor_y, "Payment Method:")
    c.setFont("Helvetica", 11)
    c.drawString(left + 140, cursor_y, row.get("payment_method", "Online"))

    # Total box (right)
    total_box_w = 160
    total_box_h = 36
    total_x = right - total_box_w - 10
    total_y = cursor_y - total_box_h + 10
    c.setFillColor(dark_blue)
    c.roundRect(total_x, total_y, total_box_w, total_box_h, 6, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(total_x + total_box_w - 12, total_y + total_box_h - 12, "TOTAL")
    c.setFont("Helvetica-Bold", 14)
    c.drawRightString(total_x + total_box_w - 12, total_y + 8, amount_text)

    # ----------------------------------------------------------------
    # Blue official seal (bottom-left)
    # ----------------------------------------------------------------
    seal_cx = left + 70
    seal_cy = bottom + 50
    seal_radius_outer = 40
    c.setLineWidth(1.2)
    c.setStrokeColor(dark_blue)
    c.circle(seal_cx, seal_cy, seal_radius_outer, stroke=1, fill=0)
    c.setStrokeColor(colors.lightblue)
    c.circle(seal_cx, seal_cy, seal_radius_outer - 6, stroke=1, fill=0)

    # Inner filled small circle
    c.setFillColor(dark_blue)
    c.circle(seal_cx, seal_cy, 10, stroke=0, fill=1)

    # Seal text (simple stacked)
    c.setFillColor(dark_blue)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(seal_cx, seal_cy + 26, "AUTHORIZED")
    c.drawCentredString(seal_cx, seal_cy - 26, "ENFORCEMENT")

    # centered small label
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(seal_cx, seal_cy - 2, "VioTrack")

    # ----------------------------------------------------------------
    # Footer note
    # ----------------------------------------------------------------
    c.setFillColor(colors.grey)
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(width / 2, 80, "This is an auto-generated receipt from VioTrack. Keep this for your records.")

    # Save
    c.save()


# ------------------------------------------------------------
# EMAIL SENDER – PAYMENT LINK
# ------------------------------------------------------------
def send_payment_email(to_email, violation, index):

    subject = f"Payment Request for Violation #{index}"
    pay_url = f"http://127.0.0.1:5000/pay_fine/{violation['index']}"

    html = f"""
    <html>
        <body>
            <h2>Traffic Violation Payment Notice</h2>
            <p>Your vehicle <b>{violation['vehicle_number']}</b> committed:</p>
            <p><b>{violation['violation_type']}</b></p>
            <p>Fine Amount: <b>₹{violation['fine_amount']}</b></p>

            <a href="{pay_url}"
               style="padding: 10px 20px; background:#007BFF; color:white;
               text-decoration:none; border-radius:5px;">
               Pay Fine
            </a>
        </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html, "html"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
    server.quit()


# ------------------------------------------------------------
# EMAIL WITH RECEIPT (AFTER PAYMENT)
# ------------------------------------------------------------
def send_receipt_email(to_email, row, pdf_path, index):
    try:
        sender = "iampallavivasanth77@gmail.com"
        password = "prcw mmvb nauj kzfi"

        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = to_email
        msg["Subject"] = f"Payment Receipt for Violation #{index}"

        html = """
        <h3>Your Payment Receipt</h3>
        <p>Thank you for your payment. Your receipt is attached below.</p>
        """
        msg.attach(MIMEText(html, "html"))

        # Attach the PDF
        with open(pdf_path, "rb") as f:
            attach = MIMEApplication(f.read(), _subtype="pdf")

        attach.add_header(
            "Content-Disposition",
            "attachment",
            filename=f"receipt_{index}.pdf"
        )
        msg.attach(attach)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, to_email, msg.as_string())
        server.quit()

        print("Email sent successfully with PDF!")

    except Exception as e:
        print("EMAIL ERROR:", e)


# ------------------------------------------------------------
# LOGIN & HOME
# ------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect("/home")
    return render_template("login.html")


@app.route("/home")
def home():
    return render_template("home.html")

# ------------------------------------------------------------
# UPLOAD & DETECTION
# ------------------------------------------------------------
@app.route("/upload", methods=["GET", "POST"])
def upload():
    try:
        if request.method == "POST":

            uploaded = request.files.get("image")
            if not uploaded or uploaded.filename == "":
                return "No image selected."

            image_name = uploaded.filename
            image_path = os.path.join(IMG_PATH, image_name)
            uploaded.save(image_path)

            # Create proof image
            proof_save_path = os.path.join(PROOF_PATH, f"proof_{image_name}")
            create_proof_image(image_path, proof_save_path)

            # Extract OCR + YOLO
            extract_text_violations(image_path)
            det_boxes, yolo_violation, fine = run_detection(image_path)
            plate_text, plate_conf = extract_plate(det_boxes, image_path)

            # ... earlier code in upload()
            now = datetime.datetime.now()  

            # collect email from the upload form (add this line)
            email = request.form.get("email", "").strip()


            # Append to dataset
            index = append_violation_row(
                CSV_PATH,
                plate_text,
                "Unknown",
                yolo_violation,
                fine,
                now.strftime("%Y-%m-%d"),
                now.strftime("%H:%M:%S"),
                "Bengaluru",
                "Pending",
                plate_conf,
                image_name,
                email
            )

            return redirect(f"/view_violation/{index}")

        return render_template("upload.html")

    except Exception:
        return f"<pre>{traceback.format_exc()}</pre>"

# ------------------------------------------------------------
# LOCATION MAP (Auto-fill based on image_name)
# ------------------------------------------------------------
LOCATION_MAP = {
    "BikeWrongLane.png": "J.C. Road, Bengaluru",
    "DrivingUsingMobile.png": "Richmond Road, Bengaluru",
    "NoParking.png": "Church Street, Bengaluru",
    "Overloading.png": "Kalantharakanatava",
    "Overspeeding.png": "Outer Ring Road, Bengaluru",
    "OverSpeeding2.png": "Outer Ring Road, Bengaluru",
    "SignalJump.png": "MG Road, Bengaluru",
    "SingleJumpandRidingWithoutHelmet.png": "MG Road, Bengaluru",
    "TripleRide.png": "Mysore Road, Bengaluru",
    "WrongLane.png": "Seshadri Road, Bengaluru"
}

# ------------------------------------------------------------
# VIEW VIOLATION (SHOW DETAILS + PROOF IMAGE)
# ------------------------------------------------------------
@app.route("/view_violation/<int:index>")
def view_violation(index):

    df = load_csv(CSV_PATH)

    # Fill missing values
    df = df.ffill().bfill().fillna("")

    if index not in df.index:
        return "Invalid ID"

    row = df.loc[index].copy()

    # Get image filename
    image_name = row.get("image_name", "")

    # AUTO-FILL LOCATION
    auto_location = LOCATION_MAP.get(image_name, row.get("location", "Bengaluru"))

    # Save auto-location
    row["location"] = auto_location
    df.loc[index, "location"] = auto_location
    df.to_csv(CSV_PATH, index=False)

    # Extract violation value
    violation_value = row.get("violation", "").strip()

    # FIXED: Use image if no mapped proof image exists
    proof_image = VIOLATION_IMAGE_MAP.get(violation_value, image_name)

    # Check if file exists in data/images_data
    proof_path = os.path.join("data", "images_data", proof_image)
    proof_exists = os.path.exists(proof_path)

    return render_template(
        "view_violation.html",
        ID=index,
        proof_image=proof_image,
        proof_exists=proof_exists,
        row=row
    )

# ------------------------------------------------------------
# SEND PAYMENT EMAIL ROUTE
# ------------------------------------------------------------
@app.route("/send_payment_email/<int:index>", methods=["POST"])
def send_payment_email_route(index):

    df = load_csv(CSV_PATH)

    if index not in df.index:
        return "Invalid ID"

    user_email = request.form.get("email")
    if not user_email:
        return "Email missing"

    # Save email to CSV
    df.loc[index, "Email"] = user_email
    df.to_csv(CSV_PATH, index=False)

    row = df.loc[index]

    violation = {
        "id": row["ID"],              # visible ID from CSV
        "index": index,               # INTERNAL row index used for routing
        "vehicle_number": row["vehicle_number"],
        "violation_type": row["violation"],
        "fine_amount": row["fine_amount"],
    }

    # Send email
    send_payment_email(user_email, violation, index)

    return redirect(f"/email_sent_success/{index}")


@app.route("/email_sent_success/<int:index>")
def email_sent_success(index):

    df = load_csv(CSV_PATH)
    email = df.loc[index].get("Email", "")

    return render_template("email_sent.html", email=email)

# ------------------------------------------------------------
# PAYMENT PAGE (UPI + CARD + NET BANKING)
# ------------------------------------------------------------
@app.route("/pay_fine/<int:index>")
def pay_fine_page(index):

    df = load_csv(CSV_PATH)
    if index not in df.index:
        return "Invalid ID"

    row = df.loc[index]

    # -----------------------------
    # Generate dynamic UPI QR code
    # -----------------------------
    amount = str(row["fine_amount"]).replace(".0", "")  # convert float → string safely

    upi_string = (
        f"upi://pay?"
        f"pa=pallavi@oksbi&"
        f"pn=Pallavi&"
        f"am={amount}&"
        f"cu=INR"
    )

    qr_filename = f"upi_{index}.png"
    qr_filepath = os.path.join(QR_PATH, qr_filename)
    qrcode.make(upi_string).save(qr_filepath)

    violation = {
        "id": row["ID"],
        "index": index,
        "vehicle_number": row["vehicle_number"],
        "violation_type": row["violation"],
        "fine_amount": amount,
        "qr_url": f"/qr/{qr_filename}"
    }

    return render_template("payment_page.html", violation=violation)


# Serve QR images
@app.route("/qr/<filename>")
def serve_qr(filename):
    return send_from_directory(QR_PATH, filename)


# ------------------------------------------------------------
# PDF RECEIPT GENERATOR (UPDATED WITH RANDOM RECEIPT NUMBER)
# ------------------------------------------------------------
import random



@app.route("/fake_pay_success/<int:index>")
def fake_payment_success(index):
    df = load_csv(CSV_PATH)

    # Validate index
    if index not in df.index:
        return "Invalid ID"

    # ensure no chained reference issues
    row = df.loc[index].copy()

    # Ensure ID column exists & fill it if missing
    if "ID" not in df.columns:
        df["ID"] = ""
    if pd.isna(row.get("ID")) or row.get("ID") == "":
        df.loc[index, "ID"] = index
        row["ID"] = index

    # Normalize email field name(s) and value
    email = ""
    possible_email_cols = ["Email", "email", "owner_email", "ownerEmail", "user_email"]

    for col in possible_email_cols:
        if col in df.columns:
            email = str(row.get(col, "")).strip()
            break

    # treat literal "nan" and empty as no-email  <-- FIXED INDENT
    if email.lower() == "nan" or email == "None":
        email = ""

    # Save back normalized email
    df.loc[index, "Email"] = email

    # Update status, payment datetime fields
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    now_time = now.strftime("%H:%M:%S")

    df.loc[index, "status"] = "Paid"
    df.loc[index, "payment_date"] = today
    df.loc[index, "payment_time"] = now_time

    # Save CSV
    df.to_csv(CSV_PATH, index=False)

    # Send receipt email IF email exists
    if email:
        # Build receipt folder path
        receipt_folder = "data/receipts"
        os.makedirs(receipt_folder, exist_ok=True)

        pdf_path = os.path.join(receipt_folder, f"receipt_{index}.pdf")

        # Generate PDF
        generate_receipt_pdf(row, pdf_path, index)

        # Send Email with PDF
        send_receipt_email(email, row, pdf_path, index)
    

    # Render success page
    return render_template(
        "payment_success.html",
        index=index,
        email=email,
        date=today,
        time=now_time,
        violation=row
    )





    # build a safe violation dict for template / receipt generation
    # make sure fine_amount is a clean number string (no trailing .0)
    fine_val = row.get("fine_amount", "")
    try:
        # handle numeric or string like '1500.0'
        fine_float = float(fine_val)
        if fine_float.is_integer():
            fine_str = str(int(fine_float))
        else:
            fine_str = str(fine_float)
    except Exception:
        fine_str = str(fine_val)

    violation = {
        "id": int(df.loc[index, "ID"]) if not pd.isna(df.loc[index, "ID"]) and df.loc[index, "ID"] != "" else index,
        "vehicle_number": str(row.get("vehicle_number", "")).strip(),
        "violation_type": str(row.get("violation", "")).strip(),
        "fine_amount": fine_str,
        "date": str(row.get("date_of_violation", today)),
        "time": str(row.get("time_of_violation", now_time)),
        "email": email
    }

    # ensure QR_PATH exists
    os.makedirs(QR_PATH, exist_ok=True)

    # Generate Receipt PDF (store in QR_PATH)
    receipt_filename = f"receipt_{violation['id']}.pdf"
    receipt_path = os.path.join(QR_PATH, receipt_filename)
    try:
        generate_receipt_pdf(violation, receipt_path)
    except Exception as e:
        # log but continue — template can still show info
        print("Receipt generation error:", e)

    # Send receipt via email (if provided)
    if violation["email"]:
        try:
            send_receipt_email(violation["email"], violation, receipt_path)
            email_sent = True
        except Exception as e:
            print("Email send error:", e)
            email_sent = False
    else:
        email_sent = False

    # Render payment success page, include whether a receipt was emailed
    return render_template(
        "payment_success.html",
        violation=violation,
        receipt_path=os.path.basename(receipt_path),
        receipt_exists=os.path.exists(receipt_path),
        email_sent=email_sent
    )

# ------------------------------------------------------------
# VIEW ALL VIOLATIONS (TABLE LIST)
# ------------------------------------------------------------
@app.route("/view_all")
def view_all():
    df = load_csv(CSV_PATH)

    # handle missing values
    df = df.ffill().bfill().fillna("")

    # convert to records for Jinja
    records = df.to_dict(orient="records")

    return render_template("view_all.html", data=records)

# ------------------------------------------------------------
# ANALYSIS
# ------------------------------------------------------------
@app.route("/analysis")
def analysis():
    df = load_csv(CSV_PATH)

    # Clean dataset
    df = df.ffill().bfill().fillna("")

    # --- 1. Violations count per type ---
    violation_counts = df["violation"].value_counts().to_dict()

    # --- 2. Total fine collected (Paid Only) ---
    if "status" in df.columns:
        paid_df = df[df["status"] == "Paid"]
    else:
        paid_df = df[df["status"].str.lower() == "paid"]

    total_collected = paid_df["fine_amount"].sum()

    # --- 3. Pending vs Paid ---
    status_counts = df["status"].value_counts().to_dict()

    # --- 4. Monthly trend ---
    df["date_of_violation"] = pd.to_datetime(df["date_of_violation"], errors="coerce")
    df["month"] = df["date_of_violation"].dt.strftime("%b %Y")

    monthly_counts = df["month"].value_counts().sort_index().to_dict()

    return render_template(
        "analysis.html",
        violation_counts=violation_counts,
        status_counts=status_counts,
        monthly_counts=monthly_counts,
        total_collected=total_collected
    )

# ------------------------------------------------------------
# ANALYSIS INDEX
# ------------------------------------------------------------
@app.route("/analysis")
def analysis_index():
    return render_template("analysis_index.html")


# Convert any chart to base64
def make_chart(chart_func):
    def wrapper():
        try:
            df = load_csv(CSV_PATH)

            fig = plt.figure(figsize=(10, 6))
            plt.clf()

            chart_func(df, plt)

            img = render_fig_to_base64(fig)
            return render_template("single_graph.html", graph=img)

        except Exception as e:
            print("ERROR:", e)
            return str(e)

    return wrapper


# ------------------------------------------------------------
# CHART FUNCTIONS
# ------------------------------------------------------------

def chart_violations_type(df, plt):
    plt.clf()
    df["violation"].value_counts().plot(kind="bar")
    plt.title("Violations by Type")
    plt.xlabel("Violation Type")
    plt.ylabel("Count")


def chart_status_pie(df, plt):
    plt.clf()
    df["status"].value_counts().plot(kind="pie", autopct="%1.1f%%")
    plt.title("Status Distribution")
    plt.ylabel("")


def chart_fine_hist(df, plt):
    plt.clf()
    df["fine_amount"].astype(float).plot(kind="hist", bins=15)
    plt.title("Fine Amount Distribution")
    plt.xlabel("Fine (₹)")


def chart_violations_time(df, plt):
    plt.clf()

    df["parsed_date"] = pd.to_datetime(df["date_of_violation"], errors="coerce")
    daily_counts = df["parsed_date"].dt.date.value_counts().sort_index()

    plt.fill_between(daily_counts.index, daily_counts.values, alpha=0.5)
    plt.plot(daily_counts.index, daily_counts.values, marker="o")

    plt.title("Violations Over Time (Area Chart)")
    plt.xlabel("Date")
    plt.ylabel("Number of Violations")
    plt.grid(True, linestyle="--", alpha=0.4)

    plt.xticks(rotation=45, ha="right")




def chart_violations_location(df, plt):
    plt.clf()

    # Count violations per location
    location_counts = df["location"].value_counts()

    # Prepare heatmap-like horizontal color graph
    plt.imshow([location_counts.values], aspect="auto")

    plt.yticks([])  # hide y axis labels (heatmap style)
    plt.xticks(range(len(location_counts.index)), location_counts.index, rotation=45, ha="right")

    plt.colorbar(label="Number of Violations")
    plt.title("Violation Density by Location (Heatmap)")


# ------------------------------------------------------------
# REGISTER ROUTES
# ------------------------------------------------------------
app.add_url_rule("/analysis/type", "analysis_type", make_chart(chart_violations_type))
app.add_url_rule("/analysis/status", "analysis_status", make_chart(chart_status_pie))
app.add_url_rule("/analysis/fine", "analysis_fine", make_chart(chart_fine_hist))
app.add_url_rule("/analysis/time", "analysis_time", make_chart(chart_violations_time))
app.add_url_rule("/analysis/location", "analysis_location", make_chart(chart_violations_location))

# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
