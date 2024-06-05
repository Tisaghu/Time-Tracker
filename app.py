from flask import Flask, jsonify, request, render_template
from datetime import datetime

import json


# Create a Flask application
app = Flask(__name__)

# In-memory storage for the start time
timer_data = {
    "start_time": None
}


# Render HTML template
@app.route('/')
def index():
    return render_template('index.html')


# Route to start the timer
@app.route('/start_timer', methods=['POST'])
def start_timer():
    if timer_data['start_time'] is not None:
        return jsonify({"message": "Timer is already running"}), 400
    
    timer_data['start_time'] = datetime.now()
    return jsonify({"message": "Timer started"}), 200

# Route to stop the timer and show elapsed time
@app.route('/stop_timer', methods=['POST'])
def stop_timer():
    if timer_data['start_time'] is None:
        return jsonify({"message": "Timer is not running"}), 400
    
    start_time = timer_data['start_time']
    end_time = datetime.now()
    elapsed_time = (end_time - start_time).total_seconds()

    timer_data['start_time'] = None
    return jsonify({"message": "Timer stopped", "elapsed_time": elapsed_time}), 200

# Route to check elapsed time without stopping the  timer
@app.route('/elapsed_time', methods=['GET'])
def elapsed_time():
    if timer_data['start_time'] is None:
        return jsonify({"message": "Timer is not running,", "elapsed_time": 0}), 200
    
    start_time = timer_data['start_time']
    current_time = datetime.now()
    elapsed_time = (current_time - start_time).total_seconds()

    return jsonify({"elapsed_time": elapsed_time}), 200


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
