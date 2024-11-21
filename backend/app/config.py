import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    MONGO_URI = os.getenv("MONGO_URI")
    DEBUG = os.getenv("FLASK_DEBUG", 0)
    TESTING = False


class DevelopmentConfig(Config):
    """Development-specific configuration."""
    DEBUG = True


class TestingConfig(Config):
    """Testing-specific configuration."""
    TESTING = True
    MONGO_URI = "mongodb://localhost:27017/air_quality_test"


class ProductionConfig(Config):
    """Production-specific configuration."""
    DEBUG = False
    TESTING = False

# Environment configuration mapping
config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
