from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

def generate_pdf_invoice(email, package_name, package_price):
    buffer = BytesIO() 
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Styles
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    normal_style = styles["Normal"]

    # Title
    elements = []
    elements.append(Paragraph("Booking Confirmation Invoice", title_style))
    elements.append(Spacer(1, 20))  

    # Customer details
    customer_details = [
        ["Customer Email:", email],
        ["Package Name:", package_name],
        ["Package Price:", f"${package_price:.2f}"],
    ]
    table = Table(customer_details, hAlign="LEFT", colWidths=[150, 300])
    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ])
    )
    elements.append(table)
    elements.append(Spacer(1, 30))

    # Add invoice details section
    elements.append(Paragraph("Invoice Details", styles["Heading2"]))
    invoice_table_data = [
        ["Description", "Amount"],
        [package_name, f"${package_price:.2f}"],
        ["Total", f"${package_price:.2f}"]
    ]
    invoice_table = Table(invoice_table_data, hAlign="LEFT", colWidths=[400, 100])
    invoice_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 10),
        ])
    )
    elements.append(invoice_table)
    elements.append(Spacer(1, 50))

    # Footer
    footer = Paragraph(
        "This is a computer-generated invoice. No signature required.",
        styles["Italic"],
    )
    elements.append(footer)

    # Build the PDF
    doc.build(elements)
    buffer.seek(0) 
    return buffer

@shared_task
def send_booking_email(email, package_name, package_price):
    try:
        logger.info(f"Sending booking confirmation email to {email}.")

        pdf_buffer = generate_pdf_invoice(email, package_name, package_price)

        # Create the email
        subject = "Booking Confirmation"
        body = (
            f"Dear Customer,\n\n"
            f"Thank you for booking {package_name}.\n\n"
            f"Please find your invoice attached.\n\n"
            f"Best regards,\nTravel Agency"
        )
        email_message = EmailMessage(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [email],
        )

        # Attach the PDF
        email_message.attach(
            f"{package_name.replace(' ', '_')}_invoice.pdf",  
            pdf_buffer.getvalue(),  
            "application/pdf" 
        )
        pdf_buffer.close()

        # Send the email
        email_message.send(fail_silently=False)
        logger.info(f"Email with invoice sent successfully to {email}.")
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")
        raise
