#!/usr/bin/env python
"""
Quick Database Fix for SmSalon - Run this on DigitalOcean server
Usage: python run_fix.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salon_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from salon_app.models import Service, Stylist, SalonSettings

print("=" * 50)
print("🚀 SmSalon Quick Database Fix")
print("=" * 50)
print()

# Step 1: Verify/Run migrations
print("📦 Step 1: Running migrations...")
from django.core.management import call_command
call_command('migrate', '--run-syncdb', verbosity=1)
print("✅ Migrations complete")
print()

# Step 2: Create services
print("🏪 Step 2: Creating services...")
services = [
    {'name': 'Ladies Haircut', 'category': 'hair', 'description': 'Professional ladies haircut', 'price': 500},
    {'name': 'Gents Haircut', 'category': 'hair', 'description': 'Professional gents haircut', 'price': 400},
    {'name': 'Hair Coloring', 'category': 'hair', 'description': 'Professional hair coloring', 'price': 1450},
    {'name': 'Manicure', 'category': 'nails', 'description': 'Classic or gel manicure', 'price': 500},
    {'name': 'Pedicure', 'category': 'nails', 'description': 'Classic or gel pedicure', 'price': 1500},
    {'name': 'Makeup Only', 'category': 'makeup', 'description': 'Professional makeup application', 'price': 3000},
    {'name': 'Box Braids', 'category': 'braiding', 'description': 'Classic box braids', 'price': 4000},
]

for s in services:
    Service.objects.get_or_create(name=s['name'], defaults=s)
print(f"✅ Services: {Service.objects.count()} in database")
print()

# Step 3: Create stylists
print("👤 Step 3: Creating stylists...")
stylists = [
    {'name': 'Mary Wanjiku', 'email': 'mary@smsalon.com', 'phone': '+254712345671', 'specialization': 'hair', 'bio': 'Master stylist'},
    {'name': 'Sarah Akinyi', 'email': 'sarah@smsalon.com', 'phone': '+254712345672', 'specialization': 'nails', 'bio': 'Expert nail technician'},
]

for s in stylists:
    Stylist.objects.get_or_create(email=s['email'], defaults=s)
print(f"✅ Stylists: {Stylist.objects.count()} in database")
print()

# Step 4: Create settings
print("⚙️  Step 4: Creating salon settings...")
SalonSettings.objects.get_or_create(
    pk=1,
    defaults={
        'salon_name': 'SmSalon',
        'salon_description': 'Your premier beauty destination',
        'phone': '+254712345678',
        'email': 'info@smsalon.com',
        'address': 'Nairobi, Kenya',
    }
)
print("✅ Settings created")
print()

# Step 5: Create admin user
print("🔑 Step 5: Creating admin user...")
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@smsalon.com', 'Admin@123')
    print("✅ Admin user created: admin / Admin@123")
else:
    print("ℹ️  Admin user already exists")
print()

# Verify
print("=" * 50)
print("📊 Database Status")
print("=" * 50)
print(f"Services: {Service.objects.count()}")
print(f"Stylists: {Stylist.objects.count()}")
print(f"Settings: {'Yes' if SalonSettings.objects.exists() else 'No'}")
print(f"Admin: {'Yes' if User.objects.filter(username='admin').exists() else 'No'}")
print()

print("✅ Fix complete! Restart gunicorn with:")
print("  sudo systemctl restart gunicorn")
print("=" * 50)

