from flask import Blueprint, jsonify, request
from app.services.timer_service import start_timer, stop_timer, reset_timer, check_elapsed_time

timer_bp = Blueprint('timer', __name__)

@timer_bp.route('/start', methods=['POST'])
def start():
    response, status_code = start_timer()
    return jsonify(response), status_code

@timer_bp.route('/stop', methods=['POST'])
def stop():
    response, status_code = stop_timer()
    return jsonify(response), status_code

@timer_bp.route('/reset', methods=['POST'])
def reset():
    response, status_code = reset_timer()
    return jsonify(response), status_code

@timer_bp.route('/check', methods=['GET'])
def check():
    response, status_code = check_elapsed_time()
    return jsonify(response), status_code
