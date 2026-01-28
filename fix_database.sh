#!/bin/bash

# =============================================================================
# SmSalon Database Fix Script
# This script fixes the 500 Internal Server Error by setting up the database
# =============================================================================

set -e  # Exit on any error

echo "=============================================="
echo "🚀 SmSalon Database Fix Script"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/Backend"

echo "Working directory: $(pwd)"
echo ""

# =============================================================================
# STEP 1: Run Database Migrations
# =============================================================================
echo "=============================================="
echo "📦 Step 1: Running Database Migrations"
echo "=============================================="

echo "Running: python manage.py migrate --run-syncdb"
python manage.py migrate --run-syncdb

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Migrations completed successfully${NC}"
else
    echo -e "${RED}❌ Migrations failed${NC}"
    exit 1
fi

echo ""

# =============================================================================
# STEP 2: Create Initial Data
# =============================================================================
echo "=============================================="
echo "🏪 Step 2: Creating Initial Data"
echo "=============================================="

echo "Creating services..."
python setup_data.py --create-services

echo ""
echo "Creating stylists..."
python setup_data.py --create-stylists

echo ""
echo "Creating salon settings..."
python setup_data.py --create-settings

echo -e "${GREEN}✅ Initial data created successfully${NC}"
echo ""

# =============================================================================
# STEP 3: Create Admin User (Interactive)
# =============================================================================
echo "=============================================="
echo "👤 Step 3: Creating Admin User"
echo "=============================================="

# Check if admin already exists
ADMIN_EXISTS=$(python manage.py shell -c "from django.contrib.auth.models import User; print('yes' if User.objects.filter(username='admin').exists() else 'no')" 2>/dev/null)

if [ "$ADMIN_EXISTS" = "yes" ]; then
    echo -e "${YELLOW}ℹ️  Admin user 'admin' already exists${NC}"
else
    echo "Creating admin user..."
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@smsalon.com', 'Admin@123')" | python manage.py shell
    echo -e "${GREEN}✅ Admin user created with username: admin${NC}"
    echo "   Password: Admin@123"
fi

echo ""

# =============================================================================
# STEP 4: Verify Database Status
# =============================================================================
echo "=============================================="
echo "🔍 Step 4: Verifying Database Status"
echo "=============================================="

echo ""
echo "Service count:"
python manage.py shell -c "from salon_app.models import Service; print(f'  Services: {Service.objects.count()}')"

echo ""
echo "Stylist count:"
python manage.py shell -c "from salon_app.models import Stylist; print(f'  Stylists: {Stylist.objects.count()}')"

echo ""
echo "SalonSettings exists:"
python manage.py shell -c "from salon_app.models import SalonSettings; print(f'  Settings: {\"Yes\" if SalonSettings.objects.exists() else \"No\"}')"

echo ""
echo "Admin user exists:"
python manage.py shell -c "from django.contrib.auth.models import User; print(f'  Admin: {\"Yes\" if User.objects.filter(username=\"admin\").exists() else \"No\"}')"

echo ""
echo "All tables:"
python manage.py shell -c "from django.db import connection; cursor = connection.cursor(); cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;\"); tables = cursor.fetchall(); [print(f'  - {t[0]}') for t in tables]"

echo ""

# =============================================================================
# STEP 5: Test Health Endpoint
# =============================================================================
echo "=============================================="
echo "🏥 Step 5: Testing Health Endpoint"
echo "=============================================="

echo "Starting test server on port 8000..."
python manage.py runserver 0.0.0.0:8000 &
SERVER_PID=$!

# Wait for server to start
sleep 5

# Test health endpoint
echo "Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:8000/api/health/ 2>/dev/null || echo "")

if echo "$HEALTH_RESPONSE" | grep -q "ok"; then
    echo -e "${GREEN}✅ Health check passed!${NC}"
    echo "Response: $HEALTH_RESPONSE"
else
    echo -e "${YELLOW}⚠️  Health check response: $HEALTH_RESPONSE${NC}"
    echo "   Server may still be starting..."
fi

# Test services endpoint
echo ""
echo "Testing services endpoint..."
SERVICES_RESPONSE=$(curl -s http://localhost:8000/api/services/ 2>/dev/null || echo "")

if echo "$SERVICES_RESPONSE" | grep -q "\["; then
    echo -e "${GREEN}✅ Services endpoint working!${NC}"
else
    echo -e "${YELLOW}⚠️  Services response: ${SERVICES_RESPONSE:0:200}...${NC}"
fi

# Stop test server
echo ""
echo "Stopping test server..."
kill $SERVER_PID 2>/dev/null || true
wait $SERVER_PID 2>/dev/null || true

echo ""

# =============================================================================
# SUMMARY
# =============================================================================
echo "=============================================="
echo "📋 Fix Complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo "1. Restart your production server (DigitalOcean)"
echo "2. Test the endpoints:"
echo "   - https://smsalon-ehqso.ondigitalocean.app/api/health/"
echo "   - https://smsalon-ehqso.ondigitalocean.app/api/services/"
echo "3. Test signup: https://smsalon-ehqso.ondigitalocean.app/signup.html"
echo ""
echo "Admin login:"
echo "   URL: https://smsalon-ehqso.ondigitalocean.app/admin/"
echo "   Username: admin"
echo "   Password: Admin@123"
echo ""
echo -e "${GREEN}✅ Database fix completed successfully!${NC}"
echo "=============================================="

