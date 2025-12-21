from flask import Flask, render_template, request
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
    if not first_name or not last_name or not email:
        return "Please fill all required fields.", 400

    # Compose email
    subject = f"New Booking from {first_name} {last_name}"
    body = f"""
    Booking Details:
    Name: {first_name} {last_name}
    Email: {email}
    Phone: {phone}
    Nationality: {nationality}
    People: {people}
    Tour: {tour}
    Date: {date}
    Special Requests: {requests_text}
    """

    # Send email via Postmark API
    response = requests.post(
        "https://api.postmarkapp.com/email",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Postmark-Server-Token": POSTMARK_API_KEY
        },
        json={
            "From": FROM_EMAIL,
            "To": TO_EMAIL,
            "Subject": subject,
            "TextBody": body
        }
    )

    if response.status_code != 200:
        return "Booking received but failed to send email.", 500

    return f"Booking received for {first_name} {last_name}! Confirmation email sent."

if __name__ == "__main__":
    app.run(debug=True)
