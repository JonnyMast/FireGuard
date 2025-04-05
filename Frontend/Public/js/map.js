import { API_URL } from './config.js';

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const logoutBtn = document.getElementById('logout-btn');
    const searchInput = document.getElementById('location-search');
    const searchBtn = document.getElementById('search-btn');
    const daysSlider = document.getElementById('days-slider');
    const daysValue = document.getElementById('days-value');
    const mapContainer = document.getElementById('map-container');
    
    // Map initialization
    let map;
    let markers = [];
    
    // State variables
    let currentLocation = '';
    let historyDays = 1; // Default value matching the HTML
    
    // Initialize the map with Leaflet
    function initMap() {
        try {
            // Default location: Oslo, Norway
            const defaultLocation = [59.9139, 10.7522]; // Oslo coordinates
            
            // Create the map with Oslo as the default location
            map = L.map('map-container').setView(defaultLocation, 13);
            
            // Add the base map layer
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);
            
            // Add a marker for the default location
            const defaultMarker = L.marker(defaultLocation)
                .addTo(map)
                .bindPopup('Default location: Oslo, Norway');
                
            // If user allows geolocation, update the map to their location
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(position => {
                    const { latitude, longitude } = position.coords;
                    
                    // Remove the default marker
                    map.removeLayer(defaultMarker);
                    
                    // Update view to user's location
                    map.setView([latitude, longitude], 13);
                    
                    // Add a marker for user's location
                    L.marker([latitude, longitude])
                        .addTo(map)
                        .bindPopup('Your current location')
                        .openPopup();
                }, error => {
                    console.log('Geolocation error:', error);
                    // Keep the default marker open if geolocation fails
                    defaultMarker.openPopup();
                });
            } else {
                // Browser doesn't support geolocation, keep Oslo as default
                defaultMarker.openPopup();
            }
        } catch (e) {
            console.error('Error initializing map:', e);
            displayError('Failed to initialize the map. Please refresh the page.');
        }
    }
    
    // Setup event listeners
    function setupEventListeners() {
        // Slider event listener
        daysSlider.addEventListener('input', function() {
            historyDays = this.value;
            daysValue.textContent = historyDays;
            // Optionally refresh data when slider changes
            // fetchFireRiskData();
        });
        
        // Search button event listener
        searchBtn.addEventListener('click', function() {
            currentLocation = searchInput.value;
            fetchFireRiskData();
        });
        
        // Logout button event listener
        logoutBtn.addEventListener('click', function() {
            localStorage.removeItem('jwt');
            window.location.href = 'index.html'; // Redirect to front page after logout
        });
    }
    
    // Fetch fire risk data from API
    async function fetchFireRiskData() {
        try {
            showLoading();
            
            const token = localStorage.getItem('jwt');
            console.log('Using JWT:', token); // Debug the token
            
            if (!token) {
                throw new Error('Authentication token not found. Please log in again.');
            }
            
            const apiUrl = `${API_URL}/api/fireguard/firerisk/city?city=${encodeURIComponent(currentLocation)}&days=${historyDays}`;
            const response = await fetch(apiUrl, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }
            
            const data = await response.json();
            displayFireRiskData(data);
            
        } catch (error) {
            console.error('Error fetching fire risk data:', error);
            
            if (error.message.includes('token not found')) {
                // Special handling for missing token
                localStorage.removeItem('jwt'); // Clear any invalid token
                window.location.href = 'login.html'; // Redirect to login
            } else {
                displayError('Failed to load fire risk data. Please try again.');
            }
        } finally {
            hideLoading();
        }
    }
    
    // Display fire risk data
    function displayFireRiskData(data) {
        // Implementation will depend on your data structure
        console.log('Fire risk data:', data);
        // TODO: Display data on the map or in a chart
    }
    
    // Show loading indicator
    function showLoading() {
        // TODO: Implement loading indicator
        console.log('Loading...');
    }
    
    // Hide loading indicator
    function hideLoading() {
        // TODO: Hide loading indicator
        console.log('Loading complete');
    }
    
    // Display error message
    function displayError(message) {
        // Implementation for displaying errors to the user
        console.error(message);
        // TODO: Show error message in the UI
    }
    
    // Initialize the application
    function initApp() {
        // Check for JWT directly in localStorage
        const jwt = localStorage.getItem('jwt');
        if (!jwt) {
            // Redirect to front page if no JWT found
            window.location.href = 'login.html';
            return;
        }
        
        // First load CSS for Leaflet
        const leafletCSS = document.createElement('link');
        leafletCSS.id = 'leaflet-css';
        leafletCSS.rel = 'stylesheet';
        leafletCSS.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
        document.head.appendChild(leafletCSS);
        
        // Then load Leaflet script dynamically
        const script = document.createElement('script');
        script.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
        script.onload = function() {
            // Initialize map once Leaflet is loaded
            initMap();
            setupEventListeners();
        };
        document.head.appendChild(script);
    }
    
    // Start the application
    initApp();
});