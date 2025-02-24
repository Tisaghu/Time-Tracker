// categories.js

import { API } from './api.js';
import { setCurrentCategory } from './timer.js';

export function updateCategoriesOnLoad() {
    API.getCategories().then(data => {
        const categoryDropdown = document.getElementById('categoryDropdown');
        categoryDropdown.innerHTML = ''; // Clear existing items

        if (data.categories.length === 0) {
            const noCategoriesItem = document.createElement('a');
            noCategoriesItem.className = 'dropdown-item';
            noCategoriesItem.href = '#';
            noCategoriesItem.textContent = 'No Categories';
            categoryDropdown.appendChild(noCategoriesItem);
        } else {
            data.categories.forEach(category => {
                const categoryItem = document.createElement('a');
                categoryItem.className = 'dropdown-item';
                categoryItem.href = '#';
                categoryItem.textContent = category;
                categoryItem.onclick = () => selectCategory(category);
                categoryDropdown.appendChild(categoryItem);
            });
        }
    });
}

export function selectCategory(categoryName) {
    document.getElementById('dropdownMenuButton').textContent = categoryName;
    setCurrentCategory(categoryName); // Update the timer with the selected category
}
