from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# =========================
# POSTMARK CONFIG
# =========================
POSTMARK_API_KEY = "c8c0dbf4-c718-430f-bf8b-ec64937a1930"
FROM_EMAIL = "moffassa@travellers.co.tz"
TO_EMAIL = "moffassa@travellers.co.tz"

# =========================
# HELPER FUNCTION TO SEND POSTMARK EMAIL
# =========================
def send_postmark_email(to_email, subject, html_body):
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
                "To": to_email,
                "Subject": subject,
                "HtmlBody": html_body,
            },
            timeout=10
        )
        print(f"Email sent to {to_email}: {response.status_code}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

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

        # -------- Image / WhatsApp config --------
        banner = "https://moffassatravellers.co.tz/assets/img/sere1.webp"
        whatsapp_number = "255745224845"  # Your number without '+'
        confirm_link = f"https://booking-repository-20.onrender.com/confirm-booking?email={email}&first_name={first_name}&last_name={last_name}"

        # =========================
        # ADMIN EMAIL
        # =========================
        admin_subject = "📸 New Safari Booking Request"
        admin_body = f"""
        <!DOCTYPE html>
        <html>
        <body style="margin:0; background:#f4f4f4; font-family:Arial, sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0">
        <tr><td align="center" style="padding:20px;">
        <table width="600" style="background:#fff; border-radius:8px; overflow:hidden;">
        <tr><td><img src="{banner}" width="600" style="display:block;"></td></tr>
        <tr><td style="padding:20px; color:#333;">
        <h2>New Safari Booking Received</h2>
        <p><strong>Name:</strong> {first_name} {last_name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Phone:</strong> {phone}</p>
        <p><strong>Nationality:</strong> {nationality}</p>
        <p><strong>Message:</strong><br>{message}</p>

        <!-- Buttons -->
        <a href="mailto:{email}" style="display:inline-block; margin-top:15px; background:#0a66c2; color:#fff; padding:12px 18px; text-decoration:none; border-radius:4px;">↩️ Reply to Customer</a>
        <br><br>
        <a href="{confirm_link}" style="display:inline-block; background:#198754; color:#fff; padding:14px 22px; text-decoration:none; border-radius:6px; font-weight:bold;">✅ Confirm Booking</a>

        </td></tr>
        <tr><td align="center" style="font-size:12px; color:#777; padding:15px;">© 2025 Moffassa Travellers · Tanzania</td></tr>
        </table></td></tr></table>
        </body></html>
        """
        send_postmark_email(TO_EMAIL, admin_subject, admin_body)

        # =========================
        # CUSTOMER INITIAL EMAIL
        # =========================
        customer_subject = "✅ Booking Received – Moffassa Travellers"
        customer_body = f"""
        <!DOCTYPE html>
        <html>
        <body style="margin:0; background:#f4f4f4; font-family:Arial, sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0">
        <tr><td align="center" style="padding:20px;">
        <table width="600" style="background:#fff; border-radius:8px; overflow:hidden;">
        <tr><td><img src="{banner}" width="600" style="display:block;"></td></tr>
        <tr><td style="padding:20px; color:#333;">
        <h2>Thank you, {first_name}!</h2>
        <p>Your safari booking request has been received successfully.</p>
        <p>Our team will contact you shortly with availability and pricing.</p>
        <a href="https://wa.me/{whatsapp_number}" style="display:inline-block; margin:15px 0; background:#25D366; color:#fff; padding:12px 20px; text-decoration:none; border-radius:4px;">📲 Chat on WhatsApp</a>
        <p style="margin-top:20px;">Warm regards,<br><b>Moffassa Travellers</b></p>
        </td></tr>
        <tr><td align="center" style="font-size:12px; color:#777; padding:15px;">© 2025 Moffassa Travellers · Tanzania</td></tr>
        </table></td></tr></table>
        </body></html>
        """
        send_postmark_email(email, customer_subject, customer_body)

        return render_template("success.html", first_name=first_name)

    except Exception as app_error:
        print("Application error:", app_error)
        return "Something went wrong, but your booking was received.", 200

# =========================
# CONFIRM BOOKING ROUTE
# =========================
@app.route("/confirm-booking")
def confirm_booking():
    email = request.args.get("email")
    first_name = request.args.get("first_name", "")
    last_name = request.args.get("last_name", "")
    customer_name = f"{first_name} {last_name}" if first_name else email

    # ------------------------
    # Send CONFIRMATION email to customer
    # ------------------------
    banner = "https://moffassatravellers.co.tz/assets/img/sere1.webp"
    whatsapp_number = "255745224845"

    confirm_email_subject = "🎉 Your Safari Booking is Confirmed!"
    confirm_email_body = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0; background:#f4f4f4; font-family:Arial, sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0">
    <tr><td align="center" style="padding:20px;">
    <table width="600" style="background:#fff; border-radius:8px; overflow:hidden;">
    <tr><td><img src="{banner}" width="600" style="display:block;"></td></tr>
    <tr><td style="padding:20px; color:#333;">
    <h2>Hi {customer_name},</h2>
    <p>Your safari booking has been <strong>confirmed</strong> successfully!</p>
    <p>Our team will contact you shortly for further details.</p>
    <a href="https://wa.me/{whatsapp_number}" style="display:inline-block; margin:15px 0; background:#25D366; color:#fff; padding:12px 20px; text-decoration:none; border-radius:4px;">📲 Chat on WhatsApp</a>
    <p style="margin-top:20px;">Warm regards,<br><b>Moffassa Travellers</b></p>
    </td></tr>
    <tr><td align="center" style="font-size:12px; color:#777; padding:15px;">© 2025 Moffassa Travellers · Tanzania</td></tr>
    </table></td></tr></table>
    </body></html>
    """
    send_postmark_email(email, confirm_email_subject, confirm_email_body)

    # ------------------------
    # Render admin confirmation page
    # ------------------------
    return render_template("confirm_booking.html", customer_name=customer_name)

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)
