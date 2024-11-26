from app.routes.data_routes import blp as data_routes

def register_blueprints(app):
    app.register_blueprint(data_routes, url_prefix='/api/air-quality')
