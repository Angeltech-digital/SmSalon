# ✅ Deployment Checklist

## Pre-Deployment (Do Before Deploying)

### Backend Setup
- [ ] Generate strong SECRET_KEY
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- [ ] Create `.env` file in `Backend/` with all variables
- [ ] Test locally with `DEBUG=False` to catch errors
- [ ] Run migrations locally: `python manage.py migrate`
- [ ] Collect static files: `python manage.py collectstatic --noinput`
- [ ] Create superuser: `python manage.py createsuperuser`

### Frontend Setup
- [ ] Update API_BASE_URL in `login.html` to production domain
- [ ] Update API_BASE_URL in `signup.html` to production domain
- [ ] Update API_BASE_URL in `admin-dashboard.html` to production domain
- [ ] Test links are correct
- [ ] Verify responsive design on mobile

### Security
- [ ] Set `DEBUG = False` in settings.py
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Update `CORS_ALLOWED_ORIGINS` with your domain
- [ ] Enable HTTPS (required for JWT tokens)
- [ ] Update `SECURE_SSL_REDIRECT = True`
- [ ] Set secure cookie flags
- [ ] Change all default credentials

### Dependencies
- [ ] All required packages in `requirements.txt`
- [ ] Run `pip install -r requirements.txt` successfully
- [ ] No deprecated packages
- [ ] All imports working

### Database
- [ ] Database selected (PostgreSQL recommended for production)
- [ ] Database connection tested locally
- [ ] Backups configured
- [ ] Database user/password created

### Files
- [ ] `.env` file created and filled
- [ ] `.env.example` created for documentation
- [ ] Procfile created (for Heroku/Render)
- [ ] Runtime.txt created (for Heroku/Render)
- [ ] wsgi.py configured
- [ ] All required config files present

---

## Deployment (Choose Your Platform)

### Option A: Heroku (Easiest - Recommended for First Time)

- [ ] Heroku account created and verified
- [ ] Heroku CLI installed: `heroku --version`
- [ ] Git repository initialized
- [ ] All changes committed: `git commit -m "Ready for deployment"`
- [ ] Heroku app created: `heroku create app-name`
- [ ] Environment variables set: `heroku config:set ...`
- [ ] PostgreSQL addon added (optional but recommended)
- [ ] Deployed: `git push heroku main`
- [ ] Migrations ran: `heroku run python manage.py migrate`
- [ ] App opened: `heroku open`
- [ ] Admin panel tested: `/admin/`

### Option B: PythonAnywhere

- [ ] PythonAnywhere account created
- [ ] Project uploaded or cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Web app created and configured
- [ ] WSGI file configured
- [ ] Static files collected
- [ ] Environment variables set
- [ ] App reloaded
- [ ] Domain configured
- [ ] SSL certificate enabled

### Option C: DigitalOcean

- [ ] DigitalOcean account created
- [ ] Droplet created (Ubuntu 22.04)
- [ ] SSH key configured
- [ ] Connected to droplet
- [ ] System updated and dependencies installed
- [ ] Project cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] PostgreSQL configured
- [ ] Gunicorn configured
- [ ] Systemd service created
- [ ] Nginx configured as reverse proxy
- [ ] SSL certificate installed (Let's Encrypt)
- [ ] Domain pointing to server
- [ ] Service started and enabled

---

## Post-Deployment (Do After Deploying)

### Verify Everything Works
- [ ] Frontend loads at your domain
- [ ] Signup page works
- [ ] Signup form submits successfully
- [ ] Login page works
- [ ] Login with new account works
- [ ] Dashboard loads after login
- [ ] Dashboard data displays
- [ ] Profile section loads
- [ ] Profile update works
- [ ] Logout works
- [ ] Can login again after logout
- [ ] Admin link from home page works
- [ ] HTTPS certificate valid (no warnings)
- [ ] Responsive design works on mobile

### Test API Endpoints
- [ ] `/api/auth/login/` works
- [ ] `/api/auth/signup/` works
- [ ] `/api/auth/profile/` works (with token)
- [ ] `/api/bookings/` works
- [ ] `/api/stylists/` works
- [ ] `/api/services/` works
- [ ] All other endpoints respond

### Security Verification
- [ ] No debug information exposed
- [ ] Error messages don't reveal structure
- [ ] CORS properly restricted
- [ ] HTTPS enforced
- [ ] Admin panel requires login
- [ ] CSRF protection working

### Database & Backups
- [ ] Database connection verified
- [ ] Migrations completed successfully
- [ ] Superuser account created
- [ ] Backup configured
- [ ] Can access Django admin
- [ ] Can add test data

### Monitoring
- [ ] Error logging configured
- [ ] Logs accessible
- [ ] Set up alerts for errors
- [ ] Set up performance monitoring

---

## Common Issues & Solutions

### Issue: CORS Error
**Solution:** 
```python
# In settings.py
CORS_ALLOWED_ORIGINS = [
    "https://your-domain.com",
    "https://www.your-domain.com",
]
```

### Issue: Static Files Not Loading
**Solution:**
```bash
python manage.py collectstatic --noinput
```

### Issue: Database Connection Failed
**Solution:**
- Check DATABASE_URL environment variable
- Verify database credentials
- Ensure database is running

### Issue: Migrations Not Running
**Solution:**
```bash
# For Heroku:
heroku run python manage.py migrate

# For others:
python manage.py migrate
```

### Issue: Admin Panel Shows 404
**Solution:**
- Ensure migrations completed
- Check DEBUG setting
- Verify URL configuration

### Issue: JWT Token Not Working
**Solution:**
- Verify simplejwt installed
- Check JWT configuration in settings.py
- Ensure token in Authorization header

---

## Maintenance Tasks

### Daily
- [ ] Check error logs
- [ ] Monitor app availability

### Weekly
- [ ] Review performance metrics
- [ ] Check for security alerts
- [ ] Verify backups running

### Monthly
- [ ] Update dependencies (security patches)
- [ ] Review access logs
- [ ] Update SSL certificates if needed

### Quarterly
- [ ] Full security audit
- [ ] Load testing
- [ ] Database optimization
- [ ] Performance review

---

## Rollback Plan (If Something Goes Wrong)

### Quick Fixes
1. Check logs: `heroku logs --tail`
2. Restart app: `heroku restart`
3. Check environment variables: `heroku config`
4. Redeploy previous version: `git revert HEAD~1 && git push heroku main`

### Database Issues
1. Check database connection
2. Verify migrations ran: `heroku run python manage.py migrate`
3. Reset if necessary (after backup): `heroku pg:reset DATABASE_URL`

### Rollback to Previous Version
```bash
git log --oneline
git revert <commit-id>
git push heroku main
```

---

## Success Indicators ✅

- [ ] App loads without errors
- [ ] All pages render correctly
- [ ] Authentication works
- [ ] API endpoints respond
- [ ] Database queries execute
- [ ] Static files load
- [ ] No console errors
- [ ] HTTPS certificate valid
- [ ] Mobile responsive
- [ ] Admin panel functional

---

## Support & Documentation

- **Heroku:** https://devcenter.heroku.com/
- **PythonAnywhere:** https://www.pythonanywhere.com/help/
- **DigitalOcean:** https://docs.digitalocean.com/
- **Django Docs:** https://docs.djangoproject.com/
- **Your Project Docs:** See DEPLOYMENT_GUIDE.md

---

**Status:** Ready to Deploy ✅
**Last Updated:** January 22, 2026
