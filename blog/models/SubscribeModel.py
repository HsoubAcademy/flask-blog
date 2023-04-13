from blog import db


class StripeCustomer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subscription_type = db.Column(db.String(20), nullable=True, unique=False)
    status = db.Column(db.String(20), nullable=True, unique=False)
    customer_id = db.Column(db.String(255), nullable=True, unique=False)
    subscription_id = db.Column(db.String(255), nullable=True, unique=False)
    amount = db.Column(db.Integer)
    subscription_start = db.Column(db.DateTime)
    subscription_end = db.Column(db.DateTime)
    subscription_canceled = db.Column(db.Boolean, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Customer('{self.user_id}'. '{self.status}')"
