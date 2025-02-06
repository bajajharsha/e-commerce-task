import base64
import json
import os
from email.mime.text import MIMEText
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from typing import List
from app.config.settings import settings

class EmailUtils:
    def __init__(self):
        """Initialize Gmail API with service account."""
        self.SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
        self.service = self.authenticate()

    def authenticate(self):
        """Authenticate using service account JSON file."""
        key_path = settings.google_cloud_credentials_path
        creds = Credentials.from_service_account_file(key_path, scopes=self.SCOPES)
        return build("gmail", "v1", credentials=creds)

    def create_email(self, sender: str, recipients: List[str], subject: str, body: str) -> dict:
        """Create an email message."""
        message = MIMEText(body, "html")
        message["From"] = sender
        message["To"] = ", ".join(recipients)
        message["Subject"] = subject

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        return {"raw": raw_message}

    async def send_email(self, recipients: List[str], subject: str, body: str):
        """Send an email notification using the Gmail API."""
        try:
            sender_email = "harsha-storage@nodal-talon-449309-c2.iam.gserviceaccount.com"  # Must match the one added in Gmail settings
            email_msg = self.create_email(sender_email, recipients, subject, body)
            self.service.users().messages().send(userId="me", body=email_msg).execute()
            return {"message": "Email sent successfully"}
        except Exception as e:
            return {"error": str(e)}

    