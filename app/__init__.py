from flask import Flask
from app.config import Config
from flask_jwt_extended import JWTManager
from flask_pydantic_spec import FlaskPydanticSpec

from flask_cors import CORS

from app.engine import engine, get_session  # SQLModel engine and session generator

# Create spec instance at module level to be imported by routes
spec = FlaskPydanticSpec("flaskblog-api", title="BlogPlatform API", version="1.0.0")

# Initialize JWTManager instance (to be initialized with app)
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)

    # Initialize JWT with Flask app
    jwt.init_app(app)

    # Import blueprints here to avoid circular imports
    from app.routes.auth import auth_bp
    from app.routes.post import post_bp
    from app.routes.category import category_bp
    from app.routes.comment import comment_bp

    # Register blueprints with the Flask app
    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(comment_bp)

    # Register OpenAPI spec AFTER blueprints are registered
    spec.register(app)

    return app
