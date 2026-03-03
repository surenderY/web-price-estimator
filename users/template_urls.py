from django.urls import path
from .template_views import (
    home_view,
    login_view,
    register_view,
    logout_view,
    dashboard_view,
    # workorders view
    workorders_view,
    price_estimator_view,
    skus_management_view
    # profile_view
)

urlpatterns = [
    # Template-based views
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('workorders/', workorders_view, name='workorders'),
    path('price-estimator/', price_estimator_view, name='price-estimator'),
    path('skus-management/', skus_management_view, name='skus-management'),
    # path('profile/', profile_view, name='profile'),
]
