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
                    CategoryStorage.load_categories_from_csv(row['category'])
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
        raw_start_time = data.get('startTime', '')
        raw_end_time = data.get('endTime', '')
        raw_duration = data.get('duration')
        raw_category = data.get('category')

        formatted_start_time = self._format_datetime(raw_start_time)
        formatted_end_time = self._format_datetime(raw_end_time)

        #format duration
        formatted_duration = self._format_duration(raw_duration)

        log = {
            'record_id': self._get_next_record_id(self.CSV_FILE),
            'start_time': formatted_start_time,
            'end_time': formatted_end_time,
            'duration': formatted_duration,
            'category': raw_category
        }
        self.save_log(log)
        return log
    
    def _get_next_record_id(self, CSV_FILE):
        try:
            with open(CSV_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                record_ids = [int(row['record_id']) for row in reader if row['record_id'].isdigit()]
                return max(record_ids, default=0) + 1
        except FileNotFoundError:
            return 1
        
    def _format_datetime(self, iso_datetime_str):
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
        
    def _format_duration(self, total_seconds):
        # Convert total seconds into HH:MM:SS format
        if total_seconds is None:
            return ""
        
        try:
            total_seconds = int(total_seconds)

            if total_seconds < 0:
                print(f"Warning: Received negative duration ({total_seconds}s). Formatting as 00:00:00.")
                total_seconds = 0

            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        except (ValueError, TypeError) as e:
            print(f"Warning: Could not format duration '{total_seconds}'. Must be a number. Error: {e}")
            return ""