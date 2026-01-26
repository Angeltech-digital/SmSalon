#!/bin/bash

# Salon MVP - Quick Start Script
# This script helps you get started with the Salon MVP project

echo "🧴 Salon Website MVP - Quick Start"
echo "===================================="
echo ""

# Check Python version
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 found"
    python3 --version
else
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi

echo ""
echo "Choose an option:"
echo "1. Start Frontend Only (http://localhost:8001)"
echo "2. Start Backend (http://localhost:8000)"
echo "3. Start Both (Frontend + Backend)"
echo "4. Setup Backend (First time only)"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "Starting Frontend..."
        cd Frontend
        python3 -m http.server 8001
        ;;
    
    2)
        echo ""
        echo "Starting Backend..."
        cd Backend
        if [ ! -d "venv" ]; then
            echo "Creating virtual environment..."
            python3 -m venv venv
            source venv/bin/activate
            pip install -r requirements.txt
        else
            source venv/bin/activate
        fi
        python manage.py runserver
        ;;
    
    3)
        echo ""
        echo "Starting both Frontend and Backend..."
        echo "⚠️  This will open two terminals"
        echo ""
        echo "Backend starting at http://localhost:8000"
        echo "Frontend starting at http://localhost:8001"
        echo ""
        
        # Start backend in background
        cd Backend
        if [ ! -d "venv" ]; then
            python3 -m venv venv
            source venv/bin/activate
            pip install -r requirements.txt
        else
            source venv/bin/activate
        fi
        python manage.py runserver &
        BACKEND_PID=$!
        
        # Start frontend
        cd ../Frontend
        python3 -m http.server 8001 &
        FRONTEND_PID=$!
        
        echo ""
        echo "✅ Both servers are running!"
        echo "Press Ctrl+C to stop"
        wait
        ;;
    
    4)
        echo ""
        echo "Setting up Backend..."
        cd Backend
        
        # Create virtual environment
        echo "Creating virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
        
        # Install dependencies
        echo "Installing dependencies..."
        pip install -r requirements.txt
        
        # Create .env file
        if [ ! -f ".env" ]; then
            echo "Creating .env file..."
            cp .env.example .env
            echo "⚠️  Please edit .env with your settings"
        fi
        
        # Run migrations
        echo "Setting up database..."
        python manage.py makemigrations
        python manage.py migrate
        
        # Create superuser
        echo ""
        echo "Creating admin account..."
        python manage.py createsuperuser
        
        echo ""
        echo "✅ Backend setup complete!"
        echo "Run: python manage.py runserver"
        ;;
    
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac
