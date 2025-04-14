export const API = {
    
    // Timer functions
    async startTimer() {
        return await API.fetchJSON('/timer/start', 'POST');
    },

    async stopTimer() {
        return await API.fetchJSON('/timer/stop', 'POST');
    },

    async resetTimer() {
        return await API.fetchJSON('/timer/reset', 'POST');
    },

    async checkElapsedTime() {
        return await API.fetchJSON('/timer/check', 'GET');
    },

    // Category functions
    async getCategories() {
        return await API.fetchJSON('/category/categories', 'GET');
    },

    async addCategory(categoryName) {
        return await API.fetchJSON('/category/add_category', 'POST', { category: categoryName });
    },

    // Log functions
    async addLog(categoryName, startTime, endTime, duration) {
        console.log("API addLog called");
        return await API.fetchJSON('/log/add', 'POST', {category: categoryName, startTime: startTime, endTime: endTime, duration: duration})
    },

    // Shared fetch function for all API calls
    async fetchJSON(url, method = 'GET', body = null) {
        try {
            const options = { method, headers: { 'Content-Type': 'application/json' } };
            if (body) options.body = JSON.stringify(body); // Only add body if needed

            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`Fetch error (${method} ${url}):`, error);
            return { error: error.message };
        }
    }
};

window.API = API;
