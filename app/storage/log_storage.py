import csv
import os

class LogStorage:
    CSV_FILE = './time_records.csv'
    IMPORT_CSV_FILE = './history.csv'
    CATEGORIES = []
    
    def __init__(self):
        self.load_logs()  # Load logs & categories from log file on startup
        self.load_categories_from_txt()  # Load any extra categories from text file

    # Load Logs from CSV, also gets categories and loads them to the CATEGORIES list
    def load_logs(self):
        logs = []
        try:
            with open(self.CSV_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.load_categories_from_csv(row['category'])
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



    #Categories
    #TODO: Seperate these into a different service

    def load_categories_from_csv(self, category):
        category = category.strip()
        if category and category not in self.CATEGORIES:
            self.CATEGORIES.append(category)
        return self.CATEGORIES
    
    def load_categories_from_txt(self):
        try:
            with open('categories.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and line not in self.CATEGORIES:
                        self.CATEGORIES.append(line)
        except FileNotFoundError:
            pass
    
    def get_categories(self):
        if not self.CATEGORIES:
            try:
                with open('categories.txt', 'r') as f:
                    self.CATEGORIES = [line.strip() for line in f.readlines() if line.strip()]
            except FileNotFoundError:
                pass
        return self.CATEGORIES

    def add_category(self, category):
        self.CATEGORIES.append(category)
        self.update_categories_file()


    def update_categories_file(self):
        with open('categories.txt', 'w') as f:
            for category in self.CATEGORIES:
                f.write(category + '\n')
