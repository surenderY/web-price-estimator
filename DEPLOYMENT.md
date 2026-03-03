# Deployment Guide

This guide covers deploying your Django REST Framework application to production.

## Pre-Deployment Checklist

### 1. Security Settings

Update `config/settings.py`:

```python
# Must be set from environment variable
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable must be set")

# Turn off debug mode
DEBUG = False

# Set allowed hosts
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# HTTPS settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### 2. Database Configuration

Use PostgreSQL in production:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

### 3. Static Files

Configure static file serving:

```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Use WhiteNoise for serving static files
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... rest of middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

Install WhiteNoise:
```bash
pip install whitenoise
```

### 4. Environment Variables

Create a `.env` file (never commit this):

```env
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
```

### 5. Requirements

Generate production requirements:

```bash
pip freeze > requirements.txt
```

## Deployment Options

### Option 1: Deploy to Heroku

1. **Install Heroku CLI**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Create Heroku app**
```bash
heroku create your-app-name
```

3. **Add PostgreSQL addon**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. **Set environment variables**
```bash
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set DEBUG=False
```

5. **Create Procfile**
```
web: gunicorn config.wsgi --log-file -
release: python manage.py migrate
```

6. **Install Gunicorn**
```bash
pip install gunicorn
pip freeze > requirements.txt
```

7. **Deploy**
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

8. **Create superuser**
```bash
heroku run python manage.py createsuperuser
```

### Option 2: Deploy to DigitalOcean/AWS/VPS

#### Server Setup (Ubuntu 22.04)

1. **Update system**
```bash
sudo apt update
sudo apt upgrade -y
```

2. **Install dependencies**
```bash
sudo apt install python3-pip python3-venv postgresql nginx -y
```

3. **Setup PostgreSQL**
```bash
sudo -u postgres psql
CREATE DATABASE yourdb;
CREATE USER youruser WITH PASSWORD 'yourpassword';
ALTER ROLE youruser SET client_encoding TO 'utf8';
ALTER ROLE youruser SET default_transaction_isolation TO 'read committed';
ALTER ROLE youruser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE yourdb TO youruser;
\q
```

4. **Clone your repository**
```bash
cd /var/www
sudo git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

5. **Setup virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

6. **Configure environment variables**
```bash
sudo nano /etc/environment
# Add your environment variables
```

7. **Run migrations**
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

8. **Setup Gunicorn service**
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/your-repo
Environment="PATH=/var/www/your-repo/venv/bin"
ExecStart=/var/www/your-repo/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/your-repo/gunicorn.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

9. **Start Gunicorn**
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

10. **Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/your-app
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/your-repo;
    }
    
    location /media/ {
        root /var/www/your-repo;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/your-repo/gunicorn.sock;
    }
}
```

11. **Enable site**
```bash
sudo ln -s /etc/nginx/sites-available/your-app /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

12. **Setup SSL with Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Option 3: Deploy with Docker

1. **Create Dockerfile**
```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

2. **Create docker-compose.yml**
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=yourdb
      - POSTGRES_USER=youruser
      - POSTGRES_PASSWORD=yourpassword

  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

3. **Build and run**
```bash
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## Post-Deployment

### Monitoring

1. **Setup logging**
   - Use services like Sentry, Papertrail, or Loggly
   - Configure Django logging in settings.py

2. **Setup monitoring**
   - Use New Relic, Datadog, or similar
   - Monitor server resources (CPU, memory, disk)

3. **Setup backups**
   - Regular database backups
   - Backup media files
   - Store backups off-site

### Maintenance

1. **Update dependencies regularly**
```bash
pip list --outdated
pip install --upgrade package-name
```

2. **Monitor logs**
```bash
# For systemd services
sudo journalctl -u gunicorn -f

# For Docker
docker-compose logs -f web
```

3. **Database maintenance**
```bash
# Vacuum database
python manage.py dbshell
VACUUM ANALYZE;
```

## Performance Optimization

1. **Use caching**
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

2. **Database optimization**
   - Add database indexes
   - Use select_related() and prefetch_related()
   - Enable connection pooling

3. **Use CDN for static files**
   - Configure AWS S3 or CloudFront
   - Update STATIC_URL in settings

## Troubleshooting

### Common Issues

1. **502 Bad Gateway**
   - Check Gunicorn is running: `sudo systemctl status gunicorn`
   - Check socket file permissions
   - Check Nginx error logs: `sudo tail -f /var/log/nginx/error.log`

2. **Static files not loading**
   - Run `python manage.py collectstatic`
   - Check STATIC_ROOT and STATIC_URL settings
   - Verify Nginx configuration

3. **Database connection errors**
   - Verify database credentials
   - Check database is running
   - Verify network connectivity

4. **Permission errors**
   - Check file ownership: `sudo chown -R www-data:www-data /var/www/your-repo`
   - Check file permissions: `sudo chmod -R 755 /var/www/your-repo`
