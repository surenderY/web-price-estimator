from django.urls import path
from .views import (
    CountryListView,
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    CurrentUserView,
    ChangePasswordView,
    UserListView,
    UserDetailView,
    CountrySKUView,
    CountrySKUManageView,
    WorkOrderListCreateView,
    WorkOrderDetailView,
    WorkOrderPriceEstimateDownloadView,
    WorkOrderPriceEstimateView,
    WorkOrderPriceEstimateListView,
)

app_name = 'users'

urlpatterns = [
    # Authentication endpoints
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    
    # Current user endpoints
    path('user/', CurrentUserView.as_view(), name='current-user'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    
    # Admin endpoints
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    # Countries list for frontend
    path('countries/', CountryListView.as_view(), name='country-list'),
    path('countries/<str:code>/skus/', CountrySKUView.as_view(), name='country-skus'),
    path('countries/<str:code>/skus/manage/', CountrySKUManageView.as_view(), name='country-skus-manage'),
    path('workorders/', WorkOrderListCreateView.as_view(), name='workorder-list-create'),
    path('workorders/<int:pk>/', WorkOrderDetailView.as_view(), name='workorder-detail'),
    path('workorders/<int:pk>/price-estimate/', WorkOrderPriceEstimateView.as_view(), name='workorder-price-estimate'),
    path('workorders/price-estimate/download/', WorkOrderPriceEstimateDownloadView.as_view(), name='workorder-price-estimate-download'),
    path('workorders/price-estimate/list/', WorkOrderPriceEstimateListView.as_view(), name='workorder-price-estimate-list'),
]
