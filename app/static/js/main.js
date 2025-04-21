import { API } from './api.js';
import { startTimer, stopOrResetTimer } from './timer.js';
import { updateCategoriesOnLoad, selectCategory } from './categories.js';
import { addLog } from './logs.js'; 


document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded');
    initializeButtons();
    initializeCategories();
    //updateCategoriesOnLoad();
});


function initializeButtons() {
    const startButton = document.getElementById('startButton');
    const stopButton = document.getElementById('stopButton');
    const saveButton = document.getElementById('saveButton');

    if (startButton) {
        startButton.addEventListener('click', startTimer);
    }

    if (stopButton) {
        stopButton.addEventListener('click', stopOrResetTimer);
    }

    if(saveButton) {
        saveButton.addEventListener('click', addLog);
    }
    else
    {
        console.log("Save button not found");
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