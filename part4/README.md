# HBnB Evolution - Part 4: Web Client Implementation

## Project Overview

Part 4 implements a complete front-end web client for the HBnB application, providing users with an intuitive interface to interact with the RESTful API developed in Part 3. The application features user authentication, place listings, detailed place views, and review functionality.

---

## Technologies Used

### Front-End
- **HTML5**: Semantic markup and structure
- **CSS3**: Styling with CSS variables and flexbox/grid
- **JavaScript (ES6+)**: Modern JavaScript with async/await
- **Fetch API**: HTTP requests to backend
- **Cookie API**: JWT token management

### Back-End Integration
- **Flask REST API**: Running on `http://localhost:5001`
- **JWT Authentication**: Bearer token authorization
- **CORS**: Cross-origin resource sharing enabled

### Development Tools
- **Python HTTP Server**: Simple development server (`python3 -m http.server 8000`)
- **Git**: Version control

---

## Setup and Installation

### Prerequisites

1. **Part 3 API Server** must be running:
```bash
   cd ../part3
   source venv/bin/activate
   python3 run.py
   # API runs on http://localhost:5001
```

2. **Python 3.x** installed on your system

### Installation Steps

1. **Clone the repository** (if not already done):
```bash
   git clone https://github.com/YOUR_USERNAME/holbertonschool-hbnb.git
   cd holbertonschool-hbnb/part4
```

2. **Start the development server**:
```bash
   python3 -m http.server 8000
```

3. **Access the application**:
   - Open browser: `http://localhost:8000/index.html`

---

## Usage Guide

### Login

1. Navigate to `http://localhost:8000/index.html`
2. Enter credentials:
   - **Email**: `admin@hbnb.com`
   - **Password**: `AdminPass123`
3. Click "Login"
4. Upon success, you'll be redirected to the places listing

**Test Users:**
- `admin@hbnb.com` / `AdminPass123`
- `john@example.com` / `AdminPass123`
- `jane@example.com` / `AdminPass123`

### Browse Places

- View all available places as cards
- Each card displays:
  - Place image (if available)
  - Title
  - Price per night
  - Brief description
  - "View Details" button
- Use price filter dropdown to filter by maximum price:
  - Under $50
  - Under $100
  - Under $200
  - Under $500
  - All Prices

### View Place Details

1. Click "View Details" on any place card
2. View comprehensive information:
   - Full description
   - Location coordinates
   - Amenities list
   - User reviews with ratings
3. Click "Add a Review" (if authenticated)

### Add a Review

1. From place details page, click "Add a Review"
2. Adjust star rating (1-5 stars) using slider
3. Enter review comment (10-500 characters)
4. Click "Submit Review"
5. Success message appears
6. Redirected back to place details

### Logout

- Click "Logout" button in header
- Confirm logout
- Cookie cleared, redirected to login

---

## Implementation Details

### Design & HTML/CSS Structure

**Objective**: Create responsive, accessible HTML pages with modern CSS styling.

**Files Created**:
- `index.html` - Login page
- `places.html` - Places listing
- `place-details.html` - Place details view
- `add-review.html` - Review form
- `static/css/styles.css` - Complete styling

**Key Features**:
- CSS variables for consistent theming
- Flexbox and Grid layouts
- Mobile-responsive design (breakpoints: 768px, 1024px)
- Semantic HTML5 elements
- Accessible forms with proper labels

**CSS Variables**:
```css
:root {
    --primary-color: #007bff;
    --success-color: #28a745;
    --danger-color: #dc3545;
    --text-color: #333;
    --background-color: #f8f9fa;
}
```

---

### Login Implementation

**Objective**: Implement secure user authentication with JWT tokens.

**File**: `static/js/auth.js`

**Key Functions**:

1. **Cookie Management**:
```javascript
   function setCookie(name, value, days)
   function getCookie(name)
   function deleteCookie(name)
```

2. **Login Process**:
```javascript
   async function loginUser(email, password) {
       const response = await fetch(`${API_URL}/auth/login`, {
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify({ email, password })
       });
       const data = await response.json();
       setCookie('token', data.access_token, 1);
       window.location.href = 'places.html';
   }
```

**Authentication Flow**:
1. User submits email/password
2. POST request to `/api/auth/login`
3. API validates credentials
4. Returns JWT token
5. Token stored in cookie (1 day expiration)
6. Redirect to places page

**Error Handling**:
- Invalid credentials display error message
- Network errors caught and displayed
- Form validation for empty fields

---

### Places Listing

**Objective**: Display all places with client-side filtering.

