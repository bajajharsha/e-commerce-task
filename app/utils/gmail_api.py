import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from app.config.settings import settings

async def send_email(email_draft: str, seller_email: str, admin_emails: list[str]):
    """Send an email using the Gmail API.
    
    Args:
        email_draft: The body content of the email
        seller_email: The seller's email address
        admin_emails: List of admin email addresses
    
    Returns:
        str: Success or error message
    """
    try:
        # Get service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            settings.google_cloud_credentials_path,
            scopes=[   
                'https://www.googleapis.com/auth/gmail.send',
                'https://www.googleapis.com/auth/gmail.readonly'
            ]
        )
        
        # Add domain-wide delegation
        delegated_credentials = credentials.with_subject(settings.gmail_delegate_email)
        
        # Build the Gmail service
        service = build('gmail', 'v1', credentials=delegated_credentials)
        
        # Create the email message
        message = MIMEText(email_draft)
        message['to'] = ', '.join([seller_email] + admin_emails)
        message['from'] = settings.gmail_delegate_email
        message['subject'] = "Urgent: Buyer Complaint Regarding Product Issue"
        
        # Encode the message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        body = {'raw': raw_message}
        
        # Send the email
        send_request = service.users().messages().send(
            userId=settings.gmail_delegate_email,
            body=body
        ).execute()
        
        return f"Email sent successfully. Message ID: {send_request.get('id', 'unknown')}"
        
    except Exception as e:
        error_message = f"Error sending email: {str(e)}"
        print(error_message)  # For logging
        return error_message