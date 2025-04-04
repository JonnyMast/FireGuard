document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    loginForm.addEventListener('submit', function(event) {
        // Prevent the default form submission
        event.preventDefault();
        
        // Get form values
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        // Here you would typically validate credentials with a server
        // For now, we'll just redirect to map.html
        
        // Redirect to map.html
        window.location.href = 'map.html';
    });
});