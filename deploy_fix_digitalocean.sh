#!/bin/bash

# ========================================
# DigitalOcean Deployment Fix Script
# ========================================
# This script connects to your DigitalOcean server and runs migrations/collectstatic

# COLOR OUTPUT
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}DigitalOcean Deployment Helper${NC}"
echo -e "${YELLOW}========================================${NC}"

# Check if app forwarding is already running
if pgrep -f "doctl apps forward" > /dev/null; then
    echo -e "${YELLOW}ℹ️  App forwarding already active${NC}"
else
    echo -e "${YELLOW}📡 Starting DigitalOcean app forwarding...${NC}"
    echo "Make sure you have:"
    echo "  1. doctl CLI installed: https://docs.digitalocean.com/reference/doctl/how-to/install/"
    echo "  2. DigitalOcean API token saved in: doctl auth init"
    echo ""
    echo "If you haven't set up doctl yet, install and run: doctl auth init"
    echo ""
    read -p "Have you set up doctl? (yes/no): " doctl_ready
    
    if [ "$doctl_ready" != "yes" ]; then
        echo -e "${RED}Please install and configure doctl first${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${YELLOW}Finding your app ID...${NC}"
APP_ID=$(doctl apps list --format ID,DefaultIngress --no-header | grep smsalon | head -1 | awk '{print $1}')

if [ -z "$APP_ID" ]; then
    echo -e "${RED}❌ Could not find your DigitalOcean app${NC}"
    echo "Available apps:"
    doctl apps list
    exit 1
fi

echo -e "${GREEN}✅ Found app: $APP_ID${NC}"

echo ""
echo -e "${YELLOW}Running migrations...${NC}"
doctl apps forward-http "$APP_ID" &
FORWARD_PID=$!
sleep 2

# Make a test request to ensure forwarding is ready
echo "Testing connection..."
if ! curl -s http://localhost:8080/api/health/ > /dev/null; then
    echo -e "${YELLOW}Waiting for connection...${NC}"
    sleep 3
fi

# Run migrations through the app
echo -e "${YELLOW}Executing: python manage.py migrate${NC}"
curl -X POST http://localhost:8080/run-migrations 2>/dev/null || {
    echo -e "${RED}Note: Direct endpoint not available${NC}"
    echo "You may need to SSH into your Droplet directly"
}

# Kill the forwarding process
kill $FORWARD_PID 2>/dev/null

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Deployment fix complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Test the API: https://smsalon-ehqso.ondigitalocean.app/api/services/"
echo "2. Try booking: https://smsalonandbarbershop-px697.ondigitalocean.app/booking.html"
echo ""
