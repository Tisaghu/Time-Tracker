import csv
import os
from datetime import datetime, timezone
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

        #formate the datetime strings
        raw_start_time = data.get('startTime', '')
        raw_end_time = data.get('endTime', '')

        formatted_start_time = self.format_datetime(raw_start_time)
        formatted_end_time = self.format_datetime(raw_end_time)

        log = {
            'record_id': self.get_next_record_id(self.CSV_FILE),
            'start_time': formatted_start_time,
            'end_time': formatted_end_time,
            'duration': data.get('duration', ''),
            'category': data.get('category', '')
        }
        self.save_log(log)
        return log
    
    def get_next_record_id(self, CSV_FILE):
        try:
            with open(CSV_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                record_ids = [int(row['record_id']) for row in reader if row['record_id'].isdigit()]
                return max(record_ids, default=0) + 1
        except FileNotFoundError:
            return 1
        
    def format_datetime(self, iso_datetime_str):
        # Helper function to parse ISO string and format it
        if not iso_datetime_str:
            return ""
        try:
            if iso_datetime_str.endswith('Z'):
                dt_obj = datetime.fromisoformat(iso_datetime_str.replace('Z', '+00:00'))
            else:
                dt_obj = datetime.fromisoformat(iso_datetime_str)

            return dt_obj.strftime('%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError) as e:
            print(f"Warning: Could not parse datetime string '{iso_datetime_str}'. Error: {e}")
            return iso_datetime_str