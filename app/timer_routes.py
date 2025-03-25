from flask import Blueprint, jsonify, request
from datetime import datetime

timer_bp = Blueprint('timer', __name__)

# In-memory timer storage
timer_data = {'start_time': None,
              'end_time': None}

isRunning = False
hasRun = False

#Initialize Timer
@timer_bp.route('/init')
def init_timer():
    timer_data['start_time'] = None
    timer_data['end_time'] = None
    return jsonify({"message": "Timer initialized"}), 200

# Start Timer
@timer_bp.route('/start')
def start_timer():
    global isRunning
    if timer_data['start_time'] is not None:
        return jsonify({"message": "Timer is already running"}), 409
    timer_data['start_time'] = datetime.now()
    isRunning = True
    return jsonify({"message": "Timer started"}), 200

# Stop Timer
@timer_bp.route('/stop')
def stop_timer():
    global isRunning
    if not isRunning:
        return jsonify({"message": "Timer is not running"}), 409
    elapsed_time_str = calculate_elapsed_time(timer_data['start_time'])
    #timer_data['start_time'] = None
    return jsonify({"message": "Timer stopped", "elapsed_time": elapsed_time_str, "start_time": timer_data['start_time'], "end_time": timer_data['end_time']}), 200

# Reset Timer
@timer_bp.route('/reset')
def reset_timer():
    global isRunning
    timer_data['start_time'] = None
    timer_data['end_time'] = None
    isRunning = False
    return jsonify({"message": "Timer reset"}), 200

# Check Elapsed Time
@timer_bp.route('/check', methods=['GET'])
def check_elapsed_time():
    if timer_data['start_time'] is None:
        return jsonify({"message": "Timer is not running", "elapsed_time": "00:00:00"}), 200
    elapsed_time_str = calculate_elapsed_time(timer_data['start_time'])
    return jsonify({"elapsed_time": elapsed_time_str}), 200

# Helper Function: Calculate Elapsed Time
def calculate_elapsed_time(start):
    timer_data['end_time'] = datetime.now()
    elapsed_time = timer_data['end_time'] - timer_data['start_time']
    hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
