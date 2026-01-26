from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ServiceViewSet, StylistViewSet, BookingViewSet, ContactMessageViewSet,
    ReviewViewSet, SalonSettingsViewSet, health_check,
    SignupView, LoginView, LogoutView, UserProfileView
)

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'stylists', StylistViewSet, basename='stylist')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'contacts', ContactMessageViewSet, basename='contact')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'settings', SalonSettingsViewSet, basename='settings')

urlpatterns = [
    path('', include(router.urls)),
    path('health/', health_check, name='health-check'),
    
    # Authentication endpoints
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
