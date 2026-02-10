from rest_framework import serializers
from .models import Client

class ClientRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # добавляем пароль

    class Meta:
        model = Client
        fields = ['id', 'name', 'phone', 'password']  # добавляем password

    def validate_phone(self, value):
        if Client.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Клиент с таким телефоном уже существует")
        return value

    def create(self, validated_data):
        # создаём пользователя через менеджер, чтобы пароль хэшировался
        return Client.objects.create_user(
            name=validated_data['name'],
            phone=validated_data.get('phone'),
            password=validated_data['password']
        )
