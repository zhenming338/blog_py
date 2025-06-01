from app.dao import article_dao, account_dao
from app.models.article import ArticleCardVo
from flask import g


def get_channel_list():
    channel_list = article_dao.get_channel_list()
    return [channel.to_dict() for channel in channel_list]


def get_article_card_list(post_data):
    authorName = post_data.get('authorName')
    context = post_data.get('context')
    title = post_data.get('title')
    user = account_dao.searchByName(authorName)
    user_id = None
    if user is not None:
        user_id = user.id
    article_list = article_dao.get_article_list(user_id, context, title)
    article_card_list = []
    for article in article_list:
        article_card = ArticleCardVo.from_dict(article.to_dict()).to_dict()
        article_card["author_name"] = account_dao.get_user_by_id(article.author_id).username
        article_card["author_avatar"] = article.cover_url
        article_card["article_id"] = article.id
        article_card_list.append(article_card)
    return article_card_list


def get_article_page(post_data):
    article_page = article_dao.get_article_page(post_data)
    article_count = article_dao.get_article_count()
    article_vo_page = []
    for article in article_page:
        article = article.to_dict()
        article['createTime'] = article['create_time']
        article['authorName'] = account_dao.get_user_by_id(article['author_id']).username
        article['channelName'] = article_dao.get_channel_by_id(article['channel_id']).name
        article_vo_page.append(article)
    return {
        "count": article_count,
        "data": article_vo_page,
    }


def add_article(post_data):
    post_data['authorId'] = g.user_info['id']
    post_data['status'] = 1
    article_dao.add_article(post_data)
    return None


def delete_article(article_id):
    authorId = g.user_info['id']
    article_dao.delete_article(article_id, authorId)
    return None


def get_article_content(article_id):
    article = article_dao.get_article_by_id(article_id)
    if article is None:
        return None
    article['authorName'] = account_dao.get_user_by_id(article['author_id']).username
    article['createTime'] = article['create_time']
    article['updateTime'] = article['update_time']
    article['channelName'] = article_dao.get_channel_by_id(article['channel_id']).name
    return article
