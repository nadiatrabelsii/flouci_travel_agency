# travel_app/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import requests
from bs4 import BeautifulSoup
import numpy as np
from weasyprint import HTML
from django.template.loader import render_to_string
import tempfile
import os

@shared_task
def send_booking_confirmation_email(to_email, booking_details):
    subject = "Booking Confirmation"
    message = f"Hello! Your booking details are: {booking_details}"
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        fail_silently=False
    )
    return f"Email sent to {to_email}"

@shared_task
def generate_pdf_invoice(booking_id):
    # Example: Using a Django template to render a PDF
    context = {'booking_id': booking_id, 'price': 1000}
    html_string = render_to_string('invoice_template.html', context)
    html = HTML(string=html_string)
    
    # Generate a temporary PDF file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
        html.write_pdf(pdf_file.name)
        file_path = pdf_file.name
    
    # In a real app, you might store this PDF path in a model or serve it to user
    return f"PDF invoice generated at {file_path}"

@shared_task
def scrape_latest_travel_news():
    url = "https://example.com/travel-news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Parse the news items...
    news_data = []
    # Example: Grab all article headings
    for heading in soup.find_all('h2'):
        news_data.append(heading.text.strip())
    # Save to DB if needed...
    return news_data

@shared_task
def calculate_recommendations(preferences):
    # Example: using numpy
    arr = np.array(preferences)
    # Some dummy math...
    score = arr.mean()
    recommendations = "We recommend a trip to the Bahamas!" if score > 5 else "Try a local weekend getaway!"
    return recommendations
