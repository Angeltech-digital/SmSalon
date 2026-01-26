# Quick Start: Admin Authentication

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
cd Backend
pip install -r requirements.txt
```

### Step 2: Run Migrations
```bash
python manage.py migrate
```

### Step 3: Start Server
```bash
python manage.py runserver
```

---

## 📱 Access Points

| Page | URL |
|------|-----|
| **Login** | `Frontend/login.html` |
| **Signup** | `Frontend/signup.html` |
| **Dashboard** | `Frontend/admin-dashboard.html` (after login) |
| **Django Admin** | `http://localhost:8000/admin/` |

---

## 🔐 New Auth Endpoints

All require JWT token in header: `Authorization: Bearer <token>`

```
POST   /api/auth/signup/          - Register admin
POST   /api/auth/login/           - Login admin  
GET    /api/auth/profile/         - Get profile
PUT    /api/auth/profile/         - Update profile
POST   /api/auth/logout/          - Logout
POST   /api/auth/token/           - Get token
POST   /api/auth/token/refresh/   - Refresh token
```

---

## 📝 Default Test Account (Create New)

Username: `admin`
Password: `admin123456`
Email: `admin@salon.com`

Create via frontend signup or:

```bash
python manage.py createsuperuser
```

---

## 🎯 Features Added

✅ JWT Token Authentication
✅ User Registration & Login
✅ Admin Dashboard with:
   - Booking Management
   - Stylist Management
   - Service Management
   - Contact Messages
   - Customer Reviews
   - Profile Management
✅ Secure Token Storage
✅ Auto-Redirect When Logged In
✅ Responsive Mobile Design

---

## 🔧 Key Files Modified/Created

**Backend:**
- `salon_app/views.py` - Auth views added
- `salon_app/urls.py` - Auth routes added
- `salon_project/settings.py` - JWT config added
- `requirements.txt` - djangorestframework-simplejwt added

**Frontend:**
- `login.html` ⭐ NEW
- `signup.html` ⭐ NEW
- `admin-dashboard.html` ⭐ NEW
- `index.html` - Admin link added

**Documentation:**
- `AUTH_API_DOCUMENTATION.md` ⭐ NEW
- `ADMIN_AUTHENTICATION_SETUP.md` ⭐ NEW

---

## ⚠️ Important Notes

1. **Access tokens expire after 1 hour** - Use refresh token to get new one
2. **Refresh tokens expire after 1 day** - User must login again
3. **Never use localStorage for tokens in production** - Use httpOnly cookies
4. **Change SECRET_KEY before deployment** - Update in settings.py
5. **Add your domain to CORS_ALLOWED_ORIGINS** - For production use

---

## 🧪 Quick Test with cURL

```bash
# Signup
curl -X POST http://localhost:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@salon.com",
    "password": "admin123456",
    "password_confirm": "admin123456",
    "first_name": "Admin",
    "last_name": "User"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123456"
  }'

# Get Profile (use token from login response)
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🎨 Frontend Features

### Login Page
- Clean gradient design
- Form validation
- Error/success messages
- Loading spinner
- Auto-redirect if already logged in

### Signup Page  
- Full registration form
- Password strength checker
- Real-time validation
- First/last name fields
- Mobile responsive

### Admin Dashboard
- Sidebar navigation
- Statistics cards (total, confirmed, pending bookings, stylists)
- Recent bookings table
- Full data management sections:
  - All Bookings
  - Stylists Management
  - Services Management
  - Contact Messages
  - Customer Reviews
  - Profile Management
- User profile dropdown
- Logout button
- Mobile-friendly responsive design

---

## 🚨 Troubleshooting

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError: simplejwt | `pip install djangorestframework-simplejwt` |
| CORS Error | Add domain to CORS_ALLOWED_ORIGINS in settings.py |
| Invalid Token | Clear localStorage and login again |
| Can't reach API | Ensure `python manage.py runserver` is running |
| 404 on /api/auth/ | Check urls.py has auth endpoints included |

---

## 📚 Full Documentation

See `AUTH_API_DOCUMENTATION.md` for:
- Complete API reference
- Request/response examples
- All error codes
- Security best practices
- Frontend integration examples

See `ADMIN_AUTHENTICATION_SETUP.md` for:
- Detailed setup instructions
- Configuration guide
- Testing procedures
- Production checklist

---

## 💡 Next Steps

1. ✅ Install dependencies
2. ✅ Run migrations
3. ✅ Start Django server
4. ✅ Test signup at Frontend/signup.html
5. ✅ Test dashboard at Frontend/admin-dashboard.html
6. ✅ Manage your salon data!

---

## 📞 Support

For issues:
1. Check error message in browser console
2. Review AUTH_API_DOCUMENTATION.md
3. Check ADMIN_AUTHENTICATION_SETUP.md Troubleshooting section
4. Verify Django server is running with `python manage.py runserver`

Enjoy your new admin panel! 🎉
