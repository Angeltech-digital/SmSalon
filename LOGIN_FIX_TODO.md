# Login 500 Error Fix Plan

## Problem
The login endpoint `/api/auth/login/` returns a 500 Internal Server Error with HTML content instead of JSON. This causes the frontend to fail parsing the response.

## Root Causes Identified
1. **SignupView not registered** - Defined in views.py but not imported in urls.py
2. **No exception handling in LoginView** - If `authenticate()` throws an exception, it causes a 500 error
3. **Missing proper error responses** - Unhandled exceptions return Django's debug HTML page

## Fix Plan

### Step 1: Fix urls.py - Add missing SignupView import and route
- [x] Import `SignupView`, `LogoutView`, `UserProfileView` from views
- [x] Add route for `auth/signup/`
- [x] Add route for `auth/logout/`
- [x] Add route for `auth/profile/`

### Step 2: Enhance LoginView with exception handling
- [x] Wrap `authenticate()` call in try/except
- [x] Wrap `RefreshToken.for_user()` in try/except
- [x] Return proper JSON error responses for all exceptions
- [x] Add logging for debugging

### Step 3: Deploy and test
- [ ] Run migrations on production server
- [ ] Create admin user with `python setup_data.py --create-admin --password=YourPassword123`
- [ ] Deploy changes to DigitalOcean
- [ ] Test login endpoint

## Files Modified
1. `Backend/salon_app/urls.py` - Added all auth views
2. `Backend/salon_app/views.py` - Added exception handling to LoginView

## Required Next Steps
1. **Run on DigitalOcean server:**
   ```bash
   cd Backend
   python manage.py migrate --run-syncdb
   python setup_data.py --create-admin --password=YourAdminPassword123
   ```
2. **Deploy changes:** Push code and restart the Django app
3. **Test:** Try logging in at `https://smsalonandbarbershop-px697.ondigitalocean.app/login.html`

