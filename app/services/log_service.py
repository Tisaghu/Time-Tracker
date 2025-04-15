from app.storage.log_storage import LogStorage
from flask import jsonify

class LogService:
    def __init__(self):
        self.storage = LogStorage()

    def get_logs(self):
        return self.storage.load_logs()
    
    def add_log(self, data):
        print("Received log data:", data)
        message = self.storage.add_log(data)
        return message