**File**: `static/js/places.js`

**Key Functions**:

1. **Authentication Check**:
```javascript
   function checkAuthentication() {
       const token = getCookie('token');
       if (!token) {
           window.location.href = 'index.html';
           return false;
       }
       return true;
   }
```

2. **Fetch Places**:
```javascript
   async function fetchPlaces(token) {
       const response = await fetch(`${API_URL}/places/`, {
           headers: { 'Authorization': `Bearer ${token}` }
       });
       const places = await response.json();
       displayPlaces(places);
   }
```

3. **Display Places**:
   - Dynamic card creation for each place
   - Image display with fallback
   - Price formatting
   - Navigation to details page

4. **Price Filter**:
```javascript
   function filterPlacesByPrice(maxPrice) {
       const cards = document.querySelectorAll('.place-card');
       cards.forEach(card => {
           const price = parseFloat(card.dataset.price);
           card.style.display = 
               maxPrice === 'all' || price <= maxPrice ? 'flex' : 'none';
       });
   }
```

**Features**:
- Protected route (requires authentication)
- Loading states during fetch
- Error handling for failed requests
- Client-side filtering (no page reload)
- Responsive grid layout

---

### Place Details

**Objective**: Display comprehensive place information including amenities and reviews.

**File**: `static/js/place-details.js`

**Key Functions**:

1. **Get Place ID from URL**:
```javascript
   function getPlaceIdFromURL() {
       const params = new URLSearchParams(window.location.search);
       return params.get('id');
   }
```

2. **Fetch Place Details**:
```javascript
   async function fetchPlaceDetails(token, placeId) {
       const response = await fetch(`${API_URL}/places/${placeId}`, {
           headers: { 'Authorization': `Bearer ${token}` }
       });
       return await response.json();
   }
```

3. **Fetch Reviews**:
```javascript
   async function fetchPlaceReviews(token, placeId) {
       const response = await fetch(
           `${API_URL}/reviews/?place_id=${placeId}`,
           { headers: { 'Authorization': `Bearer ${token}` }}
       );
       const reviews = await response.json();
       return reviews.filter(r => r.place_id === placeId);
   }
```

4. **Display Components**:
   - Place information (title, price, description, location)
   - Amenities list
   - Reviews with star ratings
   - "Add Review" link (authenticated users only)

**Review Display**:
- Star rating visualization (★★★★★)
- User ID (truncated for privacy)
- Comment text
- Date formatting

---

### Add Review Form

**Objective**: Allow authenticated users to submit reviews.

**File**: `static/js/add-review.js`

**Key Functions**:

1. **Star Rating Display**:
```javascript
   function setupStarRating() {
       const ratingInput = document.getElementById('rating');
       ratingInput.addEventListener('input', (e) => {
           const stars = '★'.repeat(e.target.value) + 
                        '☆'.repeat(5 - e.target.value);
           document.getElementById('stars-display').textContent = stars;
       });
   }
```

2. **Submit Review**:
```javascript
   async function submitReview(token, placeId, rating, comment) {
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
       return await response.json();
   }
```

3. **Form Validation**:
   - Rating: 1-5 (enforced by range input)
   - Comment: 10-500 characters (HTML validation)
   - Client-side and server-side validation

**User Flow**:
1. User clicks "Add a Review" from place details
2. Form loads with place_id from URL
3. User adjusts rating slider (live preview)
4. User enters comment
5. Submit → Success message → Redirect to place details
6. New review appears in reviews list

**Features**:
- Interactive star rating preview
- Character count validation
- Submit button disabled during submission
- Success/error message display
- Auto-redirect after success
- Cancel button returns to place details

---

## Security Considerations

### Authentication
- JWT tokens stored in HTTP-only cookies (client-side)
- 1-day token expiration
- Automatic redirect on expired/invalid tokens
- Protected routes check authentication on load

### CORS Configuration
- API configured to accept requests from `http://localhost:8000`
- Flask-CORS enabled in Part 3 API

### Input Validation
- Client-side form validation
- Server-side validation in API
- XSS prevention through proper escaping
- SQL injection prevented by SQLAlchemy ORM

### Data Privacy
- User IDs truncated in display (first 8 characters)
- Passwords never stored or transmitted in plain text
- Bearer token authentication for all protected endpoints

---

## Testing

### Manual Testing Checklist

**Login Functionality**:
- ✅ Valid credentials → successful login → redirect to places
- ✅ Invalid credentials → error message displayed
- ✅ Empty fields → validation error
- ✅ Token saved in cookie
- ✅ Token persists across page refreshes

