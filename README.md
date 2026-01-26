# 🧴 Salon Website MVP - Complete Code Package

A complete, production-ready Minimum Viable Product (MVP) for a salon website with booking system.

## 📋 What's Included

### ✨ Features
- ✅ **Responsive Home Page** - Hero section with salon vibe
- ✅ **Services Page** - All services with pricing
- ✅ **Appointment Booking** - Complete booking form with validation
- ✅ **About Page** - Salon story & team
- ✅ **Contact Page** - Phone, WhatsApp, Email, Map
- ✅ **Mobile Optimized** - Works perfectly on all devices
- ✅ **Admin Dashboard** - Django admin for management
- ✅ **Email Notifications** - Booking confirmations
- ✅ **Responsive Design** - Beautiful on all screens

### 📁 Project Structure

```
Salon/
├── Frontend/                    # Website code
│   ├── index.html              # Home page
│   ├── services.html           # Services list
│   ├── booking.html            # Booking form
│   ├── about.html              # About page
│   ├── contact.html            # Contact page
│   ├── styles.css              # Styling
│   ├── script.js               # JavaScript
│   └── README.md               # Frontend guide
│
└── Backend/                     # Django API
    ├── manage.py
    ├── requirements.txt        # Python dependencies
    ├── .env.example            # Environment template
    ├── README.md               # Backend setup guide
    ├── DEPLOYMENT.md           # Production guide
    │
    ├── salon_project/          # Main Django project
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    │
    └── salon_app/              # Django app
        ├── models.py           # Database models
        ├── views.py            # API views
        ├── serializers.py      # Data serialization
        ├── urls.py             # API routes
        ├── admin.py            # Admin panel
        └── migrations/
```

## 🚀 Quick Start (2 Minutes)

### Option 1: Frontend Only (No Backend)

```bash
# Navigate to frontend
cd Frontend

# Open in browser
# Option A: Direct open
open index.html  # macOS
start index.html # Windows
xdg-open index.html # Linux

# Option B: Python HTTP Server
python -m http.server 8001
# Visit: http://localhost:8001
```

### Option 2: Full Stack (Frontend + Backend)

#### Step 1: Start Backend
```bash
cd Backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start server
python manage.py runserver
# Runs at: http://localhost:8000
```

#### Step 2: Start Frontend
```bash
cd Frontend

# In another terminal
python -m http.server 8001
# Visit: http://localhost:8001
```

## 📚 Complete Setup Guides

### For Frontend Developers
👉 See [Frontend/README.md](Frontend/README.md)
- Customization guide
- How to change colors & content
- Testing checklist
- Deployment instructions

### For Backend Developers
👉 See [Backend/README.md](Backend/README.md)
- Django setup
- Database configuration
- Email setup
- API documentation

### For Deployment
👉 See [Backend/DEPLOYMENT.md](Backend/DEPLOYMENT.md)
- DigitalOcean setup
- Production configuration
- SSL/HTTPS setup
- Monitoring & backups

## 🔧 Tech Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern responsive design
- **JavaScript** - Vanilla JS (no frameworks)
- **Features:**
  - Mobile responsive
  - Form validation
  - Auto-save functionality
  - WhatsApp integration
  - Google Maps embed

### Backend
- **Django 4.2** - Python web framework
- **Django REST Framework** - API
- **MySQL/SQLite** - Database
- **Celery** - Background tasks (optional)
- **SMTP** - Email notifications

## 📱 Pages Overview

### 1. Home Page (`index.html`)
- Hero section with CTA
- Services preview (4 cards)
- Why choose us
- Navigation & footer

### 2. Services Page (`services.html`)
- Complete service list
- Organized by category
- Prices displayed
- Quick book button

### 3. Booking Page (`booking.html`)
- Personal info fields
- Service selection
- Date & time picker
- Stylist selection
- Notes field
- Form validation
- Success confirmation

### 4. About Page (`about.html`)
- Salon story
- Mission & values
- Team profiles
- Experience stats

### 5. Contact Page (`contact.html`)
- Contact form
- Phone number
- WhatsApp click-to-chat
- Email link
- Location with Google Map
- Social media links

## 🎨 Customization

### Change Salon Name
1. Update `SALON_INFO` in `Frontend/script.js`
2. Update navbar logo in HTML files
3. Update admin site name in `Backend/salon_project/settings.py`

### Change Colors
Edit `Frontend/styles.css`:
```css
:root {
    --primary-color: #d4a5a5;      /* Main brand color */
    --secondary-color: #8b6f6f;    /* Secondary color */
    --accent-color: #f4d4d4;       /* Accent color */
}
```

### Add Services
1. Add in Django admin panel
2. Or insert directly in database

### Update Contact Info
1. `Frontend/script.js` - SALON_INFO
2. `Backend/.env` - EMAIL_HOST_USER, etc.
3. `Backend/salon_app/models.py` - SalonSettings

## 🔌 API Endpoints

