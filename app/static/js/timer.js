import { API } from './api.js';

// Timer State
const TimerState = {
    timerRunning: false,
    timerWasRun: false,
    canBeResumed: false,
    canBeReset: false,
    intervalId: null,
    elapsedSeconds: 0, 
    currentCategory: 'None',
    startTime: null,
    endTime: null
};

export let { currentCategory } = TimerState;

// Export TimerState directly
export { TimerState };

// Button Text Constants
const BUTTON_TEXT = {
    START: "Start Timer",
    STOP: "Stop Timer",
    RESET: "Reset Timer",
    RESUME: "Resume Timer",
    RUNNING: "Timer Running"
};

// Element Constants
const ELEMENTS = {
    status: _getElement('status'),
    elapsedTime: _getElement('elapsed_time'),
    saveButton: _getElement('saveButton'),
    startButton: _getElement('startButton'),
    stopButton: _getElement('stopButton'),
    timer: _getElement('timer')
};


export function startTimer() {
    API.startTimer().then(data => {
        TimerState.timerRunning = true;
        TimerState.timerWasRun = true;
        TimerState.canBeReset = true;
        TimerState.startTime = new Date(data.start_time)
        ELEMENTS.status.innerText = data.message;

        // Show the "status" and "elapsed_time" boxes when the timer starts
        _showElement(ELEMENTS.status);

        clearInterval(TimerState.intervalId);
        TimerState.intervalId = setInterval(updateTimer, 1000);

        updateStartButton(
            BUTTON_TEXT.RUNNING,
            true,
            ['btn-secondary'],
            TimerState.canBeResumed ? ['btn-success'] : ['btn-primary']
        );
        if (TimerState.canBeReset) updateStopButton(BUTTON_TEXT.STOP);
    });
}

export function stopOrResetTimer() {
    if (ELEMENTS.stopButton.innerText === BUTTON_TEXT.RESET) {
        // Hide elapsed time box on reset
        _hideElement(ELEMENTS.elapsedTime);
        _hideElement(ELEMENTS.saveButton);
        resetTimer();
    } else {
        _showElement(ELEMENTS.elapsedTime);
        _showElement(ELEMENTS.saveButton);
        stopTimer();
    }
}

export function stopTimer() {
    API.stopTimer().then(data => {
        TimerState.timerRunning = false;
        TimerState.endTime = new Date(data.end_time);

        //Display "Timer Stopped" message
        ELEMENTS.status.innerText = data.message;
        ELEMENTS.elapsedTime.innerHTML = `
            <strong>Category:</strong> ${TimerState.currentCategory}
            <br>
            <strong>Start Time:</strong> ${data.start_time}
            <br>
            <strong>End Time:</strong> ${data.end_time}
        `;

        clearInterval(TimerState.intervalId);

        if (TimerState.timerWasRun && !TimerState.timerRunning) {
            updateStartButton(BUTTON_TEXT.RESUME, false, ['btn-success'], ['btn-secondary']);
            updateStopButton(BUTTON_TEXT.RESET);
            TimerState.canBeResumed = true;
            TimerState.canBeReset = true;
        }
    });
}

export function resetTimer() {
    API.resetTimer().then(data => {
        TimerState.timerWasRun = TimerState.timerRunning = TimerState.canBeResumed = TimerState.canBeReset = false;

        ELEMENTS.status.innerText = data.message;
        TimerState.elapsedSeconds = 0; // Reset elapsed time
        updateTimerDisplay();
        ELEMENTS.elapsedTime.innerText = '';
        ELEMENTS.status.innerText = 'Timer Reset';

        updateStartButton(BUTTON_TEXT.START, false, ['btn-primary'], ['btn-secondary', 'btn-success']);
        updateStopButton(BUTTON_TEXT.STOP);
    });
}

// Timer Helper Functions
function updateTimer() {
    TimerState.elapsedSeconds++; // Increment elapsed time
    updateTimerDisplay();
}

function updateTimerDisplay() {
    const hours = Math.floor(TimerState.elapsedSeconds / 3600);
    const minutes = Math.floor((TimerState.elapsedSeconds % 3600) / 60);
    const seconds = TimerState.elapsedSeconds % 60;
    ELEMENTS.timer.innerHTML = `<strong>Total Elapsed Time:</strong> ${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
}

function pad(num) {
    return num.toString().padStart(2, '0');
}

function updateStartButton(text, disabled, addClasses, removeClasses) {
    const startButton = ELEMENTS.startButton;
    startButton.innerText = text;
    startButton.disabled = disabled;
    startButton.classList.add(...addClasses);
    startButton.classList.remove(...removeClasses);
}

function updateStopButton(text) {
    ELEMENTS.stopButton.innerText = text;
}

// Utility function for getting elements
function _getElement(id) {
    return document.getElementById(id);
}

function _hideElement(element) {
    element.style.display = "none";
}

function _showElement(element) {
    element.style.display = "block";
}

function _hideInitialFields() {
    _hideElement(ELEMENTS.status);
    _hideElement(ELEMENTS.elapsedTime);
    _hideElement(ELEMENTS.saveButton);
}

document.addEventListener("DOMContentLoaded", _hideInitialFields);

// Getter and Setter Functions
export function _setCurrentCategory(category) {
    TimerState.currentCategory = category;
}

export function _getCurrentCategory() {
    return TimerState.currentCategory;
}