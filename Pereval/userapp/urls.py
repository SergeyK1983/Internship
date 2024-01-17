from django.urls import path
from .views import user_create_pereval


urlpatterns = [
    path('create/', user_create_pereval, name='create-pereval'),
]

