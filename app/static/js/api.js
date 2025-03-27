export const API = {
    
    // Timer functions
    async initTimer() {
        return await API.fetchJSON('/timer/init', 'POST');
    },

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
        return await API.fetchJSON('/logs/categories', 'GET');
    },

    async addCategory(categoryName) {
        return await API.fetchJSON('/logs/add_category', 'POST', { category: categoryName });
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
