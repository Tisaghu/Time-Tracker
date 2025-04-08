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
};