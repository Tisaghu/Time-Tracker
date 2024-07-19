"""
This module implements a set of test routes for a Flask application used for time tracking.

The test routes provide the following functionalities:
- Test importing logs from a CSV file.
- Test loading logs from a CSV file.
- Test saving logs to a CSV file.

Routes:
- /test/test_import_logs: Test import of logs from a CSV file.
- /test/test_load_logs: Test loading of logs from a CSV file.
- /test/test_save_log: Test saving of logs to a CSV file.
"""

from flask import Blueprint, jsonify
from app.main_routes import import_logs, load_logs, save_log

test_bp = Blueprint('test', __name__, static_folder='static', template_folder='templates')

IMPORT_CSV_FILE = './history.csv'
CSV_FILE = './time_records.csv'

logs = []
categories = []

@test_bp.route('/test_import_logs', methods=['GET'])
def test_import_logs():
    """
    Test import of logs from a CSV file.

    This view function handles the '/test_import_logs' URL and tests the import of logs
    from a CSV file.

    Returns:
    Response: A JSON response with the imported logs.
    """
    imported_logs = import_logs()
    return jsonify(imported_logs), 200

@test_bp.route('/test_load_logs', methods=['GET'])
def test_load_logs():
    """
    Test loading of logs from a CSV file.

    This view function handles the '/test_load_logs' URL and tests the loading of logs
    from a CSV file.

    Returns:
    Response: A JSON response with the loaded logs.
    """
    loaded_logs = load_logs()
    return jsonify(loaded_logs), 200

@test_bp.route('/test_save_log', methods=['POST'])
def test_save_log():
    """
    Test saving of logs to a CSV file.

    This view function handles the '/test_save_log' URL and tests the saving of logs
    to a CSV file.

    Returns:
    Response: A JSON response with a success message.

    For testing POST:
    curl -X POST http://127.0.0.1:5000/test_save_log

    """
    imported_logs = import_logs()
    for log in imported_logs:
        save_log(log)
    return jsonify({"message": "Logs imported and saved successfully"}), 200