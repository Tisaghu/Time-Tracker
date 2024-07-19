"""
This module implements a simple Flask application for time tracking.

The application provides the following functionalities:
- Render the home page.
- Start and stop a timer.
- Check the elapsed time without stopping the timer.
- Import logs from a CSV file.
- Load and save logs.
- Retrieve and manage timed categories.

Routes:
- /: Render the home page.
- /start_timer: Start the timer.
- /stop_timer: Stop the timer and show elapsed time.
- /check_elapsed_time: Check elapsed time without stopping the timer.
- /test_import_logs: Test import of logs from a CSV file.
- /test_load_logs: Test loading of logs.
- /test_save_logs: Test saving of logs.
- /logs: Get all logs.
- /add_log: Add a new log.
- /test_load_categories: Test loading of categories.
- /retrieve_categories: Retrieve all categories.
"""


import os
import csv

from datetime import datetime
from flask import Flask, jsonify, request, render_template


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
    """

    Render the home page.

    This view function handles the root URL and returns the rendered HTML template 
    for the home page.

    Returns:
    str: The rendered HTML content of the home page.
    """
    return render_template('index.html')


# Route to start the timer
@app.route('/start_timer', methods=['POST'])
def start_timer():
    """
    Start the timer.
    
    This view function handles the '/start_timer' URL and starts the timer by recording the current
    time. If the timer is already running, it returns an error message.
    
    Returns:
    Response: A JSON response with a success or error message.
    """
    if timer_data['start_time'] is not None:
        return jsonify({"message": "Timer is already running"}), 400
    timer_data['start_time'] = datetime.now()
    return jsonify({"message": "Timer started"}), 200


# Route to stop the timer and show elapsed time
@app.route('/stop_timer', methods=['POST'])
def stop_timer():
    """
    Stop the timer and show elapsed time.
    
    This view function handles the '/stop_timer' URL and stops the timer by calculating
    the elapsed time since the timer started. If the timer is not  running, it returns an error
    message.
    
    Returns:
    Response: A JSON response with a success or error message and the elapsed time.
    """
    if timer_data['start_time'] is None:
        return jsonify({"message": "Timer is not running"}), 400
    elapsed_time_str = find_elapsed(timer_data['start_time'])

    timer_data['start_time'] = None
    return jsonify({"message": "Timer stopped", "elapsed_time": elapsed_time_str}), 200


# Route to check elapsed time without stopping the  timer
@app.route('/check_elapsed_time', methods=['GET'])
def check_elapsed_time():
    """
    Check elapsed time without stopping the timer.
    
    This view function handles the '/check_elapsed_time' URL and calculates the elapsed time
    since the timer started without stopping the timer. If the timer is not running, it returns
    an error message.
     
    Returns:
    Response: A JSON response with the elapsed time.
    """
    if timer_data['start_time'] is None:
        return jsonify({"message": "Timer is not running,", "elapsed_time": 0}), 200

    elapsed_time_str = find_elapsed(timer_data['start_time'])

    return jsonify({"elapsed_time": elapsed_time_str}), 200


def find_elapsed(start):
    """
    Calculate the elapsed time since the start time.

    This function calculates the elapsed time in hours, minutes, and seconds since the 
    provided start time.

    Args:
    start (datetime): The start time.

    Returns:
    str: The elapsed time formatted as HH:MM:SS.
    """
    start_time = start
    current_time = datetime.now()
    elapsed_time = current_time - start_time

    hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)

    elapsed_time_str = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    return elapsed_time_str


#Used for imoprting logs from Time Tracker App - will most likely be modified/removed in the future
def import_logs():
    """
    Import logs from a CSV file.

    This function reads logs from the specified CSV file and appends them to the logs list.
    If the file does not exist, it handles the exception gracefully.

    Returns:
    list: A list of logs imported from the CSV file.
    """
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
    """
    Test import of logs from a CSV file.

    This view function handles the '/test_import_logs' URL and tests the import of logs
    from a CSV file.

    Returns:
    Response: A JSON response with the imported logs.
    """
    imported_logs = import_logs()
    return jsonify(imported_logs), 200

#Used for loading regular time logs in the format of this application - also imports categories
def load_logs():
    """
    Load logs from a CSV file.

    This function reads logs from the specified CSV file and appends them to the logs list.
    It also imports categories from the logs. If the file does not exist, it handles the 
    exception gracefully.

    Returns:
    list: A list of logs loaded from the CSV file.
    """
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
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
        #TODO: Handle the case where the file doesn't exists yet.
        pass
    return logs

@app.route('/test_load_logs', methods=['GET'])
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


def save_log(log):
    """
    Save a log to the CSV file.

    This function saves a log to the specified CSV file. If the file does not exist,
    it creates a new file with headers.

    Args:
    log (dict): The log to save.
    """
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=
                                ['record_id', 'start_time', 'end_time', 'duration', 'category'])
        if not file_exists:
            writer.writeheader()
        writer.writerow(log)

@app.route('/test_save_log', methods=['POST'])
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


@app.route('/logs', methods=['GET'])
def get_logs():
    """
    Get all logs.

    This view function handles the '/logs' URL and returns all the logs loaded from the
    CSV file.

    Returns:
    Response: A JSON response with all the logs.
    """
    loaded_logs = load_logs()
    return jsonify(loaded_logs)


@app.route('/add_log', methods=['POST'])
def add_log():
    """
    Add a new log.

    This view function handles the '/add_log' URL and adds a new log to the CSV file.

    Returns:
    Response: A JSON response with the added log.
    """
    data = request.json
    log = {
        'record_id': data['record_id'],
        'duration': data['duration'],
        'category': data['category']
    }
    save_log(log)
    return jsonify(log), 201

def load_categories(category):
    """
    Load a category into the categories list.

    This function strips any leading or trailing whitespace from the provided category
    and adds it to the categories list if it is not already present.

    Args:
    category (str): The category to load.
    """
    strip_cat = category.strip()
    if strip_cat not in categories:
        categories.append(strip_cat)


@app.route('/test_load_categories', methods=['GET'])
def test_load_categories():
    """
    Test loading of categories.

    This view function handles the '/test_load_categories' URL and tests the loading of
    categories by calling the load_logs function, which also imports categories.

    Returns:
    list: The list of loaded categories.
    """
    load_logs()
    return categories


@app.route('/retrieve_categories', methods=['GET'])
def retrieve_categories():
    """
    Retrieve all categories.

    This view function handles the '/retrieve_categories' URL and returns all the
    categories that have been loaded.

    Returns:
    Response: A JSON response with all the categories.
    """
    return jsonify({"categories": categories}), 200

# Load logs at the start of the program
load_logs()
