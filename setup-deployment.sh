#!/bin/bash
# Salon Management System - Quick Deployment Setup Script
# This script prepares your project for deployment

set -e

echo "================================"
echo "🚀 Salon Deployment Setup Script"
echo "================================"
echo ""

# Check if we're in the right directory
if [ ! -f "Backend/manage.py" ]; then
    echo "❌ Error: Please run this script from the Salon project root directory"
    exit 1
fi

echo "📋 Step 1: Installing Production Dependencies..."
cd Backend
pip install -r requirements.txt
pip install gunicorn whitenoise python-dotenv psycopg2-binary
pip freeze > requirements.txt.production
echo "✅ Dependencies installed"
echo ""

echo "📋 Step 2: Creating Production Configuration Files..."

# Create Procfile for Heroku
cat > Procfile << 'EOF'
release: python manage.py migrate
web: gunicorn salon_project.wsgi:application --log-file -
EOF
echo "✅ Created Procfile"

# Create runtime.txt for Heroku
echo "python-3.10.13" > runtime.txt
echo "✅ Created runtime.txt"

# Create .env.example for reference
cat > .env.example << 'EOF'
# Django Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database (PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/salon_db

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Celery (Optional)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
EOF
echo "✅ Created .env.example"

cd ..
echo ""

echo "📋 Step 3: Creating Deployment Helper Scripts..."

# Create Heroku deployment script
cat > deploy-heroku.sh << 'EOF'
#!/bin/bash
echo "🚀 Deploying to Heroku..."
echo ""
echo "Step 1: Login to Heroku"
heroku login
echo ""
echo "Step 2: Create Heroku app (enter app name when prompted)"
read -p "Enter app name (e.g., angela-salon): " APP_NAME
heroku create $APP_NAME
echo ""
echo "Step 3: Set environment variables"
read -sp "Enter SECRET_KEY: " SECRET_KEY
heroku config:set SECRET_KEY="$SECRET_KEY"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="$APP_NAME.herokuapp.com"
echo ""
echo "Step 4: Add PostgreSQL addon"
heroku addons:create heroku-postgresql:hobby-dev
echo ""
echo "Step 5: Deploy"
git push heroku main
echo ""
echo "✅ Deployment complete!"
echo "Visit: https://$APP_NAME.herokuapp.com"
EOF
chmod +x deploy-heroku.sh
echo "✅ Created deploy-heroku.sh"

# Create static files collection script
cat > collect-static.sh << 'EOF'
#!/bin/bash
echo "📦 Collecting static files..."
cd Backend
python manage.py collectstatic --noinput
cd ..
echo "✅ Static files collected in Backend/staticfiles/"
EOF
chmod +x collect-static.sh
echo "✅ Created collect-static.sh"

# Create migration script
cat > run-migrations.sh << 'EOF'
#!/bin/bash
echo "🔄 Running database migrations..."
cd Backend
python manage.py migrate
echo "✅ Migrations completed"
cd ..
EOF
chmod +x run-migrations.sh
echo "✅ Created run-migrations.sh"

echo ""
echo "================================"
echo "✅ Setup Complete!"
echo "================================"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Edit Backend/.env with your production settings:"
echo "   - Generate SECRET_KEY: python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\""
echo "   - Set DEBUG=False"
echo "   - Configure database"
echo "   - Configure email"
echo ""
echo "2. Choose deployment platform:"
echo ""
echo "   For Heroku (Easiest):"
echo "   $ bash deploy-heroku.sh"
echo ""
echo "   For PythonAnywhere:"
echo "   - Manual upload or git clone"
echo "   - See DEPLOYMENT_GUIDE.md for steps"
echo ""
echo "   For DigitalOcean:"
echo "   - See DEPLOYMENT_GUIDE.md for steps"
echo ""
echo "3. Before deploying, test locally:"
echo "   $ bash run-migrations.sh"
echo "   $ bash collect-static.sh"
echo ""
echo "📖 For detailed instructions, see: DEPLOYMENT_GUIDE.md"
echo ""
