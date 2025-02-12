//Handles all API requests (fetch calls)
export const API = {
    startTimer: () => fetch('/timer/start', { method: 'POST' }).then(res => res.json()),
    stopTimer: () => fetch('/timer/stop', { method: 'POST' }).then(res => res.json()),
    checkElapsedTime: () => fetch('/timer/check').then(res => res.json()),
    getCategories: () => fetch('/logs/categories').then(res => res.json())
};
