from flask import Blueprint, jsonify, request

from app.common import result
from app.common.result import Result
from app.dao import article_dao
from app.services import article_service

article_bp = Blueprint("/api/article", __name__)


@article_bp.route("getChannelList", methods=["GET"])
def get_channel_list() -> Result:
    channel_list = article_service.get_channel_list()
    return Result.success("", channel_list).to_dict_json()


@article_bp.route("getArticleCardList", methods=["POST"])
def get_article_card_list() -> Result:
    post_data = request.get_json()
    article_card_list = article_service.get_article_card_list(post_data)
    print(article_card_list)
    return Result.success("get success", article_card_list).to_dict_json()


@article_bp.route("getArticlePage", methods=["POST"])
def get_article_page() -> Result:
    post_data = request.get_json()
    article_page = article_service.get_article_page(post_data)
    return Result.success("", article_page).to_dict_json()


@article_bp.route("addArticle", methods=["POST"])
def add_article() -> Result:
    post_data = request.get_json()
    article_service.add_article(post_data)
    return Result.success("add success").to_dict_json()


@article_bp.route("deleteMyArticle", methods=["DELETE"])
def delete_article() -> Result:
    article_id = request.args.get("articleId")
    article_service.delete_article(article_id)
    return Result.success("delete success").to_dict_json()


@article_bp.route("getArticleContent", methods=['GET'])
def get_article_content() -> Result:
    article_id = request.args.get("articleId")
    content = article_service.get_article_content(article_id)
    return Result.success("", content).to_dict_json()
