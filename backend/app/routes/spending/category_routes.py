from flask import Blueprint, request, jsonify
from app import db
from app.models.spending.category import Category

category_bp = Blueprint('category', __name__, url_prefix='/api/categories')

@category_bp.route('/', methods=['POST'])
def add_category():
    data = request.json
    category = Category(
        name=data['name'],
        parent_id=data.get('parent_id')  # Can be None for top-level categories
    )
    db.session.add(category)
    db.session.commit()
    return jsonify({'message': 'Category added successfully', 'category_id': category.id}), 201

@category_bp.route('/', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'parent_id': c.parent_id
    } for c in categories]), 200

@category_bp.route('/nested', methods=['GET'])
def get_nested_categories():
    def build_category_tree(parent_id=None):
        categories = Category.query.filter_by(parent_id=parent_id).all()
        return [{
            'id': cat.id,
            'name': cat.name,
            'subcategories': build_category_tree(cat.id)
        } for cat in categories]

    return jsonify(build_category_tree())

