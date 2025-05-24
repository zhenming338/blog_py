from flask import Blueprint,request,jsonify
from app.models.user import User
from app.extensions import db
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from datetime import timedelta
user_dp=Blueprint("t_users",__name__)

@user_dp.route("/login",methods=["POST"])
def login():
    data = request.get_json()
    email=data.get("email")
    user=User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"msg":"invaild email"}),401
    token = create_access_token(identity=user.id,expires_delta=timedelta(hours=1))
    return jsonify({"access_token":token})

@user_dp.route("/",methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([
        {
            "id":u.id,
            "name":u.name,
            "email":u.email
        } for u in users
    ])

@user_dp.route("/",methods=['POST'])
def add_user():
    data=request.get_json()
    user=User(name=data['name'])
   
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
       var = db.session.rollback
       return {"error":"Email already exists"},400
    return jsonify({"msg":"User added ","id":User.id}),201

@user_dp.route("/<int:user_id>",methods=['PUT'])
def update_user(user_id):
    data=request.get_json()
    user=User.query.get_or_404(user_id)
    user.name=data['name']
    user.email=data['email']
    db.session.commit()
    return jsonify({"msg":"User updated"})

@user_dp.route("/<int:user_id>",methods=['DELETE'])
def delete_user(user_id):
    user=User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg":"user deleted"})
