from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.spending.category import Category

category_bp = Blueprint('category', __name__, url_prefix='/api/categories')


@category_bp.route('/', methods=['POST'])
@jwt_required()
def add_category():
    """
    Adds a new category or subcategory.
    """
    data = request.json

    # Validate category name
    if not data.get('name'):
        return jsonify({'error': 'Category name is required'}), 400

    category = Category(
        name=data['name'],
        parent_id=data.get('parent_id')  # None for top-level categories
    )
    db.session.add(category)
    db.session.commit()

    return jsonify({'message': 'Category added successfully', 'category_id': category.id}), 201

@category_bp.route('/', methods=['GET'])
@jwt_required()
def get_categories():
    """
    Retrieves all categories for the authenticated user.
    """
    categories = Category.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'parent_id': c.parent_id
    } for c in categories]), 200

@category_bp.route('/nested/', methods=['GET'])
@jwt_required()
def get_nested_categories():
    """
    Retrieves categories in a nested structure.
    """
    def build_category_tree(parent_id=None):
        categories = Category.query.filter_by(parent_id=parent_id).all()
        return [{
            'id': cat.id,
            'name': cat.name,
            'subcategories': build_category_tree(cat.id)
        } for cat in categories]

    return jsonify(build_category_tree()), 200

@category_bp.route('/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    """
    Deletes a category and its subcategories.
    """
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    # Delete category and all subcategories
    def delete_category_tree(category_id):
        subcategories = Category.query.filter_by(parent_id=category_id).all()
        for subcategory in subcategories:
            delete_category_tree(subcategory.id)
        category_to_delete = Category.query.get(category_id)
        db.session.delete(category_to_delete)

    delete_category_tree(category_id)
    db.session.commit()

    return jsonify({'message': 'Category and its subcategories deleted successfully'}), 200
