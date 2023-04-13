from blog import db
from sqlalchemy.sql import func


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    article_img = db.Column(db.String(50), nullable=False, default="default.png")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes = db.relationship("Like", backref='article', passive_deletes=True)

    def __repr__(self):
        return f"Article('{self.user_id}'. '{self.title}')"
