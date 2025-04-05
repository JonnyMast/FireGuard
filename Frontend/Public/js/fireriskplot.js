/**
 * FireRisk Plot Module for visualizing fire risk data on Leaflet maps
 */

// Constants for visualization
const TTF_COLORS = {
    high: '#ff0000',    // Red for high risk (low TTF)
    medium: '#ffa500',  // Orange for medium risk
    low: '#ffff00'      // Yellow for low risk (high TTF)
};

// TTF thresholds in minutes (these are examples - adjust based on your domain knowledge)
const TTF_THRESHOLDS = {
    high: 4,     // 0-30 minutes is high risk
    medium: 6.5    // 30-60 minutes is medium risk, >60 is low risk
};

/**
 * Creates fire risk visualization on a Leaflet map
 * 
 * @param {Object} map - Leaflet map instance
 * @param {Object} data - Fire risk data from API
 * @param {Number} timestampIndex - Index of the timestamp to display
 * @returns {Object} References to created map elements
 */
export function createFireRiskPlot(map, data, timestampIndex = 0) {
    if (!data || !data.location || !data.firerisks || !data.firerisks.length) {
        console.error('Invalid fire risk data format');
        return null;
    }
    
    // Check if we have valid time-based information
    const hasTimeData = data.firerisks.some(risk => risk.timestamp);
    if (!hasTimeData) {
        console.warn('No time information available for this location');
    }
    
    // Get the specific timestamp data
    const timepoint = data.firerisks[timestampIndex];
    if (!timepoint) {
        console.error('No data available for the selected timestamp index');
        return null;
    }
    
    // Create the main marker at the location
    const { latitude, longitude } = data.location;
    
    // Determine color based on TTF
    const color = getTtfColor(timepoint.ttf);
    
    // Create circle marker with radius based on wind speed
    const radius = calculateRadius(timepoint.wind_speed);
    
    // Create the circle marker
    const riskMarker = L.circleMarker([latitude, longitude], {
        radius: radius,
        fillColor: color,
        color: '#000',
        weight: 1,
        opacity: 1,
        fillOpacity: 0.7,
        className: 'fire-risk-marker' // Add class for easy selection
    }).addTo(map);
    
    // Add popup with detailed information
    const formattedTime = formatTimestamp(timepoint.timestamp);
    const popupContent = `
        <div class="fire-risk-popup">
            <h3>Fire Risk Assessment</h3>
            <p><strong>Time:</strong> ${formattedTime}</p>
            <p><strong>Time to Flashover:</strong> ${timepoint.ttf.toFixed(2)} minutes</p>
            <p><strong>Wind Speed:</strong> ${timepoint.wind_speed.toFixed(2)} m/s</p>
            <p><strong>Risk Level:</strong> ${getRiskLevel(timepoint.ttf)}</p>
        </div>
    `;
    
    riskMarker.bindPopup(popupContent);
    
    // Make marker clickable to set as active city
    riskMarker.on('click', function() {
        if (window.setActiveCity) {
            window.setActiveCity(data.location.name);
        }
    });
    
    return {
        marker: riskMarker,
        data: data,
        currentIndex: timestampIndex,
        hasTimeData: hasTimeData
    };
}

/**
 * Updates an existing fire risk visualization to a different timestamp
 * 
 * @param {Object} plot - Plot reference returned by createFireRiskPlot
 * @param {Number} newTimestampIndex - Index of the new timestamp to display
 */
export function updateFireRiskPlot(plot, newTimestampIndex) {
    if (!plot || !plot.marker || !plot.data || !plot.data.firerisks) {
        console.error('Invalid plot reference');
        return;
    }
    
    // Get the new timepoint data
    const timepoint = plot.data.firerisks[newTimestampIndex];
    if (!timepoint) {
        console.error('No data available for the selected timestamp index');
        return;
    }
    
    // Update the marker style
    const color = getTtfColor(timepoint.ttf);
    const radius = calculateRadius(timepoint.wind_speed);
    
    plot.marker.setStyle({
        radius: radius,
        fillColor: color
    });
    
    // Update the popup content
    const formattedTime = formatTimestamp(timepoint.timestamp);
    const popupContent = `
        <div class="fire-risk-popup">
            <h3>Fire Risk Assessment</h3>
            <p><strong>Time:</strong> ${formattedTime}</p>
            <p><strong>Time to Flashover:</strong> ${timepoint.ttf.toFixed(2)} minutes</p>
            <p><strong>Wind Speed:</strong> ${timepoint.wind_speed.toFixed(2)} m/s</p>
            <p><strong>Risk Level:</strong> ${getRiskLevel(timepoint.ttf)}</p>
        </div>
    `;
    
    plot.marker.getPopup().setContent(popupContent);
    
    // Update the current index reference
    plot.currentIndex = newTimestampIndex;
}

/**
 * Clears fire risk visualizations from the map
 * 
 * @param {Object} map - Leaflet map instance
 */
export function clearFireRiskPlot(map) {
    // Find and remove all fire risk markers
    map.eachLayer(layer => {
        if (layer instanceof L.CircleMarker) {
            map.removeLayer(layer);
        }
    });
}

/**
 * Calculates the visualization radius based on wind speed
 * 
 * @param {Number} windSpeed - Wind speed in m/s
 * @returns {Number} Radius for the circle marker
 */
function calculateRadius(windSpeed) {
    // Base size
    const baseRadius = 10;
    
    // Scale based on wind speed (adjust these values as needed)
    const scaleFactor = 2;
    
    return baseRadius + (windSpeed * scaleFactor);
}

/**
 * Determines color based on TTF value
 * 
 * @param {Number} ttf - Time to flashover in minutes
 * @returns {String} Color hex code
 */
function getTtfColor(ttf) {
    if (ttf <= TTF_THRESHOLDS.high) {
        return TTF_COLORS.high;
    } else if (ttf <= TTF_THRESHOLDS.medium) {
        return TTF_COLORS.medium;
    } else {
        return TTF_COLORS.low;
    }
}

/**
 * Gets the risk level description based on TTF
 * 
 * @param {Number} ttf - Time to flashover in minutes
 * @returns {String} Risk level description
 */
function getRiskLevel(ttf) {
    if (ttf <= TTF_THRESHOLDS.high) {
        return 'High';
    } else if (ttf <= TTF_THRESHOLDS.medium) {
        return 'Medium';
    } else {
        return 'Low';
    }
}

/**
 * Formats a timestamp for display
 * 
 * @param {String} timestamp - ISO timestamp string
 * @returns {String} Formatted date/time string
 */
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString(); // Adjust format as needed
}