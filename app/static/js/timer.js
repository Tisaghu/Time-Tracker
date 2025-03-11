// timer.js

import { API } from './api.js';

let timerRunning = false;
let timerWasRun = false;
let canBeResumed = false;
let canBeReset = false;
let intervalId;
let seconds = 0, minutes = 0, hours = 0;
let currentCategory = 'None';

export function startTimer() {
    API.startTimer().then(data => {
        document.getElementById('status').innerText = data.message;

        //Show the "status" and "elapsed_time" boxes when the timer starts
        document.getElementById("status").style.display = "block";
        
        
        timerRunning = true;
        timerWasRun = true;
        clearInterval(intervalId);
        intervalId = setInterval(updateTimer, 1000);

        updateStartButton('Timer Running', true, ['btn-secondary'], canBeResumed ? ['btn-success'] : ['btn-primary']);
        if (canBeReset) updateStopButton('Stop Timer');

        canBeReset = true;
    });
}

export function stopOrResetTimer() {
    const stopButton = document.getElementById('stopButton');
    if (stopButton.innerText === 'Reset Timer') {
        //hide elapsed time box on reset
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
        document.getElementById('elapsed_time').innerHTML = `
            <strong>Elapsed Time:</strong> ${data.elapsed_time}
            <br>
            <strong>Category:</strong> ${currentCategory}
        `;

        clearInterval(intervalId);
        timerRunning = false;

        if (timerWasRun && !timerRunning) {
            updateStartButton('Resume Timer', false, ['btn-success'], ['btn-secondary']);
            updateStopButton('Reset Timer');
            canBeResumed = true;
            canBeReset = true;
        }
    });
}

export function resetTimer() {
    seconds = minutes = hours = 0;
    updateTimerDisplay();
    document.getElementById('elapsed_time').innerText = '';
    document.getElementById('status').innerText = 'Timer Reset';

    updateStartButton('Start Timer', false, ['btn-primary'], ['btn-secondary', 'btn-success']);
    updateStopButton('Stop Timer');

    timerWasRun = timerRunning = canBeResumed = canBeReset = false;
}

export function checkElapsedTime() {
    if (timerRunning) {
        API.checkElapsedTime().then(data => {
            document.getElementById('elapsed_time').innerText = `Elapsed Time: ${data.elapsed_time}`;
        });
    }
}

// Timer Helper Functions
function updateTimer() {
    seconds++;
    if (seconds >= 60) {
        seconds = 0;
        minutes++;
        if (minutes >= 60) {
            minutes = 0;
            hours++;
        }
    }
    updateTimerDisplay();
}

function updateTimerDisplay() {
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

function hideInitialFields() {
    document.getElementById("status").style.display = "none";
    document.getElementById("elapsed_time").style.display = "none";
    document.getElementById("saveButton").style.display = "none";
}

document.addEventListener("DOMContentLoaded", hideInitialFields)