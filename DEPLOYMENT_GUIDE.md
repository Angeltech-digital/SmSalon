# 🚀 Complete Deployment Guide - Salon Management System

## 📊 Current Status

✅ **Development Setup Ready:**
- Frontend server running on port 8001
- Backend Django configured (4.2)
- Database migrations completed
- JWT authentication system active
- All features implemented
- Documentation complete

**Ready to deploy!**

---

## 🎯 Deployment Approaches

### Quick Choice Guide

**Are you deploying:**
- [ ] **For Testing/Staging?** → Go to **Option 1: Heroku** (Free tier available)
- [ ] **For Production (Small)** → Go to **Option 2: PythonAnywhere** (Simple, reliable)
- [ ] **For Production (Scale)** → Go to **Option 3: DigitalOcean** (More control)
- [ ] **For Production (Enterprise)** → Go to **Option 4: AWS** (Maximum scale)

---

## 🔧 Pre-Deployment Checklist

Before deploying, complete these steps:

### Step 1: Create .env File

Create `Backend/.env` with your production settings:

```
SECRET_KEY=your-very-secure-random-key-here-minimum-50-characters
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/salon_db
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```

**Generate a secure SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 2: Update requirements.txt

Add production dependencies. Your current file needs:

```bash
# Add these to Backend/requirements.txt:
gunicorn==21.2.0        # Production WSGI server
python-dotenv==1.0.0    # Load environment variables
psycopg2-binary==2.9.9  # PostgreSQL adapter
whitenoise==6.6.0       # Serve static files
```

### Step 3: Create Runtime Configuration Files

#### A. Create `Backend/Procfile` (for Heroku/Render)
```
release: python manage.py migrate
web: gunicorn salon_project.wsgi:application --log-file -
```

#### B. Create `Backend/runtime.txt` (for Heroku)
```
python-3.10.13
```

#### C. Create `Backend/wsgi.py` Production Version
Already exists but verify it's configured correctly.

---

## 🌍 OPTION 1: Heroku Deployment (EASIEST - FREE TIER)

**Time:** 15 minutes
**Cost:** Free (with limitations) or $7/month basic
**Best For:** Quick testing, prototyping

### Step 1: Install Heroku CLI

```bash
# On Ubuntu/Linux
curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

# Or use Snap
sudo snap install --classic heroku

# Verify
heroku --version
```

### Step 2: Login to Heroku

```bash
heroku login
# Opens browser for authentication
```

### Step 3: Prepare Your Project

```bash
cd /home/angela/Salon/Backend

# Create Procfile (if not exists)
echo "release: python manage.py migrate" > Procfile
echo "web: gunicorn salon_project.wsgi:application --log-file -" >> Procfile

# Create runtime.txt
echo "python-3.10.13" > runtime.txt
```

### Step 4: Update Requirements

```bash
pip install gunicorn whitenoise python-dotenv
pip freeze > requirements.txt
```

### Step 5: Initialize Git (if not already)

```bash
cd /home/angela/Salon
git init
git add .
git commit -m "Initial commit - Salon Management System with Auth"
```

### Step 6: Create Heroku App

```bash
heroku create your-salon-app-name
# Example: heroku create angela-salon-management
```

### Step 7: Set Environment Variables

```bash
heroku config:set SECRET_KEY="your-generated-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-salon-app-name.herokuapp.com
```

### Step 8: Add PostgreSQL (Optional but Recommended)

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

### Step 9: Deploy

```bash
git push heroku main
# Or if using master branch:
git push heroku master
```

### Step 10: View Logs

```bash
heroku logs --tail
# To exit: Ctrl+C
```

### Step 11: Access Your App

```bash
heroku open
# Or visit: https://your-salon-app-name.herokuapp.com
```

---

## 💻 OPTION 2: PythonAnywhere Deployment (RECOMMENDED FOR BEGINNERS)

**Time:** 20 minutes
**Cost:** Free tier or $5/month
**Best For:** Easy hosting, good for learning

### Step 1: Create Account

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for free account
3. Verify email

### Step 2: Upload Project

#### Option A: Upload ZIP
1. Go to Dashboard → Files
2. Upload your project as ZIP
3. Extract it

#### Option B: Clone from Git
```bash
# In PythonAnywhere console
git clone https://github.com/your-username/salon-management.git
cd salon-management
```

### Step 3: Create Virtual Environment

In PythonAnywhere Bash Console:
```bash
mkvirtualenv --python=/usr/bin/python3.10 salon_venv
pip install -r Backend/requirements.txt
```

### Step 4: Configure Web App

1. Go to Web → Add a new web app
2. Select "Manual configuration"
3. Choose Python 3.10
4. Configure the WSGI file:
   - Path: `/home/your-username/salon-management/Backend/salon_project/wsgi.py`

### Step 5: Set Environment Variables

In PythonAnywhere Web app settings:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-username.pythonanywhere.com
```

### Step 6: Configure Static Files

```bash
python Backend/manage.py collectstatic
```

Map:
- URL: `/static/`
- Directory: `/home/your-username/salon-management/Backend/staticfiles/`

### Step 7: Reload Web App

Click "Reload" button on PythonAnywhere Web tab.

### Step 8: Access Your App

Visit: `https://your-username.pythonanywhere.com`

---

## 🚀 OPTION 3: DigitalOcean Deployment (PRODUCTION-READY)

**Time:** 30-45 minutes
**Cost:** $6/month+ (more control, better performance)
**Best For:** Production, scaling, custom domain

### Step 1: Create DigitalOcean Account

