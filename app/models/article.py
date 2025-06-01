import datetime

from app.models.base_model import BaseModel
from app.extensions import db


class Article(BaseModel, db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30))
    author_id = db.Column(db.Integer)
    context = db.Column(db.Text)
    channel_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    cover_url = db.Column(db.Text)


class ArticleCardVo(Article):
    def __init__(self, article_id=1, like_count=0, collect_count=0, author_avatar="", author_name="", liked=False, collected=False):
        self.id = id,
        self.article_id = article_id,
        self.like_count = like_count
        self.collect_count = collect_count
        self.author_avatar = author_avatar
        self.author_name = author_name
        self.liked = liked
        self.collected = collected
        self.create_time = datetime.datetime.now()
        self.update_time = datetime.datetime.now()
        self.cover_url = None
        self.status = 0
        self.create_user = None
        self.update_user = None
