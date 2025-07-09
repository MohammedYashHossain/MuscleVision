from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Supabase Configuration
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_ANON_KEY", "")
    
    # JWT Configuration
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # File Upload Configuration
    upload_dir: str = "static/session_outputs"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    
    # Model Configuration
    pose_model_path: str = "models/mmpose_hrnet_w48_coco_256x192"
    confidence_threshold: float = 0.5
    
    # API Configuration
    api_v1_str: str = "/api/v1"
    project_name: str = "MuscleVision"
    
    class Config:
        env_file = ".env"

settings = Settings() 