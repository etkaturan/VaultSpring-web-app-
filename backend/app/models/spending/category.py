from app import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    
    subcategories = db.relationship('Category', backref=db.backref('parent', remote_side=[id]), lazy=True)

    def __repr__(self):
        return f"<Category {self.name} (Parent: {self.parent_id})>"
