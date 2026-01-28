# 🚀 DigitalOcean App Platform Deployment Checklist

## Status: 🔧 In Progress

---

## ✅ Step 1: Database Setup (COMPLETE)

- [x] PostgreSQL database created (ID: `31e91af2-f792-492f-8ecc-33f30da4eae7`)
- [ ] Get connection string from DigitalOcean dashboard

**How to get DATABASE_URL:**
1. Go to https://cloud.digitalocean.com/databases
2. Click on your database
3. Look for "Connection Details" or "Connection String"
4. Copy the full URI (starts with `postgresql://`)

---

## ✅ Step 2: Backend Configuration (COMPLETE)

- [x] Procfile updated with release command
- [x] settings.py configured for DATABASE_URL
- [x] requirements.txt has all dependencies

---

## 🔴 Step 3: Environment Variables (REQUIRED)

**Go to:** https://cloud.digitalocean.com/apps → Your App → Settings → Environment Variables

Add these variables:

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | Generate at https://djecrety.ir/ |
| `DATABASE_URL` | From your PostgreSQL database (see Step 1) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `plankton-app-q4rym.ondigitalocean.app` |
| `DISABLE_COLLECTSTATIC` | `1` |

**Example SECRET_KEY:**
```
django-insecure-abc123xyz456def789ghi012jkl345mno678pqr901stu234
```

**Example DATABASE_URL:**
```
postgresql://doadmin:AVNS_xxxxx@db-postgresql-fra1-xxxxx-do-user-xxxxx-0.db.ondigitalocean.com:25060/defaultdb?sslmode=require
```

---

## ✅ Step 4: Code Updates (COMPLETE)

- [x] Backend/Procfile - Added release command for migrations
- [x] Backend/settings.py - Database configuration ready
- [x] Backend/requirements.txt - All dependencies included

---

## 🔴 Step 5: Deploy

1. **Commit and push changes:**
```bash
git add -A
git commit -m "Fix deployment configuration"
git push origin main
```

2. **Monitor deployment:**
   - Go to https://cloud.digitalocean.com/apps
   - Click on `plankton-app`
   - Watch the "Activity" tab for deployment progress

3. **Check deployment logs:**
   - Look for any errors in the build/deploy logs
   - Verify migrations ran successfully

---

## 🔴 Step 6: Verify Backend

After deployment, test these endpoints:

1. **Health Check:**
   ```
   https://plankton-app-q4rym.ondigitalocean.app/api/health/
   ```
   Expected response: `{"status": "ok", "message": "Salon API is running"}`

2. **Services List:**
   ```
   https://plankton-app-q4rym.ondigitalocean.app/api/services/
   ```

3. **Contact Endpoint (POST):**
   ```
   https://plankton-app-q4rym.ondigitalocean.app/api/contacts/
   ```

---

## 🔴 Step 7: Create Admin User

You need to create a superuser to access the admin panel:

**Option 1: Via DigitalOcean Console**
1. Go to your App → Console
2. Run:
```bash
cd Backend
python manage.py createsuperuser
```

**Option 2: Use Django shell**
```bash
cd Backend
python manage.py shell
```

Then in Python:
```python
from django.contrib.auth.models import User
User.objects.create_superuser('admin', 'admin@salon.com', 'YourPassword123')
exit()
```

---

## 🔴 Step 8: Add Initial Data

Add services and settings:

**Via Console:**
```bash
cd Backend
python manage.py shell
```

```python
from salon_app.models import Service, SalonSettings

# Create Services
services = [
    {'name': 'Haircut & Style', 'category': 'hair', 'description': 'Professional haircut and styling', 'price': 1500, 'duration_minutes': 60},
    {'name': 'Hair Coloring', 'category': 'hair', 'description': 'Full hair coloring treatment', 'price': 3500, 'duration_minutes': 120},
    {'name': 'Manicure', 'category': 'nails', 'description': 'Nail care and polish', 'price': 800, 'duration_minutes': 45},
    {'name': 'Pedicure', 'category': 'nails', 'description': 'Foot nail care and polish', 'price': 1000, 'duration_minutes': 60},
    {'name': 'Makeup Application', 'category': 'makeup', 'description': 'Professional makeup for any occasion', 'price': 2500, 'duration_minutes': 90},
    {'name': 'Braiding', 'category': 'braiding', 'description': 'Various braid styles', 'price': 3000, 'duration_minutes': 180},
]

for s in services:
    Service.objects.get_or_create(name=s['name'], defaults=s)

# Create Settings
SalonSettings.objects.get_or_create(
    pk=1,
    defaults={
        'salon_name': 'SmSalon',
        'salon_description': 'Your premier beauty destination',
        'phone': '+254712345678',
        'email': 'info@smsalon.com',
        'address': 'Nairobi, Kenya'
    }
)

print("Initial data created!")
exit()
```

---

## 🔴 Step 9: Test Frontend

1. Visit: `https://plankton-app-q4rym.ondigitalocean.app/`
2. Test booking form
3. Test contact form
4. Open browser console (F12) to verify no errors

---

## ✅ Step 10: Project Files Updated

| File | Status | Description |
|------|--------|-------------|
| `Backend/Procfile` | ✅ Updated | Added release command for migrations |
| `Backend/requirements.txt` | ✅ Ready | All dependencies included |
| `Backend/settings.py` | ✅ Ready | Database URL support enabled |
| `DEPLOYMENT_CHECKLIST.md` | ✅ Created | This file |

---

## 🚨 Troubleshooting

### Error: "504 Gateway Timeout"
- Backend is not responding
- Check if migrations ran (Step 3)
- Verify DATABASE_URL is set correctly

### Error: "404 Not Found" on /api/health/
- Backend app might not be running
- Check deployment logs for errors
- Verify ALLOWED_HOSTS includes your domain

### Error: "400 Bad Request" on forms
- CSRF issue - check browser console
- May be CORS configuration needed

### Error: "Database connection failed"
- DATABASE_URL not set or incorrect
- Check SSL requirements for PostgreSQL

---

## 📞 Next Steps

1. ⬆️ Push the updated code to GitHub
2. 🌐 Go to DigitalOcean Dashboard
3. ⚙️ Add environment variables (Step 3 above)
4. 🔄 Trigger a redeploy
5. ✅ Verify backend endpoints
6. 👤 Create admin user (Step 7)
7. 📋 Add initial data (Step 8)
8. 🧪 Test everything works

---

**Generated:** January 28, 2026
**Status:** Waiting for environment variables

