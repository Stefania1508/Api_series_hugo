from flask import Flask
from app.routes.series_routes import series_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(series_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)