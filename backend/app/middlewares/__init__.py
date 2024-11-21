from .logging_middleware import setup_logging_middleware
from .error_middleware import setup_error_handling_middleware

def register_middlewares(app):
    setup_logging_middleware(app)
    setup_error_handling_middleware(app)
    return
