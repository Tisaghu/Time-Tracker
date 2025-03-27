from flask import Blueprint, jsonify, request
from app.services.category_service import CategoryService

category_bp = Blueprint('category', __name__)
category_service = CategoryService()

@category_bp.route('/categories', methods=['GET'])
def retrieve_categories():
    return jsonify({"categories": category_service.get_categories()}), 200

@category_bp.route('/add_category', methods=['POST'])
def add_category():
    data = request.json
    response, status = category_service.add_category(data)
    return jsonify(response), status