from app.dao import account_dao
from flask import g
from app.exception.account_exceptions import (
    UserAccessInvalidException,
    UserNotFoundException,
)
from app.extensions import db
from app.utils import encrypt_util
from app.utils.encrypt_util import bcrypt_encode
from app.utils.jwt_util import JWTUtil


def login(data):
    print(data)
    username = data["username"]
    password = data["password"]
    roleName = data["role"]
    user = account_dao.get_user_by_username(username)
    role = account_dao.get_role_by_name(roleName)
    print(user)
    if user is None:
        raise UserNotFoundException("user is not exists")
    if not encrypt_util.bcrypt_check(password, user.password):
        raise UserAccessInvalidException("password is invalid")
    return JWTUtil.generate_token({"id": user.id, "roleId": role.id})


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


def get_user_info():
    user_id = g.get("user_info", {}).get("id")
    user_info = account_dao.get_user_by_id(user_id)
    user_info.password = "**************"
    return user_info
