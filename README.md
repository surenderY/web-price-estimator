# Django REST Framework Backend Project

A complete Django backend setup with Django REST Framework, custom user model, authentication, and modern web templates.

## Features

- Custom User Model (email-based authentication)
- Django REST Framework API endpoints
- Session-based authentication
- Token authentication (optional)
- User registration and login
- Password reset functionality
- Profile management
- Permissions and authorization
- **Modern Web Templates** (Login, Register, Dashboard, Profile)
- Responsive UI with Bootstrap 5
- REST API + Traditional Web Interface

## Project Structure

```
django_project/
├── config/                 # Project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                  # Custom user app
│   ├── models.py          # Custom User model
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   ├── template_views.py  # Template-based views
│   ├── forms.py           # Django forms
│   ├── urls.py            # API URL routing
│   ├── template_urls.py   # Template URL routing
│   └── managers.py        # Custom user manager
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── home.html          # Landing page
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── dashboard.html     # User dashboard
│   └── profile.html       # User profile
├── requirements.txt
├── start.sh               # Quick start script
└── manage.py
```

## Quick Start

### Option 1: Use the Start Script (Recommended)

```bash
chmod +x start.sh
./start.sh
```

This script will:
- Create virtual environment
- Install dependencies
- Run migrations
- Collect static files
- Prompt to create superuser
- Start the development server

### Option 2: Manual Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## Available URLs

### Web Interface (Templates)
- **Home:** http://localhost:8000/
- **Login:** http://localhost:8000/login/
- **Register:** http://localhost:8000/register/
- **Dashboard:** http://localhost:8000/dashboard/ (requires login)
- **Profile:** http://localhost:8000/profile/ (requires login)
- **Admin:** http://localhost:8000/admin/

### API Endpoints
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/user/` - Get current user
- `PUT /api/auth/user/` - Update user profile
- `POST /api/auth/change-password/` - Change password

### Example Usage

**Register a new user:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

## Configuration

### Settings

Key settings in `config/settings.py`:

- `AUTH_USER_MODEL = 'users.User'` - Custom user model
- `REST_FRAMEWORK` - DRF configuration
- `SESSION_COOKIE_AGE` - Session duration
- `CORS_ALLOWED_ORIGINS` - CORS settings

### Security

Remember to:
- Set `SECRET_KEY` from environment variable in production
- Set `DEBUG = False` in production
- Configure `ALLOWED_HOSTS`
- Use HTTPS in production
- Set secure cookie settings

## Testing

Run tests:
```bash
python manage.py test
```

## Documentation

- **README.md** - This file, project overview
- **API_USAGE.md** - Complete API documentation with examples
- **TEMPLATES_GUIDE.md** - Guide for using and customizing templates
- **DEPLOYMENT.md** - Production deployment guide

## Web Interface Features

### Modern UI Templates
- **Responsive Design** - Works on mobile, tablet, and desktop
- **Bootstrap 5** - Modern component library
- **Font Awesome Icons** - Beautiful icons throughout
- **Gradient Backgrounds** - Eye-catching visual design
- **Interactive Forms** - Password strength, validation, toggles
- **Dashboard** - Statistics, activity feed, quick actions
- **Profile Management** - Tabbed interface for user settings

### Template Features
- Password visibility toggle
- Password strength indicator
- Real-time form validation
- Animated transitions
- Mobile-responsive navigation
- Alert messages
- Profile avatar display
- Progress charts

See **TEMPLATES_GUIDE.md** for detailed template documentation.

## License

MIT License
