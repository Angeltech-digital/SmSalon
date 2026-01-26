# Salon MVP - Frontend Setup Guide

## Project Structure

```
Frontend/
├── index.html          # Home page
├── services.html       # Services page
├── booking.html        # Booking page
├── about.html          # About page
├── contact.html        # Contact page
├── styles.css          # Main styling
├── script.js           # JavaScript functionality
└── README.md          # This file
```

## Features Included

### 1. **Responsive Design**
- Mobile-first approach
- Works on all screen sizes (320px to 4K)
- Touch-friendly interface for mobile users

### 2. **Home Page**
- Hero section with booking CTA
- Services preview
- Why choose us section
- Navigation & footer

### 3. **Services Page**
- All salon services listed
- Service categories (Hair, Nails, Makeup, Braiding)
- Pricing displayed
- Quick booking link

### 4. **Booking System**
- Form with all required fields
- Validation (dates, phone numbers)
- Auto-save to browser storage
- Submit to backend API
- Success confirmation

### 5. **About Page**
- Salon story
- Mission & values
- Team member profiles
- Years of experience

### 6. **Contact Page**
- Contact form
- Phone number (clickable)
- WhatsApp chat link
- Email
- Location with Google Map
- Social media links

## Quick Start (Without Backend)

### Method 1: Simple File Opening
```bash
cd Frontend

# Open in browser
open index.html  # Mac
start index.html # Windows
xdg-open index.html # Linux
```

Or right-click any HTML file → Open with Browser

### Method 2: Using Python HTTP Server
```bash
cd Frontend

# Python 3
python -m http.server 8001

# Python 2
python -m SimpleHTTPServer 8001
```

Then open: `http://localhost:8001`

### Method 3: Using Node.js
```bash
# Install http-server
npm install -g http-server

# Start server
http-server Frontend -p 8001
```

## Connect to Backend API

### 1. Update API Endpoints in `script.js`

Find these lines in `script.js`:

```javascript
// Line ~85: Change this URL
fetch('http://localhost:8000/api/bookings/', {
```

### 2. Configure Backend URL

Create a config file at the top of `script.js`:

```javascript
// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// Service endpoints
const API_ENDPOINTS = {
    bookings: `${API_BASE_URL}/bookings/`,
    contacts: `${API_BASE_URL}/contacts/`,
    services: `${API_BASE_URL}/services/`,
    settings: `${API_BASE_URL}/settings/current/`,
};
```

### 3. Update Frontend to Use Config

Replace fetch URLs:
```javascript
// Old
fetch('http://localhost:8000/api/bookings/', { ... })

// New
fetch(API_ENDPOINTS.bookings, { ... })
```

## Features Details

### Booking Form Validation
- ✅ Full name required
- ✅ Phone number format validation
- ✅ Date must be future date
- ✅ Time validation (9 AM - 8 PM)
- ✅ Email optional but validated if provided

### Form Auto-Save
- Booking form data saved to browser storage automatically
- Data persists even if page is refreshed
- User can continue from where they left off

### WhatsApp Integration
- Click-to-chat link to salon WhatsApp number
- Message pre-filled with appointment details
- Update salon number in script.js

### Mobile Navigation
- Hamburger menu for mobile
- Automatic menu closing when link clicked
- Full-width mobile menu

## Customization

### 1. Change Salon Name & Colors

In `styles.css`:
```css
:root {
    --primary-color: #d4a5a5;      /* Your brand color */
    --secondary-color: #8b6f6f;     /* Secondary color */
    --accent-color: #f4d4d4;
    --dark-color: #3d3d3d;
    --light-color: #f9f7f7;
}
```

### 2. Update Salon Information

In `script.js`:
```javascript
const SALON_INFO = {
    name: 'Salon',
    phone: '+254712345678',
    whatsapp: '254712345678',
    email: 'info@salon.com',
    address: '123 Beauty Lane, Nairobi'
};
```

### 3. Change Navigation Links

In HTML files, update navbar links if needed.

### 4. Update Services List

Edit `services.html`:
```html
<div class="service-item">
    <div class="service-info">
        <h3>Your Service Name</h3>
        <p>Service description</p>
    </div>
    <span class="price">KES 0</span>
</div>
```

## Testing Checklist

- [ ] All pages load correctly
- [ ] Responsive on mobile (test with DevTools)
- [ ] Forms submit without errors
- [ ] Booking form saves data
- [ ] WhatsApp link works
- [ ] Google Map loads
- [ ] Images load properly
- [ ] Links work (internal and external)
- [ ] Dark mode (if browser supports)
- [ ] Accessibility (keyboard navigation, screen readers)

## Performance Optimization

### 1. Image Optimization
```html
<!-- Use optimized images -->
<img src="image.webp" alt="Description" loading="lazy">
```

### 2. CSS Optimization
- Minify styles.css for production
- Remove unused CSS

### 3. JavaScript Optimization
- Minify script.js
- Defer non-critical scripts
- Use lazy loading

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Troubleshooting

### CORS Errors
**Problem**: "Access to XMLHttpRequest blocked by CORS policy"

**Solution**: 
1. Make sure backend is running
2. Check CORS_ALLOWED_ORIGINS in Django settings
3. Ensure frontend URL is in allowed origins

### Form Won't Submit
**Problem**: Booking form doesn't submit

**Solutions**:
1. Check browser console for errors (F12)
2. Verify backend is running
3. Check API endpoint URL
4. Validate form data

### Styles Not Loading
**Problem**: Page looks unstyled

**Solutions**:
1. Check CSS file path
2. Refresh browser (Ctrl+Shift+R)
3. Clear browser cache
4. Check browser console for 404 errors

## Production Deployment

### 1. Minify CSS & JS
```bash
# Using csso-cli
npm install -g csso-cli
csso styles.css -o styles.min.css

# Using terser
npm install -g terser
terser script.js -o script.min.js
```

### 2. Update HTML to Use Minified Files
```html
<link rel="stylesheet" href="styles.min.css">
<script src="script.min.js"></script>
```

### 3. Deploy to Server
```bash
# Via FTP/SFTP or Git
scp -r Frontend/* user@your-server:/var/www/salon/frontend
```

### 4. Configure Web Server (Nginx)
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    root /var/www/salon/frontend;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://your-backend:8000;
    }
}
```

## Next Steps

1. ✅ Customize salon name & colors
2. ✅ Update contact information
3. ✅ Connect to backend API
4. ✅ Test all forms
5. ✅ Deploy to server
6. ✅ Setup domain & SSL
7. ✅ Monitor performance

---

**Questions?** Check the main README or contact support.
