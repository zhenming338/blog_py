from flask import Flask, request, jsonify, g
from flask_cors import CORS
from .config import Config
from .exception.account_exceptions import UserAccessInvalidException
from .extensions import db, migrate, register_exception_handlers
from .routes.user_routes import user_dp
from .routes.account_routes import account_dp
from flask_jwt_extended import JWTManager
from app.exception import *
import jwt
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(user_dp, url_prefix="/api/users")
    app.register_blueprint(account_dp, url_prefix="/api/account")

    register_exception_handlers(app)

    @app.before_request
    def jwt_auth_filter():
        if request.path.startswith("/api/users/login") or request.path.startswith(
                "/api/account"
        ):
            return
        token = request.headers.get("Authorization")
        if not token:
            raise UserAccessInvalidException("token is required")
        try:
            jwt.decode(token)


    return app
