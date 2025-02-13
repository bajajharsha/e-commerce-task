from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str 
    mongodb_db: str 
    jwt_secret: str
    jwt_algorithm: str 
    access_token_expire_minutes: int
    google_cloud_credentials_path: str
    gcs_bucket_name: str
    google_gemini_api_key: str
    gmail_delegate_email: str

    class Config:
        env_file = ".env"

settings = Settings()


