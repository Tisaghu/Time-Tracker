from app.storage.log_storage import LogStorage

class LogService:
    def __init__(self):
        self.storage = LogStorage()

    def get_logs(self):
        return self.storage.load_logs()
    
    def add_log(self, data):
        log = {
            'record_id': data.get('record_id'),
            'start_time': data.get('start_time', ''),
            'end_time': data.get('end_time', ''),
            'duration': data.get('duration', ''),
            'category': data.get('category', '')
        }
        self.storage.save_log(log)
        return log
    
    
