# TODO: User vs Admin Login Differentiation

## Backend Changes ✅ COMPLETED
- [x] 1. Update `Backend/salon_app/views.py` - Modified LoginView to return user_type, added CustomerLoginView and AdminLoginView
- [x] 2. Update `Backend/salon_app/urls.py` - Added customer and admin login endpoints

## Frontend Changes ✅ COMPLETED
- [x] 3. Create `Frontend/customer-login.html` - Separate login page for customers
- [x] 4. Create `Frontend/customer-dashboard.html` - Customer dashboard for viewing bookings
- [x] 5. Update `Frontend/login.html` - Now uses admin-specific login endpoint with role-based redirect
- [x] 6. Update `Frontend/signup.html` - Added choice between customer and admin signup
- [x] 7. Update `Frontend/admin-dashboard.html` - Added customer redirect check
- [x] 8. Update `Frontend/index.html` - Added dropdown with both login options and Book Now button
- [x] 9. Update `Frontend/styles.css` - Added dropdown menu and book link styles

## Setup Script ✅ COMPLETED
- [x] 10. Create `create_admin.py` - Script to create admin user with staff privileges

## Usage Instructions
1. **To create an admin user**, run:
   ```bash
   cd /home/angela/SmSalon
   python create_admin.py
   ```
   
2. **Admin Login Flow**:
   - Go to `login.html` or click "Admin Login" in the dropdown
   - Use admin credentials (username: admin, password: admin123)
   - Redirects to `admin-dashboard.html`

3. **Customer Login Flow**:
   - Go to `customer-login.html` or click "Customer Login" in the dropdown
   - Sign up as a customer via `signup.html` (select "Customer" option)
   - Redirects to `customer-dashboard.html`

## API Endpoints
- `POST /api/auth/login/` - Generic login (auto-detects user type)
- `POST /api/auth/customer/login/` - Customer-only login
- `POST /api/auth/admin/login/` - Admin-only login


