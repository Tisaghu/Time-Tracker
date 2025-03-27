from flask import Blueprint, jsonify, request
from app.services.log_service import LogService

log_bp = Blueprint('log', __name__)
log_service = LogService()

@log_bp.route('/', methods=['GET'])
def get_logs():
    return jsonify(log_service.get_logs()), 200

@log_bp.route('/add', methods=['POST'])
def add_log():
    data = request.json
    log = log_service.add_log(data)
    return jsonify(log), 201

@log_bp.route('/categories', methods=['GET'])
def retrieve_categories():
    return jsonify({"categories": log_service.get_categories()}), 200

@log_bp.route('/add_category', methods=['POST'])
def add_category():
    data = request.json
    response, status = log_service.add_category(data)
    return jsonify(response), status