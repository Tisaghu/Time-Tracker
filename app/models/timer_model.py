from datetime import datetime

class TimerModel:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.is_running = False

    def start(self):
        if self.is_running:
            return False, "Timer is already running"
        self.start_time = datetime.now()
        self.is_running = True
        return True, "Timer started"
    
    def stop(self):
        if not self.is_running:
            return False, "Timer is not running"
        self.end_time = datetime.now()
        self.is_running = False
        elapsed_time = self.calculate_elapsed_time()
        return True, {"message": "Timer stopped", "elapsed_time": elapsed_time}
    
    def reset(self):
        self.start_time = None
        self.end_time = None
        self.is_running = False
        return "Timer reset"
    
    def calculate_elapsed_time(self):
        if not self.start_time:
            return "00:00:00"
        elapsed_time = (self.end_time or datetime.now()) - self.start_time
        hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"