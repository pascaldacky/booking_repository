from flask import Flask, request, render_template
import requests
from urllib.parse import quote, unquote

app = Flask(__name__)

# =========================
# POSTMARK CONFIG
# =========================
POSTMARK_API_KEY = "c8c0dbf4-c718-430f-bf8b-ec64937a1930"
FROM_EMAIL = "moffassa@travellers.co.tz"
ADMIN_EMAIL = "moffassa@travellers.co.tz"

POSTMARK_URL = "https://api.postmarkapp.com/email"
POSTMARK_HEADERS = {
    "X-Postmark-Server-Token": POSTMARK_API_KEY,
    "Accept": "application/json",
    "Content-Type": "application/json",
}


# =========================
# HELPER: SEND EMAIL
# =========================
def send_email(to, subject, html_body):
    response = requests.post(
        POSTMARK_URL,
        headers=POSTMARK_HEADERS,
        json={
            "From": FROM_EMAIL,
            "To": to,
            "Subject": subject,
            "HtmlBody": html_body,
        },
        timeout=10,
    )
    print("EMAIL STATUS:", response.status_code)
    print("EMAIL RESPONSE:", response.text)


# =========================
# HOME / BOOKING PAGE
# =========================
@app.route("/")
def index():
    return render_template("booking.html")


# =========================
# SUBMIT BOOKING (ADMIN EMAIL)
# =========================
@app.route("/submit_booking", methods=["POST"])
def submit_booking():
    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    email = request.form.get("email", "").strip()
    nationality = request.form.get("nationality", "").strip()
    phone = request.form.get("phone", "").strip()
    message = request.form.get("message", "").strip()

    safe_email = quote(email)

    confirm_link = (
        f"https://booking-repository-21.onrender.com/confirm-booking"
        f"?email={safe_email}&first_name={quote(first_name)}&last_name={quote(last_name)}"
    )

    banner = "https://moffassatravellers.co.tz/assets/img/sere1.webp"

    admin_body = f"""
    <html>
    <body style="font-family:Arial;">
      <h2>New Safari Booking</h2>
      <img src="{banner}" width="100%" style="border-radius:6px;">
      <p><b>Name:</b> {first_name} {last_name}</p>
      <p><b>Email:</b> {email}</p>
      <p><b>Nationality:</b> {nationality}</p>
      <p><b>Phone:</b> {phone}</p>
      <p><b>Message:</b> {message}</p>

      <br>
      <a href="{confirm_link}"
         style="display:inline-block;background:#28a745;color:#fff;
                padding:12px 20px;text-decoration:none;border-radius:5px;">
         ✅ Confirm Booking
      </a>
    </body>
    </html>
    """

    send_email(ADMIN_EMAIL, "New Safari Booking Request", admin_body)

    return render_template("success.html", first_name=first_name)


# =========================
# CONFIRM BOOKING (CUSTOMER EMAIL)
# =========================
@app.route("/confirm-booking")
def confirm_booking():
    email = unquote(request.args.get("email", ""))
    first_name = unquote(request.args.get("first_name", ""))
    last_name = unquote(request.args.get("last_name", ""))

    print("CONFIRMING BOOKING FOR:", email)

    banner = "https://moffassatravellers.co.tz/assets/img/sere1.webp"
    whatsapp_number = "255745224845"

    customer_body = f"""
    <html>
    <body style="font-family:Arial;background:#f4f4f4;padding:20px;">
      <table width="100%" align="center">
        <tr><td align="center">
          <table width="600" style="background:#fff;border-radius:8px;">
            <tr><td>
              <img src="{banner}" width="600">
            </td></tr>
            <tr><td style="padding:20px;">
              <h2>Hello {first_name} {last_name},</h2>
              <p>Your safari booking has been <b>successfully confirmed</b>.</p>
              <p>We will contact you shortly with full details.</p>

              <a href="https://wa.me/{whatsapp_number}"
                 style="display:inline-block;background:#25D366;color:#fff;
                        padding:12px 20px;text-decoration:none;border-radius:5px;">
                 📲 Chat on WhatsApp
              </a>
            </td></tr>
          </table>
        </td></tr>
      </table>
    </body>
    </html>
    """

    send_email(email, "🎉 Your Safari Booking is Confirmed", customer_body)

    return render_template("confirm_booking.html", customer_name=f"{first_name} {last_name}")


# =========================
# RUN APP (LOCAL)
# =========================
if __name__ == "__main__":
    app.run(debug=True)
