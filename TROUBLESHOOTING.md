# Salon MVP - Troubleshooting Guide

## Common Issues & Solutions

### 🔴 Backend Issues

#### Issue 1: "ModuleNotFoundError: No module named 'django'"
**Problem:** Django not installed
**Solution:**
```bash
cd Backend
source venv/bin/activate
pip install -r requirements.txt
```

#### Issue 2: "No such table: salon_app_booking"
**Problem:** Database migrations not run
**Solution:**
```bash
python manage.py migrate
python manage.py makemigrations salon_app
python manage.py migrate salon_app
```

#### Issue 3: "django.db.utils.OperationalError: no such table"
**Problem:** Database doesn't exist or not migrated
**Solution:**
```bash
# For SQLite
rm db.sqlite3  # Delete old database
python manage.py migrate  # Create new one

# For MySQL
# Drop and recreate database in MySQL, then run migrate
```

#### Issue 4: "Email backend not working"
**Problem:** Email configuration incorrect
**Solution:**
1. Check `.env` file:
   ```
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```
2. For Gmail: Use App Password, not regular password
3. Enable "Less Secure Apps" (if not using 2FA)

#### Issue 5: "CORS error: blocked by CORS policy"
**Problem:** Frontend & Backend on different origins
**Solution:**
In `Backend/salon_project/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8001",  # Frontend URL
    "http://localhost:3000",  # If using Node dev server
]
```

#### Issue 6: "Port already in use"
**Problem:** Another process using port 8000
**Solution:**
```bash
# Find and kill process
lsof -i :8000
kill -9 <PID>

# Or use different port
python manage.py runserver 8080
```

#### Issue 7: "Secret key not found"
**Problem:** `.env` not configured
**Solution:**
```bash
cp .env.example .env
# Edit .env with your settings
```

---

### 🔴 Frontend Issues

#### Issue 1: "API call fails / 404 errors"
**Problem:** Backend not running or wrong API URL
**Solution:**
1. Check if backend is running: `http://localhost:8000/api/health/`
2. Verify API_BASE_URL in `script.js`:
   ```javascript
   const API_CONFIG = {
       BASE_URL: 'http://localhost:8000/api'
   };
   ```

#### Issue 2: "Booking form won't submit"
**Problem:** JavaScript errors or validation failing
**Solution:**
1. Open DevTools (F12)
2. Check Console for errors
3. Check all required fields are filled
4. Verify date is in future

#### Issue 3: "Page styles look broken"
**Problem:** CSS file not loading
**Solution:**
1. Check file path in HTML:
   ```html
   <link rel="stylesheet" href="styles.css">
   ```
2. Make sure file exists: `Frontend/styles.css`
3. Hard refresh: Ctrl+Shift+R
4. Clear cache

#### Issue 4: "WhatsApp link not opening"
**Problem:** Invalid WhatsApp number format
**Solution:**
In `script.js`, update:
```javascript
const SALON_INFO = {
    whatsapp: '254712345678'  // Without + or spaces
};
```

#### Issue 5: "Mobile menu not opening"
**Problem:** JavaScript not loading
**Solution:**
1. Check `script.js` is linked in HTML
2. Open DevTools console
3. Try hard refresh

#### Issue 6: "Forms submitting twice"
**Problem:** Multiple event listeners
**Solution:**
1. Check for duplicate script.js includes
2. Clear browser cache
3. Check for JavaScript errors in console

#### Issue 7: "Google Map not showing"
**Problem:** Map embed URL not working
**Solution:**
Update in `contact.html`:
```html
<iframe src="https://www.google.com/maps/embed?pb=YOUR_EMBED_CODE"
        width="100%" height="400" ...></iframe>
```

---

### 🔴 Deployment Issues

#### Issue 1: "502 Bad Gateway"
**Problem:** Gunicorn/Backend crashed
**Solution:**
```bash
# Check logs
sudo journalctl -u salon-gunicorn -f

# Restart
sudo systemctl restart salon-gunicorn
```

#### Issue 2: "Static files not loading (404)"
**Problem:** CSS/JS not found in production
**Solution:**
```bash
python manage.py collectstatic --noinput
# Check Nginx config points to correct path
```

