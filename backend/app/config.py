import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class Config:
    """Base configuration."""
    PROPAGATE_EXCEPTIONS = True
    TESTING = False

    # mongoDB 
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_HOST = os.getenv("MONGO_HOST")
    MONGO_PORT = int(os.getenv("MONGO_PORT"))
    MONGO_USERNAME = os.getenv("MONGO_USERNAME")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_AUTH_SOURCE = os.getenv("MONGO_AUTH_SOURCE")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

    # flask-smorest    
    API_TITLE = "Air Quality Data API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"


class DevelopmentConfig(Config):
    """Development-specific configuration."""
    DEBUG = True


# Environment configuration mapping
config_map = {
    "development": DevelopmentConfig
}
