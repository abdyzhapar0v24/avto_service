from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class ClientManager(BaseUserManager):
    def create_user(self, name, password=None, phone=None):  # добавили phone
        if not name:
            raise ValueError('Имя обязательно')

        user = self.model(
            name=name,
            phone=phone  # сохраняем телефон
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password):
        user = self.create_user(name=name, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Client(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)  # добавляем phone

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = ClientManager()

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []  # ❗ пусто, чтобы суперпользователь не спрашивал phone

    def __str__(self):
        return self.name
