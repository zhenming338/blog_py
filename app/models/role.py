from dataclasses import dataclass

from app.extensions import db
from app.models.base_model import BaseModel

class Role(db.Model,BaseModel):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)
    authLabel = db.Column(db.String(30), unique=True)
    label = db.Column(db.String(30))
    channelId = db.Column(db.Integer)
    isAdmin = db.Column(db.Integer)
