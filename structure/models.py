from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from client.models import Client
from django.conf import settings



class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Administrator(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='administrators'
    )

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)  # Название услуги
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Цена за приём
    description = models.TextField(blank=True)  # Описание услуги (опционально)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Master(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField()
    weekend_days = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    services = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='masters')
    def __str__(self):
        return self.name



class Booking(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('confirmed', 'Подтверждена'),
        ('canceled', 'Отменена'),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.name} у {self.master.name} в {self.date} {self.time}"
