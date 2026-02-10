from django.urls import path
from .views import ClientRegisterView

urlpatterns = [
    path('register/', ClientRegisterView.as_view(), name='client-register'),
]
