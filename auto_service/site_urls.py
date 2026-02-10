from django.urls import path
from . import site_views

urlpatterns = [
    path('', site_views.home, name='home'),  # главная страница
    path('site/login/', site_views.login_page, name='login'),  # логин
    path('site/register/', site_views.register_page, name='register'),  # регистрация
    path('site/bookings/', site_views.bookings_page, name='create-booking'),  # создать запись
    path('site/my-bookings/', site_views.my_bookings_page, name='my-bookings'),  # мои записи
]
