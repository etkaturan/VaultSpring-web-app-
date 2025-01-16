from app import db
from datetime import datetime

class RecurringSpending(db.Model):
    __tablename__ = 'recurring_spendings'

    id = db.Column(db.Integer, primary_key=True)
    spending_id = db.Column(db.Integer, db.ForeignKey('spendings.id'), nullable=False)
    frequency = db.Column(db.String(20), nullable=False)  # e.g., Weekly, Monthly
    next_occurrence = db.Column(db.DateTime, nullable=False)

    spending = db.relationship('Spending', backref=db.backref('recurring', lazy=True))

    def __repr__(self):
        return f"<RecurringSpending {self.spending.category} - {self.frequency}>"
