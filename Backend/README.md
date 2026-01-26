# Salon MVP - Backend Setup Guide

## Quick Start

### 1. Create Virtual Environment
```bash
cd Backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your settings (email, database, etc.)
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
# Follow the prompts to create admin account
```

### 6. Create Initial Data (Services, Stylists)
```bash
python manage.py shell
```

Then in the Python shell:
```python
from salon_app.models import Service, Stylist, SalonSettings

# Create services
Service.objects.create(
    name="Hair Cut",
    category="hair",
    description="Professional haircut",
    price=500,
    duration_minutes=45
)

# Create salon settings
SalonSettings.objects.create(
    salon_name="Salon",
    phone="+254712345678",
    email="info@salon.com",
    address="123 Beauty Lane, Nairobi",
    salon_description="Professional beauty salon"
)

exit()
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Server will run at: `http://localhost:8000`

## API Endpoints

### Base URL: `http://localhost:8000/api/`

**Services:**
- `GET /services/` - List all services
- `GET /services/{id}/` - Service details

**Stylists:**
- `GET /stylists/` - List stylists
- `GET /stylists/{id}/` - Stylist details
- `GET /stylists/{id}/available-slots/?date=2026-01-20` - Available slots

**Bookings:**
- `POST /bookings/` - Create booking
- `GET /bookings/` - List bookings
- `GET /bookings/{id}/` - Booking details
- `POST /bookings/{id}/confirm/` - Confirm booking
- `POST /bookings/{id}/cancel/` - Cancel booking

**Contacts:**
- `POST /contacts/` - Send contact message

**Reviews:**
- `GET /reviews/` - Get approved reviews
- `POST /reviews/` - Submit review

**Settings:**
- `GET /settings/current/` - Get salon settings

**Health:**
- `GET /health/` - Health check

## Admin Panel
Access at: `http://localhost:8000/admin/`
Use the superuser credentials created earlier.

## Email Setup (Gmail)

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Add to .env:
   ```
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-generated-app-password
   ```

## Using MySQL Instead of SQLite

1. Install MySQL: `pip install mysqlclient`
2. Update .env:
   ```
   DB_ENGINE=django.db.backends.mysql
   DB_NAME=salon_db
   DB_USER=root
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=3306
   ```
3. Create database: `CREATE DATABASE salon_db;`
4. Run migrations: `python manage.py migrate`

## Deployment (DigitalOcean / Production)

See `DEPLOYMENT.md` for detailed production setup.

## Troubleshooting

**Import Error on models:**
```bash
python manage.py makemigrations salon_app
python manage.py migrate
```

**Admin panel not loading:**
```bash
python manage.py collectstatic
```

**Email not sending:**
- Check .env EMAIL settings
- Enable "Less secure app access" (if using personal Gmail)
- Use App Password (recommended)

**CORS errors:**
- Update CORS_ALLOWED_ORIGINS in settings.py or .env

## Next Steps

1. Connect Frontend to Backend (update API URL in script.js)
2. Set up payment gateway (M-Pesa)
3. Deploy to DigitalOcean
4. Set up domain and SSL certificate
