from app.extensions import db
from sqlalchemy.sql import func
from app.models.base_model import BaseModel

class User(db.Model,BaseModel):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(
        db.String(255),
        nullable=False,
    )
    email = db.Column(db.String(100), nullable=False, unique=False)
    phone = db.Column(db.String(15), nullable=True)
    enabled = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, server_default=func.now())
    update_time = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
