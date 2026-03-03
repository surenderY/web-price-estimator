#!/bin/bash

# Django Project Quick Start Script
# This script sets up and runs your Django project

echo "🚀 Django Project Quick Start"
echo "=============================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "📁 Creating necessary directories..."
mkdir -p media/profile_pics
mkdir -p staticfiles
mkdir -p logs
echo "✓ Directories created"

# Run migrations
echo ""
echo "🗄️  Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo ""
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser prompt
echo ""
echo "👤 Do you want to create a superuser? (y/n)"
read -r create_superuser

if [ "$create_superuser" = "y" ]; then
    python manage.py createsuperuser
fi

# Run the server
echo ""
echo "🎉 Setup complete!"
echo ""
echo "Starting development server..."
echo "Visit http://localhost:8000 in your browser"
echo ""
echo "Available URLs:"
echo "  - Home: http://localhost:8000/"
echo "  - Login: http://localhost:8000/login/"
echo "  - Register: http://localhost:8000/register/"
echo "  - Dashboard: http://localhost:8000/dashboard/"
echo "  - Admin: http://localhost:8000/admin/"
echo "  - API: http://localhost:8000/api/auth/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver
