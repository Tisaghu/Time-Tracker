import csv
import os
from app.storage.category_storage import CategoryStorage

class LogStorage:
    CSV_FILE = './time_records.csv'
    IMPORT_CSV_FILE = './history.csv'
    CATEGORIES = []
    
    def __init__(self):
        self.load_logs()  # Load logs & categories from log file on startup

    # Load Logs from CSV, also gets categories and loads them to the CATEGORIES list
    def load_logs(self):
        logs = []
        try:
            with open(self.CSV_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    CategoryStorage.load_categories_from_csv(self, row['category'])
                    logs.append(row)
        except FileNotFoundError:
            pass
        return logs

    def save_log(self, log):
        file_exists = os.path.isfile(self.CSV_FILE)
        with open(self.CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['record_id', 'start_time', 'end_time', 'duration', 'category'])
            if not file_exists:
                writer.writeheader()
            writer.writerow(log)

    def add_log(self, data):
        print("Received log:", data)
        log = {
            'record_id': data.get('record_id'),
            'start_time': data.get('start_time', ''),
            'end_time': data.get('end_time', ''),
            'duration': data.get('duration', ''),
            'category': data.get('category', '')
        }
        self.save_log(log)
        return log