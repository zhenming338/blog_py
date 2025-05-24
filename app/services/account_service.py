from dataclasses import asdict

from app.dao import account_dao
from flask_jwt_extended import create_access_token
from datetime import timedelta
from app.utils import encrypt_util
from app.exception.account_exceptions import (
    UserAccessInvalidException,
    UserNotFoundException,
)
from app.utils.encrypt_util import bcrypt_encode
from app.extensions import db

def login(data):
    print(data)
    username = data["username"]
    password = data["password"]
    email = data["email"]
    role_id = data["roleId"]
    print(email)
    user = account_dao.get_user_by_username(username)
    print(user)
    if user is None:
        raise UserNotFoundException("user is not exists")
    if not encrypt_util.bcrypt_check(password, user.password):
        raise UserAccessInvalidException("password is invalid")
    return create_access_token(identity=user.id, expires_delta=timedelta(hours=1))


def get_roles() -> list:
    roles = account_dao.get_roles()
    return [role.to_dict() for role in roles]


def register(data):
    username = data["username"]
    password = data["password"]
    data["password"] = bcrypt_encode(password)
    user_by_username = account_dao.get_user_by_username(username)
    if user_by_username is not None:
        raise UserAccessInvalidException("user is already registered")
    data["roleId"] = 1
    try:
        id = account_dao.add_user(data)

        account_dao.add_role_user_record(user_id=id, role_id=1)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e.__str__())
        raise UserAccessInvalidException(str(e))
