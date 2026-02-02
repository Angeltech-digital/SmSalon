#!/usr/bin/env python3
"""
Script to create an admin user for the SM Salon application.
Run this script to set up the initial admin account.
"""
import os
import sys
import django

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salon_project.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_admin_user():
    User = get_user_model()
    
    print("=" * 50)
    print("SM Salon - Admin User Creation")
    print("=" * 50)
    
    # Check if admin already exists
    if User.objects.filter(username='admin').exists():
        admin = User.objects.get(username='admin')
        if admin.is_staff:
            print("\n✓ Admin user 'admin' already exists with staff privileges.")
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()
            print("✓ Updated admin privileges.")
            return
        else:
            print("\n✗ User 'admin' exists but is not staff. Updating...")
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()
            print("✓ Admin privileges granted.")
            return
    
    # Create new admin user
    username = 'admin'
    email = 'admin@sm-salon.com'
    password = 'admin123'
    
    try:
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name='Admin',
            last_name='User'
        )
        print(f"\n✓ Admin user created successfully!")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        print("\n⚠️  Please change the password after first login!")
    except Exception as e:
        print(f"\n✗ Error creating admin user: {e}")

if __name__ == '__main__':
    create_admin_user()

