// ============================================
// HBnB - Add Review Module
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
// Get Place ID from URL
// ============================================

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('place_id');
}

// ============================================
// Submit Review
// ============================================

async function submitReview(token, placeId, rating, comment) {
    try {
        const response = await fetch(`${API_URL}/reviews/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                place_id: placeId,
                rating: parseInt(rating),
                comment: comment
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || `HTTP error! status: ${response.status}`);
        }
        
        return data;
        
    } catch (error) {
        console.error('Error submitting review:', error);
        throw error;
    }
}

// ============================================
// Show Message
// ============================================

function showMessage(message, isError = false) {
    const messageDiv = document.getElementById('message');
    
    if (messageDiv) {
        messageDiv.textContent = message;
        messageDiv.className = isError ? 'error-message' : 'success-message';
        messageDiv.style.display = 'block';
        
        // Hide message after 5 seconds
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 5000);
    }
}

// ============================================
// Update Star Rating Display
// ============================================

function setupStarRating() {
    const ratingInput = document.getElementById('rating');
    const starsContainer = document.getElementById('stars-display');
    
    if (!ratingInput || !starsContainer) return;
    
    // Initial display
    updateStars(ratingInput.value);
    
    // Update on change
    ratingInput.addEventListener('input', (e) => {
        updateStars(e.target.value);
    });
    
    function updateStars(rating) {
        const stars = '★'.repeat(rating) + '☆'.repeat(5 - rating);
        starsContainer.textContent = stars;
    }
}

// ============================================
// Initialize Form
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    // Check authentication
    const token = checkAuthentication();
    if (!token) return;
    
    // Get place ID
    const placeId = getPlaceIdFromURL();
    
    if (!placeId) {
        showMessage('No place ID provided. Redirecting...', true);
        setTimeout(() => {
            window.location.href = 'places.html';
        }, 2000);
        return;
    }
    
    // Setup star rating display
    setupStarRating();
    
    // Get form
    const reviewForm = document.getElementById('review-form');
    
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            // Get form data
            const rating = document.getElementById('rating').value;
            const comment = document.getElementById('comment').value.trim();
            
            // Validate
            if (!comment) {
                showMessage('Please enter a comment', true);
                return;
            }
            
            if (rating < 1 || rating > 5) {
                showMessage('Please select a rating between 1 and 5', true);
                return;
            }
            
            // Disable submit button
            const submitButton = reviewForm.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            submitButton.disabled = true;
            submitButton.textContent = 'Submitting...';
            
            try {
                // Submit review
                await submitReview(token, placeId, rating, comment);
                
                // Show success message
                showMessage('Review submitted successfully! Redirecting...', false);
                
                // Clear form
                reviewForm.reset();
                setupStarRating();
                
                // Redirect back to place details after 2 seconds
                setTimeout(() => {
                    window.location.href = `place-details.html?id=${placeId}`;
                }, 2000);
                
            } catch (error) {
                // Show error message
                showMessage(error.message || 'Failed to submit review. Please try again.', true);
                
                // Re-enable submit button
                submitButton.disabled = false;
                submitButton.textContent = originalText;
            }
        });
    }
    
    // Cancel button
    const cancelButton = document.getElementById('cancel-button');
    if (cancelButton) {
        cancelButton.addEventListener('click', (e) => {
            e.preventDefault();
            window.location.href = `place-details.html?id=${placeId}`;
        });
    }
});