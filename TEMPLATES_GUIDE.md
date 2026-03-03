# Django Templates Guide

This guide explains how to use the Django templates included in this project.

## Overview

The project includes modern, responsive templates for:
- **Home Page** - Landing page with hero section and features
- **Login Page** - User authentication with password toggle
- **Registration Page** - New user signup with validation
- **Dashboard** - User dashboard with statistics and activity
- **Profile** - User profile management with tabs

## Template Structure

### Base Template
All templates extend `base.html` which provides:
- Responsive navigation bar
- Bootstrap 5 styling
- Font Awesome icons
- Custom CSS variables
- Message notifications
- Footer

### Template Hierarchy

```
base.html
├── home.html          (Landing page)
├── login.html         (User login)
├── register.html      (User registration)
├── dashboard.html     (User dashboard)
└── profile.html       (User profile)
```

## URL Routes

The following URL routes are configured:

| URL | View | Template | Description |
|-----|------|----------|-------------|
| `/` | `home_view` | `home.html` | Home/landing page |
| `/login/` | `login_view` | `login.html` | User login |
| `/register/` | `register_view` | `register.html` | User registration |
| `/logout/` | `logout_view` | - | Logout (redirects) |
| `/dashboard/` | `dashboard_view` | `dashboard.html` | User dashboard |
| `/profile/` | `profile_view` | `profile.html` | User profile |

## Setup Instructions

### 1. Verify Directory Structure

Ensure your templates directory exists:
```
django_project/
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── profile.html
```

### 2. Settings Configuration

The `config/settings.py` is already configured with:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Points to templates directory
        'APP_DIRS': True,
        ...
    },
]
```

### 3. URL Configuration

The main `config/urls.py` includes template URLs:

```python
urlpatterns = [
    path('', include('users.template_urls')),  # Template-based views
    path('api/auth/', include('users.urls')),  # API endpoints
    ...
]
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Static Files Directory

```bash
python manage.py collectstatic --noinput
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

Visit http://localhost:8000 to see the home page.

## Template Features

### Home Page (`home.html`)
- Hero section with gradient background
- Feature cards with icons
- Call-to-action section
- Responsive design
- Animation effects

**Usage:**
```python
# View automatically renders home.html
def home_view(request):
    return render(request, 'home.html')
```

### Login Page (`login.html`)
- Email and password fields
- Password toggle (show/hide)
- Remember me checkbox
- Forgot password link
- Social login buttons (optional)
- Form validation
- Error messages

**Features:**
- Password visibility toggle
- Client-side validation
- CSRF protection
- "Remember me" functionality

### Registration Page (`register.html`)
- First name and last name fields
- Email field with validation
- Password strength indicator
- Password confirmation
- Terms & conditions checkbox
- Real-time validation

**Features:**
- Password strength meter (weak/medium/strong)
- Password match validation
- Duplicate email detection
- Visual feedback

### Dashboard Page (`dashboard.html`)
- Welcome section with user name
- Statistics cards (tasks, completed, pending, progress)
- Recent activity timeline
- Quick action buttons
- Progress charts
- Responsive grid layout

**Customization:**
```html
<!-- Update statistics in dashboard.html -->
<div class="stat-value">{{ total_tasks }}</div>
<div class="stat-label">Total Tasks</div>
```

### Profile Page (`profile.html`)
- Profile header with avatar
- Tabbed interface (Overview, Edit, Security)
- Profile information display
- Profile editing form
- Password change form
- Account statistics
- Quick links sidebar

**Features:**
- Three tabs: Overview, Edit Profile, Security
- Avatar display (or initials)
- File upload for profile picture
- Real-time profile updates

## Customization

### Change Colors

Edit the CSS variables in `base.html`:

```css
:root {
    --primary-color: #4f46e5;      /* Main brand color */
    --secondary-color: #7c3aed;    /* Secondary color */
    --success-color: #10b981;      /* Success messages */
    --danger-color: #ef4444;       /* Error messages */
    --dark-color: #1f2937;         /* Dark text */
    --light-color: #f9fafb;        /* Light background */
}
```

### Update Navigation

Edit the navigation in `base.html`:

```html
<ul class="navbar-nav ms-auto">
    {% if user.is_authenticated %}
        <li class="nav-item">
            <a class="nav-link" href="{% url 'your_new_page' %}">
                <i class="fas fa-icon"></i> New Link
            </a>
        </li>
    {% endif %}
