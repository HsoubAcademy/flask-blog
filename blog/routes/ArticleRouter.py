from flask import Blueprint
from blog.controllers.ArticleController import ArticleController

ArticleRouter = Blueprint("article_controller", __name__, url_prefix="/article")

ArticleRouter.route("/article_add", methods=["POST", "GET"])(ArticleController.article_add)
ArticleRouter.route("/<int:id>", methods=["GET"])(ArticleController.article_show)
ArticleRouter.route("/<int:id>/like", methods=["POST", "GET"])(ArticleController.article_like)
ArticleRouter.route("/<int:id>/update", methods=["POST", "GET"])(ArticleController.article_update)
ArticleRouter.route("/<int:id>/delete", methods=["GET"])(ArticleController.article_delete)
ArticleRouter.route("/articles_list", methods=["GET"])(ArticleController.articles_list)
