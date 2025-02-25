// categories.js

import { API } from './api.js';
import { setCurrentCategory } from './timer.js';

export function updateCategoriesOnLoad() {
    API.getCategories().then(data => {
        console.log("Fetched categories from API:", data); //Debugging

        //const categoryDropdown = document.getElementById('categoryDropdown');
        //categoryDropdown.innerHTML = ''; // Clear existing items

        if (data.categories.length === 0) {
            console.log("No categories found, adding 'No Categories' message.")
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

        // Add the input field and button dynamically
        addCategoryInputField();
    });
}

function addCategoryInputField() {
    const categoryDropdown = document.getElementById('categoryDropdown');

    // Separator line
    const divider = document.createElement('div');
    divider.className = 'dropdown-divider';
    categoryDropdown.appendChild(divider);

    // Input field + button container
    const inputContainer = document.createElement('div');
    inputContainer.className = 'd-flex p-2';

    // Input field
    const newCategoryInput = document.createElement('input');
    newCategoryInput.type = 'text';
    newCategoryInput.className = 'form-control';
    newCategoryInput.id = 'newCategoryInput';
    newCategoryInput.placeholder = 'New Category';

    // Add button
    const addButton = document.createElement('button');
    addButton.className = 'btn btn-sm btn-success ml-2';
    addButton.textContent = '+';
    addButton.id = 'addCategoryButton';

    // Append elements
    inputContainer.appendChild(newCategoryInput);
    inputContainer.appendChild(addButton);
    categoryDropdown.appendChild(inputContainer);

    // Button exists, add event listener
    addButton.addEventListener('click', () => {
        const newCategory = newCategoryInput.value.trim();
        if(newCategory) {
            console.log("New Category Entered:", newCategory);
        }
    })
}




export function selectCategory(categoryName) {
    document.getElementById('dropdownMenuButton').textContent = categoryName;
    setCurrentCategory(categoryName); // Update the timer with the selected category
}
