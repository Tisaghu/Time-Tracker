from flask import Flask, jsonify, request, render_template
from datetime import datetime

import os
import json
import csv


#set FLASK_ENV=development
#flask run


# Create a Flask application
app = Flask(__name__)

# In-memory storage for the start time
timer_data = {
    "start_time": None
}

logs = []
categories = []

# Storage for CSV information
IMPORT_CSV_FILE = './history.csv'
CSV_FILE = './time_records.csv'


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
    
    elapsed_time_str = find_elapsed(timer_data['start_time'])

    timer_data['start_time'] = None
    return jsonify({"message": "Timer stopped", "elapsed_time": elapsed_time_str}), 200


# Route to check elapsed time without stopping the  timer
@app.route('/elapsed_time', methods=['GET'])
def elapsed_time():
    if timer_data['start_time'] is None:
        return jsonify({"message": "Timer is not running,", "elapsed_time": 0}), 200

    elapsed_time_str = find_elapsed(timer_data['start_time'])

    return jsonify({"elapsed_time": elapsed_time_str}), 200


def find_elapsed(start):
    start_time = start
    current_time = datetime.now()
    elapsed_time = current_time - start_time

    hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)

    elapsed_time_str = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
    return elapsed_time_str


#Used for imoprting logs from Time Tracker App - will most likely be modified/removed in the future
def import_logs():
    #logs = []
    try:
        with open(IMPORT_CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames
            print("CSV Headers:", headers) # Debugging print statement
            for row in reader:
                print("CSV Row:", row) # Debugging print statement
                logs.append({
                    'record_id': row['RECORD ID'],
                    'start_time': row[' START TIME'],
                    'end_time': row[' END TIME'],
                    'duration': row[' DURATION'],
                    'category': row[' ACTIVITY NAME']
                })
    except FileNotFoundError:
        pass # Handle the case where the file doesn't exist yet
    return logs

@app.route('/test_import_logs', methods=['GET'])
def test_import_logs():
    logs = import_logs()
    return jsonify(logs), 200

#Used for loading regular time logs in the format of this application - also imports categories
def load_logs():
    logs = []
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames
            #print("CSV Headers:", headers) # Debugging print statement
            for row in reader:
                load_categories(row['category'])
                logs.append({
                    'record_id': row['record_id'],
                    'start_time': row['start_time'],
                    'end_time': row['end_time'],
                    'duration': row['duration'],
                    'category': row['category']
                })
    except FileNotFoundError:
        pass # Handle the case where the file doesn't exist yet
    return logs

@app.route('/test_load_logs', methods=['GET'])
def test_load_logs():
    logs = load_logs()
    return jsonify(logs), 200


def save_log(log):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['record_id', 'start_time', 'end_time', 'duration', 'category'])
        if not file_exists:
            writer.writeheader()
        writer.writerow(log)

@app.route('/test_save_log', methods=['POST'])
def test_save_log():
    logs = import_logs()
    for log in logs:
        save_log(log)
    return jsonify({"message": "Logs imported and saved successfully"}), 200


@app.route('/logs', methods=['GET'])
def get_logs():
    logs = load_logs()
    return jsonify(logs)


@app.route('/add_log', methods=['POST'])
def add_log():
    data = request.json
    log = {
        'record_id': data['record_id'],
        'duration': data['duration'],
        'category': data['category']
    }
    save_log(log)
    return jsonify(log), 201

def load_categories(category):
    strip_cat = category.strip()
    if strip_cat not in categories:
        categories.append(strip_cat)


@app.route('/test_load_categories', methods=['GET'])
def test_load_categories():
    load_logs()
    return categories


@app.route('/retrieve_categories', methods=['GET'])
def retrieve_categories():
    return jsonify({"categories": categories}), 200



# Load logs at the start of the program
load_logs()

