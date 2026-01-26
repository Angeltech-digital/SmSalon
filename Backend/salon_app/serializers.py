from rest_framework import serializers
from .models import Service, Stylist, Booking, ContactMessage, Review, SalonSettings

# ==================== SERVICE SERIALIZER ====================
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'category', 'description', 'price', 'duration_minutes']


# ==================== STYLIST SERIALIZER ====================
class StylistSerializer(serializers.ModelSerializer):
    available_services = ServiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Stylist
        fields = ['id', 'name', 'specialization', 'bio', 'photo', 'available_services']


# ==================== BOOKING SERIALIZER ====================
class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'fullname', 'phone', 'email', 'service', 'stylist',
            'date', 'time', 'notes', 'send_email'
        ]
    
    def validate_date(self, value):
        """Ensure booking date is in the future"""
        from datetime import date
        if value < date.today():
            raise serializers.ValidationError("Booking date must be in the future")
        return value
    
    def validate_phone(self, value):
        """Validate phone number format"""
        import re
        if not re.match(r'^\+?[0-9]{7,}$', value.replace(' ', '')):
            raise serializers.ValidationError("Invalid phone number format")
        return value
    
    def validate(self, data):
        """Validate date and time combination"""
        from datetime import datetime
        appointment_datetime = datetime.combine(data['date'], data['time'])
        if appointment_datetime < datetime.now():
            raise serializers.ValidationError(
                "Booking time must be in the future"
            )
        return data
    
    def create(self, validated_data):
        """Create booking and send confirmation email"""
        booking = Booking.objects.create(**validated_data)
        booking.status = 'confirmed'
        booking.save()
        
        # Send confirmation email
        if booking.send_email:
            booking.send_confirmation_email()
        
        # Send admin notification
        self.send_admin_notification(booking)
        
        return booking
    
    @staticmethod
    def send_admin_notification(booking):
        """Send notification to salon admin"""
        from django.core.mail import send_mail
        settings = SalonSettings.get_settings()
        
        if not settings.admin_notification_enabled:
            return
        
        try:
            subject = f"New Booking - {booking.service.name}"
            message = f"""
            New booking received!
            
            Client: {booking.fullname}
            Phone: {booking.phone}
            Email: {booking.email or 'Not provided'}
            Service: {booking.service.name}
            Date: {booking.date}
            Time: {booking.time}
            Notes: {booking.notes or 'None'}
            """
            
            send_mail(
                subject,
                message,
                'noreply@salon.com',
                [settings.email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Error sending admin notification: {e}")


class BookingListSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    stylist = StylistSerializer(read_only=True)
    is_upcoming = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'fullname', 'phone', 'email', 'service', 'stylist',
            'date', 'time', 'status', 'created_at', 'is_upcoming'
        ]
        read_only_fields = ['id', 'created_at', 'status']
    
    def get_is_upcoming(self, obj):
        return obj.is_upcoming()


# ==================== CONTACT MESSAGE SERIALIZER ====================
class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
    
    def create(self, validated_data):
        """Create contact message and send notification"""
        message = ContactMessage.objects.create(**validated_data)
        
        # Send admin notification
        self.send_admin_notification(message)
        
        return message
    
    @staticmethod
    def send_admin_notification(contact_message):
        """Send notification to salon admin"""
        from django.core.mail import send_mail
        settings = SalonSettings.get_settings()
        
        try:
            subject = f"New Message - {contact_message.subject}"
            message = f"""
            New contact message received!
            
            From: {contact_message.name}
            Email: {contact_message.email}
            Subject: {contact_message.subject}
            
            Message:
            {contact_message.message}
            """
            
            send_mail(
                subject,
                message,
                'noreply@salon.com',
                [settings.email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Error sending contact notification: {e}")


# ==================== REVIEW SERIALIZER ====================
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'booking', 'client_name', 'rating', 'title', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']


# ==================== SALON SETTINGS SERIALIZER ====================
class SalonSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalonSettings
        fields = [
            'salon_name', 'salon_description', 'phone', 'email', 'address',
            'opening_time', 'closing_time', 'facebook_url', 'instagram_url', 'twitter_url'
        ]
