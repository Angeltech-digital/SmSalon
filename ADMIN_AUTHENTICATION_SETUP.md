# Admin Authentication Setup Guide

## What's Been Added

I've successfully implemented a complete authentication system for your salon admin panel. Here's what was created:

### Backend Components

#### 1. **JWT Authentication with Django REST Framework**
   - Added `djangorestframework-simplejwt` to requirements.txt
   - Configured JWT settings in `settings.py`
   - Access token lifetime: 1 hour
   - Refresh token lifetime: 1 day

#### 2. **Authentication Views** (`views.py`)
   - `SignupView` - Register new admin users
   - `LoginView` - Authenticate users
   - `LogoutView` - Revoke refresh tokens
   - `UserProfileView` - Get and update user profile

#### 3. **Authentication URLs** (`urls.py`)
   - `/api/auth/signup/` - Register
   - `/api/auth/login/` - Login
   - `/api/auth/logout/` - Logout
   - `/api/auth/profile/` - Get/Update profile
   - `/api/auth/token/` - Get JWT token
   - `/api/auth/token/refresh/` - Refresh access token

### Frontend Components

#### 1. **Login Page** (`login.html`)
   - Clean, modern UI with gradient background
   - Username/password fields
   - Error and success message displays
   - Client-side form validation
   - Auto-redirect if already logged in
   - Token storage in localStorage

#### 2. **Signup Page** (`signup.html`)
   - Registration form for new admins
   - Password strength requirements
   - Form validation
   - First name and last name fields
   - Password confirmation check
   - Responsive design

#### 3. **Admin Dashboard** (`admin-dashboard.html`)
   - Full-featured admin panel with sidebar navigation
   - Dashboard with statistics:
     - Total bookings count
     - Confirmed bookings
     - Pending bookings
     - Active stylists count
   - Sections:
     - Dashboard (statistics & recent bookings)
     - Bookings (view all bookings)
     - Stylists (manage stylists)
     - Services (manage services)
     - Messages (contact messages)
     - Reviews (customer reviews)
     - My Profile (update profile)
   - User profile section (top-right)
   - Logout button
   - Responsive mobile-friendly design

#### 4. **Navigation Update**
   - Added "Admin" link to main index.html navbar
   - Link to login.html for easy access

### Documentation

- **AUTH_API_DOCUMENTATION.md** - Complete API reference with examples
  - Endpoint descriptions
  - Request/response examples
  - Error codes
  - Security notes
  - cURL testing examples

---

## Installation & Setup

### 1. Install Backend Dependencies

```bash
cd /home/angela/Salon/Backend
pip install -r requirements.txt
```

This will install:
- `djangorestframework-simplejwt==5.3.2` (for JWT authentication)
- All other existing dependencies

### 2. Run Migrations

```bash
cd /home/angela/Salon/Backend
python manage.py migrate
```

This creates the necessary database tables for authentication.

### 3. Create a Superuser (Optional but Recommended)

```bash
python manage.py createsuperuser
```

This allows you to manage users through Django admin at `/admin/`.

### 4. Test the Backend

Start the Django development server:

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api`

### 5. Access Frontend

Open your browser and navigate to:
- **Main site:** `http://localhost:8000/` or local file
- **Login:** `Frontend/login.html`
- **Signup:** `Frontend/signup.html`
- **Dashboard:** `Frontend/admin-dashboard.html` (after login)

---

## How to Use

### First Time Setup

1. **Register as Admin:**
   - Go to `Frontend/signup.html`
   - Fill in the registration form
   - Username, email, password (min 6 characters)
   - First and last name (optional)
   - Click "Create Account"

2. **Auto-Redirect:**
   - After successful signup, you'll be redirected to the admin dashboard
   - Your tokens are stored in localStorage

3. **Access Admin Panel:**
   - Visit `Frontend/admin-dashboard.html` directly
   - Or click "Admin" link from main site

### Subsequent Logins

1. Go to `Frontend/login.html`
2. Enter your username and password
3. Click "Login to Admin Panel"
4. You'll be redirected to the dashboard

### Features Available

- View all bookings with filtering options
- Manage stylists
- Manage services
- View contact messages
- View and approve reviews
- Update your profile

---

## API Endpoints Summary

### Authentication Endpoints (Public)
- `POST /api/auth/signup/` - Register new admin
- `POST /api/auth/login/` - Login admin
- `POST /api/auth/token/` - Get JWT token
- `POST /api/auth/token/refresh/` - Refresh access token

### Protected Endpoints (Requires JWT Token)
- `GET /api/auth/profile/` - Get current user profile
- `PUT /api/auth/profile/` - Update user profile
- `POST /api/auth/logout/` - Logout user

