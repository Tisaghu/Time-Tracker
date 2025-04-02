import { API } from './api.js';
import { getCurrentCategory }  from './timer.js'

export function addLog() {
    console.log("addLog was called");
    //Need: start time, end time, duration, and category
    let category = getCurrentCategory();
    if (!category) {
        console.error("Category is not defined");
        return;
    }
    console.log("Category is:", category);

};