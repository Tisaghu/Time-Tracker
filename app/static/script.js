// Constants for button texts
const START_TIMER_TEXT = 'Start Timer';
const STOP_TIMER_TEXT = 'Stop Timer';
const RESET_TIMER_TEXT = 'Reset Timer';
const TIMER_RUNNING_TEXT = 'Timer Running';
const RESUME_TIMER_TEXT = 'Resume Timer';
const TIMER_RESET_TEXT = 'Timer Reset';
const ELAPSED_TIME_TEXT = 'Elapsed Time: ';
const CATEGORY_TEXT = 'Category: ';
const TIMER_DISPLAY_TEXT = 'Total Elapsed Time: ';

// Timer state flags
let timerWasRun = false;
let timerRunning = false;
let canBeResumed = false;
let canBeReset = false;

let intervalId;
let currentCategory = 'None';

// Timer variables
let seconds = 0;
let minutes = 0;
let hours = 0;

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('timer').innerHTML = `<strong>${TIMER_DISPLAY_TEXT}</strong> 00:00:00`;
    updateCategoriesOnLoad();
})

async function startTimer() 
{
    const response = await fetch('/start_timer', { method: 'POST' });
    const data = await response.json();
    document.getElementById('status').innerText = data.message;
    timerRunning = true;
    timerWasRun = true;
    clearInterval(intervalId);
    intervalId = setInterval(updateTimer, 1000);

    updateStartButton(TIMER_RUNNING_TEXT, true, ['btn-secondary'], canBeResumed ? ['btn-success'] : ['btn-primary']);
    if (canBeReset) {
        updateStopButton(STOP_TIMER_TEXT);
    }
    canBeReset = true;
}

async function stopOrResetTimer() 
{
    const stopButton = document.getElementById('stopButton');
    if (stopButton.innerText === RESET_TIMER_TEXT) {
        resetTimer();
    } else {
        stopTimer();
    }
}

async function stopTimer() 
{
    const response = await fetch('/stop_timer', { method: 'POST' });
    const data = await response.json();
    document.getElementById('status').innerText = data.message;
    document.getElementById('elapsed_time').innerHTML = `
        <strong>${ELAPSED_TIME_TEXT}</strong>${data.elapsed_time} seconds
        <br>
        <strong>${CATEGORY_TEXT}</strong> ${currentCategory}
    `;
    
    clearInterval(intervalId);
    timerRunning = false;

    if (timerWasRun && !timerRunning) {
        updateStartButton(RESUME_TIMER_TEXT, false, ['btn-success'], ['btn-secondary']);
        updateStopButton(RESET_TIMER_TEXT);
        canBeResumed = true;
        canBeReset = true;
    }
}

function resetTimer() 
{
    seconds = 0;
    minutes = 0;
    hours = 0;
    updateTimerDisplay();
    document.getElementById('elapsed_time').innerText = '';
    document.getElementById('status').innerText = TIMER_RESET_TEXT;

    updateStartButton(START_TIMER_TEXT, false, ['btn-primary'], ['btn-secondary', 'btn-success']);
    updateStopButton(STOP_TIMER_TEXT);

    timerWasRun = false;
    timerRunning = false;
    canBeResumed = false;
    canBeReset = false;
}

async function checkElapsedTime() 
{
    if (timerRunning) {
        const response = await fetch('/check_elapsed_time');
        const data = await response.json();
        document.getElementById('elapsed_time').innerText = ELAPSED_TIME_TEXT + data.elapsed_time + ' seconds';
    }
}

function updateTimer() 
{
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

function updateTimerDisplay() 
{
    document.getElementById('timer').innerHTML = `<strong>${TIMER_DISPLAY_TEXT}</strong> ${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
}

function pad(num) 
{
    return num.toString().padStart(2, '0');
}

function selectCategory(categoryName) 
{
    document.getElementById('dropdownMenuButton').textContent = categoryName;
    currentCategory = categoryName;
}

async function updateCategoriesOnLoad()
{
    const response = await fetch('/retrieve_categories');
    const data = await response.json();
    const catgoryDropdown = document.getElementById('categoryDropdown');

    categoryDropdown.innerHTML = ''; // Clear existing dropdown items

    if(data.categories.length === 0)
    {
        const noCategoriesItem = document.createElement('a');
        categoryItem.className = 'dropdown-item';
        categoryItem.href = '#';
        categoryItem.textContent = 'No Categories';
        categoryDropdown.appendChild(noCategoriesItem);
    }
    else
    {
        data.categories.forEach(category => {
            const categoryItem = document.createElement('a');
            categoryItem.className = 'dropdown-item';
            categoryItem.href = '#';
            categoryItem.textContent = category;
            categoryItem.onclick = () => selectCategory(category);
            categoryDropdown.appendChild(categoryItem);
        });
    }
}

function updateStartButton(text, disabled, addClasses, removeClasses) 
{
    const startButton = document.getElementById('startButton');
    startButton.innerText = text;
    startButton.disabled = disabled;
    startButton.classList.add(...addClasses);
    startButton.classList.remove(...removeClasses);
}

function updateStopButton(text) 
{
    document.getElementById('stopButton').innerText = text;
}

// Call updateCategoriesOnLoad when the page loads
document.addEventListener('DOMContentLoaded', updateCategoriesOnLoad);