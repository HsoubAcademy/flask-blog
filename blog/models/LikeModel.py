from blog import db
from sqlalchemy.sql import func


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    liked_user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id', ondelete="CASCADE"), nullable=False)
