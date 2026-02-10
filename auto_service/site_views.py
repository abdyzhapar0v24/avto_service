from django.shortcuts import render, redirect
from structure.models import Branch, Service, Master
from django.contrib.auth.decorators import login_required

# Главная страница
def home(request):
    branches = Branch.objects.all()
    services = Service.objects.all()
    masters = Master.objects.all()
    context = {
        'branches': branches,
        'services': services,
        'masters': masters,
    }
    return render(request, 'site/home.html', context)

# Страница логина
def login_page(request):
    return render(request, 'site/login.html')

# Страница регистрации
def register_page(request):
    return render(request, 'site/register.html')

# Страница записи (только для залогиненных)
@login_required
def bookings_page(request):
    return render(request, 'site/bookings.html')

# Страница "Мои записи" (только для залогиненных)
@login_required
def my_bookings_page(request):
    return render(request, 'site/my_bookings.html')
