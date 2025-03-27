import { API } from './api.js';
import {  startTimer, stopOrResetTimer } from './timer.js';
import { updateCategoriesOnLoad, selectCategory } from './categories.js';

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded');

    API.initTimer().then(data => {
        console.log('Timer initialized:', data);
    });
    //initializeTimerText();
    initializeButtons();
    initializeCategories();
    updateCategoriesOnLoad();
});


function initializeTimerText() {
    const timer = document.getElementById('timer');
    if (timer) {
        timer.innerHTML = `<strong>Total Elapsed Time:</strong> 00:00:00`;
    }
}


function initializeButtons() {
    const startButton = document.getElementById('startButton');
    const stopButton = document.getElementById('stopButton');

    if (startButton) {
        startButton.addEventListener('click', startTimer);
    }

    if (stopButton) {
        stopButton.addEventListener('click', stopOrResetTimer);
    }
}


function initializeCategories() {
    // Attach click events to category dropdown items
    const categoryItems = document.querySelectorAll('#categoryDropdown .dropdown-item');
    categoryItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const category = item.getAttribute('data-category');
            selectCategory(category);
        });
    });
}