#### Issue 3: "SSL certificate error"
**Problem:** HTTPS not configured
**Solution:**
```bash
sudo certbot --nginx -d yourdomain.com
# Auto-renewal enabled
```

#### Issue 4: "Database connection timeout"
**Problem:** MySQL server not running
**Solution:**
```bash
# Check MySQL status
sudo systemctl status mysql

# Start if stopped
sudo systemctl start mysql

# Check credentials in .env
```

---

### 🟡 Performance Issues

#### Issue: "Page loading slowly"
**Solutions:**
1. Minify CSS & JavaScript
2. Optimize images
3. Enable caching in Nginx
4. Use CDN for static files
5. Check database queries

#### Issue: "High server CPU usage"
**Solutions:**
1. Increase Gunicorn workers:
   ```bash
   --workers 8  # For 4 CPU cores
   ```
2. Monitor with: `top` or `htop`
3. Check Django logs for errors

---

### 🟡 Data Issues

#### Issue: "Booking not saved"
**Check:**
1. Database has data: `python manage.py shell`
   ```python
   from salon_app.models import Booking
   print(Booking.objects.count())
   ```
2. No database errors in logs
3. Form validation passed

#### Issue: "Email not sent"
**Check:**
1. Email configuration in `.env`
2. App password (for Gmail)
3. SMTP port not blocked
4. Check logs: `tail -f logs/salon.log`

#### Issue: "Admin panel not loading"
**Solution:**
```bash
python manage.py migrate
python manage.py createsuperuser
# If new user, logout and login again
```

---

### 🟢 Verification Checklist

**Backend Working:**
- [ ] `http://localhost:8000/api/health/` returns `{"status": "ok"}`
- [ ] Admin panel accessible: `http://localhost:8000/admin/`
- [ ] Can create booking via API
- [ ] Services load in API

**Frontend Working:**
- [ ] Pages load without 404 errors
- [ ] Forms have proper styling
- [ ] Responsive on mobile
- [ ] Booking form submits

**Email Working:**
- [ ] Check `.env` has EMAIL settings
- [ ] Test with: `python manage.py shell`
  ```python
  from django.core.mail import send_mail
  send_mail('Test', 'Test message', 'from@gmail.com', ['to@gmail.com'])
  ```
- [ ] Check spam folder

**Database Working:**
- [ ] Tables created: `python manage.py showmigrations`
- [ ] Can add data via admin
- [ ] Data persists after restart

---

## Debug Mode

### Enable Debug Output
In `Frontend/script.js`:
```javascript
const API_CONFIG = {
    DEBUG: true  // Set to true for logging
};
```

### Django Debug
In `Backend/.env`:
```
DEBUG=True
```

Then check logs:
```bash
tail -f Backend/logs/salon.log
```

### Browser Console
Press F12 → Console tab:
- See JavaScript errors
- Log API requests
- Test code snippets

---

## Log Locations

**Django Logs:**
- `Backend/logs/salon.log`
- System: `journalctl -u salon-gunicorn`

**Nginx Logs:**
- Error: `/var/log/nginx/error.log`
- Access: `/var/log/nginx/access.log`

**Database Logs:**
- MySQL: `/var/log/mysql/error.log`

---

## Testing Commands

```bash
# Test backend API
curl http://localhost:8000/api/health/

# Test frontend loads
curl http://localhost:8001

# Test database
python manage.py dbshell

# Test email
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Body', 'from@example.com', ['to@example.com'])

# Test specific model
python manage.py test salon_app.tests.BookingTest
```

---

## Getting Help

1. **Check console errors** (F12)
2. **Review logs** (see above)
3. **Google the error message** - usually already solved!
4. **Check Django docs** - https://docs.djangoproject.com
5. **Stack Overflow** - search error message

## Common Search Terms

- "Django migration error"
- "CORS error Django REST"
- "Gunicorn not running"
- "Nginx 502 bad gateway"
- "Python email SMTP error"

---

**Remember:** Most issues have simple solutions. Start with the error message, check the logs, and search online!

Last Updated: January 2026
