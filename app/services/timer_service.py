from app.models.timer_model import TimerModel

# Create a global timer instance
timer = TimerModel()

def start_timer():
    success, response = timer.start()
    if success:
        return response, 201
    return {"error": response}, 409

def stop_timer():
    success, response = timer.stop()
    if success:
        return response, 201
    return {"error": response}, 409

def reset_timer():
    return {"message": timer.reset()}, 200

def check_elapsed_time():
    return {"elapsed_time": timer.calculate_elapsed_time()}, 200
