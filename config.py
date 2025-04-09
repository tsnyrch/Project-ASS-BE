"""
Configuration settings for the ASS/NSS API.

This module provides a simpler, type-safe configuration system with environment-specific settings.
"""

import logging
import os
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Environment(str, Enum):
    """Environment types for the application."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


@dataclass
class AppConfig:
    """Application configuration with type-safe settings."""
    # Environment settings
    ENV: Environment = field(default_factory=lambda: Environment(
        os.environ.get("FLASK_ENV", "development").lower()
    ))
    DEBUG: bool = field(default_factory=lambda: 
                        os.environ.get("DEBUG", "True").lower() in ("true", "1", "yes") 
                        if os.environ.get("FLASK_ENV", "").lower() != "production" else False)
    TESTING: bool = field(default_factory=lambda: os.environ.get("FLASK_ENV", "").lower() == "testing")
    
    # Flask settings
    PORT: int = field(default_factory=lambda: int(os.environ.get("PORT", 5005)))
    HOST: str = field(default_factory=lambda: os.environ.get("HOST", "0.0.0.0"))
    
    # Camera settings
    DEFAULT_RGB_CAMERA_WIDTH: int = field(
        default_factory=lambda: int(os.environ.get("DEFAULT_RGB_CAMERA_WIDTH", 1920))
    )
    DEFAULT_RGB_CAMERA_HEIGHT: int = field(
        default_factory=lambda: int(os.environ.get("DEFAULT_RGB_CAMERA_HEIGHT", 1080))
    )
    DEFAULT_RGB_CAMERA_FORMAT: str = field(
        default_factory=lambda: os.environ.get("DEFAULT_RGB_CAMERA_FORMAT", "RGB8")
    )
    CAMERA_DEVICE: str = field(
        default_factory=lambda: os.environ.get("CAMERA_DEVICE", "/dev/null")
    )
    
    # Sensor settings
    DEFAULT_SENSOR_IP: str = field(
        default_factory=lambda: os.environ.get("DEFAULT_SENSOR_IP", "192.168.0.196")
    )
    DEFAULT_SENSOR_PORT: int = field(
        default_factory=lambda: int(os.environ.get("DEFAULT_SENSOR_PORT", 40999))
    )
    
    # Storage settings
    DEFAULT_STORAGE_PATH: str = field(
        default_factory=lambda: os.environ.get("DEFAULT_STORAGE_PATH", "./storage/")
    )
    
    # Logging settings
    LOG_LEVEL: str = field(
        default_factory=lambda: 
        os.environ.get("LOG_LEVEL", "DEBUG" if os.environ.get("FLASK_ENV", "").lower() != "production" else "WARNING")
    )
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # CORS settings
    CORS_ORIGINS: str = field(
        default_factory=lambda: os.environ.get("CORS_ORIGINS", "*")
    )
    
    # Only add development settings if in development mode
    FLASK_DEBUG_TB_ENABLED: bool = field(default_factory=lambda: 
                                        os.environ.get("FLASK_ENV", "").lower() != "production")
    FLASK_DEBUG_TB_INTERCEPT_REDIRECTS: bool = False
    
    # Only add testing settings if in testing mode
    TEST_DATA_PATH: str = field(default_factory=lambda: "./test_data/")
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        # Ensure environment is valid
        if self.ENV not in Environment:
            self.ENV = Environment.DEVELOPMENT
        
        # Ensure storage directory exists
        os.makedirs(self.DEFAULT_STORAGE_PATH, exist_ok=True)
        
        # If in testing mode, ensure test data directory exists
        if self.ENV == Environment.TESTING:
            os.makedirs(self.TEST_DATA_PATH, exist_ok=True)
    
    def get_log_level(self) -> int:
        """Convert string log level to logging module constant."""
        levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        return levels.get(self.LOG_LEVEL.upper(), logging.INFO)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return asdict(self)


# Create a global configuration instance
Config = AppConfig()