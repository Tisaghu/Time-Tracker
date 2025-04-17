from app.models.timer_model import TimerModel

# Create a global timer instance
timer = TimerModel()

def start_timer():
    success, response = timer.start()
    return response, 201 if success else ({"error": response}, 409)

def stop_timer():
    success, response = timer.stop()
    return response, 201 if success else ({"error": response}, 409)

def reset_timer():
    return {"message": timer.reset()}, 200

def check_elapsed_time():
    return {"elapsed_time": timer.calculate_elapsed_time()}, 200
