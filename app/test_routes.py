from flask import Blueprint, jsonify
#from app.routes.log_routes import import_logs, load_logs, save_log, CATEGORIES


test_bp = Blueprint('test', __name__)

# Test importing logs from external CSV
@test_bp.route('/import', methods=['GET'])
def test_import_logs():
    return jsonify(import_logs()), 200

# Test loading logs from app CSV
@test_bp.route('/load', methods=['GET'])
def test_load_logs():
    return jsonify(load_logs()), 200

# Test saving logs
@test_bp.route('/save', methods=['POST'])
def test_save_log():
    imported_logs = import_logs()
    for log in imported_logs:
        save_log(log)
    return jsonify({"message": "Logs imported and saved successfully"}), 200

# Test to check contents of categories
@test_bp.route('/categories', methods=['GET'])
def test_categories():
    return jsonify({"categories": CATEGORIES }), 200
