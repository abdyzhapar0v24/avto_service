from django.shortcuts import render
from rest_framework import generics
from .models import Client
from .serializers import ClientRegisterSerializer

class ClientRegisterView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientRegisterSerializer



# Create your views here.
