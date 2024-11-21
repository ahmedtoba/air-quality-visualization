from flask import Flask, redirect
from flask_pymongo import PyMongo
from flasgger import Swagger
from app.config import config_map
from app.logging_config import setup_logger
from app.middlewares import register_middlewares
from app.routes import register_blueprints
from dotenv import load_dotenv
from app.services.data_service import seed_data
import logging
import sys

# Load environment variables
load_dotenv()

# Initialize MongoDB
mongo = PyMongo()

def create_app():
    # Set up logging
    setup_logger()
    logger = logging.getLogger(__name__)

    # Create Flask app
    app = Flask(__name__)

    # Load configuration based on environment
    env = app.config.get('FLASK_ENV', 'development')
    app.config.from_object(config_map[env])

    # Enable Swagger
    Swagger(app)

    # Initialize MongoDB
    try:
        mongo.init_app(app)
        # Test MongoDB connection
        mongo.cx.server_info()  # This checks the connection to MongoDB
        logger.info("Successfully connected to MongoDB.")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        sys.exit(1)  # Terminate the application if MongoDB connection fails

    # Register middlewares
    register_middlewares(app)

    # Register routes
    register_blueprints(app)

    # Redirect from base URL to Swagger docs
    @app.route('/')
    def redirect_to_docs():
        return redirect('/apidocs')
    
    # seed the database
    with app.app_context():
        seed_data()

    return app
