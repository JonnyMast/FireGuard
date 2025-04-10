/**
 * Logout functionality for FireGuard application
 * This script attaches event handlers to logout buttons across the application
 */
document.addEventListener('DOMContentLoaded', function() {
    // Find all logout buttons in the document
    const logoutBtn = document.getElementById('logout-btn');
    
    if (logoutBtn) {
        // Add click event listener to the logout button
        logoutBtn.addEventListener('click', function(event) {
            event.preventDefault();
            
            // Show confirmation if needed
            const confirmLogout = confirm('Are you sure you want to log out?');
            
            if (confirmLogout) {
                // Use the Auth module to handle logout logic
                if (typeof Auth !== 'undefined' && Auth.logout) {
                    Auth.logout();
                } else {
                    // Fallback if Auth module is not available
                    localStorage.removeItem('authToken');
                    window.location.href = '../index.html';
                }
            }
        });
    }
});