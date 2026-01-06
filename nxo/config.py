"""Configuration management for NXO."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""

    # AWS Configuration
    aws_region: str = "us-east-1"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None

    # AWS Bedrock Configuration
    bedrock_model_id: str = "anthropic.claude-v2"
    bedrock_endpoint_url: Optional[str] = None

    # AWS Neptune Configuration
    neptune_endpoint: Optional[str] = None
    neptune_port: int = 8182
    neptune_use_ssl: bool = True

    # Application Configuration
    app_name: str = "nxo"
    app_version: str = "0.1.0"
    log_level: str = "INFO"
    debug: bool = False

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = False

    # Graph Database Configuration
    graph_db_type: str = "neptune"  # Options: neptune, neo4j, in-memory
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: Optional[str] = None

    # Versioning Configuration
    enable_versioning: bool = True
    version_storage_type: str = "s3"  # Options: s3, local
    version_s3_bucket: Optional[str] = None

    # Audit Configuration
    enable_audit: bool = True
    audit_storage_type: str = "cloudwatch"  # Options: cloudwatch, s3, local
    audit_s3_bucket: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()

