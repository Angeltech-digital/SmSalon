# 🚀 Quick Start Guide - Salon Booking Website

Your salon website is now **fully functional**! Here's how to run it:

## ✅ Setup Complete

- ✓ Backend: Django installed and configured  
- ✓ Database: Migrations applied, services created
- ✓ Admin: Superuser created (admin / admin123)
- ✓ Frontend: Ready to test

---

## 1️⃣ Start the Backend (API Server)

```bash
cd /home/angela/Salon/Backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

**Backend will run at:** http://localhost:8000

**API Documentation:** 
- Services: http://localhost:8000/api/services/
- Bookings: http://localhost:8000/api/bookings/
- Contact: http://localhost:8000/api/contact/
- Admin Panel: http://localhost:8000/admin/

**Admin Login:**
- Username: `admin`
- Password: `admin123`

---

## 2️⃣ Start the Frontend (In a NEW Terminal)

```bash
cd /home/angela/Salon/Frontend
python -m http.server 8001
```

**Frontend will run at:** http://localhost:8001

---

## 🎯 What You Can Do Now

### 1. View the Website
- Open http://localhost:8001 in your browser
- All pages fully functional: Home, Services, Booking, About, Contact

### 2. Test Booking System
- Go to **Booking** page
- Fill in the form (name, phone, email, service, date, time, stylist)
- Submit booking - it will save to the database
- Check backend admin panel to see bookings

### 3. Admin Panel
- Open http://localhost:8000/admin/
- Login with: admin / admin123
- Manage:
  - Services (add/edit/delete)
  - Stylists (create team members, assign services)
  - Bookings (confirm, complete, cancel)
  - Contact messages (replies)
  - Reviews (approve testimonials)
  - Settings (salon info, hours, social media)

### 4. API Testing
Test API endpoints directly:

```bash
# Get all services
curl http://localhost:8000/api/services/

# Get bookings
curl http://localhost:8000/api/bookings/

# Get salon settings
curl http://localhost:8000/api/settings/current/
```

---

## 🔧 Additional Configuration

### Email Setup (Optional)
To enable booking confirmation emails:

1. Open `/home/angela/Salon/Backend/.env`
2. Add your email credentials:
   ```
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   DEFAULT_FROM_EMAIL=your-email@gmail.com
   ```
3. Restart backend

### Add Stylists
1. Go to http://localhost:8000/admin/
2. Click "Stylists"
3. Add new stylists with specializations
4. Clients can choose stylists when booking

### Customize Services
1. Go to http://localhost:8000/admin/
2. Click "Services"
3. Add/edit/delete services with pricing and duration

---

## 📱 Responsive Design

The website is fully responsive:
- **Desktop:** Full width with navigation menu
- **Tablet:** Optimized layout
- **Mobile:** Hamburger menu, stacked layout

Test by resizing your browser or using mobile view (F12 → Toggle device toolbar)

---

## 🐛 Troubleshooting

### Backend won't start
```bash
cd /home/angela/Salon/Backend
source venv/bin/activate
python manage.py migrate  # Ensure DB is initialized
python manage.py runserver
```

### Frontend shows "Cannot GET" on other pages
- Make sure you're running from port 8001
- Refresh the browser (Ctrl+Shift+R)

### Booking form not submitting
- Check backend is running (http://localhost:8000/)
- Check browser console (F12 → Console tab)
- Verify CORS is enabled in Django settings

### Admin login fails
- Reset password: 
  ```bash
  cd /home/angela/Salon/Backend
  source venv/bin/activate
  python manage.py changepassword admin
  ```

---

## 📁 Project Structure

```
/home/angela/Salon/
├── Frontend/              # Website files (HTML, CSS, JS)
├── Backend/               # Django API server
│   ├── salon_app/        # Main app models, views, serializers
│   ├── salon_project/    # Django settings, URLs, WSGI
│   ├── db.sqlite3        # Database file
│   ├── requirements.txt   # Python packages
│   ├── manage.py         # Django CLI
│   └── venv/             # Virtual environment (Python 3.10)
└── Documentation files
```

---

## 🚀 Next Steps

1. **Test all features** - Go through the website and test booking, contact form, etc.
2. **Customize content** - Edit services, pricing, salon information
3. **Add stylists** - Create team member profiles
4. **Setup email** - Configure SMTP for booking confirmations
5. **Deploy to server** - Follow DEPLOYMENT.md for production setup

---

## 📚 Documentation

- [Backend Setup](Backend/README.md)
- [Frontend Customization](Frontend/README.md)
- [API Documentation](Backend/PROJECT_MAP.txt)
- [Deployment Guide](Backend/DEPLOYMENT.md)
- [Troubleshooting](Backend/TROUBLESHOOTING.md)

---

**You're all set! Start both servers and visit http://localhost:8001 🎉**
