import csv
import os

class LogStorage:
    CSV_FILE = './time_records.csv'
    IMPORT_CSV_FILE = './history.csv'
    CATEGORIES = []
    
    def __init__(self):
        self.load_logs()  # Load logs & categories on startup

    def load_logs(self):
        logs = []
        try:
            with open(self.CSV_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.load_categories(row['category'])
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

    def load_categories(self, category):
        category.strip()
        if category and category not in self.CATEGORIES:
            self.CATEGORIES.append(category)
        return self.CATEGORIES

    def add_category(self, category):
        self.CATEGORIES.append(category)
        self.update_categories_file()

    def update_categories_file(self):
        with open('categories.txt', 'w') as f:
            for category in self.CATEGORIES:
                f.write(category + '\n')
