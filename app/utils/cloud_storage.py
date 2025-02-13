# utils/cloud_storage.py
import uuid

from fastapi import UploadFile
from google.cloud import storage

from app.config.settings import settings


async def upload_to_cloud(file: UploadFile) -> str:
    client = storage.Client.from_service_account_json(
        settings.google_cloud_credentials_path
    )
    bucket = client.bucket(settings.gcs_bucket_name)

    # Generate unique filename
    extension = file.filename.split(".")[-1]
    blob_name = f"products/{uuid.uuid4()}.{extension}"
    blob = bucket.blob(blob_name)

    # Upload using stream
    contents = await file.read()
    blob.upload_from_string(contents, content_type=file.content_type)

    return blob.public_url
