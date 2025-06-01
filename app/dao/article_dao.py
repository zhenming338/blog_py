from sqlalchemy import text

from flask import g
from app.extensions import db
from app.models.article import Article
from app.models.channel import Channel


def get_channel_list() -> list[Channel]:
    sql = text("SELECT * FROM channel")
    result = db.session.execute(sql)
    rows = result.mappings()
    channel_list = [Channel.from_dict(row) for row in rows]
    return channel_list


def get_article_list(authorId: int | None, context: str, title: str) -> list[Article]:
    conditions = []
    params = {}

    if authorId is not None:
        conditions.append("author_id = :authorId")
        params["authorId"] = authorId
    else:
        conditions.append("author_id IS NULL")

    if context:
        conditions.append("context LIKE CONCAT('%', :context, '%')")
        params["context"] = context

    if title:
        conditions.append("title LIKE CONCAT('%', :title, '%')")
        params["title"] = title

    where_clause = " OR ".join(conditions)
    sql = text(f"SELECT * FROM article WHERE {where_clause}")

    result = db.session.execute(sql, params)
    rows = result.mappings()
    article_list = [Article.from_dict(row) for row in rows]
    return article_list


def get_article_page(post_data):
    pageIndex = post_data["pageIndex"]
    pageSize = post_data["pageSize"]
    pageStartCount = (pageIndex - 1) * pageSize
    sql = text("select * from article limit :pageStartCount, :pageSize")
    result = db.session.execute(sql, {"pageStartCount": pageStartCount, "pageSize": pageSize})
    rows = result.mappings()
    article_page = [Article.from_dict(row) for row in rows]
    return article_page


def get_article_count():
    sql = text("select count(1) as articleCount from article ")
    result = db.session.execute(sql)
    row = result.mappings().first()
    print(row)
    return row['articleCount']


def get_channel_by_id(channel_id):
    sql = text("select * from channel where id = :channel_id")
    result = db.session.execute(sql, {"channel_id": channel_id})
    row = result.mappings().first()
    return row


def add_article(post_data):
    sql = text(
        "insert into article values (default,:title,:authorId,:context,:channelId,:status,default,default,:coverUrl)")
    db.session.execute(sql, post_data)
    db.session.commit()
    return None


def delete_article(article_id, authorId):
    print(article_id, authorId)
    sql = text("delete from article where id = :article_id and author_id = :author_id")
    db.session.execute(sql, {"article_id": article_id, "author_id": authorId})
    db.session.commit()
    return None


def get_article_by_id(article_id):
    print(article_id)
    sql = text("select * from article where id = :article_id")
    result = db.session.execute(sql, {"article_id": article_id})
    row = result.mappings().first()
    if row is None:
        return None
    return Article.from_dict(row).to_dict()
