# Authentication API Documentation

## Overview
This document describes the authentication endpoints for the Salon Management System admin panel.

## Base URL
```
http://localhost:8000/api
```

## Authentication

### 1. Sign Up (Register New Admin)
**Endpoint:** `POST /auth/signup/`

**Description:** Create a new admin account

**Request Body:**
```json
{
  "username": "admin_username",
  "email": "admin@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (201 Created):**
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "username": "admin_username",
    "email": "admin@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Validation Rules:**
- Username: 3+ characters, unique
- Email: Valid format, unique
- Password: Minimum 6 characters
- Password and password_confirm must match

**Error Responses:**
- 400: Validation error (missing fields, passwords don't match, etc.)
- 409: Username or email already exists

---

### 2. Login
**Endpoint:** `POST /auth/login/`

**Description:** Authenticate admin and get JWT tokens

**Request Body:**
```json
{
  "username": "admin_username",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "admin_username",
    "email": "admin@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_staff": false,
    "is_superuser": false
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Error Responses:**
- 400: Missing username or password
- 401: Invalid credentials

---

### 3. Get User Profile
**Endpoint:** `GET /auth/profile/`

**Description:** Get current logged-in user's profile

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "admin_username",
  "email": "admin@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "is_staff": false,
  "is_superuser": false
}
```

**Error Responses:**
- 401: Unauthorized (missing or invalid token)

---

### 4. Update User Profile
**Endpoint:** `PUT /auth/profile/`

**Description:** Update current user's profile

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "newemail@example.com"
}
```

**Response (200 OK):**
```json
{
  "message": "Profile updated successfully",
  "user": {
    "id": 1,
    "username": "admin_username",
    "email": "newemail@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

**Error Responses:**
- 400: Invalid data
- 401: Unauthorized

---

### 5. Logout
**Endpoint:** `POST /auth/logout/`

**Description:** Logout and invalidate refresh token

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{
  "message": "Logout successful"
}
```

**Error Responses:**
- 400: Missing refresh token
- 401: Unauthorized

---

### 6. Refresh Access Token
**Endpoint:** `POST /auth/token/refresh/`

**Description:** Get a new access token using refresh token

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Error Responses:**
- 401: Invalid or expired refresh token

---

## JWT Token Details

### Token Lifetime
- **Access Token:** 1 hour (3600 seconds)
- **Refresh Token:** 1 day (86400 seconds)

### Using JWT Tokens
All authenticated endpoints require the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

Example:
```bash
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  http://localhost:8000/api/auth/profile/
```

---

## Protected Endpoints

After authentication, you can access these admin endpoints with your access token:

### Bookings
- `GET /bookings/` - List all bookings
- `GET /bookings/{id}/` - Get booking details
- `POST /bookings/` - Create new booking
- `PUT /bookings/{id}/` - Update booking
- `DELETE /bookings/{id}/` - Cancel booking
- `POST /bookings/{id}/confirm/` - Confirm booking
- `POST /bookings/{id}/cancel/` - Cancel booking

### Stylists
- `GET /stylists/` - List all stylists
- `GET /stylists/{id}/` - Get stylist details
- `GET /stylists/{id}/available-slots/?date=2026-01-20` - Get available slots

### Services
- `GET /services/` - List all services
- `GET /services/{id}/` - Get service details

### Contacts
- `GET /contacts/` - List all contact messages (admin only)
- `GET /contacts/{id}/` - Get message details (admin only)
- `POST /contacts/` - Submit contact message (public)

### Reviews
- `GET /reviews/` - List approved reviews (public)
- `POST /reviews/` - Submit review (public)
- `GET /reviews/{id}/` - Get review details (public)

### Settings
- `GET /settings/` - Get salon settings (public)
- `GET /settings/current/` - Get current salon settings (public)

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict (duplicate) |
| 500 | Server Error |

---

## Frontend Integration Example

### Login
```javascript
const response = await fetch('http://localhost:8000/api/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'admin_username',
    password: 'securepassword123'
  })
});

const data = await response.json();
localStorage.setItem('access_token', data.access);
localStorage.setItem('refresh_token', data.refresh);
```

### Authenticated Request
```javascript
const response = await fetch('http://localhost:8000/api/auth/profile/', {
  headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
});

const user = await response.json();
console.log(user);
```

### Refresh Token
```javascript
const response = await fetch('http://localhost:8000/api/auth/token/refresh/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    refresh: localStorage.getItem('refresh_token')
  })
});

const data = await response.json();
localStorage.setItem('access_token', data.access);
```

---

## CORS Configuration

The API is configured to accept requests from:
- http://localhost:3000
- http://localhost:8000
- http://localhost
- http://127.0.0.1:3000
- http://127.0.0.1

To add more origins, update `CORS_ALLOWED_ORIGINS` in `Backend/salon_project/settings.py`.

---

## Security Notes

1. **Never** store access tokens in localStorage for production. Use httpOnly cookies instead.
2. **Always** use HTTPS in production to prevent token interception.
3. Refresh tokens should be stored securely and sent only with requests requiring new access tokens.
4. Consider implementing token rotation for enhanced security.
5. Set appropriate CORS policies for your domain in production.

---

## Testing with cURL

```bash
# Sign up
curl -X POST http://localhost:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testadmin",
    "email": "test@example.com",
    "password": "test1234",
    "password_confirm": "test1234",
    "first_name": "Test",
    "last_name": "Admin"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testadmin",
    "password": "test1234"
  }'

# Get Profile
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
