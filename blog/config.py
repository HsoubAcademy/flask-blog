# from datetime import datetime
from datetime import datetime
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config():
    TESTING = False
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")


class DevelopmentCfg(Config):
    DEBUG = True
    APP_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
    VIEWS_DIR = APP_DIR / "template"
    CONTROLLER_DIR = APP_DIR / "controllers"
    STATIC_DIR = APP_DIR / "static"
    IMAGES_DIR = STATIC_DIR / "images"
    # PostgreSQL
    SQLALCHEMY_DATABASE_URI = f'postgresql://{os.environ.get("DATABASE_USERNAME")}:{os.environ.get("DATABASE_PASSWORD")}@localhost/{os.environ.get("DATABASE_NAME")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Owner data
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME")
    OWNER_EMAIL = os.environ.get("OWNER_EMAIL")
    OWNER_PASSWORD = os.environ.get("OWNER_PASSWORD")

    STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY")
    STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
    STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")

    prices = {
        'yearly_subscription': os.environ.get("YEARLY_SUBSCRIPTION"),
        'monthly_subscription': os.environ.get("MONTHLY_SUBSCRIPTION")
    }

    # Seed Data
    ACCOUNT_COUNT = 50
    ADMIN_PERCENTAGE = 10  # 10%
    USER_PASSWORD = '123'
    ARTICLE_COUNT = 100
    CUSTOMER_COUNT = 40
    START_DATE = datetime(2023, 2, 1)
    LIKE_COUNT = 200

    LOGIN_MSG = "يجب عليك الاشتراك لمشاهدة المحتوى"

    POSTS_PER_PAGE = 9
    # Pagination Lists
    RECORD_PER_PAGE = 20
    USERS_PER_PAGE = 25

    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    RESET_MAIL = "noreply-blog@hsoub.com"


class ProductionCfg(Config):
    pass
