# Environment Variables for DigitalOcean App Platform

## Copy these exact settings:

Go to: https://cloud.digitalocean.com/apps → plankton-app → Settings → Environment Variables

Add/Edit these variables:

---

### Required Variables:

| Variable | Value |
|----------|-------|
| **SECRET_KEY** | `django-insecure-[GENERATE_A_NEW_KEY]` |
| **DATABASE_URL** | `postgresql://dev-db-540694:YOUR_PASSWORD@app-da9a8f3c-40b2-484a-8b2c-df05aab32981-do-user-32520461-0.f.db.ondigitalocean.com:25060/dev-db-540694?sslmode=require` |
| **DEBUG** | `False` |
| **ALLOWED_HOSTS** | `plankton-app-q4rym.ondigitalocean.app` |
| **DISABLE_COLLECTSTATIC** | `1` |

---

### How to Get DATABASE_URL:

1. Go to https://cloud.digitalocean.com/databases
2. Click on your PostgreSQL database
3. Look for "Connection Details" or "Connection String"
4. Copy the full string starting with `postgresql://`

---

### Generate a Strong SECRET_KEY:

Run this in terminal:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Or use: https://djecrety.ir/

---

## Steps to Complete:

1. ✅ **Go to** DigitalOcean App Platform → Your App → Settings
2. ✅ **Add** all the required variables above
3. ✅ **Save** the changes (app will auto-redeploy)
4. ✅ **Wait** for deployment to complete (check "Activity" tab)
5. ✅ **Test** health endpoint: `https://plankton-app-q4rym.ondigitalocean.app/api/health/`

---

## Testing After Setup:

1. **Health Check:**
   ```
   https://plankton-app-q4rym.ondigitalocean.app/api/health/
   ```

2. **Services:**
   ```
   https://plankton-app-q4rym.ondigitalocean.app/api/services/
   ```

---

## Create Admin User:

Go to App Console and run:
```bash
cd Backend
python manage.py shell
```

Then paste:
```python
from django.contrib.auth.models import User
User.objects.create_superuser('admin', 'admin@smsalon.com', 'ChangeMe123!')
print("Admin created!")
exit()
```

---

## Add Initial Data:

```bash
python setup_data.py --all --password=ChangeMe123!
```

