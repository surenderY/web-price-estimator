from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, UserUpdateForm
from .models import User
from .models import MasterSKUMapping, Country


def home_view(request):
    """
    Home page view
    """
    return render(request, 'home.html')


def login_view(request):
    """
    Login page view
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.email}!')
                
                # Redirect to next page or dashboard
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


def register_view(request):
    """
    Registration page view
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome aboard!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    """
    Logout view
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def dashboard_view(request):
    """
    Dashboard page view
    """
    return render(request, 'dashboard.html')


@login_required
def workorders_view(request):
    """
    Frontend view to list existing work orders.
    """
    return render(request, 'workorders.html')


@login_required
def price_estimator_view(request):
    """
    Frontend view for price estimator.
    """
    return render(request, 'price_estimator.html')


@login_required
def skus_management_view(request):
    """
    Page to manage SKUs per country.
    Shows all master SKUs on the left and SKUs associated with the selected country on the right.
    """
    # Get all master SKUs
    master_skus = MasterSKUMapping.objects.select_related('partner_mapping').all().order_by('master_sku_name')
    # Get list of countries
    countries = Country.objects.all().order_by('name')

    # default country: US if available
    default_code = 'US'
    selected_country = None
    try:
        selected_country = Country.objects.filter(code__iexact=default_code).first()
    except Exception:
        selected_country = countries.first() if countries.exists() else None

    context = {
        'master_skus': master_skus,
        'countries': countries,
        'selected_country': selected_country,
    }
    return render(request, 'skus_management.html', context)


# @login_required
# def profile_view(request):
#     """
#     User profile page view
#     """
#     if request.method == 'POST':
#         # Check if this is a password change request
#         if request.POST.get('action') == 'change_password':
#             old_password = request.POST.get('old_password')
#             new_password1 = request.POST.get('new_password1')
#             new_password2 = request.POST.get('new_password2')
            
#             # Validate old password
#             if not request.user.check_password(old_password):
#                 messages.error(request, 'Current password is incorrect.')
#             elif new_password1 != new_password2:
#                 messages.error(request, 'New passwords do not match.')
#             elif len(new_password1) < 8:
#                 messages.error(request, 'Password must be at least 8 characters long.')
#             else:
#                 # Change password
#                 request.user.set_password(new_password1)
#                 request.user.save()
#                 # Update session to prevent logout
#                 from django.contrib.auth import update_session_auth_hash
#                 update_session_auth_hash(request, request.user)
#                 messages.success(request, 'Password changed successfully!')
#                 return redirect('profile')
#         else:
#             # Handle profile update
#             form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
#             if form.is_valid():
#                 form.save()
#                 messages.success(request, 'Profile updated successfully!')
#                 return redirect('profile')
#     else:
#         form = UserUpdateForm(instance=request.user)
    
#     return render(request, 'profile.html', {'form': form})
