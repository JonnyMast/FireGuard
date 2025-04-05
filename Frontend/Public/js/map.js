import { API_URL } from './config.js';
import { createFireRiskPlot, updateFireRiskPlot, clearFireRiskPlot } from './fireriskplot.js';

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
    
    // Fire risk visualization data
    let currentFireRiskPlot = null;
    let timeSlider = null;
    let timeControls = null;
    let timeLabel = null;
    
    // State variables
    let searchedLocation = '';
    let userLocation = null;  // New variable to store user's actual geographical position
    let historyDays = 1; // Default value matching the HTML
    
    // Initialize the map with Leaflet
    function initMap() {
        try {
            // Default location: Oslo, Norway
            const defaultLocation = [59.9139, 10.7522]; // Oslo coordinates
            
            // Create the map with Oslo as the default location (but no marker)
            map = L.map('map-container').setView(defaultLocation, 13);
            
            // Add the base map layer
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);
            
            // If user allows geolocation, update the map to their location
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(position => {
                    const { latitude, longitude } = position.coords;
                    userLocation = { latitude, longitude }; // Store user's actual location
                    
                    // Update view to user's location
                    map.setView([latitude, longitude], 13);
                    
                    // Add a marker for user's location
                    L.marker([latitude, longitude])
                        .addTo(map)
                        .bindPopup('Your current location')
                        .openPopup();
                }, error => {
                    console.log('Geolocation error:', error);
                    // No marker displayed if permission denied
                });
            }
            
            // Create container for the time slider
            createTimeSliderControls();
            
        } catch (e) {
            console.error('Error initializing map:', e);
            displayError('Failed to initialize the map. Please refresh the page.');
        }
    }
    
    // Create time slider controls
    function createTimeSliderControls() {
        // Create a custom control for the time slider
        timeControls = L.control({ position: 'topright' });
        
        timeControls.onAdd = function(map) {
            const container = L.DomUtil.create('div', 'time-slider-container');
            container.style.backgroundColor = 'white';
            container.style.padding = '10px';
            container.style.borderRadius = '5px';
            container.style.boxShadow = '0 1px 5px rgba(0,0,0,0.4)';
            container.style.width = '300px';
            container.style.display = 'none'; // Hide initially until we have data
            
            // Create time display label
            timeLabel = L.DomUtil.create('div', 'time-label', container);
            timeLabel.innerHTML = 'No data available';
            timeLabel.style.marginBottom = '5px';
            timeLabel.style.textAlign = 'center';
            
            // Create slider element
            timeSlider = L.DomUtil.create('input', 'time-slider', container);
            timeSlider.type = 'range';
            timeSlider.min = '0';
            timeSlider.max = '0';
            timeSlider.value = '0';
            timeSlider.style.width = '100%';
            
            // Prevent map interaction when using the slider
            L.DomEvent.disableClickPropagation(container);
            L.DomEvent.disableScrollPropagation(container);
            
            return container;
        };
        
        timeControls.addTo(map);
    }
    
    // Update time slider with new fire risk data
    function updateTimeSlider(fireRiskData) {
        const container = timeControls.getContainer();
        
        if (fireRiskData && fireRiskData.firerisks && fireRiskData.firerisks.length > 0) {
            // Show the container
            container.style.display = 'block';
            
            // Update slider max value
            timeSlider.max = fireRiskData.firerisks.length - 1;
            timeSlider.min = 0;
            timeSlider.value = 0;
            
            // Update the label
            updateTimeLabel(fireRiskData, 0);
            
            // Add event listener
            timeSlider.addEventListener('input', function() {
                const index = parseInt(this.value);
                updateTimeLabel(fireRiskData, index);
                
                // Update the visualization
                if (currentFireRiskPlot) {
                    updateFireRiskPlot(currentFireRiskPlot, index);
                }
            });
        } else {
            // Hide the container if no data
            container.style.display = 'none';
        }
    }
    
    // Update the time label with timestamp information
    function updateTimeLabel(data, index) {
        if (data && data.firerisks && data.firerisks[index]) {
            const timestamp = new Date(data.firerisks[index].timestamp);
            timeLabel.innerHTML = `Time: ${timestamp.toLocaleString()}`;
        } else {
            timeLabel.innerHTML = 'No data available';
        }
    }
    
    // Setup event listeners
    function setupEventListeners() {
        // Slider event listener
        daysSlider.addEventListener('input', function() {
            historyDays = this.value;
            daysValue.textContent = historyDays;
            // Optionally refresh data when slider changes
            // if (searchedLocation) fetchFireRiskData();
        });
        
        // Search button event listener
        searchBtn.addEventListener('click', function() {
            searchedLocation = searchInput.value; // Use searchedLocation instead of currentLocation
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
            
            if (!token) {
                throw new Error('Authentication token not found. Please log in again.');
            }
            
            const apiUrl = `${API_URL}/api/fireguard/firerisk/city?city=${encodeURIComponent(searchedLocation)}&days=${historyDays}`;
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
        console.log('Fire risk data:', data);
        
        if (data && data.location && data.firerisks && data.firerisks.length > 0) {
            // Clear any existing fire risk plots
            if (currentFireRiskPlot) {
                clearFireRiskPlot(map);
            }
            
            // Center the map on the location
            map.setView([data.location.latitude, data.location.longitude], 13);
            
            // Create fire risk visualization
            currentFireRiskPlot = createFireRiskPlot(map, data);
            
            // Update the time slider
            updateTimeSlider(data);
        } else {
            displayError('No fire risk data available for this location');
        }
    }
    
    // Show loading indicator
    function showLoading() {
        // TODO: Implement loading indicator
        console.log('Loading fire-risk data...');
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