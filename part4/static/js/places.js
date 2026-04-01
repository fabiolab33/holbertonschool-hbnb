// ============================================
// HBnB - Places List Module
// ============================================

// API Configuration
const API_URL = 'http://localhost:5001/api';

// ============================================
// Cookie Management (from auth.js)
// ============================================

function getCookie(name) {
    const nameEQ = `${name}=`;
    const cookies = document.cookie.split(';');
    
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.indexOf(nameEQ) === 0) {
            return cookie.substring(nameEQ.length);
        }
    }
    return null;
}

function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

// ============================================
// Authentication Check
// ============================================

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const logoutButton = document.getElementById('logout-button');
    
    if (!token) {
        // User not authenticated - redirect to login
        window.location.href = 'index.html';
        return false;
    }
    
    // User authenticated - fetch places
    fetchPlaces(token);
    return true;
}

// ============================================
// Fetch Places from API
// ============================================

async function fetchPlaces(token) {
    const placesContainer = document.getElementById('places-container');
    
    try {
        placesContainer.innerHTML = '<p class="loading">Loading places...</p>';
        
        const response = await fetch(`${API_URL}/places/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                // Token expired or invalid
                deleteCookie('token');
                window.location.href = 'index.html';
                return;
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const places = await response.json();
        displayPlaces(places);
        setupPriceFilter(places);
        
    } catch (error) {
        console.error('Error fetching places:', error);
        placesContainer.innerHTML = `
            <p class="error">
                Failed to load places. Please try again later.
            </p>
        `;
    }
}

// ============================================
// Display Places
// ============================================

function displayPlaces(places) {
    const placesContainer = document.getElementById('places-container');
    
    if (!places || places.length === 0) {
        placesContainer.innerHTML = `
            <p class="text-center">No places available at the moment.</p>
        `;
        return;
    }
    
    placesContainer.innerHTML = '';
    
    places.forEach(place => {
        const placeCard = createPlaceCard(place);
        placesContainer.appendChild(placeCard);
    });
}

function createPlaceCard(place) {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.setAttribute('data-price', place.price);
    
    // Create image (placeholder or actual)
    const img = document.createElement('img');
    img.src = place.image_url || 'static/images/placeholder.jpg';
    img.alt = place.title;
    img.onerror = function() {
        this.src = 'static/images/placeholder.jpg';
    };
    
    // Create title
    const title = document.createElement('h3');
    title.textContent = place.title;
    
    // Create price
    const price = document.createElement('p');
    price.className = 'price';
    price.textContent = `$${parseFloat(place.price).toFixed(2)} / night`;
    
    // Create location (if available)
    const location = document.createElement('p');
    location.className = 'location';
    if (place.latitude && place.longitude) {
        location.textContent = `📍 ${place.latitude.toFixed(4)}, ${place.longitude.toFixed(4)}`;
    }
    
    // Create description preview
    const description = document.createElement('p');
    description.className = 'description';
    description.textContent = place.description 
        ? (place.description.substring(0, 100) + '...') 
        : 'No description available';
    
    // Create details button
    const detailsButton = document.createElement('a');
    detailsButton.href = `place-details.html?id=${place.id}`;
    detailsButton.className = 'details-button';
    detailsButton.textContent = 'View Details';
    
    // Append all elements
    card.appendChild(img);
    card.appendChild(title);
    card.appendChild(price);
    if (location.textContent) {
        card.appendChild(location);
    }
    card.appendChild(description);
    card.appendChild(detailsButton);
    
    return card;
}

// ============================================
// Price Filter
// ============================================

function setupPriceFilter(places) {
    const priceFilter = document.getElementById('price-filter');
    
    if (!priceFilter) return;
    
    // Populate filter options
    priceFilter.innerHTML = `
        <option value="all">All Prices</option>
        <option value="50">Under $50</option>
        <option value="100">Under $100</option>
        <option value="200">Under $200</option>
        <option value="500">Under $500</option>
    `;
    
    // Add event listener for filtering
    priceFilter.addEventListener('change', (event) => {
        const selectedPrice = event.target.value;
        filterPlacesByPrice(selectedPrice);
    });
}

function filterPlacesByPrice(maxPrice) {
    const placeCards = document.querySelectorAll('.place-card');
    
    placeCards.forEach(card => {
        const cardPrice = parseFloat(card.getAttribute('data-price'));
        
        if (maxPrice === 'all' || cardPrice <= parseFloat(maxPrice)) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });
}

// ============================================
// Logout Handler
// ============================================

function setupLogout() {
    const logoutButton = document.getElementById('logout-button');
    
    if (logoutButton) {
        logoutButton.addEventListener('click', (event) => {
            event.preventDefault();
            
            if (confirm('Are you sure you want to logout?')) {
                deleteCookie('token');
                window.location.href = 'index.html';
            }
        });
    }
}

// ============================================
// Initialize on Page Load
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
    setupLogout();
});
