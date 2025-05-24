from sqlalchemy import text
from app.extensions import db
from app.models.user import User
from typing import Optional
from app.models.role import Role


def get_roles() -> list:
    sql = text("select * from role")
    result = db.session.execute(sql)
    rows = result.mappings()
    roles = [Role.from_dict(row) for row in rows]
    return roles


def get_user_by_username(username) -> Optional[User]:
    sql = text("select * from user where username = :username")
    result = db.session.execute(sql, {"username": username})
    row = result.mappings().first()
    if row is None:
        return None
    user = User(**row)
    return user


def get_user_by_email(email) -> Optional[User]:
    sql = text("select * from user where email=:email")
    result = db.session.execute(sql, {"email": email})
    row = result.first()
    if row is None:
        return None
    user = User(**row)
    return user


def add_user(data) -> int:
    print(data)
    sql = text(
        "insert into user(username,password,email,enabled) values (:username,:password,:email,1)")
    result = db.session.execute(sql,
                                {"username": data["username"], "password": data["password"],
                                 "email": data['username'] + "@qq.com"})
    id = result.lastrowid
    return id


def add_role_user_record(user_id, role_id):
    sql = text("insert into user_role(role_id, user_id) values (:role_id, :user_id)")
    db.session.execute(sql, {"role_id": role_id, "user_id": user_id})
