from app.routes.data_routes import data_bp

def register_blueprints(app):
    app.register_blueprint(data_bp, url_prefix='/api')
