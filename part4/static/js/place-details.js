// ============================================
// HBnB - Place Details Module
// ============================================

// API Configuration
const API_URL = 'http://localhost:5001/api';

// ============================================
// Cookie Management
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

// ============================================
// Get Place ID from URL
// ============================================

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

// ============================================
// Check Authentication
// ============================================

function checkAuthentication() {
    const token = getCookie('token');
    
    if (!token) {
        // Redirect to login if not authenticated
        window.location.href = 'index.html';
        return null;
    }
    
    return token;
}

// ============================================
// Fetch Place Details
// ============================================

async function fetchPlaceDetails(token, placeId) {
    try {
        const response = await fetch(`${API_URL}/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                // Token expired
                document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
                window.location.href = 'index.html';
                return;
            }
            if (response.status === 404) {
                throw new Error('Place not found');
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const place = await response.json();
        return place;
        
    } catch (error) {
        console.error('Error fetching place details:', error);
        throw error;
    }
}

// ============================================
// Fetch Place Reviews
// ============================================

async function fetchPlaceReviews(token, placeId) {
    try {
        const response = await fetch(`${API_URL}/reviews/?place_id=${placeId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const reviews = await response.json();
            return reviews.filter(review => review.place_id === placeId);
        }
        
        return [];
        
    } catch (error) {
        console.error('Error fetching reviews:', error);
        return [];
    }
}

// ============================================
// Display Place Details
// ============================================

function displayPlaceDetails(place) {
    const detailsContainer = document.getElementById('place-details');
    
    detailsContainer.innerHTML = `
        <div class="place-info">
            <h1>${place.title}</h1>
            <p class="host">Hosted by: ${place.owner_id}</p>
            <p class="price">$${parseFloat(place.price).toFixed(2)} / night</p>
            
            ${place.description ? `
                <div class="description">
                    <h2>Description</h2>
                    <p>${place.description}</p>
                </div>
            ` : ''}
            
            ${place.latitude && place.longitude ? `
                <div class="location">
                    <h2>Location</h2>
                    <p>📍 ${place.latitude.toFixed(4)}, ${place.longitude.toFixed(4)}</p>
                </div>
            ` : ''}
        </div>
        
        <div class="amenities" id="amenities-section">
            <h2>Amenities</h2>
            <div class="amenities-list" id="amenities-list">
                <p class="loading">Loading amenities...</p>
            </div>
        </div>
    `;
}

// ============================================
// Display Amenities
// ============================================

function displayAmenities(amenities) {
    const amenitiesList = document.getElementById('amenities-list');
    
    if (!amenities || amenities.length === 0) {
        amenitiesList.innerHTML = '<p>No amenities listed.</p>';
        return;
    }
    
    amenitiesList.innerHTML = '';
    
    amenities.forEach(amenity => {
        const amenityItem = document.createElement('div');
        amenityItem.className = 'amenity-item';
        amenityItem.innerHTML = `
            <strong>${amenity.name}</strong>
            ${amenity.description ? `<p>${amenity.description}</p>` : ''}
        `;
        amenitiesList.appendChild(amenityItem);
    });
}

// ============================================
// Display Reviews
// ============================================

function displayReviews(reviews) {
    const reviewsContainer = document.getElementById('reviews-container');
    
    if (!reviews || reviews.length === 0) {
        reviewsContainer.innerHTML = '<p>No reviews yet. Be the first to review!</p>';
        return;
    }
    
    reviewsContainer.innerHTML = '';
    
    reviews.forEach(review => {
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';
        
        // Create star rating
        const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
        
        reviewCard.innerHTML = `
            <div class="review-header">
                <span class="user-name">User ${review.user_id.substring(0, 8)}</span>
                <span class="rating">${stars}</span>
            </div>
            <p class="review-comment">${review.comment}</p>
            <p class="review-date">${new Date(review.created_at).toLocaleDateString()}</p>
        `;
        
        reviewsContainer.appendChild(reviewCard);
    });
}

// ============================================
// Show/Hide Add Review Link
// ============================================

function setupAddReviewLink(placeId, token) {
    const addReviewLink = document.getElementById('add-review-link');
    
    if (token && addReviewLink) {
        addReviewLink.href = `add-review.html?place_id=${placeId}`;
        addReviewLink.classList.remove('hidden');
    }
}

// ============================================
// Initialize Page
// ============================================

document.addEventListener('DOMContentLoaded', async () => {
    // Check authentication
    const token = checkAuthentication();
    if (!token) return;
    
    // Get place ID from URL
    const placeId = getPlaceIdFromURL();
    
    if (!placeId) {
        document.getElementById('place-details').innerHTML = `
            <p class="error">No place ID provided. Please select a place from the list.</p>
        `;
        return;
    }
    
    try {
        // Fetch place details
        const place = await fetchPlaceDetails(token, placeId);
        displayPlaceDetails(place);
        
        // Display amenities if available
        if (place.amenities) {
            displayAmenities(place.amenities);
        }
        
        // Fetch and display reviews
        const reviews = await fetchPlaceReviews(token, placeId);
        displayReviews(reviews);
        
        // Setup add review link
        setupAddReviewLink(placeId, token);
        
    } catch (error) {
        document.getElementById('place-details').innerHTML = `
            <p class="error">Failed to load place details: ${error.message}</p>
        `;
    }
});
