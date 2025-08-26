from datetime import datetime

class TimerModel:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.is_running = False
        self.can_be_resumed = False

    def start(self):
        """Starts the timer. 
        
        Returns: True if timer was started, and message showing that the timer has has started 
        and what time it was started at. If Timer is already running then returns false with message indicating that
        it has already been started."""
        if self.is_running:
            return False, "Timer is already running"
        elif self.can_be_resumed:
            return self.resume()
        self.start_time = datetime.now()
        self.is_running = True
        return True, {"message": "Timer started", "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S")}
    
    def resume(self):
        """Resumes the timer. Changes is_running variable to True and 
        
        Returns: Boolean result of resume along with status message."""
        self.is_running = True
        return True, {"message": "Timer resumed", "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S")}
    
    def stop(self):
        """Checks that the timer is running then stops it. Sets end_time variable, and other state variables to 
        indicate that the timer has stopped.

        Returns: boolean result of stopping, and message with more information about the stop"""
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
    
    #TODO: This should probably return True/False, as well as the message.
    def reset(self):
        """Resets the timer model to default state.
        
        Returns: Message indicating timer has been reset."""
        self.start_time = None
        self.end_time = None
        self.is_running = False
        self.can_be_resumed = False
        return "Timer reset"
    
    def calculate_elapsed_time(self):
        """Calculates how much time has elapsed since between start_time and end_time.
        
        Returns: Formatted string with elapsed time."""
        if not self.start_time:
            return "00:00:00"
        elapsed_time = (self.end_time or datetime.now()) - self.start_time
        hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    
    def format_time(self, time):
        pass  # Placeholder for future formatting logic