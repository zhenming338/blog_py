from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.common.result import Result
from app.exception.account_exceptions import *

db = SQLAlchemy()
migrate = Migrate()


def register_exception_handlers(app):
    @app.errorhandler(UserNotFoundException)
    def handler_user_not_found(error):
        print(error)
        return Result.fail(str(error)).to_dict_json()

    @app.errorhandler(UserAccessInvalidException)
    def handler_user_access_invalid(error):
        print(error)
        return Result.fail(str(error)).to_dict_json()
