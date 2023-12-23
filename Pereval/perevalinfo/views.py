from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Users, PerevalAdded, Coords, DifficultyLevel, PerevalImages
from .serializer import PerevalAddedSerializer


class PerevalAddedCreate(generics.CreateAPIView):
    serializer_class = PerevalAddedSerializer
    permission_classes = [permissions.AllowAny]


#  post_a_job_serializer = PostAJobSerializer(data=request.data)
#  return Response(post_a_job_serializer.data, status=status.HTTP_201_CREATED)
#  return Response(post_a_job_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
