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
    # Reset timer on initialization
    reset_timer()
    return jsonify({"message": "Timer initialized"}), 200

# Start Timer
@timer_bp.route('/start')
def start_timer():
    global isRunning
    global hasRun

    if isRunning:
        return jsonify({"message": "Timer is already running"}), 409
    if hasRun:
        isRunning = True
        return jsonify({"message": "Timer resumed"}), 200
    isRunning = True
    hasRun = True
    timer_data['start_time'] = datetime.now()
    return jsonify({"message": "Timer started"}), 200

# Stop Timer
@timer_bp.route('/stop')
def stop_timer():
    global isRunning
    global hasRun

    if not isRunning:
        if hasRun:
            reset_timer()
            return jsonify({"message": "Resetting Timer"}), 200
        else:
            return jsonify({"message": "Timer is not running"}), 409
    else:
        isRunning = False
        hasRun = True
        elapsed_time_str = calculate_elapsed_time(timer_data['start_time'])
        #timer_data['start_time'] = None
        return jsonify({"message": "Timer stopped",
                        "elapsed_time": elapsed_time_str,
                        "start_time": timer_data['start_time'],
                        "end_time": timer_data['end_time']}), 200

# Reset Timer
@timer_bp.route('/reset')
def reset_timer():
    global isRunning
    global hasRun
    timer_data['start_time'] = None
    timer_data['end_time'] = None
    isRunning = False
    hasRun = False
    return jsonify({"message": "Timer reset"}), 200

# Check Elapsed Time
@timer_bp.route('/check', methods=['GET'])
def check_elapsed_time():
    global hasRun
    if not hasRun:
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
