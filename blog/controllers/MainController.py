from flask import render_template
from blog.models.ArticleModel import Article
from blog.utils.MainUtils import Paginate
from blog import cfg


class MainController:
    def home():
        pagination, articles_per_page = Paginate(cfg.POSTS_PER_PAGE, Article, Article.created_date.desc())
        return render_template("main/home.jinja", articles_per_page=articles_per_page, pagination=pagination,
                               title="مدونة حسوب")
