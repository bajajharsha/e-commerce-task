import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

async def send_complaint_email(user_id: str, order_id: str, product_id: str, issue_summary: str, image_url: str):
    # Gmail API logic to send the complaint email (you can integrate with Gmail API here)
    
    # For example, using SMTP to send an email
    sender_email = "your-email@gmail.com"
    receiver_emails = ["seller-email@example.com", "admin-email@example.com"]
    subject = "Urgent: Buyer Complaint Regarding Product Issue"
    
    body = f"""
    Hello Seller/Admin,
    
    A Buyer (User ID: {user_id}) has reported an issue with their order.
    
    Order ID: {order_id}
    Product ID: {product_id}
    Issue Summary: {issue_summary}
    Uploaded Image (if any): {image_url}
    
    Please review the complaint and take necessary action.
    
    Best Regards,
    Customer Support Team
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_emails)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, "your-email-password")
        server.sendmail(sender_email, receiver_emails, msg.as_string())
