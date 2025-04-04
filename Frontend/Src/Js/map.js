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
    let historyDays = 7;
    
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
    
    // The rest of your code remains unchanged
    // Fetch fire risk data from API
    async function fetchFireRiskData() {
        try {
            showLoading();
            
            // Make API call (adjust URL to match your backend)
            const apiUrl = `/api/fire-risk?location=${encodeURIComponent(currentLocation)}&days=${historyDays}`;
            const response = await fetch(apiUrl, {
                headers: {
                    'Authorization': `Bearer ${Auth.getToken()}`
                }
            });
            
            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }
            
            const data = await response.json();
            displayFireRiskData(data);
            
        } catch (error) {
            console.error('Error fetching fire risk data:', error);
            displayError('Failed to load fire risk data. Please try again.');
        } finally {
            hideLoading();
        }
    }
    
    // Initialize the application
    function initApp() {
       if (!Auth.isAuthenticated()) return;
        
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