**Places Listing**:
- ✅ Places load and display correctly
- ✅ Images load with fallback for missing images
- ✅ Price filter works without page reload
- ✅ All filter options functional
- ✅ "View Details" navigates correctly
- ✅ Unauthenticated users redirected to login

**Place Details**:
- ✅ All place information displays
- ✅ Amenities list shows correctly
- ✅ Reviews display with star ratings
- ✅ "Add Review" link only for authenticated users
- ✅ Back navigation works
- ✅ Invalid place_id shows error message

**Add Review**:
- ✅ Form only accessible when authenticated
- ✅ Star rating slider works
- ✅ Live star preview updates
- ✅ Comment validation (10-500 chars)
- ✅ Successful submission → success message
- ✅ Redirect back to place details
- ✅ New review appears in list
- ✅ Cancel returns to place details

**Logout**:
- ✅ Logout confirmation dialog
- ✅ Cookie cleared on logout
- ✅ Redirect to login page
- ✅ Cannot access protected pages after logout

### Browser Compatibility

Tested on:
- ✅ Safari (macOS)
- ✅ Chrome
- ✅ Firefox
- ✅ Mobile Safari (iOS)

---

## Future Enhancements

### Potential Features
- [ ] User registration functionality
- [ ] Password reset flow
- [ ] User profile pages
- [ ] Edit/delete own reviews
- [ ] Place search functionality
- [ ] Advanced filtering (location, amenities)
- [ ] Booking system
- [ ] Wishlist/favorites
- [ ] Image upload for places
- [ ] Real-time notifications
- [ ] Admin dashboard

### Technical Improvements
- [ ] Build process (webpack/vite)
- [ ] TypeScript conversion
- [ ] Unit tests (Jest)
- [ ] E2E tests (Cypress)
- [ ] Progressive Web App (PWA)
- [ ] State management (Redux/Context)
- [ ] Code splitting
- [ ] Performance optimization
- [ ] Accessibility audit

---

## Project Structure Explained

### HTML Pages

**index.html** (Login):
- Simple login form
- Email and password inputs
- Error message display area
- Redirects to places.html on success

**places.html** (Listing):
- Header with logout button
- Price filter dropdown
- Places grid container
- Dynamically populated with JavaScript

**place-details.html** (Details):
- Place information section
- Amenities display
- Reviews list
- Add review link (conditional)

**add-review.html** (Review Form):
- Star rating slider with visual feedback
- Textarea for comment
- Submit and cancel buttons
- Success/error message display

### JavaScript Modules

**auth.js**:
- Handles login/logout
- Cookie management functions
- Form validation
- API authentication requests

**places.js**:
- Fetches places list
- Creates place cards dynamically
- Implements price filtering
- Handles navigation to details

**place-details.js**:
- Fetches individual place data
- Fetches place reviews
- Displays all information
- Manages "Add Review" link visibility

**add-review.js**:
- Handles review form submission
- Star rating interaction
- Form validation
- Success/error handling
- Redirection logic

### CSS Organization

**styles.css** structure:
1. CSS Variables (colors, spacing)
2. Global Styles (reset, typography)
3. Header & Navigation
4. Forms & Inputs
5. Cards & Containers
6. Place Details
7. Reviews
8. Responsive Design (media queries)

---

## Development Workflow

### Starting Development

1. **Terminal 1 - API Server**:
```bash
   cd part3
   source venv/bin/activate
   python3 run.py
```

2. **Terminal 2 - Front-end Server**:
```bash
   cd part4
   python3 -m http.server 8000
```

3. **Browser**:
   - Open `http://localhost:8000/index.html`
   - Open DevTools (F12) for debugging

### Debugging Tips

**JavaScript Errors**:
- Open Console tab in DevTools
- Look for red error messages
- Check line numbers and stack traces

**API Issues**:
- Open Network tab in DevTools
- Click on failed request
- Check Headers, Preview, Response tabs
- Verify request payload and headers

**CSS Issues**:
- Open Elements/Inspector tab
- Select element to see applied styles
- Check for overridden styles
- Use computed styles panel

---

## API Requirements

This front-end requires the Part 3 API with:

- ✅ Flask-CORS enabled
- ✅ JWT authentication configured
- ✅ SQLAlchemy database initialized
- ✅ Test users created
- ✅ All endpoints functional:
  - POST `/api/auth/login`
  - GET `/api/places/`
  - GET `/api/places/{id}`
  - GET `/api/reviews/`
  - POST `/api/reviews/`

### Required Environment Variables (Part 3)
```env
USE_DATABASE=true
JWT_SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/development.db
```
