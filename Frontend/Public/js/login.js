import { API_URL } from './config.js'

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    loginForm.addEventListener('submit', async function(event) {
        // Prevent the default form submission
        event.preventDefault();
        
        // Get form values
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        // Display loading state or disable submit button
        const submitButton = loginForm.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = 'Logging in...';
        }
        
        try {
            // Make API call to get JWT
            const response = await fetch(`${API_URL}/api/gen/jwt/user`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });
            
            if (!response.ok) {
                throw new Error(`Authentication failed: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            // Store JWT token in localStorage
            localStorage.setItem('jwt', data.token);
            console.log(data.token)
            // Redirect to map.html
            window.location.href = 'map.html';
            
        } catch (error) {
            console.error('Login error:', error);
            
            // Show error message to user
            const errorElement = document.createElement('div');
            errorElement.className = 'error-message';
            errorElement.textContent = 'Login failed. Please check your credentials.';
            
            // Insert error message before the form or in a designated error container
            const errorContainer = document.getElementById('error-container') || loginForm.parentNode;
            errorContainer.prepend(errorElement);
            
            // Reset button state
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = 'Login';
            }
        }
    });
});