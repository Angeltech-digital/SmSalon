# 🔧 500 Internal Server Error Fix Plan

## Problem Analysis

The following endpoints are returning 500 Internal Server Error:
- `GET https://smsalon-ehqso.ondigitalocean.app/api/services/`
- `POST https://smsalon-ehqso.ondigitalocean.app/api/auth/login/`
- `GET https://smsalon-ehqso.ondigitalocean.app/api/bookings/`
- `POST https://smsalon-ehqso.ondigitalocean.app/api/contacts/`

**Root Cause:** Database tables and initial data are not set up on the production server.

---

## Fix Plan

### Step 1: Connect to DigitalOcean Server

Run this command to connect to your server:

```bash
ssh angela@smsalon-ehqso.ondigitalocean.app
```

Enter your password when prompted.

---

### Step 2: Navigate to Project Directory

```bash
cd /home/angela/smsalon
```

---

### Step 3: Pull Latest Code

```bash
git pull origin main
```

---

### Step 4: Activate Virtual Environment

```bash
cd Backend
source venv/bin/activate
```

---

### Step 5: Run Database Migrations

This will create all necessary database tables:

```bash
python manage.py migrate --run-syncdb
```

---

### Step 6: Create Initial Data

Run the setup script to create services, stylists, and settings:

```bash
# Create services
python setup_data.py --create-services

# Create stylists
python setup_data.py --create-stylists

# Create salon settings
python setup_data.py --create-settings
```

---

### Step 7: Create Admin User

```bash
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@smsalon.com', 'Admin@123')" | python manage.py shell
```

---

### Step 8: Restart the Application

If using systemd/gunicorn:

```bash
sudo systemctl restart gunicorn
```

Or if using Dokku:

```bash
git push dokku main
```

---

### Step 9: Verify the Fix

Test the endpoints in your browser:

1. **Health Check:** `https://smsalon-ehqso.ondigitalocean.app/api/health/`
   - Should return: `{"status": "ok", "message": "Salon API is running"}`

2. **Services List:** `https://smsalon-ehqso.ondigitalocean.app/api/services/`
   - Should return JSON array of services

3. **Signup:** `https://smsalon-ehqso.ondigitalocean.app/signup.html`
   - Should allow creating a new account

4. **Login:** `https://smsalon-ehqso.ondigitalocean.app/login.html`
   - Should log in with username: `admin`, password: `Admin@123`

---

## Alternative: Run Automated Fix Script

If you've already connected to the server, you can run this single command:

```bash
cd /home/angela/smsalon && ./fix_database.sh
```

This script will:
1. Run database migrations
2. Create initial services
3. Create stylists
4. Create salon settings
5. Create admin user
6. Test the endpoints

---

## Expected Results After Fix

✅ **Health endpoint returns:** `{"status": "ok", "message": "Salon API is running"}`  
✅ **Services endpoint returns:** List of salon services  
✅ **Login endpoint works:** Returns JWT tokens  
✅ **Signup endpoint works:** Creates new users  
✅ **Booking endpoint works:** Creates and lists bookings  
✅ **Contact endpoint works:** Sends messages  

---

## If Issues Persist

### Check Database Status

```bash
cd /home/angela/smsalon/Backend
source venv/bin/activate
python manage.py shell
```

Then in Python shell:
```python
from django.contrib.auth.models import User
print(f"Users: {User.objects.count()}")

from salon_app.models import Service
print(f"Services: {Service.objects.count()}")

from salon_app.models import Stylist
print(f"Stylists: {Stylist.objects.count()}")
```

### Check Server Logs

```bash
# If using systemd
sudo journalctl -u gunicorn -f

# If using Dokku
dokku logs smsalon
```

### Test Database Connection

```bash
cd /home/angela/smsalon/Backend
source venv/bin/activate
python manage.py dbshell
```

Then run: `.tables` to list all tables.

---

## Frontend Testing

After fixing the backend, test these frontend pages:

1. **Home Page:** https://smsalon-ehqso.ondigitalocean.app/
2. **Services Page:** https://smsalon-ehqso.ondigitalocean.app/services.html
3. **Booking Page:** https://smsalon-ehqso.ondigitalocean.app/booking.html
4. **Signup:** https://smsalon-ehqso.ondigitalocean.app/signup.html
5. **Login:** https://smsalon-ehqso.ondigitalocean.app/login.html
6. **Admin Dashboard:** https://smsalon-ehqso.ondigitalocean.app/admin-dashboard.html

---

## Status: Pending User Action

This plan requires the user to:
1. Connect to the server via SSH
2. Run the database fix commands

Once the user runs these commands, the 500 errors should be resolved.

