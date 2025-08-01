import { API } from './api.js';
import { TimerState } from './timer.js'; 

export function addLog() {
    let category = TimerState.currentCategory; 
    if (!category) {
        console.error("Category is not defined");
        return;
    }
    let start_time = TimerState.startTime;
    let end_time = TimerState.endTime; 
    let duration = calculateDuration(start_time, end_time);

    API.addLog(category,start_time,end_time,duration);
};

function calculateDuration(start_time, end_time) {
    if (!start_time || !end_time) {
        console.error("Error finding duration: Start time or end time is not defined");
        return;
    }

    let duration = (new Date(end_time) - new Date(start_time)) / 1000; // Duration in seconds
    return duration;
}