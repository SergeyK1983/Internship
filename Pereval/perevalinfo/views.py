from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Users, PerevalAdded, Coords, DifficultyLevel, PerevalImages
from .serializer import PerevalAddedSerializer


class PerevalAddedCreate(generics.CreateAPIView):
    serializer_class = PerevalAddedSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PerevalAddedSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif status.HTTP_400_BAD_REQUEST:
            return Response(serializer.errors, status={'status': status.HTTP_400_BAD_REQUEST, 'message': 'Плохой запрос BAD_REQUEST'})
        else:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
