

//Handles all API requests (fetch calls)
export const API = {
    
    //Timer functions
    initTimer: ()=> fetch('/timer/init', { method: 'GET' }).then(res => res.json()),
    startTimer: () => fetch('/timer/start', { method: 'GET' }).then(res => res.json()),
    stopTimer: () => fetch('/timer/stop').then(res => res.json()),
    resetTimer: () => fetch('/timer/reset').then(res => res.json()),
    checkElapsedTime: () => fetch('/timer/check').then(res => res.json()),

    //Category functions
    getCategories: () => fetch('/logs/categories').then(res => res.json()),
    addCategory: (categoryName) => fetch('/logs/add_category', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify({category: categoryName}) // Convert to JSON
    })
    .then(res => res.json())
    .then(data => console.log("Server Response:", data)) // Log response
    .catch(error => console.error("Fetch Error:", error)) // Handle errors

    //Log functions
};


window.API = API;