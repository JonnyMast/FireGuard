/**
 * Authentication module for FireGuard application
 */
const Auth = (function() {
    /**
     * Check if user is authenticated
     * @returns {boolean} True if authenticated, false otherwise
     */
    function isAuthenticated() {
        const token = localStorage.getItem('authToken');
        if (!token) {
            redirectToLogin();
            return false;
        }
        return true;
    }

    /**
     * Get authentication token
     * @returns {string} Authentication token
     */
    function getToken() {
        return localStorage.getItem('authToken');
    }

    /**
     * Set authentication token
     * @param {string} token - Authentication token
     */
    function setToken(token) {
        localStorage.setItem('authToken', token);
    }

    /**
     * Remove authentication token and redirect to login
     */
    function logout() {
        localStorage.removeItem('authToken');
        redirectToLogin();
    }

    /**
     * Redirect to login page
     */
    function redirectToLogin() {
        window.location.href = '../Views/login.html';
    }

    // Public API
    return {
        isAuthenticated,
        getToken,
        setToken,
        logout
    };
})();