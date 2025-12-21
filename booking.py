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
    tour_package = request.form.get("tour_package")
    tour_duration = request.form.get("tour_duration")
    departure_date = request.form.get("daparture_date")
    return_date = request.form.get("return_date")
    adults = request.form.get("adults")
    children = request.form.get("children")
    infants = request.form.get("infants")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    nationality = request.form.get("nationality")
    dietary = request.form.get("dietary")
    special_requests = request.form.get("special_requests")
    travel_insurance = request.form.get("travel_insurance")
    airport_transfer = request.form.get("airport_transfer")
    extra_nights = request.form.get("extra_nights")
    local_guide = request.form.get("local_guide")
    payment_method = request.form.get("payment_method")
    card_name = request.form.get("card_name")
    card_number = request.form.get("card_number")
    card_cvv = request.form.get("card_cvv")
    card_expiry_month = request.form.get("card_expiry_month")
    card_expiry_year = request.form.get("card_expiry_year")
    terms_agreement = request.form.get("terms_agreement")    
    
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
        "TextBody": f"Name: {first_name}\nEmail: {last_name}\nMessage: {email}\ndeparture Date:{departure_date}",
        "HtmlBody": f"<h3>New Booking</h3><p><b>First Name:</b> {first_name}<br><b>Last Name:</b>{last_name}<br><b>Email:</b> {email}<br><b>Nationality:</b> {nationality}</p>"
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return "Booking submitted successfully! Check your company inbox."
    else:
        return f"Error sending booking: {response.status_code}, {response.text}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
