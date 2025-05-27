from flask import Blueprint, request, jsonify
from ..common.result import Result
from app.extensions import db
from sqlalchemy import text
from app.services import account_service
from dataclasses import asdict

account_dp = Blueprint("account", __name__)


@account_dp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    token = account_service.login(data)
    return Result.success("login success", {"token": token}).to_dict_json()


@account_dp.route("/getRoles", methods=["GET"])
def get_roles():
    dict_roles = account_service.get_roles()
    return Result.success("get success", dict_roles).to_dict_json()


@account_dp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    account_service.register(data)
    return Result.success("register success").to_dict_json()


@account_dp.route("/getUserInfo", methods=["GET"])
def get_user_info():
    user_info = account_service.get_user_info()
    return Result.success("get userInfo success", user_info.to_dict()).to_dict_json()


@account_dp.route("/getUsers", methods=["GET"])
def get_users():
    try:
        sql = text("SELECT * FROM user")
        result = db.session.execute(sql)
        users = [dict(row) for row in result.mappings().all()]
        return jsonify({"code": 200, "data": users})
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)})
