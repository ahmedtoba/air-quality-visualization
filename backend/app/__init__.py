from pathlib import Path
from flask import Flask, redirect
from flask_pymongo import PyMongo
from flask_smorest import Api
from app.config import config_map
from app.logging_config import setup_logger
from app.middlewares import register_middlewares
from app.routes import register_blueprints
from dotenv import load_dotenv
import sys

# Initialize MongoDB
mongo = PyMongo()

def create_app():
    # Set up logging
    setup_logger()

    # Create Flask app
    app = Flask(__name__)

    # Load configuration based on environment
    env = app.config.get('FLASK_ENV', 'development')
    app.config.from_object(config_map[env])

    # Register Flask-Smorest API
    api = Api(app)

    # Register middlewares
    register_middlewares(app)

    # Register routes
    register_blueprints(api)

    # Recognize app directory as a known module
    sys.path.append(str(Path(__file__).resolve().parent))

    @app.route('/')
    def index():
        return redirect('/swagger-ui')

    return app
