from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from structure.models import Branch, Service, Master, Booking

# === Главная страница ===
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





# === Страница входа ===
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Неверный логин или пароль")
            return render(request, 'site/login.html')

    return render(request, 'site/login.html')


# === Выход из системы ===
def logout_view(request):
    logout(request)
    return redirect('home')


# === Страница создания записи (только для залогиненных) ===
@login_required
def bookings_page(request):
    branches = Branch.objects.all()
    services = Service.objects.all()
    masters = Master.objects.all()

    if request.method == "POST":
        branch_id = request.POST.get('branch')
        service_id = request.POST.get('service')
        master_id = request.POST.get('master')
        date = request.POST.get('date')
        time = request.POST.get('time')

        booking = Booking.objects.create(
            client=request.user,
            branch_id=branch_id,
            service_id=service_id,
            master_id=master_id,
            date=date,
            time=time
        )
        messages.success(request, "Запись создана успешно!")
        return redirect('my-bookings')

    context = {
        'branches': branches,
        'services': services,
        'masters': masters
    }
    return render(request, 'site/bookings.html', context)


# === Страница "Мои записи" (только для залогиненных) ===
@login_required
def my_bookings_page(request):
    bookings = Booking.objects.filter(client=request.user)
    context = {'bookings': bookings}
    return render(request, 'site/my_bookings.html', context)


# === Админка (только для админов) ===
def is_admin(user):
    return user.is_staff

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Доступ запрещен")
        return redirect('home')
    return render(request, 'site/admin_dashboard.html')