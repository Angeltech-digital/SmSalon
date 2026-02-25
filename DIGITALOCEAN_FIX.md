DIGITALOCEAN DEPLOYMENT FIX GUIDE
==================================

Your booking form code is working locally, but the backend on DigitalOcean is returning 500 errors. 
This is because migrations haven't been run after the code was deployed.

SOLUTION DEPENDS ON YOUR DEPLOYMENT TYPE:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPTION 1: DigitalOcean App Platform (Recommended - Easiest)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Go to: https://cloud.digitalocean.com/apps
2. Find your app "smsalon" 
3. Go to Settings → Environment tab
4. Make sure these environment variables are set:
   - DATABASE_URL: (your PostgreSQL database URL)
   - SECRET_KEY: (random string)
   - DEBUG: False

5. Go to Deploy tab and manually trigger a redeploy:
   Click "Deploy" or "Create Deployment"
   
6. Wait for deployment to complete (watch the logs)
   
7. If still seeing 500 errors, check the Logs tab:
   - Click "Logs" 
   - Look for Python error messages
   
8. Test the fix:
   https://smsalon-ehqso.ondigitalocean.app/api/services/
   Should return a list of services (not an error)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPTION 2: Deployed on a Droplet with SSH access
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. SSH into your server:
   ssh root@YOUR_DROPLET_IP

2. Navigate to your app:
   cd /app
   # or wherever your code is deployed

3. Pull the latest code:
   git pull origin main

4. Run migrations:
   python manage.py migrate

5. Collect static files:
   python manage.py collectstatic --noinput

6. Restart the app (depends on your setup):
   
   If using systemd:
     sudo systemctl restart gunicorn
   
   If using supervisor:
     sudo supervisorctl restart salon
   
   If using Docker:
     docker-compose restart

7. Test the fix:
   curl https://YOUR_SERVER_IP/api/services/
   Should return JSON, not an error


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPTION 3: Using doctl CLI (If you have it installed)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Install doctl (if not already installed):
   https://docs.digitalocean.com/reference/doctl/how-to/install/

2. Authenticate:
   doctl auth init

3. Find your app ID:
   doctl apps list

4. Trigger a deployment:
   doctl apps create-deployment YOUR_APP_ID

5. Watch the deployment logs:
   doctl apps logs YOUR_APP_ID --follow


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT WAS FIXED IN THE CODE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Fixed syntax error in serializers.py (line 164)
❌ OLD: except Exception as e:1 community question
✅ NEW: except Exception as e:

✅ Fixed booking form event handler in script.js
   - Added setupBookingForm() function
   - Form now submits to /api/bookings/
   - Shows success/error messages

✅ Fixed contact form event handler in script.js
   - Added setupContactForm() function
   - Form now submits to /api/contacts/


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HOW TO VERIFY THE FIX WORKED:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Test Services endpoint:
   https://smsalon-ehqso.ondigitalocean.app/api/services/
   
   Should return JSON like:
   {
     "count": 51,
     "results": [
       {"id": 1, "name": "Haircut", "price": "500.00", ...},
       ...
     ]
   }

2. Try the booking form:
   https://smsalonandbarbershop-px697.ondigitalocean.app/booking.html
   - Fill in the form and submit
   - Should see success message
   - Check backend logs for booking confirmation


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IF YOU STILL GET 500 ERRORS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Check the app logs on DigitalOcean:
   https://cloud.digitalocean.com/apps → Your App → Logs
   
   Look for Python error messages that show what's failing

2. Common issues:
   ❌ DATABASE_URL not set → Database connection fails
   ❌ Migrations not run → Tables don't exist
   ❌ Missing STATIC_ROOT → Static files not served
   ✅ Solution: Run migrations manually (see Option 1-3 above)

3. Test locally first:
   cd /home/angela/SmSalon/Backend
   python manage.py runserver
   Visit http://localhost:8000/api/services/
   If it works locally, the issue is environment setup on DigitalOcean


NEED HELP?
Run this locally to get detailed error info:
  python manage.py shell
  >>> from salon_app.models import Service
  >>> Service.objects.all()
  
If this errors, you're missing migrations locally too.
