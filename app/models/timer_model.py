from datetime import datetime

class TimerModel:
    """
    A model representing a simple timer with start, stop, resume, reset, and elapsed time calculation functionality.
    Tracks the timer's state and provides methods to control and query the timer.
    """
    def __init__(self):
        """
        Initialize a new TimerModel instance with default state (not running, not resumable).
        """
        self.start_time = None
        self.end_time = None
        self.is_running = False
        self.can_be_resumed = False

    def start(self):
        """
        Start the timer. If already running, returns an error. If resumable, resumes instead.

        Returns:
            tuple: (success (bool), response (str or dict))
        """
        if self.is_running:
            return False, "Timer is already running"
        elif self.can_be_resumed:
            return self.resume()
        self.start_time = datetime.now()
        self.is_running = True
        return True, {"message": "Timer started", "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S")}
    
    def resume(self):
        """
        Resume the timer from a paused state. Assumes start_time is set.

        Returns:
            tuple: (success (bool), response (dict))
        """
        self.is_running = True
        return True, {"message": "Timer resumed", "start_time": self.start_time.strftime("%Y-%m-%d %H:%M:%S")}
    
    def stop(self):
        """
        Stop the timer. If not running, returns an error. Otherwise, records end time and calculates elapsed time.

        Returns:
            tuple: (success (bool), response (dict))
        """
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
        """
        Reset the timer to its initial state (clears start and end times, running and resumable flags).

        Returns:
            str: Confirmation message.
        """
        self.start_time = None
        self.end_time = None
        self.is_running = False
        self.can_be_resumed = False
        return "Timer reset"
    
    def calculate_elapsed_time(self):
        """
        Calculate the elapsed time between start and end (or now if running).

        Returns:
            str: Elapsed time in HH:MM:SS format, or '00:00:00' if not started.
        """
        if not self.start_time:
            return "00:00:00"
        elapsed_time = (self.end_time or datetime.now()) - self.start_time
        hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def format_time(self, time):
        """
        Placeholder for future time formatting logic.

        Args:
            time (datetime): The datetime object to format.
        Returns:
            str: Formatted time string (to be implemented).
        """
        pass  # Placeholder for future formatting logic