# API Usage Guide

This guide provides examples of how to use the authentication API endpoints.

## Base URL
```
http://localhost:8000/api/auth/
```

## Authentication Flow

### 1. Register a New User

**Endpoint:** `POST /api/auth/register/`

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890"
  }'
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890",
    "bio": "",
    "birth_date": null,
    "profile_picture": null,
    "date_joined": "2024-02-03T10:30:00Z",
    "is_active": true
  },
  "message": "User registered successfully"
}
```

### 2. Login

**Endpoint:** `POST /api/auth/login/`

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "john.doe@example.com",
    "password": "SecurePass123!"
  }'
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890",
    "bio": "",
    "birth_date": null,
    "profile_picture": null,
    "date_joined": "2024-02-03T10:30:00Z",
    "is_active": true
  },
  "message": "Login successful"
}
```

> **Note:** The `-c cookies.txt` flag saves the session cookie for subsequent requests.

### 3. Get Current User

**Endpoint:** `GET /api/auth/user/`

**Request:**
```bash
curl -X GET http://localhost:8000/api/auth/user/ \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

**Response:**
```json
{
  "id": 1,
  "email": "john.doe@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890",
  "bio": "",
  "birth_date": null,
  "profile_picture": null,
  "date_joined": "2024-02-03T10:30:00Z",
  "is_active": true
}
```

### 4. Update User Profile

**Endpoint:** `PUT /api/auth/user/` or `PATCH /api/auth/user/`

**Request:**
```bash
curl -X PATCH http://localhost:8000/api/auth/user/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "first_name": "John",
    "last_name": "Smith",
    "bio": "Software developer with 5 years of experience",
    "phone_number": "+1234567890"
  }'
```

**Response:**
```json
{
  "first_name": "John",
  "last_name": "Smith",
  "phone_number": "+1234567890",
  "bio": "Software developer with 5 years of experience",
  "birth_date": null,
  "profile_picture": null
}
```

### 5. Change Password

**Endpoint:** `POST /api/auth/change-password/`

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/change-password/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "old_password": "SecurePass123!",
    "new_password": "NewSecurePass456!",
    "new_password_confirm": "NewSecurePass456!"
  }'
```

**Response:**
```json
{
  "message": "Password changed successfully"
}
```

### 6. Logout

**Endpoint:** `POST /api/auth/logout/`

**Request:**
```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -b cookies.txt
```

**Response:**
```json
{
  "message": "Logout successful"
}
```

## Admin Endpoints (Requires Admin Privileges)

### List All Users

**Endpoint:** `GET /api/auth/users/`

**Request:**
```bash
curl -X GET http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

### Get Specific User

**Endpoint:** `GET /api/auth/users/<user_id>/`

**Request:**
```bash
curl -X GET http://localhost:8000/api/auth/users/1/ \
  -H "Content-Type: application/json" \
  -b cookies.txt
```

## JavaScript/Fetch Examples

### Register User
```javascript
const registerUser = async (userData) => {
  const response = await fetch('http://localhost:8000/api/auth/register/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  });
  
  const data = await response.json();
  return data;
};

// Usage
const userData = {
  email: 'john.doe@example.com',
  password: 'SecurePass123!',
  password_confirm: 'SecurePass123!',
  first_name: 'John',
  last_name: 'Doe'
};

registerUser(userData).then(data => console.log(data));
```

### Login User
```javascript
const loginUser = async (credentials) => {
  const response = await fetch('http://localhost:8000/api/auth/login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include', // Important for session cookies
    body: JSON.stringify(credentials),
  });
  
  const data = await response.json();
  return data;
};

// Usage
const credentials = {
  email: 'john.doe@example.com',
  password: 'SecurePass123!'
};

loginUser(credentials).then(data => console.log(data));
```

### Get Current User
```javascript
const getCurrentUser = async () => {
  const response = await fetch('http://localhost:8000/api/auth/user/', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include', // Include session cookie
  });
  
  const data = await response.json();
  return data;
};

getCurrentUser().then(data => console.log(data));
```

### Update User Profile
```javascript
const updateProfile = async (updates) => {
  const response = await fetch('http://localhost:8000/api/auth/user/', {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify(updates),
  });
  
  const data = await response.json();
  return data;
};

// Usage
const updates = {
  first_name: 'John',
  last_name: 'Smith',
  bio: 'Updated bio'
};

updateProfile(updates).then(data => console.log(data));
```

### Logout
```javascript
const logoutUser = async () => {
  const response = await fetch('http://localhost:8000/api/auth/logout/', {
    method: 'POST',
    credentials: 'include',
  });
  
  const data = await response.json();
  return data;
};

logoutUser().then(data => console.log(data));
```

## React Example with Axios

```javascript
import axios from 'axios';

// Configure axios defaults
axios.defaults.baseURL = 'http://localhost:8000';
axios.defaults.withCredentials = true; // Important for session cookies

// Login
const login = async (email, password) => {
  try {
    const response = await axios.post('/api/auth/login/', {
      email,
      password
    });
    return response.data;
  } catch (error) {
    console.error('Login failed:', error.response.data);
    throw error;
  }
};

// Get current user
const getCurrentUser = async () => {
  try {
    const response = await axios.get('/api/auth/user/');
    return response.data;
  } catch (error) {
    console.error('Failed to get user:', error.response.data);
    throw error;
  }
};

// Logout
const logout = async () => {
  try {
    const response = await axios.post('/api/auth/logout/');
    return response.data;
  } catch (error) {
    console.error('Logout failed:', error.response.data);
    throw error;
  }
};
```

## Error Responses

All endpoints return standard error responses:

**400 Bad Request:**
```json
{
  "email": ["This field is required."],
  "password": ["This field is required."]
}
```

**401 Unauthorized:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden:**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**404 Not Found:**
```json
{
  "detail": "Not found."
}
```

## CSRF Protection

For session-based authentication, you need to include the CSRF token in your requests. Django provides this automatically in forms, but for AJAX requests:

1. Get the CSRF token from the cookie
2. Include it in the `X-CSRFToken` header

```javascript
// Get CSRF token from cookie
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Include in fetch requests
fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken,
  },
  credentials: 'include',
  body: JSON.stringify(data),
});
```
