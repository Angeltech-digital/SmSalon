from django.contrib import admin
from .models import Service, Stylist, Booking, ContactMessage, Review, SalonSettings


# ==================== SERVICE ADMIN ====================
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'duration_minutes', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'category', 'description', 'price', 'duration_minutes')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ==================== STYLIST ADMIN ====================
@admin.register(Stylist)
class StylistAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'is_active', 'email', 'phone']
    list_filter = ['specialization', 'is_active']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['available_services']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone', 'photo')
        }),
        ('Professional Details', {
            'fields': ('specialization', 'bio', 'available_services')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ==================== BOOKING ADMIN ====================
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'service', 'stylist', 'date', 'time', 'status', 'phone']
    list_filter = ['status', 'date', 'service']
    search_fields = ['fullname', 'phone', 'email']
    readonly_fields = ['created_at', 'updated_at', 'confirmed_at', 'completed_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('fullname', 'phone', 'email')
        }),
        ('Appointment Details', {
            'fields': ('service', 'stylist', 'date', 'time', 'notes')
        }),
        ('Booking Status', {
            'fields': ('status', 'send_email')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['confirm_booking', 'mark_completed', 'cancel_booking']
    
    def confirm_booking(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} bookings confirmed')
    
    def mark_completed(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='completed', completed_at=timezone.now())
        self.message_user(request, f'{updated} bookings marked as completed')
    
    def cancel_booking(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} bookings cancelled')


# ==================== CONTACT MESSAGE ADMIN ====================
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'replied', 'created_at']
    list_filter = ['is_read', 'replied', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Message Information', {
            'fields': ('name', 'email', 'subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'replied')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_replied']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} messages marked as read')
    
    def mark_as_replied(self, request, queryset):
        updated = queryset.update(replied=True)
        self.message_user(request, f'{updated} messages marked as replied')


# ==================== REVIEW ADMIN ====================
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'rating', 'title', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['client_name', 'title', 'comment']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Review Information', {
            'fields': ('booking', 'client_name', 'rating', 'title', 'comment', 'photo')
        }),
        ('Status', {
            'fields': ('is_approved',)
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_reviews']
    
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} reviews approved')


# ==================== SALON SETTINGS ADMIN ====================
@admin.register(SalonSettings)
class SalonSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Salon Information', {
            'fields': ('salon_name', 'salon_description', 'phone', 'email', 'address')
        }),
        ('Operating Hours', {
            'fields': ('opening_time', 'closing_time')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url'),
            'classes': ('collapse',)
        }),
        ('Email Notifications', {
            'fields': ('booking_confirmation_enabled', 'admin_notification_enabled'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['updated_at']
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SalonSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False
