#!/bin/bash

# 🚀 Salon Website Launcher Script

SALON_PATH="/home/angela/Salon"

echo "================================================"
echo "    🏪 Angela's Salon Website Launcher"
echo "================================================"
echo ""
echo "This script will start the frontend and backend."
echo ""
echo "Choose an option:"
echo "1. Start Backend Only (Django API)"
echo "2. Start Frontend Only (Website)"
echo "3. Start Both (in separate terminals)"
echo "4. View Admin Panel"
echo "5. View API Docs"
echo "6. Exit"
echo ""
read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo "Starting Backend (Django)..."
        cd "$SALON_PATH/Backend"
        source venv/bin/activate
        echo ""
        echo "📌 Backend running at: http://localhost:8000"
        echo "📌 Admin panel: http://localhost:8000/admin/"
        echo "   Login: admin / admin123"
        echo ""
        python manage.py runserver 0.0.0.0:8000
        ;;
    2)
        echo "Starting Frontend..."
        cd "$SALON_PATH/Frontend"
        echo ""
        echo "📌 Frontend running at: http://localhost:8001"
        echo ""
        python -m http.server 8001
        ;;
    3)
        echo "Starting both Backend and Frontend..."
        echo ""
        echo "🔄 Opening two terminal windows..."
        echo ""
        
        # Start backend in background
        (cd "$SALON_PATH/Backend" && source venv/bin/activate && python manage.py runserver 0.0.0.0:8000) &
        BACKEND_PID=$!
        
        sleep 2
        
        # Start frontend in background
        (cd "$SALON_PATH/Frontend" && python -m http.server 8001) &
        FRONTEND_PID=$!
        
        echo "✓ Backend running at http://localhost:8000"
        echo "✓ Frontend running at http://localhost:8001"
        echo ""
        echo "Press Ctrl+C to stop both servers"
        echo ""
        
        # Wait for both processes
        wait $BACKEND_PID $FRONTEND_PID
        ;;
    4)
        echo ""
        echo "Opening Admin Panel..."
        echo "URL: http://localhost:8000/admin/"
        echo "Username: admin"
        echo "Password: admin123"
        echo ""
        echo "⚠️  Make sure backend is running!"
        ;;
    5)
        echo ""
        echo "API Endpoints:"
        echo "- Services: http://localhost:8000/api/services/"
        echo "- Bookings: http://localhost:8000/api/bookings/"
        echo "- Contact: http://localhost:8000/api/contact/"
        echo "- Settings: http://localhost:8000/api/settings/"
        echo ""
        echo "⚠️  Make sure backend is running!"
        ;;
    6)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting..."
        exit 1
        ;;
esac
