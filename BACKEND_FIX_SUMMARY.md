# 🔧 Fix Backend Connection Issues - Complete Guide

## 📋 Summary of Changes Made

I've updated your project to fix the backend connection issues. Here's what was done:

### ✅ Files Updated:

1. **Backend/Procfile** - Added release command to run migrations on deploy
2. **Backend/settings.py** - Improved DATABASE_URL parsing for PostgreSQL SSL
3. **Backend/setup_data.py** - New script to create initial data
4. **Backend/.env.example** - Template for environment variables
5. **DEPLOYMENT_CHECKLIST.md** - Step-by-step deployment guide

---

## 🚨 Current Issues (Based on Your Errors)

```
❌ GET https://plankton-app-q4rym.ondigitalocean.app/api/health/ 404 (Not Found)
❌ POST https://plankton-app-q4rym.ondigitalocean.app/api/contacts/ 400 (Bad Request)
```

**Root Causes:**
1. Database not connected (migrations not run)
2. Missing environment variables
3. Backend not responding to API calls

---

## 🔴 IMMEDIATE ACTION REQUIRED

### Step 1: Get Your DATABASE_URL from DigitalOcean

1. **Go to:** https://cloud.digitalocean.com/databases
2. **Click** on your PostgreSQL database (the one with ID `31e91af2...`)
3. **Look for** "Connection Details" or "Connection String"
4. **Copy** the full connection string (starts with `postgresql://`)

### Step 2: Set Environment Variables

1. **Go to:** https://cloud.digitalocean.com/apps
2. **Click** on `plankton-app`
3. **Click** on **Settings** tab
4. **Scroll** to "Environment Variables"
5. **Add/Edit** these variables:

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | `django-insecure-$(openssl rand -base64 32)` or generate at https://djecrety.ir/ |
| `DATABASE_URL` | `postgresql://doadmin:YOUR_PASSWORD@db-xxxxx-do-user-xxxxx-0.db.ondigitalocean.com:25060/defaultdb?sslmode=require` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `plankton-app-q4rym.ondigitalocean.app` |
| `DISABLE_COLLECTSTATIC` | `1` |

### Step 3: Trigger Redeploy

After setting environment variables, DigitalOcean should automatically redeploy. If not:
1. Go to your app
2. Click "Actions" → "Redeploy"

---

## 🧪 Testing After Deployment

### Test Backend Health:
```
https://plankton-app-q4rym.ondigitalocean.app/api/health/
```

**Expected Response:**
```json
{"status": "ok", "message": "Salon API is running"}
```

### Test Contact Form:
```bash
curl -X POST https://plankton-app-q4rym.ondigitalocean.app/api/contacts/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "email": "test@example.com", "subject": "Test", "message": "Hello"}'
```

---

## 👤 Creating Admin User

Once deployed, create an admin user via the Console:

1. Go to https://cloud.digitalocean.com/apps → Your App → **Console**
2. Run these commands:

```bash
cd Backend
python manage.py shell
```

Then paste this:

```python
from django.contrib.auth.models import User
User.objects.create_superuser('admin', 'admin@smsalon.com', 'AdminPass123')
print("Admin user created!")
exit()
```

---

## 📋 Adding Initial Data

In the Console, run:

```bash
cd Backend
python setup_data.py --all --password=AdminPass123
```

This will create:
- ✅ Admin user
- ✅ Sample services (16 services)
- ✅ Sample stylists (4 stylists)
- ✅ Salon settings

---

## 🔍 Troubleshooting

### Still Getting 404 on /api/health/?

**Check:**
1. Is the backend component running? (DigitalOcean App → Components)
2. Did migrations run? Check deployment logs
3. Is ALLOWED_HOSTS set correctly?

### Getting 400 on Contact Form?

**Check:**
1. Is the Content-Type header `application/json`?
2. Are all required fields provided (name, email, subject, message)?

### Database Connection Failed?

**Check:**
1. Is DATABASE_URL set in environment variables?
2. Is the connection string correct?
3. Does the database have the correct SSL settings?

---

## 📁 Project Structure

```
SmSalon/
├── Backend/
│   ├── salon_project/
│   │   ├── settings.py ✅ Updated
│   │   └── urls.py
│   ├── salon_app/
│   │   ├── models.py
│   │   ├── views.py
│   │   └── ...
│   ├── Procfile ✅ Updated
│   ├── requirements.txt
│   ├── runtime.txt
│   └── setup_data.py ✅ Created
├── Frontend/
│   ├── index.html
│   ├── booking.html
│   ├── contact.html
│   ├── script.js
│   └── ...
├── DEPLOYMENT_CHECKLIST.md ✅ Created
└── DEPLOYMENT_GUIDE.md
```

---

## 📞 Next Steps

1. **Get DATABASE_URL** from DigitalOcean
2. **Set Environment Variables** in App Platform
3. **Redeploy** the app
4. **Test** the health endpoint
5. **Create** admin user via Console
6. **Add** initial data
7. **Test** the frontend

---

**Generated:** January 28, 2026
**Status:** Awaiting environment variable configuration