</ul>
```

### Add New Template

1. Create new template file in `templates/` directory
2. Create corresponding view in `users/template_views.py`
3. Add URL pattern in `users/template_urls.py`

Example:
```python
# users/template_views.py
@login_required
def settings_view(request):
    return render(request, 'settings.html')

# users/template_urls.py
path('settings/', settings_view, name='settings'),
```

### Customize Messages

Django messages are displayed automatically. Add custom messages:

```python
from django.contrib import messages

# Success message
messages.success(request, 'Operation completed successfully!')

# Error message
messages.error(request, 'Something went wrong.')

# Warning message
messages.warning(request, 'Please be careful.')

# Info message
messages.info(request, 'Here is some information.')
```

## Form Handling

### Login Form

The login form uses Django's built-in `AuthenticationForm`:

```python
if request.method == 'POST':
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
```

### Registration Form

Custom registration form with email as username:

```python
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
```

### Profile Update Form

```python
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'bio', 
                  'birth_date', 'profile_picture']
```

## JavaScript Features

### Password Toggle
```javascript
// Toggles password visibility
const toggle = document.getElementById('togglePassword');
toggle.addEventListener('click', function() {
    const type = password.type === 'password' ? 'text' : 'password';
    password.type = type;
    this.classList.toggle('fa-eye');
    this.classList.toggle('fa-eye-slash');
});
```

### Password Strength Indicator
```javascript
// Shows password strength (weak/medium/strong)
passwordInput.addEventListener('input', function() {
    const password = this.value;
    let strength = calculateStrength(password);
    updateStrengthBar(strength);
});
```

## Responsive Design

All templates are fully responsive:
- **Mobile** (< 768px): Single column layout
- **Tablet** (768px - 1024px): Two column layout
- **Desktop** (> 1024px): Multi-column layout

## Icons

Templates use Font Awesome 6 icons:
```html
<i class="fas fa-user"></i>      <!-- User icon -->
<i class="fas fa-lock"></i>      <!-- Lock icon -->
<i class="fas fa-envelope"></i>  <!-- Email icon -->
```

Browse all icons at: https://fontawesome.com/icons

## Bootstrap Components

Templates use Bootstrap 5 components:
- Cards
- Forms
- Buttons
- Navigation
- Alerts
- Progress bars
- Tabs

Documentation: https://getbootstrap.com/docs/5.3/

## Security Features

- CSRF protection on all forms
- Password strength validation
- Secure session handling
- Login required decorators
- XSS protection (automatic escaping)

## Troubleshooting

### Templates Not Found
Ensure `TEMPLATES['DIRS']` in settings includes your templates directory:
```python
'DIRS': [BASE_DIR / 'templates'],
```

### Static Files Not Loading
Run:
```bash
python manage.py collectstatic
```

### Forms Not Submitting
Check:
1. CSRF token is present: `{% csrf_token %}`
2. Form method is POST: `<form method="post">`
3. Form action URL is correct

### User Not Redirecting After Login
Check `LOGIN_REDIRECT_URL` in settings:
```python
LOGIN_REDIRECT_URL = 'dashboard'
```

## Next Steps

1. **Customize Templates**: Update colors, fonts, and layouts
2. **Add More Pages**: Create additional templates for your app
3. **Connect to Database**: Display real data in dashboard
4. **Add Features**: Implement task management, file uploads, etc.
5. **Deploy**: Follow DEPLOYMENT.md for production deployment

## Support

For issues or questions:
1. Check Django documentation: https://docs.djangoproject.com/
2. Review Bootstrap docs: https://getbootstrap.com/
3. Check the API_USAGE.md for API endpoints
