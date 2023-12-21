from django.urls import path

from .views import PerevalAddedCreate

urlpatterns = [
    path('v1/create/', PerevalAddedCreate.as_view(), name='pereval-create'),
]

