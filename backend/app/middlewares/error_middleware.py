from flask import jsonify
from app.logging_config import logger

def setup_error_handling_middleware(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.error(f"Unhandled Exception: {e}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
