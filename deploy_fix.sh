#!/bin/bash

# =============================================================================
# SmSalon Deploy Fix to DigitalOcean
# This script deploys the database fixes to the production server
# =============================================================================

set -e

echo "=============================================="
echo "🚀 Deploying Fix to DigitalOcean"
echo "=============================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
DO_APP_NAME="smsalon"
DO_SPACE_NAME="smsalon-files"

echo "Step 1: Committing changes to git..."
echo "===================================="

# Add and commit the fix script
git add fix_database.sh
git commit -m "Add database fix script"

echo -e "${GREEN}✅ Changes committed${NC}"
echo ""

echo "Step 2: Pushing to GitHub..."
echo "============================"
git push origin main

echo -e "${GREEN}✅ Pushed to GitHub${NC}"
echo ""

echo "Step 3: Triggering DigitalOcean deployment..."
echo "=============================================="
echo "Your app will automatically deploy from GitHub."
echo ""
echo "Once deployed, you need to:"
echo "1. SSH into your DigitalOcean server"
echo "2. Run the database fix script"
echo ""
echo "Commands to run on the server:"
echo "--------------------------------"
echo "cd /home/angela/smsalon"
echo "git pull origin main"
echo "cd Backend"
echo "source venv/bin/activate"
echo "python manage.py migrate --run-syncdb"
echo "python setup_data.py --create-services"
echo "python setup_data.py --create-stylists"
echo "python setup_data.py --create-settings"
echo "echo 'from django.contrib.auth.models import User; User.objects.create_superuser(\"admin\", \"admin@smsalon.com\", \"Admin@123\")' | python manage.py shell"
echo "sudo systemctl restart gunicorn"
echo ""
echo "Or simply run:"
echo "  cd /home/angela/smsalon"
echo "  ./fix_database.sh"
echo ""

echo "Step 4: Testing after deployment..."
echo "===================================="
echo "After deployment, test these URLs:"
echo ""
echo "1. Health Check:"
echo "   https://smsalon-ehqso.ondigitalocean.app/api/health/"
echo ""
echo "2. Services List:"
echo "   https://smsalon-ehqso.ondigitalocean.app/api/services/"
echo ""
echo "3. Signup Page:"
echo "   https://smsalon-ehqso.ondigitalocean.app/signup.html"
echo ""
echo "4. Admin Panel:"
echo "   https://smsalon-ehqso.ondigitalocean.app/admin/"
echo ""

echo -e "${GREEN}✅ Deployment script ready!${NC}"
echo "=============================================="

# Ask if user wants to connect to server
read -p "Do you want to connect to the server now? (y/n): " CONNECT

if [ "$CONNECT" = "y" ] || [ "$CONNECT" = "Y" ]; then
    echo ""
    echo "Connecting to server..."
    echo "Type 'exit' to disconnect"
    echo ""
    ssh angela@smsalon-ehqso.ondigitalocean.app
else
    echo ""
    echo "To connect later, run:"
    echo "  ssh angela@smsalon-ehqso.ondigitalocean.app"
fi

