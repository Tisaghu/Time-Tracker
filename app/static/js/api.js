//Handles all API requests (fetch calls)
export const API = {
    startTimer: () => fetch('/timer/start', { method: 'POST' }).then(res => res.json()),
    stopTimer: () => fetch('/timer/stop', { method: 'POST' }).then(res => res.json()),
    checkElapsedTime: () => fetch('/timer/check').then(res => res.json()),
    getCategories: () => fetch('/logs/categories').then(res => res.json()),
    addCategory: (categoryName) => fetch('/logs/add_category', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({category: categoryName}) // Convert to JSON
    })
    .then(res => res.json())
    .then(data => console.log("Server Response:", data)) // Log response
    .catch(error => console.error("Fetch Error:", error)) // Handle errors
};


window.API = API;