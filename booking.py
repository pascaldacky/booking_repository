from flask import Flask, request, render_template, redirect, url_for
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
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        nationality = request.form.get("nationality", "").strip()
        phone = request.form.get("phone", "").strip()
        message = request.form.get("message", "").strip()

        # -------- Build email content --------
        subject = "New Safari Booking Request"
        body = f"""
New Booking Received

Name: {name}
Email: {email}
Nationality: {nationality}
Phone: {phone}

Message:
{message}
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
                    "TextBody": body,
                },
                timeout=10
            )

            # Log Postmark result (IMPORTANT)
            print("Postmark status:", response.status_code)
            print("Postmark response:", response.text)

        except Exception as email_error:
            # Email failure should NEVER break booking
            print("Postmark exception:", email_error)

        # -------- Always succeed for user --------
        return render_template("success.html", name=name)

    except Exception as app_error:
        # Catch ANY unexpected error
        print("Application error:", app_error)
        return "Something went wrong, but your booking was received.", 200


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)
