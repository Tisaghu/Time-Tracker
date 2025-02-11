from flask import Blueprint, jsonify, request
from datetime import datetime

timer_bp = Blueprint('timer', __name__)

# In-memory timer storage
timer_data = {"start_time": None}

# Start Timer
@timer_bp.route('/start', methods=['POST'])
def start_timer():
    if timer_data['start_time'] is not None:
        return jsonify({"message": "Timer is already running"}), 400
    timer_data['start_time'] = datetime.now()
    return jsonify({"message": "Timer started"}), 200

# Stop Timer
@timer_bp.route('/stop', methods=['POST'])
def stop_timer():
    if timer_data['start_time'] is None:
        return jsonify({"message": "Timer is not running"}), 400

    elapsed_time_str = find_elapsed(timer_data['start_time'])
    timer_data['start_time'] = None
    return jsonify({"message": "Timer stopped", "elapsed_time": elapsed_time_str}), 200

# Check Elapsed Time
@timer_bp.route('/check', methods=['GET'])
def check_elapsed_time():
    if timer_data['start_time'] is None:
        return jsonify({"message": "Timer is not running", "elapsed_time": "00:00:00"}), 200

    elapsed_time_str = find_elapsed(timer_data['start_time'])
    return jsonify({"elapsed_time": elapsed_time_str}), 200

# Helper Function: Calculate Elapsed Time
def find_elapsed(start):
    current_time = datetime.now()
    elapsed_time = current_time - start
    hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
