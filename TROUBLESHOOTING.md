# Troubleshooting Guide

This guide helps you resolve common issues with the Django project.

## Table of Contents
1. [URL/Routing Errors](#urlrouting-errors)
2. [Template Errors](#template-errors)
3. [Form Errors](#form-errors)
4. [Database Errors](#database-errors)
5. [Static Files Issues](#static-files-issues)
6. [Authentication Issues](#authentication-issues)

---

## URL/Routing Errors

### Error: `NoReverseMatch at /path/`

**Cause:** URL name doesn't exist or is misspelled.

**Solution:**
1. Check that the URL name exists in `urls.py`:
   ```python
   path('login/', login_view, name='login'),  # 'login' is the name
   ```

2. Use the correct name in templates:
   ```html
   <a href="{% url 'login' %}">Login</a>
   ```

3. If you get `'password_reset' is not a valid view`, it means that URL isn't defined yet. Either:
   - Remove the reference from the template
   - Or add the URL pattern

**Common Missing URLs:**
- `password_reset` - Add Django's built-in password reset URLs
- `password_change` - Already handled in profile view

### Error: `Page not found (404)`

**Cause:** URL pattern doesn't match.

**Solution:**
1. Check `config/urls.py` includes the app URLs:
   ```python
   path('', include('users.template_urls')),
   ```

2. Check `users/template_urls.py` has the pattern:
   ```python
   path('dashboard/', dashboard_view, name='dashboard'),
   ```

3. Make sure you're using the correct URL (no typos).

---

## Template Errors

### Error: `TemplateDoesNotExist at /path/`

**Cause:** Django can't find the template file.

**Solution:**
1. Verify template exists in `templates/` directory:
   ```
   templates/
   ├── base.html
   ├── login.html
   └── ...
   ```

2. Check `settings.py` has correct TEMPLATES configuration:
   ```python
   TEMPLATES = [
       {
           'DIRS': [BASE_DIR / 'templates'],
           ...
       },
   ]
   ```

3. Restart the development server after adding templates.

### Error: `Invalid block tag on line X: 'url'`

**Cause:** Template syntax error.

**Solution:**
1. Make sure you're using correct syntax:
   ```html
   {% url 'name' %}  <!-- Correct -->
   {{ url 'name' }}  <!-- Wrong -->
   ```

2. Check for missing `{% load static %}` if using static files.

---

## Form Errors

### Login Form Not Working

**Issue:** Can't login with correct credentials.

**Solution:**
1. Make sure the user exists:
   ```bash
   python manage.py createsuperuser
   ```

2. Check you're using email, not username:
   ```python
   # In login view, use email as username
   user = authenticate(username=email, password=password)
   ```

3. Verify `AUTH_USER_MODEL` in settings:
   ```python
   AUTH_USER_MODEL = 'users.User'
   ```

### Registration Form Errors

**Issue:** User registration failing.

**Solution:**
1. Check password validators in `settings.py`
2. Ensure passwords match
3. Verify email is unique
4. Check form errors in template:
   ```html
   {% if form.errors %}
       {{ form.errors }}
   {% endif %}
   ```

### CSRF Verification Failed

**Issue:** Form submission returns CSRF error.

**Solution:**
1. Add CSRF token to all POST forms:
   ```html
   <form method="post">
       {% csrf_token %}
       ...
   </form>
   ```

2. Check `MIDDLEWARE` includes CSRF:
   ```python
   'django.middleware.csrf.CsrfViewMiddleware',
   ```

3. For AJAX requests, include CSRF token in headers.

---

## Database Errors

### Error: `no such table: users_user`

**Cause:** Migrations haven't been run.

**Solution:**
```bash
python manage.py makemigrations
python manage.py migrate
```

### Error: `(1146, "Table 'db.users_user' doesn't exist")`

**Cause:** Custom user model not migrated.

**Solution:**
1. Delete existing migrations (except `__init__.py`):
   ```bash
   rm users/migrations/0*.py
   ```

2. Delete database:
   ```bash
   rm db.sqlite3
   ```

3. Run migrations again:
   ```bash
   python manage.py makemigrations users
   python manage.py migrate
   ```

### Error: `UNIQUE constraint failed`

**Cause:** Trying to create duplicate record (usually email).

**Solution:**
- Use different email address
- Or delete the existing user from admin panel

---

## Static Files Issues

### CSS/JS Not Loading

**Issue:** Styles or scripts not appearing on page.

**Solution:**
1. Check templates load static files:
   ```html
   {% load static %}
   <link rel="stylesheet" href="{% static 'css/style.css' %}">
   ```

2. Run collectstatic:
   ```bash
   python manage.py collectstatic
   ```

3. In development, make sure `DEBUG = True` in settings.

4. Check `STATIC_URL` and `STATIC_ROOT` in settings:
   ```python
   STATIC_URL = '/static/'
   STATIC_ROOT = BASE_DIR / 'staticfiles'
   ```

### Bootstrap/Font Awesome Not Working

**Issue:** Using CDN links but no internet connection.

**Solution:**
1. Download files locally
2. Place in `static/` directory
3. Update template links:
   ```html
   <link href="{% static 'css/bootstrap.min.css' %}" rel="stylesheet">
   ```

---

## Authentication Issues

### Can't Access Dashboard (Redirects to Login)

**Cause:** User not authenticated.

**Solution:**
1. Make sure you logged in successfully
2. Check `@login_required` decorator on view
3. Verify `LOGIN_URL` in settings:
   ```python
   LOGIN_URL = 'login'
   ```

### Session Expires Immediately

**Cause:** Session configuration issue.

**Solution:**
1. Check session settings:
   ```python
   SESSION_COOKIE_AGE = 1209600  # 2 weeks
   SESSION_SAVE_EVERY_REQUEST = False
   ```

2. Clear browser cookies
3. Restart development server

### Password Not Working After Change

**Cause:** Session not updated after password change.

**Solution:**
Already handled in profile view:
```python
from django.contrib.auth import update_session_auth_hash
update_session_auth_hash(request, request.user)
```

---

## Import Errors

### Error: `ImportError: cannot import name 'X'`

**Cause:** Missing or incorrect import.

**Solution:**
1. Check the import path:
   ```python
   from users.models import User  # Correct
   from models import User  # Wrong
   ```

2. Make sure `__init__.py` exists in directories
3. Restart development server

### Error: `ModuleNotFoundError: No module named 'rest_framework'`

**Cause:** Package not installed.

**Solution:**
```bash
pip install -r requirements.txt
```

---

## Quick Fixes

### Reset Everything

If nothing works, reset the project:

```bash
# 1. Delete database
rm db.sqlite3

# 2. Delete migrations
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# 3. Recreate migrations
python manage.py makemigrations
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser

# 5. Restart server
python manage.py runserver
```

### Check Django Installation

```bash
python -c "import django; print(django.get_version())"
```

Should show: 4.2.x or higher

### Verify Project Structure

```bash
tree -I 'venv|__pycache__|*.pyc' -L 2
```

Should show:
```
.
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/
│   ├── models.py
│   ├── views.py
│   ├── template_views.py
│   └── ...
├── templates/
│   ├── base.html
│   └── ...
├── manage.py
└── requirements.txt
```

---

## Getting Help

### Enable Debug Mode

In `settings.py`:
```python
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

### Check Logs

View Django logs in terminal where server is running.

### Django Shell

Test components in Django shell:
```bash
python manage.py shell
```

```python
# Test user creation
from users.models import User
user = User.objects.create_user(email='test@test.com', password='test123')
print(user)

# Test authentication
from django.contrib.auth import authenticate
user = authenticate(username='test@test.com', password='test123')
print(user)
```

### Common Commands

```bash
# Check for issues
python manage.py check

# Show migrations status
python manage.py showmigrations

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Start fresh shell
python manage.py shell
```

---

## Still Having Issues?

1. Check Django documentation: https://docs.djangoproject.com/
2. Search error message on Stack Overflow
3. Review project files for typos
4. Make sure all files are saved
5. Restart the development server
6. Clear browser cache and cookies
7. Try a different browser

## Prevention Tips

1. **Always run migrations** after model changes
2. **Use version control** (git) to track changes
3. **Keep backups** of your database
4. **Test incrementally** - don't change too much at once
5. **Read error messages carefully** - they usually tell you what's wrong
6. **Check Django docs** when trying new features
