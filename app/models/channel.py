from app.models.base_model import BaseModel
from app.extensions import db


class Channel(BaseModel, db.Model):
    __tablename__ = 'channel'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
