from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str 
    mongodb_db: str 
    jwt_secret: str
    jwt_algorithm: str 
    access_token_expire_minutes: int
    google_cloud_credentials_path: str
    gcs_bucket_name: str

    class Config:
        env_file = ".env"

settings = Settings()


