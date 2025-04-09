import { API } from './api.js';
import { TimerState } from './timer.js'; 

export function addLog() {
    console.log("addLog was called");
    // Need: start time, end time, duration, and category
    let category = TimerState.currentCategory; 
    if (!category) {
        console.error("Category is not defined");
        return;
    }
    console.log("Category is:", category);
    let start_time = TimerState.startTime;
    let end_time = TimerState.endTime; 

    console.log("Start Time:", start_time);
    console.log("End Time:", end_time);

    let duration = calculateDuration(start_time, end_time)
};

function calculateDuration(start_time, end_time) {
    if (!start_time || !end_time) {
        console.error("Error finding duration: Start time or end time is not defined");
        return;
    }

    let duration = (new Date(end_time) - new Date(start_time)) / 1000; // Duration in seconds
    console.log("Duration (in seconds):", duration);
    return duration;
}