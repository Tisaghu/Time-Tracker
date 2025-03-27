from flask import Blueprint, jsonify, request
import csv
import os

log_bp = Blueprint('log', __name__)

CSV_FILE = './time_records.csv'
IMPORT_CSV_FILE = './history.csv'

# In-memory categories (avoid duplicate categories)
CATEGORIES = []
LOGS = []

# Load Logs from CSV, also gets categories and loads them to the CATEGORIES list
# This function is called in the get_logs function
def load_logs():
    logs = []
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                load_categories_from_csv(row['category'])  # Load categories dynamically
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
@log_bp.route('/save', methods=['POST'])
def save_log(log):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['record_id', 'start_time', 'end_time', 'duration', 'category'])
        if not file_exists:
            writer.writeheader()
        writer.writerow(log)


# Loads all categories contained in the csv file to the CATEGORIES list
# This function is called in the load_logs function
def load_categories_from_csv(category):
    strip_cat = category.strip()
    if strip_cat not in CATEGORIES:
        CATEGORIES.append(strip_cat)
    update_categories_file()


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
    load_categories_from_csv(log['category'])
    return jsonify(log), 201


@log_bp.route('/categories', methods=['GET'])
def retrieve_categories():
    load_logs()  # Ensure categories are loaded from logs (csv file)
    # Save categories to text file
    update_categories_file()
    return jsonify({"categories": CATEGORIES}), 200


def update_categories_file():
    #check if file exists
    if os.path.isfile('categories.txt'):
        #read the file and update the CATEGORIES list
        with open('categories.txt', 'r') as f:
            for line in f:
                category = line.strip()
                if category not in CATEGORIES:
                    CATEGORIES.append(category)

    #create the file and write the categories to it
    with open('categories.txt', 'w') as f:
        for category in CATEGORIES:
            f.write(category + '\n')


@log_bp.route('/add_category', methods=['POST'])
def add_category():
    data = request.json # Get JSON data from the request
    category = data.get('category', '').strip()

    if not category:
        return jsonify({"error": "Invalid category"}), 400
    
    if category in CATEGORIES:
        return jsonify({"error": "Category already exists"}), 400
    
    CATEGORIES.append(category)
    return jsonify({"message": "Category added successfully"})

