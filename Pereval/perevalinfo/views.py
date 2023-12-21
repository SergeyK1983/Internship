from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Users, PerevalAdded, Coords, DifficultyLevel, PerevalImages
from .serializer import PerevalAddedSerializer


class PerevalAddedCreate(generics.CreateAPIView):
    serializer_class = PerevalAddedSerializer
    permission_classes = [permissions.AllowAny]

