from flask import Blueprint, jsonify
from app.storage.log_storage import LogStorage
from app.storage.category_storage import CategoryStorage


test_bp = Blueprint('test', __name__)

# Test loading logs from app CSV
@test_bp.route('/load', methods=['GET'])
def test_load_logs():
    storage = LogStorage()
    return jsonify(storage.load_logs()), 200

# Test to check contents of categories
@test_bp.route('/categories', methods=['GET'])
def test_categories():
    cs = CategoryStorage()
    return jsonify({"categories": cs.get_categories()}), 200
