from flask import Flask, request, render_template
import requests

app = Flask(__name__)

POSTMARK_API_KEY = "6945d30b-b3c9-4b49-a9ed-79898895acef"
FROM_EMAIL = "moffassa@travellers.co.tz"
TO_EMAIL = "moffassa@travellers.co.tz"

@app.route("/")
def booking_form():
    return render_template("booking.html")

@app.route("/submit_booking", methods=["POST"])
def submit_booking():
    name = request.form.get("name")
    email = request.form.get("email")
    message_text = request.form.get("message")
    
    # Save booking to file
    with open("bookings.txt", "a") as f:
        f.write(f"Name: {name}\nEmail: {email}\nMessage: {message_text}\n---\n")
    
    # Send email via Postmark
    url = "https://api.postmarkapp.com/email"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Postmark-Server-Token": POSTMARK_API_KEY
    }
    data = {
        "From": FROM_EMAIL,
        "To": TO_EMAIL,
        "Subject": f"New Booking from {name}",
        "TextBody": f"Name: {name}\nEmail: {email}\nMessage: {message_text}",
        "HtmlBody": f"<h3>New Booking</h3><p><b>Name:</b> {name}<br><b>Email:</b> {email}<br><b>Message:</b> {message_text}</p>"
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return "Booking submitted successfully! Check your company inbox."
    else:
        return f"Error sending booking: {response.status_code}, {response.text}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
