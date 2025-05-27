import jwt
from flask import Flask, request, g
from flask_cors import CORS

from app.exception import *
from app.utils.jwt_util import JWTUtil
from .config import Config
from .exception.account_exceptions import UserAccessInvalidException
from .extensions import db, migrate, register_exception_handlers
from .routes.account_routes import account_dp
from .routes.user_routes import user_dp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)
    migrate.init_app(app, db)

    app.register_blueprint(user_dp, url_prefix="/api/users")
    app.register_blueprint(account_dp, url_prefix="/api/account")

    register_exception_handlers(app)

    @app.before_request
    def jwt_auth_filter():
        account_white_route = ["login", "register", "getRoles"]
        for route in account_white_route:
            if request.path.startswith("/api/account/" + route):
                return
        token = request.headers.get("Authorization")
        if not token:
            raise UserAccessInvalidException("token is required")
        try:
            print("start tot decode token")
            user_info = JWTUtil.decode_token(token)
            print(user_info)
            g.user_info = user_info
        except jwt.ExpiredSignatureError:
            raise UserAccessInvalidException("token is expired")
        except jwt.InvalidTokenError:
            raise UserAccessInvalidException("token is invalid")

    return app