All other endpoints (bookings, stylists, services, etc.) can be accessed with the bearer token.

---

## Token Management

### How Tokens Work

1. **Access Token:** Short-lived (1 hour), used for API requests
   - Include in header: `Authorization: Bearer <access_token>`
   - Stored in: `localStorage.access_token`

2. **Refresh Token:** Long-lived (1 day), used to get new access tokens
   - Stored in: `localStorage.refresh_token`
   - Used at: `POST /api/auth/token/refresh/`

### Manual Token Refresh (Optional)

If needed, you can refresh the token programmatically:

```javascript
const response = await fetch('http://localhost:8000/api/auth/token/refresh/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    refresh: localStorage.getItem('refresh_token')
  })
});

const data = await response.json();
localStorage.setItem('access_token', data.access);
```

---

## Configuration

### Backend Settings

All authentication settings are in `Backend/salon_project/settings.py`:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    # ... other settings
}
```

### Frontend API Configuration

The frontend uses this base URL:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

To change this in production:

1. Update `login.html` - Change `API_BASE_URL`
2. Update `signup.html` - Change `API_BASE_URL`
3. Update `admin-dashboard.html` - Change `API_BASE_URL`

---

## Testing

### Test Sign Up via cURL

```bash
curl -X POST http://localhost:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testadmin",
    "email": "test@example.com",
    "password": "test1234",
    "password_confirm": "test1234",
    "first_name": "Test",
    "last_name": "Admin"
  }'
```

### Test Login via cURL

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testadmin",
    "password": "test1234"
  }'
```

### Test Protected Endpoint

```bash
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

---

## Security Notes

⚠️ **Important for Production:**

1. **Change SECRET_KEY**
   - Current: `django-insecure-change-this-in-production`
   - Update in `.env` or `settings.py`

2. **Enable HTTPS**
   - Required for token transmission
   - Use SSL certificates

3. **Use Environment Variables**
   - Store sensitive data in `.env` files
   - Never commit secrets to version control

4. **Update CORS Settings**
   - Production domain should be added to `CORS_ALLOWED_ORIGINS`
   - Remove localhost origins in production

5. **Use httpOnly Cookies (Optional)**
   - Better than localStorage for storing tokens
   - Prevents XSS attacks
   - Requires additional configuration

6. **Implement Rate Limiting**
   - Protect login endpoint from brute force
   - Consider using `django-ratelimit`

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'rest_framework_simplejwt'"

**Solution:**
```bash
pip install djangorestframework-simplejwt==5.3.2
```

### Issue: CORS Error in Browser Console

**Solution:** Check `CORS_ALLOWED_ORIGINS` in settings.py and add your domain.

### Issue: "Invalid token" when accessing dashboard

**Solution:**
1. Clear localStorage: `localStorage.clear()`
2. Logout and login again
3. Check token hasn't expired (1 hour)

### Issue: Can't connect to API

**Solution:**
1. Ensure Django server is running: `python manage.py runserver`
2. Check API base URL matches in frontend code
3. Verify CORS is properly configured

---

## Next Steps

### Optional Enhancements

1. **Email Verification**
   - Add email confirmation on signup
   - Send activation link

2. **Password Reset**
   - Implement forgot password functionality
   - Send reset link via email

3. **Two-Factor Authentication**
   - Add 2FA for enhanced security
   - SMS or email OTP

4. **Role-Based Access**
   - Different admin roles (manager, stylist, receptionist)
   - Permissions based on roles

5. **Audit Logging**
   - Track admin actions
   - Log all modifications

6. **User Management**
   - Admin can manage other admin accounts
   - Disable/enable users

---

## File Locations

```
/home/angela/Salon/
├── Backend/
│   ├── salon_app/
│   │   ├── views.py (authentication views added)
│   │   └── urls.py (auth endpoints added)
│   ├── salon_project/
│   │   └── settings.py (JWT config added)
│   ├── requirements.txt (simplejwt added)
│   └── AUTH_API_DOCUMENTATION.md (new)
└── Frontend/
    ├── login.html (new)
    ├── signup.html (new)
    ├── admin-dashboard.html (new)
    └── index.html (admin link added)
```

---

## Summary

Your Salon Management System now has a complete authentication system with:
- ✅ Secure JWT-based authentication
- ✅ User registration and login
- ✅ Protected admin dashboard
- ✅ Responsive design
- ✅ Complete API documentation
- ✅ Easy token management

Start by running `pip install -r requirements.txt`, then `python manage.py runserver`, and visit `Frontend/login.html` to get started!
