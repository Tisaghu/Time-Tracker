from datetime import datetime

class TimerModel:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.is_running = False
        self.can_be_resumed = False

    def start(self):
        if self.is_running:
            return False, "Timer is already running"
        elif self.can_be_resumed:
            return self.resume()
        self.start_time = datetime.now()
        self.is_running = True
        return True, {"message": "Timer started", "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S")}
    
    def resume(self):
        self.is_running = True
        return True, {"message": "Timer resumed", "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S")}
    
    def stop(self):
        if not self.is_running:
            return False, "Timer is not running"
        self.end_time = datetime.now()
        self.is_running = False
        self.can_be_resumed = True
        elapsed_time = self.calculate_elapsed_time()
        return True, {"message": "Timer stopped",
                      "elapsed_time": elapsed_time,
                      "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                      "end_time": self.end_time.strftime("%Y-%m-%d %H:%M:%S")}
    
    def reset(self):
        self.start_time = None
        self.end_time = None
        self.is_running = False
        self.can_be_resumed = False
        return "Timer reset"
    
    def calculate_elapsed_time(self):
        if not self.start_time:
            return "00:00:00"
        elapsed_time = (self.end_time or datetime.now()) - self.start_time
        hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def format_time(self, time):
        pass  # Placeholder for future formatting logic