from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ServiceViewSet,
    StylistViewSet,
    BookingViewSet,
    ContactMessageViewSet,
    ReviewViewSet,
    SalonSettingsViewSet,
    health_check,
    LoginView,
)

# ---------------------------
# DRF Router
# ---------------------------
router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'stylists', StylistViewSet, basename='stylist')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'contacts', ContactMessageViewSet, basename='contact')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'settings', SalonSettingsViewSet, basename='settings')

# ---------------------------
# URL Patterns
# ---------------------------
urlpatterns = [
    path('', include(router.urls)),
    path('health/', health_check, name='health-check'),
    path('auth/login/', LoginView.as_view(), name='login'),
]
