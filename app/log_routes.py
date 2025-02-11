from flask import Blueprint, jsonify, request
import csv
import os

log_bp = Blueprint('log', __name__)

CSV_FILE = './time_records.csv'
IMPORT_CSV_FILE = './history.csv'

# In-memory categories (avoid duplicate categories)
categories = []

# Load Logs from CSV
def load_logs():
    logs = []
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                load_categories(row['category'])  # Load categories dynamically
                logs.append(row)
    except FileNotFoundError:
        pass
    return logs

# Import Logs from External CSV
def import_logs():
    logs = []
    try:
        with open(IMPORT_CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                logs.append({
                    'record_id': row.get('RECORD ID', ''),
                    'start_time': row.get(' START TIME', ''),
                    'end_time': row.get(' END TIME', ''),
                    'duration': row.get(' DURATION', ''),
                    'category': row.get(' ACTIVITY NAME', '')
                })
    except FileNotFoundError:
        pass
    return logs

# Save a Single Log to CSV
def save_log(log):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['record_id', 'start_time', 'end_time', 'duration', 'category'])
        if not file_exists:
            writer.writeheader()
        writer.writerow(log)

# Load Unique Categories
def load_categories(category):
    strip_cat = category.strip()
    if strip_cat not in categories:
        categories.append(strip_cat)

# API Routes
@log_bp.route('/', methods=['GET'])
def get_logs():
    return jsonify(load_logs()), 200

@log_bp.route('/add', methods=['POST'])
def add_log():
    data = request.json
    log = {
        'record_id': data.get('record_id'),
        'start_time': data.get('start_time', ''),
        'end_time': data.get('end_time', ''),
        'duration': data.get('duration', ''),
        'category': data.get('category', '')
    }
    save_log(log)
    load_categories(log['category'])
    return jsonify(log), 201

@log_bp.route('/categories', methods=['GET'])
def retrieve_categories():
    load_logs()  # Ensure categories are loaded from logs
    return jsonify({"categories": categories}), 200
