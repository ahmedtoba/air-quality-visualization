import logging
from flask import request

logger = logging.getLogger(__name__)

def setup_logging_middleware(app):
    @app.before_request
    def log_request_info():
        logger.info(f"Request: {request.method} {request.url}")
        if request.method in ["POST", "PUT", "PATCH"] and request.content_type == "application/json":
            try:
                logger.info(f"Request Body: {request.json}")
            except Exception as e:
                logger.warning(f"Failed to parse JSON body: {e}")

    @app.after_request
    def log_response_info(response):
        logger.info(f"Response: {response.status_code}")
        return response
