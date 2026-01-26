from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.utils import timezone
from datetime import timedelta

# ==================== SERVICE MODEL ====================
class Service(models.Model):
    """Service offered by the salon"""
    
    SERVICE_CATEGORY_CHOICES = [
        ('hair', 'Hair Services'),
        ('nails', 'Nail Services'),
        ('makeup', 'Makeup Services'),
        ('braiding', 'Braiding & Weaves'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SERVICE_CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    duration_minutes = models.IntegerField(default=60, help_text="Service duration in minutes")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'name']
        verbose_name_plural = "Services"
    
    def __str__(self):
        return f"{self.name} - KES {self.price}"


# ==================== STYLIST MODEL ====================
class Stylist(models.Model):
    """Salon stylists/employees"""
    
    SPECIALIZATION_CHOICES = [
        ('hair', 'Hair Specialist'),
        ('nails', 'Nail Specialist'),
        ('makeup', 'Makeup Artist'),
        ('braiding', 'Braiding Expert'),
        ('general', 'General'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?[0-9]{7,}$', 'Enter a valid phone number')]
    )
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='stylists/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    available_services = models.ManyToManyField(Service, related_name='stylists')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def available_slots(self, date):
        """Get available time slots for a specific date"""
        # Define salon hours: 9 AM - 8 PM
        booked_times = Booking.objects.filter(
            stylist=self,
            date=date,
            status__in=['confirmed', 'completed']
        ).values_list('time', flat=True)
        
        # Generate available slots (hourly, 9 AM - 8 PM)
        from datetime import time, datetime, timedelta
        all_slots = []
        start_hour = 9
        end_hour = 20
        
        for hour in range(start_hour, end_hour):
            slot_time = time(hour, 0)
            if slot_time not in booked_times:
                all_slots.append(slot_time)
        
        return all_slots


# ==================== BOOKING MODEL ====================
class Booking(models.Model):
    """Appointment bookings"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Customer information
    fullname = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^\+?[0-9]{7,}$', 'Enter a valid phone number')]
    )
    email = models.EmailField(blank=True, null=True)
    
    # Appointment details
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='bookings')
    stylist = models.ForeignKey(Stylist, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    send_email = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-date', '-time']
        indexes = [
            models.Index(fields=['date', 'time']),
            models.Index(fields=['status']),
            models.Index(fields=['phone']),
        ]
    
    def __str__(self):
        return f"{self.fullname} - {self.service.name} on {self.date} at {self.time}"
    
    def is_upcoming(self):
        """Check if booking is in the future"""
        from datetime import datetime
        appointment_datetime = datetime.combine(self.date, self.time)
        return appointment_datetime > datetime.now()
    
    def is_overdue(self):
        """Check if booking time has passed"""
        from datetime import datetime
        appointment_datetime = datetime.combine(self.date, self.time)
        return appointment_datetime < datetime.now() and self.status != 'completed'
    
    def can_be_cancelled(self):
        """Check if booking can be cancelled (24 hours before appointment)"""
        from datetime import datetime, timedelta
        appointment_datetime = datetime.combine(self.date, self.time)
        return (appointment_datetime - datetime.now()).days >= 1
    
    def send_confirmation_email(self):
        """Send booking confirmation email"""
        from django.core.mail import send_mail
        from django.template.loader import render_to_string
        
        if not self.send_email or not self.email:
            return False
        
        try:
            subject = f"Booking Confirmation - {self.service.name}"
            message = f"""
            Hello {self.fullname},
            
            Your appointment has been confirmed!
            
            Service: {self.service.name}
            Date: {self.date}
            Time: {self.time}
            Stylist: {self.stylist.name if self.stylist else 'TBD'}
            Price: KES {self.service.price}
            
            Notes: {self.notes if self.notes else 'None'}
            
            Please arrive 5 minutes early.
            
            Thank you for booking with us!
            """
            
            send_mail(
                subject,
                message,
                'noreply@salon.com',
                [self.email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False


# ==================== CONTACT MESSAGE MODEL ====================
class ContactMessage(models.Model):
    """Contact form submissions"""
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    replied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


# ==================== SALON SETTINGS MODEL ====================
class SalonSettings(models.Model):
    """Salon configuration and settings"""
    
    salon_name = models.CharField(max_length=100, default="Salon")
    salon_description = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    opening_time = models.TimeField(default="09:00")
    closing_time = models.TimeField(default="20:00")
    
    # Social media
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    
    # Email settings
    booking_confirmation_enabled = models.BooleanField(default=True)
    admin_notification_enabled = models.BooleanField(default=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Salon Settings"
    
    def __str__(self):
        return self.salon_name
    
    @classmethod
    def get_settings(cls):
        """Get or create salon settings"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


# ==================== REVIEW/TESTIMONIAL MODEL ====================
class Review(models.Model):
    """Client reviews and testimonials"""
    
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    client_name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)
    title = models.CharField(max_length=100)
    comment = models.TextField()
    photo = models.ImageField(upload_to='reviews/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.client_name} - {self.rating} stars"
