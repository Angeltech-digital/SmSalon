#!/bin/bash
# =============================================================================
# SmSalon Quick Fix Script - Run on DigitalOcean Server
# This fixes the 500 Internal Server Error by setting up the database
# =============================================================================

set -e

echo "=============================================="
echo "🚀 SmSalon Quick Fix Script"
echo "=============================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Navigate to project
cd /home/angela/smsalon

echo "Step 1: Pulling latest code..."
echo "================================"
git pull origin main
echo -e "${GREEN}✅ Code updated${NC}"
echo ""

echo "Step 2: Running database migrations..."
echo "======================================"
cd Backend
source venv/bin/activate

python manage.py migrate --run-syncdb
echo -e "${GREEN}✅ Migrations completed${NC}"
echo ""

echo "Step 3: Creating initial data..."
echo "================================="
python setup_data.py --create-services
python setup_data.py --create-stylists
python setup_data.py --create-settings
echo -e "${GREEN}✅ Initial data created${NC}"
echo ""

echo "Step 4: Creating admin user..."
echo "================================"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@smsalon.com', 'Admin@123')" | python manage.py shell
echo -e "${GREEN}✅ Admin user created${NC}"
echo ""

echo "Step 5: Restarting server..."
echo "=============================="
sudo systemctl restart gunicorn
echo -e "${GREEN}✅ Server restarted${NC}"
echo ""

echo "=============================================="
echo "✅ Fix Complete!"
echo "=============================================="
echo ""
echo "Test these URLs:"
echo "1. https://smsalon-ehqso.ondigitalocean.app/api/health/"
echo "2. https://smsalon-ehqso.ondigitalocean.app/api/services/"
echo "3. https://smsalon-ehqso.ondigitalocean.app/login.html"
echo ""
echo "Admin login: admin / Admin@123"
echo "=============================================="

