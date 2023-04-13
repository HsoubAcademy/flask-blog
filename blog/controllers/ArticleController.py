from blog.forms.ArticleForm import ArticleForm
from blog.models.ArticleModel import Article
from blog import db, cfg
from flask import redirect, url_for, render_template, flash, request, jsonify
from flask_login import current_user, login_required
from blog.models.LikeModel import Like
from blog.models.SubscribeModel import StripeCustomer
from blog.utils.ArticlesUtils import save_image
from blog.utils.MainUtils import Paginate


class ArticleController:

    @login_required
    def article_add():
        if current_user.is_admin is False:
            flash('لا تملك صلاحية الوصول للصفحة المطلوبة', 'warning')
            return redirect(url_for('main_controller.home'))
        form = ArticleForm()
        if form.validate_on_submit():
            if form.article_img.data:
                image_name = save_image(form.article_img.data)
            else:
                image_name = None
            new_article = Article(user_id=current_user.id, title=form.title.data, content=form.content.data,
                                  article_img=image_name)
            db.session.add(new_article)
            db.session.commit()
            flash("تم إضافة المقال بنجاح", "success")
            return redirect(url_for("main_controller.home"))
        return render_template("articles/article_add.jinja", form=form, legend="إضافة مقالة جديدة", title="إضافة مقالة")

    @login_required
    def article_update(id):
        if current_user.is_admin is False:
            flash('لا تملك صلاحية الوصول للصفحة المطلوبة', 'warning')
            return redirect(url_for('main_controller.home'))
        form = ArticleForm()
        article = Article.query.get_or_404(id)
        if form.validate_on_submit():
            if form.article_img.data:
                image_name = save_image(form.article_img.data)
                article.article_img = image_name
            article.title = form.title.data
            article.content = form.content.data
            db.session.commit()
            flash('تم تعديل المقالة', 'success')
            return redirect(url_for('article_controller.article_show', id=article.id))
        form.title.data = article.title
        form.content.data = article.content
        form.article_img.data = article.article_img
        return render_template("articles/article_add.jinja", title="تعديل المقالة", legend='تعديل المقالة:', form=form)

    @login_required
    def article_delete(id):
        article = Article.query.get_or_404(id)
        if current_user.is_admin:
            db.session.delete(article)
            db.session.commit()
            flash('تم حذف المقالة.', 'success')
            return redirect(url_for('article_controller.articles_list'))
        else:
            flash('لا تملك صلاحية الوصول للصفحة المطلوبة', 'warning')
            return redirect(url_for("main_controller.home"))

    def article_show(id):
        article = Article.query.get_or_404(id)
        if current_user.is_authenticated:
            customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
            if customer and customer.status == "active":
                return render_template("articles/article.jinja", article=article, customer=customer,
                                       title=article.title)
        return render_template("articles/article.jinja", article=article, title=article.title)

    @login_required
    def articles_list():
        if current_user.is_admin:
            pagination, articles_list = Paginate(cfg.RECORD_PER_PAGE, Article, Article.id.desc())
            return render_template("articles/articles_list.jinja", articles_list=articles_list, pagination=pagination,
                                   title="لائحة المقالات")
        else:
            flash('لا تملك صلاحية الوصول للصفحة المطلوبة', 'warning')
            return redirect(url_for('main_controller.home'))

    @login_required
    def article_like(id):
        if request.method == "GET":
            flash('لا تملك صلاحية الوصول للصفحة المطلوبة', 'warning')
            return redirect(url_for('main_controller.home'))
        try:
            customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
            article = Article.query.filter_by(id=id).first()
            if customer and customer.status == "active" or current_user.is_admin:
                like = Like.query.filter_by(liked_user=current_user.id, article_id=article.id).first()
                if like:
                    db.session.delete(like)
                    db.session.commit()
                else:
                    like = Like(liked_user=current_user.id, article_id=article.id)
                    db.session.add(like)
                    db.session.commit()
                return jsonify({"likes": len(article.likes),
                                "liked": current_user.id in map(lambda x: x.liked_user, article.likes)})
            else:
                flash('يجب عليك الاشتراك أولا', 'danger')
                return redirect(url_for('article_controller.article_show', article_id=article.id, id=article.id))
        except:
            flash('المقالة غير موجودة', 'danger')
            return redirect(url_for('main_controller.home'))
