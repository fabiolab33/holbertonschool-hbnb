// ============================================
// HBnB - Authentication Module
// ============================================

// API Configuration
const API_URL = 'http://localhost:5001/api';

// ============================================
// Cookie Management Functions
// ============================================

/**
 * Set a cookie with given name, value, and expiration days
 * @param {string} name - Cookie name
 * @param {string} value - Cookie value
 * @param {number} days - Expiration in days
 */
function setCookie(name, value, days = 1) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = `expires=${date.toUTCString()}`;
    document.cookie = `${name}=${value}; ${expires}; path=/; SameSite=Lax`;
}

/**
 * Get cookie value by name
 * @param {string} name - Cookie name
 * @returns {string|null} Cookie value or null if not found
 */
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

/**
 * Delete cookie by name
 * @param {string} name - Cookie name
 */
function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

// ============================================
// Authentication Functions
// ============================================

/**
 * Login user with email and password
 * @param {string} email - User email
 * @param {string} password - User password
 * @returns {Promise<Object>} Response data with access_token
 */
async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `Login failed: ${response.statusText}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
}

/**
 * Check if user is authenticated
 * @returns {boolean} True if user has valid token
 */
function isAuthenticated() {
    const token = getCookie('token');
    return token !== null && token !== '';
}

/**
 * Get the stored JWT token
 * @returns {string|null} JWT token or null
 */
function getToken() {
    return getCookie('token');
}

/**
 * Logout user by clearing token
 */
function logout() {
    deleteCookie('token');
    window.location.href = 'index.html';
}

/**
 * Check authentication and redirect if needed
 * @param {boolean} requireAuth - If true, redirect to login if not authenticated
 */
function checkAuth(requireAuth = true) {
    const token = getToken();
    const isLoginPage = window.location.pathname.includes('index.html') || 
                       window.location.pathname === '/';

    if (requireAuth && !token && !isLoginPage) {
        // User needs to be authenticated but isn't - redirect to login
        window.location.href = 'index.html';
        return false;
    }

    if (token && isLoginPage) {
        // User is already logged in and on login page - redirect to places
        window.location.href = 'places.html';
        return false;
    }

    return true;
}

// ============================================
// Login Form Handler
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');

    // If on login page and already authenticated, redirect
    if (loginForm) {
        checkAuth(false);
    }

    // Setup login form submission handler
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            // Clear previous error messages
            if (errorMessage) {
                errorMessage.style.display = 'none';
                errorMessage.textContent = '';
            }

            // Get form data
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;

            // Basic validation
            if (!email || !password) {
                showError('Please enter both email and password');
                return;
            }

            // Disable submit button to prevent double submission
            const submitButton = loginForm.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.textContent;
            submitButton.disabled = true;
            submitButton.textContent = 'Logging in...';

            try {
                // Attempt login
                const data = await loginUser(email, password);

                // Store token in cookie (expires in 1 day)
                setCookie('token', data.access_token, 1);

                // Show success message briefly
                showError('Login successful! Redirecting...', 'success');

                // Redirect to places page after short delay
                setTimeout(() => {
                    window.location.href = 'places.html';
                }, 500);

            } catch (error) {
                // Show error message
                showError(error.message || 'Login failed. Please check your credentials.');
                
                // Re-enable submit button
                submitButton.disabled = false;
                submitButton.textContent = originalButtonText;
            }
        });
    }

    /**
     * Display error or success message
     * @param {string} message - Message to display
     * @param {string} type - 'error' or 'success'
     */
    function showError(message, type = 'error') {
        if (errorMessage) {
            errorMessage.textContent = message;
            errorMessage.style.display = 'block';
            errorMessage.style.color = type === 'success' ? '#28a745' : '#dc3545';
        }
    }
});

// ============================================
// Global Logout Handler
// ============================================

// Add logout handler if logout button exists
document.addEventListener('DOMContentLoaded', () => {
    const logoutButton = document.getElementById('logout-button');
    
    if (logoutButton) {
        logoutButton.addEventListener('click', (event) => {
            event.preventDefault();
            
            // Confirm logout
            if (confirm('Are you sure you want to logout?')) {
                logout();
            }
        });
    }
});

// ============================================
// Export functions for use in other modules
// ============================================

// Make functions available globally for other scripts
window.HBnBAuth = {
    loginUser,
    logout,
    isAuthenticated,
    getToken,
    checkAuth,
    getCookie,
    setCookie,
    deleteCookie
};
