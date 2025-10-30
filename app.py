from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    JWTManager(app)
    CORS(app)

    from routes.auth import auth_bp
    from routes.movies import movies_bp
    from routes.favorites import favorites_bp
    from routes.home import home_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(movies_bp, url_prefix='/api')
    app.register_blueprint(favorites_bp, url_prefix='/api/favorites')
    app.register_blueprint(home_bp)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
