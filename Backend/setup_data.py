#!/usr/bin/env python
"""
Initial Data Setup Script for SmSalon
Run this after deployment to populate the database with initial data.

Usage:
    python setup_data.py --create-admin
    python setup_data.py --create-services
    python setup_data.py --create-settings
    python setup_data.py --all
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salon_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from salon_app.models import Service, Stylist, SalonSettings


def create_admin_user(username='admin', email='admin@smsalon.com', password=None):
    """Create superuser account"""
    if not password:
        print("❌ Error: Password is required")
        print("Usage: python setup_data.py --create-admin --password=YourPassword123")
        return False
    
    try:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'is_staff': True, 'is_superuser': True}
        )
        
        if created:
            user.set_password(password)
            user.save()
            print(f"✅ Admin user created: {username}")
        else:
            print(f"ℹ️  Admin user already exists: {username}")
        
        return True
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return False


def create_services():
    """Create initial services for the salon"""
    services = [
        # Hair Services
        {
            'name': 'Haircut & Style',
            'category': 'hair',
            'description': 'Professional haircut and styling with premium products',
            'price': 1500.00,
            'duration_minutes': 60
        },
        {
            'name': 'Hair Coloring',
            'category': 'hair',
            'description': 'Full hair coloring treatment including consultation',
            'price': 3500.00,
            'duration_minutes': 120
        },
        {
            'name': 'Hair Treatment',
            'category': 'hair',
            'description': 'Deep conditioning treatment for damaged hair',
            'price': 2000.00,
            'duration_minutes': 90
        },
        {
            'name': 'Blow Dry',
            'category': 'hair',
            'description': 'Professional blow drying and styling',
            'price': 800.00,
            'duration_minutes': 45
        },
        
        # Nail Services
        {
            'name': 'Manicure',
            'category': 'nails',
            'description': 'Complete nail care including cuticle treatment and polish',
            'price': 800.00,
            'duration_minutes': 45
        },
        {
            'name': 'Pedicure',
            'category': 'nails',
            'description': 'Luxury foot spa treatment with massage',
            'price': 1200.00,
            'duration_minutes': 60
        },
        {
            'name': 'Nail Extension',
            'category': 'nails',
            'description': 'Acrylic or gel nail extensions',
            'price': 2500.00,
            'duration_minutes': 90
        },
        {
            'name': 'Gel Polish',
            'category': 'nails',
            'description': 'Long-lasting gel polish application',
            'price': 1000.00,
            'duration_minutes': 45
        },
        
        # Makeup Services
        {
            'name': 'Bridal Makeup',
            'category': 'makeup',
            'description': 'Complete bridal makeup with trial session',
            'price': 5000.00,
            'duration_minutes': 120
        },
        {
            'name': 'Event Makeup',
            'category': 'makeup',
            'description': 'Professional makeup for parties and events',
            'price': 2500.00,
            'duration_minutes': 60
        },
        {
            'name': 'Natural Makeup',
            'category': 'makeup',
            'description': 'Subtle, natural-looking makeup enhancement',
            'price': 1500.00,
            'duration_minutes': 45
        },
        
        # Braiding Services
        {
            'name': 'Box Braids',
            'category': 'braiding',
            'description': 'Classic box braids (medium size)',
            'price': 4000.00,
            'duration_minutes': 240
        },
        {
            'name': 'Cornrows',
            'category': 'braiding',
            'description': 'Traditional cornrow braids',
            'price': 2000.00,
            'duration_minutes': 120
        },
        {
            'name': 'Twists',
            'category': 'braiding',
            'description': 'Two-strand twists styling',
            'price': 3000.00,
            'duration_minutes': 180
        },
        {
            'name': 'Faux Locs',
            'category': 'braiding',
            'description': 'Faux locs installation and styling',
            'price': 5000.00,
            'duration_minutes': 300
        },
    ]
    
    created_count = 0
    for service_data in services:
        service, created = Service.objects.get_or_create(
            name=service_data['name'],
            defaults=service_data
        )
        if created:
            created_count += 1
    
    print(f"✅ Created {created_count} new services")
    print(f"ℹ️  Total services in database: {Service.objects.count()}")
    return True


def create_stylists():
    """Create sample stylists"""
    stylists = [
        {
            'name': 'Mary Wanjiku',
            'email': 'mary@smsalon.com',
            'phone': '+254712345671',
            'specialization': 'hair',
            'bio': 'Master stylist with 10 years experience in hair coloring and styling'
        },
        {
            'name': 'Sarah Akinyi',
            'email': 'sarah@smsalon.com',
            'phone': '+254712345672',
            'specialization': 'nails',
            'bio': 'Expert nail technician specializing in nail art'
        },
        {
            'name': 'Grace Muthoni',
            'email': 'grace@smsalon.com',
            'phone': '+254712345673',
            'specialization': 'makeup',
            'bio': 'Professional makeup artist for weddings and events'
        },
        {
            'name': 'Faith Kemunto',
            'email': 'faith@smsalon.com',
            'phone': '+254712345674',
            'specialization': 'braiding',
            'bio': 'Braiding specialist with expertise in all braid styles'
        },
    ]
    
    created_count = 0
    for stylist_data in stylists:
        stylist, created = Stylist.objects.get_or_create(
            email=stylist_data['email'],
            defaults=stylist_data
        )
        if created:
            created_count += 1
    
    print(f"✅ Created {created_count} new stylists")
    print(f"ℹ️  Total stylists in database: {Stylist.objects.count()}")
    return True


def create_settings():
    """Create or update salon settings"""
    settings, created = SalonSettings.objects.get_or_create(
        pk=1,
        defaults={
            'salon_name': 'SmSalon',
            'salon_description': 'Your premier beauty destination. We offer professional hair, nail, makeup, and braiding services.',
            'phone': '+254712345678',
            'email': 'info@smsalon.com',
            'address': 'Nairobi, Kenya',
            'opening_time': '09:00:00',
            'closing_time': '20:00:00',
            'booking_confirmation_enabled': True,
            'admin_notification_enabled': True,
        }
    )
    
    if created:
        print("✅ Created salon settings")
    else:
        print("ℹ️  Salon settings already exist")
    
    return True


def main():
    """Main function to handle command line arguments"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Setup initial data for SmSalon')
    parser.add_argument('--create-admin', action='store_true', help='Create admin user')
    parser.add_argument('--create-services', action='store_true', help='Create initial services')
    parser.add_argument('--create-stylists', action='store_true', help='Create sample stylists')
    parser.add_argument('--create-settings', action='store_true', help='Create salon settings')
    parser.add_argument('--all', action='store_true', help='Create everything')
    parser.add_argument('--password', type=str, help='Password for admin user')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("🚀 SmSalon Data Setup")
    print("=" * 50)
    
    # If no specific arguments, show help
    if not any([args.create_admin, args.create_services, args.create_stylists, 
                args.create_settings, args.all]):
        parser.print_help()
        print("\n" + "=" * 50)
        print("Examples:")
        print("  python setup_data.py --all --password=MyPassword123")
        print("  python setup_data.py --create-services")
        print("  python setup_data.py --create-admin --password=admin123")
        print("=" * 50)
        return
    
    success = True
    
    if args.all or args.create_admin:
        if args.password:
            success = create_admin_user(password=args.password) and success
        else:
            print("⚠️  Skipping admin creation (--password not provided)")
    
    if args.all or args.create_services:
        success = create_services() and success
    
    if args.all or args.create_stylists:
        success = create_stylists() and success
    
    if args.all or args.create_settings:
        success = create_settings() and success
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Setup completed successfully!")
    else:
        print("⚠️  Setup completed with some errors")
    print("=" * 50)


if __name__ == '__main__':
    main()

