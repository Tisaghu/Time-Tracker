from app.storage.log_storage import LogStorage

class LogService:
    def __init__(self):
        self.storage = LogStorage()

    def get_logs(self):
        return self.storage.load_logs()
    

