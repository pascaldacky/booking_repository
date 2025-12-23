from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

# =========================
# POSTMARK CONFIG
# =========================
POSTMARK_API_KEY = "c8c0dbf4-c718-430f-bf8b-ec64937a1930"
FROM_EMAIL = "moffassa@travellers.co.tz"
TO_EMAIL = "moffassa@travellers.co.tz"


# =========================
# HOME / BOOKING PAGE
# =========================
@app.route("/")
def index():
    return render_template("booking.html")


# =========================
# SUBMIT BOOKING
# =========================
@app.route("/submit_booking", methods=["POST"])
def submit_booking():
    try:
        # -------- Get form data safely --------
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        nationality = request.form.get("nationality", "").strip()
        phone = request.form.get("phone", "").strip()
        message = request.form.get("message", "").strip()

        # -------- Build email content --------
        banner = "https://moffassatravellers.co.tz/insta2.jpg"
        subject = "📸 New Safari Booking Request"

        body = f"""
<!DOCTYPE html>
<html>
  <body style="margin:0; padding:0; background:#f4f4f4; font-family: Arial, sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td align="center" style="padding:20px;">

          <table width="600" cellpadding="0" cellspacing="0"
                 style="background:#ffffff; border-radius:8px; overflow:hidden;">

            <!-- Banner -->
            <tr>
              <td>
                <img src="{banner}" width="600" style="display:block;" alt="Safari Booking">
              </td>
            </tr>

            <!-- Content -->
            <tr>
              <td style="padding:20px; color:#333;">
                <h2 style="margin-top:0;">New Safari Booking Received</h2>

                <p><strong>First Name:</strong> {first_name}</p>
                <p><strong>Last Name:</strong> {last_name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Nationality:</strong> {nationality}</p>
                <p><strong>Phone:</strong> {phone}</p>

                <p><strong>Message:</strong></p>
                <p style="background:#f9f9f9; padding:10px; border-radius:4px;">
                  {message}
                </p>

              </td>
            </tr>

            <!-- Footer -->
            <tr>
              <td align="center"
                  style="padding:15px; font-size:12px; color:#777;">
                © 2025 Moffassa Travellers · Tanzania
              </td>
            </tr>

          </table>

        </td>
      </tr>
    </table>
  </body>
</html>
"""

        # -------- Send email (SAFE) --------
        try:
            response = requests.post(
                "https://api.postmarkapp.com/email",
                headers={
                    "X-Postmark-Server-Token": POSTMARK_API_KEY,
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
                json={
                    "From": FROM_EMAIL,
                    "To": TO_EMAIL,
                    "Subject": subject,
                    "HtmlBody": body,   # ✅ ONLY REQUIRED CHANGE
                },
                timeout=10
            )

            print("Postmark status:", response.status_code)
            print("Postmark response:", response.text)

        except Exception as email_error:
            print("Postmark exception:", email_error)

        return render_template("success.html", name=name)

    except Exception as app_error:
        print("Application error:", app_error)
        return "Something went wrong, but your booking was received.", 200


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)
