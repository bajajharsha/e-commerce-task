import base64
import os
import pickle
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, List

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


async def get_gmail_service():
    """Gets valid user credentials from storage and creates Gmail service."""
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # For desktop applications, we use a simpler flow
            flow = InstalledAppFlow.from_client_secrets_file(
                "/Users/harshabajaj/Desktop/e-commerce/gmail.json", SCOPES
            )
            # This will open the default browser for authentication
            creds = flow.run_local_server(
                port=0
            )  # port=0 means pick any available port

        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)


async def send_email(
    email_draft: str, seller_email: str, admin_emails: List[str]
) -> Dict[str, Any]:
    """
    Send email to seller and admins using Gmail API
    """
    try:
        service = await get_gmail_service()

        message = MIMEMultipart()
        message["to"] = seller_email
        message["cc"] = ", ".join(admin_emails)
        message["subject"] = "Urgent: Buyer Complaint Regarding Product Issue"
        message["from"] = "me"

        body = MIMEText(email_draft)
        message.attach(body)

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}

        send_message = (
            service.users().messages().send(userId="me", body=create_message).execute()
        )

        return {
            "success": True,
            "message_id": send_message["id"],
            "thread_id": send_message["threadId"],
        }

    except Exception as error:
        print(f"Error details: {str(error)}")  # Added detailed error logging
        return {"success": False, "error": str(error)}
