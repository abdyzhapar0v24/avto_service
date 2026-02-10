from rest_framework import serializers, viewsets
from .models import Service, Master, Booking, Branch, Administrator
from datetime import datetime, timedelta
from client.models import Client



class BranchSerializer(serializers.ModelSerializer):
   class Meta:
       model = Branch
       fields = '__all__'

class AdministratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrator
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = '__all__'
        extra_kwargs = { 'photo': {'required': False}
        }

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

        def validate(self, data):
            client = self.context['request'].user  # берем клиента из request
            if not client.is_authenticated:
                raise serializers.ValidationError("Вы должны быть зарегистрированы")
            data['client'] = client

    def validate(self, data):
        master = data['master']
        service = data['service']
        date = data['date']
        time = data['time']
        branch = data['branch']

        # 1️⃣ Проверка филиала мастера
        if master.branch != branch:
            raise serializers.ValidationError(
                "Мастер не работает в этом филиале"
            )

        # 2️⃣ Проверка выходного дня
        weekday = date.strftime("%a").lower()  # 'mon', 'tue', ...
        weekend_days = master.weekend_days.lower().split(',')  # ['sat','sun']
        if weekday in weekend_days:
            raise serializers.ValidationError(
                "Мастер не работает в этот день"
            )

        # 3️⃣ Проверка занятости мастера
        start = datetime.combine(date, time)
        end = start + timedelta(minutes=service.duration)

        bookings = Booking.objects.filter(
            master=master,
            date=date,
            status__in=['new', 'confirmed']
        )

        for booking in bookings:
            booked_start = datetime.combine(booking.date, booking.time)
            booked_end = booked_start + timedelta(minutes=booking.service.duration)
            if start < booked_end and end > booked_start:
                raise serializers.ValidationError(
                    "Мастер занят на выбранное время"
                )

        return data
