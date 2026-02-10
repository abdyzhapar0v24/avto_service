from rest_framework import viewsets,generics
from .models import Service, Branch
from .serializers import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from client.serializers import ClientRegisterSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

from django.contrib.auth import logout
from django.shortcuts import redirect


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class AdministratorViewSet(viewsets.ModelViewSet):
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer



class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['branch', 'name']

    # ПОИСК
    search_fields = ['name', 'description']

    # СОРТИРОВКА
    ordering_fields = ['price', 'name']




class MasterViewSet(viewsets.ModelViewSet):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]


    filterset_fields = ['branch', 'services', 'experience']

    # ПОИСК
    search_fields = ['name', 'specialization']

    # СОРТИРОВКА
    ordering_fields = ['experience', 'name']

class ClientRegisterView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientRegisterSerializer



class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()  # ← это нужно обязательно
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # администратор
            return Booking.objects.all()
        return Booking.objects.filter(client=user)  # клиент видит только свои записи

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)  # автоматически привязываем запись к клиенту


# Проверка, что пользователь админ
def is_admin(user):
    return user.is_staff  # или is_superuser, если так назначены админы

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'site/admin_dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('home')  # после выхода редирект на главную