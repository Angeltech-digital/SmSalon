#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salon_project.settings')
django.setup()

from salon_app.models import Service

# Services to add from services.html
services_to_add = [
    # Hair Services
    {'name': 'Ladies Haircut', 'category': 'hair', 'description': 'Professional ladies haircut', 'price': 500},
    {'name': 'Gents Haircut', 'category': 'hair', 'description': 'Professional gents haircut', 'price': 400},
    {'name': 'Kids Haircut', 'category': 'hair', 'description': 'Professional kids haircut', 'price': 200},
    {'name': 'Braiding', 'category': 'hair', 'description': 'Professional braiding services', 'price': 1500},
    {'name': 'Weaving', 'category': 'hair', 'description': 'Professional hair weaving', 'price': 2000},
    {'name': 'Wig Gluing', 'category': 'hair', 'description': 'Professional wig gluing service', 'price': 1000},
    {'name': 'Dreadlocks Fresh', 'category': 'hair', 'description': 'Fresh dreadlock installation', 'price': 3000},
    {'name': 'Dreadlocks Retouch', 'category': 'hair', 'description': 'Dreadlock retouch and maintenance', 'price': 1750},
    {'name': 'Hair Relaxer', 'category': 'hair', 'description': 'Hair relaxer treatment', 'price': 1750},
    {'name': 'Hair & Scalp Treatment', 'category': 'hair', 'description': 'Professional hair and scalp treatment', 'price': 1300},
    {'name': 'Hair Coloring / Dye', 'category': 'hair', 'description': 'Professional hair coloring and dyeing', 'price': 1450},
    
    # Nail Services
    {'name': 'Manicure', 'category': 'nails', 'description': 'Classic or gel manicure', 'price': 500},
    {'name': 'Pedicure', 'category': 'nails', 'description': 'Classic or gel pedicure', 'price': 1500},
    {'name': 'Normal Polish', 'category': 'nails', 'description': 'Nail polish application', 'price': 300},
    {'name': 'Gel Polish', 'category': 'nails', 'description': 'Gel polish application', 'price': 700},
    {'name': 'Acrylics', 'category': 'nails', 'description': 'Acrylic nail extensions', 'price': 2750},
    {'name': 'Gum Gel', 'category': 'nails', 'description': 'Gum gel nail service', 'price': 1750},
    {'name': 'Stick Ons', 'category': 'nails', 'description': 'Pre-made stick on nails', 'price': 1200},
    {'name': 'Dip Powder', 'category': 'nails', 'description': 'Dip powder nail coating', 'price': 1750},
    {'name': 'Builder Gel / Overlay', 'category': 'nails', 'description': 'Builder gel or overlay application', 'price': 1250},
    {'name': 'Soak Off', 'category': 'nails', 'description': 'Removal of nail extensions', 'price': 650},
    
    # Makeup & Lashes
    {'name': 'Makeup Only', 'category': 'makeup', 'description': 'Professional makeup application', 'price': 3000},
    {'name': 'Makeup with Eyelashes', 'category': 'makeup', 'description': 'Professional makeup with eyelashes', 'price': 3250},
    {'name': 'Synthetic Eyelashes', 'category': 'makeup', 'description': 'Synthetic eyelash application', 'price': 1000},
    {'name': 'Human Hair Eyelashes', 'category': 'makeup', 'description': 'Human hair eyelash application', 'price': 2500},
    
    # Wigs
    {'name': 'Straight / Bob Wigs', 'category': 'braiding', 'description': 'Straight or bob style wigs', 'price': 11000},
    {'name': 'Water Curl / Jerry / Deep Wave', 'category': 'braiding', 'description': 'Curly or wavy style wigs', 'price': 12000},
    {'name': 'Wig Washing & Styling', 'category': 'braiding', 'description': 'Professional wig washing and styling', 'price': 1400},
    
    # Other Services (Skincare/Massage/Piercing)
    {'name': 'Facial', 'category': 'general', 'description': 'Professional facial treatment', 'price': 1500},
    {'name': 'Full Body Massage', 'category': 'general', 'description': 'Full body massage therapy', 'price': 2500},
    {'name': 'Ear Piercing', 'category': 'general', 'description': 'Professional ear piercing', 'price': 700},
    {'name': 'Nose Piercing', 'category': 'general', 'description': 'Professional nose piercing', 'price': 700},
    {'name': 'Eyebrow Shaping', 'category': 'general', 'description': 'Eyebrow shaping and trimming', 'price': 350},
    {'name': 'Eyebrow Shaping with Henna', 'category': 'general', 'description': 'Eyebrow shaping with henna tint', 'price': 600},
    
    # Barbershop
    {'name': 'Beard Trim', 'category': 'hair', 'description': 'Professional beard trimming', 'price': 200},
    {'name': 'Hair Wash & Scalp Massage', 'category': 'hair', 'description': 'Hair wash with relaxing scalp massage', 'price': 400},
    {'name': 'Head & Neck Massage', 'category': 'general', 'description': 'Relaxing head and neck massage', 'price': 500},
    {'name': 'Under Arm Waxing', 'category': 'general', 'description': 'Under arm waxing service', 'price': 700},
    {'name': 'Chest Waxing', 'category': 'general', 'description': 'Chest waxing service', 'price': 1000},
]

# Get existing services to avoid duplicates
existing_services = set(Service.objects.values_list('name', flat=True))

added_count = 0
for service_data in services_to_add:
    if service_data['name'] not in existing_services:
        service = Service.objects.create(**service_data)
        print(f"✅ Added: {service.name} - KES {service.price}")
        added_count += 1
    else:
        print(f"⏭️  Already exists: {service_data['name']}")

print(f"\n✅ Total new services added: {added_count}")
print(f"📊 Total services in database: {Service.objects.count()}")
