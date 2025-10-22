"""
Application configuration management using pydantic-settings.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    app_name: str = "Dota 2 Analytics API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Database Configuration
    database_url: str = "postgresql://dota_user:dota_password@localhost:5432/dota_db"
    
    # OpenDota API
    opendota_api_key: Optional[str] = None
    opendota_base_url: str = "https://api.opendota.com/api"
    
    # CORS Configuration
    cors_origins: list[str] = ["http://localhost:3000"]
    
    # Cache Configuration (in minutes)
    cache_ttl_hero_constants: int = 1440  # 24 hours
    cache_ttl_player_profile: int = 30    # 30 minutes
    cache_ttl_player_winloss: int = 60    # 1 hour
    cache_ttl_player_heroes: int = 120    # 2 hours
    cache_ttl_player_matches: int = 10    # 10 minutes
    cache_ttl_search_results: int = 5     # 5 minutes
    
    # Logging
    log_level: str = "INFO"
    
    # GitHub (if needed)
    github_token: Optional[str] = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Global settings instance
settings = Settings()