All endpoints at: `http://localhost:8000/api/`

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/services/` | List all services |
| GET | `/services/{id}/` | Service details |
| GET | `/stylists/` | List stylists |
| GET | `/stylists/{id}/available-slots/?date=YYYY-MM-DD` | Available time slots |
| **POST** | **`/bookings/`** | **Create booking** |
| GET | `/bookings/` | List bookings |
| GET | `/bookings/{id}/` | Booking details |
| POST | `/bookings/{id}/confirm/` | Confirm booking |
| POST | `/bookings/{id}/cancel/` | Cancel booking |
| **POST** | **`/contacts/`** | **Send message** |
| GET | `/reviews/` | Approved reviews |
| POST | `/reviews/` | Submit review |
| GET | `/settings/current/` | Salon settings |

## 💾 Database Schema

### Services
```python
name, category, description, price, duration_minutes, is_active
```

### Bookings
```python
fullname, phone, email, service, stylist, date, time, notes, status
```

### Stylists
```python
name, email, phone, specialization, bio, photo, available_services
```

### Contact Messages
```python
name, email, subject, message, is_read, replied
```

## 📧 Email Setup

### Using Gmail
1. Enable 2-Factor Authentication
2. Create App Password: https://myaccount.google.com/apppasswords
3. Add to `.env`:
   ```
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=generated-app-password
   ```

### Using Other Email Providers
- Zoho Mail
- SendGrid
- AWS SES
- Mailgun

See `Backend/README.md` for detailed instructions.

## 🧪 Testing

### Frontend Testing
```bash
cd Frontend
# Open in browser and test:
# - All pages load
# - Forms work
# - Mobile responsive (F12 DevTools)
# - Links function
# - WhatsApp link works
```

### Backend Testing
```bash
cd Backend
source venv/bin/activate

# Run tests
python manage.py test

# Test specific model
python manage.py test salon_app.tests.BookingTest
```

## 🔐 Security Checklist

- [ ] Change SECRET_KEY in Django
- [ ] Set DEBUG=False for production
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS/SSL
- [ ] Configure ALLOWED_HOSTS
- [ ] Setup CORS properly
- [ ] Regular database backups
- [ ] Monitor error logs
- [ ] Update dependencies regularly

## 📊 Monitoring

### View Logs
```bash
# Django logs
tail -f Backend/logs/salon.log

# Check database
python manage.py dbshell

# View admin panel
http://localhost:8000/admin/
```

### Monitor Services
```bash
# Check if backend is running
curl http://localhost:8000/api/health/

# Check frontend
curl http://localhost:8001
```

## 🚀 Deployment

### Quick Deploy to DigitalOcean
```bash
# See Backend/DEPLOYMENT.md for full instructions
# Summary:
# 1. Create droplet (Ubuntu 22.04 LTS, 2GB RAM)
# 2. SSH into server
# 3. Clone repo
# 4. Setup Python environment
# 5. Configure database
# 6. Setup Nginx + Gunicorn
# 7. Enable SSL with Let's Encrypt
# 8. Deploy frontend
```

**Estimated cost:** $5-12/month on DigitalOcean

## 🆘 Troubleshooting

### CORS Errors
```
Problem: "Access to XMLHttpRequest blocked by CORS policy"
Solution: Backend not running or CORS not configured
```

### Form Won't Submit
```
Problem: Booking form doesn't submit
Solution: 
1. Check browser console (F12)
2. Verify backend is running
3. Check API endpoint in script.js
```

### Styles Not Loading
```
Problem: Page looks unstyled
Solution:
1. Refresh with Ctrl+Shift+R
2. Check CSS file path
3. Check console for 404 errors
```

### Database Errors
```
Problem: "No such table" or migration errors
Solution:
1. Run: python manage.py migrate
2. Check database connection
3. Review settings.py
```

## 📞 Support Resources

- Django Docs: https://docs.djangoproject.com
- REST Framework: https://www.django-rest-framework.org
- MDN Web Docs: https://developer.mozilla.org
- DigitalOcean Docs: https://docs.digitalocean.com

## 📝 License

This code is provided as-is for salon websites. Customize as needed.

## 🎯 Next Steps

1. **Customize** - Update salon info, colors, content
2. **Test** - Try all features in both desktop & mobile
3. **Configure** - Set up email, database, environment
4. **Deploy** - Launch on your domain
5. **Monitor** - Check logs and fix issues
6. **Enhance** - Add payment (M-Pesa), reviews, gallery (Phase 2)

## 📞 Quick Reference

| Task | Command |
|------|---------|
| Start frontend | `cd Frontend && python -m http.server 8001` |
| Start backend | `cd Backend && python manage.py runserver` |
| Create superuser | `python manage.py createsuperuser` |
| Database migrations | `python manage.py migrate` |
| Create backup | See `Backend/DEPLOYMENT.md` |
| View admin | `http://localhost:8000/admin/` |
| View frontend | `http://localhost:8001` |

---

**Built with ❤️ for salon businesses in Kenya and beyond.**

Made simple. Made beautiful. Made for your salon.

