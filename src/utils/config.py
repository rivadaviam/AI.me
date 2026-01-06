"""Configuration management"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""

    # AWS Configuration
    aws_region: str = Field(default="us-east-1", env="AWS_REGION")
    aws_access_key_id: Optional[str] = Field(default=None, env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = Field(
        default=None, env="AWS_SECRET_ACCESS_KEY"
    )

    # AWS Neptune
    neptune_endpoint: Optional[str] = Field(default=None, env="NEPTUNE_ENDPOINT")
    neptune_port: int = Field(default=8182, env="NEPTUNE_PORT")
    neptune_use_ssl: bool = Field(default=True, env="NEPTUNE_USE_SSL")

    # AWS Bedrock
    bedrock_model_id: str = Field(
        default="anthropic.claude-v2", env="BEDROCK_MODEL_ID"
    )
    bedrock_region: str = Field(default="us-east-1", env="BEDROCK_REGION")

    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_reload: bool = Field(default=True, env="API_RELOAD")

    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")

    # Security
    secret_key: str = Field(default="change-me", env="SECRET_KEY")
    api_key: Optional[str] = Field(default=None, env="API_KEY")

    # Feature Flags
    enable_versioning: bool = Field(default=True, env="ENABLE_VERSIONING")
    enable_audit_trail: bool = Field(default=True, env="ENABLE_AUDIT_TRAIL")
    enable_reasoning_engine: bool = Field(
        default=True, env="ENABLE_REASONING_ENGINE"
    )

    # Graph Processing
    max_graph_size: int = Field(default=100000, env="MAX_GRAPH_SIZE")
    graph_cache_ttl: int = Field(default=3600, env="GRAPH_CACHE_TTL")

    # LLM Configuration
    max_tokens: int = Field(default=4096, env="MAX_TOKENS")
    temperature: float = Field(default=0.7, env="TEMPERATURE")
    top_p: float = Field(default=0.9, env="TOP_P")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()

