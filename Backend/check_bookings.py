#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salon_project.settings')
django.setup()

from salon_app.models import Booking, Service

bookings = Booking.objects.all()
print(f"Total bookings in database: {bookings.count()}")
print(f"Total services in database: {Service.objects.count()}")

if bookings.exists():
    print("\nRecent bookings:")
    for booking in bookings.order_by('-created_at')[:10]:
        print(f"  - {booking.fullname} | Service: {booking.service.name} | Date: {booking.date} {booking.time} | Status: {booking.status} | Created: {booking.created_at}")
else:
    print("No bookings found in database.")
