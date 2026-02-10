from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ServiceViewSet,
    MasterViewSet,
    BookingViewSet,
    BranchViewSet,
    AdministratorViewSet,
    ClientRegisterView,
)
from django.views.generic import TemplateView

from .views import admin_dashboard
from django.contrib.auth import views as auth_views


# ------------------ API ------------------
router = DefaultRouter()
router.register(r'branches', BranchViewSet)
router.register(r'administrators', AdministratorViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'masters', MasterViewSet)
router.register(r'bookings', BookingViewSet)

# ------------------ HTML шаблоны ------------------
urlpatterns = [
    # API
    path('api/', include(router.urls)),
    path('api/clients/register/', ClientRegisterView.as_view(), name='client-register'),

    # Шаблоны
    path('', TemplateView.as_view(template_name='site/home.html'), name='home'),
    path('site/register/', TemplateView.as_view(template_name='site/register.html'), name='client-register'),
    path('site/login/', auth_views.LoginView.as_view(template_name='site/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('site/bookings/', TemplateView.as_view(template_name='site/bookings.html'), name='create-booking'),
    path('site/my-bookings/', TemplateView.as_view(template_name='site/my_bookings.html'), name='my-bookings'),

    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
]
