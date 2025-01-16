from app import db
from datetime import datetime

class Spending(db.Model):
    __tablename__ = 'spendings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default="USD", nullable=False)  # New field
    description = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_method = db.Column(db.String(20), nullable=False)  # e.g., Cash, Card

    user = db.relationship('User', backref=db.backref('spendings', lazy=True))
    category = db.relationship('Category', backref=db.backref('spendings', lazy=True))

    def __repr__(self):
        return f"<Spending {self.category.name} - {self.amount} {self.currency}>"
