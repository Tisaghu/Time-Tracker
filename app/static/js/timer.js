import { API } from './api.js';

// Timer State
let timerRunning = false;
let timerWasRun = false;
let canBeResumed = false;
let canBeReset = false;
let intervalId;
let elapsedSeconds = 0; // Single source of truth for time
export let currentCategory = 'None';

// Button Text Constants
const BUTTON_TEXT = {
    START: "Start Timer",
    STOP: "Stop Timer",
    RESET: "Reset Timer",
    RESUME: "Resume Timer",
    RUNNING: "Timer Running"
};

export function startTimer() {
    API.startTimer().then(data => {
        document.getElementById('status').innerText = data.message;

        // Show the "status" and "elapsed_time" boxes when the timer starts
        document.getElementById("status").style.display = "block";

        timerRunning = true;
        timerWasRun = true;
        clearInterval(intervalId);
        intervalId = setInterval(updateTimer, 1000);

        updateStartButton(BUTTON_TEXT.RUNNING, true, ['btn-secondary'], canBeResumed ? ['btn-success'] : ['btn-primary']);
        if (canBeReset) updateStopButton(BUTTON_TEXT.STOP);

        canBeReset = true;
    });
}

export function stopOrResetTimer() {
    const stopButton = document.getElementById('stopButton');
    if (stopButton.innerText === BUTTON_TEXT.RESET) {
        // Hide elapsed time box on reset
        document.getElementById("elapsed_time").style.display = "none";
        document.getElementById("saveButton").style.display = "none";
        resetTimer();
    } else {
        document.getElementById("elapsed_time").style.display = "block";
        document.getElementById("saveButton").style.display = "";
        stopTimer();
    }
}

export function stopTimer() {
    API.stopTimer().then(data => {
        document.getElementById('status').innerText = data.message;
        console.log(data);
        document.getElementById('elapsed_time').innerHTML = `
            <strong>Category:</strong> ${currentCategory}
            <br>
            <strong>Start Time:</strong> ${data.start_time}
            <br>
            <strong>End Time:</strong> ${data.end_time}
        `;

        clearInterval(intervalId);
        timerRunning = false;

        if (timerWasRun && !timerRunning) {
            updateStartButton(BUTTON_TEXT.RESUME, false, ['btn-success'], ['btn-secondary']);
            updateStopButton(BUTTON_TEXT.RESET);
            canBeResumed = true;
            canBeReset = true;
        }
    });
}

export function resetTimer() {
    API.resetTimer().then(data => {
        document.getElementById('status').innerText = data.message;
        elapsedSeconds = 0; // Reset elapsed time
        updateTimerDisplay();
        document.getElementById('elapsed_time').innerText = '';
        document.getElementById('status').innerText = 'Timer Reset';

        updateStartButton(BUTTON_TEXT.START, false, ['btn-primary'], ['btn-secondary', 'btn-success']);
        updateStopButton(BUTTON_TEXT.STOP);

        timerWasRun = timerRunning = canBeResumed = canBeReset = false;
    });
}

// Timer Helper Functions
function updateTimer() {
    elapsedSeconds++; // Increment elapsed time
    updateTimerDisplay();
}

function updateTimerDisplay() {
    const hours = Math.floor(elapsedSeconds / 3600);
    const minutes = Math.floor((elapsedSeconds % 3600) / 60);
    const seconds = elapsedSeconds % 60;
    document.getElementById('timer').innerHTML = `<strong>Total Elapsed Time:</strong> ${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
}

function pad(num) {
    return num.toString().padStart(2, '0');
}

function updateStartButton(text, disabled, addClasses, removeClasses) {
    const startButton = document.getElementById('startButton');
    startButton.innerText = text;
    startButton.disabled = disabled;
    startButton.classList.add(...addClasses);
    startButton.classList.remove(...removeClasses);
}

function updateStopButton(text) {
    document.getElementById('stopButton').innerText = text;
}

export function setCurrentCategory(category) {
    currentCategory = category;
}

export function getCurrentCategory(category) {
    return currentCategory;
}

function hideInitialFields() {
    document.getElementById("status").style.display = "none";
    document.getElementById("elapsed_time").style.display = "none";
    document.getElementById("saveButton").style.display = "none";
}

document.addEventListener("DOMContentLoaded", hideInitialFields);