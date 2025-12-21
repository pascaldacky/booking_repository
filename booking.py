from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
POSTMARK_API_KEY = "6945d30b-b3c9-4b49-a9ed-79898895acef"
FROM_EMAIL = "moffassa@travellers.co.tz"
TO_EMAIL = "moffassa@travellers.co.tz"


@app.route('/')
def index():
    return render_template('booking.html')

@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    # Get form data safely
    first_name = request.form.get('firstName', '')
    last_name = request.form.get('lastName', '')
    email = request.form.get('email', '')
    phone = request.form.get('phone', '')
    nationality = request.form.get('nationality', '')
    people = request.form.get('people', '')
    tour = request.form.get('tour', '')
    date = request.form.get('date', '')
    requests_text = request.form.get('requests', '')

    # Validate required fields
    if not first_name or not last_name or not email or not tour or not date:
        return "Please fill in all required fields.", 400

    # Admin email (HTML)
    html_admin = f"""
    <h2>New Booking Received</h2>
    <p><b>Name:</b> {first_name} {last_name}</p>
    <p><b>Email:</b> {email}</p>
    <p><b>Phone:</b> {phone}</p>
    <p><b>Nationality:</b> {nationality}</p>
    <p><b>People:</b> {people}</p>
    <p><b>Tour:</b> {tour}</p>
    <p><b>Date:</b> {date}</p>
    <p><b>Special Requests:</b> {requests_text}</p>
    """

    response_admin = requests.post(
        "https://api.postmarkapp.com/email",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Postmark-Server-Token": POSTMARK_API_KEY
        },
        json={
            "From": FROM_EMAIL,
            "To": ADMIN_EMAIL,
            "Subject": f"New Booking from {first_name} {last_name}",
            "HtmlBody": html_admin
        }
    )

    # User confirmation email (HTML)
    html_user = f"""
    <h2>Booking Confirmation</h2>
    <p>Hi {first_name},</p>
    <p>Thank you for booking your tour with us! Here are your booking details:</p>
    <ul>
        <li><b>Tour:</b> {tour}</li>
        <li><b>Date:</b> {date}</li>
        <li><b>People:</b> {people}</li>
        <li><b>Special Requests:</b> {requests_text}</li>
    </ul>
    <p>We will contact you soon with further details.</p>
    <p>Regards,<br>Travel Booking Team</p>
    """

    response_user = requests.post(
        "https://api.postmarkapp.com/email",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Postmark-Server-Token": POSTMARK_API_KEY
        },
        json={
            "From": FROM_EMAIL,
            "To": email,
            "Subject": "Booking Confirmation",
            "HtmlBody": html_user
        }
    )

    if response_admin.status_code != 200 or response_user.status_code != 200:
        return "Booking received but failed to send emails.", 500

    # Redirect to success page
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == "__main__":
    app.run(debug=True)
