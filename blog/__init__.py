import mimetypes

mimetypes.add_type('application/javascript', '.js')

from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from flask_login import LoginManager
from flask_mail import Mail
from flask_ckeditor import CKEditor
import stripe
from blog.config import ProductionCfg, DevelopmentCfg

"""Enable for Development mode"""
cfg = DevelopmentCfg
"""Enable for Production mode"""
# cfg = ProductionCfg

bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
seeder = FlaskSeeder()
mail = Mail()
ckeditor = CKEditor()
login_manger = LoginManager()

stripe.api_key = cfg.STRIPE_SECRET_KEY

login_manger.login_view = "auth_controller.user_login"
login_manger.login_message = cfg.LOGIN_MSG
login_manger.login_message_category = "warning"


def create_app():
    app = Flask(__name__, template_folder=cfg.VIEWS_DIR, static_folder=cfg.STATIC_DIR)
    app.config.from_object(cfg)

    with app.app_context():
        register_extention(app)
        # الموجهات وصفحات الخطأ
        register_blueprints(app)
        register_errorhandlers(app)

        app.before_first_request(populate_database)
    return app


def register_extention(app):
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    seeder.init_app(app, db)
    login_manger.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    return None


def register_blueprints(app):
    from blog.routes.MainRouter import MainRouter
    from blog.routes.ArticleRouter import ArticleRouter
    from blog.routes.AuthRouter import AuthRouter
    from blog.routes.SubscribeRouter import SubscribeRouter

    app.register_blueprint(MainRouter)
    app.register_blueprint(ArticleRouter)
    app.register_blueprint(AuthRouter)
    app.register_blueprint(SubscribeRouter)

    return None


from blog.models.AuthModel import User
from blog.models.ArticleModel import Article
from blog.models.SubscribeModel import StripeCustomer
from blog.models.LikeModel import Like


def populate_database():
    db.create_all()
    if not User.query.filter_by(username=cfg.OWNER_USERNAME).first():
        user = User(
            username=cfg.OWNER_USERNAME,
            email=cfg.OWNER_EMAIL,
            password=bcrypt.generate_password_hash(cfg.OWNER_PASSWORD).decode("utf-8"),
            is_admin=True
        )
        db.session.add(user)
        db.session.commit()


def register_errorhandlers(app):
    def render_error(error):
        error_code = getattr(error, "code", 404)
        return render_template("main/{0}.jinja".format(error_code), error_code=error_code,
                               title="غير متوفر"), error_code

    for errcode in [404]:
        app.errorhandler(errcode)(render_error)
    return None
