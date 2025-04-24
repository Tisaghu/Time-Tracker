import { API } from './api.js';
import { _setCurrentCategory } from './timer.js';


document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM fully loaded and parsed");

    //Get global variables after ensuring DOM content loaded
    const categoryDropdown = document.getElementById('categoryDropdown');
    const dropdownMenuButton = document.getElementById('dropdownMenuButton');

    if(!categoryDropdown) {
        console.error("ERROR: Could not find element with ID 'categoryDropdown' in the HTML.");
    }

    updateCategoriesOnLoad();
})

export function updateCategoriesOnLoad() {
    console.log("Running updateCategoriesOnLoad()"); //Debugging

    if(!categoryDropdown) {
        console.error("Category dropdown not found!");
        return;
    }

    categoryDropdown.innerHTML = ''; // Clear existing items before adding new categories

    API.getCategories().then(data => {

        if(!data || !data.categories) {
            console.error("No categories found in API response!");
            return;
        }


        if (data.categories.length === 0) {
            console.log("No categories found, adding 'No Categories' message.")
            const noCategoriesItem = document.createElement('a');
            noCategoriesItem.className = 'dropdown-item';
            noCategoriesItem.href = '#';
            noCategoriesItem.textContent = 'No Categories';
            categoryDropdown.appendChild(noCategoriesItem);
        } else {
            data.categories.forEach(category => {
                addCategoryToDropdown(category);
            });
            console.log("Successfully added all categories to dropdown."); //Debugging
        }

        // Add the input field and button dynamically
        addCategoryInputField();
    });
}

function addCategoryToDropdown(categoryName) {
    if(!categoryDropdown) {
        console.error("Category dropdown not found!");
        return;
    }

    // Create the new category element
    const categoryItem = document.createElement('a');
    categoryItem.className = 'dropdown-item';
    categoryItem.href = '#';
    categoryItem.textContent = categoryName;
    categoryItem.addEventListener('click', () => selectCategory(categoryName));

    //Insert the new category before the input field and button
    categoryDropdown.insertBefore(categoryItem, categoryDropdown.lastChild);

    }

function addCategoryInputField() {

    if(!categoryDropdown) {
        console.error("addCategoryInputField: categoryDropdown not found!");
        return;
    }

    if(categoryDropdown.querySelector('#addCategoryButton')) {
        console.log("Input field already exists, skipping add.");
        return;
    }

    // Separator line
    const divider = document.createElement('div');
    divider.className = 'dropdown-divider';
    categoryDropdown.appendChild(divider);

    // Container for input field and button
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
            API.addCategory(newCategory)
            .then(() => {
                console.log("Successfully added new category:", newCategory);
                addCategoryToDropdown(newCategory);
                newCategoryInput.value = ''; // Clear the input field
            })
            .catch(error => console.error("Error adding category:", error));
        }
    })
}




export function selectCategory(categoryName) {
    document.getElementById('dropdownMenuButton').textContent = categoryName;
    _setCurrentCategory(categoryName); // Update the timer with the selected category
}