1. Sign up at [digitalocean.com](https://www.digitalocean.com)
2. Add payment method
3. Create SSH key

### Step 2: Create a Droplet

1. Droplet → Create → Choose image → Ubuntu 22.04
2. Size: Basic ($6/month)
3. Add SSH key
4. Create

### Step 3: Connect to Droplet

```bash
ssh root@your-droplet-ip
```

### Step 4: Setup Server

```bash
# Update system
apt update && apt upgrade -y

# Install Python and tools
apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx

# Create app user
useradd -m -s /bin/bash salon_user
su - salon_user

# Clone your project
git clone https://github.com/your-username/salon-management.git
cd salon-management
```

### Step 5: Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r Backend/requirements.txt
pip install gunicorn
```

### Step 6: Setup PostgreSQL

```bash
sudo -u postgres createdb salon_db
sudo -u postgres createuser salon_user
sudo -u postgres psql
```

In PostgreSQL shell:
```sql
ALTER USER salon_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE salon_db TO salon_user;
\q
```

### Step 7: Create Systemd Service

Create `/etc/systemd/system/salon.service`:

```ini
[Unit]
Description=Salon Management System
After=network.target

[Service]
Type=notify
User=salon_user
WorkingDirectory=/home/salon_user/salon-management/Backend
Environment="PATH=/home/salon_user/salon-management/venv/bin"
ExecStart=/home/salon_user/salon-management/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/home/salon_user/salon-management/salon.sock \
    salon_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Step 8: Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl start salon
sudo systemctl enable salon
```

### Step 9: Configure Nginx

Create `/etc/nginx/sites-available/salon`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/salon_user/salon-management/Backend/staticfiles/;
    }

    location /media/ {
        alias /home/salon_user/salon-management/Backend/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/salon_user/salon-management/salon.sock;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/salon /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### Step 10: Setup SSL (Free with Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

---

## ⚙️ Post-Deployment Configuration

### 1. Database Migration

After deploying, run migrations on production:

```bash
# For Heroku:
heroku run python manage.py migrate

# For PythonAnywhere (Bash console):
cd ~/salon-management/Backend
python manage.py migrate

# For DigitalOcean:
ssh root@your-ip
sudo -u salon_user bash
cd ~/salon-management/Backend
python manage.py migrate
```

### 2. Create Superuser

```bash
python manage.py createsuperuser
# Enter username, email, password
```

### 3. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 4. Update Frontend API URL

Update these files with your production domain:
- `Frontend/login.html` - Change `API_BASE_URL`
- `Frontend/signup.html` - Change `API_BASE_URL`
- `Frontend/admin-dashboard.html` - Change `API_BASE_URL`

From:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

To:
```javascript
const API_BASE_URL = 'https://your-domain.com/api';
```

### 5. Test Admin Panel

1. Visit `https://your-domain.com/Frontend/login.html`
2. Create admin account
3. Test dashboard functionality

---

## 🔒 Security Hardening

### Before Going Live:

✅ **Update settings.py:**

```python
# Set DEBUG to False
DEBUG = False

# Update ALLOWED_HOSTS
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# Update CORS
CORS_ALLOWED_ORIGINS = [
    "https://your-domain.com",
    "https://www.your-domain.com",
]

# Add security headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
```

✅ **Update .env file with strong credentials**

✅ **Setup HTTPS** (mandatory for tokens)

✅ **Enable backups** on database

✅ **Monitor logs** regularly

---

## 📊 Testing After Deployment

### Test Checklist:

- [ ] Frontend loads
- [ ] Signup works
- [ ] Login works
- [ ] Dashboard displays
- [ ] Data loads from API
- [ ] Profile update works
- [ ] Logout works
- [ ] Admin link from home works
- [ ] Responsive design works
- [ ] HTTPS certificate valid

---

## 🆘 Troubleshooting

### Issue: 404 on /api/ endpoints
**Fix:** Ensure migrations ran: `python manage.py migrate`

### Issue: CORS errors
**Fix:** Update CORS_ALLOWED_ORIGINS in settings.py with your domain

### Issue: Static files not loading
**Fix:** Run `python manage.py collectstatic --noinput`

### Issue: Database connection failed
**Fix:** Check DATABASE_URL environment variable and database credentials

### Issue: Token authentication not working
**Fix:** Ensure simplejwt is installed and configured in settings.py

---

## 📈 Monitoring & Maintenance

### Regular Tasks:

1. **Check Logs** (weekly)
   - Heroku: `heroku logs --tail`
   - DigitalOcean: `journalctl -u salon -f`

2. **Backup Database** (daily)
   - Setup automated backups through platform

3. **Monitor Performance** (weekly)
   - Check response times
   - Monitor CPU/Memory usage

4. **Update Dependencies** (monthly)
   - Check for security updates
   - Test before deploying

5. **Review Errors** (daily)
   - Check error logs
   - Fix issues promptly

---

## 🎯 Quick Reference

### Heroku
```bash
heroku create your-app
heroku config:set SECRET_KEY="key"
git push heroku main
heroku run python manage.py migrate
heroku open
```

### PythonAnywhere
1. Upload project
2. Create web app
3. Configure WSGI
4. Set env variables
5. Reload

### DigitalOcean
```bash
# Server setup, then:
git clone project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
gunicorn salon_project.wsgi
```

---

## 📞 Support Resources

- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/
- Heroku Docs: https://devcenter.heroku.com/
- PythonAnywhere Docs: https://help.pythonanywhere.com/
- DigitalOcean Community: https://www.digitalocean.com/community/tutorials

---

**Ready to deploy? Choose your platform above and follow the steps!** 🚀
