from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .models import Service, Stylist, Booking, ContactMessage, Review, SalonSettings
from .serializers import (
    ServiceSerializer, StylistSerializer, BookingCreateSerializer,
    BookingListSerializer, ContactMessageSerializer, ReviewSerializer,
    SalonSettingsSerializer
)


# ==================== SERVICE VIEWSET ====================
class ServiceViewSet(viewsets.ModelViewSet):
    """
    List, retrieve, create, and manage services.
    GET /api/services/
    GET /api/services/{id}/
    POST /api/services/ - Create new service (admin only)
    PUT /api/services/{id}/ - Update service (admin only)
    DELETE /api/services/{id}/ - Delete service (admin only)
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filterset_fields = ['category']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def get_queryset(self):
        """Show inactive services to admins, only active to others"""
        if self.request.user and self.request.user.is_authenticated:
            return Service.objects.all()
        return Service.objects.filter(is_active=True)
    
    def destroy(self, request, *args, **kwargs):
        """Delete a service with proper error handling"""
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            if 'ProtectedError' in str(type(e)):
                return Response(
                    {'error': 'Cannot delete this service as it is used in existing bookings. Please mark it as inactive instead.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            raise


# ==================== STYLIST VIEWSET ====================
class StylistViewSet(viewsets.ModelViewSet):
    """
    List, retrieve, create, and manage stylists.
    GET /api/stylists/
    GET /api/stylists/{id}/
    POST /api/stylists/ - Create new stylist (admin only)
    PUT /api/stylists/{id}/ - Update stylist (admin only)
    DELETE /api/stylists/{id}/ - Delete stylist (admin only)
    GET /api/stylists/{id}/available-slots/?date=2026-01-20
    """
    queryset = Stylist.objects.filter(is_active=True)
    serializer_class = StylistSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]
    
    def get_queryset(self):
        """Show inactive stylists to admins, only active to others"""
        if self.request.user and self.request.user.is_authenticated:
            return Stylist.objects.all()
        return Stylist.objects.filter(is_active=True)
    
    @action(detail=True, methods=['get'])
    def available_slots(self, request, pk=None):
        """Get available time slots for a stylist"""
        stylist = self.get_object()
        date_str = request.query_params.get('date')
        
        if not date_str:
            return Response(
                {'error': 'date parameter is required (YYYY-MM-DD format)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from datetime import datetime
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            slots = stylist.available_slots(date)
            
            return Response({
                'date': date,
                'available_slots': [str(slot) for slot in slots]
            })
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )


# ==================== BOOKING VIEWSET ====================
class BookingViewSet(viewsets.ModelViewSet):
    """
    Create, list, and manage bookings.
    
    POST /api/bookings/ - Create new booking
    GET /api/bookings/ - List all bookings
    GET /api/bookings/{id}/ - Get booking details
    PUT /api/bookings/{id}/ - Update booking
    DELETE /api/bookings/{id}/ - Cancel booking
    POST /api/bookings/{id}/confirm/ - Confirm booking
    POST /api/bookings/{id}/cancel/ - Cancel booking
    """
    
    permission_classes = [AllowAny]
    filterset_fields = ['status', 'date', 'phone']
    search_fields = ['fullname', 'phone', 'email']
    ordering_fields = ['date', 'time', 'created_at']
    ordering = ['-date', '-time']
    
    def get_queryset(self):
        """Filter bookings by phone number or status"""
        queryset = Booking.objects.all()
        phone = self.request.query_params.get('phone')
        
        if phone:
            queryset = queryset.filter(phone=phone)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingListSerializer
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a booking"""
        booking = self.get_object()
        
        if booking.status == 'confirmed':
            return Response(
                {'error': 'Booking is already confirmed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'confirmed'
        booking.confirmed_at = timezone.now()
        booking.save()
        booking.send_confirmation_email()
        
        serializer = BookingListSerializer(booking)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()
        
        if not booking.can_be_cancelled():
            return Response(
                {'error': 'Booking can only be cancelled 24 hours before appointment'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'cancelled'
        booking.save()
        
        serializer = BookingListSerializer(booking)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming bookings"""
        from datetime import datetime
        bookings = Booking.objects.filter(
            date__gte=datetime.today(),
            status__in=['confirmed', 'pending']
        ).order_by('date', 'time')
        
        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data)


# ==================== CONTACT MESSAGE VIEWSET ====================
class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    Manage contact messages.
    
    POST /api/contacts/ - Send contact message
    GET /api/contacts/ - List all messages (admin only)
    """
    
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]


# ==================== REVIEW VIEWSET ====================
class ReviewViewSet(viewsets.ModelViewSet):
    """
    Manage reviews and testimonials.
    
    POST /api/reviews/ - Submit review
    GET /api/reviews/ - List approved reviews
    """
    
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        if self.request.method == 'GET':
            return Review.objects.filter(is_approved=True)
        return Review.objects.all()


# ==================== SALON SETTINGS VIEWSET ====================
class SalonSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get salon settings and information.
    
    GET /api/settings/
    """
    
    queryset = SalonSettings.objects.all()
    serializer_class = SalonSettingsSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current salon settings"""
        settings = SalonSettings.get_settings()
        serializer = self.get_serializer(settings)
        return Response(serializer.data)


# ==================== UTILITY ENDPOINTS ====================
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint"""
    return Response({'status': 'ok', 'message': 'Salon API is running'})


# ==================== AUTHENTICATION VIEWSET ====================
class SignupView(APIView):
    """
    User signup endpoint.
    POST /api/auth/signup/
    
    Required fields: username, email, password, password_confirm
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        password_confirm = request.data.get('password_confirm')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        
        # Validation
        if not all([username, email, password, password_confirm]):
            return Response(
                {'error': 'All fields are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if password != password_confirm:
            return Response(
                {'error': 'Passwords do not match'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(password) < 6:
            return Response(
                {'error': 'Password must be at least 6 characters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'User created successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    """
    User login endpoint.
    POST /api/auth/login/
    
    Required fields: username, password
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response(
                {'error': 'Invalid username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    User logout endpoint.
    POST /api/auth/logout/
    
    Required fields: refresh token
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response(
                {'message': 'Logout successful'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(APIView):
    """
    Get current user profile.
    GET /api/auth/profile/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        })
    
    def put(self, request):
        """Update user profile"""
        user = request.user
        
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.email = request.data.get('email', user.email)
        
        user.save()
        
        return Response({
            'message': 'Profile updated successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        })


# ==================== URL Configuration ====================
# DRF Router
router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'stylists', StylistViewSet, basename='stylist')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'contacts', ContactMessageViewSet, basename='contact')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'settings', SalonSettingsViewSet, basename='settings')

# URL Patterns
urlpatterns = [
    path('', include(router.urls)),
    path('health/', health_check, name='health-check'),
    path('auth/login/', LoginView.as_view(), name='login'),
]

